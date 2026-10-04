#!/usr/bin/env python3
"""Initialize machine-readable Project Truth Compiler specs in a target project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from toolchain_identity import SOURCE_ONLY_TOOLS, write_toolchain_lock


GITATTRIBUTES_MARKER = "# BEGIN SKILL_WORKFLOW GOVERNANCE EOL"
GITATTRIBUTES_BLOCK = """# BEGIN SKILL_WORKFLOW GOVERNANCE EOL
/AGENTS.md text eol=lf
/PROJECT_PROFILE.yaml text eol=lf
/.workflow/** text eol=lf
/docs/** text eol=lf
# END SKILL_WORKFLOW GOVERNANCE EOL
"""


def ensure_gitattributes(root: Path) -> str:
    path = root / ".gitattributes"
    if path.is_file():
        current = path.read_text(encoding="utf-8")
        if GITATTRIBUTES_MARKER in current:
            if "/AGENTS.md text eol=lf" in current:
                return "SKIP"
            current = current.replace(
                GITATTRIBUTES_MARKER + "\n",
                GITATTRIBUTES_MARKER + "\n/AGENTS.md text eol=lf\n",
                1,
            )
            path.write_text(current, encoding="utf-8", newline="\n")
            return "WRITE"
        separator = "" if not current or current.endswith("\n") else "\n"
        path.write_text(current + separator + GITATTRIBUTES_BLOCK, encoding="utf-8", newline="\n")
    else:
        path.write_text(GITATTRIBUTES_BLOCK, encoding="utf-8", newline="\n")
    return "WRITE"


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
    ap.add_argument("--no-tools", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    skill_root = Path(__file__).resolve().parent.parent
    template_root = skill_root / "templates" / "workflow_specs"
    profile_template = skill_root / "templates" / "PROJECT_PROFILE.yaml"
    agents_template = skill_root / "templates" / "AGENTS.md"

    if not template_root.is_dir():
        print("FAIL WORKFLOW_SPEC_TEMPLATES_NOT_FOUND:" + str(template_root))
        return 1

    spec_root = Path(args.spec_root)
    if not spec_root.is_absolute():
        spec_root = root / spec_root

    writes = 0
    skips = 0

    attributes_result = ensure_gitattributes(root)
    if attributes_result == "WRITE":
        writes += 1
        print("WRITE .gitattributes")
    else:
        skips += 1
        print("SKIP .gitattributes")

    if agents_template.is_file():
        result = copy_file(agents_template, root / "AGENTS.md", args.force)
        if result == "WRITE":
            writes += 1
            print("WRITE AGENTS.md")
        else:
            skips += 1
            print("SKIP AGENTS.md")

    if profile_template.is_file():
        result = copy_file(profile_template, root / "PROJECT_PROFILE.yaml", args.force)
        if result == "WRITE":
            writes += 1
            print("WRITE PROJECT_PROFILE.yaml")
        else:
            skips += 1
            print("SKIP PROJECT_PROFILE.yaml")

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

    docs_root = root / "docs"
    docs_root.mkdir(parents=True, exist_ok=True)

    if not args.no_tools:
        tools_root = spec_root / "tools"
        tools_root.mkdir(parents=True, exist_ok=True)
        source_tools = Path(__file__).resolve().parent
        excluded_tools = SOURCE_ONLY_TOOLS
        for src in sorted(source_tools.glob("*.py")):
            if src.name in excluded_tools:
                continue
            dst = tools_root / src.name
            result = copy_file(src, dst, args.force)
            if result == "WRITE":
                writes += 1
                print("WRITE " + dst.relative_to(root).as_posix())
            else:
                skips += 1
                print("SKIP " + dst.relative_to(root).as_posix())

        lock_result = write_toolchain_lock(root, spec_root, tools_root, skill_root)
        if lock_result == "WRITE":
            writes += 1
            print("WRITE " + (spec_root / "toolchain.lock.json").relative_to(root).as_posix())
        else:
            skips += 1
            print("SKIP " + (spec_root / "toolchain.lock.json").relative_to(root).as_posix())

    print("SPEC_ROOT=" + str(spec_root))
    print("DOCS_ROOT=" + str(docs_root))
    print("WRITES=" + str(writes))
    print("SKIPS=" + str(skips))
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
