#!/usr/bin/env python3
"""Record Git-only reconstruction. No candidate transitions are called."""
import hashlib
import json
import platform
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BENCH = HERE.parent
sys.path.insert(0, str(BENCH))
import search

BASE = 'e1299901c3533ce1f6843c425ff8c458b834facc'
MERGE = '5f061f2df33e74e7b416e958ca1e427536763ce9'
SESSION_START = 1790066700


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO, text=True).strip()


def main():
    assert not (HERE / 'run').exists(), 'Refuse audit after research output exists'
    assert git('rev-parse', 'origin/main') == BASE
    assert git('branch', '--show-current') == 'codex/r45-h001-b-resume'
    manifest_path = BENCH / 'h001-a/handoff-manifest.json'
    m = json.loads(manifest_path.read_text())
    for commit in (MERGE, m['code_commit']):
        subprocess.run(['git', 'merge-base', '--is-ancestor', commit, BASE], cwd=REPO, check=True)
    assert git('show', '-s', '--format=%P', MERGE).split() == [
        '6031a203863a71cae5a34793c5d87dbc9b24479b',
        'afb386070addbfd5549d21be2a8bc41e2e9acd07']
    historical = {}
    for p, expected in m['artifact_sha256'].items():
        raw = subprocess.check_output(['git', 'show', BASE + ':' + p], cwd=REPO)
        historical[p] = hashlib.sha256(raw).hexdigest()
        assert historical[p] == search.file_hash(REPO / p) == expected, p
    phase_a_audit = subprocess.run([sys.executable, str(BENCH / 'h001-a/audit.py')],
                                 cwd=REPO, text=True, capture_output=True, check=True)
    search.write_json(HERE / 'phase-a-audit.json', json.loads(phase_a_audit.stdout))
    cp, config = search.load_checkpoint(REPO / m['checkpoint_path'], REPO / m['config_path'],
                                        m['checkpoint_sha256'])
    s = cp['state']
    command = shlex.split(m['resume_command'])
    assert command[-2:] == ['--execution-base', '$(git rev-parse origin/main)']
    command[-1] = BASE
    validation_command = command[:2] + ['validate', '--config', m['config_path'],
                          '--checkpoint', m['checkpoint_path'], '--expected-sha256', m['checkpoint_sha256']]
    validation = subprocess.run(validation_command, cwd=REPO, text=True, capture_output=True, check=True)
    search.write_json(HERE / 'checkpoint-validation.json', json.loads(validation.stdout))
    read_files = [
        'README.md', 'methodology.md', 'prompts/codex-goal.md',
        'results/stage3-pr-policy-verification.md', 'results/benchmark-summary.md',
        'results/r45-h001-a-integration-receipt.md']
    read_files += ['benchmarks/r4-5/' + p for p in (
        'goals/H001-A.md', 'goals/H001-B.md', 'problem.md', 'handoff-protocol.md',
        'checkpoint-schema.md', 'h001-a-plan.md', 'h001-a-discovery.md', 'h001-b-discovery.md',
        'research-notes.md', 'proof.md', 'verification.md', 'reviews/H001-A.md',
        'search.py', 'verify.py', 'test_search.py', 'h001-a/audit.py',
        'h001-a/environment.json', 'h001-a/submission-record.json', 'h001-a/handoff-manifest.json',
        'h001-a/test-result.json', 'h001-a/run/run-result.json', 'h001-a/run/progress.jsonl')]
    read_files = sorted(set(read_files) | set(m['artifact_sha256']))
    env = {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
           'machine': platform.machine(), 'dependencies': 'Python standard library only',
           'actual_model': 'missing', 'actual_reasoning_effort': 'missing',
           'metadata_only': True}
    old_env = json.loads((BENCH / 'h001-a/environment.json').read_text())
    changes = {k: {'phase_a': old_env.get(k), 'phase_b': env[k]}
               for k in ('python', 'executable', 'platform', 'machine') if old_env.get(k) != env[k]}
    search.write_json(HERE / 'environment.json', env)
    audit = {'status': 'PASS', 'recorded_at_utc': search.now(), 'phase': 'H001-B',
        'session_start_unix': SESSION_START, 'session_start_source': 'goal service createdAt, second resolution',
        'deadline_utc': '2026-09-22T09:15:00Z', 'execution_base': BASE, 'phase_a_merge_commit': MERGE,
        'audit_head': git('rev-parse', 'HEAD'), 'fresh_session': True,
        'phase_a_conversation_supplied': False, 'extra_user_questions': 0,
        'manifest_path': str(manifest_path.relative_to(REPO)), 'manifest_sha256': search.file_hash(manifest_path),
        'checkpoint_path': m['checkpoint_path'], 'checkpoint_sha256': m['checkpoint_sha256'],
        'checkpoint_schema': cp['schema'], 'state_sha256': cp['state_sha256'],
        'code_commit_phase_a': cp['code_commit'], 'code_sha256': cp['code_sha256'],
        'config_path': m['config_path'], 'config_sha256': cp['config_sha256'],
        'artifact_hashes_verified_against_git_and_manifest': historical,
        'code_config_changed_before_resume': False,
        'consumed_interval': [0, 2000000], 'last_completed_candidate_index': 1999999,
        'next_candidate_index': s['next_candidate_index'], 'remaining_interval': [2000000, 10000000],
        'remaining_candidate_budget': 8000000, 'research_evaluations_before_audit': 0,
        'state_summary': {k: v for k, v in s.items() if k not in ('graph', 'best_graph', 'certificates')},
        'graph_state_source': m['checkpoint_path'] + '#state (all fields validated)',
        'missing_or_ambiguous_semantic_fields': [],
        'metadata_caveats': ['Phase A manifest preserves submission-time UNREVIEWED; merged review and integration receipt establish ACCEPTED. This is historical review metadata, not semantic search state.'],
        'environment_differences': changes,
        'manifest_resume_command': m['resume_command'], 'resolved_resume_argv': command,
        'resolved_resume_command': shlex.join(command),
        'actual_launch_command': 'python3 benchmarks/r4-5/h001-b/run_resume.py',
        'observer': 'runpy executes unchanged search.py CLI with identical argv; first step entry is observed without state mutation and profiling is immediately disabled',
        'files_read_during_reconstruction': {p: search.file_hash(REPO / p) for p in read_files}}
    search.write_json(HERE / 'startup-audit.json', audit)
    print(json.dumps({'status': 'PASS', 'manifest_sha256': audit['manifest_sha256'],
                      'next_candidate_index': s['next_candidate_index'], 'remaining': 8000000,
                      'hashed_artifacts': len(historical), 'environment_differences': changes}, indent=2))


if __name__ == '__main__':
    main()
