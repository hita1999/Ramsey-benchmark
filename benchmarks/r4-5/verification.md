# H001-A verification record

All checks below are researcher self-audits. R45-C001 is **PROVEN × UNREVIEWED**, not independently accepted.

- Split/resume: PASS on fixed 111+157 test, initialization/target boundary 1+1, and restart boundary 7+1. All semantic fields and their canonical JSON bytes agree. Exact test configs, state hashes and excluded wrapper metadata are in `h001-a/test-result.json`; executable code is `test_search.py`.
- Test candidate transitions: 556, all explicitly TEST_REPLAY_OUTSIDE_RESEARCH_BUDGET. No real research trajectory was replayed.
- Delta verification: 11,136 full-score comparisons (every graph and edge at n=5, plus 32 deterministic n=8 samples); PASS.
- PRNG scalar arithmetic, seven hash/semantic corruption rejection controls, and six invalid-certificate controls: PASS.
- Real checkpoint: loader and full graph-score validation PASS at next_candidate_index=2,000,000. See `h001-a/checkpoint-validation.json`. Validation consumes zero research candidates.
- All 19 certificates n=5..23: exhaustive certificate-only verification PASS, recorded in `h001-a/certificate-verification.json`.
- Strongest certificate: isolated Python process supplied only verify.py and certificate.json confirms n=23, 114 edges, zero K4 and zero independent 5-sets. `h001-a/isolated-verification.json` records environment and output; this is an independent code path/process, not an independent researcher/session.
- Phase B: NOT RUN. Cross-session exact resume and combined-interval audit remain pending after this checkpoint PR is merged.

Operational Phase A mechanism checks: PASS. Overall handoff experiment: **PARTIAL_PROGRESS**, pending fresh-session H001-B and its audit. Current 24-vertex best score 4 is not a valid certificate and supplies no lower bound beyond R45-C001.

Reviewer handoff: a later independent reviewer should record verdicts under `reviews/H001-A.md` (or the explicitly assigned next review Goal), including code/checkpoint integrity and R45-C001. The reviewer/closure owner synchronizes proof.md, research-notes.md, verification.md and results/benchmark-summary.md through a PR. The integrator records the merge SHA/time and remaining Phase B/review work through a subsequent documentation PR. This Phase A session neither merges its own checkpoint nor starts H001-B.
