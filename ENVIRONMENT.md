# Environment and reproduction policy

## Local policy

- Allowed compute: local CPU and local GTX 1050.
- Disallowed for this audit: paid compute, remote compute, upgraded Hugging Face CPU, Hugging Face Jobs, and other external execution.
- The bounded toy uses only the Python standard library.
- The paper’s figure reports 200-decimal-place mpmath calculations, but this repository does not claim to have reproduced that gradient-descent run.

## Lightweight checks

From the repository root:

~~~bash
python3 verify_final.py
python3 src/claim1_algorithm1_toy.py
python3 src/claim1_audit.py
python3 -m pytest -q tests/test_contract.py tests/test_source_recovery.py
sha256sum -c evidence/source/SHA256SUMS
sha256sum -c outputs/claim1_algorithm1_toy/SHA256SUMS
~~~

The final verifier is the publication gate for this scoped audit. Passing it means the recorded evidence is internally consistent; it does not upgrade a toy or source transcription into an end-to-end reproduction.
