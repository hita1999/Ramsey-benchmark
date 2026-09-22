# H001-A verification record

## Current state

- R45-C001: **PROVEN × ACCEPTED**. Independent review: [reviews/H001-A.md](reviews/H001-A.md).
- H001-A acceptance criteria: **PASS**.
- H001-A termination remains **PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT** by design.
- Overall H001 experiment: **PARTIAL_PROGRESS**. Phase B has not run, so cross-session handoff PASS/FAIL is not yet determined.
- Discovery: **CONTAMINATED**.

## Independent review — 2026-09-22

Reviewer: ChatGPT / GPT-5.6 Sol, reasoning effort High. Review target was PR #15 with pre-review head `995a89beb5cbcb5acc2af5776af24e7fc460d79b`.

The reviewer used a separate certificate checker that imports neither `search.py` nor the research-side `verify.py`:

```text
review/r45-h001-a-independent.py
review/r45-h001-a-independent-result.json
```

Independent result:

- n=23
- edges=114
- all `C(23,4)=8,855` four-subsets checked
- K4=0
- all `C(23,5)=33,649` five-subsets checked
- independent 5-set=0
- triangles=125
- independent 4-sets=153
- clique number=3
- independence number=4
- canonical certificate SHA-256 `5e5f6b18a032f0be038a83c69a39ae4f42755432dd36e8f30d43931fb6aad498`

Therefore the saved certificate proves `R(4,5)>=24`, and R45-C001 is accepted.

The checkpoint accounting was also audited independently from saved state:

- completed n=5..23 target evaluations sum to 477,561
- current n=24 target evaluations = 1,522,439
- `152*10,000 + 2,439 = 1,522,439`
- global total = 2,000,000
- next candidate index = 2,000,000
- Phase B consumed research candidates = 0
- remaining interval = `[2,000,000,10,000,000)`
- raw checkpoint SHA-256 = `fd295fd8595c2eff2e4800f2862e7bc61ca54d72c3d7c421a61688f26e43b3a3`
- semantic state SHA-256 = `e93c2555c8ef11e173ea2a8c1357b09052f004716babc4e1cea68be95d8a051a`

The reviewer inspected the exact-resume state machine and the saved pre-research split/resume evidence. The tests compare every semantic state field and canonical state bytes across normal, target-advance/initialize, and restart boundaries. This supports acceptance of the Phase A checkpoint mechanism. The reviewer did **not** replay the two million Phase A research candidates and did **not** execute H001-B; the real fresh-session handoff remains the next experiment.

Integration requirement: PR #15 must use a **normal merge commit** rather than squash/rebase because `checkpoint.json` fixes `code_commit=5cabb7e2...` and `audit.py` verifies its historical source with `git show`. The integration receipt must confirm that commit remains reachable and the checkpoint hash remains unchanged before H001-B starts.

## Researcher self-audits — historical evidence

The checks below were performed by the Phase A researcher before independent review:

- Split/resume: PASS on fixed 111+157 test, initialization/target boundary 1+1, and restart boundary 7+1. All semantic fields and their canonical JSON bytes agree. Exact test configs, state hashes and excluded wrapper metadata are in `h001-a/test-result.json`; executable code is `test_search.py`.
- Test candidate transitions: 556, all explicitly TEST_REPLAY_OUTSIDE_RESEARCH_BUDGET. No real research trajectory was replayed.
- Delta verification: 11,136 full-score comparisons (every graph and edge at n=5, plus 32 deterministic n=8 samples); PASS.
- PRNG scalar arithmetic, seven hash/semantic corruption rejection controls, and six invalid-certificate controls: PASS.
- Real checkpoint: loader and full graph-score validation PASS at next_candidate_index=2,000,000. See `h001-a/checkpoint-validation.json`. Validation consumes zero research candidates.
- All 19 certificates n=5..23: exhaustive certificate-only verification PASS, recorded in `h001-a/certificate-verification.json`.
- Strongest certificate: isolated Python process supplied only verify.py and certificate.json confirms n=23, 114 edges, zero K4 and zero independent 5-sets. `h001-a/isolated-verification.json` records environment and output; this is an independent code path/process, not an independent researcher/session.
- Phase B: NOT RUN. Cross-session exact resume and combined-interval audit remain pending after this checkpoint PR is merged.

Current 24-vertex best score 4 is not a valid certificate and supplies no lower bound beyond R45-C001. It is not evidence for nonexistence or an upper bound.
