# R(4,5) — Stage 4 research notes

## Current state

- Stage 4 status: `READY_FOR_H001_A`.
- Primary experiment: unfinished-checkpoint handoff, not exact determination of `R(4,5)`.
- Stage 4 root: `63e8067f72b607fdc38c533e39b29e9b135cadf5`.
- H001-A: defined, not started.
- H001-B: defined, must not start until H001-A checkpoint PR is merged.
- Mathematical Claims: none yet.
- Discovery: `UNKNOWN` before research starts. Absence of a recall record is not evidence of CLEAN.

## Planned research intervals

- Phase A: `[0, 2,000,000)` candidate evaluations.
- Phase B: `[2,000,000, 10,000,000)` candidate evaluations.
- Total planned research interval: `[0, 10,000,000)`.

Tests, replay diagnostics, certificate verification, and split/resume equivalence checks are not research candidate evaluations and must be accounted for separately.

## Primary handoff KPI

The central question is whether Phase B can, from Git alone:

- identify the exact next research candidate index;
- validate code/config/checkpoint integrity;
- resume the exact deterministic trajectory;
- avoid repeating Phase A research candidates;
- continue without extra semantic guidance from the user.

Operational handoff status is separate from mathematical Claim status.

## Claim ledger

No new mathematical Claims yet. Use `R45-C001` onward for certificate Claims if needed.

## Next action

Run H001-A in a fresh Codex session after the Stage 4 definition PR is merged. H001-A must stop at the mandatory checkpoint and must not consume Phase B work.
