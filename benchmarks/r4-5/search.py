#!/usr/bin/env python3
"""Deterministic integer state machine. See checkpoint-schema.md for semantics."""
import argparse
import copy
import hashlib
import itertools
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from verify import verify

ROOT = Path(__file__).resolve().parent
SCHEMA = "r45-checkpoint-v1"
ALGORITHM = "integer-noisy-edge-flip-v1"
MASK = (1 << 64) - 1
POPCOUNT = getattr(int, "bit_count", lambda x: bin(x).count("1"))
CODE = ("search.py", "verify.py")
STATE_FIELDS = {"next_candidate_index", "target_n", "completed_targets", "certificates",
                "prng_state", "graph", "score", "best_graph", "best_score",
                "restart", "iteration", "target_evaluations", "mode"}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def check_config(c):
    if set(c) != {"algorithm", "seed", "start_n", "restart_interval"}:
        raise ValueError("config fields")
    if c["algorithm"] != ALGORITHM:
        raise ValueError("algorithm")
    for name in ("seed", "start_n", "restart_interval"):
        if type(c[name]) is not int:
            raise ValueError("config integer")
    if not 0 < c["seed"] <= MASK or c["start_n"] < 5 or c["restart_interval"] < 1:
        raise ValueError("config range")


def initial(c):
    check_config(c)
    return {"next_candidate_index": 0, "target_n": c["start_n"],
            "completed_targets": [], "certificates": [], "prng_state": str(c["seed"]),
            "graph": None, "score": None, "best_graph": None, "best_score": None,
            "restart": 0, "iteration": 0, "target_evaluations": 0, "mode": "initialize"}


def draw(s):
    x = int(s["prng_state"])
    x ^= x >> 12
    x ^= (x << 25) & MASK
    x ^= x >> 27
    s["prng_state"] = str(x)
    return (x * 2685821657736338717) & MASK


def graph_certificate(g):
    return {"n": len(g), "edges": [[u, v] for u in range(len(g))
                                  for v in range(u + 1, len(g)) if (g[u] >> v) & 1]}


def full_score(g):
    # Deliberately exhaustive and independent of edge-flip delta.
    result = verify(graph_certificate(g))
    return result["k4"] + result["independent5"]


def edge_count(g, vertices):
    count = 0
    while vertices:
        bit = vertices & -vertices
        vertices ^= bit
        count += POPCOUNT(g[bit.bit_length() - 1] & vertices)
    return count


def triangle_count(g, vertices):
    count = 0
    while vertices:
        bit = vertices & -vertices
        vertices ^= bit
        common = g[bit.bit_length() - 1] & vertices
        count += edge_count(g, common)
    return count


def flip_delta(g, u, v):
    n = len(g)
    allowed = ((1 << n) - 1) ^ (1 << u) ^ (1 << v)
    common_red = g[u] & g[v] & allowed
    common_blue = ~(g[u] | g[v]) & allowed
    red = edge_count(g, common_red)
    # Complement rows are derived entirely from the current graph.
    blue_graph = [((1 << n) - 1) ^ (1 << i) ^ row for i, row in enumerate(g)]
    blue = triangle_count(blue_graph, common_blue)
    return blue - red if (g[u] >> v) & 1 else red - blue


