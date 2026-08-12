from pathlib import Path

def test_mismatched_pin_is_recorded_and_verified_source_is_used():
    text = Path('outputs/claim1_source_recovery/RECOVERY.md').read_text()
    assert 'not** the contracted OpenReview paper' in text
    assert 'arXiv:2607.12332' in text
    assert 'verified primary method' in text
    assert 'unverified beyond the bounded toy' in text
