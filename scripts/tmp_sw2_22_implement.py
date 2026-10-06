#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def load(path: str) -> dict:
    return json.loads(read(path))


def dump(path: str, value: dict) -> None:
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError("PATCH_TARGET_MISSING:" + path + ":" + old[:80])
    if text.count(old) != 1:
        raise RuntimeError("PATCH_TARGET_NON_UNIQUE:" + path)
    write(path, text.replace(old, new, 1))


def run(*args: str, expect: int = 0) -> str:
    proc = subprocess.run(list(args), cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    print(proc.stdout, end="")
    if proc.returncode != expect:
        raise RuntimeError(f"command failed expected={expect} actual={proc.returncode}: {' '.join(args)}")
    return proc.stdout


def patch_toolchain_identity() -> None:
    replace_once(
        "scripts/toolchain_identity.py",
        "import json\nimport shutil\nimport subprocess\n",
        "import json\nimport re\nimport shutil\nimport subprocess\n",
    )
    replace_once(
        "scripts/toolchain_identity.py",
        '    "migrate_governance_v1.py",\n    "selftest_project_truth_compiler.py",\n',
        '    "migrate_governance_v1.py",\n    "selftest_project_truth_compiler.py",\n    "upgrade_governance_toolchain.py",\n',
    )
    replace_once(
        "scripts/toolchain_identity.py",
        '''def producer_metadata(skill_root: Path) -> dict[str, str]:\n    return {\n        "repository": _git_value(skill_root, "config", "--get", "remote.origin.url"),\n        "commit_hint": _git_value(skill_root, "rev-parse", "HEAD"),\n    }\n''',
        '''def producer_metadata(skill_root: Path) -> dict[str, str]:\n    repository = _git_value(skill_root, "config", "--get", "remote.origin.url")\n    source_sha = _git_value(skill_root, "rev-parse", "HEAD").lower()\n    release = _git_value(skill_root, "describe", "--tags", "--exact-match", "HEAD")\n    if not repository or not re.fullmatch(r"[0-9a-f]{40}", source_sha):\n        raise ValueError("TOOLCHAIN_PRODUCER_GIT_IDENTITY_UNAVAILABLE")\n    return {\n        "identity_source": "GIT",\n        "repository": repository,\n        "source_sha": source_sha,\n        "release": release or "UNRELEASED",\n    }\n''',
    )
    replace_once(
        "scripts/toolchain_identity.py",
        '''    producer = lock.get("producer")\n    if not isinstance(producer, dict):\n        failures.append("TOOLCHAIN_PRODUCER_METADATA_INVALID")\n    return failures\n''',
        '''    producer = lock.get("producer")\n    if not isinstance(producer, dict):\n        failures.append("TOOLCHAIN_PRODUCER_METADATA_INVALID")\n        return failures\n    if str(producer.get("identity_source", "")).strip() != "GIT":\n        failures.append("TOOLCHAIN_PRODUCER_IDENTITY_SOURCE_INVALID")\n    if not str(producer.get("repository", "")).strip():\n        failures.append("TOOLCHAIN_PRODUCER_REPOSITORY_MISSING")\n    source_sha = str(producer.get("source_sha", "")).strip().lower()\n    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):\n        failures.append("TOOLCHAIN_PRODUCER_SOURCE_SHA_INVALID")\n    if not str(producer.get("release", "")).strip():\n        failures.append("TOOLCHAIN_PRODUCER_RELEASE_MISSING")\n    if "commit_hint" in producer:\n        failures.append("TOOLCHAIN_PRODUCER_LEGACY_COMMIT_HINT")\n    return failures\n''',
    )


def write_upgrader() -> None:
    write(
        "scripts/upgrade_governance_toolchain.py",
        r'''#!/usr/bin/env python3
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
    producer_mismatch = target_identity != source_identity
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
''',
    )


def update_authority_and_docs() -> None:
    replace_once("scripts/schema_contract.py", "TOOLCHAIN_CONTRACT_VERSION = 1\n", "TOOLCHAIN_CONTRACT_VERSION = 2\n")

    contracts = load(".workflow/contracts.json")
    for item in contracts.get("data_contracts", []):
        if item.get("name") == ".workflow/toolchain.lock.json":
            item["invariants"] = [
                "toolchain file hashes and manifest digest match .workflow/tools/*.py",
                "producer repository, exact source SHA, release identity, and identity source are explicit and validator-enforced",
                "legacy hint-only producer identity is migration input, never acceptance authority",
                "source-side upgrade check is read-only and apply mutates only toolchain-owned surfaces",
            ]
            item["legal_writes"] = [
                "scripts/initialize_project_truth.py",
                "scripts/migrate_governance_v1.py",
                "scripts/upgrade_governance_toolchain.py",
            ]
            item["source_of_truth"] = "deterministic manifest of project-local vendored governance tool bytes plus exact producer source identity"
    dump(".workflow/contracts.json", contracts)

    decisions = load(".workflow/decisions.json")
    if not any(item.get("id") == "SW2-ADR-011" for item in decisions.get("decisions", [])):
        decisions["decisions"].append(
            {
                "id": "SW2-ADR-011",
                "title": "Make consumer toolchain provenance exact and upgrades explicit",
                "status": "ACCEPTED",
                "decision": "Toolchain contract version 2 replaces informational producer commit hints with validator-enforced Git repository, exact source SHA, and release identity. Consumer upgrades are source-side, plan-before-write, limited to vendored tool files plus the lock, and legacy v2.1 locks migrate explicitly.",
                "rationale": "Content digests prove internal byte consistency but do not identify which upstream Skill Workflow snapshot supplied those bytes. Exact producer identity plus a deterministic read-only upgrade plan closes that provenance gap without allowing automated edits to Owner semantic authority.",
            }
        )
    dump(".workflow/decisions.json", decisions)

    session = load("docs/sequence/sessions/SW2-22-GOVERNANCE.json")
    entries = session["actual"]["entries"]
    if "scripts/upgrade_governance_toolchain.py::main" not in entries:
        entries.append("scripts/upgrade_governance_toolchain.py::main")
    session["evidence_boundary"] = "SW2-22 sequence evidence covers exact producer identity generation/validation plus deterministic source-side toolchain upgrade planning/apply. It does not authorize writes outside vendored toolchain-owned files and the toolchain lock."
    dump("docs/sequence/sessions/SW2-22-GOVERNANCE.json", session)

    commands = read("docs/handbook/reference/commands.md")
    marker = "## Toolchain provenance and upgrade"
    if marker not in commands:
        insertion = '''\n## Toolchain provenance and upgrade\n\nRun upgrade inspection from the Skill Workflow checkout/package that should become the consumer's toolchain source:\n\n```bash\npython scripts/upgrade_governance_toolchain.py --root /path/to/project --check\n```\n\n`--check` is read-only and exits non-zero when an upgrade or provenance migration is required. Review the emitted `PLAN_JSON`, then apply only the vendored toolchain surfaces:\n\n```bash\npython scripts/upgrade_governance_toolchain.py --root /path/to/project --apply\n```\n\nApply may change only `.workflow/tools/*.py` owned by the prior/current toolchain and `.workflow/toolchain.lock.json`. It does not rewrite `AGENTS.md`, project semantic `.workflow/*.json`, source code, or project-specific configuration.\n'''
        commands = commands.replace("\n## Synchronize Project Truth\n", insertion + "\n## Synchronize Project Truth\n", 1)
        write("docs/handbook/reference/commands.md", commands)

    adoption = read("docs/handbook/getting-started/adoption.md")
    marker = "### Toolchain identity and later upgrades"
    if marker not in adoption:
        insertion = '''\n### Toolchain identity and later upgrades\n\nInitialization records a content manifest and exact producer identity in `.workflow/toolchain.lock.json`. Updating an installed agent skill does not silently replace the vendored governance tools already committed in a consumer repository. To inspect a later Skill Workflow checkout against an existing consumer, run `scripts/upgrade_governance_toolchain.py --root <project> --check` from that checkout and review the machine-readable plan before using `--apply`. Legacy hint-only locks require this explicit migration path.\n'''
        adoption = adoption.replace("\n## 3. Populate semantic authority\n", insertion + "\n## 3. Populate semantic authority\n", 1)
        write("docs/handbook/getting-started/adoption.md", adoption)

    normative = read("references/governance-and-project-truth.md")
    marker = "## Consumer Toolchain Provenance"
    if marker not in normative:
        normative += '''\n\n## Consumer Toolchain Provenance\n\nVendored `.workflow/tools/` bytes and `.workflow/toolchain.lock.json` form one governed toolchain identity. The lock MUST record validator-enforced producer repository, exact Git source SHA, release identity (`UNRELEASED` when HEAD is not exactly tagged), and `identity_source=GIT`. A legacy `commit_hint` is migration input only and MUST NOT be treated as acceptance authority.\n\nToolchain upgrades MUST be inspected read-only before mutation. Apply may write only toolchain-owned vendored files and the toolchain lock; it MUST NOT rewrite `AGENTS.md`, project source, or semantic `.workflow` authority. Unknown or unmanaged tool files fail closed rather than being deleted automatically.\n'''
        write("references/governance-and-project-truth.md", normative)


def strengthen_regression() -> None:
    path = "scripts/selftest_toolchain_provenance_upgrade.py"
    text = read(path)
    old = '''        baseline = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--check")\n        if "UPGRADE_REQUIRED=NO" not in baseline or "RESULT=PASS" not in baseline:\n            return fail("CURRENT_CHECK_NOT_CLEAN")\n'''
    new = '''        baseline = run(skill_root, sys.executable, str(upgrader), "--root", str(root), "--check")\n        if "UPGRADE_REQUIRED=NO" not in baseline or "RESULT=PASS" not in baseline:\n            return fail("CURRENT_CHECK_NOT_CLEAN")\n        plan_line = next((line for line in baseline.splitlines() if line.startswith("PLAN_JSON=")), "")\n        if not plan_line:\n            return fail("MACHINE_READABLE_PLAN_MISSING")\n        plan = json.loads(plan_line.split("=", 1)[1])\n        file_plan = plan.get("files") or {}\n        if sorted(file_plan) != ["added", "changed", "removed", "unchanged", "unmanaged"]:\n            return fail("PLAN_FILE_CLASSES_INCOMPLETE")\n'''
    if old not in text:
        raise RuntimeError("REGRESSION_PATCH_TARGET_MISSING")
    write(path, text.replace(old, new, 1))


def commit_source() -> str:
    run("git", "add", "scripts/schema_contract.py", "scripts/toolchain_identity.py", "scripts/upgrade_governance_toolchain.py", "scripts/selftest_toolchain_provenance_upgrade.py", ".workflow/contracts.json", ".workflow/decisions.json", "docs/handbook/reference/commands.md", "docs/handbook/getting-started/adoption.md", "references/governance-and-project-truth.md", "docs/sequence/sessions/SW2-22-GOVERNANCE.json")
    run("git", "commit", "-m", "SW2-22: implement exact toolchain provenance and upgrade")
    return run("git", "rev-parse", "HEAD").strip()


def regenerate_sequence() -> None:
    session = load("docs/sequence/sessions/SW2-22-GOVERNANCE.json")
    actual = session["actual"]
    cmd = [sys.executable, "scripts/generate_sequence_actual.py", "--root", ".", "--output-json", actual["graph"], "--output-mermaid", actual["diagram"]]
    for entry in actual["entries"]:
        cmd.extend(["--entry", entry])
    run(*cmd)
    human = session["human_view"]
    run(sys.executable, "scripts/sequence_human_view.py", "--root", ".", "--actual-json", actual["graph"], "--actual-mermaid", actual["diagram"], "--output-json", human["graph"], "--output-mermaid", human["diagram"], "--output-markdown", human["document"], "--session-id", session["session_id"])
    graph = load(actual["graph"])
    session["actual"]["source_digest"] = graph["source_digest"]
    session["human_view"]["source_digest"] = graph["source_digest"]
    dump("docs/sequence/sessions/SW2-22-GOVERNANCE.json", session)
    run(sys.executable, "scripts/validate_sequence_contract.py", "--root", ".", "--session", "docs/sequence/sessions/SW2-22-GOVERNANCE.json", "--report", "artifacts/sequence/SW2-22-GOVERNANCE.acceptance.json")
    run(sys.executable, "scripts/validate_sequence_human_view.py", "--root", ".", "--session", "docs/sequence/sessions/SW2-22-GOVERNANCE.json")
    run(sys.executable, "scripts/validate_sequence_sessions.py", "--root", ".")


def main() -> int:
    patch_toolchain_identity()
    write_upgrader()
    update_authority_and_docs()
    strengthen_regression()
    source_head = commit_source()
    print("SW2_22_SOURCE_HEAD=" + source_head)

    run(sys.executable, "scripts/selftest_toolchain_provenance_upgrade.py")
    run(sys.executable, "scripts/selftest_schema_toolchain.py")
    run(sys.executable, "scripts/migrate_governance_v1.py", "--root", ".")
    run(sys.executable, "scripts/migrate_governance_v1.py", "--root", ".")
    run(sys.executable, "scripts/validate_schema_toolchain.py", "--root", ".")
    run(sys.executable, "scripts/selftest_adoption_profiles.py")
    run(sys.executable, "scripts/selftest_strict_project_workflow.py")

    regenerate_sequence()
    run(sys.executable, "scripts/sync_project_truth.py", "--root", ".")
    run(sys.executable, "scripts/validate_project_docs.py", "--root", ".")
    run(sys.executable, "scripts/selftest_public_docs.py")
    run(sys.executable, "scripts/validate_public_docs.py", "--root", ".")
    run(sys.executable, "scripts/selftest_cross_document_regressions.py")

    state = load(".workflow/state.json")
    state["status"] = "SW2_22_IMPLEMENTED_PENDING_ACCEPTANCE"
    state["next_authorized_actions"] = [
        "Run the permanent exact-head matrix on the helper-free SW2-22 implementation candidate.",
        "Promote R1-R4 only from exact candidate evidence; R5 remains pending merge and post-merge revalidation.",
        "Do not begin SW2-23 or publish a new release without separate Owner authorization.",
    ]
    dump(".workflow/state.json", state)
    run(sys.executable, "scripts/sync_project_truth.py", "--root", ".")
    print("SW2_22_TARGETED_IMPLEMENTATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
