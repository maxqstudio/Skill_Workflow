#!/usr/bin/env python3
import json
import os
from pathlib import Path

ACCEPTED = "81b76ccad6785538d898a0fd5767e1b426a2eb56"
BRANCH = "work/sw2-20-documentation-inventory-freshness"


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


roadmap = load(".workflow/roadmap.json")
roadmap["current_phase"] = "SW2-20"
found19 = found20 = False
for phase in roadmap["phases"]:
    if phase.get("id") == "SW2-19":
        phase["status"] = "COMPLETE"
        found19 = True
    elif phase.get("id") == "SW2-20":
        phase["status"] = "CURRENT"
        found20 = True
if not found19:
    raise RuntimeError("SW2_19_ROADMAP_MISSING")
if not found20:
    roadmap["phases"].append({
        "id": "SW2-20",
        "title": "Deterministic Documentation Inventory & Freshness Contract",
        "objective": "Make every tracked documentation surface deterministically discoverable, classified, authority-bound, and freshness-validated so root README/community docs, bundled references, handbook pages, generated projections, templates, and evidence cannot silently escape governance.",
        "status": "CURRENT",
        "exit_criteria": [
            "A deterministic git-tracked documentation inventory discovers every governed documentation surface without relying on a hand-maintained file allowlist; explicit exclusions are machine-readable, justified, and fail closed.",
            "Every discovered documentation file is classified exactly once by role and authority (source-authored public/operating/normative, generated projection, sequence/evidence, template, legal/community, or explicitly excluded); unclassified and multiply-classified files fail.",
            "Every source-authored document has a declared or deterministic path-derived freshness contract; dynamic claims such as current phase, release/version, license, repository enforcement, schema/toolchain, and support state are bound to canonical authority or explicitly marked historical/static.",
            "README.md, AGENTS.md, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, SKILL.md, references/**/*.md, docs/**/*.md, docs/sequence/views/**/*.md, and tracked documentation templates are represented in machine-readable coverage evidence; adding, deleting, moving, or renaming a documentation file without coverage fails.",
            "Regression fixtures reproduce the stale-document classes found by the 2026-10-06 audit (root README release headline, CONTRIBUTING license/protection claims, SECURITY pre-release wording, SW2-09 versioning/release wording, and an omitted handbook architecture page), and the exact final candidate passes the complete permanent matrix.",
        ],
    })
if sum(1 for p in roadmap["phases"] if p.get("status") == "CURRENT") != 1:
    raise RuntimeError("ROADMAP_CURRENT_PHASE_CARDINALITY")
write(".workflow/roadmap.json", roadmap)


defects = load(".workflow/known_defects.json")
if not any(item.get("id") == "SW2-DEF-DOC-003" for item in defects["defects"]):
    defects["defects"].append({
        "id": "SW2-DEF-DOC-003",
        "status": "CONFIRMED",
        "summary": "Documentation governance is not coverage-complete: tracked source-authored documents can contain stale semantic claims while current validators still pass because discovery/freshness coverage is partly hand-maintained and dynamic facts are not uniformly authority-bound.",
        "evidence": "2026-10-06 audit: README.md still names v2.0.0 while accepted authority is v2.1.0; CONTRIBUTING.md still claims no Owner-approved license and default-branch deletion/non-fast-forward enforcement; SECURITY.md still says no stable release exists; docs/handbook/reference/versioning.md says stable V2 publication remains blocked under SW2-09; docs/handbook/reference/release-process.md presents SW2-09/SW2-09-R4 as generic future publication semantics; scripts/validate_public_docs.py uses a hand-maintained REQUIRED_PUBLIC_FILES tuple and omits docs/handbook/architecture/analyzer-contract.md plus root community docs.",
    })
write(".workflow/known_defects.json", defects)

