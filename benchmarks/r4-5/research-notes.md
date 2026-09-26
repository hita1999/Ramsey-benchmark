# R(4,5) — Stage 4 research notes

## Current state after H001-B independent review

- H001-A: independent acceptance **PASS**; historical termination remains **PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT**. PR #15 merged as `5f061f2`; integration receipt merged in PR #16.
- H001-B: **SOLVED** and independently accepted; operational handoff **PASS × ACCEPTED**. Review: [reviews/H001-B.md](reviews/H001-B.md). PR #17 integration remains pending.
- Overall H001 checkpoint-resume experiment: **operationally SOLVED / PASS accepted**.
- Fresh Phase B reconstructed from Git base `e1299901c3533ce1f6843c425ff8c458b834facc` and consumed exactly `[2,000,000,10,000,000)`. First observed candidate 2,000,000; final next index 10,000,000. Combined interval `[0,10,000,000)`; repeated research indices and gaps 0.
- Target n=24, current score 27, best score 4. No new certificate. Mathematical workload remains **PARTIAL_PROGRESS**; no upper bound or nonexistence claim follows.
- Strongest certificate/Claim remains **R45-C001: R(4,5)>=24, PROVEN × ACCEPTED** (n=23, 114 edges).
- Discovery **CONTAMINATED**, including disclosed Phase B Git-source exposure. Model/effort missing; no extra user questions or semantic checkpoint fields missing.
- Full Phase B evidence and measurements: [h001-b/reproduce.md](h001-b/reproduce.md), machine result [h001-b/handoff-evaluation.json](h001-b/handoff-evaluation.json), independent review [reviews/H001-B.md](reviews/H001-B.md).

## Phase A historical execution record

The following sections preserve Phase A's measurements and submission-time statements. Their pending-Phase-B language describes that earlier point; the current state above and Phase B review supersede it.

## Git, inputs, and execution provenance

- Stage 4 root: `63e8067f72b607fdc38c533e39b29e9b135cadf5`.
- Original local checkout: `a0658a0`; cached origin/main: `17aece2`. Fetch obtained actual execution base `6031a203863a71cae5a34793c5d87dbc9b24479b`.
- Dedicated branch: `codex/r45-h001-a-checkpoint`, created with --no-track from that origin/main. No direct/force/argumentless main push.
- Source: Git only, user supplied repository URL and H001-A Goal path; no prior Ramsey conversation, extra questions, web/math lookup, subagent or previous-stage certificate reuse.
- Required inputs read: H001-A.md, problem.md, handoff-protocol.md, methodology.md, prompts/codex-goal.md, results/stage3-pr-policy-verification.md. The methodology read exceeded the intended sections; details in h001-a-discovery.md. The existing r4-5 research notes were read only after independently writing the fixed plan. Other-stage file names were listed, but their search/proof content was not read.
- Fresh session: yes, based on the research session's supplied context.
- Actual model/effort: missing / missing; recommended gpt-6-astra/high is not substituted for runtime telemetry. Token and cost counters: missing.
- Contract/design commit: `f03bb70`; immutable implementation/config/test commit: `5cabb7e2ea0f9ccbd237674666031d7d9f67ae3c`.
- PR safety evidence: Stage 3 stored read-only audit dated 2026-09-21 records active main PR rule and no bypass. No destructive protection test was performed.

## Plan, findings, and limitations

The pre-research contract `h001-a-plan.md` fixes candidate semantics, RNG, restart rule and budget. Each transition scores one random initialization/restart or one proposed edge flip, counting rejected proposals. Every valid certificate advances the target by one, starting at the problem-defined larger forbidden size 5. The exact stored state is sufficient to continue at the next candidate without reconstructing or replaying the first two million transitions.

Generic integer noisy edge-flip search found certificates for every target n=5 through n=23. The n=23 certificate was found at global index 477,560. The remaining 1,522,439 Phase A evaluations were at n=24. At the Phase A boundary, restart=152, iteration=2439, PRNG internal state=`7431988031815036543`, current score 40 and best score 4.

The n=24 search had not reached score zero at the Phase A boundary. The fixed restart heuristic can discard a promising current state at a restart while retaining the best graph. This is a heuristic limitation, not evidence for nonexistence. No upper-bound proof was attempted.

## Claim ledger

- ID: **R45-C001**.
- Statement: **R(4,5)>=24**.
- Mathematical status: **PROVEN** (finite certificate, exhaustive verification and complete reduction in proof.md).
- Independent review: **ACCEPTED** ([reviews/H001-A.md](reviews/H001-A.md)).
- Discovery: **CONTAMINATED**; correctness is separate.
- Dependencies: none from previous benchmarks; Ramsey definition and the explicit graph only.
- Evidence: h001-a/run/certificate.json, verify.py, proof.md, h001-a/certificate-verification.json, h001-a/isolated-verification.json, review/r45-h001-a-independent.py, review/r45-h001-a-independent-result.json.
- Target mathematical artifact commit: `4189237ad41e171d20a972da09d999263e130cc8`; independent review was added later on the same PR branch.

## H001-A independent review and closure — 2026-09-22

