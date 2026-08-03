import json
from pathlib import Path
d=json.loads((Path(__file__).parents[1]/"contract/live_claims.json").read_text())
assert d["orid"] == "IJph1t3Egr" and d["claim_count"] > 0
