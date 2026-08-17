# Status

- Repository: MachineLearning-Nerd/icml26-gradient-flow-implicit-bias-diagonal-networks
- Former name: icml26-repro-IJph1t3Egr-gradient-flow-implicit-bias-diagonal-linear-networks
- OpenReview ID: IJph1t3Egr
- Paper: Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization
- Claims / maximum points: 2 / 4
- Source: arXiv 2607.12332, SHA-256 pinned in evidence/source/SHA256SUMS.
- Phase: published_and_verified
- Overall verdict: INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY
- Publication of theorem-level claims: false
- Compute: local CPU/local GTX 1050 only; no paid, remote, upgraded, or HF compute.
- Branches: main only
- Claim C1: TOY_SOURCE_ALGORITHM1
- Claim C2: UNVERIFIED
- Next action: select the next ICML repository for a scoped source-and-claim audit.

## Evidence boundary

The canonical source is arXiv 2607.12332. The original local arXiv pin, 2602.11401, was unrelated and remains only as explicitly named legacy evidence. The local result is an exact-rational execution of the paper’s finite Algorithm 1 appendix fixture. It does not reproduce continuous-time gradient flow, the infinitesimal initialization limit, the theorem proof, or the paper’s high-precision gradient-descent figure.

## Completed checkpoints

- Verified the exact-title primary source and pinned its PDF and source archive.
- Preserved and documented the unrelated 2602.11401 recovery mismatch.
- Executed the four-feature Algorithm 1 fixture with exact fractions.
- Confirmed selected features 1, 3, and 4, final vector (0, 0, 10/7, -10/49), and zero residual.
- Recorded the paper’s printed delta_1=20 versus formula-derived delta_1=40; selection is unchanged.
- Normalized the repository identity and branch inventory.
- Published the standardized dossier, evidence manifest, and final verifier.
