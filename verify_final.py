#!/usr/bin/env python3
"""Verify the published, source-pinned scoped audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = "https://github.com/MachineLearning-Nerd/icml26-gradient-flow-implicit-bias-diagonal-networks"
EXPECTED_EMAILS = {
    "MachineLearning-Nerd@users.noreply.github.com",
    "37579156+MachineLearning-Nerd@users.noreply.github.com",
}
REQUIRED_FILES = {
    ".gitignore",
    "README.md",
    "STATUS.md",
    "AUTONOMOUS_STATE.json",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "BRANCH_AUDIT.md",
    "branch-audit.md",
    "claims.json",
    "contract/live_claims.json",
    "EVIDENCE_MANIFEST.json",
    "evidence/source/SHA256SUMS",
    "evidence/source/arxiv.pdf",
    "evidence/source/arxiv_source.tar.gz",
    "evidence/source/legacy-2602.11401-unrelated.pdf",
    "evidence/source/legacy-2602.11401-unrelated.tar.gz",
    "outputs/claim1_algorithm1_toy/README.md",
    "outputs/claim1_algorithm1_toy/SHA256SUMS",
    "outputs/claim1_algorithm1_toy/trace.json",
    "outputs/claim1_source_recovery/RECOVERY.md",
    "outputs/claim1_source_recovery/SHA256SUMS",
    "src/claim1_algorithm1_toy.py",
    "src/claim1_audit.py",
    "tests/test_contract.py",
    "tests/test_source_recovery.py",
    "verify_final.py",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def fail(message: str) -> None:
    raise SystemExit(f"FINAL_AUDIT=FAILED {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_sha(path: Path, expected: str) -> None:
    if not path.is_file():
        fail(f"missing={path.relative_to(ROOT)}")
    actual = sha256(path)
    if actual != expected:
        fail(f"sha256={path.relative_to(ROOT)}:{actual}")


def check_checksum_file(path: Path) -> None:
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        relative = relative.strip()
        candidate = ROOT / relative
        if not candidate.is_file():
            candidate = ROOT / path.parent.relative_to(ROOT) / relative
        check_sha(candidate, expected)


def check_git_state() -> list[str]:
    if run("git", "branch", "--show-current") != "main":
        fail("current_branch")
    if run("git", "remote", "get-url", "origin").removesuffix(".git") != EXPECTED_REPOSITORY:
        fail("origin_url")
    local_branches = run("git", "for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines()
    if local_branches != ["main"]:
        fail(f"local_branches={local_branches}")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs").splitlines()
    if any(ref.startswith("refs/original/") or "backup" in ref for ref in refs):
        fail("stale_refs")
    commits = run("git", "rev-list", "main").splitlines()
    if len(commits) < 3:
        fail(f"reachable_commits={len(commits)}")
    for commit in commits:
        fields = run("git", "show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce%x00%B", commit).split("\x00", 4)
        author_name, author_email, committer_name, committer_email, body = fields
        if author_name != "MachineLearning-Nerd" or committer_name != "MachineLearning-Nerd":
            fail(f"attribution={commit}")
        if author_email not in EXPECTED_EMAILS or committer_email not in EXPECTED_EMAILS:
            fail(f"email={commit}")
        if "co-authored-by:" in body.lower():
            fail(f"coauthor={commit}")
    return commits


def check_json() -> tuple[dict, dict, dict]:
    state = json.loads((ROOT / "AUTONOMOUS_STATE.json").read_text())
    claims = json.loads((ROOT / "claims.json").read_text())
    contract = json.loads((ROOT / "contract/live_claims.json").read_text())
    if state["phase"] != "published_and_verified":
        fail("state_phase")
    if state["github_repository"] != EXPECTED_REPOSITORY:
        fail("state_repository")
    if state["branch_set"] != ["main"]:
        fail("state_branches")
    if state["overall_verdict"] != "INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY":
        fail("state_verdict")
    if state["claim_statuses"] != {"C1": "TOY_SOURCE_ALGORITHM1", "C2": "UNVERIFIED"}:
        fail("state_claims")
    if claims["repository"]["url"] != EXPECTED_REPOSITORY:
        fail("claims_repository")
    if claims["overall_verdict"] != state["overall_verdict"] or claims["publication_allowed"]:
        fail("claims_verdict")
    if contract["orid"] != "IJph1t3Egr" or contract["arxiv"] != "2607.12332":
        fail("contract_source")
    if contract["claim_count"] != 2 or len(claims["claims"]) != 2:
        fail("claim_count")
    return state, claims, contract


def check_source() -> None:
    check_checksum_file(ROOT / "evidence/source/SHA256SUMS")
    check_checksum_file(ROOT / "outputs/claim1_algorithm1_toy/SHA256SUMS")
    check_checksum_file(ROOT / "outputs/claim1_source_recovery/SHA256SUMS")
    archive = ROOT / "evidence/source/arxiv_source.tar.gz"
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        regular = [member for member in members if member.isfile()]
        directories = [member for member in members if member.isdir()]
        executable = [member for member in regular if member.mode & 0o111]
    if len(members) != 15 or len(regular) != 14 or len(directories) != 1 or executable:
        fail("source_archive_inventory")
    recovery = (ROOT / "outputs/claim1_source_recovery/RECOVERY.md").read_text()
    if "2602.11401" not in recovery or "unrelated" not in recovery or "2607.12332" not in recovery:
        fail("source_recovery_record")


def check_toy() -> None:
    trace = json.loads((ROOT / "outputs/claim1_algorithm1_toy/trace.json").read_text())
    if trace["paper_fixture"]["arxiv"] != "2607.12332":
        fail("toy_source")
    if [item["selected_feature"] for item in trace["iterations"]] != [1, 3, 4]:
        fail("toy_selection")
    if trace["final_k"]["fraction"] != ["0", "0", "10/7", "-10/49"]:
        fail("toy_final")
    if trace["final_squared_residual"] != "0":
        fail("toy_residual")
    comparison = trace["paper_comparison"]
    if comparison["printed_delta_feature_1_at_p_3"] != "20" or comparison["algorithm_delta_feature_1_at_p_3"] != "40":
        fail("toy_discrepancy")


def check_manifest() -> None:
    manifest = json.loads((ROOT / "EVIDENCE_MANIFEST.json").read_text())
    tracked = set(run("git", "ls-files").splitlines())
    excluded = {"AUTONOMOUS_STATE.json", "EVIDENCE_MANIFEST.json"}
    expected = sorted(tracked - excluded)
    entries = manifest.get("entries", [])
    actual = sorted(entry["path"] for entry in entries)
    if actual != expected:
        fail("manifest_paths")
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            fail(f"manifest_missing={entry['path']}")
        if entry["bytes"] != path.stat().st_size or entry["sha256"] != sha256(path):
            fail(f"manifest_hash={entry['path']}")


def main() -> None:
    check_git_state()
    check_json()
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(f"required={relative}")
    check_source()
    check_toy()
    check_manifest()
    print("FINAL_AUDIT=VERIFIED branches=1 claims=C1:toy_source_algorithm1,C2:unverified publication_allowed=false")


if __name__ == "__main__":
    main()
