#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tmp_sw2_22_open_red as phase

ROOT = Path(__file__).resolve().parent.parent
PREVIOUS_SESSION = "docs/sequence/sessions/SW2-21-GOVERNANCE.json"
CURRENT_SESSION = "docs/sequence/sessions/SW2-22-GOVERNANCE.json"


def commit_anchor() -> str:
    subprocess.run(
        ["git", "add", ".workflow", "docs", "artifacts/sequence", "scripts/selftest_toolchain_provenance_upgrade.py"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "SW2-22: establish historical freeze anchor"],
        cwd=ROOT,
        check=True,
    )
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def generate_current_sequence() -> None:
    phase.run(sys.executable, "scripts/sync_project_truth.py", "--root", ".")
    phase.run(
        sys.executable,
        "scripts/generate_sequence_actual.py",
        "--root", ".",
        "--output-json", "docs/sequence/generated/SW2-22-GOVERNANCE.actual.json",
        "--output-mermaid", "docs/sequence/generated/SW2-22-GOVERNANCE.actual.mmd",
        "--entry", "scripts/toolchain_identity.py::producer_metadata",
        "--entry", "scripts/toolchain_identity.py::write_toolchain_lock",
        "--entry", "scripts/toolchain_identity.py::validate_toolchain_lock",
        "--entry", "scripts/initialize_project_truth.py::main",
        "--entry", "scripts/migrate_governance_v1.py::main",
        "--entry", "scripts/validate_schema_toolchain.py::main",
    )
    phase.run(
        sys.executable,
        "scripts/sequence_human_view.py",
        "--root", ".",
        "--actual-json", "docs/sequence/generated/SW2-22-GOVERNANCE.actual.json",
        "--actual-mermaid", "docs/sequence/generated/SW2-22-GOVERNANCE.actual.mmd",
        "--output-json", "docs/sequence/generated/SW2-22-GOVERNANCE.human.json",
        "--output-mermaid", "docs/sequence/generated/SW2-22-GOVERNANCE.human.mmd",
        "--output-markdown", "docs/sequence/views/SW2-22-GOVERNANCE.md",
        "--session-id", "SW2-22-GOVERNANCE",
    )
    session = phase.load(CURRENT_SESSION)
    actual = phase.load(session["actual"]["graph"])
    session["actual"]["source_digest"] = actual["source_digest"]
    session["human_view"]["source_digest"] = actual["source_digest"]
    phase.write(CURRENT_SESSION, session)
    phase.run(
        sys.executable,
        "scripts/validate_sequence_contract.py",
        "--root", ".",
        "--session", CURRENT_SESSION,
        "--report", "artifacts/sequence/SW2-22-GOVERNANCE.acceptance.json",
    )
    phase.run(
        sys.executable,
        "scripts/validate_sequence_human_view.py",
        "--root", ".",
        "--session", CURRENT_SESSION,
    )


def main() -> int:
    phase.open_authority()

    previous = phase.load(PREVIOUS_SESSION)
    if previous.get("scope") != "CURRENT" or previous.get("status") != "COMPLETE":
        raise RuntimeError("SW2_21_SESSION_NOT_ACCEPTED_CURRENT")
    previous["scope"] = "HISTORICAL"
    phase.write(PREVIOUS_SESSION, previous)

    phase.install_red_test()
    generate_current_sequence()

    anchor = commit_anchor()
    print("HISTORICAL_FREEZE_ANCHOR=" + anchor)

    phase.run(
        sys.executable,
        "scripts/validate_sequence_sessions.py",
        "--root", ".",
        "--freeze-historical",
        "--authorize-migration", "SW2-22 phase-open freezes accepted SW2-21 evidence",
        "--frozen-commit", anchor,
    )
    phase.run(sys.executable, "scripts/validate_sequence_sessions.py", "--root", ".")

    acceptance = phase.load(".workflow/acceptance.json")
    acceptance["sequence_sync_status"] = "PASS"
    acceptance.setdefault("truth_gates", {})["SEQUENCE_SYNC"] = "PASS"
    phase.write(".workflow/acceptance.json", acceptance)
    phase.run(sys.executable, "scripts/sync_project_truth.py", "--root", ".")

    phase.prove_red()
    print("SW2_22_PHASE_OPEN=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
