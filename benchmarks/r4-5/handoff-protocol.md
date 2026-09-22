# Stage 4 handoff protocol

## Required checkpoint contents

A resumable search checkpoint must be machine-readable and versioned. At minimum it records:

- schema/version identifier;
- benchmark and phase;
- execution base and code commit;
- search algorithm identifier and immutable configuration hash;
- current target `n` and any completed target sizes;
- global candidate-evaluation counter;
- Phase A evaluation interval already consumed;
- random/PRNG state or other deterministic generator state;
- current candidate graph/search state;
- current score and best score;
- best certificate(s) found so far;
- restart number / iteration position / temperature or analogous algorithm state;
- checkpoint creation timestamp as metadata only;
- hashes of code/config/certificate files required to resume.

The checkpoint must not rely on opaque process memory or a Python object pickle whose semantics are not documented. Prefer portable JSON plus an explicitly implemented deterministic PRNG/state machine.

## Exact-resume invariant

For a fixed code/config/seed, let `S(k)` be the complete search state after exactly `k` candidate evaluations.

The implementation must support:

- uninterrupted: `S(0) -> S(a+b)`;
- split: `S(0) -> S(a)`; serialize; deserialize; resume `b` evaluations -> `S'(a+b)`.

A small pre-registered equivalence test must verify that `S(a+b) == S'(a+b)` for every semantically relevant field. Environment-only metadata such as timestamp or output path is excluded explicitly before the test.

The test budget is separate from the research candidate budget.

## Evaluation intervals

Research candidate evaluations use a global half-open interval convention:

- Phase A consumes `[0, A)`.
- Phase B must resume at exactly `A` and consume `[A, A+B)`.

No candidate index may be evaluated twice as research work. Replay for testing or verification must be labeled separately and excluded from the research budget.

## Phase A merge boundary

The unfinished checkpoint is a first-class research artifact. Phase A must stop after saving and pushing it. It is merged through PR before Phase B begins.

This deliberate merge boundary is part of the benchmark: the second fresh session receives only repository state, not the first session's conversation.

## Phase B startup audit

Before performing a new candidate evaluation, Phase B must record:

1. current execution base;
2. files read to reconstruct state;
3. checkpoint SHA/hash and schema;
4. last completed candidate index and next candidate index;
5. remaining budget;
6. code/config hash verification;
7. successful checkpoint load and invariant checks;
8. whether any extra user information was required.

If the checkpoint cannot be resumed exactly, Phase B must stop with `BLOCKED` or `NEEDS_REPAIR`; it must not silently restart from scratch.

## Handoff metrics

Record at least:

- extra user questions needed by Phase B;
- number of repeated research candidate evaluations (target 0);
- number of missing/ambiguous checkpoint fields discovered;
- wall-clock time from Phase B start to first resumed candidate;
- whether code/config changed before resume;
- whether split-resume equivalence passed;
- whether Phase B correctly identified the remaining evaluation interval;
- any semantic drift in Goal interpretation.

## Claims

The handoff result is operational, not a mathematical Claim about `R(4,5)`.

Mathematical certificate Claims use the normal two-axis state (`PROVEN/… × ACCEPTED/…`).
Handoff findings are recorded separately as PASS / NEEDS_REVISION / FAIL with explicit evidence.
