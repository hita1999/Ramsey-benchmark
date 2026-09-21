#!/usr/bin/env python3
"""Generic increasing-order annealing, no known construction or vertex horizon.

One candidate evaluation = one initial graph full score OR one proposed
single-edge-flip score (whether accepted or rejected). No verifier is imported.
"""
import argparse
from datetime import datetime, timezone
from itertools import combinations
import json
import math
from pathlib import Path
import random
import time


def setup(n):
    pairs = list(combinations(range(n), 2))
    index = {pair: i for i, pair in enumerate(pairs)}
    quads = [tuple(index[p] for p in combinations(q, 2))
             for q in combinations(range(n), 4)]
    affected = [[] for _ in pairs]
    for i, quad in enumerate(quads):
        for e in quad:
            affected[e].append(i)
    return pairs, quads, affected


def initial_score(bits, quads):
    counts = [sum(bits[e] for e in q) for q in quads]
    return counts, sum(c == 0 or c == 6 for c in counts)


def flip_delta(bit, indices, counts):
    # Adding: 0->1 removes an independent set, 5->6 creates a clique.
    # Removing: 6->5 removes a clique, 1->0 creates an independent set.
    remove, create = (6, 1) if bit else (0, 5)
    delta = 0
    for q in indices:
        c = counts[q]
        delta += (c == create) - (c == remove)
    return delta


def run(args):
    start = time.monotonic()
    utc_start = datetime.now(timezone.utc).isoformat()
    rng = random.Random(args.seed)
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    (output / 'certificates').mkdir()
    evaluated = 0
    n = 4
    best_n = None
    restart = 0
    best_score = None
    pairs, quads, affected = setup(n)
    config = dict(seed=args.seed, max_evaluations=args.max_evaluations,
                  seconds=args.seconds, restart_steps=args.restart_steps,
                  initial_temperature=1.5, final_temperature=0.05,
                  start_n=4, vertex_horizon=None,
                  evaluation_definition='initial full graph score or proposed single-edge-flip score',
                  utc_start=utc_start)
    (output / 'search-config.json').write_text(json.dumps(config, indent=2)+'\n')
    with (output / 'search-progress.jsonl').open('w') as log:
        def emit(event, **fields):
            record = dict(event=event, evaluations=evaluated, n=n,
                          elapsed_seconds=time.monotonic()-start, **fields)
            log.write(json.dumps(record, sort_keys=True)+'\n')
            log.flush()
            print(json.dumps(record, sort_keys=True), flush=True)

        while evaluated < args.max_evaluations and time.monotonic()-start < args.seconds:
            bits = [rng.randrange(2) for _ in pairs]
            counts, score = initial_score(bits, quads)
            evaluated += 1
            restart += 1
            best_score = score if best_score is None else min(best_score, score)
            for step in range(args.restart_steps):
                if score == 0:
                    break
                if evaluated >= args.max_evaluations or time.monotonic()-start >= args.seconds:
                    break
                edge = rng.randrange(len(pairs))
                delta = flip_delta(bits[edge], affected[edge], counts)
                evaluated += 1
                temperature = 1.5 * (0.05/1.5)**(step / max(1, args.restart_steps-1))
                if delta <= 0 or rng.random() < math.exp(-delta / temperature):
                    change = 1 - 2*bits[edge]
                    bits[edge] ^= 1
                    for q in affected[edge]:
                        counts[q] += change
                    score += delta
                    best_score = min(best_score, score)
            if score == 0:
                cert = dict(n=n, edges=[list(p) for i,p in enumerate(pairs) if bits[i]])
                encoded = json.dumps(cert, indent=2)+'\n'
                (output / 'certificates' / ('n%02d.json' % n)).write_text(encoded)
                (output / 'certificate.json').write_text(encoded)
                best_n = n
                emit('certificate', restart=restart, edge_count=sum(bits))
                n += 1
                restart = 0
                best_score = None
                if evaluated < args.max_evaluations and time.monotonic()-start < args.seconds:
                    pairs, quads, affected = setup(n)
            else:
                emit('restart_end', restart=restart, final_score=score, best_score=best_score)
        reason = 'candidate_budget' if evaluated >= args.max_evaluations else 'search_time_budget'
        result = dict(config, evaluations=evaluated, best_n=best_n,
                      next_n=n, next_n_best_score=best_score,
                      stop_reason=reason, search_status='EXHAUSTED_BUDGET',
                      elapsed_seconds=time.monotonic()-start,
                      utc_end=datetime.now(timezone.utc).isoformat())
        (output / 'search-result.json').write_text(json.dumps(result, indent=2)+'\n')
        emit('stop', **{k: result[k] for k in ('stop_reason','best_n')})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20260921)
    parser.add_argument('--max-evaluations', type=int, default=10_000_000)
    parser.add_argument('--seconds', type=float, default=600)
    parser.add_argument('--restart-steps', type=int, default=50_000)
    args = parser.parse_args()
    if args.max_evaluations < 1 or args.seconds <= 0 or args.restart_steps < 1:
        parser.error('budgets and restart steps must be positive')
    run(args)


if __name__ == '__main__':
    main()
