#!/usr/bin/env python3
"""Replay saved R44 certificate checks; no search and no new independent proof."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    benchmark = "benchmarks/r4-4"
    runs = []

    def run(name, argv):
        result = subprocess.run(argv, cwd=root, text=True, capture_output=True)
        (output / (name + ".stdout.txt")).write_text(result.stdout)
        (output / (name + ".stderr.txt")).write_text(result.stderr)
        runs.append(dict(name=name, argv=argv, returncode=result.returncode))
        if result.returncode:
            raise RuntimeError("{} failed; see saved logs".format(name))

    run("research-verifier", [sys.executable, benchmark + "/verify.py",
                              benchmark + "/run/certificate.json",
                              "--output", str(output / "research-result.json")])
    run("existing-tests", [sys.executable, "-m", "unittest", "discover",
                           "-s", benchmark, "-p", "test_*.py", "-v"])
    run("reviewer-verifier", [sys.executable, benchmark + "/review/r44-g001-independent.py",
                              benchmark + "/run/certificate.json",
                              "--output", str(output / "reviewer-result.json")])
    saved_path = root / benchmark / "review/r44-g001-independent-result.json"
    actual_path = output / "reviewer-result.json"
    saved = json.loads(saved_path.read_text())
    actual = json.loads(actual_path.read_text())
    excluded = ["platform", "python"]
    # Compare all keys except explicitly declared environment metadata; no selected subset.
    normalized = lambda data: {k: v for k, v in data.items() if k not in excluded}
    differing = sorted(k for k in saved.keys() | actual.keys() if saved.get(k) != actual.get(k))
    sources = [benchmark + "/verify.py", benchmark + "/review/r44-g001-independent.py",
               benchmark + "/run/certificate.json",
               benchmark + "/review/r44-g001-independent-result.json"]
    report = dict(
        utc=datetime.now(timezone.utc).isoformat(),
        git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        python=sys.version, executable=sys.executable, platform=platform.platform(),
        runs=runs, excluded_keys=excluded, differing_keys=differing,
        byte_equal=saved_path.read_bytes() == actual_path.read_bytes(),
        mathematical_fields_equal=normalized(saved) == normalized(actual),
        source_sha256={p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sources},
        scope="Saved certificate verifiers and existing tests only; full search not rerun; not a new independent review",
    )
    (output / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["mathematical_fields_equal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
