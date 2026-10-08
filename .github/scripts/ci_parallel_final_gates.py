#!/usr/bin/env python3
"""Complete producer STRICT and read-only VERIFY gates concurrently on Windows.

These two gates operate on isolated temporary fixtures versus the unchanged
checked-out source. Both execute in full; no result cache or short circuit.
The entire source HEAD and governed worktree are verified before/after.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SHA=re.compile(r"^[0-9a-f]{40}$")
GATES=("verify_read_only","strict_workflow_selftest")
STATUS_PATHS=("PROJECT_PROFILE.yaml",".workflow","docs","artifacts/sequence","scripts")
TIMEOUT_SECONDS=240


def git(root:Path,*args:str)->tuple[int,str]:
    proc=subprocess.run(["git","-C",str(root),*args],text=True,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
    return proc.returncode,proc.stdout.strip()


def require_exact_clean(root:Path,expected:str)->None:
    rc,head=git(root,"rev-parse","HEAD")
    if rc or head!=expected:
        raise ValueError("WINDOWS_FINAL_HEAD_MISMATCH:"+head)
    rc,dirty=git(root,"status","--porcelain","--untracked-files=all",
                 "--",*STATUS_PATHS)
    if rc or dirty:
        raise ValueError("WINDOWS_FINAL_GOVERNED_STATE_DIRTY:"+dirty[:300])


def authority(root:Path)->tuple[str,str]:
    acceptance=root/".workflow"/"state.json"
    if not acceptance.is_file():
        raise ValueError("WINDOWS_FINAL_STATE_MISSING")
    state=json.loads(acceptance.read_text(encoding="utf-8"))
    base=str(state.get("last_accepted_sha","")).strip()
    _,head=git(root,"rev-parse","HEAD")
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise ValueError("WINDOWS_FINAL_BASE_OR_HEAD_INVALID")
    rc,_=git(root,"merge-base","--is-ancestor",base,head)
    if rc:
        raise ValueError("WINDOWS_FINAL_BASE_NOT_ANCESTOR")
    require_exact_clean(root,head)
    return base,head


def commands(root:Path,base:str,head:str)->tuple[tuple[str,list[str]],...]:
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise ValueError("WINDOWS_FINAL_SHA_INVALID")
    for script in ("governance_engine.py","selftest_strict_project_workflow.py"):
        if not (root/"scripts"/script).is_file():
            raise ValueError("WINDOWS_FINAL_REQUIRED_SCRIPT_MISSING:"+script)
    return (
       (GATES[0],[sys.executable,"scripts/governance_engine.py",
                   "--root",".","--base",base,"--mode","verify","--expected-head",head]),
       (GATES[1],[sys.executable,"scripts/selftest_strict_project_workflow.py"])
    )


def run_one(name:str,cmd:list[str],root:Path,runner=None)->dict:
    started=time.monotonic()
    try:
        if runner is None:
            env=os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"]="1"
            proc=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,check=False,timeout=TIMEOUT_SECONDS,env=env)
            rc,out=proc.returncode,proc.stdout
        else:
            rc,out=runner(name,cmd,root)
        return {"gate":name,"result":"PASS" if rc==0 else "FAIL",
            "exit_code":rc,"seconds":round(time.monotonic()-started,3),
            "output_tail":out[-6000:]}
    except Exception as exc:
        return {"gate":name,"result":"FAIL","exit_code":1,
            "seconds":round(time.monotonic()-started,3),
            "output_tail":type(exc).__name__+":"+str(exc)}


def run(root:Path,runner=None)->dict:
    root=root.resolve()
    report={"schema_version":1,"result":"FAIL","first_failed_gate":"",
        "expected_gates":2,"executed_gates":0,"gates":[],
        "evidence_boundary":"Both full producer verify/STRICT gates executed against one pinned clean HEAD; independent temporary fixtures, no skipped checks or cached acceptance. Windows-only overlap; Ubuntu remains serial."}
    try:
        base,head=authority(root)
        report.update({"expected_head":head,"base":base})
        planned=commands(root,base,head)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(run_one,name,cmd,root,runner) for name,cmd in planned]
            results=[future.result() for future in futures]
        report["gates"]=results
        report["executed_gates"]=len(results)
        failure=next((item["gate"] for item in results if item["result"]!="PASS"),"")
        if failure:
            report["first_failed_gate"]=failure
            return report
        require_exact_clean(root,head)
        report["result"]="PASS"
    except Exception as exc:
        report["first_failed_gate"]=type(exc).__name__+":"+str(exc)
    return report


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    report=run(Path(args.root))
    for item in report["gates"]:
        print("WINDOWS_FINAL_GATE="+json.dumps(item,sort_keys=True),flush=True)
    print("WINDOWS_FINAL_JSON="+json.dumps(report,sort_keys=True,separators=(",",":")),flush=True)
    if report["result"]=="PASS" and report["executed_gates"]==2:
        print("WINDOWS_STRICT_AND_VERIFY_BOTH_PASS=PASS")
        return 0
    print("FIRST_FAILED_GATE="+(report["first_failed_gate"] or "WINDOWS_FINAL_INCOMPLETE"))
    return 1


if __name__=="__main__":
    raise SystemExit(main())
