# Scoped reproduction report

Date: 2026-08-17

## Result

This repository is a published, source-pinned audit of the ICML 2026 paper “Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization.” Its overall verdict is:

INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY

The source identity is resolved and the finite Algorithm 1 appendix fixture is checked with exact rational arithmetic. The theorem-level gradient-flow and implicit-bias claims remain unverified.

## Claim matrix

| Claim | Local result | Evidence boundary |
| --- | --- | --- |
| C1: gradient-flow algorithm converges to a modified-l1 solution | TOY_SOURCE_ALGORITHM1 | Algorithm 1 fixture only; no continuous-time dynamics, infinitesimal limit, or theorem audit |
| C2: diagonal-network implicit bias is modified l1 | UNVERIFIED | Source theorem and corollary documented; no independent proof or parameterized gradient-flow run |

## Recovered source

The canonical source is arXiv 2607.12332. The previous 2602.11401 pin was unrelated and remains explicitly named as legacy evidence. The PDF, source archive, source member hashes, and recovery path are documented in SOURCE_AUDIT.md; that file and CLAIM_EVIDENCE.md identify the exact paper anchors used.

## Bounded local result

The four-feature fixture selects features 1, 3, and 4 and reaches:

~~~text
k = (0, 0, 10/7, -10/49)
X k = y
||X k - y||² = 0
~~~

The audit records the paper’s p=3 printed delta_1=20 and the displayed-formula value delta_1=40. The discrepancy does not change the selected feature, final vector, or zero-residual result.

## Limitations and handoff

- The source archive contains no official experiment repository or training implementation.
- The paper’s practical figure uses gradient descent, while the main theorem concerns continuous-time gradient flow.
- The repository does not establish the s-to-zero iterated limit or the theorem assumptions.
- The next audit should begin with a different ICML repository; this repository’s next action is recorded in AUTONOMOUS_STATE.json.
