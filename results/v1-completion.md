# Ramsey-benchmark v1.0 — completion decision

## Decision

- Decision date: **2026-10-25** (Asia/Tokyo).
- Project release scope: **v1.0 COMPLETED**.
- Research stages in v1.0: **Stage 1–4**; no Stage 5 is planned or required to close v1.0.
- Decision provenance: user-approved completion after Stage 4 retrospective was integrated via [PR #19](https://github.com/hita1999/Ramsey-benchmark/pull/19).
- Reference main commit before this documentation-only closure: `b689a934274d5d776e4350eeef0ba75cce763c67`.
- Source of truth: merged Git artifacts, formal Claims, independent review records and integration receipts.
- This document is a completion decision, **not** a new mathematical Claim, a new experiment, an extra independent review or a git release/tag.

## What v1.0 establishes

1. For the three smaller Ramsey benchmarks, saved proofs and/or finite certificates support the independently accepted statements `R(3,4)=9`, `R(3,5)=14`, and `R(4,4)=18`.
2. In Stage 4, a saved graph on 23 vertices with 114 edges was independently verified to have no `K4` and no independent 5-set, yielding **`R(4,5) ≥ 24` = PROVEN × ACCEPTED**.
3. Stage 4 deliberately stopped at the incomplete search state `S(2,000,000)`, merged the checkpoint and its integration receipt to main, then resumed in another fresh Codex session from the Git state at research candidate index `2,000,000`. Its saved counters/code audit support a combined research interval `[0,10,000,000)` with no gap or overlap. The operational handoff was independently accepted: **H001-B SOLVED; PASS × ACCEPTED**.
4. The Git-centric workflow includes dedicated researcher PRs, independent review records, reproducibility assets, completion/closure synchronization and merge receipts. See [benchmark summary](benchmark-summary.md) and the [Stage 4 retrospective](stage4-retrospective.md).

## What v1.0 does not establish

- **`R(4,5)` is mathematically PARTIAL_PROGRESS**, with only `R(4,5) ≥ 24` accepted here. Exhausting a heuristic budget at 24 vertices, including a best score of 4, proves neither nonexistence nor an upper bound.
- All recorded discovery states remain **CONTAMINATED**; the experiment has not demonstrated novel mathematical Discovery on an unknown problem.
- The single deliberate, same-environment checkpoint-resume test does **not** establish robustness under unplanned process crashes, data corruption, arbitrary restart positions or cross-environment search continuation.
- The split/resume tests and code/counter evidence do not constitute a separately replayed uninterrupted 10M-candidate research trajectory.
- Actual runtime model/effort values and important token/cost/review-effort data were missing in some stages. No performance or cost superiority of Astra, Luna, Sol, or the multi-agent workflow over a single-session baseline is claimed.

## Why there is no Stage 5 now

The purpose of v1.0 was to test the feasibility, auditability and Git-only continuity of the Codex + ChatGPT mathematical research workflow. Stage 4 supplied the previously missing evidence for a deliberate incomplete-checkpoint handoff. A further numbered Stage without a decision-relevant hypothesis would add process and review cost without ensuring new knowledge.

The earlier suggestion to compare Astra vs Luna is **not** retained as a required next stage. Changing model options and the lack of a controlled, instrumented comparative setup reduce the immediate value of such a comparison. This is a prioritization choice, not a finding about any model's relative capability.

## Preservation and reopening conditions

- Preserve the recorded mathematical / review / discovery / operational states, original Goal contracts, immutable code commits, research counters and generated evidence. Do not reclassify an incomplete mathematical problem as solved to fit the project-level completion status.
- Keep the repository available as a reproducible reference. This decision **does not archive the GitHub repository, create a version tag, or disable further PRs**.
- If a concrete research need arises (novel discovery, a failure in real research handoff, crash recovery, portability or calibrated model comparison), propose a **new, bounded Goal** with its initial base, clean evidence scope, metrics, independent review procedure and stop rule. Such work is outside v1.0 and does not retroactively change its findings.
- Future work is optional; **Stage 5 is not scheduled or defined**.

This document closes the current evaluation program, not the underlying open mathematical questions.
