#!/usr/bin/env python3
"""SW2-24 negative acceptance for concurrent 19+2 Windows gates."""
from __future__ import annotations
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
import ci_parallel_windows as combined
import ci_parallel_selftests as independent
import ci_parallel_final_gates as final

def git(root:Path,*args:str)->str:
    return subprocess.check_output(["git","-C",str(root),*args],text=True,stderr=subprocess.STDOUT).strip()

def put(root:Path,name:str,body:str)->None:
    p=root/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(body,encoding="utf-8",newline="\n")

def commit(root:Path)->str:
    git(root,"add","-A")
    git(root,"commit","-m","fixture")
    return git(root,"rev-parse","HEAD")

def main()->int:
    assert len(independent.GROUPS)==15
    assert combined.EXPECTED_COMMANDS==19
    assert combined.EXPECTED_FINAL_GATES==2
    with tempfile.TemporaryDirectory(prefix="sw2-24-full-windows-") as td:
        root=Path(td)
        git(root,"init")
        git(root,"config","user.name","SW2-24")
        git(root,"config","user.email","sw2@example.invalid")
        for _,specs in independent.GROUPS:
            for spec in specs:
                put(root,spec.split()[0],"print('fixture')\n")
        for name in ("governance_engine.py","selftest_strict_project_workflow.py"):
            put(root,"scripts/"+name,"print('fixture')\n")
        base=commit(root)
        put(root,".workflow/state.json",'{"last_accepted_sha":"'+base+'"}\n')
        commit(root)
        lock=threading.Lock()
        active=[0]
        peak=[0]
        observed=[]
        def entered(name):
            with lock:
                active[0]+=1
                peak[0]=max(peak[0],active[0])
                observed.append(name)
            time.sleep(.055)
            with lock:
                active[0]-=1
        def group_pass(argv,where):
            entered("group:"+Path(argv[1]).name)
            return 0,"fixture PASS"
        def final_pass(name,argv,where):
            entered("final:"+name)
            return 0,"fixture PASS"
        ok=combined.run(root,groups_runner=group_pass,final_runner=final_pass)
        assert ok["result"]=="PASS",ok
        assert ok["independent_groups"]==15 and ok["independent_commands"]==19
        assert ok["complete_final_gates"]==2
        assert len(observed)==21 and peak[0]>=3,peak
        print("CI_ALL_21_EXACT_GATES_OVERLAP_AND_EXECUTE=PASS")
        observed.clear()
        def regression_failure(argv,where):
            entered("group:"+Path(argv[1]).name)
            return (9 if Path(argv[1]).name=="selftest_schema_toolchain.py" else 0),"fixture"
        negative=combined.run(root,groups_runner=regression_failure,final_runner=final_pass)
        assert negative["result"]=="FAIL" and negative["first_failed_gate"].startswith("independent_regressions:schema_toolchain:"),negative
        assert negative["complete_final_gates"]==2
        assert negative["independent_groups"]==15
        print("CI_REGRESSION_FAILURE_CANNOT_SKIP_FINAL_GATES=PASS")
        observed.clear()
        def final_failure(name,argv,where):
            entered("final:"+name)
            return (7 if name=="verify_read_only" else 0),"fixture"
        negative=combined.run(root,groups_runner=group_pass,final_runner=final_failure)
        assert negative["result"]=="FAIL" and negative["first_failed_gate"]=="complete_final_gates:verify_read_only",negative
        assert negative["independent_commands"]==19
        print("CI_FINAL_FAILURE_CANNOT_SKIP_REGRESSIONS=PASS")
        observed.clear()
        def mutating_group(argv,where):
            if Path(argv[1]).name=="selftest_schema_toolchain.py":
                put(root,".workflow/mutated.txt","DIRTY")
            return 0,"fixture"
        negative=combined.run(root,groups_runner=mutating_group,final_runner=final_pass)
        assert negative["result"]=="FAIL" and "WINDOWS_FINAL_GOVERNED_STATE_DIRTY" in negative["first_failed_gate"],negative
        (root/".workflow/mutated.txt").unlink()
        print("CI_COMBINED_DIRTY_WORKTREE_REJECTED=PASS")
        (root/"scripts/selftest_release_preflight.py").unlink()
        negative=combined.run(root,groups_runner=group_pass,final_runner=final_pass)
        assert negative["result"]=="FAIL" and "CI_PARALLEL_SCRIPT_MISSING_OR_ESCAPE" in negative["first_failed_gate"],negative
        print("CI_COMBINED_MISSING_SCRIPT_REJECTED=PASS")
    print("CI_COMBINED_FAIL_CLOSED=PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
