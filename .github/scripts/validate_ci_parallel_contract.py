#!/usr/bin/env python3
"""Static SW2-24 policy ensuring parallelism cannot erase Windows regressions."""
from __future__ import annotations
from pathlib import Path
import ci_parallel_selftests as parallel
import ci_parallel_final_gates as final_gates

WINDOWS_STEP = "Windows bounded independent regression matrix"
SELFTEST_STEP = "CI parallel regression contract self-test"
GUARD_LINUX = "if: matrix.os != 'windows-latest'"
GUARD_WINDOWS = "if: matrix.os == 'windows-latest'"
SERIAL_STEPS = {
    "consumer_finalize": ("Consumer finalize negative-path regression",
                          ("python scripts/selftest_consumer_finalize.py",)),
    "schema_toolchain": ("Schema and toolchain version regression",
                         ("python scripts/selftest_schema_toolchain.py",
                          "python scripts/validate_schema_toolchain.py --root .")),
    "analyzer_contract": ("Cross-language analyzer contract regression",
                          ("python scripts/selftest_analyzer_contract.py",)),
    "historical_evidence": ("Historical evidence freeze regression",
                            ("python scripts/selftest_historical_evidence.py",)),
    "public_docs": ("Public documentation regression",
                    ("python scripts/selftest_public_docs.py",
                     "python scripts/selftest_generated_doc_presentation.py",
                     "python scripts/validate_public_docs.py --root .")),
    "release_preflight": ("Release preflight regression",
                          ("python scripts/selftest_release_preflight.py",)),
    "project_truth_compiler": ("Project Truth Compiler self-test",
                               ("python scripts/selftest_project_truth_compiler.py",)),
}
WINDOWS_FINAL_STEP = "Windows concurrent full STRICT and read-only VERIFY"
FINAL_SELFTEST_STEP = "Windows complete final gates negative-path regression"
FINAL_SERIAL_STEPS = {
    "Verify mode is read-only": "python scripts/governance_engine.py --root . --base ",
    "STRICT workflow self-test": "python scripts/selftest_strict_project_workflow.py",
}
CONTEXT_NAMES = ("Self Governance (ubuntu-latest)",
    "SW2 Sequence Evidence (ubuntu-latest)",
    "Governance Engine Performance (ubuntu-latest)",
    "Consumer Engine Performance (max-grounding)")


def steps_from_workflow(workflow: str) -> dict[str, str]:
    import re
    if "  governance-selftest:\n" not in workflow or "  sequence-evidence:\n" not in workflow:
        raise ValueError("CI_PARALLEL_GOVERNANCE_MATRIX_SCOPE_MISSING")
    block=workflow.split("  governance-selftest:\n",1)[1].split("  sequence-evidence:\n",1)[0]
    segments = re.split(r"(?m)^      - name: ", block)
    result={}
    for segment in segments[1:]:
        first,sep,rest=segment.partition("\n")
        if first in result:
            raise ValueError("CI_PARALLEL_DUPLICATE_STEP:"+first)
        result[first]=rest
    return result


def findings(workflow: str) -> list[str]:
    problems=[]
    steps=steps_from_workflow(workflow)
    for name in CONTEXT_NAMES:
        if workflow.count("name: "+name)!=1:
            problems.append("CI_REQUIRED_CONTEXT_CHANGED:"+name)
    if workflow.count("Governance Selftest (")==0:
        problems.append("CI_SELFTEST_MATRIX_CONTEXT_MISSING")
    if "        os:\n          - ubuntu-latest\n          - windows-latest" not in workflow:
        problems.append("CI_PARALLEL_PLATFORM_MATRIX_CHANGED")
    if tuple(SERIAL_STEPS)!=parallel.GROUP_NAMES:
        problems.append("CI_PARALLEL_GROUP_INVENTORY_CHANGED")
    if not all(step in steps for step in (WINDOWS_STEP,SELFTEST_STEP)):
        problems.append("CI_PARALLEL_STEP_MISSING")
    else:
        windows=steps[WINDOWS_STEP]
        if GUARD_WINDOWS not in windows or (
            "python .github/scripts/ci_parallel_selftests.py --root . --workers 3" not in windows
        ):
            problems.append("CI_PARALLEL_WINDOWS_BOUNDARY_WEAKENED")
        if "python .github/scripts/selftest_ci_parallel_selftests.py" not in steps[SELFTEST_STEP]:
            problems.append("CI_PARALLEL_SELFTEST_MISSING")
    for name,(stepname,commands) in SERIAL_STEPS.items():
        if stepname not in steps:
            problems.append("CI_REQUIRED_SERIAL_STEP_MISSING:"+stepname)
            continue
        body=steps[stepname]
        if GUARD_LINUX not in body:
            problems.append("CI_UBUNTU_SERIAL_FALLBACK_MISSING:"+stepname)
        for cmd in commands:
            if cmd not in body:
                problems.append("CI_SERIAL_COMMAND_MISSING:"+name+":"+cmd)
        specs=dict(parallel.GROUPS).get(name)
        if specs is None or tuple("python "+item for item in specs)!=commands:
            problems.append("CI_WINDOWS_INVENTORY_NOT_EQUAL_UBUNTU:"+name)
    if final_gates.GATES!=("verify_read_only","strict_workflow_selftest"):
        problems.append("CI_WINDOWS_FINAL_GATE_SET_CHANGED")
    for mandatory,command in FINAL_SERIAL_STEPS.items():
        if mandatory not in steps or GUARD_LINUX not in steps.get(mandatory,""):
            problems.append("CI_UBUNTU_FINAL_GATE_FALLBACK_MISSING:"+mandatory)
        elif command not in steps[mandatory]:
            problems.append("CI_UBUNTU_FINAL_GATE_COMMAND_MISSING:"+mandatory)
    # Windows runs the same two complete gates in one bounded independent process.
    if WINDOWS_FINAL_STEP not in steps or FINAL_SELFTEST_STEP not in steps:
        problems.append("CI_WINDOWS_FINAL_OR_REGRESSION_MISSING")
    else:
        body=steps[WINDOWS_FINAL_STEP]
        if GUARD_WINDOWS not in body or (
            "python .github/scripts/ci_parallel_final_gates.py --root ." not in body
        ):
            problems.append("CI_WINDOWS_FINAL_BOUNDARY_WEAKENED")
        if "python .github/scripts/selftest_ci_parallel_final_gates.py" not in steps[FINAL_SELFTEST_STEP]:
            problems.append("CI_WINDOWS_FINAL_NEGATIVE_TEST_MISSING")
    return problems


def main()->int:
    root=Path(__file__).resolve().parents[2]
    p=root/".github"/"workflows"/"governance-ci.yml"
    try:
        values=findings(p.read_text(encoding="utf-8"))
    except Exception as exc:
        values=["CI_PARALLEL_INVALID_WORKFLOW:"+str(exc)]
    for item in values:
        print("FAIL "+item)
    if values:
        return 1
    print("CI_PARALLEL_EXACT_INVENTORY=PASS")
    print("CI_PARALLEL_LINUX_FALLBACK=PASS")
    print("CI_PARALLEL_WINDOWS_BOUND=PASS")
    print("CI_PARALLEL_STRICT_AND_VERIFY_BOTH_EXECUTED=PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
