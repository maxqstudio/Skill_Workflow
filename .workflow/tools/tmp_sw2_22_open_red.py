#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "65c28fcdfebec68a20adc02ae95406f9261d5a51"
BRANCH = "work/sw2-22-consumer-toolchain-provenance-upgrade"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path: str, value: dict) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run(*args: str, expect: int = 0) -> str:
    proc = subprocess.run(
        list(args), cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False
    )
    print(proc.stdout, end="")
    if proc.returncode != expect:
        raise RuntimeError(f"command failed expected={expect} actual={proc.returncode}: {' '.join(args)}")
    return proc.stdout


def open_authority() -> None:
    roadmap = load(".workflow/roadmap.json")
    if roadmap.get("current_phase") != "SW2-21":
        raise RuntimeError("UNEXPECTED_CURRENT_PHASE:" + str(roadmap.get("current_phase")))
    for phase in roadmap.get("phases", []):
        if phase.get("id") == "SW2-21":
            phase["status"] = "COMPLETE"
    if any(p.get("id") == "SW2-22" for p in roadmap.get("phases", [])):
        raise RuntimeError("SW2_22_ALREADY_EXISTS")
    roadmap["current_phase"] = "SW2-22"
    roadmap["phases"].append(
        {
            "id": "SW2-22",
            "title": "Consumer Toolchain Provenance & Upgrade Contract",
            "status": "CURRENT",
            "objective": "Bind every vendored consumer toolchain to explicit upstream source identity and provide deterministic, fail-closed, idempotent upgrade planning and execution without modifying Owner semantic authority.",
            "exit_criteria": [
                "Every newly written consumer toolchain lock records machine-verifiable producer repository, exact source SHA, and exact release tag when the producer HEAD is tagged; untagged development sources are explicitly marked UNRELEASED rather than guessed.",
                "Missing, malformed, or legacy hint-only producer identity fails closed under the current validator and has an explicit deterministic migration path.",
                "A source-side upgrade command provides a read-only check/plan before mutation, reports added/removed/changed/unchanged tool-owned surfaces plus source/target identity, and returns non-success when upgrade is required.",
                "Apply mutates only vendored toolchain-owned files and the toolchain lock, preserves AGENTS.md and semantic .workflow authority, and repeated apply against the same source is idempotent.",
                "STANDARD, STRICT, legacy-v2.1, tamper, Ubuntu, Windows, and pinned max-grounding consumer regressions prove fail-closed behavior and compatibility.",
                "The exact final candidate and post-merge main both pass the complete permanent Governance CI matrix without weakening exact-head, no-ruleset, sequence, performance, documentation, or consumer guarantees.",
            ],
        }
    )
    write(".workflow/roadmap.json", roadmap)

    state = load(".workflow/state.json")
    state["last_accepted_branch"] = "main"
    state["last_accepted_sha"] = BASE
    state["phase"] = "SW2-22"
    state["status"] = "SW2_22_CONSUMER_TOOLCHAIN_PROVENANCE_UPGRADE_RED"
    state["working_branch"] = BRANCH
    state["blockers"] = []
    state["blocked_actions"] = [
        "Do not treat producer commit_hint metadata as acceptance-grade toolchain provenance.",
        "Do not mutate AGENTS.md or project semantic .workflow authority as part of a toolchain upgrade.",
        "Do not claim an upgrade is current when producer source identity is missing, malformed, or mismatched.",
        "Do not claim automatic GitHub merge protection or required-check enforcement while no repository ruleset is configured.",
        "Do not begin SW2-23 or publish a new release unless the Owner explicitly authorizes that separate boundary.",
    ]
    state["next_authorized_actions"] = [
        "Reproduce the accepted SW2-22 RED gap on exact base 65c28fcdfebec68a20adc02ae95406f9261d5a51.",
        "Implement the minimum exact producer-identity and deterministic toolchain upgrade contract required by SW2-22.",
        "Promote no SW2-22 requirement until permanent exact-head evidence proves it.",
    ]
    state.setdefault("not_proven", [])
    for item in [
        "SW2-22 exact producer source identity in consumer toolchain locks is NOT_PROVEN.",
        "SW2-22 deterministic read-only upgrade planning and apply idempotence are NOT_PROVEN.",
        "SW2-22 semantic-authority preservation across consumer upgrades is NOT_PROVEN.",
        "SW2-22 legacy v2.1 and real-consumer compatibility are NOT_PROVEN.",
    ]:
        if item not in state["not_proven"]:
            state["not_proven"].append(item)
    proof = (
        "SW2-22 Consumer Toolchain Provenance & Upgrade Contract is Owner-authorized from exact terminal main "
        "65c28fcdfebec68a20adc02ae95406f9261d5a51; implementation remains RED/NOT_PROVEN until dedicated "
        "regression and permanent CI evidence pass."
    )
    state.setdefault("proven", [])
    if proof not in state["proven"]:
        state["proven"].append(proof)
    write(".workflow/state.json", state)

    acceptance = {
        "schema_version": 1,
        "evidence_boundary": "SW2-22 covers exact producer identity for vendored consumer toolchains and deterministic source-side upgrade planning/apply. It does not add remote auto-update, package-manager infrastructure, release publication, GitHub rulesets, or permission to rewrite Owner semantic authority.",
        "runtime_status": "NOT_APPLICABLE",
        "human_comprehension_status": "NOT_PROVEN",
        "human_comprehension_questions": {},
        "sequence_mode": "DURING",
        "sequence_session": "SW2-22-GOVERNANCE",
        "sequence_sync_status": "NOT_PROVEN",
        "truth_gates": {
            "SOURCE_TESTS": "NOT_PROVEN",
            "RUNTIME_E2E": "NOT_APPLICABLE",
            "PROVENANCE_SYNC": "NOT_PROVEN",
            "REFERENCE_SYNC": "NOT_PROVEN",
            "STRUCTURAL_SYNC": "NOT_PROVEN",
            "SEMANTIC_SYNC": "NOT_PROVEN",
            "BEHAVIORAL_SYNC": "NOT_APPLICABLE",
            "CROSS_DOCUMENT_CONSISTENCY": "NOT_PROVEN",
            "DOC_SOURCE_TRACEABILITY": "NOT_PROVEN",
            "DOC_TEST_TRACEABILITY": "NOT_PROVEN",
            "TEST_RUNTIME_TRACEABILITY": "NOT_APPLICABLE",
            "PROJECT_STATE_SYNC": "NOT_PROVEN",
            "ROADMAP_SYNC": "NOT_PROVEN",
            "PROJECT_DOCS_SYNC": "NOT_PROVEN",
            "DOC_LAYOUT": "NOT_PROVEN",
            "PROJECT_DOCS_NORMALIZED": "NOT_PROVEN",
            "DOC_READABILITY": "NOT_PROVEN",
            "HUMAN_COMPREHENSION": "NOT_PROVEN",
            "SEQUENCE_SYNC": "NOT_PROVEN",
        },
        "requirements": [
            {"id": "SW2-22-R1", "requirement": "Consumer toolchain locks bind vendored bytes to explicit producer repository, exact source SHA, and exact release identity when tagged; missing/malformed/hint-only producer identity fails closed.", "status": "NOT_PROVEN", "evidence": "RED baseline pending."},
            {"id": "SW2-22-R2", "requirement": "A source-side read-only upgrade check produces a deterministic machine-readable plan and reports whether upgrade is required without mutating the consumer.", "status": "NOT_PROVEN", "evidence": "RED baseline pending."},
            {"id": "SW2-22-R3", "requirement": "Upgrade apply mutates only toolchain-owned surfaces, preserves Owner semantic authority, and is idempotent for an already-current consumer.", "status": "NOT_PROVEN", "evidence": "RED baseline pending."},
            {"id": "SW2-22-R4", "requirement": "Legacy v2.1, STANDARD, STRICT, tamper, Ubuntu/Windows, and pinned max-grounding consumer paths retain governance parity under the new provenance/upgrade contract.", "status": "NOT_PROVEN", "evidence": "RED baseline pending."},
            {"id": "SW2-22-R5", "requirement": "Exact final candidate and post-merge main pass the complete six-context permanent Governance CI matrix.", "status": "NOT_PROVEN", "evidence": "No final candidate exists."},
        ],
        "test_commands": [
            "python scripts/selftest_schema_toolchain.py",
            "python scripts/selftest_toolchain_provenance_upgrade.py",
            "python scripts/validate_schema_toolchain.py --root .",
            "python scripts/selftest_adoption_profiles.py",
            "python scripts/selftest_strict_project_workflow.py",
            "python scripts/governance_engine.py --root . --base 65c28fcdfebec68a20adc02ae95406f9261d5a51 --mode finalize --expected-head <EXACT_HEAD>",
        ],
        "runtime_checks": [],
    }
    write(".workflow/acceptance.json", acceptance)

    session = {
        "schema_version": 1,
        "session_id": "SW2-22-GOVERNANCE",
        "phase": "SW2-22",
        "mode": "DURING",
        "scope": "CURRENT",
        "status": "IN_PROGRESS",
        "critical": True,
        "implementation_base_sha": BASE,
        "evidence_boundary": "SW2-22 sequence evidence covers consumer toolchain identity generation/validation, initialization/migration, and governance validation paths. Upgrade implementation is intentionally absent at RED and remains NOT_PROVEN until source and regression evidence exist.",
        "plan": {"required": False, "frozen": False, "contract": "", "diagram": "", "frozen_commit": "", "sha256": ""},
        "actual": {
            "graph": "docs/sequence/generated/SW2-22-GOVERNANCE.actual.json",
            "diagram": "docs/sequence/generated/SW2-22-GOVERNANCE.actual.mmd",
            "entries": [
                "scripts/toolchain_identity.py::producer_metadata",
                "scripts/toolchain_identity.py::write_toolchain_lock",
                "scripts/toolchain_identity.py::validate_toolchain_lock",
                "scripts/initialize_project_truth.py::main",
                "scripts/migrate_governance_v1.py::main",
                "scripts/validate_schema_toolchain.py::main",
            ],
            "source_digest": "",
        },
        "human_view": {
            "graph": "docs/sequence/generated/SW2-22-GOVERNANCE.human.json",
            "diagram": "docs/sequence/generated/SW2-22-GOVERNANCE.human.mmd",
            "document": "docs/sequence/views/SW2-22-GOVERNANCE.md",
            "granularity": "module",
            "policy_id": "module-collapse-v1",
            "source_digest": "",
        },
        "runtime_trace": {"required": False, "graph": ""},
        "test_traceability_required": True,
        "tests": ["scripts/selftest_schema_toolchain.py", "scripts/selftest_toolchain_provenance_upgrade.py"],
        "acceptance_report": "artifacts/sequence/SW2-22-GOVERNANCE.acceptance.json",
    }
    write("docs/sequence/sessions/SW2-22-GOVERNANCE.json", session)


