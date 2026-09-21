#!/usr/bin/env python3
"""Certificate-only exhaustive R(4,4) verifier; Python >= 3.9, stdlib only."""
import argparse
from itertools import combinations
import json
from pathlib import Path


def verify(certificate):
    """Validate canonical edges on range(n), then inspect EVERY four-set."""
    result = dict(valid=False, format_valid=False, checked_four_sets=0,
                  k4_count=0, independent4_count=0)
    if not isinstance(certificate, dict):
        return dict(result, error='certificate must be an object')
    n, edges = certificate.get('n'), certificate.get('edges')
    if type(n) is not int or n < 0 or not isinstance(edges, list):
        return dict(result, error='n must be a nonnegative integer and edges a list')
    seen = set()
    for edge in edges:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(type(v) is not int for v in edge)):
            return dict(result, error='each edge must be a pair of integers')
        u, v = edge
        if not 0 <= u < v < n:
            return dict(result, error='edges must satisfy 0 <= u < v < n')
        if (u, v) in seen:
            return dict(result, error='duplicate edge')
        seen.add((u, v))
    result.update(format_valid=True, n=n, edge_count=len(seen))
    for vertices in combinations(range(n), 4):
        count = sum(pair in seen for pair in combinations(vertices, 2))
        result['checked_four_sets'] += 1
        result['k4_count'] += count == 6
        result['independent4_count'] += count == 0
    result['valid'] = result['k4_count'] == result['independent4_count'] == 0
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = verify(json.loads(args.certificate.read_text()))
    except (OSError, ValueError) as exc:
        result = dict(valid=False, format_valid=False, error=str(exc),
                      checked_four_sets=0, k4_count=0, independent4_count=0)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
