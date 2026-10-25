# Independent verification: proved statements and remaining obligations

This is a finite computational verification with new programs, not a HOL4 replay.
The overall status is **PARTIAL_PROGRESS**, not an independent proof of
`R(4,5)=25`. The precise machine-checked subset is recorded in `results/` and
`CHECKPOINT.json`. A SAT solver's failure, timeout, or UNSAT message is never
accepted as a proof.

Write `(s,t,n)` for a simple undirected n-vertex graph having neither a clique
of size s nor an independent set of size t. Edges are the clique color.

## 1. Lower bound, independently rechecked

On vertices 0,...,23, insert the undirected edges `{i,(i+d) mod 24}` for every
i and d in `{1,2,4,8,9}`. This is exactly the circular-distance construction in
the parent directory: inserting an undirected edge inserts both offsets d
and -d, with neither loops nor duplicate opposite offsets in this set.

`src/lower24.cpp` constructs bitset adjacency rows. It does not import, execute,
or translate the pair predicate of the existing Python verifier. It iterates
all integer masks with exactly four or five bits set using the next-combination
formula. Summing popcounts of restricted adjacency rows counts each induced
edge twice. A four-set is a K4 precisely when the sum is 12; a five-set is
independent precisely when the sum is zero. The counters measure the actual
iterations, then compare them with the binomial coefficients.

The saved run inspects 10,626 four-sets and 42,504 five-sets, finds no forbidden
set, and verifies that all degrees equal 10 and that there are 120 edges.
Thus this explicit witness proves `R(4,5) >= 25`.

## 2. Degree reduction without assuming smaller exact Ramsey values

Only upper bounds for smaller Ramsey numbers are needed. Here are proofs of
all such bounds, so this step does not assume a published exact-value table.

1. `R(2,t) <= t`: a graph without any edge is an independent set. Taking
   complements proves `R(t,2) <= t` and, generally, symmetry of upper bounds.
2. If every a-vertex graph has a K(s-1) or independent t-set, and every
   b-vertex graph has a Ks or independent (t-1)-set, then `R(s,t) <= a+b`.
   In a hypothetical counterexample choose v. Its neighbors number at most
   a-1 and its antineighbors at most b-1, but their sum is a+b-1, impossible.
3. Applying this recurrence to `R(2,3) <= 3` and its complement gives
   `R(3,3) <= 6`.
4. In a hypothetical `(3,4,9)` graph each neighborhood is independent, so
   every degree is at most 3. Each antineighborhood is a `(3,3)` graph, so
   has at most 5 vertices. Thus every degree is exactly 3. The degree sum
   would be 27, whereas each edge contributes twice: contradiction.
   Hence `R(3,4) <= 9`, and by complements `R(4,3) <= 9`.
5. The recurrence now gives `R(3,5) <= 5+9 = 14` and
   `R(4,4) <= 9+9 = 18`.

Suppose F were a `(4,5,25)` graph. For every vertex v of degree d, its
neighborhood A is `(3,5,d)`: a triangle together with v would form a K4.
Its antineighborhood B is `(4,4,24-d)`: an independent four-set together
with v would form an independent five-set. Forbidden sets of the other
sizes are inherited from F. The preceding upper bounds imply
`d <= 13` and `24-d <= 17`, so `7 <= d <= 13`.

If all 25 degrees were odd, their sum would be odd, contradicting the
handshaking identity `sum deg(v) = 2|E|`. Thus at least one vertex has even
degree, necessarily **8, 10, or 12**. This is an existential choice of a
splitting vertex; it does not assert that all vertices have these degrees.

## 3. Complete catalogues on at most eight vertices

`src/catalogue8.cpp` is independent of nauty and all SAT solvers. It decodes
the provided graph6 representatives, checks their Ramsey property, and
enumerates **every permutation** of their n vertices. It stores the union of
their labeled edge masks in a bitset. The minimum mask of each orbit detects
isomorphic duplicate representatives.

Separately, it loops over every integer from 0 to `2^(n(n-1)/2)-1`. For every
graph it directly tests the masks of all s-subsets for cliques and all
t-subsets for independence. It requires equality, graph by graph, between
this predicate and membership in the stored orbit union. Therefore no
unlisted isomorphism class can be missed. This is an exhaustive check, not a
comparison of only the total counts with literature.

| Family | Representatives | All labeled graphs tested | Valid labeled graphs |
|---|---:|---:|---:|
| (3,5,8) | 179 | 268,435,456 | 2,728,617 |
| (3,4,7) | 9 | 2,097,152 | 13,842 |
| (3,4,8) | 3 | 268,435,456 | 17,640 |

Inputs are credited to McKay's public data collection, but their completeness
on these orders is rechecked by the above procedure, not assumed from that
collection's description.

## 4. Completeness of the two (4,4,16) candidates

In a `(4,4,16)` graph, neighbors of any vertex form a `(3,4)` graph and
antineighbors a `(4,3)` graph. The bound 9 from section 2 implies both sets
have at most eight vertices; as their sizes sum to 15, the degree is 7 or 8.

For degree d, the neighbors must be isomorphic to one of the fully checked
`(3,4,d)` representatives. The antineighbors must be isomorphic to the
complement of one of the fully checked `(3,4,15-d)` representatives.
There are `9*3 + 3*9 = 54` representative pairs. The two bijections act on
disjoint vertex sets, so they extend to a relabeling fixing the splitting
vertex. After relabeling, only the `d*(15-d)=56` cross edges are undetermined.