state = load(".workflow/state.json")
state.update({
    "phase": "SW2-20",
    "status": "IN_PROGRESS",
    "working_branch": BRANCH,
    "last_accepted_branch": "main",
    "last_accepted_sha": ACCEPTED,
    "blockers": [],
})
state["blocked_actions"] = [
    "Do not repair stale documentation only by adding more hand-maintained required-file lists.",
    "Do not treat Markdown shape, link validity, or file presence as proof that dynamic documentation claims are current.",
    "Do not let tracked documentation files escape deterministic discovery/classification through implicit exclusions.",
    "Do not rewrite generated Project Truth or historical sequence evidence manually to satisfy documentation freshness.",
    "Do not weaken accepted V2.1 governance, exact-head, cross-platform, consumer, or release guarantees.",
]
state["next_authorized_actions"] = [
    "Build a deterministic git-tracked documentation inventory and exact-one role classifier.",
    "Define machine-readable freshness rules for dynamic claims including current release/version, phase, license, repository enforcement, schema/toolchain, and support state.",
    "Add regressions for every stale-document class captured in SW2-DEF-DOC-003 plus add/delete/move/rename coverage drift.",
    "Repair all confirmed stale source-authored documents through the new coverage/freshness contract, then run the complete exact-head acceptance matrix.",
]
state["not_proven"] = [
    "SW2-20 deterministic discovery and exactly-one classification of every tracked documentation surface are NOT_PROVEN.",
    "SW2-20 dynamic documentation claim freshness against canonical authority is NOT_PROVEN.",
    "SW2-20 fail-closed add/delete/move/rename coverage plus stale-semantic regression is NOT_PROVEN.",
    "SW2-20 complete cross-platform and real-consumer acceptance is NOT_PROVEN.",
    "Automatic GitHub merge protection and required-check enforcement remain intentionally NOT_PROVEN because no repository ruleset is configured; this remains non-blocking.",
]
write(".workflow/state.json", state)

previous = load("docs/sequence/sessions/SW2-19-GOVERNANCE.json")
previous["scope"] = "HISTORICAL"
previous["status"] = "COMPLETE"
write("docs/sequence/sessions/SW2-19-GOVERNANCE.json", previous)

questions = {q: "PASS" for q in [
    "How does failure/recovery behave?",
    "How does important data flow through the system?",
    "What are the important lifecycle states and transitions?",
    "What are the main user/domain workflows?",
    "What are the major components and how do they relate?",
    "What is mutable and what is immutable?",
    "What is proven and what is not proven?",
    "What is the current project state?",
    "What is the project and what problem does it solve?",
    "What may happen next and what is blocked?",
    "Who uses it and what are the primary outcomes?",
    "Who/what is authoritative for important decisions?",
]}
gates = {
    "BEHAVIORAL_SYNC": "NOT_APPLICABLE",
    "CROSS_DOCUMENT_CONSISTENCY": "NOT_PROVEN",
    "DOC_LAYOUT": "PASS",
    "DOC_READABILITY": "NOT_PROVEN",
    "DOC_SOURCE_TRACEABILITY": "NOT_PROVEN",
    "DOC_TEST_TRACEABILITY": "NOT_PROVEN",
    "HUMAN_COMPREHENSION": "PASS",
    "PROJECT_DOCS_NORMALIZED": "PASS",
    "PROJECT_DOCS_SYNC": "PASS",
    "PROJECT_STATE_SYNC": "NOT_PROVEN",
    "PROVENANCE_SYNC": "NOT_PROVEN",
    "REFERENCE_SYNC": "NOT_PROVEN",
    "ROADMAP_SYNC": "PASS",
    "RUNTIME_E2E": "NOT_APPLICABLE",
    "SEMANTIC_SYNC": "NOT_PROVEN",
    "SEQUENCE_SYNC": "NOT_PROVEN",
    "SOURCE_TESTS": "NOT_PROVEN",
    "STRUCTURAL_SYNC": "NOT_PROVEN",
    "TEST_RUNTIME_TRACEABILITY": "NOT_APPLICABLE",
}
acceptance = {
    "evidence_boundary": "SW2-20 covers deterministic discovery, classification, authority binding, freshness validation, and complete machine-readable coverage of tracked documentation surfaces. It must preserve accepted V2.1 Project Truth, sequence, cross-platform, real-consumer, performance, and release guarantees.",
    "human_comprehension_questions": questions,
    "human_comprehension_status": "PASS",
    "requirements": [
        {"id": "SW2-20-R1", "requirement": "Every tracked documentation surface is deterministically discovered and classified exactly once without a hand-maintained complete-file allowlist.", "status": "NOT_PROVEN", "evidence": "NOT_PROVEN until tracked-file inventory, role classification, explicit exclusion semantics, and add/delete/move/rename regressions pass."},
        {"id": "SW2-20-R2", "requirement": "Dynamic claims in source-authored documentation are deterministically bound to canonical authority or explicitly classified historical/static.", "status": "NOT_PROVEN", "evidence": "NOT_PROVEN until phase, release/version, license, repository enforcement, schema/toolchain, and support-state freshness rules reject stale semantics."},
        {"id": "SW2-20-R3", "requirement": "Machine-readable documentation coverage evidence proves no tracked document is silently omitted and reproduces all confirmed stale-document classes from SW2-DEF-DOC-003.", "status": "NOT_PROVEN", "evidence": "NOT_PROVEN until coverage evidence plus stale README, CONTRIBUTING, SECURITY, versioning/release, and missing-handbook-page regressions pass."},
        {"id": "SW2-20-R4", "requirement": "All confirmed stale documentation is repaired through the new contract and the exact final candidate passes the permanent Ubuntu/Windows/sequence/engine/consumer acceptance matrix.", "status": "NOT_PROVEN", "evidence": "NOT_PROVEN until final exact-head permanent acceptance is green after complete documentation coverage/freshness repair."},
    ],
    "runtime_checks": [],
    "runtime_status": "NOT_APPLICABLE",
    "schema_version": 1,
    "sequence_mode": "DURING",
    "sequence_session": "SW2-20-GOVERNANCE",
    "sequence_sync_status": "NOT_PROVEN",
    "test_commands": [
        "python scripts/selftest_public_docs.py",
        "python scripts/selftest_repository_health.py",
        "python scripts/selftest_cross_document_regressions.py",
        "python scripts/validate_public_docs.py --root .",
        "python scripts/validate_project_docs.py --root .",
        "python scripts/validate_sequence_sessions.py --root .",
        "python scripts/governance_engine.py --root . --base 81b76ccad6785538d898a0fd5767e1b426a2eb56 --mode finalize --expected-head <EXACT_HEAD>",
    ],
    "truth_gates": gates,
}
write(".workflow/acceptance.json", acceptance)

