#!/usr/bin/env python3
"""Independent graph6 decoder, direct all-subsets CNF audit and witness check.

Imports neither build_cases.py nor any graph/SAT library. Checks constants for
all forbidden subsets INCLUDING the splitting vertex, then compares clauses.
"""
import argparse
from collections import Counter
import gzip
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graphs(name, n):
    result = []
    for line in (ROOT/'data'/name).read_bytes().splitlines():
        require(len(line) == 1+(n*(n-1)//2+5)//6 and line[0]-63 == n,
                'invalid graph6 size')
        require(all(63 <= x <= 126 for x in line), 'invalid graph6 byte')
        edges = set()
        for y in range(1,n):
            for x in range(y):
                offset = y*(y-1)//2+x
                if (line[1+offset//6]-63) & (1 << (5-offset%6)):
                    edges.add((x,y))
        for offset in range(n*(n-1)//2, 6*(len(line)-1)):
            require(not (line[1+offset//6]-63) & (1 << (5-offset%6)), 'padding')
        result.append(edges)
    return result


def pair(x,y):
    return (min(x,y),max(x,y))


def ramsey(edges,n,s,t):
    for k,color in [(s,True),(t,False)]:
        for q in itertools.combinations(range(n),k):
            require(not all((e in edges) == color for e in itertools.combinations(q,2)),
                    f'forbidden {k}-subset: {q}')


def inspect(case):
    d=case['degree']
    coverage=case['suite']=='coverage16'
    bsize=15-d if coverage else 16
    n=d+bsize+1
    if coverage:
        aa=graphs(f'r34_{d}.g6',d)
        raw=graphs(f'r34_{bsize}.g6',bsize)
        bb=[set(itertools.combinations(range(bsize),2))-g for g in raw]
        s,t=4,4
    else:
        aa,bb=graphs('r35_8.g6',8),graphs('r44_16.g6',16)
        s,t=4,5
    a,b=aa[case['a']],bb[case['b']]
    ramsey(a,d,s-1,t)
    ramsey(b,bsize,s,t-1)
    fixed={}
    variables={}
    for x,y in itertools.combinations(range(n),2):
        if y==n-1:
            fixed[(x,y)]=x<d
        elif y<d:
            fixed[(x,y)]=(x,y) in a
        elif x>=d:
            fixed[(x,y)]=(x-d,y-d) in b
        else:
            variables[(x,y)]=1+x*bsize+(y-d)
    clauses=[]
    for k,color in [(s,True),(t,False)]:
        for q in itertools.combinations(range(n),k):
            clause=[]
            for e in itertools.combinations(q,2):
                if e in fixed:
                    if fixed[e] != color:
                        break  # This forbidden pattern is already impossible.
                else:
                    clause.append((-1 if color else 1)*variables[e])
            else:
                clauses.append(tuple(sorted(clause)))
    if coverage:
        target_graphs=graphs('r44_16.g6',16)
        with gzip.open(ROOT/'proofs'/f'{case["name"]}.witnesses.json.gz','rt') as f:
            witnesses=json.load(f)
        require(len(witnesses)==case['blocked_assignments'],'witness count')
        masks=set()
        for w in witnesses:
            require(type(w['target']) is int and 0 <= w['target'] < len(target_graphs), 'target index')
            target=target_graphs[w['target']]
            p=w['permutation']
            require(len(p)==n and sorted(p)==list(range(n)), 'not a permutation')
            mask=w['mask']
            require(type(mask) is int and 0 <= mask < 1 << (d*bsize),'bad assignment')
            require(mask not in masks,'duplicate witness')
            masks.add(mask)
            for e,value in fixed.items():
                require((pair(p[e[0]],p[e[1]]) in target)==value,'fixed-edge witness mismatch')
            for e,var in variables.items():
                require((pair(p[e[0]],p[e[1]]) in target)==bool(mask >> (var-1) & 1),
                        'cross-edge witness mismatch')
            clauses.append(tuple(sorted(-(v+1) if mask >> v & 1 else v+1
                                        for v in range(d*bsize))))
    path=ROOT/'proofs'/f'{case["name"]}.cnf.gz'
    with gzip.open(path,'rt') as f:
        lines=f.read().splitlines()
    require(lines[0].split()==['p','cnf',str(d*bsize),str(len(lines)-1)],'CNF header')
    actual=[]
    for line in lines[1:]:
        lits=list(map(int,line.split()))
        require(lits and lits[-1]==0 and all(0 < abs(v) <= d*bsize for v in lits[:-1]),'bad clause')
        actual.append(tuple(sorted(lits[:-1])))
    require(Counter(actual)==Counter(clauses),'CNF differs from all-subsets semantics')
    require(case['variables']==d*bsize and case['clauses']==len(actual),'metadata mismatch')
    return len(clauses)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('suite',choices=['coverage16','degree8'])
    args=parser.parse_args()
    cases=json.loads((ROOT/'results'/f'{args.suite}-cases.json').read_text())
    expected={(d,a,b) for d,na,nb in ([(7,9,3),(8,3,9)] if args.suite=='coverage16' else [(8,179,2)])
              for a in range(na) for b in range(nb)}
    require(len(cases)==len(expected),'missing/extra cases')
    require({(c['degree'],c['a'],c['b']) for c in cases}==expected,'wrong case index set')
    require(len({c['name'] for c in cases})==len(cases),'duplicate filenames')
    require(all(c['suite']==args.suite for c in cases),'wrong suite')
    for edges in graphs('r44_16.g6',16):
        ramsey(edges,16,4,4)
    count=sum(inspect(case) for case in cases)
    print(json.dumps({'suite':args.suite,'cases_audited':len(cases),
                      'clauses_audited':count,'status':'VERIFIED_ENCODING_AND_WITNESSES'}))


if __name__=='__main__':
    main()
