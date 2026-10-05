#!/usr/bin/env python3
"""Validate the SW2-18 unified permanent CI contract."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_CONTEXTS = (
    "Self Governance (ubuntu-latest)",
    "Governance Selftest (ubuntu-latest)",
    "Governance Selftest (windows-latest)",
    "SW2 Sequence Evidence (ubuntu-latest)",
    "Governance Engine Performance (ubuntu-latest)",
    "Consumer Engine Performance (max-grounding)",
)
OLD_ROUTINE_WORKFLOWS = (
    "governance-selftest.yml",
    "self-governance.yml",
    "sw2-baseline.yml",
    "sw2-consumer-baseline.yml",
    "sw2-sequence.yml",
)


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

    for context in REQUIRED_CONTEXTS:
        if text.count(f"name: {context}") != 1:
            failures.append(f"CHECK_CONTEXT_MISSING_OR_DUPLICATE:{context}")

    if text.count("./.github/actions/governance-bootstrap") < 5:
        failures.append("BOOTSTRAP_NOT_CENTRALIZED")
    if "ci_applicability" not in text and "steps.bootstrap.outputs.heavy" not in text:
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

    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    print("UNIFIED_CI_REQUIRED_CONTEXTS=PASS")
    print("UNIFIED_CI_BOOTSTRAP=PASS")
    print("UNIFIED_CI_LEGACY_ROUTINES_REMOVED=PASS")
    print("UNIFIED_CI_SPECIAL_WORKFLOWS_PRESERVED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
