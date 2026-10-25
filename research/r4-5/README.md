# R(4,5) — direct mathematical proof project

This is a **new mathematical effort outside Ramsey-benchmark v1.0**. It is not Stage 5, not a model comparison, and not an experiment on researcher-agent performance. Known published mathematics may be read and credited; no discovery-contamination scoring is attempted here.

**Mathematical theorem (published): R(4,5)=25.**

**Independent verification checkpoint (2026-10-25): PARTIAL_PROGRESS.**
See [independent/README.md](independent/README.md) for a second lower-bound
implementation, a self-contained degree reduction, exhaustive candidate
coverage checks, saved LRAT certificates, an independent checker, and the
exact unresolved-case ledger. The full upper bound is still not independently
proved here. This work does not modify the workflow benchmark.

**What this repository has actually re-established so far:**

- **Lower bound R(4,5)≥25:** explicit 24-vertex circulant graph and exhaustive check, [lower-bound.md](lower-bound.md) and [verify_lower24.py](verify_lower24.py).
- **Upper-bound starting lemma:** a hypothetical 25-vertex counterexample must have a vertex of degree 8, 10, or 12, with neighbor and antineighbor subgraphs of types (3,5) and (4,4), respectively; [upper-bound.md](upper-bound.md).
- **Upper-bound exhaustive certificate:** **not yet produced or independently checked here**. Reproducing the published computational/formal proof remains the substantive work.

Do not conflate the externally established theorem with the independently reproduced subset of its proof. Mathematical proof status here should only be upgraded after auditable evidence exists.

The separately completed [v1 workflow benchmark](../../results/benchmark-summary.md) retains its historical Stage 4 claim R(4,5)≥24 and original checkpoint state, unaffected by this work.
