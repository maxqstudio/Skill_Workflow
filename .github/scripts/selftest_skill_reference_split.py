#!/usr/bin/env python3
"""Negative-path regression for Skill Workflow progressive disclosure."""
from __future__ import annotations

import importlib.util
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".github" / "scripts" / "validate_skill_reference_split.py"
spec = importlib.util.spec_from_file_location("skill_split_validator", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def copy_fixture() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="sw2-13-skill-split-"))
    shutil.copy2(ROOT / "SKILL.md", tmp / "SKILL.md")
    shutil.copytree(ROOT / "references", tmp / "references")
    return tmp


def require_failure(root: Path, prefix: str) -> None:
    failures = module.validate(root)
    if not any(item.startswith(prefix) for item in failures):
        raise AssertionError(f"expected {prefix}, got {failures}")


def main() -> int:
    clean = module.validate(ROOT)
    if clean:
        raise AssertionError(f"clean contract failed: {clean}")

    fixtures: list[Path] = []
    try:
        missing = copy_fixture(); fixtures.append(missing)
        (missing / module.REQUIRED_REFERENCES[0]).unlink()
        require_failure(missing, "MISSING_REQUIRED_REFERENCE:")

        broken = copy_fixture(); fixtures.append(broken)
        text = (broken / "SKILL.md").read_text(encoding="utf-8")
        text = text.replace(module.REQUIRED_REFERENCES[0], "references/missing.md")
        (broken / "SKILL.md").write_text(text, encoding="utf-8")
        require_failure(broken, "BROKEN_REFERENCE_LINK:")

        duplicate = copy_fixture(); fixtures.append(duplicate)
        text = (duplicate / "SKILL.md").read_text(encoding="utf-8")
        text += f"\n[duplicate]({module.REQUIRED_REFERENCES[0]})\n"
        (duplicate / "SKILL.md").write_text(text, encoding="utf-8")
        require_failure(duplicate, "REQUIRED_REFERENCE_ROUTE_COUNT:")

        chained = copy_fixture(); fixtures.append(chained)
        ref = chained / module.REQUIRED_REFERENCES[0]
        ref.write_text(ref.read_text(encoding="utf-8") + "\n[nested](references/sequence-contracts.md)\n", encoding="utf-8")
        require_failure(chained, "REFERENCE_CHAIN_FORBIDDEN:")

        invariant = copy_fixture(); fixtures.append(invariant)
        text = (invariant / "SKILL.md").read_text(encoding="utf-8")
        text = text.replace("FINAL SOURCE SHA = TESTED SHA", "FINAL SOURCE ID = TESTED ID")
        (invariant / "SKILL.md").write_text(text, encoding="utf-8")
        require_failure(invariant, "CORE_INVARIANT_MISSING:")

        oversized = copy_fixture(); fixtures.append(oversized)
        text = (oversized / "SKILL.md").read_text(encoding="utf-8") + ("padding\n" * 600)
        (oversized / "SKILL.md").write_text(text, encoding="utf-8")
        require_failure(oversized, "SKILL_LINE_BUDGET_EXCEEDED:")
    finally:
        for path in fixtures:
            shutil.rmtree(path, ignore_errors=True)

    print("SKILL_REFERENCE_SPLIT_SELFTEST=PASS negative_paths=6")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