For each pair build a CNF F imposing no K4 and no independent four-set on
the full 16-vertex graph. For selected complete cross-edge assignments m
that are isomorphic to one of the two supplied 16-vertex graphs, add a
blocking clause `B_m`: it is false exactly at m. Every such m carries a
full 16-vertex permutation witness. The independent audit checks that the
permutation is bijective and preserves **every edge and nonedge**, including
the splitting vertex and both fixed sides. It also directly checks that
the target graphs really have the `(4,4,16)` property.

All 54 formulas `F AND conjunction(B_m)` have independently checked LRAT
refutations. Consequently every model of F equals a blocked assignment,
and hence is isomorphic to a supplied target graph. Completeness of the
producer's list of blocking assignments is **not** assumed: omitted models
would leave a satisfiable formula and prevent a valid refutation. There are
128 blocking witnesses in total across these 54 formulas.

Together with the small catalogues and the degree argument, this proves the
two graphs cover **all** `(4,4,16)` graphs up to isomorphism. They are distinct
isomorphism classes: the first has zero nonadjacent degree-7 vertex pairs
with exactly two common neighbors, whereas the second has eight. This
isomorphism invariant is recomputed in `results/r44_16-invariants.json`.

## 5. Gluing semantics and the exact boundary of the checked upper bound

For a fixed `(3,5,8)` graph A and `(4,4,16)` graph B, add v adjacent to all
of A and none of B. Variable `1 + 16*a + b` is the edge from a to b.
For every four-subset prohibit all its pairs being edges; for every
five-subset prohibit all its pairs being nonedges. Substitute the fixed
relations and discard satisfied clauses. This is an exact CNF encoding:
each truth assignment specifies one graph and satisfies the formula iff
that graph has the required Ramsey property.

The producer uses products of homogeneous subsets of the two sides. The
independent audit instead enumerates all subsets of the entire 25-vertex
set, **including v**, substitutes constants pair by pair, and compares the
complete clause multisets. Thus the omission of v from the producer's
optimization is checked, not merely presumed. No degree constraints,
isomorphism clauses, solver assumptions, or symmetry breaking are added to
these 358 gluing formulas.

Both candidate lists are complete, and **all 358 gluing instances now have
saved certificates accepted by the independent checker**. Therefore no
`(4,5,25)` graph has a degree-8 vertex: choosing such a vertex would give a
pair isomorphic to one of these representatives, and its cross edges would
satisfy a CNF that has been refuted. Relabeling the two sides is legitimate
because they are disjoint and all cross-edge assignments were allowed.

`CHECKPOINT.json` lists every pair and its status. The initial checkpoint
contained 198 accepted refutations; the continuation supplies the other 160,
including a valid refutation for the previously timed-out instance. A timeout
was not used as evidence. In general, an absent certificate, timeout,
unfinished job, or missing result is **unresolved**.

**The degree-8 case is closed. Degrees 10 and 12 are not checked.** By section
2 a hypothetical counterexample must therefore have a vertex of degree 10
or 12. Excluding these remaining cases is still necessary; the final upper
bound and equality are not claimed.

## 6. Independent proof checker and trust boundary

CaDiCaL produces text LRAT proofs with `--plain --lrat --no-binary`.
`src/check_lrat.cpp` is newly written and contains no solver or external
checker code. For each added clause C it assumes every literal of C false
and checks that the indicated preceding clauses yield a contradiction by
unit propagation. Initial clauses are indexed in DIMACS order. Unknown or
forward references, nonunit hints, unsupported negative RAT hints, malformed
input and proofs without a verified empty clause are rejected. Duplicate
literals are normalized. Deletions are ignored: retaining already proved
consequences is sound for this RUP-only proof system.

Soundness argument: by induction every accepted clause is entailed by the
original CNF. Otherwise a model falsifying C would satisfy all earlier
clauses and its negated literals, so sound unit propagation could not
derive a contradiction. An accepted empty clause therefore implies that
the original CNF has no model. The optional dependency-cone trimmer is an
untrusted producer too: its output must pass this same checker.

The trusted computation consists of the saved audit/checker sources, their
compilers/interpreters, and the execution platform. This does not reduce the
trust base to a theorem-prover kernel. Adversarial tests increase confidence
but are not a formal proof of the implementations. Neither solver output
nor SHA256 hashes alone establish mathematical correctness; hashes bind the
actual inputs and accepted certificates to the recorded runs.

## 7. External facts, not replayed here

- B. D. McKay and S. P. Radziszowski, *R(4,5)=25*, Journal of Graph Theory
  19 (1995), 309–322, [original paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
  DOI [10.1002/jgt.3190190304](https://doi.org/10.1002/jgt.3190190304).
  The paper proves the full theorem computationally. Its original decomposition
  is different from the three-even-degree reduction used here.
- T. Gauthier and C. E. Brown, *A Formal Proof of R(4,5)=25*, ITP 2024,
  [paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.16),
  [preprint](https://arxiv.org/abs/2404.01761),
  [HOL4 sources](https://github.com/barakeel/ramsey).
  Their work supplies a HOL4 formal proof and uses the even-degree splitting
  argument. No HOL4 build or replay was performed in this session.
- [McKay's Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
  supplies the four graph6 files. File hashes and exact URLs are recorded in
  `PROVENANCE.json`. The rechecked scope is specified above.

The published equality is background knowledge, not a premise used to
justify any missing computation in this checkpoint.
