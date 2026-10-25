#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
task_root="$(cd "$(dirname "$0")" && pwd)"
task_tmp="$(mktemp -d "${TMPDIR:-/tmp}/r45-replay.XXXXXX")"
trap 'rm -rf "$task_tmp"' EXIT
cd "$task_root"
shasum -a 256 -c ARTIFACTS.sha256 > "$task_tmp/hashes.log"
${CXX:-c++} -O3 -std=c++17 src/lower24.cpp -o "$task_tmp/lower24"
${CXX:-c++} -O3 -std=c++17 src/catalogue8.cpp -o "$task_tmp/catalogue8"
${CXX:-c++} -O2 -std=c++17 src/check_lrat.cpp -o "$task_tmp/check-lrat"
"$task_tmp/lower24"
"$task_tmp/catalogue8" data/r35_8.g6 8 3 5
"$task_tmp/catalogue8" data/r34_7.g6 7 3 4
"$task_tmp/catalogue8" data/r34_8.g6 8 3 4
python3 src/test_checkers.py --checker "$task_tmp/check-lrat"
python3 src/audit_cases.py coverage16
python3 src/audit_cases.py degree8
python3 src/run_proofs.py coverage16 --checker "$task_tmp/check-lrat" \
  --report "$task_tmp/coverage16.json"
python3 src/run_proofs.py degree8 --checker "$task_tmp/check-lrat" \
  --available-only --jobs 4 --report "$task_tmp/degree8.json"
python3 - "$task_tmp/degree8.json" <<'PY'
import json, sys
from pathlib import Path
cases=json.loads(Path('results/degree8-cases.json').read_text())
checked=json.loads(Path(sys.argv[1]).read_text())
done={r['name'] for r in checked if r['status']=='VERIFIED_UNSAT'}
missing=[c['name'] for c in cases if c['name'] not in done]
print(json.dumps({'checkpoint_status':'PARTIAL_PROGRESS',
                  'degree8_proofs_checked':len(done),
                  'degree8_proofs_missing':len(missing),
                  'degree10':'NOT_ATTEMPTED','degree12':'NOT_ATTEMPTED',
                  'full_upper_bound_proved':False},indent=2))
PY
