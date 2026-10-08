#!/usr/bin/env python3
"""Validate the SW2-18 unified permanent CI contract."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from validate_ci_parallel_contract import findings as ci_parallel_findings
from validate_release_bundle_ci import findings as bundle_findings

FIXED_CONTEXTS = (
    "Self Governance (ubuntu-latest)",
    "SW2 Sequence Evidence (ubuntu-latest)",
    "Governance Engine Performance (ubuntu-latest)",
    "Consumer Engine Performance (max-grounding)",
)
MATRIX_CONTEXT_TEMPLATE = "Governance Selftest (${{ matrix.os }})"
OLD_ROUTINE_WORKFLOWS = (
    "governance-selftest.yml",
    "self-governance.yml",
    "sw2-baseline.yml",
    "sw2-consumer-baseline.yml",
    "sw2-sequence.yml",
)
PERFORMANCE_BUDGET = "benchmarks/baselines/sw2-19-v2.1-mode-budget.json"


def run_performance_budget_contract(root: Path) -> list[str]:
    budget = root / PERFORMANCE_BUDGET
    if not budget.is_file():
        return []

    failures: list[str] = []
    commands = (
        ("PERFORMANCE_BUDGET_SELFTEST", [sys.executable, "scripts/selftest_performance_budget.py"]),
        (
            "PERFORMANCE_BUDGET_VALIDATION",
            [sys.executable, "scripts/validate_performance_budget.py", "--root", "."],
        ),
    )
    for label, command in commands:
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.stdout:
            print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
        if completed.returncode != 0:
            failures.append(f"{label}_FAILED")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    workflow = root / ".github" / "workflows" / "governance-ci.yml"
    failures: list[str] = []

    if not workflow.is_file():
        failures.append("UNIFIED_WORKFLOW_MISSING")
        text = ""
    else:
        text = workflow.read_text(encoding="utf-8")

    for context in FIXED_CONTEXTS:
        if text.count(f"name: {context}") != 1:
            failures.append(f"CHECK_CONTEXT_MISSING_OR_DUPLICATE:{context}")

    if text.count(f"name: {MATRIX_CONTEXT_TEMPLATE}") != 1:
        failures.append("GOVERNANCE_SELFTEST_MATRIX_CONTEXT_MISSING_OR_DUPLICATE")
    if text.count("- ubuntu-latest") < 1 or text.count("- windows-latest") < 1:
        failures.append("GOVERNANCE_SELFTEST_OS_MATRIX_INCOMPLETE")

    if text.count("./.github/actions/governance-bootstrap") < 5:
        failures.append("BOOTSTRAP_NOT_CENTRALIZED")
    if "steps.bootstrap.outputs.heavy" not in text:
        failures.append("APPLICABILITY_NOT_DECLARED")

    workflows = root / ".github" / "workflows"
    for filename in OLD_ROUTINE_WORKFLOWS:
        if (workflows / filename).exists():
            failures.append(f"LEGACY_ROUTINE_WORKFLOW_PRESENT:{filename}")

    for filename in ("release-preflight.yml", "ruleset-audit.yml"):
        if not (workflows / filename).is_file():
            failures.append(f"SPECIAL_WORKFLOW_MISSING:{filename}")

    bootstrap = root / ".github" / "actions" / "governance-bootstrap" / "action.yml"
    if not bootstrap.is_file():
        failures.append("BOOTSTRAP_ACTION_MISSING")

    classifier = root / ".github" / "scripts" / "ci_applicability.py"
    if not classifier.is_file():
        failures.append("APPLICABILITY_CLASSIFIER_MISSING")

    failures.extend(ci_parallel_findings(text))
    bundle_workflow = workflows / "release-bundle-dry-run.yml"
    if not bundle_workflow.is_file():
        failures.append("BUNDLE_MANUAL_WORKFLOW_MISSING")
    else:
        failures.extend(bundle_findings(text, bundle_workflow.read_text(encoding="utf-8")))
    failures.extend(run_performance_budget_contract(root))

    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    print("UNIFIED_CI_REQUIRED_CONTEXTS=PASS")
    print("UNIFIED_CI_GOVERNANCE_MATRIX=PASS")
    print("UNIFIED_CI_BOOTSTRAP=PASS")
    print("UNIFIED_CI_PARALLEL_INVENTORY=PASS")
    print("UNIFIED_CI_LEGACY_ROUTINES_REMOVED=PASS")
    print("UNIFIED_CI_SPECIAL_WORKFLOWS_PRESERVED=PASS")
    if (root / PERFORMANCE_BUDGET).is_file():
        print("UNIFIED_CI_PERFORMANCE_BUDGET=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
