# Codex Goal Protocol

Use this document to start a bounded research task from Git. The repository is the source of truth; conversation history is optional and must not be required for resumption.

## Goal contract

Every Goal should specify:

- Goal ID
- Benchmark
- Base commit
- Research question
- Allowed methods
- Forbidden information
- Required artifacts
- Acceptance criteria
- Token / compute budget
- Checkpoint policy
- Stop conditions

At Goal completion or interruption, update Git with:

1. newly established claims;
2. computational-only findings;
3. refuted hypotheses / failed approaches;
4. remaining cases;
5. current bottleneck;
6. concrete next-step recommendation;
7. enough information for a fresh session to resume.

Do not report budget exhaustion as mathematical success.

---

# G001 — Construct a lower-bound certificate for R(3,4)

## Benchmark

`benchmarks/r3-4/problem.md`

## Research question

Without consulting external known solutions, find a concrete red/blue coloring (equivalently, a graph) on as many vertices as you can that contains neither a red triangle nor a blue `K_4`.

The immediate objective is not to determine the exact Ramsey number. The objective is to create the first reproducible, independently checkable lower-bound certificate in this benchmark.

## Allowed methods

- direct mathematical construction;
- Python search;
- brute force where feasible;
- local search / randomized search;
- SAT/SMT or other finite constraint solving;
- symmetry reduction.

## Forbidden information

- web search;
- papers, OEIS, databases, benchmark repositories, or reference implementations;
- intentionally using a memorized exact value, known critical graph, or known proof.

If prior knowledge is involuntarily recalled, record it under `Known contamination` in `research-notes.md` and do not use it as evidence.

## Required artifacts

At minimum:

1. an explicit certificate (edge list, adjacency representation, or coloring representation);
2. a verifier that checks the certificate for both forbidden configurations;
3. instructions to reproduce the verification;
4. an update to `research-notes.md` with a Claim ID and precise status;
5. a concise record of failed search approaches that would otherwise be repeated by a fresh session.

Put code and certificates under `benchmarks/r3-4/` in clearly named files or subdirectories.

## Acceptance criteria

The Goal is `SOLVED` only if:

- a concrete certificate is stored in Git;
- the verifier deterministically confirms the claimed avoidance properties;
- the claimed lower bound follows directly from that certificate;
- `research-notes.md` is updated so another session can understand exactly what has been established.

Independent verification is not required to finish G001; that is a separate review step. Until reviewed, do not describe the result as independently verified.

## Budget

Use a bounded research run. Prefer simple, auditable computation over elaborate infrastructure for this first benchmark. If the run is nearing its token or compute limit, checkpoint partial progress rather than compressing reasoning into an unsupported conclusion.

## Stop conditions

End with exactly one research outcome classification:

- `SOLVED`
- `PARTIAL_PROGRESS`
- `EXHAUSTED_BUDGET`
- `BLOCKED`
- `NO_PROGRESS`

Regardless of outcome, commit or otherwise save the durable research state before stopping.