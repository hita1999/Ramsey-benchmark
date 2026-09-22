# Stage 4 — R(4,5) checkpoint-resume experiment

## Primary objective

Stage 4 is not primarily an attempt to determine the exact value of `R(4,5)`.
The primary experiment is whether an unfinished computational research state can be checkpointed in Git and resumed in a separate fresh session without hidden conversational state, duplicated search work, or semantic drift.

The mathematical workload is a lower-bound certificate search for a graph with:

- no `K_4`, and
- no independent set of size 5.

Any concrete valid `n`-vertex graph proves `R(4,5) >= n+1`.
Failure to find a graph at any `n` is not an upper bound or nonexistence proof.

## Stage 4 root

The Stage 4 root is the Stage 3 retrospective merge commit:

`63e8067f72b607fdc38c533e39b29e9b135cadf5`

Each execution phase records its actual `main` HEAD as its execution base.

## Experiment structure

The experiment has two deliberately separated phases.

### H001-A — checkpoint creation

A fresh Codex session begins from Git, implements a deterministic resumable search, performs only the Phase A budget, saves an unfinished checkpoint, tests split/resume equivalence, pushes a dedicated PR, and stops.

It MUST NOT continue into Phase B even if time remains.

### H001-B — fresh-session resume

Only after the H001-A checkpoint PR is merged, a different fresh Codex session begins from Git with no conversation history from A. It must reconstruct the research state from repository artifacts, resume from the saved checkpoint, consume only the remaining Phase B budget, and record whether the resume was faithful.

## Primary evaluation criteria

The handoff experiment is successful only if all of the following are demonstrated:

1. Phase A stops intentionally while the research Goal remains incomplete.
2. The checkpoint contains enough machine-readable state to continue the exact search trajectory.
3. A small deterministic test shows uninterrupted execution and split+resume execution reach identical final state.
4. Phase B starts from Git only, without receiving Phase A conversation history.
5. Phase B does not restart the search from evaluation 0 or repeat the Phase A evaluation interval.
6. Phase B validates checkpoint integrity before resuming.
7. The combined evaluation interval is auditable from counters/state, with no gap or overlap.
8. Research notes distinguish resumed work from recomputation, replay, and independent verification.

Mathematical progress is secondary: a certificate discovered in either phase is valuable, but the experiment can still succeed operationally even if no new large certificate is found.

## Discovery / contamination

If the researcher recalls an exact value, known construction, known extremal graph, known search horizon, or proof strategy for `R(4,5)`, it must be recorded in a notes-only checkpoint commit before use.

The recalled information must not become a target size, stop condition, initialization, seed graph, or proof evidence unless the Goal explicitly allows it.

Discovery and correctness are separate axes. A contaminated run may still yield a valid certificate and a successful handoff experiment.

## Git policy

All research, checkpoints, reviews, and closures use dedicated branches and PRs. No direct pushes to `main`, force pushes, or argumentless pushes.

Git is the source of truth. The second session must not depend on hidden chat history from the first session.