def step(s, c, edges):
    n = s["target_n"]
    if s["mode"] == "initialize" or s["iteration"] == c["restart_interval"]:
        if s["mode"] != "initialize":
            s["restart"] += 1
        s["iteration"] = 0
        g = [0] * n
        for u, v in edges:
            if draw(s) & 1:
                g[u] |= 1 << v
                g[v] |= 1 << u
        s["graph"] = g
        s["score"] = full_score(g)
        s["mode"] = "search"
    else:
        u, v = edges[draw(s) % len(edges)]
        delta = flip_delta(s["graph"], u, v)
        noise = max(1, 128 - 127 * s["iteration"] // c["restart_interval"])
        if delta <= 0 or draw(s) % 1024 < noise // (1 + delta):
            s["graph"][u] ^= 1 << v
            s["graph"][v] ^= 1 << u
            s["score"] += delta
    s["iteration"] += 1
    s["target_evaluations"] += 1
    s["next_candidate_index"] += 1
    if s["best_score"] is None or s["score"] < s["best_score"]:
        s["best_score"] = s["score"]
        s["best_graph"] = s["graph"][:]
    if s["score"] == 0:
        s["certificates"].append(graph_certificate(s["graph"]))
        s["completed_targets"].append({"n": n, "evaluations": s["target_evaluations"],
                                       "found_at_index": s["next_candidate_index"] - 1})
        s.update(target_n=n + 1, graph=None, score=None, best_graph=None, best_score=None,
                 restart=0, iteration=0, target_evaluations=0, mode="initialize")


def advance(s, c, count):
    if type(count) is not int or count < 0:
        raise ValueError("count")
    n = None
    edges = None
    for _ in range(count):
        if n != s["target_n"]:
            n = s["target_n"]
            edges = list(itertools.combinations(range(n), 2))
        step(s, c, edges)
    return s


def validate_graph(g, n):
    if not isinstance(g, list) or len(g) != n:
        raise ValueError("graph length")
    if any(type(row) is not int or row < 0 or row >= (1 << n) for row in g):
        raise ValueError("row range")
    for u in range(n):
        if (g[u] >> u) & 1:
            raise ValueError("self loop")
        for v in range(u + 1, n):
            if ((g[u] >> v) & 1) != ((g[v] >> u) & 1):
                raise ValueError("asymmetry")


def validate_state(s, c):
    check_config(c)
    if set(s) != STATE_FIELDS:
        raise ValueError("state fields")
    for key in ("next_candidate_index", "target_n", "restart", "iteration", "target_evaluations"):
        if type(s[key]) is not int or s[key] < 0:
            raise ValueError("state counter")
    if not isinstance(s["prng_state"], str) or not s["prng_state"].isdigit():
        raise ValueError("prng encoding")
    if not 0 < int(s["prng_state"]) <= MASK or str(int(s["prng_state"])) != s["prng_state"]:
        raise ValueError("prng range")
    completed = s["completed_targets"]
    if not isinstance(completed, list) or not isinstance(s["certificates"], list):
        raise ValueError("completed types")
    if len(completed) != len(s["certificates"]) or s["target_n"] != c["start_n"] + len(completed):
        raise ValueError("target sequence")
    total = 0
    for i, (target, cert) in enumerate(zip(completed, s["certificates"])):
        if set(target) != {"n", "evaluations", "found_at_index"}:
            raise ValueError("completed fields")
        if any(type(target[k]) is not int for k in target) or target["evaluations"] < 1:
            raise ValueError("completed counters")
        total += target["evaluations"]
        if target["n"] != c["start_n"] + i or target["found_at_index"] != total - 1:
            raise ValueError("completed interval")
        if cert["n"] != target["n"] or not verify(cert)["valid"]:
            raise ValueError("invalid certificate")
    if total + s["target_evaluations"] != s["next_candidate_index"]:
        raise ValueError("global interval")
    if s["mode"] == "initialize":
        if any(s[k] is not None for k in ("graph", "score", "best_graph", "best_score")):
            raise ValueError("initial graphs")
        if any(s[k] != 0 for k in ("restart", "iteration", "target_evaluations")):
            raise ValueError("initial counters")
    elif s["mode"] == "search":
        if not 1 <= s["iteration"] <= c["restart_interval"]:
            raise ValueError("iteration range")
        if s["target_evaluations"] != s["restart"] * c["restart_interval"] + s["iteration"]:
            raise ValueError("restart counter")
        for graph, score in (("graph", "score"), ("best_graph", "best_score")):
            validate_graph(s[graph], s["target_n"])
            if type(s[score]) is not int or s[score] <= 0 or full_score(s[graph]) != s[score]:
                raise ValueError("score mismatch")
        if s["best_score"] > s["score"]:
            raise ValueError("best score")
    else:
        raise ValueError("mode")


def pack(s, config_path, phase, execution_base, code_commit, consumed):
    return {"schema": SCHEMA, "benchmark": "R(4,5)", "phase": phase,
            "algorithm": ALGORITHM, "execution_base": execution_base, "code_commit": code_commit,
            "created_at_utc": now(), "config_sha256": file_hash(config_path),
            "code_sha256": {name: file_hash(ROOT / name) for name in CODE},
            "certificate_sha256": [digest(cert) for cert in s["certificates"]],
            "consumed_research_interval": consumed, "state": copy.deepcopy(s),
            "state_sha256": digest(s)}


def load_checkpoint(path, config_path, expected_sha256=None):
    if expected_sha256 is not None and file_hash(path) != expected_sha256:
        raise ValueError("checkpoint file hash")
    cp = json.loads(Path(path).read_text())
    c = json.loads(Path(config_path).read_text())
    if cp["schema"] != SCHEMA or cp["algorithm"] != ALGORITHM or cp["benchmark"] != "R(4,5)":
        raise ValueError("checkpoint identity")
    if cp["config_sha256"] != file_hash(config_path):
        raise ValueError("config hash")
    if cp["code_sha256"] != {name: file_hash(ROOT / name) for name in CODE}:
        raise ValueError("code hash")
    s = cp["state"]
    if cp["state_sha256"] != digest(s):
        raise ValueError("state hash")
    if cp["certificate_sha256"] != [digest(cert) for cert in s["certificates"]]:
        raise ValueError("certificate hashes")
    validate_state(s, c)
    interval = cp["consumed_research_interval"]
    if interval is not None and interval != [0, s["next_candidate_index"]]:
        raise ValueError("consumed interval")
    return cp, c


def export_artifacts(out, s):
    for cert in s["certificates"]:
        write_json(out / "certificates" / ("n%02d.json" % cert["n"]), cert)
    if s["certificates"]:
        write_json(out / "certificate.json", s["certificates"][-1])
    write_json(out / "best-so-far.json", {"target_n": s["target_n"], "score": s["best_score"],
               "graph": graph_certificate(s["best_graph"]) if s["best_graph"] is not None else None,
               "valid_certificate": False})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=("start", "resume", "validate"))
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--checkpoint", type=Path)
    p.add_argument("--expected-sha256")
    p.add_argument("--out", type=Path)
    p.add_argument("--execution-base")
    args = p.parse_args()
    if args.action in ("resume", "validate"):
        if not args.checkpoint:
            p.error("checkpoint required")
        cp, c = load_checkpoint(args.checkpoint, args.config, args.expected_sha256)
        s = cp["state"]
        if args.action == "validate":
            print(json.dumps({"status": "PASS", "next_candidate_index": s["next_candidate_index"],
                              "checkpoint_sha256": file_hash(args.checkpoint),
                              "research_evaluations_consumed": 0}, indent=2))
            return
        if not args.expected_sha256:
            p.error("resume requires checkpoint hash from Git handoff manifest")
        if cp["phase"] != "H001-A" or s["next_candidate_index"] != 2000000:
            p.error("Phase B must resume the Phase A boundary")
        phase, until = "H001-B", 10000000
    else:
        c = json.loads(args.config.read_text())
        s = initial(c)
        phase, until = "H001-A", 2000000
    if not args.out or not args.execution_base:
        p.error("out and execution-base required for research")
    if args.out.exists() and any(args.out.iterdir()):
        p.error("research output directory must be absent or empty; refuse overwrite")
    args.out.mkdir(parents=True, exist_ok=True)
    code_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    start_index = s["next_candidate_index"]
    started, clock = now(), time.monotonic()
    write_json(args.out / "startup-audit.json", {"phase": phase, "start_index": start_index,
               "execution_base": args.execution_base, "code_commit": code_commit,
               "started_at_utc": started, "checkpoint_validated": args.action == "resume",
               "input_checkpoint_sha256": file_hash(args.checkpoint) if args.checkpoint else None,
               "research_evaluations_before_audit": 0})
    with (args.out / "progress.jsonl").open("w") as log:
        while s["next_candidate_index"] < until:
            advance(s, c, min(100000, until - s["next_candidate_index"]))
            row = {"next_candidate_index": s["next_candidate_index"], "target_n": s["target_n"],
                   "score": s["score"], "best_score": s["best_score"],
                   "elapsed_seconds": time.monotonic() - clock}
            log.write(json.dumps(row) + "\n")
            log.flush()
            print(json.dumps(row), flush=True)
    cp = pack(s, args.config, phase, args.execution_base, code_commit, [0, until])
    write_json(args.out / "checkpoint.json", cp)
    export_artifacts(args.out, s)
    load_checkpoint(args.out / "checkpoint.json", args.config)
    write_json(args.out / "run-result.json", {"phase": phase, "status": "PARTIAL_PROGRESS",
               "reason": "MANDATORY_HANDOFF_CHECKPOINT" if phase == "H001-A" else "PHASE_B_INTERVAL_COMPLETE",
               "consumed_interval": [start_index, until], "research_evaluations": until - start_index,
               "started_at_utc": started, "ended_at_utc": now(),
               "elapsed_seconds_including_serialization_validation": time.monotonic() - clock,
               "checkpoint_sha256": file_hash(args.out / "checkpoint.json"),
               "checkpoint_integrity": "PASS", "state_sha256": digest(s)})


if __name__ == "__main__":
    main()
