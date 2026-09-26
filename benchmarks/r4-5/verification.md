# R(4,5) verification record

## Current state

- R45-C001: **PROVEN × ACCEPTED**. Independent mathematical review: [reviews/H001-A.md](reviews/H001-A.md).
- H001-A acceptance criteria: **PASS**.
- H001-A termination remains **PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT** by design.
- H001-B operational handoff: **PASS × ACCEPTED**; researcher goal **SOLVED** and independently accepted. Review: [reviews/H001-B.md](reviews/H001-B.md).
- Overall H001 checkpoint-resume experiment: **operationally SOLVED / PASS accepted**.
- Mathematical R(4,5) workload remains **PARTIAL_PROGRESS**.
- Discovery: **CONTAMINATED**.

## Phase A independent review — 2026-09-22

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

The reviewer inspected the exact-resume state machine and the saved pre-research split/resume evidence. The tests compare every semantic state field and canonical state bytes across normal, target-advance/initialize, and restart boundaries. This supports acceptance of the Phase A checkpoint mechanism. The reviewer did **not** replay the two million Phase A research candidates and did **not** execute H001-B; the real fresh-session handoff remained the next experiment at that historical point.

Integration requirement: PR #15 used a **normal merge commit** rather than squash/rebase because `checkpoint.json` fixes `code_commit=5cabb7e2...` and `audit.py` verifies its historical source with `git show`. The subsequent integration receipt confirmed that commit remained reachable and the checkpoint hash remained unchanged before H001-B began.

## Researcher self-audits — Phase A historical evidence

The checks below were performed by the Phase A researcher before independent review:

- Split/resume: PASS on fixed 111+157 test, initialization/target boundary 1+1, and restart boundary 7+1. All semantic fields and their canonical JSON bytes agree. Exact test configs, state hashes and excluded wrapper metadata are in `h001-a/test-result.json`; executable code is `test_search.py`.
- Test candidate transitions: 556, all explicitly TEST_REPLAY_OUTSIDE_RESEARCH_BUDGET. No real research trajectory was replayed.
- Delta verification: 11,136 full-score comparisons (every graph and edge at n=5, plus 32 deterministic n=8 samples); PASS.
- PRNG scalar arithmetic, seven hash/semantic corruption rejection controls, and six invalid-certificate controls: PASS.
- Real checkpoint: loader and full graph-score validation PASS at next_candidate_index=2,000,000. See `h001-a/checkpoint-validation.json`. Validation consumes zero research candidates.
- All 19 certificates n=5..23: exhaustive certificate-only verification PASS, recorded in `h001-a/certificate-verification.json`.
- Strongest certificate: isolated Python process supplied only verify.py and certificate.json confirms n=23, 114 edges, zero K4 and zero independent 5-sets. `h001-a/isolated-verification.json` records environment and output; this is an independent code path/process, not an independent researcher/session.
- Phase B was NOT RUN at the Phase A submission point. That historical state is superseded by the Phase B sections below.

Current 24-vertex best score 4 is not a valid certificate and supplies no lower bound beyond R45-C001. It is not evidence for nonexistence or an upper bound.

## H001-B researcher verification — 2026-09-22

Detailed reproducibility and reviewer handoff: [h001-b/reproduce.md](h001-b/reproduce.md). Operational self-audit [handoff-evaluation.json](h001-b/handoff-evaluation.json) reported PASS before independent review.

- Startup: all 26 manifest artifacts matched Git/base hashes, historical code/config and checkpoint invariants validated before research. Pre-research audit commit `d1c5cdf7e1dfa3a8750f6aaaaab7fc99248203c3`.
- Exact first step: index 2,000,000 and full input-state hash match Phase A; observer does not modify semantics. No code/config changes; no extra questions; zero ambiguous/missing semantic fields.
- Accounting: 80 consecutive 100,000-candidate blocks; final index 10,000,000, Phase B count 8,000,000, no gap or repeated research index by code/counter audit. Final sum 477,561 + 9,522,439 = 10,000,000.
- Existing split/resume, boundary, tamper, PRNG and certificate tests passed; complete saved output matches Phase A. Phase B ran 556 TEST/REPLAY transitions and 11,136 delta comparisons; no research trajectory replay.
- Final checkpoint passed raw hash, state hash, graph score, certificate and counter validation. Checkpoint SHA-256 `10702e9992f823cfc18135fc68537ca7171506c1f6382b9005a7c87426ee05f4`; state SHA-256 `de0b95aa593d14e63b48fc85786175ad5dd13eff5447f86841dc532346190bff`.
- All 19 certificates n=5..23 were carried forward unchanged and certificate-only reverified; isolated verifier confirmed the strongest n=23/114-edge graph. New certificates: 0. R45-C001 remains PROVEN × ACCEPTED from the independent Phase A review.
- Final n=24 current score 27, best score 4 remains invalid heuristic state, not evidence for an upper bound.

Small equivalence tests and code/counter continuity do not claim a full uninterrupted 10M replay. Researcher self-audits do not substitute for independent review.

## H001-B independent review — 2026-09-22

Reviewer: ChatGPT / GPT-5.6 Sol, reasoning effort High. Pre-review PR #17 head: `7a2330f5df9498f168cba32275c2ececf7c66805`. Full record: [reviews/H001-B.md](reviews/H001-B.md).

The independent review accepted the operational handoff based on the merged Phase A trust anchor, pre-research Phase B chronology, exact first-state observation, unchanged search/config hashes, interval arithmetic and final checkpoint. In particular:

- execution base `e1299901c3533ce1f6843c425ff8c458b834facc` contains the accepted H001-A merge and integration receipt;
- Phase B audit/observer commit `d1c5cdf7...` predates the research artifact commit `f35b7f44...`;
- `search.py` has the same Git blob at Phase A code commit `5cabb7e2...` and Phase B executing commit `d1c5cdf7...`;
- incoming state is exactly `S(2,000,000)` with Phase A state SHA `e93c2555...` before the first resumed step;
- unchanged `advance` invokes one `step` per candidate and each `step` advances the global index exactly once;
- 80 saved progress blocks end at `S(10,000,000)` and the final target/restart arithmetic sums exactly to 10,000,000;
- there is no research replay of `[0,2,000,000)`, no gap, and no code/config semantic drift;
- split/resume tests remain identical to Phase A and are separately accounted for outside research work.

Accordingly, **H001-B = SOLVED and operational handoff = PASS × ACCEPTED**. The overall H001 checkpoint-resume experiment is operationally complete and accepted.

The reviewer did not replay a separate uninterrupted 10M research trajectory. Fresh-session/no-hidden-conversation remains a provenance attestation rather than a cryptographic proof. These limitations are preserved in the review rather than upgraded into stronger claims.

No new mathematical Claim was found in Phase B. **R45-C001 remains PROVEN × ACCEPTED**, and the mathematical `R(4,5)` workload remains **PARTIAL_PROGRESS**.

For integration, PR #17 should use a **normal merge commit**, not squash/rebase, because the final checkpoint names `code_commit=d1c5cdf7...` and the audit verifies historical source bytes with `git show`. A subsequent PR-based integration receipt should record the merge SHA/time, reachability of `d1c5cdf7...`, final checkpoint SHA, and accepted operational verdict.
