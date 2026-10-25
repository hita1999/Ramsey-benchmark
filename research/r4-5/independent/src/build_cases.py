#!/usr/bin/env python3
"""Untrusted certificate producer. audit_cases.py independently checks its output.

Fixed sides occupy 0..d-1 and d..d+b-1; the splitting vertex is last.
Cross variable (a,j) is 1+a*b+j. No symmetry-breaking clauses are used.
"""
import argparse
import gzip
import itertools as it
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_graphs(name):
    graphs = []
    for line in (ROOT / 'data' / name).read_text().splitlines():
        n = ord(line[0]) - 63
        bits = ''.join(format(ord(c)-63, '06b') for c in line[1:])
        adj = [[False]*n for _ in range(n)]
        k = 0
        for j in range(1, n):
            for i in range(j):
                adj[i][j] = adj[j][i] = bits[k] == '1'
                k += 1
        graphs.append(adj)
    return graphs


def complement(g):
    return [[i != j and not g[i][j] for j in range(len(g))]
            for i in range(len(g))]


def homogeneous(g, k, color):
    return [q for q in it.combinations(range(len(g)), k)
            if all(g[i][j] == color for i,j in it.combinations(q, 2))]


def gluing_clauses(a, b, s, t):
    # Homogeneous subsets of each side can form a forbidden set iff every
    # cross pair has the same color. Root-containing clauses are satisfied
    # because a is (s-1,t), b is (s,t-1); the independent audit checks this.
    clauses = []
    for k, color in [(s, True), (t, False)]:
        sign = -1 if color else 1
        for i in range(k+1):
            for left in homogeneous(a, i, color):
                for right in homogeneous(b, k-i, color):
                    clauses.append(tuple(sign*(1+x*len(b)+y)
                                         for x in left for y in right))
    return clauses


def isomorphisms(source, target, vertices):
    """All isomorphisms onto target[vertices], without canonicalization."""
    n = len(source)
    deg = [sum(row) for row in source]
    candidates = [[v for v in vertices
                   if sum(target[v][w] for w in vertices) == deg[i]]
                  for i in range(n)]
    order = sorted(range(n), key=lambda i: (len(candidates[i]), -deg[i], i))
    mapping, used = [-1]*n, set()

    def visit(depth):
        if depth == n:
            yield tuple(mapping)
            return
        i = order[depth]
        for v in candidates[i]:
            if v in used:
                continue
            if any(source[i][j] != target[v][mapping[j]] for j in order[:depth]):
                continue
            mapping[i] = v
            used.add(v)
            yield from visit(depth+1)
            used.remove(v)
            mapping[i] = -1
    yield from visit(0)


def blocking_witnesses(a, b, targets):
    assignments = {}
    for target_index, target in enumerate(targets):
        for root in range(len(target)):
            neighbors = [v for v in range(len(target)) if target[root][v]]
            anti = [v for v in range(len(target)) if v != root and not target[root][v]]
            if len(neighbors) != len(a):
                continue
            left_maps = list(isomorphisms(a, target, neighbors))
            right_maps = list(isomorphisms(b, target, anti))
            for p in left_maps:
                for q in right_maps:
                    mask = sum(1 << (i*len(b)+j)
                               for i in range(len(a)) for j in range(len(b))
                               if target[p[i]][q[j]])
                    assignments.setdefault(mask, {'mask': mask,
                        'target': target_index, 'permutation': list(p+q+(root,))})
    return [assignments[k] for k in sorted(assignments)]


def write_case(name, a, b, s, t, metadata, witnesses=None):
    clauses = gluing_clauses(a,b,s,t)
    nv = len(a)*len(b)
    if witnesses is not None:
        for w in witnesses:
            clauses.append(tuple(-(i+1) if w['mask'] >> i & 1 else i+1
                                 for i in range(nv)))
        with gzip.open(ROOT/'proofs'/f'{name}.witnesses.json.gz', 'wt') as f:
            json.dump(witnesses, f, separators=(',', ':'))
    with gzip.open(ROOT/'proofs'/f'{name}.cnf.gz', 'wt') as f:
        f.write(f'p cnf {nv} {len(clauses)}\n')
        for clause in clauses:
            f.write(' '.join(map(str,clause))+' 0\n')
    return dict(name=name, variables=nv, clauses=len(clauses),
                blocked_assignments=0 if witnesses is None else len(witnesses),
                **metadata)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('suite', choices=['coverage16', 'degree8'])
    args = parser.parse_args()
    cases = []
    if args.suite == 'coverage16':
        targets = read_graphs('r44_16.g6')
        for d in [7,8]:
            aa = read_graphs(f'r34_{d}.g6')
            bb = [complement(g) for g in read_graphs(f'r34_{15-d}.g6')]
            for ai, a in enumerate(aa):
                for bi, b in enumerate(bb):
                    name = f'cover16-d{d}-a{ai:03}-b{bi:03}'
                    witnesses = blocking_witnesses(a,b,targets)
                    cases.append(write_case(name,a,b,4,4,
                        {'suite': args.suite, 'degree':d, 'a':ai, 'b':bi}, witnesses))
    else:
        aa, bb = read_graphs('r35_8.g6'), read_graphs('r44_16.g6')
        for ai,a in enumerate(aa):
            for bi,b in enumerate(bb):
                name = f'glue8-a{ai:03}-b{bi:03}'
                cases.append(write_case(name,a,b,4,5,
                    {'suite':args.suite, 'degree':8, 'a':ai, 'b':bi}))
    (ROOT/'results'/f'{args.suite}-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(json.dumps({'suite':args.suite,'cases':len(cases),
                      'blocked_assignments':sum(c['blocked_assignments'] for c in cases)}))


if __name__ == '__main__':
    main()
