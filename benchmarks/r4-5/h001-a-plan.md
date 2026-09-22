# H001-A execution contract and fixed plan

- Execution base: `6031a203863a71cae5a34793c5d87dbc9b24479b` (fetched origin/main).
- Stage 4 root: `63e8067f72b607fdc38c533e39b29e9b135cadf5`.
- Branch: `codex/r45-h001-a-checkpoint`; no upstream until explicit dedicated-branch push.
- Researcher: Codex. Actual model: `missing`; actual effort: `missing` (no reliable runtime model/effort telemetry exposed). Recommended: gpt-6-astra / high.
- Fresh session and input provenance: see `h001-a-discovery.md`. Discovery CONTAMINATED.
- Session wall-clock start: `2026-09-22T07:46:00Z`, conservative minute-level lower bound from initial workspace observation, not an exact sampled start. First exact clock sample: `2026-09-22T07:47:25Z` (UTC, system `date`). Deadline: `2026-09-22T08:11:00Z`; 25 minutes includes implementation, tests, research, serialization, documentation, commits and push.
- Research budget: exactly 2,000,000 candidates; stop with PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT. Phase B [2000000,10000000) is forbidden in this session.
- Token/cost counters: missing; do not infer from account limits.

## Plan fixed before implementation/research

Use a generic integer noisy local search minimizing the number of K4 plus independent 5-sets. Start at n=5, the larger forbidden-set cardinality in the problem definition. Once score zero is obtained, save the certificate and increment n by one, with no known-value horizon. Initialize each target with independently generated edge bits. Do not import prior-stage artifacts or remembered constructions.

A candidate evaluation is exactly one proposed complete graph scored: either a fresh random initialization/restart, or one uniformly indexed edge flip from the current graph (index by PRNG output modulo edge count, documented modulo bias). Rejected flips count. Computing a delta instead of a full score does not change this definition. Verification of stored graphs, test/replay calls, serialization and rebuilding derived caches consume zero research candidates. The index k belongs to the candidate evaluated in transition S(k) to S(k+1).

Use an explicit xorshift64* generator with nonzero seed 20260922, unsigned 64-bit masking and multiplier 2685821657736338717. Each draw updates the stored internal state; never use time/random library. All decisions use integers. Accept non-worsening flips; for worsening delta d, accept if next draw modulo 1024 is below floor(noise/(1+d)), where noise=max(1,128-floor(127*iteration/restart_interval)). Restart after 10,000 evaluated candidates in a restart. A restart is another counted initialization candidate. Retain the best graph for the current target across restarts; ties retain the first. Per-target iteration/restart counters and all PRNG state are serialized.

Compute edge-flip deltas by counting edges among common neighbors (affected K4s) and triangles among common nonneighbors (affected independent 5-sets). Full scores and certificate-only verification use exhaustive combinations, separately from the delta implementation.

JSON checkpoint contains all semantic state, immutable raw-file code/config SHA-256 hashes, execution base, code commit, phase, timestamp metadata and payload digest. No opaque runtime cache is persisted or required. Validation recomputes graph scores and checks counters and all embedded certificates. Best-so-far and valid certificates are also exported as JSON.

## Pre-registered tests (outside research budget)

- Fixed split test: seed 123456789, start_n=5, restart_interval=7, a=111, b=157. Compare every semantic state field for uninterrupted 268 versus 111 + serialize/load + 157. Exclude only checkpoint wrapper metadata (timestamp, phase, execution base, code commit, hashes), never any field inside state. Total test candidate evaluations: 536.
- Additional split at an initialization/target boundary and a restart boundary, counted separately in saved test results.
- Compare incremental deltas with exhaustive full scores across every 5-vertex graph/edge and deterministic 8-vertex samples; these are verification score checks, not candidate transitions.
- Tampered checkpoint/config/code hashes and malformed graphs must fail validation.

## Inputs and workflow

Read Goal, problem, handoff protocol, operational rules, methodology (accidentally all sections, disclosed), and Stage 3 PR policy evidence. No other mathematical sources. Existing r4-5 research notes may be read now that this plan is fixed. Existing Stage 3 evidence records active main PR rule and no bypass as of 2026-09-21; no destructive push test.

Commit code/config/tests before research to fix code identity. Save exact consumed [0,2000000) and next index 2000000; validate without new research; document and commit artifacts; explicitly push `git push -u origin HEAD:refs/heads/codex/r45-h001-a-checkpoint`; open/prepare a PR and stop. Phase B requires merge of this PR and a separate fresh session, with its actual main execution base recorded.
