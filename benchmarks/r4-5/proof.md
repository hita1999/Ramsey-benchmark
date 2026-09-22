# R45-C001 — R(4,5) >= 24

Mathematical state: **PROVEN** by a finite certificate. Independent review: **ACCEPTED** ([H001-A independent review](reviews/H001-A.md)). Discovery: **CONTAMINATED** (see h001-a-discovery.md). No previous-stage Claim is a dependency.

Let G be the graph on vertices 0 through 22 whose 114 edges are listed in `h001-a/run/certificate.json` (identical to `h001-a/run/certificates/n23.json`).

The certificate-only program `verify.py` checks endpoint ranges, absence of loops and duplicate edges, and then enumerates every 4-subset and every 5-subset of the vertex set. A 4-subset is a K4 exactly when all six of its pairs are edges. A 5-subset is independent exactly when none of its ten pairs is an edge. Thus these finite loops examine all forbidden structures without any assumption about how G was discovered.

The recorded output is zero K4s and zero independent 5-sets. Color the edges of G red and its other pairs blue. There is no red K4 and no blue K5. Therefore the assertion defining R(4,5) fails on 23 vertices, so R(4,5)>23, equivalently R(4,5)>=24.

To reproduce the finite verification from repository root:

```sh
python3 benchmarks/r4-5/verify.py benchmarks/r4-5/h001-a/run/certificate.json
```

The proof depends on the complete certificate and exhaustive verifier, not on the local-search score or a remembered Ramsey value. A separate isolated-process self-audit copied only the verifier and certificate; see `h001-a/isolated-verification.json`.

The independent Reviewer additionally used `review/r45-h001-a-independent.py`, which imports neither `search.py` nor the research-side `verify.py`, and exhaustively checked all `C(23,4)=8,855` four-sets and `C(23,5)=33,649` five-sets. It found zero K4 and zero independent 5-set; see `review/r45-h001-a-independent-result.json`. Therefore R45-C001 is **PROVEN × ACCEPTED**.

## H001-B certificate continuity

The Phase B continuation completed [2,000,000,10,000,000) with no new certificate. The strongest output `h001-b/run/certificate.json` is byte-identical to the independently accepted Phase A n=23 certificate (raw SHA-256 `32d0e5d132297bb676195437d0458546e4b44611dc9654981eb05871004f5302`). All carried-forward certificates were rechecked by exhaustive certificate-only verification; the strongest also passed an isolated process with only verifier and certificate. See `h001-b/certificate-verification.json` and `h001-b/isolated-verification.json`.

R45-C001 remains **PROVEN × ACCEPTED**, with no new mathematical Claim or dependency. H001-B's operational PASS is a separate researcher evaluation, pending independent review. The n=24 best score 4 and failure to improve it within the budget do not prove nonexistence or any upper bound.
