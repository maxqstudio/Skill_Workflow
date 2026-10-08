#!/usr/bin/env python3
"""Temporary, single-purpose SW2-23 phase-opening transaction (GitHub Actions only)."""
import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(".").resolve()
BASE="f6a1e417c2f8b5adb73273c4cba4768771f8bb66"
BRANCH="work/sw2-23-multi-consumer-adoption"
def cmd(*a):
    print("+", " ".join(map(str,a)),flush=True)
    subprocess.run(list(map(str,a)),cwd=ROOT,check=True)
def obj(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def save(path,data):
    target=ROOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def git(*a):
    return subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()

assert git("rev-parse","HEAD")==git("rev-parse","HEAD")
assert git("merge-base",BASE,"HEAD")==BASE
road=obj(".workflow/roadmap.json")
assert road["current_phase"]=="SW2-22"
assert road["phases"][-1]["id"]=="SW2-22" and road["phases"][-1]["status"]=="CURRENT"
road["phases"][-1]["status"]="COMPLETE"
road["phases"].append({
    "id":"SW2-23",
    "title":"Multi-Consumer Compatibility & Adoption Contract",
    "objective":"Prove representative real-consumer adoption, deterministic provenance-aware toolchain upgrades, explicit unsupported-consumer rejection, and fail-closed evidence without mutating external consumer repositories or weakening governance.",
    "status":"CURRENT",
    "exit_criteria":[
        "At least three real consumer snapshots are pinned by exact SHA and independently classified by governance/profile/toolchain compatibility, with read-only source provenance.",
        "Legacy/unsupported consumers are rejected with an exact first failed gate; missing AGENTS.md, missing locks, and legacy hint-only locks must not become a false compatibility PASS.",
        "Compatible isolated consumer fixtures prove deterministic check-plan-apply-validate-finalize behavior, strict Owner semantic authority preservation and idempotence.",
        "Git checkout and copied/package toolchain identity paths preserve content equivalence; tamper/unsupported schema/interrupted upgrade negative paths fail closed without partial semantic mutation.",
        "Cross-platform and representative consumer evidence record actual measured CI time and cost/budget changes; any gating optimization preserves complete final acceptance.",
        "Source-authored public documentation consistently describes SW2-22 GIT+CONTENT/CONTENT provenance and a regression rejects stale provenance-hint-only assertions.",
        "Complete permanent exact-head Governance CI six-context matrix passes on feature candidate and post-merge main, with truthful evidence and separate closure transaction."
    ]
})
road["current_phase"]="SW2-23"
save(".workflow/roadmap.json",road)

state=obj(".workflow/state.json")
assert state["phase"]=="SW2-22"
state["phase"]="SW2-23"
state["status"]="SW2_23_CONSUMER_BASELINE_IN_PROGRESS"
state["last_accepted_branch"]="main"
state["last_accepted_sha"]=BASE
state["working_branch"]=BRANCH
state["blockers"]=[]
state["not_proven"]=[
    "SW2-23 R1-R7 are NOT_PROVEN pending exact pinned consumer compatibility and permanent CI evidence.",
    "DoctorCode has legacy hint-only producer provenance at pinned main; max-grounding and max-remote-commander have no supported root AGENTS.md / toolchain lock at their pinned main snapshots; unsupported paths must fail closed.",
    "Automatic GitHub merge protection and required checks remain intentionally NOT_PROVEN under Owner-approved no-ruleset boundary."
]
state["next_authorized_actions"]=[
    "Reproduce the stale provenance-hint-only public reference with a failing documentation regression before repair.",
    "Audit exact pinned consumers read-only; simulate upgrades in isolated copies only and classify unsupported governance.",
    "Measure CI latency and execute full exact-head acceptance before promotion; keep PR draft until every required gate passes."
]
state["blocked_actions"]=[
    "Do not modify actual consumer repositories during SW2-23 compatibility evaluation.",
    "Do not treat missing AGENTS.md/toolchain lock or legacy hint-only provenance as compatibility PASS.",
    "Do not weaken finalize, exact-head, fail-closed, sequence, or required cross-platform acceptance.",
    "Do not claim platform-required checks with no GitHub ruleset.",
    "Do not begin SW2-24 or release a new stable tag without separate Owner authorization."
]
save(".workflow/state.json",state)

old=obj("docs/sequence/sessions/SW2-22-GOVERNANCE.json")
assert old["scope"]=="CURRENT" and old["status"]=="COMPLETE"
old["scope"]="HISTORICAL"
save("docs/sequence/sessions/SW2-22-GOVERNANCE.json",old)
new=copy.deepcopy(old)
new.update({"phase":"SW2-23","session_id":"SW2-23-GOVERNANCE","scope":"CURRENT",
    "status":"IN_PROGRESS","implementation_base_sha":BASE,
    "evidence_boundary":"Static sequence evidence maps consumer classification/upgrade and documentation freshness paths; it does not prove remote consumer compatibility, runtime behavior, or an authorized external repository mutation."})
new["actual"]={"graph":"docs/sequence/generated/SW2-23-GOVERNANCE.actual.json",
    "diagram":"docs/sequence/generated/SW2-23-GOVERNANCE.actual.mmd",
    "entries":["scripts/upgrade_governance_toolchain.py::build_plan",
        "scripts/upgrade_governance_toolchain.py::main",
        "scripts/toolchain_identity.py::validate_toolchain_lock",
        "scripts/validate_documentation_contract.py::freshness_findings"],
    "source_digest":""}
new["human_view"]={"graph":"docs/sequence/generated/SW2-23-GOVERNANCE.human.json",
    "diagram":"docs/sequence/generated/SW2-23-GOVERNANCE.human.mmd",
    "document":"docs/sequence/views/SW2-23-GOVERNANCE.md",
    "granularity":"module","policy_id":"module-collapse-v1","source_digest":""}
new["acceptance_report"]="artifacts/sequence/SW2-23-GOVERNANCE.acceptance.json"
new["plan"]={"contract":"","diagram":"","frozen":False,"frozen_commit":"","required":False,"sha256":""}
new["runtime_trace"]={"graph":"","required":False}
new["tests"]=["scripts/selftest_toolchain_provenance_upgrade.py","scripts/selftest_documentation_contract.py"]
save("docs/sequence/sessions/SW2-23-GOVERNANCE.json",new)

prior=obj(".workflow/acceptance.json")
gates={key:("NOT_APPLICABLE" if val=="NOT_APPLICABLE" else "NOT_PROVEN") for key,val in prior["truth_gates"].items()}
acceptance={
    "schema_version":1,"sequence_mode":"DURING","sequence_session":"SW2-23-GOVERNANCE",
    "sequence_sync_status":"NOT_PROVEN","runtime_status":"NOT_APPLICABLE","runtime_checks":[],
    "evidence_boundary":"Phase open only. All SW2-23 consumer, negative-path, latency, documentation and final CI requirements are NOT_PROVEN until individually executed. Read-only pinned consumer audit does not equal adoption PASS.",
    "human_comprehension_status":"NOT_PROVEN",
    "human_comprehension_questions":{k:"NOT_PROVEN" for k in prior.get("human_comprehension_questions",{})},
    "test_commands":["python scripts/selftest_toolchain_provenance_upgrade.py",
        "python scripts/selftest_documentation_contract.py",
        "python scripts/validate_schema_toolchain.py --root .",
        "python scripts/validate_sequence_sessions.py --root ."],
    "truth_gates":gates,
    "requirements":[{
      "id":f"SW2-23-R{i}","status":"NOT_PROVEN","evidence":"NOT_PROVEN: phase-open only; no SW2-23 final evidence.",
      "requirement":description} for i,description in enumerate([
        "Freeze at least three genuinely different real consumer SHA snapshots and classify their exact compatibility/preconditions without consumer repository mutation.",
        "Reject incompatible/legacy consumer snapshots with explicit first failed gates; never fabricate successful adoption.",
        "Execute isolated supported consumer check-plan-apply-validate-finalize and test semantic preservation and idempotence.",
        "Cover GIT+CONTENT and CONTENT package copies plus tamper, unsupported schema, and interrupted-upgrade negative paths.",
        "Record reproducible CI timing/cost evidence without weakening final acceptance or silently skipping unknown impact.",
        "Repair provenance-hint-only public documentation and add regression that detects this stale contract claim.",
        "Exact final feature candidate and post-merge main pass all six permanent GitHub Governance CI contexts."
    ],1)]
}
save(".workflow/acceptance.json",acceptance)

matrix={
    "schema_version":1,
    "authority":"GitHub main commit snapshots verified at SW2-23 phase opening; fixture only, no external writes",
    "source_main_sha":BASE,
    "consumer_snapshots":[
       {"repository":"maxqstudio/max-grounding","sha":"4c45a23c48b7954bbfb0ab86bcc92c975f345a1f","profile":"strict","root_agents":"MISSING","toolchain_lock":"MISSING","classification":"LEGACY_PRECONDITIONS_MISSING","acceptance":"NOT_PROVEN"},
       {"repository":"maxqstudio/DoctorCode","sha":"bc3846e6d5c412ebe09146a66661d2c49072889b","profile":"strict","root_agents":"PRESENT","toolchain_lock":"LEGACY_HINT_ONLY","classification":"EXPLICIT_MIGRATION_REQUIRED","acceptance":"NOT_PROVEN"},
       {"repository":"maxqstudio/max-remote-commander","sha":"b968b023c322cc22dc804c5bbcb9370aee5f9ae1","profile":"strict","root_agents":"MISSING","toolchain_lock":"MISSING","classification":"LEGACY_PRECONDITIONS_MISSING","acceptance":"NOT_PROVEN"}
    ],
    "preconditions":{
       "consumer_repository_mutation":"DENIED",
       "test_checkout":"ISOLATED_ONLY",
       "owner_semantics":"IMMUTABLE",
       "unsupported":"FAIL_CLOSED",
       "exact_sha":"REQUIRED"
    }
}
save(".workflow/consumer_compatibility_matrix.json",matrix)

cmd("git","add",".workflow/roadmap.json",".workflow/state.json",".workflow/acceptance.json",
  ".workflow/consumer_compatibility_matrix.json","docs/sequence/sessions/SW2-22-GOVERNANCE.json",
  "docs/sequence/sessions/SW2-23-GOVERNANCE.json")
cmd("git","commit","-m","SW2-23: open governed consumer compatibility authority")
anchor=git("rev-parse","HEAD")
print("SW2_23_ANCHOR="+anchor,flush=True)
cmd(sys.executable,"scripts/validate_sequence_sessions.py","--root",".","--freeze-historical",
    "--frozen-commit",anchor,"--authorize-migration","SW2-23 phase-open freezes previously accepted SW2-22 sequence evidence")

sesspath=ROOT/"docs/sequence/sessions/SW2-23-GOVERNANCE.json"
sess=obj("docs/sequence/sessions/SW2-23-GOVERNANCE.json")
actual=sess["actual"]
generate=[sys.executable,"scripts/generate_sequence_actual.py","--root",".",
          "--output-json",actual["graph"],"--output-mermaid",actual["diagram"]]
for entry in actual["entries"]:generate.extend(["--entry",entry])
cmd(*generate)
human=sess["human_view"]
cmd(sys.executable,"scripts/sequence_human_view.py","--root",".",
    "--actual-json",actual["graph"],"--actual-mermaid",actual["diagram"],
    "--output-json",human["graph"],"--output-mermaid",human["diagram"],
    "--output-markdown",human["document"],"--session-id",sess["session_id"])
facts=obj(actual["graph"])
sess["actual"]["source_digest"]=facts["source_digest"]
sess["human_view"]["source_digest"]=facts["source_digest"]
save("docs/sequence/sessions/SW2-23-GOVERNANCE.json",sess)
cmd(sys.executable,"scripts/validate_sequence_contract.py","--root",".","--session",
    "docs/sequence/sessions/SW2-23-GOVERNANCE.json",
    "--report","artifacts/sequence/SW2-23-GOVERNANCE.acceptance.json")
cmd(sys.executable,"scripts/validate_sequence_human_view.py","--root",".","--session","docs/sequence/sessions/SW2-23-GOVERNANCE.json")
cmd(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
cmd(sys.executable,"scripts/sync_project_truth.py","--root",".")
cmd(sys.executable,"scripts/validate_documentation_contract.py","--root",".","--write-report")
cmd("git","add",".workflow","docs","artifacts/sequence")
cmd("git","diff","--cached","--stat")
cmd("git","commit","-m","SW2-23: synchronize phase opening Project Truth and historical freeze")
cmd(sys.executable,"scripts/validate_sequence_contract.py","--root",".","--session","docs/sequence/sessions/SW2-23-GOVERNANCE.json","--no-write-report")
cmd(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
print("SW2_23_PHASE_OPEN_HUMAN_COMPREHENSION=NOT_PROVEN (terminal gate deferred; no false PASS)",flush=True)
cmd(sys.executable,"scripts/validate_closure_defect_lifecycle.py","--root",".","--expected-base",BASE)
cmd(sys.executable,"scripts/validate_documentation_contract.py","--root",".")
cmd(sys.executable,"scripts/validate_project_docs.py","--root",".")
cmd("git","diff","--exit-code","--",".workflow","docs","artifacts/sequence")
cmd("git","push","origin","HEAD:"+BRANCH)
print("SW2_23_PHASE_OPEN=PASS",flush=True)
