#!/usr/bin/env python3
"""SW2-24 Windows exact-HEAD combined exhaustive CI orchestration.

Overlaps the complete audited 19 source-regression commands with the two
complete STRICT/VERIFY gates. Every group is blocking, even if a peer fails.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import time
from pathlib import Path

import ci_parallel_selftests as independent
import ci_parallel_final_gates as final

EXPECTED_GROUPS=len(independent.GROUPS)
EXPECTED_COMMANDS=sum(len(cmds) for _,cmds in independent.GROUPS)
EXPECTED_FINAL_GATES=len(final.GATES)


def run(root:Path, groups_runner=None, final_runner=None)->dict:
    root=root.resolve()
    result={"schema_version":1,"result":"FAIL","first_failed_gate":"",
            "independent_groups":0,"independent_commands":0,
            "complete_final_gates":0,"parallel_regressions":None,"parallel_final":None,
            "expected_groups":EXPECTED_GROUPS,"expected_commands":EXPECTED_COMMANDS,
            "expected_final_gates":EXPECTED_FINAL_GATES,
            "evidence_boundary":"Full independent regressions and complete STRICT/VERIFY execute concurrently on the same clean exact Git head. All required tests, including all error paths, remain blocking. No cached PASS, no external consumer mutation."}
    started=time.monotonic()
    try:
        base,head=final.authority(root)
        result.update({"source_head":head,"accepted_base":base})
        # Verify command inventory before any acceptance execution.
        planned=final.commands(root,base,head)
        if tuple(name for name,_ in planned)!=final.GATES:
            raise ValueError("COMBINED_FINAL_GATE_INVENTORY_MISMATCH")
        if EXPECTED_GROUPS!=15 or EXPECTED_COMMANDS!=19 or EXPECTED_FINAL_GATES!=2:
            raise ValueError("COMBINED_REQUIRED_COMMAND_COUNT_MISMATCH")
        for _,specs in independent.GROUPS:
            independent.commands_for_group(root,specs)
        def regressions():
            return independent.run_groups(root,workers=independent.MAX_WORKERS,
                                           runner=groups_runner or independent.subprocess_runner)
        def finality():
            return final.run(root,runner=final_runner)
        # Both futures are always submitted; neither can cancel the other.
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            left=pool.submit(regressions)
            right=pool.submit(finality)
            errors={}
            try:
                regress=left.result()
            except BaseException as exc:
                errors["independent_regressions"]=type(exc).__name__+":"+str(exc)
                regress=None
            try:
                finals=right.result()
            except BaseException as exc:
                errors["complete_final_gates"]=type(exc).__name__+":"+str(exc)
                finals=None
        result["parallel_regressions"]=regress
        result["parallel_final"]=finals
        result["independent_groups"]=regress.get("executed_groups",0) if regress else 0
        result["independent_commands"]=regress.get("executed_commands",0) if regress else 0
        result["complete_final_gates"]=finals.get("executed_gates",0) if finals else 0
        if errors:
            result["first_failed_gate"]="COMBINED_RUNNER_EXCEPTION:"+json.dumps(errors,sort_keys=True)
            return result
        if regress["result"]!="PASS":
            result["first_failed_gate"]="independent_regressions:"+regress.get("first_failed_gate","UNSPECIFIED")
            return result
        if finals["result"]!="PASS":
            result["first_failed_gate"]="complete_final_gates:"+finals.get("first_failed_gate","UNSPECIFIED")
            return result
        if (result["independent_groups"]!=EXPECTED_GROUPS or
            result["independent_commands"]!=EXPECTED_COMMANDS or
            result["complete_final_gates"]!=EXPECTED_FINAL_GATES):
            result["first_failed_gate"]="COMBINED_TEST_INVENTORY_INCOMPLETE"
            return result
        # If even a passing subrunner mutated source, fail this exact-head gate.
        final.require_exact_clean(root,head)
        result["result"]="PASS"
    except Exception as exc:
        result["first_failed_gate"]=type(exc).__name__+":"+str(exc)
    finally:
        result["seconds"]=round(time.monotonic()-started,3)
    return result


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    evidence=run(Path(args.root))
    for label in ("parallel_regressions","parallel_final"):
        info=evidence.get(label)
        if info:
            print("WINDOWS_COMBINED_SECTION="+json.dumps({"section":label,"result":info.get("result"),
                "first_failed_gate":info.get("first_failed_gate"),
                "executed_commands":info.get("executed_commands"),
                "executed_gates":info.get("executed_gates")},sort_keys=True),flush=True)
    print("WINDOWS_COMBINED_JSON="+json.dumps(evidence,sort_keys=True,separators=(",",":")),flush=True)
    if (evidence["result"]=="PASS" and evidence["independent_commands"]==EXPECTED_COMMANDS
        and evidence["complete_final_gates"]==EXPECTED_FINAL_GATES):
        print("WINDOWS_ALL_19_REGRESSIONS_AND_BOTH_FINAL_GATES=PASS")
        return 0
    print("FIRST_FAILED_GATE="+(evidence["first_failed_gate"] or "COMBINED_INCOMPLETE"))
    return 1


if __name__=="__main__":
    raise SystemExit(main())
