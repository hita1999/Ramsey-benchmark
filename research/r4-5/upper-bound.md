# Proving the upper bound R(4,5) ≤ 25

**Status: NOT YET independently established within this repository.**

The theorem R(4,5)=25 was established by B. D. McKay and S. P. Radziszowski, *R(4,5)=25*, Journal of Graph Theory 19 (1995), 309–322, DOI 10.1002/jgt.3190190304. Thibault Gauthier and Chad E. Brown, *A Formal Proof of R(4,5)=25*, ITP 2024, DOI 10.4230/LIPIcs.ITP.2024.16, formalized the theorem in HOL4. These are published external mathematical results, not a claim that this repository has independently checked the 25-vertex exhaustive exclusion.

Original text: https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf

Formal proof: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.16

Formal proof code: https://github.com/barakeel/ramsey

## 1. An elementary reduction (proved here)

Assume for contradiction there is a 25-vertex graph F with neither K4 nor an independent set of size 5. Fix a vertex v, let d be its degree, A=F[N(v)] its induced neighbor subgraph, and B=F[V(F)\\(N(v)∪{v})] its induced antineighbor subgraph.

Then:
- A cannot contain a triangle (it would form a K4 together with v), and A cannot contain an independent 5-set (it would also be one in F): A is a (3,5,d)-graph.
- B cannot contain a K4 (it would be one in F), nor an independent 4-set (together with v it would form an independent 5-set): B is a (4,4,24-d)-graph.
- The accepted values R(3,5)=14 and R(4,4)=18 imply d ≤ 13 and 24-d ≤ 17, respectively, so **7 ≤ d ≤ 13**.
- In every finite graph the number of odd-degree vertices is even (handshaking lemma). Because F has 25 vertices, at least one vertex has even degree. At that vertex, the allowed range 7..13 gives exactly **d∈{8,10,12}**.

Therefore, to establish R(4,5) ≤ 25 it is sufficient to exclude all compatible gluings for these three degree cases.

## 2. Exact gluing condition

For fixed (3,5,d)-graph A and (4,4,24-d)-graph B, form a hypothetical 25-vertex F by adding vertex v, connecting v to all vertices of A, leaving v nonadjacent to all vertices of B, and choosing all edges between A and B. Write x_ab∈{0,1} for every possible cross edge a∈A,b∈B.

Within A and B all edge/nonedge relations are fixed. The exact constraint formula is:

- For every 4-subset T⊆A∪B whose internal A-pairs and B-pairs are all edges, prohibit all its cross pairs simultaneously being edges; this gives the clause OR_{a∈T∩A,b∈T∩B} (not x_ab).
- For every 5-subset T⊆A∪B whose internal A-pairs and B-pairs are all nonedges, prohibit all its cross pairs simultaneously being nonedges; this gives OR_{a∈T∩A,b∈T∩B} x_ab.

Sets including v are already excluded by the (3,5) and (4,4) constraints. Thus **this CNF is satisfiable iff the fixed A and B extend to a (4,5,25)-graph with splitting vertex v**.

A complete upper-bound proof requires an exhaustive and independently checkable enumeration/cover of the possible A and B graphs for d=8,10,12, together with checkable UNSAT evidence for every gluing possibility. A sampled search, failure to find a graph, or unsatisfiability for only some pairs is NOT a proof.

## 3. Concrete next research task

1. Start with d=8. The 1995 enumeration and the 2024 formal proof report 179 nonisomorphic (3,5,8)-graphs and 2 nonisomorphic (4,4,16)-graphs. Verify the census/canonicalization rather than blindly trust its completeness, then check all 358 representative gluings using a SAT solver and a checkable proof format.
2. Develop graph-generalization covers and reliable isomorphism witnesses for d=10 and d=12; naive pair products are enormous. The original result uses exhaustive gluing; the later formalization relies on SAT and HOL4.
3. For every excluded pair, preserve a machine-checkable UNSAT proof (or formally check the inference in a theorem prover). Independently audit the exhaustiveness of all covers, not merely individual SAT outputs.
4. Only after all three d-cases are closed, combine with [the 24-vertex witness](lower-bound.md) and mark R(4,5)=25 independently proved by this project.

The published proof may be cited to explain the known mathematical fact R(4,5)=25. **Reproducing it is a separate and much larger task**, especially given that the 2024 formal verification reports multiple days of highly parallel computation and substantial RAM.
