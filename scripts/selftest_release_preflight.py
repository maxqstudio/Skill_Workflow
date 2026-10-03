#!/usr/bin/env python3
"""Regression tests for exact-head release preflight."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from release_preflight import validate


def run(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def commit_all(root: Path, message: str) -> str:
    run(root, "add", ".")
    run(root, "commit", "-m", message)
    return run(root, "rev-parse", "HEAD")


def governance_report(path: Path, head: str, *, mode: str, result: str = "PASS") -> None:
    assert mode in {"verify", "finalize"}
    write_json(
        path,
        {
            "schema_version": 2,
            "result": result,
            "expected_head": head,
            "effective_mode": mode,
            "final_acceptance_authority": bool(mode == "finalize" and result == "PASS"),
        },
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / "repo"
        root.mkdir()
        run(root, "init")
        run(root, "config", "user.email", "fixture@example.invalid")
        run(root, "config", "user.name", "Fixture")

        acceptance_path = root / ".workflow" / "acceptance.json"
        roadmap_path = root / ".workflow" / "roadmap.json"
        acceptance = {
            "schema_version": 1,
            "requirements": [
                {"id": "R1", "status": "PASS"},
                {"id": "R4", "status": "NOT_PROVEN"},
            ],
            "truth_gates": {
                "SOURCE_TESTS": "PASS",
                "RELEASE_EVIDENCE": "NOT_PROVEN",
                "RUNTIME_E2E": "NOT_APPLICABLE",
            },
        }
        write_json(acceptance_path, acceptance)
        write_json(
            roadmap_path,
            {
                "schema_version": 1,
                "current_phase": "SW2-07",
                "phases": [
                    {"id": "SW2-07", "status": "CURRENT"},
                    {"id": "SW2-08", "status": "PLANNED"},
                    {"id": "SW2-09", "status": "PLANNED"},
                ],
            },
        )
        (root / "README.md").write_text("fixture\n", encoding="utf-8", newline="\n")
        head = commit_all(root, "fixture evidence candidate")
        report_path = Path(temp) / "governance.json"
        governance_report(report_path, head, mode="verify")

        evidence = validate(
            root,
            expected_head=head,
            version="v2.0.0-rc.1",
            governance_report=report_path,
            evidence_only=True,
        )
        assert evidence["result"] == "PASS"
        assert evidence["publication_authority"] is False
        assert evidence["evidence_only"] is True

        strict_incomplete = validate(
            root,
            expected_head=head,
            version="v2.0.0-rc.1",
            governance_report=report_path,
        )
        assert strict_incomplete["result"] == "FAIL"
        assert "RELEASE_REQUIREMENT_NOT_PASS:R4" in strict_incomplete["failures"]
        assert strict_incomplete["publication_authority"] is False

        evidence_stable = validate(
            root,
            expected_head=head,
            version="v2.0.0",
            governance_report=report_path,
            evidence_only=True,
        )
        assert evidence_stable["result"] == "FAIL"
        assert "EVIDENCE_MODE_REQUIRES_PRERELEASE" in evidence_stable["failures"]
        assert evidence_stable["publication_authority"] is False

        acceptance["requirements"][1]["status"] = "FAIL"
        write_json(acceptance_path, acceptance)
        failed_head = commit_all(root, "fixture explicit failure")
        governance_report(report_path, failed_head, mode="verify")
        evidence_failure = validate(
            root,
            expected_head=failed_head,
            version="v2.0.0-rc.2",
            governance_report=report_path,
            evidence_only=True,
        )
        assert evidence_failure["result"] == "FAIL"
        assert "EVIDENCE_REQUIREMENT_FAIL:R4" in evidence_failure["failures"]
        assert evidence_failure["publication_authority"] is False

        acceptance["requirements"][1]["status"] = "PASS"
        acceptance["truth_gates"]["RELEASE_EVIDENCE"] = "PASS"
        write_json(acceptance_path, acceptance)
        strict_head = commit_all(root, "fixture strict prerelease")
        governance_report(report_path, strict_head, mode="finalize")

        prerelease = validate(
            root,
            expected_head=strict_head,
            version="v2.0.0-rc.3",
            governance_report=report_path,
        )
        assert prerelease["result"] == "PASS"
        assert prerelease["publication_authority"] is True
        assert prerelease["evidence_only"] is False

        stable_too_early = validate(
            root,
            expected_head=strict_head,
            version="v2.0.0",
            governance_report=report_path,
        )
        assert stable_too_early["result"] == "FAIL"
        assert "STABLE_RELEASE_OUTSIDE_SW2_09" in stable_too_early["failures"]
        assert stable_too_early["publication_authority"] is False

        write_json(
            roadmap_path,
            {
                "schema_version": 1,
                "current_phase": "SW2-09",
                "phases": [
                    {"id": "SW2-07", "status": "COMPLETE"},
                    {"id": "SW2-08", "status": "COMPLETE"},
                    {"id": "SW2-09", "status": "CURRENT"},
                ],
            },
        )
        stable_head = commit_all(root, "fixture stable")
        governance_report(report_path, stable_head, mode="finalize")
        stable = validate(
            root,
            expected_head=stable_head,
            version="v2.0.0",
            governance_report=report_path,
        )
        assert stable["result"] == "PASS"
        assert stable["publication_authority"] is True

        (root / "DIRTY.txt").write_text("dirty\n", encoding="utf-8", newline="\n")
        dirty = validate(
            root,
            expected_head=stable_head,
            version="v2.0.0",
            governance_report=report_path,
        )
        assert dirty["result"] == "FAIL"
        assert "RELEASE_WORKTREE_NOT_CLEAN" in dirty["failures"]
        assert dirty["publication_authority"] is False
        (root / "DIRTY.txt").unlink()

        governance_report(report_path, stable_head, mode="finalize", result="FAIL")
        failed_finalize = validate(
            root,
            expected_head=stable_head,
            version="v2.0.0",
            governance_report=report_path,
        )
        assert failed_finalize["result"] == "FAIL"
        assert "FINALIZE_REPORT_NOT_PASS" in failed_finalize["failures"]
        assert failed_finalize["publication_authority"] is False

    print("EVIDENCE_ONLY_PRERELEASE=PASS")
    print("EVIDENCE_ONLY_NO_PUBLICATION_AUTHORITY=PASS")
    print("EVIDENCE_ONLY_STABLE_REJECTION=PASS")
    print("EVIDENCE_ONLY_EXPLICIT_FAILURE_REJECTION=PASS")
    print("STRICT_INCOMPLETE_REJECTION=PASS")
    print("STRICT_PRERELEASE_PREFLIGHT=PASS")
    print("STABLE_PHASE_BOUNDARY_REJECTION=PASS")
    print("STABLE_SW2_09_PREFLIGHT=PASS")
    print("DIRTY_WORKTREE_REJECTION=PASS")
    print("FAILED_FINALIZE_REJECTION=PASS")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
