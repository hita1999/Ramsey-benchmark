# R(4,5) — Stage 4 research notes

## Current state

- H001-A termination: **PARTIAL_PROGRESS**, reason **MANDATORY_HANDOFF_CHECKPOINT**. This intentional termination classification is unchanged by review.
- H001-A acceptance criteria: **PASS** by independent review.
- Overall H001 experiment: **PARTIAL_PROGRESS**; intentional unfinished checkpoint, not SOLVED. Cross-session H001-B remains pending.
- Phase A consumed exactly [0,2,000,000); last completed candidate 1,999,999; next candidate 2,000,000.
- Phase B consumed zero candidates in Phase A. Remaining interval [2,000,000,10,000,000), exactly 8,000,000 candidates.
- Current target n=24; current score 40; best score 4. No n=24 certificate was found in the allocated interval. This is not a nonexistence or upper-bound conclusion.
- Strongest valid certificate: n=23, 114 edges, giving **R(4,5)>=24 = PROVEN × ACCEPTED**.
- Discovery: **CONTAMINATED**. Recollection and accidental full-methodology exposure were recorded in notes-only commit `e387f94` before design/code. Recalled values and prior-stage constructions were not used in the plan or as mathematical evidence.
- Independent review is complete; checkpoint PR #15 integration is pending. Phase B starts only after a normal merge commit and an integration receipt, in another fresh session.

## Git, inputs, and execution provenance

- Stage 4 root: `63e8067f72b607fdc38c533e39b29e9b135cadf5`.
- Original local checkout: `a0658a0`; cached origin/main: `17aece2`. Fetch obtained actual execution base `6031a203863a71cae5a34793c5d87dbc9b24479b`.
- Dedicated branch: `codex/r45-h001-a-checkpoint`, created with --no-track from that origin/main. No direct/force/argumentless main push.
- Source: Git only, user supplied repository URL and H001-A Goal path; no prior Ramsey conversation, extra questions, web/math lookup, subagent or previous-stage certificate reuse.
- Required inputs read: H001-A.md, problem.md, handoff-protocol.md, methodology.md, prompts/codex-goal.md, results/stage3-pr-policy-verification.md. The methodology read exceeded the intended sections; details in h001-a-discovery.md. The existing r4-5 research notes were read only after independently writing the fixed plan. Other-stage file names were listed, but their search/proof content was not read.
- Fresh session: yes, based on the research session's supplied context. Phase B fresh-session status cannot yet be measured.
- Actual model/effort: missing / missing; recommended gpt-6-astra/high is not substituted for runtime telemetry. Token and cost counters: missing.
- Contract/design commit: `f03bb70`; immutable implementation/config/test commit: `5cabb7e2ea0f9ccbd237674666031d7d9f67ae3c`.
- PR safety evidence: Stage 3 stored read-only audit dated 2026-09-21 records active main PR ruleset and no bypass. No destructive protection test was performed.

## Plan, findings, and limitations

The pre-research contract `h001-a-plan.md` fixes candidate semantics, RNG, restart rule and budget. Each transition scores one random initialization/restart or one proposed edge flip, counting rejected proposals. Every valid certificate advances the target by one, starting at the problem-defined larger forbidden size 5. The exact stored state is sufficient to continue at the next candidate without reconstructing or replaying the first two million transitions.

Generic integer noisy edge-flip search found certificates for every target n=5 through n=23. The n=23 certificate was found at global index 477,560. The remaining 1,522,439 evaluations were at n=24. Current restart=152, iteration=2439, PRNG internal state="7431988031815036543". Noise for the next transition is derived from the saved iteration and immutable config, not wall time. Best graph and current graph are both saved and scored independently on load.

The n=24 search has not reached score zero; the best score is 4. The fixed restart heuristic can discard a promising current state at a restart, while retaining the best graph. This is a heuristic limitation, not a reason to change trajectory during the handoff. There is no refuted mathematical hypothesis and no exhaustive exclusion of larger orders. No upper-bound proof was attempted. The next action is exact resumption of the saved trajectory, not heuristic tuning.

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
- H001 overall: remains **PARTIAL_PROGRESS**, because real cross-session Phase B has not run.
- Independent certificate result: 23 vertices, 114 edges, all 8,855 four-sets and 33,649 five-sets checked, K4=0, independent5=0. Additional invariants: 125 triangles, 153 independent 4-sets, clique number 3, independence number 4.
- Checkpoint arithmetic independently audited: completed targets consume 477,561 evaluations; live n=24 target consumes 1,522,439; total exactly 2,000,000. `restart*10000+iteration = 152*10000+2439 = 1,522,439`.
- Split/resume mechanism was audited from code and pre-research saved test evidence. Reviewer did not replay the 2,000,000-candidate research trajectory and did not run H001-B; therefore the Stage 4 primary cross-session handoff KPI is still unmeasured.
- Discovery remains **CONTAMINATED**; the chronology `e387f94 -> f03bb70 -> 5cabb7e -> 4189237` preserves the utilization-before-checkpoint rule.
- Integration requirement: PR #15 must use a **normal merge commit**, not squash/rebase, because the checkpoint names immutable `code_commit=5cabb7e2...` and the audit uses `git show <code_commit>:...`. After merge, an integration receipt must record merge SHA/time, reachability of that commit, unchanged checkpoint SHA, and the remaining Phase B interval before H001-B starts.

## Measurement phases

- Conservative session start lower bound: 2026-09-22T07:46:00Z (minute-level inferred bound, not exact measurement); first exact UTC sample 07:47:25Z. Deadline 08:11:00Z, 25 minutes from conservative bound.
- Research search start: 2026-09-22T07:54:42.462016+00:00; serialized-and-validated finish: 2026-09-22T07:55:28.712822+00:00. Measured search plus serialization/validation time: 46.253464292 seconds, Python time.monotonic; UTC timestamps via datetime.
- Research candidates: 2,000,000. Separate test/replay transitions: 556. Delta verification comparisons: 11,136. Integrity and certificate checks: zero additional research transitions. No Phase A research replay and no Phase B research execution.
- Saved test results are from the one pre-research test execution, not a later recomputation.
- Outcome commit / PR submission / phase-stop measurements are recorded as distinct events in h001-a/submission-record.json. Token/cost measurements remain missing; post-stop documentation/push overhead is labeled separately and is not search time.

## Research submission state — historical record

At research submission, R45-C001 was `PROVEN × UNREVIEWED`, checkpoint integration and independent review were both pending, and Phase B had consumed zero candidates. That state remains part of Git history and is not retroactively rewritten as if acceptance had existed then.

## Exact next action and ownership

`h001-a/handoff-manifest.json` is the machine-readable handoff. After PR #15 is merged with a normal merge commit and the integration receipt is recorded, Phase B must validate its raw-file hashes, load the checkpoint, and record the startup audit before any new candidate. Follow goals/H001-B.md only in a separate fresh session. Use a dedicated Phase B branch from freshly fetched main and record that actual execution base. If integrity fails, stop with NEEDS_REPAIR/BLOCKED; do not silently restart or alter code/config.

The next session must reconstruct everything from Git, without this conversation. Actual cross-session resume fidelity, extra questions, repeated research candidates, semantic drift, and overall H001 success are all still unmeasured.
