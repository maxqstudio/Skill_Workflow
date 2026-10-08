#!/usr/bin/env python3
"""SW2-25 fail-closed CI contract regression without running external workflows."""
from __future__ import annotations
from pathlib import Path
import validate_release_bundle_ci as policy

def require_issue(governance:str,manual:str,needle:str)->None:
    found=policy.findings(governance,manual)
    assert any(needle in item for item in found),(needle,found)

def main()->int:
    root=Path(__file__).resolve().parents[2]
    g=(root/".github/workflows/governance-ci.yml").read_text(encoding="utf-8")
    m=(root/".github/workflows/release-bundle-dry-run.yml").read_text(encoding="utf-8")
    assert not policy.findings(g,m),policy.findings(g,m)
    require_issue(g.replace("Release bundle content-integrity regressions",
                            "Disabled bundle tests",1),m,
                  "BUNDLE_CI_REQUIRED_STEP_MISSING_OR_DUPLICATE")
    require_issue(g.replace("release_bundle.py verify","release_bundle.py check",1),
                  m,"BUNDLE_CI_BUILD_OR_VERIFY_INCOMPLETE")
    require_issue(g.replace("      - name: Build and detached-verify exact-head read-only bundle\n",
                            "      - name: Build and detached-verify exact-head read-only bundle\n        if: matrix.os != 'windows-latest'\n",1),
                  m,"BUNDLE_CI_STEP_BYPASSED_OR_MUTATED")
    require_issue(g,m.replace("  workflow_dispatch:\n","  push:\n",1),
                  "BUNDLE_MANUAL_WORKFLOW_NOT_DISPATCH_ONLY")
    require_issue(g,m.replace("  contents: read","  contents: write",1),
                  "BUNDLE_PUBLICATION_PERMISSION_ESCALATION")
    require_issue(g,m.replace("assert left==right","assert left!=right",1),
                  "BUNDLE_CROSS_OS_PARITY_OR_AUTHORITY_MISSING")
    require_issue(g,m.replace('data["publication_authority"] is False',
                              'data["publication_authority"] is True',1),
                  "BUNDLE_CROSS_OS_PARITY_OR_AUTHORITY_MISSING")
    print("BUNDLE_STATIC_NEGATIVE_PATHS=PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
