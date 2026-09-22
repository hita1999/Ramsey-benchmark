# R45-C001 — R(4,5) >= 24

Mathematical state: **PROVEN** by a finite certificate. Independent review: **UNREVIEWED**. Discovery: **CONTAMINATED** (see h001-a-discovery.md). No previous-stage Claim is a dependency.

Let G be the graph on vertices 0 through 22 whose 114 edges are listed in `h001-a/run/certificate.json` (identical to `h001-a/run/certificates/n23.json`).

The certificate-only program `verify.py` checks endpoint ranges, absence of loops and duplicate edges, and then enumerates every 4-subset and every 5-subset of the vertex set. A 4-subset is a K4 exactly when all six of its pairs are edges. A 5-subset is independent exactly when none of its ten pairs is an edge. Thus these finite loops examine all forbidden structures without any assumption about how G was discovered.

The recorded output is zero K4s and zero independent 5-sets. Color the edges of G red and its other pairs blue. There is no red K4 and no blue K5. Therefore the assertion defining R(4,5) fails on 23 vertices, so R(4,5)>23, equivalently R(4,5)>=24.

To reproduce the finite verification from repository root:

```sh
python3 benchmarks/r4-5/verify.py benchmarks/r4-5/h001-a/run/certificate.json
```

The proof depends on the complete certificate and exhaustive verifier, not on the local-search score or a remembered Ramsey value. A separate isolated-process self-audit copied only the verifier and certificate; see `h001-a/isolated-verification.json`. Independent-session mathematical review is still outstanding.
