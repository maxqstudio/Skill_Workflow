#!/usr/bin/env python3
"""Adversarial evidence that Windows STRICT and VERIFY concurrency is not a bypass."""
from __future__ import annotations
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import ci_parallel_final_gates as final

def git(root:Path,*args:str)->str:
    proc=subprocess.run(["git","-C",str(root),*args],check=True,
                        text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return proc.stdout.strip()

def write(root:Path,path:str,text:str)->None:
    target=root/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text,encoding="utf-8",newline="\n")

def commit(root:Path)->str:
    git(root,"add","-A")
    git(root,"commit","-m","fixture")
    return git(root,"rev-parse","HEAD")

def fixture(root:Path)->tuple[str,str]:
    git(root,"init")
    git(root,"config","user.name","SW2-24 fixture")
    git(root,"config","user.email","sw2@example.invalid")
    write(root,"scripts/governance_engine.py","print('fixture')\n")
    write(root,"scripts/selftest_strict_project_workflow.py","print('fixture')\n")
    write(root,"README.md","# fixture\n")
    base=commit(root)
    write(root,".workflow/state.json",'{ "last_accepted_sha": "'+base+'" }\n')
    head=commit(root)
    return base,head

def main()->int:
    with tempfile.TemporaryDirectory(prefix="sw2-24-final-gates-") as td:
        root=Path(td)
        base,head=fixture(root)
        active=[0]
        maximum=[0]
        executed=[]
        lock=threading.Lock()
        def success(name,cmd,workdir):
            with lock:
                active[0]+=1
                maximum[0]=max(maximum[0],active[0])
                executed.append(name)
            time.sleep(.04)
            with lock:
                active[0]-=1
            return 0,"PASS synthetic"
        report=final.run(root,runner=success)
        assert report["result"]=="PASS",report
        assert report["executed_gates"]==2
        assert [x["gate"] for x in report["gates"]]==list(final.GATES)
        assert maximum[0]==2,"gates did not overlap in test fixture"
        assert len(executed)==2
        print("WINDOWS_FINAL_BOTH_GATES_EXECUTED=PASS")
        print("WINDOWS_FINAL_BOUNDED_INDEPENDENT_OVERLAP=PASS")

        for fail_name in final.GATES:
            invoked=[]
            def failure(name,cmd,workdir):
                invoked.append(name)
                return (5 if name==fail_name else 0),"negative"
            bad=final.run(root,runner=failure)
            assert bad["result"]=="FAIL" and bad["first_failed_gate"]==fail_name,bad
            assert bad["executed_gates"]==2 and len(invoked)==2
        print("WINDOWS_FINAL_FAILURE_NOT_SKIPPED=PASS")

        def mutation(name,cmd,workdir):
            if name=="strict_workflow_selftest":
                write(workdir,".workflow/dirty.txt","unexpected\n")
            return 0,"synthetic"
        changed=final.run(root,runner=mutation)
        assert changed["result"]=="FAIL",changed
        assert "WINDOWS_FINAL_GOVERNED_STATE_DIRTY" in changed["first_failed_gate"]
        (root/".workflow/dirty.txt").unlink()
        print("WINDOWS_FINAL_SOURCE_MUTATION_REJECTED=PASS")

        (root/"scripts/governance_engine.py").unlink()
        new_head=commit(root)
        absent=final.run(root,runner=success)
        assert absent["result"]=="FAIL" and "WINDOWS_FINAL_REQUIRED_SCRIPT_MISSING" in absent["first_failed_gate"],absent
        print("WINDOWS_FINAL_MISSING_GATE_REJECTED=PASS")
    print("RESULT=PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
