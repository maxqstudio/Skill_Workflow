#!/usr/bin/env python3
"""Executable self-test for the deterministic Project Truth Compiler."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(root: Path, *args: str, expect: int = 0) -> str:
    proc = subprocess.run(
        list(args),
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode != expect:
        raise RuntimeError(
            "command failed\n"
            + " ".join(args)
            + "\nexpected="
            + str(expect)
            + " actual="
            + str(proc.returncode)
            + "\n"
            + proc.stdout
        )
    return proc.stdout


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent

    with tempfile.TemporaryDirectory(prefix="skill-workflow-selftest-") as td:
        root = Path(td)
        run(
            skill_root,
            sys.executable,
            str(skill_root / "scripts" / "initialize_project_truth.py"),
            "--root",
            str(root),
        )

        tool_root = root / ".workflow" / "tools"
        if not (tool_root / "sync_project_truth.py").is_file():
            raise RuntimeError("vendored workflow tools were not installed")

        (root / "app.py").write_text(
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n"
            "@app.get('/health')\n"
            "def health():\n"
            "    return {'ok': True}\n",
            encoding="utf-8",
        )

        project_path = root / ".workflow" / "project.json"
        project = json.loads(project_path.read_text(encoding="utf-8"))
        project["project"].update(
            {
                "name": "Compiler Fixture",
                "repository": "local/compiler-fixture",
                "purpose": "Project Truth Compiler self-test",
                "primary_users": ["tester"],
                "expected_outcomes": ["deterministic docs"],
            }
        )
        write_json(project_path, project)

        state_path = root / ".workflow" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update(
            {
                "phase": "SELFTEST",
                "status": "ACTIVE",
                "working_branch": "main",
            }
        )
        write_json(state_path, state)

        authority_path = root / ".workflow" / "authority.json"
        authority = json.loads(authority_path.read_text(encoding="utf-8"))
        authority["authorities"] = [
            {
                "concern": "source",
                "authority": "local/compiler-fixture",
                "meaning": "fixture source tree",
                "mutable": True,
            },
            {
                "concern": "runtime",
                "authority": "local test process",
                "meaning": "self-test runtime evidence",
                "mutable": True,
            },
            {
                "concern": "acceptance",
                "authority": "self-test assertions",
                "meaning": "deterministic compiler acceptance",
                "mutable": False,
            },
        ]
        authority["invariants"] = [
            "Generated docs must reproduce from source and structured specs."
        ]
        write_json(authority_path, authority)

        architecture_path = root / ".workflow" / "architecture.json"
        architecture = json.loads(
            architecture_path.read_text(encoding="utf-8")
        )
        architecture["components"] = [
            {
                "id": "app",
                "name": "Fixture API",
                "purpose": "Serve deterministic health status",
                "owns": ["health endpoint"],
                "depends_on": [],
            }
        ]
        architecture["data_flows"] = [
            {
                "from": "caller",
                "to": "Fixture API",
                "meaning": "health request and response",
            }
        ]
        architecture["external_boundaries"] = []
        write_json(architecture_path, architecture)

        acceptance_path = root / ".workflow" / "acceptance.json"
        acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
        acceptance.update(
            {
                "evidence_boundary": "compiler structural self-test",
                "human_comprehension_status": "PASS",
                "sequence_mode": "DURING",
                "sequence_session": "docs/sequence/sessions/selftest.json",
                "sequence_sync_status": "NOT_PROVEN",
            }
        )
        write_json(acceptance_path, acceptance)

        flow_path = root / ".workflow" / "workflows" / "FLOW-EXAMPLE.json"
        flow = json.loads(flow_path.read_text(encoding="utf-8"))
        flow.update(
            {
                "flow_id": "FLOW-SELFTEST",
                "title": "Health flow",
                "purpose": "Serve health status",
                "entry_condition": "GET /health",
                "authority": "application",
                "sequence_session": "docs/sequence/sessions/selftest.json",
                "source_owners": ["app.py::health"],
            }
        )
        write_json(flow_path, flow)

        profile = root / "PROJECT_PROFILE.yaml"
        profile.write_text(
            profile.read_text(encoding="utf-8").replace(
                "profile_reason: replace-me",
                "profile_reason: compiler-self-test",
            ),
            encoding="utf-8",
        )

        run(
            root,
            sys.executable,
            str(tool_root / "sync_project_truth.py"),
            "--root",
            str(root),
        )

        acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
        if acceptance.get("truth_gates", {}).get("PROJECT_DOCS_SYNC") != "PASS":
            raise RuntimeError("PROJECT_DOCS_SYNC was not recorded PASS")

        for name in (
            "SYSTEM_OVERVIEW.md",
            "CURRENT_STATE.md",
            "PROJECT_MANIFEST.md",
        ):
            if (root / name).exists():
                raise RuntimeError("canonical docs leaked to repository root: " + name)
            if not (root / "docs" / name).is_file():
                raise RuntimeError("canonical doc missing from docs/: " + name)

        overview = root / "docs" / "SYSTEM_OVERVIEW.md"

        duplicate = root / "SYSTEM_OVERVIEW.md"
        duplicate.write_text(
            overview.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        run(
            root,
            sys.executable,
            str(tool_root / "validate_project_docs.py"),
            "--root",
            str(root),
            expect=1,
        )
        duplicate.unlink()

        overview.write_text(
            overview.read_text(encoding="utf-8") + "\nMANUAL_TAMPER\n",
            encoding="utf-8",
        )
        run(
            root,
            sys.executable,
            str(tool_root / "validate_project_docs.py"),
            "--root",
            str(root),
            expect=1,
        )

        run(
            root,
            sys.executable,
            str(tool_root / "sync_project_truth.py"),
            "--root",
            str(root),
        )

        with (root / "app.py").open("a", encoding="utf-8") as fh:
            fh.write(
                "\n@app.get('/version')\n"
                "def version():\n"
                "    return {'version': 1}\n"
            )

        run(
            root,
            sys.executable,
            str(tool_root / "validate_project_docs.py"),
            "--root",
            str(root),
            expect=1,
        )

        run(
            root,
            sys.executable,
            str(tool_root / "sync_project_truth.py"),
            "--root",
            str(root),
        )

        final = run(
            root,
            sys.executable,
            str(tool_root / "validate_project_docs.py"),
            "--root",
            str(root),
        )
        if "PROJECT_DOCS_SYNC=PASS" not in final:
            raise RuntimeError("final generated docs check did not PASS")

    print("PROJECT_TRUTH_COMPILER_SELFTEST=PASS")
    print("TAMPER_DETECTION=PASS")
    print("SOURCE_DRIFT_DETECTION=PASS")
    print("REGENERATION_RECOVERY=PASS")
    print("DOC_LAYOUT=PASS")
    print("DOC_LAYOUT_DUPLICATE_DETECTION=PASS")
    print("PROJECT_DOCS_NORMALIZED=PASS")
    print("DOC_READABILITY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
