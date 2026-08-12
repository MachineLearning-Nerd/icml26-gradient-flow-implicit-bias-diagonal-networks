# Status

- OpenReview ID: IJph1t3Egr
- Paper: Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization
- Claims / maximum points: 2 / 4
- Source: arXiv 2607.12332, SHA-256 pinned in `evidence/source/SHA256SUMS`.
- Current phase: verified-source recovery and bounded Claim 1 Algorithm 1 audit complete; **toy only**.
- Compute: local CPU/local GTX 1050 only.
- Next: independently review the bounded toy against the paper appendix, then assess whether a source-faithful gradient-flow experiment is feasible.

- 2026-08-03 source-recovery checkpoint: existing arXiv pin 2602.11401 was unrelated to this contracted paper; direct OpenReview PDF/API recovery returned ChallengeRequiredError 403. The mismatch was preserved as legacy evidence.
- 2026-08-12 verified-source checkpoint: exact-title arXiv 2607.12332 recovered the primary source and appendix fixture. The local exact-fraction audit selects features 1, 3, and 4 and reaches `(0, 0, 10/7, -10/49)` with zero residual. It also detects that the appendix prints `delta_1=20` at `p=3`, while Algorithm 1's displayed formula gives `delta_1=40`; the discrepancy does not change selection. Evidence: `outputs/claim1_algorithm1_toy/` and `outputs/claim1_source_recovery/RECOVERY.md`.
