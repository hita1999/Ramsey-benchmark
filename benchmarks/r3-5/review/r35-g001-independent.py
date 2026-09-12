#!/usr/bin/env python3
"""Independent reviewer check for R35-G001.

This implementation intentionally does not import benchmarks/r3-5/verify.py.
It uses adjacency bitmasks and two different characterizations:

- triangle-free: the endpoints of every edge have no common neighbor;
- no independent 5-set: every 5-vertex mask contains at least one edge.

It also computes the independence number by descending subset size as a
cross-check stronger than the claim needed for R35-C001.
"""
import argparse
import itertools
import json
from pathlib import Path


def load_certificate(path):
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict) or set(value) != {'n', 'edges'}:
        raise ValueError('certificate must contain exactly n and edges')
    n = value['n']
    if type(n) is not int or n < 1 or not isinstance(value['edges'], list):
        raise ValueError('malformed certificate')
    edges = set()
    for raw in value['edges']:
        if (not isinstance(raw, list) or len(raw) != 2
                or any(type(v) is not int for v in raw)):
            raise ValueError('malformed edge')
        u, v = raw
        if not 0 <= u < v < n or (u, v) in edges:
            raise ValueError('invalid or duplicate edge')
        edges.add((u, v))
    return n, edges


def independent(mask, adjacency):
    while mask:
        low = mask & -mask
        v = low.bit_length() - 1
        if adjacency[v] & (mask ^ low):
            return False
        mask ^= low
    return True


def review(path):
    n, edges = load_certificate(path)
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u

    triangle_edge_violations = []
    for u, v in sorted(edges):
        common = adjacency[u] & adjacency[v]
        if common:
            triangle_edge_violations.append([u, v, common])

    independent_fives = []
    five_sets_checked = 0
    for vertices in itertools.combinations(range(n), 5):
        five_sets_checked += 1
        mask = sum(1 << v for v in vertices)
        if independent(mask, adjacency):
            independent_fives.append(list(vertices))

    alpha = 0
    first_maximum_independent_set = None
    for size in range(n, 0, -1):
        found = None
        for vertices in itertools.combinations(range(n), size):
            mask = sum(1 << v for v in vertices)
            if independent(mask, adjacency):
                found = list(vertices)
                break
        if found is not None:
            alpha = size
            first_maximum_independent_set = found
            break

    degrees = [adjacency[v].bit_count() for v in range(n)]
    valid = not triangle_edge_violations and not independent_fives
    return {
        'valid': valid,
        'n': n,
        'edges': len(edges),
        'degree_sequence': sorted(degrees),
        'triangle_edge_common_neighbor_violations': len(triangle_edge_violations),
        'five_sets_checked': five_sets_checked,
        'independent_fives': len(independent_fives),
        'independence_number': alpha,
        'first_maximum_independent_set': first_maximum_independent_set,
        'ramsey_lower_bound': n + 1 if valid else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = review(args.certificate)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
