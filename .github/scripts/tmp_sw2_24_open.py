#!/usr/bin/env python3
"""Temporary SW2-24 phase-open authority transaction, no product changes."""
import copy
import json
import subprocess
import sys
from pathlib import Path

BASE="e5bbd9e485380cda962656e7ce8a5477cfce0e68"
BRANCH="work/sw2-24-ci-latency-cost-optimization"
def run(*args):
    print("+", " ".join(map(str,args)),flush=True)
    subprocess.run(list(map(str,args)),check=True)
def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def save(path,obj):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def git(*args):
    return subprocess.check_output(["git",*args],text=True).strip()

assert git("merge-base",BASE,"HEAD")==BASE
road=load(".workflow/roadmap.json")
assert road["current_phase"]=="SW2-23" and road["phases"][-1]["status"]=="CURRENT"
road["phases"][-1]["status"]="COMPLETE"
road["current_phase"]="SW2-24"
criteria=[
    "A traceable exact-SHA baseline records durations of all six permanent CI contexts, per-step critical path, and both observed wall time and aggregate job-seconds over at least three completed prior successful runs.",
    "Independent self-test groups are specified conservatively; their complete original test inventory remains mandatory and any conflicts or unknown independence fail closed to serial execution rather than dropping tests.",
    "Bounded parallel self-test orchestration is deterministic, runs each selected command exactly once, captures explicit first failed gate and full failed command evidence, rejects missing/racy/mutating tests, and preserves six permanent contexts, STRICT, verify, finalize, Windows, Mermaid, performance and consumer gates.",
    "Before and after measurements use exact GitHub Actions runs with a cold/warm distinction; measured speed and job-seconds are reported without unproven cost or statistically causal claims, and no significant observed performance regression is silently accepted.",
    "Authoritative public documentation, roadmap, source-derived sequence and human-view Mermaid remain consistent and readable; changes are backed by negative regressions, including false skipping/cache laundering.",
    "Final exact helper-free feature candidate passes six permanent checks, is squash-merged with exact tree identity, and passes six permanent postmerge main checks before terminal accepted closure."
]
road["phases"].append({
    "id":"SW2-24","title":"CI Latency & Cost Optimization",
    "objective":"Reduce unnecessary critical-path latency in the existing six-context GitHub Governance CI through evidence-based bounded parallelism and setup reuse while preserving exhaustive, exact-SHA, fail-closed acceptance on Windows and Ubuntu, without adding billable permanent contexts.",
    "status":"CURRENT","exit_criteria":criteria
})
save(".workflow/roadmap.json",road)
state=load(".workflow/state.json")
assert state["phase"]=="SW2-23" and state["status"]=="SW2_23_MULTI_CONSUMER_COMPATIBILITY_ACCEPTED"
state["phase"]="SW2-24"
state["status"]="SW2_24_CI_BASELINE_IN_PROGRESS"
state["working_branch"]=BRANCH
state["last_accepted_branch"]="main"
state["last_accepted_sha"]=BASE
state["blockers"]=[]
state["not_proven"]=[
    "SW2-24 R1-R6 are NOT_PROVEN pending measured exact-run baseline, regression, and feature/main acceptance.",
    "Any wall-clock or billed-minutes savings is NOT_PROVEN until comparable samples exist; previous observed 56-94 second Windows durations are variable.",
    "Owner-approved absence of automatic GitHub required checks/ruleset remains NOT_PROVEN and non-blocking."
]
state["blocked_actions"]=[
    "Do not remove, weaken or mark NOT_APPLICABLE any six permanent final contexts, Windows or Ubuntu regressions, Mermaid renderer, consumer finalization, or performance baseline.",
    "Do not parallelize dependent or source-mutating gates or reuse cached PASS authority.",
    "Do not mutate actual consumer repositories, publish release, or modify GitHub ruleset.",
    "Do not begin SW2-25 until Owner authorizes it."
]
state["next_authorized_actions"]=[
    "Record exact baseline and RED negative-path tests for parallel-runner failure/skip/mutation boundaries.",
    "Optimize only test groups with isolated workspace and independence evidence, measuring warm and cold runs.",
    "Reconcile Project Truth/sequence then require final six-context exact candidate and postmerge main before closure."
]
save(".workflow/state.json",state)
old=load("docs/sequence/sessions/SW2-23-GOVERNANCE.json")
assert old["status"]=="COMPLETE" and old["scope"]=="CURRENT"
old["scope"]="HISTORICAL"
save("docs/sequence/sessions/SW2-23-GOVERNANCE.json",old)
new={
    "schema_version":1,"session_id":"SW2-24-GOVERNANCE","phase":"SW2-24","mode":"DURING",
    "status":"IN_PROGRESS","scope":"CURRENT","critical":True,
    "implementation_base_sha":BASE,
    "evidence_boundary":"Static source graph describes CI applicability, governance DAG and performance measurement; it does not prove actual parallel scheduling speed, cross-run performance, external bill charges, or GitHub-side required check enforcement.",
    "plan":{"required":False,"contract":"","diagram":"","sha256":"","frozen":False,"frozen_commit":""},
    "actual":{"graph":"docs/sequence/generated/SW2-24-GOVERNANCE.actual.json",
              "diagram":"docs/sequence/generated/SW2-24-GOVERNANCE.actual.mmd",
              "entries":["scripts/governance_engine.py::planned_node_names",
                         "scripts/benchmark_governance.py::main",
                         "scripts/selftest_performance_budget.py::main"],
              "source_digest":""},
    "human_view":{"graph":"docs/sequence/generated/SW2-24-GOVERNANCE.human.json",
        "diagram":"docs/sequence/generated/SW2-24-GOVERNANCE.human.mmd",
        "document":"docs/sequence/views/SW2-24-GOVERNANCE.md",
        "granularity":"module","policy_id":"module-collapse-v1","source_digest":""},
    "runtime_trace":{"required":False,"graph":""},
    "test_traceability_required":True,
    "tests":["scripts/selftest_governance_engine.py","scripts/selftest_performance_budget.py"],
    "acceptance_report":"artifacts/sequence/SW2-24-GOVERNANCE.acceptance.json"
}
save("docs/sequence/sessions/SW2-24-GOVERNANCE.json",new)
old_accept=load(".workflow/acceptance.json")
gates={name:("NOT_APPLICABLE" if status=="NOT_APPLICABLE" else "NOT_PROVEN") for name,status in old_accept["truth_gates"].items()}
for name in ("DOC_LAYOUT","DOC_READABILITY","PROJECT_DOCS_NORMALIZED","PROJECT_DOCS_SYNC","ROADMAP_SYNC"):
    gates[name]="PASS"
