# H001-B verification and review handoff

H001-B is **SOLVED** at researcher submission: the declared continuation completed, and the operational handoff self-audit is **PASS × UNREVIEWED**. Independent Phase B review and PR integration are pending. This is not a statement that the mathematical problem R(4,5) is solved. Its current result remains **R45-C001: R(4,5)>=24, PROVEN × ACCEPTED** from Phase A; no new Claim or certificate was found.

## Provenance and resume

- Actual freshly fetched execution base: `e1299901c3533ce1f6843c425ff8c458b834facc`.
- Phase A merge: `5f061f2df33e74e7b416e958ca1e427536763ce9` (PR #15); receipt merged in PR #16.
- Notes-only disclosure commits: `3a86852` and `1a1ae3f`.
- Pre-research startup audit, tests and observer committed as `d1c5cdf7e1dfa3a8750f6aaaaab7fc99248203c3`. This is the executing HEAD in the final checkpoint.
- Branch: `codex/r45-h001-b-resume`; explicit push: `git push -u origin HEAD:refs/heads/codex/r45-h001-b-resume`.
- Fresh session: user provided repository URL and Goal only. No Phase A conversation, extra semantic instructions or user questions. Input file paths and hashes are in `startup-audit.json`; disclosure is in `../h001-b-discovery.md`. This is a recorded session attestation, not a cryptographic proof of absent hidden context.
- All 26 manifest artifacts matched working files and base-commit bytes. Phase A code/config history is reachable. Python, executable, platform and architecture match Phase A; no optional-environment difference was found.
- Missing or ambiguous semantic checkpoint fields: 0. The manifest's historical UNREVIEWED metadata is explicitly superseded by the merged review/receipt; it does not change search state.

The exact manifest command, resolved immutable-base command/argv and actual launcher command are saved in `startup-audit.json`. `run_resume.py` invokes the unchanged search CLI with runpy and identical arguments. Its callback observes the first `step` entry, verifies the complete semantic-state digest, writes the index/time record, and disables profiling. It does not modify any state/config/PRNG value or search function. The observer and audit were fixed in Git before research.

Startup audit was executed twice before research, with zero transitions both times; the second saved result includes the final disclosure file hash. The test suite was executed once (556 test transitions). The research launcher was executed exactly once.

## Interval evidence

| Measurement | Result |
|---|---|
| Phase A interval | [0, 2,000,000) |
| Phase B interval | [2,000,000, 10,000,000) |
| First observed Phase B candidate | 2,000,000 |
| Last evaluated candidate | 9,999,999 |
| Final next-candidate index | 10,000,000 |
| Combined interval | [0, 10,000,000) |
| Repeated research indices / gaps | 0 / 0 |
| Additional Phase B research evaluations | 8,000,000 |
| Phase B test/replay transitions | 556 (separate seeds/configs; outside research) |
| Both phases' test transitions | 1,112 |
| Phase B delta verification comparisons | 11,136 (outside research) |
| Phase A trajectory replay | 0 |

First-state digest equals the Phase A digest `e93c2555c8ef11e173ea2a8c1357b09052f004716babc4e1cea68be95d8a051a`. The unchanged `advance` iterates once per counted candidate, and unchanged `step` increments the index exactly once. Eighty successive progress blocks advance by 100,000, ending at 10,000,000. This supplies code/counter evidence for no gaps/overlap. No complete uninterrupted 10M trajectory was recomputed or claimed as an independent equivalence test.

All three preregistered split/resume tests compare every semantic field and canonical state bytes, including initialization and restart boundaries. Phase B test output is identical to Phase A's saved output. Negative integrity/certificate controls and delta checks also pass.

Final counters: completed targets total 477,561; live target total 9,522,439 = 952*10,000 + 2,439; sum 10,000,000. Target n=24, current score 27, best score 4; PRNG internal word `17278674351399343217`. Best score 4 is not a certificate and supplies no upper bound or nonexistence result.

Final checkpoint SHA-256: `10702e9992f823cfc18135fc68537ca7171506c1f6382b9005a7c87426ee05f4`.
Final semantic-state SHA-256: `de0b95aa593d14e63b48fc85786175ad5dd13eff5447f86841dc532346190bff`.
`artifact-manifest.json` hashes the saved outputs, certificates, audits and observer. All 19 certificates n=5..23 are carried forward unchanged and exhaustively reverified. An isolated process receives only verifier and strongest certificate; it confirms 23 vertices, 114 edges, zero K4 and zero independent 5-sets. These are researcher self-checks, not new independent review.

## Measurements and interpretation

Session start is 2026-09-22T08:45:00Z from goal-service createdAt, with second resolution. First research step entry was 08:50:10.815747Z: **310.815747 seconds** after that start. The callback writes the observation immediately before the transition body; this measures function entry rather than the instant its first score arithmetic executes.

CLI start 08:50:10.814842Z; serialized/validated finish 08:51:58.467393Z. Research plus final serialization/validation took **107.658952708 seconds**, measured with monotonic time. Startup reconstruction, tests, final auditing, documentation, commits and push are separate session overhead. Outcome/PR/completion measurement events belong in `submission-record.json`; recording/pushing the final completion snapshot is postprocessing and not research time.

Actual runtime model and reasoning effort are missing; recommended gpt-6-astra/high is not substituted. Goal-service token counters are tool-reported accounting units, not generated tokens or monetary cost. Cost is missing. Discovery remains CONTAMINATED, independent of correctness and operational handoff fidelity.

`run/run-result.json` deliberately retains the unchanged search program's PARTIAL_PROGRESS status for the mathematical workload. H001-B's operational goal is SOLVED and its handoff self-evaluation PASS. Independent review remains UNREVIEWED; these are distinct axes.

## Verify without research replay

From repository root, these commands consume zero research candidates:

```sh
python3 benchmarks/r4-5/search.py validate --config benchmarks/r4-5/h001-a/config.json --checkpoint benchmarks/r4-5/h001-b/run/checkpoint.json --expected-sha256 10702e9992f823cfc18135fc68537ca7171506c1f6382b9005a7c87426ee05f4
python3 benchmarks/r4-5/verify.py benchmarks/r4-5/h001-b/run/certificates/*.json
```

For a full self-audit, run `python3 benchmarks/r4-5/h001-b/audit.py` in a disposable checkout of the submitted branch. It rewrites derived audit JSON and timestamps; it never invokes a candidate transition. The separate `python3 benchmarks/r4-5/test_search.py` performs 556 explicitly labeled test transitions if rerun. Do not run `run_resume.py` as a verification step: it is the one-shot research launcher and rejects existing first-candidate/output files. Do not run `start` to reconstruct Phase A. Original search budget is exhausted; new research requires a new Goal/versioned continuation contract.

## Independent reviewer and integration ownership

The independent Reviewer should save `benchmarks/r4-5/reviews/H001-B.md` and any separate checker/results under `benchmarks/r4-5/review/`. Review the startup audit's pre-research commit, exact first-state digest, observer transparency, code/config continuity, merged Phase A ancestry, interval arithmetic, progress, split-test evidence and certificate checks. Record operational acceptance separately from R45-C001's already ACCEPTED mathematical status.

The Reviewer owns synchronization of research-notes.md, proof.md, verification.md and results/benchmark-summary.md for the review verdict. The integrator verifies synchronization and uses a normal merge commit, retaining the executing `d1c5cdf...` ancestry used by this audit. The integrator then records merge SHA/time and remaining work in a subsequent PR-based `results/r45-h001-b-integration-receipt.md`. No independent approval, merge or integration receipt is fabricated here.
