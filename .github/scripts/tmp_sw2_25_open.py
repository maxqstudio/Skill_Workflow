#!/usr/bin/env python3
"""Temporary exact-main SW2-25 governance phase-opening transaction."""
import json, subprocess, sys
from pathlib import Path

BASE="91b58b98049a7d27ed65169508177ea7dc978ca1"
BRANCH="work/sw2-25-reproducible-release-bundle"
def run(*cmd):
    print("+"," ".join(map(str,cmd)),flush=True)
    subprocess.run([str(x) for x in cmd],check=True)
def git(*args):
    return subprocess.check_output(["git",*args],text=True).strip()
def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def save(path,value):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")

assert git("merge-base",BASE,"HEAD")==BASE
road=read(".workflow/roadmap.json")
assert road["current_phase"]=="SW2-24"
assert road["phases"][-1]["id"]=="SW2-24" and road["phases"][-1]["status"]=="CURRENT"
road["phases"][-1]["status"]="COMPLETE"
road["current_phase"]="SW2-25"
criteria=[
"An exact-commit manifest records a deterministic product-only distribution allowlist, SHA-256 for every included file, stable ZIP digest, toolchain content identity and truthful Git-source versus copied-package provenance without treating self-asserted metadata as a cryptographic signature.",
"A clean exact-SHA checkout builds the same canonical bundle bytes on repeated runs, and a second clean isolated checkout on another OS verifies identical SHA-256; timestamps, file ordering, executable modes and generated contents are normalized.",
"Packaging rejects unsafe tracked paths, secrets/credentials, symlinks or submodules, untracked/extraneous archive entries, dirty working trees, missing mandatory product files, stale manifests, and unknown unsupported file modes with deterministic first failed gates.",
"Detached verification validates the archive against an independent supplied manifest, rejecting payload tampering, corruption, swapped manifests, identity mismatches, duplicate entries, path traversal, missing/extra files and wrong canonical metadata; verification never grants release/publication authority.",
"Release preflight and public handbook document read-only distribution dry-run boundaries; permanent CI exercises actual bundle build/verify and fail-closed regressions across Ubuntu and Windows, preserving the existing six contexts with no extra release or tag.",
"An exact helper-free final feature candidate passes all six permanent Governance CI contexts, squash merges with identical tree, and passes full six-context postmerge main before terminal closure; no release or distribution publication happens without separate Owner authority."
]
road["phases"].append({"id":"SW2-25","title":"Reproducible Release Bundle & Integrity Verification","status":"CURRENT","objective":"Build deterministic, content-addressed, independently verifiable consumer distribution artifacts and release dry-run evidence while preserving fail-closed GitHub acceptance and forbidding unauthorized publication.","exit_criteria":criteria})
save(".workflow/roadmap.json",road)
s=read(".workflow/state.json")
assert s["phase"]=="SW2-24" and s["status"]=="SW2_24_CI_LATENCY_COST_OPTIMIZATION_ACCEPTED"
s["phase"]="SW2-25"
s["status"]="SW2_25_REPRODUCIBLE_BUNDLE_IN_PROGRESS"
s["working_branch"]=BRANCH
s["last_accepted_branch"]="main"
s["last_accepted_sha"]=BASE
s["blockers"]=["SW2-25 R1-R6 NOT_PROVEN pending implementation and exact evidence."]
s["not_proven"]=["SW2-25 bundle determinism, cross-platform parity, independent integrity verification, packaging safety and final six-context acceptance are NOT_PROVEN.","Published stable release remains v2.1.0; no new release/tag authorized and no asset publication granted.","Automated GitHub required-status enforcement intentionally remains NOT_PROVEN under Owner decision."]
s["blocked_actions"]=["Do not publish a Git tag, GitHub release or external artifact to a distribution channel.","Do not weaken six permanent CI contexts, strict/verify, Windows/Ubuntu, consumer, performance, Mermaid or documentation gates.","Do not mutate owner devices or external consumer repositories.","Do not open SW2-26 without explicit Owner authorization."]
s["next_authorized_actions"]=["Implement dry-run deterministic bundle with exact-SHA and detached integrity verification, negative-path fixtures, and per-OS permanent CI evidence.","Synchronize public product docs, source-generated sequence, acceptance and documentation inventory.","Keep PR DRAFT and R6 NOT_PROVEN until candidate and post-merge main 6/6; use separate terminal closure."]
save(".workflow/state.json",s)
q=read("docs/sequence/sessions/SW2-24-GOVERNANCE.json")
assert q["status"]=="COMPLETE" and q["scope"]=="CURRENT"
q["scope"]="HISTORICAL"
save("docs/sequence/sessions/SW2-24-GOVERNANCE.json",q)
new={
"schema_version":1,"session_id":"SW2-25-GOVERNANCE","phase":"SW2-25",
"mode":"DURING","status":"IN_PROGRESS","scope":"CURRENT","critical":True,
"implementation_base_sha":BASE,
"evidence_boundary":"Static graph covers release preflight/provenance and bundle generation when implemented; runtime CI and byte parity require separately executed evidence. This phase does not grant stable publication.",
"plan":{"required":False,"contract":"","diagram":"","sha256":"","frozen":False,"frozen_commit":""},
"actual":{"graph":"docs/sequence/generated/SW2-25-GOVERNANCE.actual.json","diagram":"docs/sequence/generated/SW2-25-GOVERNANCE.actual.mmd","entries":["scripts/release_preflight.py::validate","scripts/toolchain_identity.py::producer_metadata"],"source_digest":""},
"human_view":{"graph":"docs/sequence/generated/SW2-25-GOVERNANCE.human.json","diagram":"docs/sequence/generated/SW2-25-GOVERNANCE.human.mmd","document":"docs/sequence/views/SW2-25-GOVERNANCE.md","granularity":"module","policy_id":"module-collapse-v1","source_digest":""},
"runtime_trace":{"required":False,"graph":""},"test_traceability_required":True,"tests":["scripts/selftest_release_preflight.py"],"acceptance_report":"artifacts/sequence/SW2-25-GOVERNANCE.acceptance.json"}
save("docs/sequence/sessions/SW2-25-GOVERNANCE.json",new)
old=read(".workflow/acceptance.json")
g={k:("NOT_APPLICABLE" if v=="NOT_APPLICABLE" else "NOT_PROVEN") for k,v in old["truth_gates"].items()}
for name in ("DOC_LAYOUT","DOC_READABILITY","PROJECT_DOCS_NORMALIZED","PROJECT_DOCS_SYNC","ROADMAP_SYNC"):g[name]="PASS"
a={
"schema_version":1,"sequence_mode":"DURING","sequence_session":"SW2-25-GOVERNANCE","sequence_sync_status":"NOT_PROVEN",
"runtime_status":"NOT_APPLICABLE","runtime_checks":[],
"evidence_boundary":"Phase-open only; no deterministic package, independent integrity proof, new stable publication or release authority.",
"human_comprehension_status":"NOT_PROVEN",
"human_comprehension_questions":{k:"NOT_PROVEN" for k in old["human_comprehension_questions"]},
"test_commands":["python scripts/selftest_release_preflight.py","python scripts/validate_schema_toolchain.py --root .","python scripts/validate_sequence_sessions.py --root ."],
"truth_gates":g,
"requirements":[{"id":f"SW2-25-R{i}","status":"NOT_PROVEN","requirement":item,"evidence":"NOT_PROVEN: SW2-25 phase-open only."} for i,item in enumerate(criteria,1)]}
save(".workflow/acceptance.json",a)
run("git","add",".workflow/roadmap.json",".workflow/state.json",".workflow/acceptance.json","docs/sequence/sessions/SW2-24-GOVERNANCE.json","docs/sequence/sessions/SW2-25-GOVERNANCE.json")
run("git","commit","-m","SW2-25: open exact-main reproducible distribution acceptance boundary")
anchor=git("rev-parse","HEAD")
run(sys.executable,"scripts/validate_sequence_sessions.py","--root",".","--freeze-historical","--frozen-commit",anchor,"--authorize-migration","SW2-25 phase open freezes accepted SW2-24")
ses=read("docs/sequence/sessions/SW2-25-GOVERNANCE.json")
ac=ses["actual"]
cmd=[sys.executable,"scripts/generate_sequence_actual.py","--root",".","--output-json",ac["graph"],"--output-mermaid",ac["diagram"]]
for entry in ac["entries"]:cmd.extend(["--entry",entry])
run(*cmd)
hv=ses["human_view"]
run(sys.executable,"scripts/sequence_human_view.py","--root",".","--actual-json",ac["graph"],"--actual-mermaid",ac["diagram"],"--output-json",hv["graph"],"--output-mermaid",hv["diagram"],"--output-markdown",hv["document"],"--session-id",ses["session_id"])
digest=read(ac["graph"])["source_digest"]
ses["actual"]["source_digest"]=digest
ses["human_view"]["source_digest"]=digest
save("docs/sequence/sessions/SW2-25-GOVERNANCE.json",ses)
run(sys.executable,"scripts/validate_sequence_contract.py","--root",".","--session","docs/sequence/sessions/SW2-25-GOVERNANCE.json","--report",ses["acceptance_report"])
run(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
run(sys.executable,"scripts/sync_project_truth.py","--root",".")
run("git","add",".workflow","docs","artifacts/sequence")
run(sys.executable,"scripts/validate_documentation_contract.py","--root",".","--write-report")
run("git","add",".workflow/generated/documentation_coverage.json")
run("git","commit","-m","SW2-25: freeze historical SW2-24 and synchronize phase-open Project Truth")
run(sys.executable,"scripts/validate_sequence_contract.py","--root",".","--session","docs/sequence/sessions/SW2-25-GOVERNANCE.json","--no-write-report")
run(sys.executable,"scripts/validate_documentation_contract.py","--root",".")
run(sys.executable,"scripts/validate_project_docs.py","--root",".")
run("git","push","origin","HEAD:"+BRANCH)
print("SW2_25_PHASE_OPEN=PASS")
