#!/usr/bin/env python3
"""Seeded heuristic search; unsuccessful search is never an upper-bound proof.

One candidate evaluation means one full initial/restart objective evaluation,
or one incremental objective evaluation of a proposed single-edge flip,
including rejected proposals. Building constraints, accepting a proposal,
serializing certificates and verifier calls are not candidate evaluations.
"""
import argparse
from datetime import datetime, timezone
import itertools
import json
import math
from pathlib import Path
import platform
import random
import time


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def constraints(n):
    edges = list(itertools.combinations(range(n), 2))
    index = {e: i for i, e in enumerate(edges)}
    groups, targets = [], []
    incidence = [[] for _ in edges]
    for size, target in ((3, 3), (5, 0)):
        for vertices in itertools.combinations(range(n), size):
            group = [index[e] for e in itertools.combinations(vertices, 2)]
            k = len(groups)
            groups.append(group)
            targets.append(target)
            for e in group:
                incidence[e].append(k)
    return edges, groups, targets, incidence


def run(args):
    started = time.monotonic()
    rng = random.Random(args.seed)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'certificates').mkdir(exist_ok=True)
    report = {
        'algorithm': 'conflict-guided single-edge simulated annealing',
        'seed': args.seed, 'max_evaluations': args.max_evaluations,
        'seconds_limit': args.seconds, 'restart_interval': args.restart_interval,
        'candidate_definition': __doc__.split('\n\n')[1].strip(),
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'platform': platform.platform(),
        'stages': [],
    }
    evaluations = 0
    n = 5
    best_certificate = None
    stop = None
    while stop is None:
        edges, groups, targets, incidence = constraints(n)
        stage = {'n': n, 'evaluations': 0, 'restarts': 0,
                 'best_score': None, 'solved': False}
        report['stages'].append(stage)
        stage_started = time.monotonic()
        counts = None
        steps = 0
        while True:
            if evaluations >= args.max_evaluations:
                stop = 'CANDIDATE_LIMIT'
                break
            if time.monotonic() - started >= args.seconds:
                stop = 'TIME_LIMIT'
                break
            if counts is None or steps >= args.restart_interval:
                # Generic random graph: no imported or remembered construction.
                bits = [int(rng.random() < 0.35) for _ in edges]
                counts = [sum(bits[e] for e in group) for group in groups]
                bad = {k for k, count in enumerate(counts) if count == targets[k]}
                score = len(bad)
                stage['restarts'] += 1
                steps = 0
            else:
                if bad and rng.random() < 0.9:
                    group = groups[rng.choice(sorted(bad))]
                    e = rng.choice(group)
                else:
                    e = rng.randrange(len(edges))
                change = 1 - 2 * bits[e]
                affected = incidence[e]
                delta = sum((counts[k] + change == targets[k]) -
                            (counts[k] == targets[k]) for k in affected)
                # A heuristic acceptance rule; no uniform-sampling claim.
                temperature = 1.5 * (0.05 / 1.5) ** (steps / args.restart_interval)
                if delta <= 0 or rng.random() < math.exp(-delta / temperature):
                    bits[e] ^= 1
                    score += delta
                    for k in affected:
                        counts[k] += change
                        if counts[k] == targets[k]:
                            bad.add(k)
                        else:
                            bad.discard(k)
                steps += 1
            evaluations += 1
            stage['evaluations'] += 1
            if stage['best_score'] is None or score < stage['best_score']:
                stage['best_score'] = score
            if score == 0:
                # Independent full objective recount protects incremental updates.
                assert all(sum(bits[e] for e in group) != target
                           for group, target in zip(groups, targets))
                best_certificate = {'n': n, 'edges': [list(e) for e, b in zip(edges, bits) if b]}
                write_json(out / 'certificates' / ('n%02d.json' % n), best_certificate)
                write_json(out / 'certificate.json', best_certificate)
                stage['solved'] = True
                stage['found_at_evaluation'] = evaluations
                print(json.dumps({'found_n': n, 'evaluations': evaluations,
                                  'elapsed_seconds': time.monotonic() - started}), flush=True)
                break
            if evaluations % 100000 == 0:
                print(json.dumps({'searching_n': n, 'evaluations': evaluations,
                                  'best_score': stage['best_score'],
                                  'elapsed_seconds': time.monotonic() - started}), flush=True)
        stage['elapsed_seconds'] = time.monotonic() - stage_started
        report.update(evaluations=evaluations, best_n=best_certificate['n'] if best_certificate else None,
                      elapsed_seconds=time.monotonic() - started, stop_reason=stop)
        write_json(out / 'search-result.json', report)
        n += 1
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    report['search_stop_classification'] = 'EXHAUSTED_BUDGET'
    write_json(out / 'search-result.json', report)
    print(json.dumps({k: report[k] for k in ('evaluations', 'best_n', 'elapsed_seconds', 'stop_reason')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=35001)
    parser.add_argument('--max-evaluations', type=int, default=5000000)
    parser.add_argument('--seconds', type=float, default=1200)
    parser.add_argument('--restart-interval', type=int, default=10000)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.max_evaluations < 1 or args.seconds <= 0 or args.restart_interval < 1:
        parser.error('budgets and restart interval must be positive')
    run(args)
