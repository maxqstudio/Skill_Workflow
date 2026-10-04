#!/usr/bin/env python3
"""Fail-closed integrity checks for Skill Workflow progressive disclosure."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

MAX_SKILL_LINES = 500
MAX_SKILL_BYTES = 18000
REQUIRED_REFERENCES = (
    "references/governance-and-project-truth.md",
    "references/execution-and-acceptance.md",
    "references/project-truth-synchronization.md",
    "references/sequence-contracts.md",
)
CORE_INVARIANTS = (
    "Do not begin by reading the entire repository blindly.",
    "AGENTS.md",
    "PROJECT_PROFILE.yaml",
    ".workflow/state.json::phase",
    ".workflow/roadmap.json::current_phase",
    "Never treat source changed as equivalent to PASS.",
    "SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL",
    "FINAL SOURCE SHA = TESTED SHA",
    "TESTED_HEAD = FINAL_SOURCE_HEAD = FINAL_DOCUMENTATION_HEAD",
    "develop → verify → finalize",
    "retrospective plans are forbidden",
    "Broken required references fail closed.",
    "If a required gate is `FAIL`, `NOT_PROVEN`, unresolved, or stale, final status cannot be PASS.",
)
LINK_RE = re.compile(r"\[[^\]]+\]\((references/[^)#?]+\.md)(?:#[^)]+)?\)")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["SKILL_MISSING:SKILL.md"]
    raw = skill.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        failures.append(f"SKILL_LINE_BUDGET_EXCEEDED:{len(lines)}>{MAX_SKILL_LINES}")
    if len(raw) > MAX_SKILL_BYTES:
        failures.append(f"SKILL_BYTE_BUDGET_EXCEEDED:{len(raw)}>{MAX_SKILL_BYTES}")
    if not text.startswith("---\n") or "\nname: project-handoff-workflow\n" not in text or "\ndescription:" not in text:
        failures.append("SKILL_FRONTMATTER_INVALID")
    for invariant in CORE_INVARIANTS:
        if invariant not in text:
            failures.append("CORE_INVARIANT_MISSING:" + invariant)

    links = LINK_RE.findall(text)
    for ref in REQUIRED_REFERENCES:
        count = links.count(ref)
        if count != 1:
            failures.append(f"REQUIRED_REFERENCE_ROUTE_COUNT:{ref}:{count}")
        if not (root / ref).is_file():
            failures.append("MISSING_REQUIRED_REFERENCE:" + ref)
    for ref in links:
        if ref not in REQUIRED_REFERENCES:
            failures.append("UNDECLARED_REFERENCE_ROUTE:" + ref)
        if not (root / ref).is_file():
            failures.append("BROKEN_REFERENCE_LINK:" + ref)
    if set(links) != set(REQUIRED_REFERENCES):
        failures.append("REFERENCE_ROUTE_SET_MISMATCH")

    for ref in REQUIRED_REFERENCES:
        path = root / ref
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        nested = LINK_RE.findall(body)
        if nested:
            failures.append("REFERENCE_CHAIN_FORBIDDEN:" + ref + ":" + ",".join(nested))
        if len(body.strip()) < 200:
            failures.append("REFERENCE_TOO_SMALL:" + ref)
    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    failures = validate(Path(args.root))
    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    root = Path(args.root).resolve()
    skill = root / "SKILL.md"
    print(f"SKILL_REFERENCE_SPLIT=PASS lines={len(skill.read_text(encoding='utf-8').splitlines())} bytes={len(skill.read_bytes())} references={len(REQUIRED_REFERENCES)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
