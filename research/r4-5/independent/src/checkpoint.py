#!/usr/bin/env python3
"""Bind checked artifacts to a conservative ledger; does not prove UNSAT itself."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import audit_cases

ROOT=Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ledger=[]
    counts={}
    for suite in ['coverage16','degree8']:
        cases=json.loads((ROOT/'results'/f'{suite}-cases.json').read_text())
        records={r['name']:r for r in json.loads((ROOT/'results'/f'{suite}-proofs.json').read_text())}
        verified=0
        for case in cases:
            name=case['name']
            record=records.get(name,{})
            status=record.get('status','NOT_ATTEMPTED')
            if status=='VERIFIED_UNSAT':
                for extension,key in [('cnf','cnf_sha256'),('lrat','lrat_sha256')]:
                    path=ROOT/'proofs'/f'{name}.{extension}.gz'
                    if not path.exists() or digest(gzip.decompress(path.read_bytes()))!=record[key]:
                        raise ValueError(f'{name}: certificate/result hash mismatch')
                verified+=1
            ledger.append({'name':name,'suite':suite,'status':status})
        counts[suite]={'total':len(cases),'verified_unsat':verified,'unresolved':len(cases)-verified}
    invariants=[]
    for edges in audit_cases.graphs('r44_16.g6',16):
        adjacency=[{w for w in range(16) if audit_cases.pair(v,w) in edges} for v in range(16)]
        pairs=sum(len(adjacency[x])==len(adjacency[y])==7 and
                  (x,y) not in edges and len(adjacency[x]&adjacency[y])==2
                  for y in range(16) for x in range(y))
        invariants.append(pairs)
    if invariants!=[0,8]:
        raise ValueError('unexpected distinguishing invariant')
    (ROOT/'results'/'r44_16-invariants.json').write_text(json.dumps({
        'invariant':'nonadjacent degree-7 pairs with exactly two common neighbors',
        'values':invariants,'nonisomorphic':True},indent=2)+'\n')
    now=datetime.now(timezone.utc)
    start=datetime(2026,10,25,6,9,48,tzinfo=timezone.utc)
    checkpoint={
        'status':'PARTIAL_PROGRESS','session_started_utc':start.isoformat(),
        'checkpoint_captured_utc':now.isoformat(),
        'initial_budget_seconds':1800,'elapsed_at_capture_seconds':round((now-start).total_seconds(),3),
        'base_commit':'d0bb92156a727be7baa8a8eee6140fff7035592f',
        'branch':'codex/r45-independent-verification',
        'lower_bound':'INDEPENDENTLY_VERIFIED_R45_GE_25',
        'degree_reduction':'WRITTEN_PROOF_FROM_ELEMENTARY_SMALL_UPPER_BOUNDS',
        'r35_8_catalogue':'COMPLETE_BY_ALL_2_POW_28_LABELED_GRAPHS',
        'r44_16_catalogue':'COMPLETE_BY_SMALL_ENUMERATIONS_AND_54_CHECKED_REFUTATIONS',
        'proof_counts':counts,'degree10':'NOT_ATTEMPTED','degree12':'NOT_ATTEMPTED',
        'full_upper_bound_independently_proved':False,'hol4_replayed':False,
        'cases':ledger}
    (ROOT/'CHECKPOINT.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
    missing=[c['name'] for c in ledger if c['suite']=='degree8' and c['status']!='VERIFIED_UNSAT']
    lines=['# Unresolved obligations — PARTIAL_PROGRESS','',
           f'Degree 8: {counts["degree8"]["verified_unsat"]}/358 gluing certificates verified.',
           'Both candidate catalogues are complete; the remaining gluing cases are listed below.',
           '', 'Degrees 10 and 12: candidate coverage and gluing exclusion have not been checked.',
           'The full upper bound and equality are not independently established here.', '',
           'Next: generate and check the missing gluing certificates using the saved CNFs,',
           'then construct independently checked covers and gluing certificates for degrees 10 and 12.',
           'A timeout, interrupted run, or absent proof is unresolved, never evidence of nonexistence.',
           '', '## Missing degree-8 refutations', '']
    lines.extend('- `'+name+'`' for name in missing)
    if not missing:
        lines.append('None. Degree 8 is closed; degrees 10 and 12 remain open.')
    (ROOT/'UNRESOLVED.md').write_text('\n'.join(lines)+'\n')
    artifacts=[]
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or path.suffix=='.pending':
            continue
        if path.name=='ARTIFACTS.sha256':
            continue
        artifacts.append(f'{digest(path.read_bytes())}  {path.relative_to(ROOT)}')
    (ROOT/'ARTIFACTS.sha256').write_text('\n'.join(artifacts)+'\n')
    print(json.dumps({'status':'PARTIAL_PROGRESS','counts':counts,'hashed_files':len(artifacts)}))


if __name__=='__main__':
    main()
