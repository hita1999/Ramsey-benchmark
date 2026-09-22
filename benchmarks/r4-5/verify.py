#!/usr/bin/env python3
"""Certificate-only exhaustive verifier; imports no search implementation."""
import argparse
import itertools
import json
from pathlib import Path


def verify(cert):
    if set(cert) != {"n", "edges"}:
        raise ValueError("certificate fields")
    n = cert["n"]
    if type(n) is not int or n < 1 or not isinstance(cert["edges"], list):
        raise ValueError("certificate types")
    edges = set()
    for edge in cert["edges"]:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError("edge shape")
        u, v = edge
        if type(u) is not int or type(v) is not int or not 0 <= u < v < n:
            raise ValueError("edge endpoints")
        if (u, v) in edges:
            raise ValueError("duplicate edge")
        edges.add((u, v))
    red = sum(all(e in edges for e in itertools.combinations(s, 2))
              for s in itertools.combinations(range(n), 4))
    blue = sum(all(e not in edges for e in itertools.combinations(s, 2))
               for s in itertools.combinations(range(n), 5))
    return {"n": n, "edges": len(edges), "k4": red,
            "independent5": blue, "valid": red == blue == 0,
            "lower_bound": n + 1 if red == blue == 0 else None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificates", nargs="+")
    args = parser.parse_args()
    results = [{"path": p, **verify(json.loads(Path(p).read_text()))}
               for p in args.certificates]
    print(json.dumps(results, indent=2))
    raise SystemExit(0 if all(r["valid"] for r in results) else 1)
