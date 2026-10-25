# Research session boundaries

## Initial 30-minute budget

- Start: 2026-10-25 15:09:48 JST (06:09:48 UTC).
- Mathematical computation stopped with 198/358 degree-8 gluing proofs
  checked, one solver timeout, and 159 further cases not attempted.
- The independent full checkpoint replay passed. The checkpoint and replay
  log were committed within the initial research window, at commit
  `190d06261a25bd263ef2d2a65a900b802be041ef`.
- Uploading approximately 780 MiB of compressed proof artifacts required
  additional transfer time and retries. No mathematical computation was
  added during that transfer. The checkpoint was submitted as draft PR #22.

## Continuation 1

- The user requested “続けて”. A choice of additional time limits was offered;
  absent a different preference, the agent stated it would use another
  30-minute limit.
- Start: 2026-10-25 20:36:08 JST (11:36:08 UTC).
- Research deadline: 2026-10-25 21:06:08 JST (12:06:08 UTC).
- Scope: finish the remaining degree-8 gluing checks if possible, replay the
  resulting checkpoint, and update the same PR. Degrees 10 and 12 remain
  outside the completed verification unless separate evidence is produced.
- Previously verified proof records are reused only after both associated
  artifact hashes match. The final reproduction run checks every saved proof
  again, without a SAT solver.
- All 358 degree-8 gluing certificates passed their individual independent
  checks by 20:48:22 JST (11:48:22 UTC).
- The complete solver-free reproduction run finished successfully, confirmed
  at 20:54:07 JST (11:54:07 UTC): lower witness, three exhaustive catalogues,
  two encoding audits, 54 coverage refutations, 358 gluing refutations, and
  17 checker tests. The new log is `results/replay.log`; the initial log is
  preserved as `results/replay-initial.log` and in the initial Git checkpoint.
- Degree 8 is therefore closed within this verification system. Degrees 10
  and 12 remain unverified; the overall status remains `PARTIAL_PROGRESS`.
- After these checks had completed, the user's answer selected checkpoint
  PR submission only. Research remains stopped; only artifact transfer and
  PR submission updates are continued. No degree-10/12 research was started.

The latest exact case ledger is `CHECKPOINT.json`; the earlier 198-case ledger
remains available in the initial checkpoint commit. A time limit is never
interpreted as an UNSAT proof.
