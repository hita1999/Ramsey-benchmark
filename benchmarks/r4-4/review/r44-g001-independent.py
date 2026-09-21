#!/usr/bin/env python3
"""Independent R44-G001 certificate audit; does not import research verifier/search."""
import argparse
from itertools import combinations
import hashlib
import json
import platform
from pathlib import Path
import sys

def popcount(value):
    return bin(value).count("1")

def audit(raw):
    cert = json.loads(raw)
    if not isinstance(cert, dict):
        raise ValueError("certificate must be an object")
    n = cert.get("n")
    edges_raw = cert.get("edges")
    if type(n) is not int or n < 0 or not isinstance(edges_raw, list):
        raise ValueError("invalid n/edges")
    edges = []
    for item in edges_raw:
        if (not isinstance(item, list) or len(item) != 2
                or any(type(x) is not int for x in item)):
            raise ValueError("invalid edge")
        u, v = item
        if not 0 <= u < v < n:
            raise ValueError("non-canonical edge")
        edges.append((u, v))
    if len(edges) != len(set(edges)):
        raise ValueError("duplicate edge")

    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    degrees = [popcount(adj[v]) for v in range(n)]

    four_sets = k4 = independent4 = 0
    for vertices in combinations(range(n), 4):
        mask = sum(1 << v for v in vertices)
        twice_edges = sum(popcount(adj[v] & mask) for v in vertices)
        if twice_edges % 2:
            raise AssertionError("odd induced degree sum")
        induced_edges = twice_edges // 2
        four_sets += 1
        k4 += induced_edges == 6
        independent4 += induced_edges == 0

    triangles = independent_triples = 0
    for vertices in combinations(range(n), 3):
        mask = sum(1 << v for v in vertices)
        induced_edges = sum(popcount(adj[v] & mask) for v in vertices) // 2
        triangles += induced_edges == 3
        independent_triples += induced_edges == 0

    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "n": n,
        "edge_count": len(edges),
        "degree_sequence": degrees,
        "four_sets_checked": four_sets,
        "k4_count": k4,
        "independent4_count": independent4,
        "triangle_count": triangles,
        "independent_triple_count": independent_triples,
        "clique_number": 3 if triangles and not k4 else None,
        "independence_number": 3 if independent_triples and not independent4 else None,
        "valid": k4 == 0 and independent4 == 0,
        "python": sys.version,
        "platform": platform.platform(),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.certificate.read_bytes())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
