#!/usr/bin/env python3
"""Conservative CI applicability classifier for SW2-18.

Heavy performance/consumer lanes may be skipped only for pull requests whose
entire diff is public documentation/reference content. Unknown or governance
impact always broadens fail-closed to the heavy lanes.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

DOC_ONLY_FILES = frozenset({
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
})
DOC_ONLY_PREFIXES = ("docs/", "references/")


def normalize(path: str) -> str:
    value = path.replace("\\", "/")
    return value[2:] if value.startswith("./") else value


def is_docs_only_path(path: str) -> bool:
    value = normalize(path)
    return value in DOC_ONLY_FILES or value.startswith(DOC_ONLY_PREFIXES)


def classify(event_name: str, changed_paths: list[str]) -> dict[str, object]:
    paths = sorted({normalize(item) for item in changed_paths if normalize(item)})
    if event_name != "pull_request":
        return {"heavy": True, "reason": "NON_PR_FAIL_CLOSED", "changed_paths": paths}
    if not paths:
        return {"heavy": True, "reason": "EMPTY_DIFF_FAIL_CLOSED", "changed_paths": paths}
    non_docs = [path for path in paths if not is_docs_only_path(path)]
    if non_docs:
        return {
            "heavy": True,
            "reason": "NON_DOC_IMPACT",
            "changed_paths": paths,
            "non_docs": non_docs,
        }
    return {"heavy": False, "reason": "PURE_DOCS_PR", "changed_paths": paths}


def git_changed_paths(root: Path, base: str, head: str) -> list[str]:
    if not base or not head:
        return []
    try:
        payload = subprocess.check_output(
            ["git", "-C", str(root), "diff", "--name-only", "-z", f"{base}...{head}"],
            stderr=subprocess.STDOUT,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [
        item.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for item in payload.split(b"\0")
        if item
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--event", required=True)
    parser.add_argument("--base", default="")
    parser.add_argument("--head", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args()

    paths = git_changed_paths(Path(args.root).resolve(), args.base.strip(), args.head.strip())
    result = classify(args.event.strip(), paths)
    print(json.dumps(result, indent=2, sort_keys=True))

    if args.github_output:
        output = Path(args.github_output)
        with output.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(f"heavy={'true' if result['heavy'] else 'false'}\n")
            fh.write(f"reason={result['reason']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
