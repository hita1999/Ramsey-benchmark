#!/usr/bin/env python3
"""Recheck merged Stage 4 artifacts in a disposable copy; never run research."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

BASE = '2cbdcd4e1f4758c5d4dc4b427bd408db8a526f3b'
STAGE_ROOT = '63e8067f72b607fdc38c533e39b29e9b135cadf5'
# Fixed before rerun. Compare every other field; do not mask semantic differences.
EXCLUDED = {'phase-a-audit': ['checked_at_utc'],
            'phase-b-audit': ['checked_at_utc'],
            'reviewer-verifier': ['python', 'platform'], 'existing-tests': []}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    gitdir = subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'], cwd=root, text=True).strip()
    report = {'status': 'RUNNING', 'base_commit': BASE, 'utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'platform': platform.platform(), 'executable': sys.executable,
              'research_candidate_evaluations': 0, 'full_trajectory_replay': False,
              'fresh_session_experiment': False, 'new_independent_review': False,
              'excluded_comparison_fields': EXCLUDED, 'runs': [], 'comparisons': {}}
    try:
        with tempfile.TemporaryDirectory(prefix='r45-retrospective-') as temp:
            temp = Path(temp)
            archive = temp / 'source.tar'
            source = temp / 'source'
            source.mkdir()
            subprocess.run(['git', 'archive', '--format=tar', '--output', str(archive), BASE], cwd=root, check=True)
            subprocess.run(['tar', '-xf', str(archive), '-C', str(source)], check=True)
            env = {**os.environ, 'GIT_DIR': gitdir, 'GIT_WORK_TREE': str(source), 'PYTHONDONTWRITEBYTECODE': '1'}
            def git(*argv):
                return subprocess.check_output(['git', *argv], cwd=source, env=env, text=True).strip()
            def run(name, argv):
                result = subprocess.run(argv, cwd=source, env=env, text=True, capture_output=True)
                (output / (name + '.stdout.txt')).write_text(result.stdout)
                (output / (name + '.stderr.txt')).write_text(result.stderr)
                report['runs'].append({'name': name, 'argv': argv, 'returncode': result.returncode,
                                       'cwd': 'disposable archive of base_commit',
                                       'git_object_source': 'original repository, historical read-only git show'})
                if result.returncode:
                    raise RuntimeError(name + ' failed; inspect raw logs')
                return json.loads(result.stdout)
            def compare(name, saved, actual):
                keys = EXCLUDED[name]
                normalize = lambda d: {k: v for k, v in d.items() if k not in keys}
                diff = sorted(k for k in saved.keys() | actual.keys() if saved.get(k) != actual.get(k))
                equal = normalize(saved) == normalize(actual)
                report['comparisons'][name] = {'excluded_keys': keys, 'differing_keys': diff,
                                               'all_nonexcluded_fields_equal': equal, 'json_equal': saved == actual}
                assert equal, name + ' semantic mismatch'
            bench = source / 'benchmarks/r4-5'
            input_paths = sorted(p for p in bench.rglob('*') if p.is_file())
            report['source_sha256'] = {str(p.relative_to(source)): sha(p) for p in input_paths}
            manifests = {}
            for phase, filename in [('a', 'handoff-manifest.json'), ('b', 'artifact-manifest.json')]:
                m = json.loads((bench / ('h001-' + phase) / filename).read_text())
                for p, expected in m['artifact_sha256'].items():
                    assert sha(source / p) == expected, p
                manifests[phase] = {'status': 'PASS', 'artifact_count': len(m['artifact_sha256'])}
            report['input_manifests'] = manifests
            snapshot = json.loads((Path(__file__).parent / 'github-snapshot.json').read_text())
            report['github_snapshot_sha256'] = sha(Path(__file__).parent / 'github-snapshot.json')
            report['merges'] = []
            for pr in snapshot['pull_requests']:
                commit = pr['merge_commit_sha']
                assert pr['merged']
                subprocess.run(['git', 'merge-base', '--is-ancestor', commit, BASE], cwd=source, env=env, check=True)
                parents = git('show', '-s', '--format=%P', commit).split()
                assert parents == [pr['base_sha'], pr['head_sha']]
                trees_equal = git('rev-parse', commit + '^{tree}') == git('rev-parse', pr['head_sha'] + '^{tree}')
                assert trees_equal
                report['merges'].append({'pr': pr['number'], 'merge_sha': commit, 'parents': parents,
                                         'merged_at_github': pr['merged_at'], 'reviewed_head_tree_preserved': trees_equal})
            report['first_parent_commits'] = git('rev-list', '--first-parent', STAGE_ROOT + '..' + BASE).splitlines()
            assert set(report['first_parent_commits']) == {p['merge_commit_sha'] for p in snapshot['pull_requests']}
            report['historical_code_reachable'] = {}
            for commit in ('5cabb7e2ea0f9ccbd237674666031d7d9f67ae3c', 'd1c5cdf7e1dfa3a8750f6aaaaab7fc99248203c3'):
                subprocess.run(['git', 'merge-base', '--is-ancestor', commit, BASE], cwd=source, env=env, check=True)
                report['historical_code_reachable'][commit] = True
            # Audit B writes derived outputs: run it only inside the disposable archive.
            for phase in ('a', 'b'):
                name = 'phase-' + phase + '-audit'
                saved_path = bench / ('h001-' + phase) / ('audit-result.json' if phase == 'a' else 'handoff-evaluation.json')
                saved = json.loads(saved_path.read_text())
                actual = run(name, [sys.executable, 'benchmarks/r4-5/h001-' + phase + '/audit.py'])
                compare(name, saved, actual)
            tests = run('existing-tests', [sys.executable, 'benchmarks/r4-5/test_search.py'])
            compare('existing-tests', json.loads((bench / 'h001-b/test-result.json').read_text()), tests)
            report['retrospective_test_candidate_evaluations'] = tests['candidate_evaluations']
            report['retrospective_delta_comparisons'] = tests['delta_comparisons']
            reviewer = run('reviewer-verifier', [sys.executable, 'benchmarks/r4-5/review/r45-h001-a-independent.py',
                           'benchmarks/r4-5/h001-b/run/certificate.json', '--output', 'reviewer-result.json'])
            saved_path = bench / 'review/r45-h001-a-independent-result.json'
            compare('reviewer-verifier', json.loads(saved_path.read_text()), reviewer)
            report['comparisons']['reviewer-verifier']['byte_equal'] = saved_path.read_bytes() == (source / 'reviewer-result.json').read_bytes()
            write(output / 'reviewer-result.json', reviewer)
            a = json.loads((bench / 'h001-a/run/checkpoint.json').read_text())
            b = json.loads((bench / 'h001-b/run/checkpoint.json').read_text())
            report['intervals'] = {'phase_a': a['consumed_research_interval'],
                                  'phase_b': [a['state']['next_candidate_index'], b['state']['next_candidate_index']],
                                  'combined': b['consumed_research_interval'],
                                  'new_certificates_phase_b': len(b['state']['certificates']) - len(a['state']['certificates'])}
            report['historical_research_and_test_counters_unchanged'] = True
        report['status'] = 'PASS'
    except Exception as exc:
        report['status'] = 'FAIL'
        report['error'] = str(exc)
        raise
    finally:
        write(output / 'report.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_sha256', 'runs')}, indent=2))


if __name__ == '__main__':
    main()
