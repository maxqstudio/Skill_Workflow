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


def governance_report(path: Path, head: str, result: str = "PASS") -> None:
    write_json(
        path,
        {
            "schema_version": 2,
            "result": result,
            "expected_head": head,
            "effective_mode": "finalize",
            "final_acceptance_authority": result == "PASS",
        },
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / "repo"
        root.mkdir()
        run(root, "init")
        run(root, "config", "user.email", "fixture@example.invalid")
        run(root, "config", "user.name", "Fixture")

        write_json(
            root / ".workflow" / "acceptance.json",
            {
                "schema_version": 1,
                "requirements": [{"id": "R1", "status": "PASS"}],
                "truth_gates": {"SOURCE_TESTS": "PASS", "RUNTIME_E2E": "NOT_APPLICABLE"},
            },
        )
        write_json(
            root / ".workflow" / "roadmap.json",
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
        head = commit_all(root, "fixture prerelease")
        report_path = Path(temp) / "finalize.json"
        governance_report(report_path, head)

        prerelease = validate(root, expected_head=head, version="v2.0.0-rc.1", governance_report=report_path)
        assert prerelease["result"] == "PASS"

        stable_too_early = validate(root, expected_head=head, version="v2.0.0", governance_report=report_path)
        assert stable_too_early["result"] == "FAIL"
        assert "STABLE_RELEASE_OUTSIDE_SW2_09" in stable_too_early["failures"]

        write_json(
            root / ".workflow" / "roadmap.json",
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
        head = commit_all(root, "fixture stable")
        governance_report(report_path, head)
        stable = validate(root, expected_head=head, version="v2.0.0", governance_report=report_path)
        assert stable["result"] == "PASS"

        (root / "DIRTY.txt").write_text("dirty\n", encoding="utf-8", newline="\n")
        assert validate(root, expected_head=head, version="v2.0.0", governance_report=report_path)["result"] == "FAIL"
        (root / "DIRTY.txt").unlink()

        governance_report(report_path, head, result="FAIL")
        assert validate(root, expected_head=head, version="v2.0.0", governance_report=report_path)["result"] == "FAIL"

    print("PRERELEASE_PREFLIGHT=PASS")
    print("STABLE_PHASE_BOUNDARY_REJECTION=PASS")
    print("STABLE_SW2_09_PREFLIGHT=PASS")
    print("DIRTY_WORKTREE_REJECTION=PASS")
    print("FAILED_FINALIZE_REJECTION=PASS")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
