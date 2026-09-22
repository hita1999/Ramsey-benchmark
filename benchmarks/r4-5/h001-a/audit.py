#!/usr/bin/env python3
"""Read-only Phase A artifact audit. Never calls a search transition."""
import json
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCHMARK = HERE.parent
REPO = HERE.parents[2]
sys.path.insert(0, str(BENCHMARK))
import search


def main():
    m = json.loads((HERE / 'handoff-manifest.json').read_text())
    for relative, expected in m['artifact_sha256'].items():
        assert search.file_hash(REPO / relative) == expected, relative
    cp, config = search.load_checkpoint(REPO / m['checkpoint_path'], REPO / m['config_path'],
                                        m['checkpoint_sha256'])
    s = cp['state']
    assert m['phase_completed'] == cp['phase'] == 'H001-A'
    assert m['overall_experiment_status'] == 'PARTIAL_PROGRESS'
    assert m['termination_reason'] == 'MANDATORY_HANDOFF_CHECKPOINT'
    assert m['consumed_research_interval'] == cp['consumed_research_interval'] == [0, 2000000]
    assert m['next_candidate_index'] == s['next_candidate_index'] == 2000000
    assert m['last_completed_candidate_index'] == 1999999
    assert m['remaining_research_interval'] == [2000000, 10000000]
    assert m['remaining_candidate_evaluations'] == 8000000
    assert m['phase_b_research_evaluations_consumed'] == m['research_replay_evaluations'] == 0
    for key, state_key in [('current_target', 'target_n'), ('current_score', 'score'),
                           ('best_score', 'best_score'), ('prng_state', 'prng_state'),
                           ('restart', 'restart'), ('iteration', 'iteration'),
                           ('target_evaluations', 'target_evaluations'), ('search_mode', 'mode')]:
        assert m[key] == s[state_key], key
    assert m['code_commit'] == cp['code_commit']
    assert m['execution_base'] == cp['execution_base']
    assert m['config_sha256'] == cp['config_sha256']
    assert m['code_sha256'] == cp['code_sha256']
    assert m['state_sha256'] == cp['state_sha256']
    for name, expected in cp['code_sha256'].items():
        data = subprocess.check_output(['git', 'show', cp['code_commit'] + ':benchmarks/r4-5/' + name], cwd=REPO)
        assert search.hashlib.sha256(data).hexdigest() == expected
    config_bytes = subprocess.check_output(['git', 'show', cp['code_commit'] + ':benchmarks/r4-5/h001-a/config.json'], cwd=REPO)
    assert search.hashlib.sha256(config_bytes).hexdigest() == cp['config_sha256']
    for cert in s['certificates']:
        saved = json.loads((HERE / 'run/certificates' / ('n%02d.json' % cert['n'])).read_text())
        assert saved == cert and search.verify(saved)['valid']
    cert = json.loads((HERE / 'run/certificate.json').read_text())
    assert cert == s['certificates'][-1]
    assert search.verify(cert)['lower_bound'] == 24
    best = json.loads((HERE / 'run/best-so-far.json').read_text())
    assert best['graph'] == search.graph_certificate(s['best_graph'])
    assert best['score'] == s['best_score'] == 4
    test = json.loads((HERE / 'test-result.json').read_text())
    assert test['status'] == 'PASS' and test['candidate_evaluations'] == 556
    assert test['code_sha256'] == cp['code_sha256']
    assert test['test_code_sha256'] == search.file_hash(BENCHMARK / 'test_search.py')
    run = json.loads((HERE / 'run/run-result.json').read_text())
    assert run['consumed_interval'] == [0, 2000000]
    assert run['research_evaluations'] == 2000000
    assert run['checkpoint_sha256'] == m['checkpoint_sha256']
    progress = [json.loads(line) for line in (HERE / 'run/progress.jsonl').read_text().splitlines()]
    assert [row['next_candidate_index'] for row in progress] == list(range(100000, 2000001, 100000))
    tokens = shlex.split(m['resume_command'])
    assert tokens[:3] == ['python3', 'benchmarks/r4-5/search.py', 'resume']
    assert tokens[tokens.index('--expected-sha256') + 1] == m['checkpoint_sha256']
    assert tokens[tokens.index('--out') + 1] == 'benchmarks/r4-5/h001-b/run'
    print(json.dumps({'status': 'PASS', 'checked_at_utc': search.now(),
                      'scope': 'read-only Git/code/config/checkpoint/certificate/test/interval/manifest audit',
                      'hashed_artifacts': len(m['artifact_sha256']), 'certificates': len(s['certificates']),
                      'next_candidate_index': s['next_candidate_index'],
                      'research_evaluations_consumed_by_audit': 0,
                      'phase_b_resume_command_executed': False,
                      'checkpoint_sha256': m['checkpoint_sha256']}, indent=2))


if __name__ == '__main__':
    main()
