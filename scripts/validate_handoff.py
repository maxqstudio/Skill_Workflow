#!/usr/bin/env python3
"""Structural handoff validator for projects using Skill Workflow.

This validator intentionally checks structural discipline only.
It does not prove that documentation is semantically correct.
A failure blocks handoff; a pass still requires human/agent semantic audit.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CORE = [
    "PROJECT_MANIFEST.md",
    "CURRENT_STATE.md",
    "SOURCE_AUTHORITY_MAP.md",
    "ARCHITECTURE.md",
    "WORKFLOW_STATE_MACHINE.md",
    "MODULE_MAP.md",
    "SYMBOL_INDEX.md",
    "FLOW_INDEX.md",
    "TEST_ACCEPTANCE_MATRIX.md",
    "DOC_SYNC_MATRIX.md",
    "PROJECT_TRUTH_SYNC.md",
]

PLACEHOLDER_PATTERNS = (
    re.compile(r"<[^>]+>"),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
)

STALE_PATTERN = re.compile(r"\bSTALE\b", re.IGNORECASE)


def git_root(start: Path) -> Path:
    try:
        value = subprocess.check_output(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return Path(value)
    except Exception:
        return start.resolve()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_meaningful_placeholder(text: str) -> bool:
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="Project root containing the handoff documents.",
    )
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Do not fail on obvious TODO/TBD/<placeholder> tokens.",
    )
    args = parser.parse_args()

    root = git_root(Path(args.root))
    failures: list[str] = []
    warnings: list[str] = []

    print(f"HANDOFF_ROOT={root}")

    for rel in CORE:
        path = root / rel
        if not path.is_file():
            failures.append(f"MISSING_REQUIRED_DOC:{rel}")
            continue

        text = read(path)
        if not text.strip():
            failures.append(f"EMPTY_REQUIRED_DOC:{rel}")
            continue

        if rel in {"SYMBOL_INDEX.md", "FLOW_INDEX.md"} and STALE_PATTERN.search(text):
            # Templates can contain the word STALE in instructions. Fail only if
            # the document explicitly declares Status: STALE.
            if re.search(r"^Status\s*:\s*STALE\s*$", text, re.MULTILINE | re.IGNORECASE):
                failures.append(f"STALE_INDEX:{rel}")

        if not args.allow_placeholders and has_meaningful_placeholder(text):
            warnings.append(f"PLACEHOLDER_TOKEN_PRESENT:{rel}")

    current = root / "CURRENT_STATE.md"
    if current.is_file():
        text = read(current)
        for field in ("Authoritative SHA:", "Status:", "Next authorized action"):
            if field not in text:
                failures.append(f"CURRENT_STATE_FIELD_MISSING:{field}")

    authority = root / "SOURCE_AUTHORITY_MAP.md"
    if authority.is_file() and "Canonical authority" not in read(authority):
        failures.append("SOURCE_AUTHORITY_MAP_STRUCTURE_INVALID")

    symbol = root / "SYMBOL_INDEX.md"
    if symbol.is_file():
        text = read(symbol)
        if "Authority SHA:" not in text:
            failures.append("SYMBOL_INDEX_AUTHORITY_SHA_MISSING")
        if "| File | Symbol |" not in text:
            failures.append("SYMBOL_INDEX_TABLE_MISSING")

    flow = root / "FLOW_INDEX.md"
    if flow.is_file():
        text = read(flow)
        if "Authority SHA:" not in text:
            failures.append("FLOW_INDEX_AUTHORITY_SHA_MISSING")
        if "Flow inventory" not in text and "| Flow |" not in text:
            failures.append("FLOW_INDEX_INVENTORY_MISSING")

    matrix = root / "TEST_ACCEPTANCE_MATRIX.md"
    if matrix.is_file():
        text = read(matrix)
        if "Evidence boundary" not in text:
            failures.append("TEST_ACCEPTANCE_EVIDENCE_BOUNDARY_MISSING")
        if "Final tested source" not in text:
            failures.append("TEST_ACCEPTANCE_TESTED_SOURCE_MISSING")


    truth = root / "PROJECT_TRUTH_SYNC.md"
    if truth.is_file():
        text = read(truth)
        if "## Truth gates" not in text:
            failures.append("PROJECT_TRUTH_GATES_MISSING")
        if "## Critical claim traceability" not in text:
            failures.append("PROJECT_TRUTH_TRACEABILITY_MISSING")
        if "PROJECT_STATE_SYNC" not in text:
            failures.append("PROJECT_TRUTH_FINAL_GATE_MISSING")

    for warning in warnings:
        print(f"WARN {warning}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print(f"RESULT=FAIL failures={len(failures)} warnings={len(warnings)}")
        return 1

    print(f"RESULT=PASS failures=0 warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
