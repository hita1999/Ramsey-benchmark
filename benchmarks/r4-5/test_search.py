#!/usr/bin/env python3
"""All transitions here are TEST/REPLAY, never research evaluations."""
import copy
import itertools
import json
import tempfile
from pathlib import Path
import search
from verify import verify


def main():
    result = {"label": "TEST_REPLAY_OUTSIDE_RESEARCH_BUDGET", "status": "PASS",
              "excluded_metadata": ["all checkpoint wrapper fields; no state fields excluded"],
              "tests": [], "candidate_evaluations": 0, "delta_comparisons": 0}
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        config_path, checkpoint_path = root / "config.json", root / "checkpoint.json"
        configs = [(5, 111, 157), (5, 1, 1), (12, 7, 1)]
        for n, a, b in configs:
            c = {"algorithm": search.ALGORITHM, "seed": 123456789,
                 "start_n": n, "restart_interval": 7}
            search.write_json(config_path, c)
            uninterrupted = search.advance(search.initial(c), c, a + b)
            split = search.advance(search.initial(c), c, a)
            cp = search.pack(split, config_path, "TEST", "TEST", "TEST", None)
            search.write_json(checkpoint_path, cp)
            restored, loaded_c = search.load_checkpoint(checkpoint_path, config_path,
                                                       search.file_hash(checkpoint_path))
            resumed = search.advance(restored["state"], loaded_c, b)
            search.validate_state(uninterrupted, c)
            search.validate_state(resumed, c)
            assert uninterrupted == resumed
            assert search.canonical(uninterrupted) == search.canonical(resumed)
            if n == 12:
                assert split["iteration"] == 7 and resumed["restart"] == 1
            result["tests"].append({"name": "split_resume", "config": c, "a": a, "b": b,
                                    "split_mode": split["mode"], "split_iteration": split["iteration"],
                                    "final_state_sha256": search.digest(resumed),
                                    "all_semantic_fields_equal": True})
            result["candidate_evaluations"] += 2 * (a + b)
        # Known PRNG arithmetic regression, obtained by explicit scalar operations.
        state = search.initial(c)
        x = c["seed"]
        expected = []
        for _ in range(8):
            x = x ^ (x >> 12)
            x = x ^ ((x * (2 ** 25)) % (2 ** 64))
            x = x ^ (x >> 27)
            expected.append((x * 2685821657736338717) % (2 ** 64))
        assert [search.draw(state) for _ in range(8)] == expected
        result["tests"].append({"name": "prng_integer_arithmetic", "outputs": expected})
        # Save a valid search-mode checkpoint for negative tests.
        cp = search.pack(uninterrupted, config_path, "TEST", "TEST", "TEST", None)
        for field, value in (("state_sha256", "bad"), ("config_sha256", "bad"),
                             ("code_sha256", {}), ("certificate_sha256", ["bad"]),
                             ("schema", "unknown")):
            bad = copy.deepcopy(cp)
            bad[field] = value
            search.write_json(checkpoint_path, bad)
            try:
                search.load_checkpoint(checkpoint_path, config_path)
                raise AssertionError("tampered checkpoint accepted: " + field)
            except ValueError:
                pass
        bad = copy.deepcopy(cp)
        bad["state"]["score"] += 1
        bad["state_sha256"] = search.digest(bad["state"])
        search.write_json(checkpoint_path, bad)
        try:
            search.load_checkpoint(checkpoint_path, config_path)
            raise AssertionError("wrong semantic score accepted")
        except ValueError:
            pass
        search.write_json(checkpoint_path, cp)
        try:
            search.load_checkpoint(checkpoint_path, config_path, "bad")
            raise AssertionError("wrong file hash accepted")
        except ValueError:
            pass
        result["tests"].append({"name": "tamper_rejection", "cases": 7})
    # Exhaustive n=5 graphs and every edge: both insertion and deletion deltas.
    edges = list(itertools.combinations(range(5), 2))
    for mask in range(1 << len(edges)):
        graph = [0] * 5
        for i, (u, v) in enumerate(edges):
            if (mask >> i) & 1:
                graph[u] |= 1 << v
                graph[v] |= 1 << u
        score = search.full_score(graph)
        for u, v in edges:
            delta = search.flip_delta(graph, u, v)
            changed = graph[:]
            changed[u] ^= 1 << v
            changed[v] ^= 1 << u
            assert search.full_score(changed) - score == delta
            result["delta_comparisons"] += 1
    # Deterministic samples at n=8, independent of search transitions.
    state = {"prng_state": "87654321"}
    edges = list(itertools.combinations(range(8), 2))
    for _ in range(32):
        graph = [0] * 8
        for u, v in edges:
            if search.draw(state) & 1:
                graph[u] |= 1 << v
                graph[v] |= 1 << u
        score = search.full_score(graph)
        for u, v in edges:
            delta = search.flip_delta(graph, u, v)
            changed = graph[:]
            changed[u] ^= 1 << v
            changed[v] ^= 1 << u
            assert search.full_score(changed) - score == delta
            result["delta_comparisons"] += 1
    result["tests"].append({"name": "delta_vs_exhaustive", "cases": result["delta_comparisons"]})
    assert not verify({"n": 5, "edges": []})["valid"]
    assert not verify({"n": 4, "edges": [list(e) for e in itertools.combinations(range(4), 2)]})["valid"]
    for cert in ({"n": 5, "edges": [[0, 0]]}, {"n": 5, "edges": [[1, 0]]},
                 {"n": 5, "edges": [[0, 1], [0, 1]]}, {"n": 5, "edges": [[0, 5]]}):
        try:
            verify(cert)
            raise AssertionError("malformed certificate accepted")
        except ValueError:
            pass
    result["tests"].append({"name": "certificate_negative_controls", "cases": 6})
    result["code_sha256"] = {name: search.file_hash(search.ROOT / name) for name in search.CODE}
    result["test_code_sha256"] = search.file_hash(__file__)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
