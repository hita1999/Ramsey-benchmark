#!/usr/bin/env python3
"""Adversarial checks for the proof and encoding trust boundary."""
import argparse
import gzip
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import audit_cases


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--checker',type=Path,required=True)
    args=p.parse_args()
    passed=[]
    unsat='p cnf 1 2\n1 0\n-1 0\n'
    sat='p cnf 2 2\n1 2 0\n-1 2 0\n'
    xor_unsat='p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n'
    examples=[
        ('valid_unit_conflict',unsat,'3 0 1 2 0\n',True),
        ('valid_resolution_chain',xor_unsat,'5 2 0 1 2 0\n6 -2 0 3 4 0\n7 0 5 6 0\n',True),
        ('duplicate_id',xor_unsat,'5 2 0 1 2 0\n5 -2 0 3 4 0\n7 0 5 5 0\n',False),
        ('valid_unit_but_missing_empty',sat,'3 2 0 1 2 0\n',False),
        ('nonunit_hint',sat,'3 0 1 2 0\n',False),
        ('missing_conflict',unsat,'3 0 1 0\n',False),
        ('unknown_hint',unsat,'3 0 1 9 0\n',False),
        ('forward_reference',unsat,'3 0 4 0\n4 1 0 1 0\n',False),
        ('out_of_range_literal',unsat,'3 2 0 1 2 0\n4 0 1 2 0\n',False),
        ('empty_proof',unsat,'',False),
        ('unsupported_rat',unsat,'3 0 -1 2 0\n',False),
        ('truncated_hints',unsat,'3 0 1 2\n',False),
        ('header_count',unsat.replace('1 2','1 3'),'3 0 1 2 0\n',False),
        ('forged_empty_without_hints',sat,'3 0 0\n',False),
    ]
    with tempfile.TemporaryDirectory(prefix='r45-test-') as temp:
        temp=Path(temp)
        for name,cnf,proof,accept in examples:
            (temp/'test.cnf').write_text(cnf)
            (temp/'test.lrat').write_text(proof)
            proc=subprocess.run([str(args.checker),str(temp/'test.cnf'),str(temp/'test.lrat')],
                                capture_output=True,text=True)
            if (proc.returncode==0)!=accept:
                raise RuntimeError(f'{name}: unexpected checker result: {proc.stdout} {proc.stderr}')
            passed.append(name)
        original=audit_cases.ROOT
        shutil.copytree(original/'data',temp/'data')
        (temp/'proofs').mkdir()
        cases=json.loads((original/'results'/'coverage16-cases.json').read_text())
        case=next(c for c in cases if c['blocked_assignments'])
        name=case['name']
        for suffix in ['cnf.gz','witnesses.json.gz']:
            shutil.copy(original/'proofs'/f'{name}.{suffix}',temp/'proofs')
        audit_cases.ROOT=temp
        audit_cases.inspect(case)
        passed.append('valid_coverage_encoding')
        cnfpath=temp/'proofs'/f'{name}.cnf.gz'
        original_cnf=cnfpath.read_bytes()
        # Flip the sign of one actual clause literal, preserving a valid header.
        text=gzip.decompress(original_cnf).decode().splitlines()
        fields=text[1].split()
        fields[0]=str(-int(fields[0]))
        text[1]=' '.join(fields)
        cnfpath.write_bytes(gzip.compress(('\n'.join(text)+'\n').encode()))
        try:
            audit_cases.inspect(case)
        except ValueError:
            passed.append('reject_altered_cnf_literal')
        else:
            raise RuntimeError('corrupt encoding accepted')
        cnfpath.write_bytes(original_cnf)
        wp=temp/'proofs'/f'{name}.witnesses.json.gz'
        witnesses=json.loads(gzip.decompress(wp.read_bytes()))
        witnesses[0]['permutation'][0]=witnesses[0]['permutation'][1]
        wp.write_bytes(gzip.compress(json.dumps(witnesses).encode()))
        try:
            audit_cases.inspect(case)
        except ValueError:
            passed.append('reject_nonbijective_isomorphism')
        else:
            raise RuntimeError('corrupt isomorphism accepted')
        audit_cases.ROOT=original
    print(json.dumps({'status':'PASS','tests':passed,'count':len(passed)},indent=2))


if __name__=='__main__':
    main()
