# Independent R(4,5) proof audit — PARTIAL_PROGRESS

This is mathematical verification of `research/r4-5/`, outside the completed
benchmark. **The full upper bound `R(4,5) <= 25` is not proved by this work.**

Verified in this session:

- A new C++ implementation exhausts all four- and five-subsets of the
  24-vertex witness, independently of the existing Python verifier.
- A written proof derives the degree-8/10/12 reduction from elementary
  smaller upper bounds, without citing exact Ramsey values as assumptions.
- All 268,435,456 labeled eight-vertex graphs are checked against the 179
  `(3,5,8)` representatives and all their permutations.
- The two `(4,4,16)` representatives form a complete cover. This follows
  from complete small catalogues and **54 independently checked LRAT
  refutations**, with 128 checked permutation witnesses for blocked models.
- All 358 degree-8 gluing CNFs are checked against a second encoding that
  enumerates every forbidden subset, including the splitting vertex.
- Saved gluing refutations are independently checked. The exact completed
  subset and all remaining cases are in [CHECKPOINT.json](CHECKPOINT.json)
  and [UNRESOLVED.md](UNRESOLVED.md). Do not infer completion from solver logs.

The [proof and trust-boundary document](PROOF.md) separates these results from
the cited 1995 theorem and 2024 HOL4 proof. HOL4 was not replayed. The checker
is independent of CaDiCaL but is not itself formally verified in a logic kernel.

## Files

- `data/`: four small graph6 inputs, with URLs/hashes in `PROVENANCE.json`.
- `src/`: independent finite checkers, certificate producer, runner, and tests.
- `proofs/`: exact DIMACS CNFs, text LRAT proofs, and blocking permutations,
  gzip-compressed. Proofs can be replayed without installing any SAT solver.
- `results/`: actual enumeration counts, complete case indices, per-case
  proof hashes/checker results, encoding audits, and adversarial tests.
- `ARTIFACTS.sha256`: hashes binding the saved evidence and sources.

## Replay without a SAT solver

From the repository root, with Python 3.9+ and a C++17 compiler:

```sh
bash research/r4-5/independent/reproduce.sh
```

This compiles the independent checkers in a temporary directory, reruns all
three small catalogue checks, both encoding audits and the lower-bound check,
tests rejection of corrupt inputs, and replays every saved proof. It reports
missing gluing proofs explicitly and preserves the saved original results.
Successful replay validates the checkpoint's subset, not the full theorem.

To create further certificates, build the pinned CaDiCaL revision described
in `PROVENANCE.json`. Then run, using your actual executable paths:

```sh
clang++ -O2 -std=c++17 research/r4-5/independent/src/check_lrat.cpp -o /tmp/r45-check-lrat
python3 research/r4-5/independent/src/run_proofs.py degree8 \
  --solver /path/to/cadical --checker /tmp/r45-check-lrat --jobs 4 \
  --budget-seconds 600
```

The runner rechecks existing proofs, generates missing ones, and accepts
only proofs passing the independent checker. A budget stop is unresolved;
it is not UNSAT. The budget stops scheduling fresh cases; already running
solver/checker calls can run up to their per-call timeout. The separate
encoding audit must also pass before using a proof mathematically.

The committed CNFs can be regenerated with `build_cases.py coverage16` and
`build_cases.py degree8`. Their decompressed bytes are deterministic; gzip
headers need not be. Recheck generated files with `audit_cases.py` before use.

Initial budget: 30 minutes beginning 2026-10-25 15:09:48 JST. The checkpoint
records its capture time and leaves degrees 10 and 12 explicitly unresolved.
No claim of a new discovery or a complete independent proof is made.