def install_red_test() -> None:
    text = r'''#!/usr/bin/env python3
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
'''
    (ROOT / "scripts" / "selftest_toolchain_provenance_upgrade.py").write_text(text, encoding="utf-8", newline="\n")


def sync_sequence() -> None:
    run(sys.executable, "scripts/sync_project_truth.py", "--root", ".")
    run(
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
    run(
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
    session = load("docs/sequence/sessions/SW2-22-GOVERNANCE.json")
    actual = load(session["actual"]["graph"])
    session["actual"]["source_digest"] = actual["source_digest"]
    session["human_view"]["source_digest"] = actual["source_digest"]
    write("docs/sequence/sessions/SW2-22-GOVERNANCE.json", session)
    run(sys.executable, "scripts/validate_sequence_contract.py", "--root", ".", "--session", "docs/sequence/sessions/SW2-22-GOVERNANCE.json", "--report", "artifacts/sequence/SW2-22-GOVERNANCE.acceptance.json")
    run(sys.executable, "scripts/validate_sequence_human_view.py", "--root", ".", "--session", "docs/sequence/sessions/SW2-22-GOVERNANCE.json")
    run(sys.executable, "scripts/validate_sequence_sessions.py", "--root", ".")
    acceptance = load(".workflow/acceptance.json")
    acceptance["sequence_sync_status"] = "PASS"
    acceptance.setdefault("truth_gates", {})["SEQUENCE_SYNC"] = "PASS"
    write(".workflow/acceptance.json", acceptance)
    run(sys.executable, "scripts/sync_project_truth.py", "--root", ".")


def prove_red() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/selftest_toolchain_provenance_upgrade.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(proc.stdout, end="")
    if proc.returncode == 0:
        raise RuntimeError("SW2_22_RED_EXPECTED_FAILURE_MISSING")
    if "FAIL PRODUCER_SOURCE_SHA_MISSING" not in proc.stdout:
        raise RuntimeError("SW2_22_RED_WRONG_FAILURE")
    print("SW2_22_RED=PASS expected_gap=PRODUCER_SOURCE_SHA_MISSING")


def main() -> int:
    open_authority()
    install_red_test()
    sync_sequence()
    prove_red()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
