# R(4,5) H001-A integration receipt

## Status

- Receipt date: 2026-09-22
- Source PR: #15
- Integration result: **PASS**
- H001-A remains: `PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT`
- H001 overall remains: `PARTIAL_PROGRESS`
- Phase B research has not started in this receipt step.

## Merge evidence

PR #15 was merged with a normal merge commit on 2026-09-22T08:33:35Z.

- Merge commit: `5f061f2df33e74e7b416e958ca1e427536763ce9`
- Parent 1: `6031a203863a71cae5a34793c5d87dbc9b24479b`
- Parent 2: `afb386070addbfd5549d21be2a8bc41e2e9acd07`
- GitHub commit verification: verified
- `main` immediately after merge: `5f061f2df33e74e7b416e958ca1e427536763ce9`

This preserves the feature-branch ancestry rather than squashing or rebasing it.

## Immutable code-history reachability

The checkpoint names the immutable pre-research implementation/config/test commit:

`5cabb7e2ea0f9ccbd237674666031d7d9f67ae3c`

A GitHub compare from that commit to the merge commit reports the merge commit is ahead of it with merge-base equal to `5cabb7e2...`. Therefore the immutable code commit remains in the ancestry/reachable history of merged `main`, satisfying the trust model used by `h001-a/audit.py`.

## Checkpoint and handoff invariants on merged main

Merged `main` contains the same Phase A handoff manifest, which records:

- checkpoint path: `benchmarks/r4-5/h001-a/run/checkpoint.json`
- checkpoint schema: `r45-checkpoint-v1`
- checkpoint SHA-256: `fd295fd8595c2eff2e4800f2862e7bc61ca54d72c3d7c421a61688f26e43b3a3`
- semantic state SHA-256: `e93c2555c8ef11e173ea2a8c1357b09052f004716babc4e1cea68be95d8a051a`
- code commit: `5cabb7e2ea0f9ccbd237674666031d7d9f67ae3c`
- consumed research interval: `[0,2000000)`
- next candidate index: `2000000`
- last completed candidate index: `1999999`
- remaining research interval: `[2000000,10000000)`
- remaining research candidate evaluations: `8000000`
- Phase B research evaluations consumed: `0`
- research replay evaluations: `0`
- current target: `24`
- current score: `40`
- best score: `4`
- restart: `152`
- iteration: `2439`
- current-target evaluations: `1522439`
- PRNG state: `7431988031815036543`

The merged checkpoint file has the same Git blob identity as the reviewed PR version (`a2750e4396a3e2309feebdce9040196ecdbb31e4`), and the merged manifest still anchors the raw checkpoint bytes with SHA-256 `fd295fd8...`.

## Mathematical state carried into Phase B

- `R45-C001: R(4,5) >= 24`
- mathematical status: `PROVEN`
- independent review: `ACCEPTED`
- Discovery: `CONTAMINATED`

The current n=24 best score 4 remains heuristic search state only. It is not a certificate, upper bound, or nonexistence result.

## Phase B execution-base rule

This receipt does **not** freeze `5f061f2...` as an unconditional future Phase B execution base if another PR lands before the Phase B session begins.

H001-B must start by freshly fetching `origin/main` and recording the actual main SHA it sees. That execution base must contain this receipt and the accepted Phase A checkpoint. If `main` has advanced, the fresh session must use and record that descendant rather than silently substituting this receipt's creation base.

## Authorization to start H001-B

The integration prerequisites for H001-B are now satisfied:

1. Phase A checkpoint PR is merged.
2. Merge was a normal merge commit.
3. Immutable code commit remains reachable.
4. Checkpoint hash and interval declaration are preserved on merged `main`.
5. Phase B has consumed zero research candidates.

The next step is a **separate fresh Codex session** supplied only with the repository URL and `benchmarks/r4-5/goals/H001-B.md`.

Before evaluating candidate index 2,000,000, that session must perform the startup audit specified in H001-B and the handoff protocol. If any hash, state, interval, or code/config check fails, it must stop `BLOCKED` / `NEEDS_REPAIR` rather than restart or repair the trajectory in place.
