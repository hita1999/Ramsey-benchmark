# A finite witness proving R(4,5) ≥ 25

Define the graph G on the vertex set Z/24Z. Two distinct residues i,j are adjacent precisely when their circular distance min((i-j) mod 24, (j-i) mod 24) belongs to D={1,2,4,8,9}. Hence G is a 10-regular graph with 24 vertices and 120 edges.

## Finite verification

The dependency-free Python 3.9+ program [verify_lower24.py](verify_lower24.py) explicitly enumerates every 4-subset and 5-subset of the 24 vertices. For each 4-subset, it tests whether all six unordered pairs are edges. For each 5-subset, it tests whether all ten unordered pairs are nonedges.

The saved result [lower24-result.json](lower24-result.json) is:

- all C(24,4)=10,626 four-subsets inspected; 0 copies of K4;
- all C(24,5)=42,504 five-subsets inspected; 0 independent sets of size 5;
- every vertex degree is 10, total edges 120.

The loops cover each subset exactly once. Their tests are equivalent to the forbidden subgraph definitions, so the existence of G gives a two-coloring of K24 without a monochromatic K4 in the edge color or monochromatic K5 in the nonedge color. Therefore **R(4,5) > 24**, i.e. **R(4,5) ≥ 25**.

Reproduce:

```sh
python3 research/r4-5/verify_lower24.py
```

## Scope

This is a concrete, independently reproducible finite witness, distinct from Stage 4's 23-vertex/114-edge witness. Its generation was a local search among cyclic distance sets; the verifier enumerates *all vertex subsets* of the chosen graph without relying on that search.

It is an independently checked calculation in this work session, **not yet a second-reviewer ACCEPTED claim**. It does not give the upper bound R(4,5) ≤ 25.

No Stage 4 experimental counter, checkpoint, or prior claim is modified.
