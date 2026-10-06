#!/usr/bin/env python3
"""Plan or apply deterministic upgrades of project-local vendored governance tools."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from schema_contract import TOOLCHAIN_CONTRACT_VERSION, TOOLCHAIN_LOCK_SCHEMA_VERSION
from toolchain_identity import (
    producer_metadata,
    source_tool_paths,
    sync_vendored_tools,
    tool_manifest,
    validate_toolchain_lock,
    write_toolchain_lock,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_manifest(skill_root: Path) -> dict[str, str]:
    return {path.name: sha256(path) for path in source_tool_paths(skill_root)}


def load_lock(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def producer_upgrade_required(target: dict, source: dict) -> bool:
    if target == source:
        return False
    same_digest = (
        str(target.get("source_digest", "")).strip().lower()
        and str(target.get("source_digest", "")).strip().lower()
        == str(source.get("source_digest", "")).strip().lower()
    )
    if (
        same_digest
        and str(target.get("identity_source", "")) == "GIT+CONTENT"
        and str(source.get("identity_source", "")) == "CONTENT"
    ):
        return False
    return True


def build_plan(skill_root: Path, project_root: Path) -> dict[str, object]:
    spec_root = project_root / ".workflow"
    tool_root = spec_root / "tools"
    lock = load_lock(spec_root / "toolchain.lock.json")
    source = source_manifest(skill_root)
    actual = tool_manifest(tool_root)
    declared_raw = lock.get("files")
    declared = declared_raw if isinstance(declared_raw, dict) else {}
    declared_names = set(str(name) for name in declared)
    source_names = set(source)
    actual_names = set(actual)

    added = sorted(source_names - actual_names)
    removed = sorted(declared_names - source_names)
    changed = sorted(name for name in source_names & actual_names if source[name] != actual[name])
    unchanged = sorted(name for name in source_names & actual_names if source[name] == actual[name])
    unmanaged = sorted(actual_names - declared_names - source_names)
    target_identity = lock.get("producer") if isinstance(lock.get("producer"), dict) else {}
    source_identity = producer_metadata(skill_root)
    validation_failures = validate_toolchain_lock(project_root, spec_root)
    contract_mismatch = (
        lock.get("schema_version") != TOOLCHAIN_LOCK_SCHEMA_VERSION
        or lock.get("toolchain_contract_version") != TOOLCHAIN_CONTRACT_VERSION
    )
    producer_mismatch = producer_upgrade_required(target_identity, source_identity)
    manifest_mismatch = declared != source
    upgrade_required = bool(
        added
        or removed
        or changed
        or unmanaged
        or contract_mismatch
        or producer_mismatch
        or manifest_mismatch
        or validation_failures
    )
    return {
        "schema_version": 1,
        "upgrade_required": upgrade_required,
        "source_identity": source_identity,
        "target_identity": target_identity,
        "files": {
            "added": added,
            "removed": removed,
            "changed": changed,
            "unchanged": unchanged,
            "unmanaged": unmanaged,
        },
        "target_validation_failures": sorted(validation_failures),
        "target_contract_version": lock.get("toolchain_contract_version"),
        "source_contract_version": TOOLCHAIN_CONTRACT_VERSION,
    }


def emit(plan: dict[str, object]) -> None:
    files = plan["files"]
    assert isinstance(files, dict)
    source_identity = plan["source_identity"]
    target_identity = plan["target_identity"]
    assert isinstance(source_identity, dict)
    assert isinstance(target_identity, dict)
    print("PLAN_JSON=" + json.dumps(plan, sort_keys=True, separators=(",", ":")))
    print("UPGRADE_REQUIRED=" + ("YES" if plan["upgrade_required"] else "NO"))
    print("SOURCE_IDENTITY=" + str(source_identity.get("identity_source", "")))
    print("SOURCE_DIGEST=" + str(source_identity.get("source_digest", "")))
    print("SOURCE_SHA=" + str(source_identity.get("source_sha", "")))
    print("TARGET_SOURCE_SHA=" + str(target_identity.get("source_sha", "")))
    for key in ("added", "removed", "changed", "unchanged", "unmanaged"):
        values = files.get(key, [])
        print("FILES_" + key.upper() + "=" + ",".join(str(item) for item in values))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.root).resolve()
    skill_root = Path(__file__).resolve().parent.parent
    spec_root = project_root / ".workflow"
    tool_root = spec_root / "tools"
    if not spec_root.is_dir() or not tool_root.is_dir():
        print("FAIL GOVERNANCE_TOOLCHAIN_MISSING")
        return 1

    before = build_plan(skill_root, project_root)
    emit(before)
    if args.check:
        print("RESULT=" + ("UPGRADE_REQUIRED" if before["upgrade_required"] else "PASS"))
        return 1 if before["upgrade_required"] else 0

    files = before["files"]
    assert isinstance(files, dict)
    unmanaged = list(files.get("unmanaged", []))
    if unmanaged:
        print("FAIL UNMANAGED_TOOL_FILES=" + ",".join(str(item) for item in unmanaged))
        return 1

    sync = sync_vendored_tools(skill_root, tool_root)
    removed_count = 0
    for name in list(files.get("removed", [])):
        target = tool_root / str(name)
        if target.is_file():
            target.unlink()
            removed_count += 1
    lock_result = write_toolchain_lock(project_root, spec_root, tool_root, skill_root)
    failures = validate_toolchain_lock(project_root, spec_root)
    if failures:
        print("FAIL TOOLCHAIN_POST_APPLY=" + ";".join(failures))
        return 1
    after = build_plan(skill_root, project_root)
    if after["upgrade_required"]:
        print("FAIL UPGRADE_STILL_REQUIRED")
        emit(after)
        return 1
    print("TOOL_FILES_WRITTEN=" + str(sync["writes"]))
    print("TOOL_FILES_REMOVED=" + str(removed_count))
    print("LOCK_WRITTEN=" + ("YES" if lock_result == "WRITE" else "NO"))
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
