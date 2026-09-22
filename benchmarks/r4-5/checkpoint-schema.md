# Checkpoint schema r45-checkpoint-v1

Python 3.9+ standard library only. JSON numbers for graph rows and counters; the 64-bit PRNG state is a decimal string to avoid loss in JSON readers using binary64. Graph rows are arbitrary-precision nonnegative bitsets: bit v in row u is the undirected edge uv. Diagonal bits are zero; rows are symmetric. A consumer must preserve integer precision (including graph rows if n grows beyond 53).

## Semantic state

Every field under `state` is compared in split/resume tests; none is excluded:

- `next_candidate_index`: next unevaluated global candidate k. State is S(k); last evaluated index is k-1.
- `target_n`: current graph order. Starts at config start_n=5; increments only after a valid score-zero candidate.
- `completed_targets`: increasing contiguous orders, each with `evaluations` and `found_at_index`. Sum of these evaluations plus target_evaluations equals k.
- `certificates`: matching complete edge lists for completed targets, including all previous certificates.
- `prng_state`: internal nonzero xorshift64 state, decimal string; not the multiplied output word.
- `graph`, `score`: current accepted graph and total forbidden-structure count, or null before initialization.
- `best_graph`, `best_score`: first best graph at the current target across restarts, or null before initialization. Completed-target bests are in certificates.
- `restart`: zero-based restart number at this target, reset upon target advance.
- `iteration`: evaluated candidates in this restart, including initialization. Range 1..restart_interval in search mode.
- `target_evaluations`: all evaluated candidates at current target; equals restart*restart_interval+iteration in search mode.
- `mode`: initialize or search. Initialize means the NEXT candidate generates/scores a fresh graph. Graphs/scores are null and all target counters zero in this mode.

For a search-mode state with iteration==restart_interval, the NEXT candidate is a counted random restart. Restart generation does not happen when a checkpoint is loaded. A zero-score discovery stores its certificate, advances target and clears current-target fields as part of the SAME transition; the next initialization is not scored until the next candidate. This includes an exact budget-boundary discovery.

## Transition and PRNG

`h001-a-plan.md` fixes candidate semantics and acceptance. Lexicographic (u,v), 0<=u<v<n, defines edge indexing. Every initialization edge consumes one draw, present iff output&1. Every flip consumes one draw modulo edge count; only worsening flips consume an additional acceptance draw. Modulo sampling has a tiny documented bias; exact uniformity is not claimed. The acceptance numerator uses iteration BEFORE the current transition. All scores, temperatures (noise), comparisons and PRNG operations are integer-valued.

For internal word x: x ^= x>>12; x ^= (x<<25)&(2^64-1); x ^= x>>27. Store x. Return (x*2685821657736338717)&(2^64-1). No time-based randomness, floating-point acceptance or platform RNG. Timing uses time.monotonic only as output metadata. Lexicographic edge lists and complement rows are derived caches with no independent semantic state.

For a flip uv, only forbidden sets containing both endpoints can change. Red K4 completions are edges in the common red neighborhood. Blue K5 completions are triangles in the common blue neighborhood. Inserting a red edge adds red completions and removes blue completions; deletion reverses the sign. Full-score verification enumerates all 4/5-subsets through verify.py, independently of this delta formula.

## Wrapper, hashes and validation

The wrapper holds schema, benchmark, phase, algorithm, execution_base, code_commit, created_at_utc, config_sha256, code_sha256, certificate_sha256, consumed_research_interval, state and state_sha256. `code_commit` is the immutable pre-research implementation commit for Phase A. At Phase B output it is the actual executing HEAD; code hashes must still agree on load.

- Code and config SHA-256 hashes use raw file bytes. Code hashes cover search.py and verify.py, the entire executable dependency set apart from Python's standard library.
- state_sha256 and embedded certificate_sha256 use UTF-8 JSON with sorted keys, separators comma/colon, no extra whitespace (Python ensure_ascii default true). Their inputs contain only ASCII property names and integers.
- The handoff manifest gives the SHA-256 of the entire checkpoint file and raw external certificate files; the checkpoint itself cannot contain its own file hash.
- consumed_research_interval is [0,k] in JSON representing half-open [0,k); TEST wrappers use null.
- `load_checkpoint` checks schema/algorithm, code/config hashes, state/certificate hashes, graph validity/scores, embedded certificates, completed order sequence and global/per-target/restart counter consistency. `--expected-sha256` also anchors every wrapper byte to the Git manifest. The manifest and Git commits are the trust anchor, not hashes alone.
- Tests exclude all wrapper fields listed above EXCEPT state, comparing every state field and canonical serialized state bytes. Different phase/timestamp/origin metadata is not search state. Each wrapper is separately validated on load.

## Commands from repository root

```sh
python3 benchmarks/r4-5/test_search.py
python3 benchmarks/r4-5/search.py validate --config benchmarks/r4-5/h001-a/config.json --checkpoint benchmarks/r4-5/h001-a/run/checkpoint.json
python3 benchmarks/r4-5/verify.py benchmarks/r4-5/h001-a/run/certificates/*.json
```

The handoff manifest supplies the exact Phase B resume command, including expected checkpoint hash. `start` hard-codes exactly 2,000,000 evaluations; `resume` requires a Phase A checkpoint at that boundary and hard-codes the remaining 8,000,000. Both reject a nonempty output directory. Load/validate does not call advance or step. No Phase B command may be run in the Phase A session.
