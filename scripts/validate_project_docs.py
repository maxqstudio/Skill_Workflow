#!/usr/bin/env python3
"""Validate deterministic Project Truth Compiler outputs without mutating docs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--report", default="artifacts/project_docs_sync_report.json")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    compiler = root / "scripts" / "generate_project_docs.py"
    if not compiler.is_file():
        print("FAIL PROJECT_TRUTH_COMPILER_MISSING")
        return 1

    cmd = [
        sys.executable,
        str(compiler),
        "--root",
        str(root),
        "--check",
        "--report",
        args.report,
    ]
    proc = subprocess.run(
        cmd,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(proc.stdout, end="")
    if proc.returncode != 0:
        print("PROJECT_DOCS_SYNC=FAIL")
        return proc.returncode

    print("PROJECT_DOCS_SYNC=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
