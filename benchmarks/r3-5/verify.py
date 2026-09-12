#!/usr/bin/env python3
"""Validate only an explicit certificate, using exhaustive subset enumeration."""
import argparse
import itertools
import json
from pathlib import Path
import sys


def verify(certificate):
    if not isinstance(certificate, dict) or set(certificate) != {'n', 'edges'}:
        raise ValueError('certificate must have exactly n and edges')
    n = certificate['n']
    if type(n) is not int or n < 1:
        raise ValueError('n must be a positive integer')
    if not isinstance(certificate['edges'], list):
        raise ValueError('edges must be a list')
    edges = set()
    for edge in certificate['edges']:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError('each edge must be a pair')
        u, v = edge
        if type(u) is not int or type(v) is not int or not (0 <= u < v < n):
            raise ValueError('edges require integer endpoints 0 <= u < v < n')
        if (u, v) in edges:
            raise ValueError('duplicate edge')
        edges.add((u, v))
    triples = fives = triangles = independent_fives = 0
    first_triangle = first_independent_five = None
    for vertices in itertools.combinations(range(n), 3):
        triples += 1
        if all(edge in edges for edge in itertools.combinations(vertices, 2)):
            triangles += 1
            if first_triangle is None:
                first_triangle = list(vertices)
    for vertices in itertools.combinations(range(n), 5):
        fives += 1
        if all(edge not in edges for edge in itertools.combinations(vertices, 2)):
            independent_fives += 1
            if first_independent_five is None:
                first_independent_five = list(vertices)
    valid = triangles == 0 and independent_fives == 0
    return {'n': n, 'edges': len(edges), 'triples_checked': triples,
            'five_sets_checked': fives, 'triangles': triangles,
            'independent_fives': independent_fives,
            'first_triangle': first_triangle,
            'first_independent_five': first_independent_five,
            'valid': valid, 'ramsey_lower_bound': n + 1 if valid else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    try:
        result = verify(json.loads(args.certificate.read_text()))
    except (ValueError, OSError) as error:
        print(json.dumps({'valid': False, 'error': str(error)}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
