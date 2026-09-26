#!/usr/bin/env python3
"""Initialize machine-readable Project Truth Compiler specs in a target project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_file(src: Path, dst: Path, force: bool) -> str:
    if dst.exists() and not force:
        return "SKIP"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return "WRITE"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--spec-root", default=".workflow")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    skill_root = Path(__file__).resolve().parent.parent
    template_root = skill_root / "templates" / "workflow_specs"

    if not template_root.is_dir():
        print("FAIL WORKFLOW_SPEC_TEMPLATES_NOT_FOUND:" + str(template_root))
        return 1

    spec_root = Path(args.spec_root)
    if not spec_root.is_absolute():
        spec_root = root / spec_root

    writes = 0
    skips = 0

    for src in sorted(template_root.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(template_root)
        dst = spec_root / rel
        result = copy_file(src, dst, args.force)
        if result == "WRITE":
            writes += 1
            print("WRITE " + dst.relative_to(root).as_posix())
        else:
            skips += 1
            print("SKIP " + dst.relative_to(root).as_posix())

    generated = spec_root / "generated"
    generated.mkdir(parents=True, exist_ok=True)

    print("SPEC_ROOT=" + str(spec_root))
    print("WRITES=" + str(writes))
    print("SKIPS=" + str(skips))
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
