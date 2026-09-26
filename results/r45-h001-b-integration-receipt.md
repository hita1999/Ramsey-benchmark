# R45 H001-B integration receipt

## Integration

- Recorded: 2026-09-26.
- Source PR: #17 `H001-B: resume merged checkpoint through 10M candidates with handoff PASS`.
- PR #17 merged at: `2026-09-26T05:46:48Z`.
- Merge commit: `fc823302ef231e57e2eb7945d0472e3221a4cf62`.
- Merge method: normal merge commit, not squash/rebase.
- Merge parents:
  - prior main: `e1299901c3533ce1f6843c425ff8c458b834facc`
  - reviewed PR head: `3503f0b03d4e4465a006b0cb6f3c52db19f6602f`
- Merge tree: `4027459141017539940901af44e90b698a30d6cf`.
- Reviewed PR-head tree: `4027459141017539940901af44e90b698a30d6cf`.
- Therefore the reviewed head tree was integrated unchanged.

## Historical source reachability

The Phase B final checkpoint names the pre-research executing code commit:

`d1c5cdf7e1dfa3a8750f6aaaaab7fc99248203c3`

Git comparison after merge reports that `d1c5cdf7...` is the merge base and the merged main commit is ahead of it, with no commits behind. The immutable Phase B code/audit ancestry therefore remains reachable from main, preserving the `git show <code_commit>:...` audit model.

## Final checkpoint anchor

Merged validation record:

- final checkpoint SHA-256: `10702e9992f823cfc18135fc68537ca7171506c1f6382b9005a7c87426ee05f4`
- final semantic state SHA-256: `de0b95aa593d14e63b48fc85786175ad5dd13eff5447f86841dc532346190bff`
- final next candidate index: `10,000,000`
- Phase B interval: `[2,000,000,10,000,000)`
- combined H001 research interval: `[0,10,000,000)`

The normal merge tree is identical to the reviewed PR-head tree, so the reviewed checkpoint bytes were integrated without conflict rewriting.

## Accepted state

- H001-A: acceptance criteria **PASS**.
- H001-B: **SOLVED**, operational handoff **PASS × ACCEPTED**.
- Overall H001 checkpoint-resume experiment: **operationally SOLVED / PASS accepted**.
- R45-C001: **PROVEN × ACCEPTED**, `R(4,5) >= 24`.
- No new mathematical Claim was established in Phase B.
- Mathematical `R(4,5)` workload: **PARTIAL_PROGRESS**.
- Discovery: **CONTAMINATED**.
- n=24 best score 4 remains heuristic state only; it is not a certificate, nonexistence proof, or upper bound.

Independent review: `benchmarks/r4-5/reviews/H001-B.md`.

## Closure and next work

This receipt is post-merge documentation only and consumes zero research candidates.

H001 has completed its registered operational objective: a deliberately unfinished checkpoint was merged, reconstructed from Git in a separate fresh session, and resumed without research-index overlap or gaps through the fixed endpoint.

Further search at n=24, a different heuristic, an upper-bound proof, or an attempt to determine the exact value of `R(4,5)` is outside H001 and requires a new Goal with a new budget and contamination record.
