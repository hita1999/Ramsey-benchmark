#!/usr/bin/env python3
"""One-shot observer around the unchanged Phase A resume CLI. Never replay."""
import hashlib
import json
import os
import runpy
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BENCH = HERE.parent
os.chdir(REPO)
audit = json.loads((HERE / 'startup-audit.json').read_text())
assert audit['status'] == 'PASS'
assert not (HERE / 'first-candidate.json').exists(), 'Refuse second research launch'
for path, expected in audit['artifact_hashes_verified_against_git_and_manifest'].items():
    assert hashlib.sha256((REPO / path).read_bytes()).hexdigest() == expected, path
argv = audit['resolved_resume_argv']
assert argv[:3] == ['python3', 'benchmarks/r4-5/search.py', 'resume']
assert not (HERE / 'run').exists(), 'Refuse overwriting research output'
sys.path.insert(0, str(BENCH))
sys.argv = argv[1:]
observed = False


def observe(frame, event, arg):
    global observed
    if event == 'call' and frame.f_code.co_name == 'step' and Path(frame.f_code.co_filename).resolve() == BENCH / 'search.py':
        sys.setprofile(None)
        observed = True
        stamp = time.time()
        state = frame.f_locals['s']
        assert state['next_candidate_index'] == audit['next_candidate_index'] == 2000000
        canonical = json.dumps(state, sort_keys=True, separators=(',', ':')).encode()
        assert hashlib.sha256(canonical).hexdigest() == audit['state_sha256']
        result = {'first_resumed_candidate_index': state['next_candidate_index'],
                  'observed_at_unix': stamp, 'observed_at_utc': datetime.fromtimestamp(stamp, timezone.utc).isoformat(),
                  'seconds_from_session_start': stamp - audit['session_start_unix'],
                  'measurement': 'entry to first research step, immediately before its body; epoch difference from second-resolution goal createdAt',
                  'state_sha256_before_first_transition': audit['state_sha256'],
                  'startup_audit_sha256': hashlib.sha256((HERE / 'startup-audit.json').read_bytes()).hexdigest(),
                  'observer_changes_to_semantic_state': 0, 'profiling_disabled_after_first_entry': True}
        (HERE / 'first-candidate.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')


sys.setprofile(observe)
try:
    runpy.run_path(str(BENCH / 'search.py'), run_name='__main__')
finally:
    sys.setprofile(None)
assert observed, 'No research step observed'
