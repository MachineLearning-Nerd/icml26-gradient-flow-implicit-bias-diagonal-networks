# Claim-to-evidence audit

This dossier separates what the paper states and proves from what this repository checks locally. The contracted claim text is preserved in contract/live_claims.json.

## Paper production path

The paper’s argument has four layers:

1. Define a diagonal model and squared-error loss.
2. Analyze continuous-time gradient flow from an infinitesimal initialization scale.
3. Use growth times, residual correlations, sign locking, and the Structural Invariant Manifold (SIM) to derive Algorithm 1’s successive feature-selection and constrained-learning states.
4. Combine the Algorithm 1 optimization theorem with the dynamics theorem to identify the modified l1 implicit bias.

The four-feature experiment uses gradient descent as a practical approximation, not continuous-time gradient flow. The paper explicitly distinguishes those dynamics.

## C1 — Algorithm and modified-l1 solution

Contract text: “The gradient flow algorithm converges to the solution of a modified ℓ1 norm minimization problem.”

Paper production path:

- The diagonal model and loss are defined in camera_ready.tex lines 235–246.
- Algorithm 1 computes residual correlation, growth-time deltas, the next inactive feature, and a sign-constrained least-squares update in lines 328–379.
- The convergence and well-posedness theorem assumes a feasible linear system, unique delta minimizers, and nonzero correlations at boundary cases. It states finite termination and the weighted positive/negative-part objective in lines 397–414.
- The dynamics theorem later connects gradient-flow trajectories to the Algorithm 1 states in lines 537–556.

Local evidence:

- src/claim1_algorithm1_toy.py translates the appendix fixture into exact Fraction arithmetic.
- outputs/claim1_algorithm1_toy/trace.json records every update, selected features [1, 3, 4], final k [0, 0, 10/7, -10/49], and zero squared residual.
- outputs/claim1_algorithm1_toy/SHA256SUMS and evidence/source/SHA256SUMS pin the generated and source artifacts.
- outputs/claim1_source_recovery/RECOVERY.md records how the verified arXiv source was recovered after the unrelated 2602.11401 pin was found.

Status: TOY_SOURCE_ALGORITHM1.

This is evidence for the finite source fixture and its arithmetic only. It does not establish the full contracted claim because this repository does not integrate the paper’s parameterized continuous-time gradient flow, test the infinitesimal limit, or re-prove the theorem assumptions. The paper’s printed p=3 delta_1=20 is also recorded alongside the formula-derived value 40; the selected feature and final vector are unchanged.

## C2 — Implicit bias

Contract text: “The implicit bias of diagonal linear networks under infinitesimal initialization corresponds to modified ℓ1 norm.”

Paper production path:

- The dynamics theorem in camera_ready.tex lines 537–556 states that gradient-flow trajectories from scaled initialization have the Algorithm 1 successive limiting states and a final iterated limit.
- The corollary in lines 573–579 identifies the implicit-bias objective as R(k) = sum_i (t_i+ k_i+ + t_i- k_i-).
- The corollary proof in lines 581–583 explicitly depends on the Algorithm 1 theorem and the dynamics theorem.
- The SIM definitions and diagonal-network theorem in lines 784–844 support the sign-locking and orbit structure used by the intuition and dynamics argument.

Local evidence:

- The canonical PDF and source archive are hash-pinned.
- The objective, assumptions, theorem statements, and corollary are transcribed in this dossier and README.
- No independent proof audit, parameterized neural-network implementation, continuous-time integration, or s-to-zero convergence study is present.

Status: UNVERIFIED.

The source archive includes figures and the paper source but no official experiment repository or training implementation. The paper’s high-precision gradient-descent experiment is therefore not silently represented as reproduced here.

## Evidence vocabulary

- TOY_SOURCE_ALGORITHM1 means a bounded finite fixture was executed and checked.
- UNVERIFIED means the source claim is documented but the required independent evidence is absent.
- REPRODUCED is intentionally not used for either contracted claim in this repository.
