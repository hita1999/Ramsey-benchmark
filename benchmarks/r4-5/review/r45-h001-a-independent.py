#!/usr/bin/env python3
"""Independent R45-C001 certificate audit; imports no research search/verifier code."""
import argparse
import hashlib
from itertools import combinations
import json
import platform
from pathlib import Path
import sys


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cert = json.loads(args.certificate.read_text())
    if set(cert) != {"n", "edges"}:
        raise ValueError("certificate fields")
    n = cert["n"]
    if type(n) is not int or n < 1 or not isinstance(cert["edges"], list):
        raise ValueError("certificate types")
    edges = set()
    for item in cert["edges"]:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("edge shape")
        u, v = item
        if type(u) is not int or type(v) is not int or not 0 <= u < v < n:
            raise ValueError("edge endpoints")
        if (u, v) in edges:
            raise ValueError("duplicate edge")
        edges.add((u, v))

    k4 = 0
    checked4 = 0
    for vertices in combinations(range(n), 4):
        checked4 += 1
        k4 += all((u, v) in edges for u, v in combinations(vertices, 2))

    independent5 = 0
    checked5 = 0
    for vertices in combinations(range(n), 5):
        checked5 += 1
        independent5 += all((u, v) not in edges for u, v in combinations(vertices, 2))

    triangles = sum(all((u, v) in edges for u, v in combinations(vertices, 2))
                    for vertices in combinations(range(n), 3))
    independent4 = sum(all((u, v) not in edges for u, v in combinations(vertices, 2))
                       for vertices in combinations(range(n), 4))
    degrees = [sum((min(v, w), max(v, w)) in edges for w in range(n) if w != v)
               for v in range(n)]

    result = {
        "canonical_certificate_sha256": hashlib.sha256(canonical(cert)).hexdigest(),
        "n": n,
        "edge_count": len(edges),
        "degree_sequence": degrees,
        "four_sets_checked": checked4,
        "k4_count": k4,
        "five_sets_checked": checked5,
        "independent5_count": independent5,
        "triangle_count": triangles,
        "independent4_count": independent4,
        "clique_number": 3 if triangles and not k4 else None,
        "independence_number": 4 if independent4 and not independent5 else None,
        "valid": k4 == 0 and independent5 == 0,
        "python": sys.version,
        "platform": platform.platform(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
