#!/usr/bin/env python3
"""Temporary SW2-23 governed evidence sync. Does not promote acceptance statuses."""
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(".")
def cmd(*args):
    print("+ "+" ".join(str(a) for a in args),flush=True)
    subprocess.run([str(a) for a in args],check=True)
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def save(p,obj):Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")

session_file="docs/sequence/sessions/SW2-23-GOVERNANCE.json"
session=load(session_file)
assert session["scope"]=="CURRENT" and session["phase"]=="SW2-23"
actual=session["actual"]
command=[sys.executable,"scripts/generate_sequence_actual.py","--root",".","--output-json",actual["graph"],"--output-mermaid",actual["diagram"]]
for name in actual["entries"]:command.extend(["--entry",name])
cmd(*command)
human=session["human_view"]
cmd(sys.executable,"scripts/sequence_human_view.py","--root",".",
    "--actual-json",actual["graph"],"--actual-mermaid",actual["diagram"],
    "--output-json",human["graph"],"--output-mermaid",human["diagram"],
    "--output-markdown",human["document"],"--session-id",session["session_id"])
digest=load(actual["graph"])["source_digest"]
session["actual"]["source_digest"]=digest
session["human_view"]["source_digest"]=digest
save(session_file,session)
cmd(sys.executable,"scripts/validate_sequence_contract.py","--root",".",
    "--session",session_file,"--report",session["acceptance_report"])
cmd(sys.executable,"scripts/validate_sequence_human_view.py","--root",".","--session",session_file)
cmd(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
cmd(sys.executable,"scripts/sync_project_truth.py","--root",".")
cmd("git","add",".workflow","docs","artifacts/sequence")
cmd(sys.executable,"scripts/validate_documentation_contract.py","--root",".","--write-report")
cmd("git","add",".workflow/generated/documentation_coverage.json")
cmd("git","diff","--cached","--stat")
result=subprocess.run(["git","diff","--cached","--quiet"])
if result.returncode != 0:
    cmd("git","commit","-m","SW2-23: synchronize source, sequence, Project Truth and document inventory")
cmd(sys.executable,"scripts/selftest_documentation_contract.py")
cmd(sys.executable,"scripts/selftest_consumer_compatibility_matrix.py")
cmd(sys.executable,"scripts/validate_sequence_contract.py","--root",".",
    "--session",session_file,"--no-write-report")
cmd(sys.executable,"scripts/validate_sequence_sessions.py","--root",".")
cmd(sys.executable,"scripts/validate_documentation_contract.py","--root",".")
cmd(sys.executable,"scripts/validate_closure_defect_lifecycle.py","--root",".",
    "--expected-base","f6a1e417c2f8b5adb73273c4cba4768771f8bb66")
cmd(sys.executable,"scripts/validate_project_docs.py","--root",".")
cmd("git","diff","--exit-code","--",".workflow","docs","scripts","artifacts/sequence")
cmd("git","push","origin","HEAD:work/sw2-23-multi-consumer-adoption")
print("SW2_23_INTERMEDIATE_SYNC=PASS",flush=True)
