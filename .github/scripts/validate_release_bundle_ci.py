#!/usr/bin/env python3
"""Fail-closed static contract for producer release-bundle CI (SW2-25)."""
from __future__ import annotations
from pathlib import Path

STEPS=(
    ("Release bundle content-integrity regressions",
     "python .github/scripts/selftest_release_bundle.py"),
    ("Build and detached-verify exact-head read-only bundle",
     "python .github/scripts/release_bundle.py build"),
)
PIN="$" + "{{ github.event.pull_request.head.sha || github.sha }}"
DISPATCH_PIN="$" + "{{ inputs.candidate_sha || github.sha }}"


def findings(governance:str,dryrun:str)->list[str]:
    failures=[]
    if governance.count("  governance-selftest:\n")!=1 or governance.count("  sequence-evidence:\n")!=1:
        return ["BUNDLE_CI_GOVERNANCE_JOB_BOUNDARY_MISSING"]
    part=governance.split("  governance-selftest:\n",1)[1].split("  sequence-evidence:\n",1)[0]
    for name,cmd in STEPS:
        anchor="      - name: "+name+"\n"
        if part.count(anchor)!=1:
            failures.append("BUNDLE_CI_REQUIRED_STEP_MISSING_OR_DUPLICATE:"+name)
            continue
        body=part.split(anchor,1)[1].split("      - name: ",1)[0]
        if cmd not in body or "if: matrix.os" in body or "if: steps.bootstrap.outputs.heavy" in body:
            failures.append("BUNDLE_CI_STEP_BYPASSED_OR_MUTATED:"+name)
        if name.startswith("Build and"):
            for token in ("--expected-head",PIN,"release_bundle.py verify","--bundle","--manifest"):
                if token not in body:
                    failures.append("BUNDLE_CI_BUILD_OR_VERIFY_INCOMPLETE:"+token)
    if "  workflow_dispatch:\n" not in dryrun or "\n  push:\n" in dryrun or "\n  pull_request:\n" in dryrun:
        failures.append("BUNDLE_MANUAL_WORKFLOW_NOT_DISPATCH_ONLY")
    if "permissions:\n  contents: read\n" not in dryrun or "contents: write" in dryrun:
        failures.append("BUNDLE_PUBLICATION_PERMISSION_ESCALATION")
    if "os: [ubuntu-latest, windows-latest]" not in dryrun:
        failures.append("BUNDLE_CROSS_OS_MATRIX_MISSING")
    for token in ("actions/upload-artifact@v4","actions/download-artifact@v4",
                  "Dry-run bundle cross-OS byte identity",
                  "assert left==right","CROSS_OS_BUNDLE_EXACT_BYTES=PASS",
                  "data[\"publication_authority\"] is False",
                  "--expected-head",DISPATCH_PIN):
        if token not in dryrun:
            failures.append("BUNDLE_CROSS_OS_PARITY_OR_AUTHORITY_MISSING:"+token)
    return failures


def main()->int:
    root=Path(__file__).resolve().parents[2]
    try:
        governance=(root/".github/workflows/governance-ci.yml").read_text(encoding="utf-8")
        dryrun=(root/".github/workflows/release-bundle-dry-run.yml").read_text(encoding="utf-8")
        issues=findings(governance,dryrun)
    except (ValueError,OSError) as exc:
        issues=["BUNDLE_CI_SOURCE_MISSING:"+str(exc)]
    if issues:
        for issue in issues:
            print("FAIL "+issue)
        return 1
    print("BUNDLE_PERMANENT_BOTH_OS_REQUIRED=PASS")
    print("BUNDLE_READ_ONLY_MANUAL_CROSS_OS_PARITY=PASS")
    print("BUNDLE_NO_PUBLICATION_AUTHORITY=PASS")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