- Reviewer: ChatGPT / GPT-5.6 Sol, reasoning effort High.
- Review target: PR #15; pre-review head `995a89beb5cbcb5acc2af5776af24e7fc460d79b`.
- Review record: `reviews/H001-A.md`.
- Independent mathematical checker: `review/r45-h001-a-independent.py` and saved result JSON.
- R45-C001: **PROVEN × ACCEPTED**.
- H001-A acceptance criteria: **PASS**.
- H001 overall at that time remained **PARTIAL_PROGRESS**, because real cross-session Phase B had not run.
- Independent certificate result: 23 vertices, 114 edges, all 8,855 four-sets and 33,649 five-sets checked, K4=0, independent5=0. Additional invariants: 125 triangles, 153 independent 4-sets, clique number 3, independence number 4.
- Checkpoint arithmetic independently audited: completed targets consume 477,561 evaluations; live n=24 target consumes 1,522,439; total exactly 2,000,000. `152*10000+2439 = 1,522,439`.
- Split/resume mechanism was audited from code and pre-research saved test evidence. Reviewer did not replay the 2,000,000-candidate research trajectory and did not run H001-B.
- Discovery remains **CONTAMINATED**; chronology `e387f94 -> f03bb70 -> 5cabb7e -> 4189237` preserves the utilization-before-checkpoint rule.
- PR #15 was normally merged as `5f061f2...`, preserving `5cabb7e2...`; PR #16 then recorded the integration receipt before H001-B began.

## Phase A measurement phases

- Conservative session start lower bound: 2026-09-22T07:46:00Z (minute-level inferred bound, not exact measurement); first exact UTC sample 07:47:25Z. Deadline 08:11:00Z, 25 minutes from conservative bound.
- Research search start: 2026-09-22T07:54:42.462016+00:00; serialized-and-validated finish: 2026-09-22T07:55:28.712822+00:00. Measured search plus serialization/validation time: 46.253464292 seconds, Python time.monotonic; UTC timestamps via datetime.
- Research candidates: 2,000,000. Separate test/replay transitions: 556. Delta verification comparisons: 11,136. Integrity and certificate checks: zero additional research transitions. No Phase A research replay and no Phase B research execution in that session.
- Saved test results are from the one pre-research test execution, not a later recomputation.
- Outcome commit / PR submission / phase-stop measurements are recorded as distinct events in h001-a/submission-record.json. Token/cost measurements remain missing; post-stop documentation/push overhead is labeled separately and is not search time.

## Research submission state — Phase A historical record

At Phase A research submission, R45-C001 was `PROVEN × UNREVIEWED`, checkpoint integration and independent review were both pending, and Phase B had consumed zero candidates. That state remains part of Git history and is not retroactively rewritten as if acceptance had existed then.

## H001-B execution findings

The continuation used unchanged `search.py`, `verify.py` and Phase A config bytes. Startup integrity/ancestry audit was committed before research as `d1c5cdf7e1dfa3a8750f6aaaaab7fc99248203c3`. A first-entry observer confirmed complete state `S(2,000,000)` before evaluation. The research launcher ran once, consuming the exact remaining 8,000,000 candidates. The 556 preregistered test transitions and 11,136 delta comparisons were separately labeled outside research; no Phase A research trajectory was replayed.

Time to first research step: 310.815747 seconds from second-resolution goal-service start. Search plus serialization/validation: 107.658952708 seconds. Final target counters: 952 restarts, iteration 2439, target evaluations 9,522,439; completed targets 477,561; global next index 10,000,000. The best score remained 4; current score ended at 27. All 19 carried-forward certificates passed certificate-only verification; strongest certificate remained byte-identical to the accepted Phase A n=23 certificate. No new Claim or refutation was established.

Final checkpoint SHA-256 is `10702e9992f823cfc18135fc68537ca7171506c1f6382b9005a7c87426ee05f4`; semantic state SHA-256 is `de0b95aa593d14e63b48fc85786175ad5dd13eff5447f86841dc532346190bff`.

## H001-B independent review and closure — 2026-09-22

- Reviewer: ChatGPT / GPT-5.6 Sol, reasoning effort High.
- Review target: PR #17; pre-review head `7a2330f5df9498f168cba32275c2ececf7c66805`.
- Review record: `reviews/H001-B.md`.
- Verdict: **H001-B SOLVED; operational handoff PASS × ACCEPTED**.
- Overall H001 checkpoint-resume experiment: **operationally SOLVED / PASS accepted**.
- Mathematical result unchanged: **R45-C001 = PROVEN × ACCEPTED**, mathematical `R(4,5)` workload still **PARTIAL_PROGRESS**.
- Reviewer verified the Phase A trust anchor, Phase B pre-research chronology, exact `S(2,000,000)` input-state digest, unchanged search/config identity, 80 progress blocks, final interval/counter arithmetic and checkpoint identity.
- No full uninterrupted 10M research trajectory was independently replayed. The small split/resume tests and actual cross-session deterministic continuation are the evidence required by the registered protocol.
- Fresh-session/no-prior-conversation remains provenance attestation, not a cryptographic proof of hidden-context absence.
- Discovery remains **CONTAMINATED**.

Remaining work is PR #17 integration with a **normal merge commit** and a subsequent PR-based `results/r45-h001-b-integration-receipt.md`. Normal merge is required because the final checkpoint names `code_commit=d1c5cdf7...` and audit logic verifies historical source bytes using `git show`. Further n=24 research requires a new Goal; the H001-B research budget is exhausted.