session = {
    "acceptance_report": "artifacts/sequence/SW2-20-GOVERNANCE.acceptance.json",
    "actual": {
        "diagram": "docs/sequence/generated/SW2-20-GOVERNANCE.actual.mmd",
        "entries": [
            "scripts/governance_engine.py::main",
            "scripts/sync_project_truth.py::main",
            "scripts/validate_project_docs.py::main",
            "scripts/validate_public_docs.py::main",
            "scripts/validate_repository_health.py::main",
            "scripts/validate_cross_document_consistency.py::main",
            "scripts/validate_sequence_sessions.py::main",
        ],
        "graph": "docs/sequence/generated/SW2-20-GOVERNANCE.actual.json",
        "source_digest": "",
    },
    "critical": True,
    "evidence_boundary": "SW2-20 baseline sequence covers the existing documentation/governance validation pipeline before deterministic documentation inventory/freshness implementation. Static pipeline evidence does not prove coverage completeness or semantic freshness until SW2-20 requirements pass.",
    "human_view": {
        "diagram": "docs/sequence/generated/SW2-20-GOVERNANCE.human.mmd",
        "document": "docs/sequence/views/SW2-20-GOVERNANCE.md",
        "granularity": "module",
        "graph": "docs/sequence/generated/SW2-20-GOVERNANCE.human.json",
        "policy_id": "module-collapse-v1",
        "source_digest": "",
    },
    "implementation_base_sha": ACCEPTED,
    "mode": "DURING",
    "phase": "SW2-20",
    "plan": {"contract": "", "diagram": "", "frozen": False, "frozen_commit": "", "required": False, "sha256": ""},
    "runtime_trace": {"graph": "", "required": False},
    "schema_version": 1,
    "scope": "CURRENT",
    "session_id": "SW2-20-GOVERNANCE",
    "status": "IN_PROGRESS",
    "test_traceability_required": True,
    "tests": ["scripts/selftest_public_docs.py", "scripts/selftest_repository_health.py", "scripts/selftest_cross_document_regressions.py"],
}
write("docs/sequence/sessions/SW2-20-GOVERNANCE.json", session)
print("SW2_20_AUTHORITY_OPEN=PASS")
