#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cwd: Path, *args: str, expect: int = 0) -> str:
    proc = subprocess.run(list(args), cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != expect:
        raise RuntimeError(f"command failed expected={expect} actual={proc.returncode}\n{proc.stdout}")
    return proc.stdout


def fail(code: str) -> int:
    print("FAIL " + code)
    return 1


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    source_sha = run(skill_root, "git", "rev-parse", "HEAD").strip()
    with tempfile.TemporaryDirectory(prefix="skill-workflow-toolchain-upgrade-") as td:
        root = Path(td)
        run(skill_root, sys.executable, str(skill_root / "scripts" / "initialize_project_truth.py"), "--root", str(root))
        lock_path = root / ".workflow" / "toolchain.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        producer = lock.get("producer") or {}
        recorded_sha = str(producer.get("source_sha", "")).strip()
        if not re.fullmatch(r"[0-9a-f]{40}", recorded_sha):
            return fail("PRODUCER_SOURCE_SHA_MISSING")
        if recorded_sha != source_sha:
            return fail("PRODUCER_SOURCE_SHA_MISMATCH")
        if not str(producer.get("repository", "")).strip():
            return fail("PRODUCER_REPOSITORY_MISSING")
        if not str(producer.get("release", "")).strip():
            return fail("PRODUCER_RELEASE_IDENTITY_MISSING")
        if str(producer.get("identity_source", "")).strip() != "GIT":
            return fail("PRODUCER_IDENTITY_SOURCE_NOT_GIT")
        if "commit_hint" in producer:
            return fail("LEGACY_COMMIT_HINT_STILL_AUTHORITATIVE")

        upgrader = skill_root / "scripts" / "upgrade_governance_toolchain.py"
        if not upgrader.is_file():
            return fail("UPGRADE_COMMAND_MISSING")
        baseline = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--check")
        if "UPGRADE_REQUIRED=NO" not in baseline or "RESULT=PASS" not in baseline:
            return fail("CURRENT_CHECK_NOT_CLEAN")
        plan_line = next((line for line in baseline.splitlines() if line.startswith("PLAN_JSON=")), "")
        if not plan_line:
            return fail("MACHINE_READABLE_PLAN_MISSING")
        plan = json.loads(plan_line.split("=", 1)[1])
        file_plan = plan.get("files") or {}
        if sorted(file_plan) != ["added", "changed", "removed", "unchanged", "unmanaged"]:
            return fail("PLAN_FILE_CLASSES_INCOMPLETE")

        tool = root / ".workflow" / "tools" / "sync_project_truth.py"
        tool.write_text(tool.read_text(encoding="utf-8") + "\n# sw2-22 tamper\n", encoding="utf-8", newline="\n")
        tampered_before = tool.read_bytes()
        check = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--check", expect=1)
        if "UPGRADE_REQUIRED=YES" not in check:
            return fail("TAMPER_NOT_PLANNED")
        if tool.read_bytes() != tampered_before:
            return fail("CHECK_MODE_MUTATED_CONSUMER")

        agents = root / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nOWNER_SENTINEL\n", encoding="utf-8", newline="\n")
        state_path = root / ".workflow" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["owner_sentinel"] = "preserve-me"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

        applied = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--apply")
        if "RESULT=PASS" not in applied:
            return fail("APPLY_FAILED")
        if "OWNER_SENTINEL" not in agents.read_text(encoding="utf-8"):
            return fail("AGENTS_OVERWRITTEN")
        if json.loads(state_path.read_text(encoding="utf-8")).get("owner_sentinel") != "preserve-me":
            return fail("SEMANTIC_AUTHORITY_OVERWRITTEN")
        run(root, sys.executable, str(root / ".workflow" / "tools" / "validate_schema_toolchain.py"), "--root", str(root))

        second = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--apply")
        if "TOOL_FILES_WRITTEN=0" not in second or "LOCK_WRITTEN=NO" not in second:
            return fail("APPLY_NOT_IDEMPOTENT")

        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["producer"] = {"repository": lock["producer"]["repository"], "commit_hint": source_sha}
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        legacy_check = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--check", expect=1)
        if "UPGRADE_REQUIRED=YES" not in legacy_check:
            return fail("LEGACY_HINT_ONLY_NOT_DETECTED")
        run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--apply")
        migrated = json.loads(lock_path.read_text(encoding="utf-8"))
        if str((migrated.get("producer") or {}).get("source_sha", "")) != source_sha:
            return fail("LEGACY_PROVENANCE_NOT_MIGRATED")

    print("EXACT_PRODUCER_IDENTITY=PASS")
    print("READ_ONLY_UPGRADE_PLAN=PASS")
    print("TOOL_OWNED_APPLY=PASS")
    print("SEMANTIC_AUTHORITY_PRESERVATION=PASS")
    print("UPGRADE_IDEMPOTENCE=PASS")
    print("LEGACY_PROVENANCE_MIGRATION=PASS")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
