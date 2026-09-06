# R(3,4) — Problem

## Objective

Determine the least integer `N` such that every red/blue coloring of the edges of `K_N` contains either:

- a red triangle `K_3`, or
- a blue clique `K_4`.

Equivalently, in graph language, determine the least `N` such that every graph on `N` vertices contains a triangle or its complement contains a `K_4`.

## Benchmark constraints

- Do not search the web, papers, databases, reference implementations, or other external sources for the known value or known proof of `R(3,4)`.
- Do not intentionally rely on a memorized exact value, known extremal graph, or known proof. If such information is recalled, record the contamination explicitly in `research-notes.md` and avoid using it as evidence.
- Standard graph theory, combinatorics, elementary linear algebra, SAT/SMT, Python, and exhaustive finite computation are allowed.
- Computational observations are not mathematical proofs unless completeness of the computation is established and the computation is reproducible.
- A concrete coloring/graph is acceptable as a finite certificate for a lower bound once independently checkable.

## Required final artifacts

A completed benchmark should eventually contain:

1. a valid lower-bound certificate;
2. a rigorous upper-bound argument;
3. a self-contained `proof.md`;
4. an independent assessment in `verification.md`;
5. enough information to reproduce any computation used as evidence.

## Source of truth

The Git repository, not any model's conversation history, is the source of truth for benchmark state. Research may stop and resume from Git alone.