# Gradient Flow Implicit Bias: Source-Pinned ICML 2026 Reproduction Audit

Repository identity: MachineLearning-Nerd/icml26-gradient-flow-implicit-bias-diagonal-networks. The former repository name was icml26-repro-IJph1t3Egr-gradient-flow-implicit-bias-diagonal-linear-networks.

This repository is a claim-by-claim audit of **“Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization.”** It pins the verified paper source, records the paper’s claim-production path, executes the paper’s four-feature Algorithm 1 appendix fixture with exact rational arithmetic, and separates bounded local evidence from the paper’s unverified continuous-time theorem claims.

> **Current status:** published source-pinned audit with verdict **INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY**. Claim 1 has a **bounded Algorithm 1 toy audit**: it selects features 1, 3, and 4 and reaches the paper’s final vector (0, 0, 10/7, -10/49) with zero residual. Continuous-time gradient flow, the infinitesimal limit, and both theorem-level claims remain **unverified locally**.

## Paper and resources

- Paper: [arXiv:2607.12332](https://arxiv.org/abs/2607.12332)
- OpenReview: [IJph1t3Egr](https://openreview.net/forum?id=IJph1t3Egr)
- Pinned paper PDF: `evidence/source/arxiv.pdf`
- Pinned paper source: `evidence/source/arxiv_source.tar.gz`
- Contracted claims: `contract/live_claims.json`

The paper studies regression with diagonal linear networks under infinitesimal initialization. It extends saddle-to-saddle gradient-flow analysis from standard two-layer diagonal networks to deep diagonal networks and a broader class of analytic two-layer models. Its central mechanism is the Structural Invariant Manifold (SIM).

The original local pin, arXiv `2602.11401`, was unrelated to this paper. It is retained as `evidence/source/legacy-2602.11401-unrelated.*` for auditability and is not used as method evidence.

## What the paper does

The paper’s claim-production path is:

1. Define an analytic diagonal model `F(theta)(x) = sum_i k_i(theta_i) x_i` and squared-error loss `||Xk(theta)-y||_2^2`.
2. Evolve parameters with continuous-time gradient flow from an infinitesimally scaled initialization `s theta*`, with `s -> 0`.
3. Associate every feature and sign with a growth-time quantity `t_i+` or `t_i-`, derived from the deep-network trajectory integral or the extreme Hessian eigenvalues of a general two-layer model.
4. Use Algorithm 1: compute the residual correlation `u = X^T(y-Xk)`, select the inactive feature with the smallest remaining growth time, update the state vector `s`, and solve a sign-constrained least-squares problem over the active features.
5. Prove that Algorithm 1 terminates under stated assumptions and solves the weighted/modified l1 problem `min R(k) subject to Xk=y`, where `R(k) = sum_i (t_i+ k_i+ + t_i- k_i-)`.
6. Prove that the gradient-flow trajectory has the Algorithm 1 iterates as its successive limiting states and that its final limit has the modified-l1 implicit bias.
7. Explain the dynamics through SIM: features first move along data-independent curves, signs become effectively locked, and feature selection alternates with constrained joint learning.
8. Illustrate the result with a four-feature general two-layer model, a 2x4 design matrix, `y=(1,0)`, initialization scale `1e-60`, learning rate `0.1`, and 200-decimal-place `mpmath` calculations.

The pinned source archive contains the paper and figures but no official experiment repository or training implementation. The local toy is therefore a clean, source-faithful translation of the printed Algorithm 1 fixture—not a claim that the original gradient-flow experiment has been reproduced.

## Repository status

| Area | Current state |
| --- | --- |
| Compute | Local CPU / local GTX 1050 only |
| Primary source | Verified arXiv `2607.12332`; SHA-256 pinned |
| Claim 1 | Algorithm 1 appendix fixture reproduced as an exact-arithmetic toy; theorem and gradient flow unverified |
| Claim 2 | Unverified locally; objective and source corollary documented |
| Continuous-time gradient flow | Not independently run |
| Infinitesimal initialization limit | Not independently established |
| Official paper code | No code link found in the pinned source archive |
| Publication of theorem-level results | Not allowed without a source-faithful gradient-flow protocol and independently checked metrics |

## Contents

| Path | Purpose |
| --- | --- |
| `contract/live_claims.json` | Paper metadata and the two contracted claims |
| `evidence/source/` | Canonical paper PDF/source archive, legacy mismatch artifacts, and checksums |
| `outputs/claim1_source_recovery/` | Historical mismatch and verified-source recovery record |
| `src/claim1_algorithm1_toy.py` | Exact-fraction implementation of the appendix Algorithm 1 fixture |
| `outputs/claim1_algorithm1_toy/trace.json` | Inputs, every iteration, selected features, residuals, and paper comparison |
| `outputs/claim1_algorithm1_toy/SHA256SUMS` | Output integrity checksum |
| `tests/` | Small contract and source-recovery checks |
| `STATUS.md` | Human-readable phase and next action |
| `AUTONOMOUS_STATE.json` | Machine-readable evidence boundary and run state |

## Branch inventory

| Branch | Role | State |
| --- | --- | --- |
| `main` | Published source-pinned audit, documentation, and bounded local evidence | Current default branch |

Only `main` is present. No experiment, legacy, or claim-specific branch currently carries separate work. Historical source mismatch artifacts are explicit files, not hidden branches.

## Claim-to-evidence ledger

The authoritative claim text is preserved in `contract/live_claims.json`. The table below explains how each claim is produced in the paper and what this repository currently demonstrates.

| Claim | How the paper produces it | Evidence in this repository | Status |
| --- | --- | --- | --- |
| 1. The gradient-flow algorithm converges to a modified l1 minimization solution. | Prove the Algorithm 1 termination/optimization theorem, then prove that infinitesimal-initialization gradient-flow trajectories approach its successive states and final constrained solution. | `src/claim1_algorithm1_toy.py` executes the appendix’s `X`, `y`, `t+`, and `t-` fixture with exact fractions. It records feature order `[1, 3, 4]`, final `k=(0,0,10/7,-10/49)`, and zero residual. It does not integrate gradient flow or check the theorem assumptions. | **Toy only / unverified theorem** |
| 2. The implicit bias of diagonal linear networks under infinitesimal initialization is modified l1. | Combine the dynamics theorem with the Algorithm 1 optimization theorem and the objective `R(k)=sum_i(t_i+ k_i+ + t_i- k_i-)`; for standard symmetric growth times this reduces to l1. | The objective, assumptions, theorem statements, and corollary are pinned in the source archive and summarized above. No independent proof audit or neural-parameter gradient-flow run is present. | **Unverified** |

### Appendix arithmetic discrepancy

At the paper’s `p=3` appendix iteration, the printed text gives `delta_1=20`. Using the paper’s own displayed update, `s_1=1`, `t_1-=1`, and `u_1=-0.05`, the value is `(1+1)/0.05 = 40`. The active feature 4 still has the smallest time (`80/49`), so this discrepancy does not change the selected sequence or final vector. The trace records both values rather than silently correcting the source.

### Toy evidence boundary

The local program validates the finite recursion and the printed least-squares fixture using rational arithmetic. It does not reproduce the paper’s parameterized functions `k_i(theta_i)`, 200-decimal `mpmath` gradient descent, continuous-time gradient flow, saddle-to-saddle timing, SIM invariance, or the `s -> 0` iterated limit. The final vector is therefore evidence for the bounded Algorithm 1 fixture only.

## Final verification

Run python3 verify_final.py from the repository root. The verifier checks the canonical repository URL, the single main branch, MachineLearning-Nerd attribution on reachable commits, paper and source hashes, the toy trace, claim-status alignment, and the tracked evidence manifest.

## Reproduce the current local evidence

From the repository root:

~~~bash
python3 src/claim1_algorithm1_toy.py
python3 src/claim1_audit.py
python3 -m pytest -q tests/test_contract.py tests/test_source_recovery.py
sha256sum -c evidence/source/SHA256SUMS
sha256sum -c outputs/claim1_algorithm1_toy/SHA256SUMS
~~~

The toy has no third-party dependency. If `pytest` is unavailable, the script and the two contract checks can still be run directly with Python.

## Reproduction policy

- A paper theorem or appendix statement is not automatically an independently reproduced result.
- A **toy** is evidence only for its finite inputs, implementation boundary, and recorded arithmetic.
- A claim becomes **reproduced** only when the required model, initialization regime, optimizer/dynamics, data, logs, and metric calculation are available and independently checked.
- Resource limits are part of the record: this audit uses local CPU/local GTX 1050 compute and does not use paid, remote, or upgraded cloud compute.
- The source checksums and explicit legacy filenames preserve the distinction between the original bad pin and the verified canonical source.

## Citation

~~~bibtex
@misc{zhao2026gradient,
  title         = {Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization},
  author        = {Jiajie Zhao and Jianxing Wang and Junjie Yang and Zhiwei Bai and Yaoyu Zhang},
  year          = {2026},
  eprint        = {2607.12332},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2607.12332}
}
~~~

## Thank you

Thank you to Jiajie Zhao, Jianxing Wang, Junjie Yang, Zhiwei Bai, and Yaoyu Zhang for the theoretical development, explicit Algorithm 1 fixture, and detailed discussion of diagonal-network dynamics and SIM. This audit is intended to credit the original work while making the boundary between paper claims, paper-linked artifacts, bounded local checks, and true end-to-end reproduction explicit.
