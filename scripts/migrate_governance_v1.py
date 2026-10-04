#!/usr/bin/env python3
"""Explicit deterministic migration of legacy governance state to schema v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from project_profile import parse_profile
from schema_contract import (
    GOVERNED_SPEC_SCHEMA_VERSION,
    PROFILE_SCHEMA_VERSION,
    governed_spec_paths,
    require_json_schema_version,
    require_profile_schema_version,
    validate_spec_tree_versions,
)
from toolchain_identity import (
    sync_vendored_tools,
    validate_toolchain_lock,
    write_toolchain_lock,
)


def add_profile_version(path: Path) -> bool:
    data = parse_profile(path, require_schema_version=False)
    if "schema_version" in data:
        require_profile_schema_version(data, path.name)
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    insert_at = 0
    while insert_at < len(lines):
        stripped = lines[insert_at].strip()
        if stripped and not stripped.startswith("#"):
            break
        insert_at += 1
    lines.insert(insert_at, "schema_version: " + str(PROFILE_SCHEMA_VERSION))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    return True


def inspect_specs(spec_root: Path) -> list[Path]:
    missing: list[Path] = []
    for path in governed_spec_paths(spec_root):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("SPEC_TOP_LEVEL_OBJECT_REQUIRED:" + path.as_posix())
        if "schema_version" not in data:
            missing.append(path)
        else:
            require_json_schema_version(data, path.relative_to(spec_root).as_posix())
    return missing


def add_spec_version(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    upgraded = {"schema_version": GOVERNED_SPEC_SCHEMA_VERSION}
    upgraded.update(data)
    path.write_text(
        json.dumps(upgraded, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skill_root = Path(__file__).resolve().parent.parent
    profile_path = root / "PROJECT_PROFILE.yaml"
    agents_path = root / "AGENTS.md"
    agents_template = skill_root / "templates" / "AGENTS.md"
    spec_root = root / ".workflow"
    if not profile_path.is_file() or not spec_root.is_dir():
        print("FAIL GOVERNANCE_ROOT_INCOMPLETE")
        return 1

    try:
        profile_data = parse_profile(profile_path, require_schema_version=False)
        profile_missing = "schema_version" not in profile_data
        if not profile_missing:
            require_profile_schema_version(profile_data, profile_path.name)
        missing_specs = inspect_specs(spec_root)
        agents_missing = not agents_path.is_file()
    except Exception as exc:
        print("FAIL MIGRATION_PRECHECK:" + str(exc))
        return 1

    tool_root = spec_root / "tools"
    lock_failures = (
        validate_toolchain_lock(root, spec_root)
        if tool_root.is_dir() or (spec_root / "toolchain.lock.json").is_file()
        else ["TOOLCHAIN_LOCK_MISSING:.workflow/toolchain.lock.json"]
    )
    required = agents_missing or profile_missing or bool(missing_specs) or bool(lock_failures)
    if args.check:
        print("MIGRATION_REQUIRED=" + ("YES" if required else "NO"))
        print("AGENTS_MISSING=" + ("YES" if agents_missing else "NO"))
        print("PROFILE_VERSION_MISSING=" + ("YES" if profile_missing else "NO"))
        print("SPEC_VERSIONS_MISSING=" + str(len(missing_specs)))
        print("TOOLCHAIN_LOCK_ISSUES=" + str(len(lock_failures)))
        return 1 if required else 0

    changes = 0
    if agents_missing:
        if not agents_template.is_file():
            print("FAIL AGENTS_TEMPLATE_MISSING")
            return 1
        agents_path.write_bytes(agents_template.read_bytes())
        changes += 1
    if profile_missing and add_profile_version(profile_path):
        changes += 1
    for path in missing_specs:
        add_spec_version(path)
        changes += 1

    sync = sync_vendored_tools(skill_root, tool_root)
    changes += int(sync["writes"])
    if write_toolchain_lock(root, spec_root, tool_root, skill_root) == "WRITE":
        changes += 1

    try:
        if not agents_path.is_file():
            raise ValueError("ROOT_AGENTS_MISSING_AFTER_MIGRATION")
        parse_profile(profile_path)
        spec_failures = validate_spec_tree_versions(spec_root)
        if spec_failures:
            raise ValueError(";".join(spec_failures))
        lock_failures = validate_toolchain_lock(root, spec_root)
        if lock_failures:
            raise ValueError(";".join(lock_failures))
    except Exception as exc:
        print("FAIL MIGRATION_POSTCHECK:" + str(exc))
        return 1

    print("MIGRATION_TARGET_SCHEMA=1")
    print("MIGRATION_CHANGES=" + str(changes))
    print("TOOL_FILES_SYNCED=" + str(sync["writes"]))
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
