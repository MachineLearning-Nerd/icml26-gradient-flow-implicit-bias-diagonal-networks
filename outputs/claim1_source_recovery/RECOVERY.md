# Claim 1 source recovery checkpoint

The workspace's original arXiv pin (`2602.11401`) was **not** the contracted OpenReview paper. Its title is *Latent Forcing: Reordering the Diffusion Trajectory for Pixel-Space Image Generation*, and its archive contains no diagonal-linear-network or gradient-flow content. Those artifacts are retained under the explicit `legacy-2602.11401-unrelated.*` names and are not used as evidence.

A direct OpenReview recovery was attempted on 2026-08-03:

* `https://openreview.net/pdf?id=IJph1t3Egr` returned HTTP 403 ChallengeRequiredError (HTML, not a PDF).
* `https://api.openreview.net/notes?id=IJph1t3Egr` returned HTTP 403 ChallengeRequiredError.

Primary-source recovery is now resolved through the exact-title arXiv record:

* Paper: [arXiv:2607.12332](https://arxiv.org/abs/2607.12332)
* Title: *Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization*
* Authors: Jiajie Zhao, Jianxing Wang, Junjie Yang, Zhiwei Bai, and Yaoyu Zhang
* Canonical local artifacts: `evidence/source/arxiv.pdf` and `evidence/source/arxiv_source.tar.gz`

The recovered source contains the model definition, Algorithm 1, the modified-l1 objective, theorem statements, and the four-feature appendix fixture. The bounded implementation in `src/claim1_algorithm1_toy.py` therefore uses a verified primary method. It validates the appendix recursion and arithmetic only; it does not prove or reproduce continuous-time gradient flow or the infinitesimal limit. Claim 1 remains **unverified beyond the bounded toy**.
