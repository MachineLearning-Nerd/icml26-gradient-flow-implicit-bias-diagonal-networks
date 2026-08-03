"""Source-audit marker: full diagonal gradient-flow fixture is the next milestone."""
import json
from pathlib import Path
contract=json.loads(Path("contract/live_claims.json").read_text())
assert contract["orid"] == "IJph1t3Egr"
assert contract["claim_count"] > 0
print("source-audit contract OK")
