#!/usr/bin/env python3
"""Bounded and fail-closed independent Windows CI selftest orchestration.

Fixed, versioned commands; zero auto-discovery, zero shell execution, and no
skipped tests on failure. Only explicitly audited temp-fixture selftests run
concurrently; full STRICT/verify, producer finalize and consumer source tests stay
in their original permanent CI steps.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

MAX_WORKERS=3
GROUPS=(
  ("consumer_finalize", ("scripts/selftest_consumer_finalize.py",)),
  ("schema_toolchain", ("scripts/selftest_schema_toolchain.py", "scripts/validate_schema_toolchain.py --root .")),
  ("analyzer_contract", ("scripts/selftest_analyzer_contract.py",)),
  ("historical_evidence", ("scripts/selftest_historical_evidence.py",)),
  ("public_docs", ("scripts/selftest_public_docs.py", "scripts/selftest_generated_doc_presentation.py", "scripts/validate_public_docs.py --root .")),
  ("release_preflight", ("scripts/selftest_release_preflight.py",)),
  ("project_truth_compiler", ("scripts/selftest_project_truth_compiler.py",)),
  ("engine_regression", ("scripts/selftest_governance_engine.py",)),
  ("sequence_call_resolution", ("scripts/selftest_sequence_call_resolution.py",)),
  ("sequence_squash_provenance", ("scripts/selftest_sequence_squash_provenance.py",)),
  ("sequence_human_view", ("scripts/selftest_sequence_human_view.py",)),
  ("repository_health", ("scripts/selftest_repository_health.py", "scripts/validate_repository_health.py --root .")),
  ("ruleset_policy", ("scripts/selftest_github_ruleset.py",)),
  ("cross_document", ("scripts/selftest_cross_document_regressions.py",)),
  ("adoption_profiles", ("scripts/selftest_adoption_profiles.py",)),
)
GROUP_NAMES=tuple(name for name, _ in GROUPS)
PASS_MARKER="CI_PARALLEL_SELFTESTS_ALL_REQUIRED=PASS"


@dataclass(frozen=True)
class Result:
    gate:str
    status:str
    exit_code:int
    commands_executed:int
    expected_commands:int
    seconds:float
    output:str
    first_failed_command:str


def commands_for_group(root:Path, scripts:tuple[str,...])->list[list[str]]:
    output=[]
    for spec in scripts:
        # Static command specs only. No shell metacharacters, path traversal or flags.
        parts=spec.split()
        if not parts or not parts[0].startswith("scripts/") or not parts[0].endswith(".py"):
            raise ValueError("CI_PARALLEL_UNSAFE_SCRIPT_SPEC:"+spec)
        if any("/../" in part or part.startswith("/") or part in ("&&","||",";","|") for part in parts):
            raise ValueError("CI_PARALLEL_UNSAFE_ARGUMENT_SPEC:"+spec)
        path=root/parts[0]
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError("CI_PARALLEL_SCRIPT_MISSING_OR_ESCAPE:"+parts[0])
        output.append([sys.executable,*parts])
    return output


def subprocess_runner(argv:list[str],root:Path)->tuple[int,str]:
    env=os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"]="1"
    completed=subprocess.run(argv,cwd=root,env=env,text=True,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
    return completed.returncode,completed.stdout


def run_one(root:Path,name:str,scripts:tuple[str,...],
            runner:Callable[[list[str],Path],tuple[int,str]])->Result:
    started=time.monotonic()
    execution=0
    output=[]
    first_failed=""
    try:
        commands=commands_for_group(root,scripts)
        for argv in commands:
            rc,payload=runner(argv,root)
            execution+=1
            output.append(payload[-8000:])
            if rc!=0:
                # No next command in a FAILED group may be silently counted as PASS.
                first_failed=" ".join(argv[1:])
                return Result(name,"FAIL",rc,execution,len(commands),
                    round(time.monotonic()-started,3),"\n".join(output),first_failed)
        return Result(name,"PASS",0,execution,len(commands),
                      round(time.monotonic()-started,3),"\n".join(output),"")
    except Exception as exc:
        return Result(name,"FAIL",1,execution,len(scripts),
            round(time.monotonic()-started,3),
            "RUNNER_EXCEPTION:"+type(exc).__name__+":"+str(exc),first_failed or "PRECONDITION")


def run_groups(root:Path,groups=GROUPS,workers:int=MAX_WORKERS,
               runner=subprocess_runner)->dict:
    root=root.resolve()
    names=[name for name,_ in groups]
    if not groups or len(names)!=len(set(names)) or workers<1 or workers>MAX_WORKERS:
        return {"result":"FAIL","first_failed_gate":"CI_PARALLEL_INVALID_GROUPS_OR_WORKERS",
                "gates":[],"expected_groups":len(groups),"executed_groups":0}
    start=time.monotonic()
    # All fixed gates are submitted. No fail-fast cancellation, regardless of completion order.
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures={name:executor.submit(run_one,root,name,scripts,runner)
                 for name,scripts in groups}
        observed={name:future.result() for name,future in futures.items()}
    ordered=[observed[name] for name in names]
    first=next((item.gate+":"+item.first_failed_command
        for item in ordered if item.status!="PASS"),"")
    return {
        "schema_version":1,"result":"FAIL" if first else "PASS",
        "first_failed_gate":first,
        "expected_groups":len(groups),"executed_groups":len(ordered),
        "expected_commands":sum(len(scripts) for _,scripts in groups),
        "executed_commands":sum(item.commands_executed for item in ordered),
        "workers":workers,"seconds":round(time.monotonic()-start,3),
        "gates":[{"gate":item.gate,"status":item.status,"exit_code":item.exit_code,
            "seconds":item.seconds,"commands_executed":item.commands_executed,
            "expected_commands":item.expected_commands,
            "first_failed_command":item.first_failed_command,
            "output_tail":item.output[-8000:]} for item in ordered],
        "evidence_boundary":"Every fixed temp-fixture regression ran; each gate's result is authoritative only for the executed commands. Original serial finalization and consumer acceptance remain required in permanent CI.",
    }


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    parser.add_argument("--workers",type=int,default=MAX_WORKERS)
    args=parser.parse_args()
    report=run_groups(Path(args.root),workers=args.workers)
    for item in report["gates"]:
        print("CI_PARALLEL_GATE="+json.dumps(item,sort_keys=True),flush=True)
    print("CI_PARALLEL_RESULT_JSON="+json.dumps(report,sort_keys=True,separators=(",",":")),flush=True)
    if report["result"]=="PASS" and report["executed_commands"]==report["expected_commands"]:
        print(PASS_MARKER)
        return 0
    print("FIRST_FAILED_GATE="+(report["first_failed_gate"] or "CI_PARALLEL_INCOMPLETE"))
    return 1


if __name__=="__main__":
    raise SystemExit(main())
