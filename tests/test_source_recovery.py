from pathlib import Path

def test_mismatched_pin_is_recorded_and_not_used_as_method_source():
    text = Path('outputs/claim1_source_recovery/RECOVERY.md').read_text()
    assert 'not** the contracted OpenReview paper' in text
    assert 'Claim 1 remains inconclusive' in text
