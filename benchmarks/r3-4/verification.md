# R(3,4) — Independent Verification

## Review status

No claim has yet passed independent verification.

## Verification record template

For each reviewed claim, record:

- Claim ID:
- Source commit:
- Claim under review:
- Discovery method:
- Verification method:
- Independent from discovery path: `YES | PARTIAL | NO`
- Result: `ACCEPTED | REJECTED | NEEDS_REVISION`
- Remaining assumptions or gaps:
- Reviewer / model configuration:
- Notes:

## Required checks

For lower-bound certificates:

1. the graph/coloring is explicitly encoded;
2. a verifier checks every forbidden configuration;
3. the verifier is simple enough to audit or has an independent implementation;
4. the certificate and verifier produce the claimed result from a fresh checkout.

For upper-bound arguments:

1. every case is covered;
2. WLOG/symmetry reductions are justified;
3. computational observations are not silently promoted to proofs;
4. dependency chains contain no circular reasoning;
5. boundary and integrality cases are checked.