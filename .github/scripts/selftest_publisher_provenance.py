#!/usr/bin/env python3
"""SW2-26 deliberately failing RED test: signed publisher evidence is absent.

This fixture proves that a valid SW2-25 unsigned integrity report does not
establish trusted GitHub publisher provenance. Acceptance remains NOT_PROVEN.
The companion verifier must never turn an unsigned manifest into trust.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import release_bundle


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def fixture(root: Path) -> str:
    root.mkdir()
    git(root, "init")
    git(root, "config", "user.name", "SW2-26 Test")
    git(root, "config", "user.email", "test@example.invalid")
    files = {
        "SKILL.md": "# Skill\n",
        "LICENSE": "MIT\n",
        "README.md": "# README\n",
        "scripts/core.py": "pass\n",
        "references/guide.md": "# Reference\n",
        "templates/basic.txt": "template\n",
        "docs/handbook/index.md": "# Handbook\n",
    }
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8", newline="\n")
    git(root, "add", "-A")
    git(root, "commit", "-m", "test-source")
    return git(root, "rev-parse", "HEAD")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sw2-26-red-") as tmp:
        td = Path(tmp)
        root = td / "repo"
        sha = fixture(root)
        archive, manifest = td / "artifact.zip", td / "manifest.json"
        release_bundle.build(root, sha, archive, manifest)
        result = release_bundle.verify(archive, manifest)
        assert result["result"] == "PASS"
        assert result["publisher_authenticated"] is False
        assert result["publication_authority"] is False
        assert result["source_git_sha_claimed"] == sha
        print("SW2_25_UNSIGNED_INTEGRITY=PASS")
        print("SW2_25_PUBLISHER_AUTHENTICATED=false")
        verifier = Path(__file__).with_name("publisher_provenance.py")
        if not verifier.is_file():
            print("SW2_26_PUBLISHER_PROVENANCE=RED")
            print("FIRST_FAILED_GATE=SW2_26_TRUSTED_VERIFIER_NOT_IMPLEMENTED")
            return 1
        # Once implemented, use the full adversarial suite here; absence
        # of actual signature checking must never turn RED into PASS.
        print("SW2_26_PUBLISHER_PROVENANCE=RED")
        print("FIRST_FAILED_GATE=SW2_26_ADVERSARIAL_TESTS_NOT_IMPLEMENTED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
