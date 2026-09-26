#!/usr/bin/env python3
"""Read-only self-audit of Phase B. No search transitions and no research replay."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BENCH = HERE.parent
sys.path.insert(0, str(BENCH))
import search


def read(path):
    return json.loads(path.read_text())


def historical(commit, relative):
    return subprocess.check_output(['git', 'show', commit + ':' + relative], cwd=REPO)


def main():
    startup = read(HERE / 'startup-audit.json')
    first = read(HERE / 'first-candidate.json')
    a = read(BENCH / 'h001-a/run/checkpoint.json')
    m = read(BENCH / 'h001-a/handoff-manifest.json')
    run = read(HERE / 'run/run-result.json')
    process = read(HERE / 'run/startup-audit.json')
    cp, config = search.load_checkpoint(HERE / 'run/checkpoint.json', REPO / m['config_path'], run['checkpoint_sha256'])
    s = cp['state']
    tests = read(HERE / 'test-result.json')
    for p, sha in m['artifact_sha256'].items():
        assert search.file_hash(REPO / p) == sha, p
    assert search.file_hash(REPO / startup['manifest_path']) == startup['manifest_sha256']
    assert startup['status'] == 'PASS' and startup['extra_user_questions'] == 0
    assert startup['missing_or_ambiguous_semantic_fields'] == []
    assert first['first_resumed_candidate_index'] == process['start_index'] == a['state']['next_candidate_index'] == 2000000
    assert first['state_sha256_before_first_transition'] == a['state_sha256']
    assert first['startup_audit_sha256'] == search.file_hash(HERE / 'startup-audit.json')
    assert startup['remaining_interval'] == run['consumed_interval'] == [2000000, 10000000]
    assert run['research_evaluations'] == 8000000
    assert s['next_candidate_index'] == 10000000
    assert cp['consumed_research_interval'] == [0, 10000000]
    assert cp['phase'] == 'H001-B' and cp['execution_base'] == startup['execution_base']
    assert cp['code_commit'] == process['code_commit']
    assert cp['code_sha256'] == a['code_sha256'] and cp['config_sha256'] == a['config_sha256']
    for p in ('startup-audit.json', 'run_resume.py', 'test-result.json'):
        relative = 'benchmarks/r4-5/h001-b/' + p
        assert historical(cp['code_commit'], relative) == (HERE / p).read_bytes()
    for p, sha in m['code_sha256'].items():
        assert hashlib.sha256(historical(cp['code_commit'], 'benchmarks/r4-5/' + p)).hexdigest() == sha
    assert hashlib.sha256(historical(cp['code_commit'], m['config_path'])).hexdigest() == m['config_sha256']
    rows = [json.loads(line) for line in (HERE / 'run/progress.jsonl').read_text().splitlines()]
    assert [r['next_candidate_index'] for r in rows] == list(range(2100000, 10000001, 100000))
    assert all(x['elapsed_seconds'] < y['elapsed_seconds'] for x, y in zip(rows, rows[1:]))
    assert all(rows[-1][k] == s[k] for k in ('next_candidate_index', 'target_n', 'score', 'best_score'))
    assert s['certificates'][:len(a['state']['certificates'])] == a['state']['certificates']
    assert s['completed_targets'][:len(a['state']['completed_targets'])] == a['state']['completed_targets']
    verification = []
    for cert in s['certificates']:
        p = HERE / 'run/certificates' / ('n%02d.json' % cert['n'])
        assert read(p) == cert
        v = search.verify(cert)
        assert v['valid']
        verification.append({'path': str(p.relative_to(REPO)), 'sha256': search.file_hash(p), **v})
    assert read(HERE / 'run/certificate.json') == s['certificates'][-1]
    best = read(HERE / 'run/best-so-far.json')
    assert best == {'target_n': s['target_n'], 'score': s['best_score'],
                    'graph': search.graph_certificate(s['best_graph']) if s['best_graph'] is not None else None,
                    'valid_certificate': False}
    assert tests['status'] == 'PASS' and tests['candidate_evaluations'] == 556
    assert tests['code_sha256'] == m['code_sha256']
    assert tests['test_code_sha256'] == search.file_hash(BENCH / 'test_search.py')
    original_tests = read(BENCH / 'h001-a/test-result.json')
    assert tests == original_tests, 'Identical test configuration must produce identical semantic results'
    with tempfile.TemporaryDirectory() as temp:
        d = Path(temp)
        shutil.copyfile(BENCH / 'verify.py', d / 'verify.py')
        shutil.copyfile(HERE / 'run/certificate.json', d / 'certificate.json')
        result = subprocess.run([sys.executable, '-I', 'verify.py', 'certificate.json'], cwd=d,
                                text=True, capture_output=True, check=True)
        isolated = {'status': 'PASS', 'classification': 'researcher self-audit, not independent review',
                    'command': [sys.executable, '-I', 'verify.py', 'certificate.json'],
                    'inputs': ['verify.py', 'certificate.json'], 'output': json.loads(result.stdout),
                    'research_candidate_evaluations': 0}
    search.write_json(HERE / 'certificate-verification.json', verification)
    search.write_json(HERE / 'isolated-verification.json', isolated)
    search.write_json(HERE / 'final-checkpoint-validation.json', {
        'status': 'PASS', 'checkpoint_sha256': search.file_hash(HERE / 'run/checkpoint.json'),
        'state_sha256': cp['state_sha256'], 'next_candidate_index': s['next_candidate_index'],
        'research_evaluations_consumed': 0})
    result = {'handoff_evaluation': 'PASS', 'evaluation_owner': 'researcher self-audit',
        'independent_review_status': 'UNREVIEWED', 'goal': 'H001-B', 'goal_status': 'SOLVED',
        'research_stop_reason': 'PHASE_B_INTERVAL_COMPLETE', 'mathematical_problem_status': 'PARTIAL_PROGRESS',
        'checked_at_utc': search.now(), 'execution_base': cp['execution_base'],
        'executing_code_commit': cp['code_commit'],
        'first_resumed_candidate_index': first['first_resumed_candidate_index'],
        'final_global_candidate_index': s['next_candidate_index'], 'last_evaluated_candidate_index': 9999999,
        'phase_a_interval': [0, 2000000], 'phase_b_interval': run['consumed_interval'],
        'combined_interval': cp['consumed_research_interval'], 'phase_b_candidate_evaluations': 8000000,
        'repeated_research_candidate_count': 0, 'gap_candidate_count': 0,
        'interval_evidence': 'First-step observer anchors complete S(2000000); immutable advance calls step once per iteration and step increments index once. 80 successive 100000-candidate progress blocks end at S(10000000). Only one launch; no research replay. This is code/counter evidence, not an independent 10M-trajectory replay.',
        'seconds_from_session_start_to_first_candidate': first['seconds_from_session_start'],
        'search_seconds_including_serialization_validation': run['elapsed_seconds_including_serialization_validation'],
        'extra_user_questions': 0, 'missing_or_ambiguous_semantic_fields': 0,
        'code_config_changes_before_or_during_resume': False,
        'semantic_drift': False, 'observer_semantic_mutations': 0,
        'test_replay_candidate_evaluations_phase_b': tests['candidate_evaluations'],
        'test_replay_candidate_evaluations_both_phases': 1112,
        'delta_comparisons_phase_b': tests['delta_comparisons'],
        'phase_a_research_trajectory_replay_evaluations': 0,
        'split_resume_equivalence': 'PASS: all semantic fields and canonical bytes, three preregistered cases; results identical to Phase A',
        'new_certificate_orders': [c['n'] for c in s['certificates'][len(a['state']['certificates']):]],
        'strongest_certificate': verification[-1], 'final_target_n': s['target_n'],
        'final_score': s['score'], 'best_score': s['best_score'],
        'final_checkpoint_sha256': search.file_hash(HERE / 'run/checkpoint.json'),
        'final_state_sha256': cp['state_sha256'], 'research_evaluations_consumed_by_audit': 0,
        'limitations': ['Fresh-session/no prior conversation is session provenance attestation; Git preserves the audit, not a proof of absence of hidden context.',
                       'Small split tests establish tested serialization cases; the full 10M uninterrupted trajectory was not recomputed.',
                       'Independent Phase B review and PR integration are pending.']}
    search.write_json(HERE / 'handoff-evaluation.json', result)
    paths = sorted(p for p in (HERE / 'run').rglob('*') if p.is_file())
    paths += [HERE / p for p in ('startup-audit.json', 'first-candidate.json', 'test-result.json',
              'checkpoint-validation.json', 'final-checkpoint-validation.json', 'certificate-verification.json',
              'isolated-verification.json', 'handoff-evaluation.json', 'audit.py', 'startup_audit.py', 'run_resume.py')]
    search.write_json(HERE / 'artifact-manifest.json', {
        'schema': 'r45-h001-b-artifacts-v1', 'execution_base': cp['execution_base'],
        'executing_code_commit': cp['code_commit'],
        'artifact_sha256': {str(p.relative_to(REPO)): search.file_hash(p) for p in paths},
        'manifest_excludes_itself': True, 'source_checkpoint_sha256': m['checkpoint_sha256']})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