acceptance={
    "schema_version":1,"sequence_mode":"DURING","sequence_session":"SW2-24-GOVERNANCE",
    "sequence_sync_status":"NOT_PROVEN","runtime_status":"NOT_APPLICABLE","runtime_checks":[],
    "evidence_boundary":"Phase-open boundary only; no SW2-24 performance improvement, concurrency safety, exact final CI, or merge is proven.",
    "human_comprehension_status":"NOT_PROVEN",
    "human_comprehension_questions":{k:"NOT_PROVEN" for k in old_accept["human_comprehension_questions"]},
    "test_commands":["python scripts/selftest_governance_engine.py",
                     "python scripts/selftest_performance_budget.py",
                     "python scripts/validate_schema_toolchain.py --root .",
                     "python scripts/validate_sequence_sessions.py --root ."],
    "truth_gates":gates,
    "requirements":[{
        "id":f"SW2-24-R{i}","status":"NOT_PROVEN",
        "requirement":item,
        "evidence":"NOT_PROVEN: SW2-24 phase-open only, no final evidence."
    } for i,item in enumerate(criteria,1)]
}
save(".workflow/acceptance.json",acceptance)
run("git","add",".workflow/roadmap.json",".workflow/state.json",".workflow/acceptance.json",
    "docs/sequence/sessions/SW2-23-GOVERNANCE.json",
    "docs/sequence/sessions/SW2-24-GOVERNANCE.json")
run("git","commit","-m","SW2-24: open exact-baseline CI optimization acceptance authority")
anchor=git("rev-parse","HEAD")
run(sys.executable,"scripts/validate_sequence_sessions.py","--root",".",
    "--freeze-historical","--frozen-commit",anchor,
    "--authorize-migration","SW2-24 phase-open freezes previously accepted SW2-23 static sequence evidence")
session=load("docs/sequence/sessions/SW2-24-GOVERNANCE.json")
actual=session["actual"]
command=[sys.executable,"scripts/generate_sequence_actual.py","--root",".",
         "--output-json",actual["graph"],"--output-mermaid",actual["diagram"]]
for entry in actual["entries"]:
    command.extend(["--entry",entry])
run(*command)
human=session["human_view"]
run(sys.executable,"scripts/sequence_human_view.py","--root",".",
    "--actual-json",actual["graph"],"--actual-mermaid",actual["diagram"],
    "--output-json",human["graph"],"--output-mermaid",human["diagram"],
    "--output-markdown",human["document"],"--session-id",session["session_id"])
digest=load(actual["graph"])["source_digest"]
session["actual"]["source_digest"]=digest
session["human_view"]["source_digest"]=digest
save("docs/sequence/sessions/SW2-24-GOVERNANCE.json",session)
run(sys.executable,"scripts/validate_sequence_contract.py","--root",".",
    "--session","docs/sequence/sessions/SW2-24-GOVERNANCE.json",
    "--report",session["acceptance_report"])
run(sys.executable,"scripts/validate_sequence_human_view.py","--root",".",
    "--session","docs/sequence/sessions/SW2-24-GOVERNANCE.json")
run(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
run(sys.executable,"scripts/sync_project_truth.py","--root",".")
run("git","add",".workflow","docs","artifacts/sequence")
run(sys.executable,"scripts/validate_documentation_contract.py","--root",".","--write-report")
run("git","add",".workflow/generated/documentation_coverage.json")
run("git","diff","--cached","--stat")
run("git","commit","-m","SW2-24: freeze historical SW2-23 and synchronize phase-open Project Truth")
run(sys.executable,"scripts/validate_sequence_contract.py","--root",".",
    "--session","docs/sequence/sessions/SW2-24-GOVERNANCE.json","--no-write-report")
run(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
run(sys.executable,"scripts/validate_documentation_contract.py","--root",".")
run(sys.executable,"scripts/validate_closure_defect_lifecycle.py","--root",".","--expected-base",BASE)
run(sys.executable,"scripts/validate_project_docs.py","--root",".")
run("git","diff","--exit-code","--",".workflow","docs","artifacts/sequence")
run("git","push","origin","HEAD:"+BRANCH)
print("SW2_24_PHASE_OPEN=PASS",flush=True)
