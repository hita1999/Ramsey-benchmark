#!/usr/bin/env python3
"""Run (or only replay) proofs. Solver status alone NEVER gives VERIFIED_UNSAT."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import threading
import signal
import time

ROOT=Path(__file__).resolve().parents[1]


def trim_proof(data):
    """Untrusted dependency-cone extraction; the result must pass the checker."""
    needed=set()
    kept=[]
    for line in reversed(data.splitlines()):
        fields=line.split(maxsplit=2)
        if len(fields)<3 or fields[0]==b'c' or fields[1]==b'd':
            continue
        ident=int(fields[0])
        if not kept and fields[1]==b'0':
            needed.add(ident)
        if ident not in needed:
            continue
        tokens=list(map(int,line.split()))
        separator=tokens.index(0,1)
        hints=tokens[separator+1:-1]
        if any(h<=0 for h in hints):
            raise ValueError('trim only supports positive RUP hints')
        needed.update(hints)
        kept.append(line)
    if not kept:
        raise ValueError('no empty clause to trim')
    return b'\n'.join(reversed(kept))+b'\n'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('suite',choices=['coverage16','degree8'])
    p.add_argument('--solver',type=Path)
    p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--timeout',type=int,default=60)
    p.add_argument('--jobs',type=int,default=1)
    p.add_argument('--budget-seconds',type=int,default=0)
    p.add_argument('--available-only',action='store_true')
    p.add_argument('--report',type=Path)
    args=p.parse_args()
    cases=json.loads((ROOT/'results'/f'{args.suite}-cases.json').read_text())
    if args.available_only:
        cases=[c for c in cases if (ROOT/'proofs'/f'{c["name"]}.lrat.gz').exists()]
    results=[]
    output=args.report or ROOT/'results'/f'{args.suite}-proofs.json'
    stop=threading.Event()
    signal.signal(signal.SIGINT,lambda *_:stop.set())
    deadline=time.monotonic()+args.budget_seconds if args.budget_seconds else float('inf')
    def process(case):
      if stop.is_set() or time.monotonic()>=deadline:
        return {'name':case['name'],'status':'NOT_ATTEMPTED_BUDGET'}
      with tempfile.TemporaryDirectory(prefix='r45-proof-') as temp:
        cnf,proof=Path(temp)/'case.cnf',Path(temp)/'case.lrat'
        start=time.monotonic()
        name=case['name']
        cnf.write_bytes(gzip.decompress((ROOT/'proofs'/f'{name}.cnf.gz').read_bytes()))
        saved=ROOT/'proofs'/f'{name}.lrat.gz'
        result={'name':name}
        try:
                generated=False
                if args.solver and not saved.exists():
                    command=[str(args.solver),'--plain','--lrat','--no-binary','-q',
                             str(cnf),str(proof)]
                    proc=subprocess.run(command,capture_output=True,text=True,timeout=args.timeout)
                    result.update(solver_returncode=proc.returncode,solver_stdout=proc.stdout,
                                  solver_stderr=proc.stderr)
                    if proc.returncode!=20:
                        raise ValueError('solver did not finish UNSAT')
                    generated=True
                else:
                    proof.write_bytes(gzip.decompress(saved.read_bytes()))
                if args.solver:
                    result['untrimmed_lrat_bytes']=proof.stat().st_size
                    proof.write_bytes(trim_proof(proof.read_bytes()))
                check=subprocess.run([str(args.checker),str(cnf),str(proof)],
                                     capture_output=True,text=True,timeout=args.timeout)
                if check.returncode:
                    raise ValueError('checker rejected: '+check.stderr)
                result.update(json.loads(check.stdout))
                result.update(cnf_sha256=hashlib.sha256(cnf.read_bytes()).hexdigest(),
                              lrat_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),
                              lrat_bytes=proof.stat().st_size)
                if args.solver:
                    pending=saved.with_suffix('.pending')
                    pending.write_bytes(gzip.compress(proof.read_bytes(),mtime=0))
                    pending.replace(saved)
                result['generated_this_run']=generated
        except (OSError, ValueError, subprocess.TimeoutExpired) as e:
                result.update(status='UNRESOLVED',error=str(e))
        result['elapsed_seconds']=round(time.monotonic()-start,6)
        return result
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for future in as_completed([pool.submit(process,case) for case in cases]):
            result=future.result()
            results.append(result)
            pending=output.with_suffix('.pending')
            pending.write_text(json.dumps(sorted(results,key=lambda r:r['name']),indent=2)+'\n')
            pending.replace(output)
            if len(results)%20==0 or result['status']!='VERIFIED_UNSAT':
                print(json.dumps({'completed':len(results),'total':len(cases),
                                  'last':result['name'],'status':result['status']}),flush=True)
    failures=[r for r in results if r['status']!='VERIFIED_UNSAT']
    print(json.dumps({'suite':args.suite,'checked':len(results),'unresolved':len(failures)}))
    if failures:
        raise SystemExit(1)


if __name__=='__main__':
    main()
