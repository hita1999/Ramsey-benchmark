# ChatGPT Independent Review Protocol

Review Git as the source of truth. Do not rely on the Codex conversation, self-assessment, or unstored reasoning.

## Inputs

At minimum, receive:

- benchmark path;
- base commit before the Goal;
- result commit after the Goal;
- files changed by the Goal.

Prefer reviewing the commit diff first, then inspect dependencies as needed.

## Review posture

Attempt to falsify the claimed result before accepting it.

Check in particular:

1. the exact statement being claimed;
2. whether the evidence proves that statement rather than a nearby one;
3. whether computational exploration is being mistaken for exhaustive proof;
4. whether all cases are covered;
5. whether WLOG or symmetry reductions are justified;
6. whether edge cases, integrality, and boundary conditions are handled;
7. whether the proof depends circularly on another claim;
8. whether a certificate can be independently checked from the repository alone;
9. whether a fresh session could resume without hidden conversation context.

## For lower-bound certificates

Independently verify that:

- the encoded object has the claimed number of vertices;
- the graph/coloring representation is unambiguous;
- no forbidden red triangle exists;
- no forbidden blue `K_4` exists;
- the verifier actually checks the full relevant search space for the fixed certificate.

Where practical, use a verification path distinct from the discovery path.

## Required output

Update `verification.md` with:

- Claim ID;
- source/result commit;
- verification method;
- whether the verification path is independent;
- `ACCEPTED`, `REJECTED`, or `NEEDS_REVISION`;
- any remaining assumptions or gaps.

If accepted, update `research-notes.md` so mathematical status and review status remain distinguishable.

Do not silently repair a failed proof and then approve the original claim. Record the failure and create a new Goal or revision path.