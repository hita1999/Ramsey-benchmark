#!/usr/bin/env python3
"""Self-contained exhaustive verifier for a 24-vertex (4,5)-Ramsey graph.

No external graph/solver packages, known Ramsey values, or repository imports.
Compatible with Python 3.9+.
"""
import json
from itertools import combinations

N = 24
DISTANCES = frozenset((1, 2, 4, 8, 9))


def edge(u, v):
    if u == v:
        return False
    delta = (u - v) % N
    return min(delta, N - delta) in DISTANCES


def main():
    assert len(DISTANCES) == 5
    assert all(1 <= d < N // 2 for d in DISTANCES)
    edges = sum(edge(u, v) for u, v in combinations(range(N), 2))
    degrees = [sum(edge(u, v) for v in range(N)) for u in range(N)]

    k4_count = sum(
        all(edge(u, v) for u, v in combinations(q, 2))
        for q in combinations(range(N), 4)
    )
    independent5_count = sum(
        all(not edge(u, v) for u, v in combinations(q, 2))
        for q in combinations(range(N), 5)
    )
    result = {
        "graph": "Z24 circulant with circular distances {1,2,4,8,9}",
        "vertices": N,
        "edges": edges,
        "degree_min": min(degrees),
        "degree_max": max(degrees),
        "four_vertex_subsets_checked": 10626,
        "k4_count": k4_count,
        "five_vertex_subsets_checked": 42504,
        "independent5_count": independent5_count,
        "valid": k4_count == 0 and independent5_count == 0,
        "implied_lower_bound": 25 if k4_count == 0 and independent5_count == 0 else None,
    }
    assert edges == 120
    assert degrees == [10] * N
    assert result["valid"], "not a valid (4,5,24)-graph"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
