"""Check an explicit simple graph for red triangles and blue K4s."""
import argparse
import json
from itertools import combinations
from pathlib import Path


def verify(certificate):
    if not isinstance(certificate, dict) or set(certificate) != {"n", "edges"}:
        raise ValueError("certificate must contain exactly n and edges")
    n, raw_edges = certificate["n"], certificate["edges"]
    if type(n) is not int or n < 1 or not isinstance(raw_edges, list):
        raise ValueError("invalid n or edges")
    edges = set()
    for edge in raw_edges:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(type(v) is not int for v in edge)):
            raise ValueError("each edge must be a pair of integers")
        u, v = edge
        if not 0 <= u < v < n or (u, v) in edges:
            raise ValueError("edge must be unique and satisfy 0 <= u < v < n")
        edges.add((u, v))
    triples = quadruples = 0
    for vertices in combinations(range(n), 3):
        triples += 1
        if all(edge in edges for edge in combinations(vertices, 2)):
            raise ValueError(f"red triangle: {vertices}")
    for vertices in combinations(range(n), 4):
        quadruples += 1
        if all(edge not in edges for edge in combinations(vertices, 2)):
            raise ValueError(f"blue K4: {vertices}")
    return {"valid": True, "n": n, "red_edges": len(edges),
            "triples_checked": triples, "quadruples_checked": quadruples,
            "lower_bound": n + 1}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        result = verify(json.loads(args.certificate.read_text()))
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, f"FAIL: {error}\n")
    print(json.dumps(result, sort_keys=True))
