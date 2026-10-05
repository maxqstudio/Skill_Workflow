#!/usr/bin/env python3
"""Regression tests for SW2-18 CI applicability."""

from ci_applicability import classify


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    docs = classify("pull_request", ["README.md", "docs/guide.md", "references/a.md"])
    require(docs["heavy"] is False, f"pure docs did not skip heavy lanes: {docs}")

    cases = (
        ["docs/guide.md", "scripts/governance_engine.py"],
        [".workflow/state.json"],
        [".github/workflows/governance-ci.yml"],
        ["SKILL.md"],
        ["AGENTS.md"],
        ["future/unknown.bin"],
    )
    for paths in cases:
        result = classify("pull_request", list(paths))
        require(result["heavy"] is True, f"unsafe narrowing for {paths}: {result}")

    push = classify("push", ["docs/guide.md"])
    require(push["heavy"] is True, f"push must remain heavy: {push}")

    empty = classify("pull_request", [])
    require(empty["heavy"] is True, f"empty diff must fail closed: {empty}")

    print("CI_APPLICABILITY_DOCS_ONLY=PASS")
    print("CI_APPLICABILITY_FAIL_CLOSED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
