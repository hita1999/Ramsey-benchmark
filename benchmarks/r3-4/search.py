"""Bounded, deterministic vertex-extension search; Python standard library only."""
import argparse
import json
from itertools import combinations
from pathlib import Path


def search(budget):
    examined = 0
    best = []
    exhausted = False

    def visit(adj):
        nonlocal examined, best, exhausted
        n = len(adj)
        if n > len(best):
            best = adj[:]
        # Every forbidden structure newly created must contain the new vertex.
        independent_triples = [
            sum(1 << v for v in triple)
            for triple in combinations(range(n), 3)
            if all(not (adj[u] >> v & 1) for u, v in combinations(triple, 2))
        ]
        for neighbors in range(1 << n):
            if examined >= budget:
                exhausted = True
                return
            examined += 1
            if any(neighbors >> u & 1 and adj[u] & neighbors for u in range(n)):
                continue
            if any(neighbors & triple == 0 for triple in independent_triples):
                continue
            visit([adj[u] | (((neighbors >> u) & 1) << n) for u in range(n)]
                  + [neighbors])
            if exhausted:
                return

    visit([])
    return {
        "budget": budget,
        "candidates_examined": examined,
        "search_status": "EXHAUSTED_BUDGET" if exhausted else "COMPLETE",
        "certificate": {
            "n": len(best),
            "edges": [[u, v] for u in range(len(best)) for v in range(u + 1, len(best))
                      if best[u] >> v & 1],
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget", type=int, default=500000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.budget < 1:
        parser.error("budget must be positive")
    result = search(args.budget)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
