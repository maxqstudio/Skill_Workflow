#!/usr/bin/env python3
"""Executable self-test for the deterministic Project Truth Compiler."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from sequence_contract import compute_source_digest, source_files


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


def test_gitignored_source_files_are_excluded() -> None:
    with tempfile.TemporaryDirectory(prefix="skill-workflow-source-inventory-") as td:
        root = Path(td).resolve()
        run(root, "git", "init", "--quiet")
        run(root, "git", "config", "user.email", "skill-workflow-selftest@example.invalid")
        run(root, "git", "config", "user.name", "Skill Workflow Selftest")

        (root / ".gitignore").write_text(
            "artifacts/\n.pytest-codex-*/\n",
            encoding="utf-8",
        )
        (root / "tracked.py").write_bytes(b"TRACKED = True\n")
        (root / "untracked.py").write_text("UNTRACKED = True\n", encoding="utf-8")
        nested_root = root / "nested"
        nested_root.mkdir()
        (nested_root / "module.py").write_text("NESTED = True\n", encoding="utf-8")
        ignored_artifact = root / "artifacts" / "optimizer" / "report.xml"
        ignored_cache = root / ".pytest-codex-fixture" / "report.xml"
        ignored_artifact.parent.mkdir(parents=True)
        ignored_cache.parent.mkdir(parents=True)
        ignored_artifact.write_text("<report />\n", encoding="utf-8")
        ignored_cache.write_text("<report />\n", encoding="utf-8")

        run(root, "git", "add", ".gitignore", "tracked.py")
        run(root, "git", "commit", "--quiet", "-m", "test: create source inventory fixture")

        observed = {
            path.relative_to(root).as_posix()
            for path in source_files(root)
        }
        required = {"tracked.py", "untracked.py", "nested/module.py"}
        forbidden = {
            "artifacts/optimizer/report.xml",
            ".pytest-codex-fixture/report.xml",
        }
        if not required.issubset(observed):
            raise RuntimeError(
                "tracked or non-ignored source omitted: "
                + ",".join(sorted(required - observed))
            )
        if observed.intersection(forbidden):
            raise RuntimeError(
                "Git-ignored source leaked into inventory: "
                + ",".join(sorted(observed.intersection(forbidden)))
            )
        nested_observed = {
            path.relative_to(nested_root).as_posix()
            for path in source_files(nested_root)
        }
        if nested_observed != {"module.py"}:
            raise RuntimeError(
                "subdirectory source inventory mismatch: "
                + ",".join(sorted(nested_observed))
            )
        lf_digest = compute_source_digest(root)
        (root / "tracked.py").write_bytes(b"TRACKED = True\r\n")
        crlf_digest = compute_source_digest(root)
        if crlf_digest != lf_digest:
            raise RuntimeError("source digest changed with Windows line endings")


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    test_gitignored_source_files_are_excluded()
    print("GITIGNORED_SOURCE_EXCLUSION=PASS")

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
        attributes = (root / ".gitattributes").read_text(encoding="utf-8")
        for required_attribute in (
            "/PROJECT_PROFILE.yaml text eol=lf",
            "/.workflow/** text eol=lf",
            "/docs/** text eol=lf",
        ):
            if required_attribute not in attributes:
                raise RuntimeError("missing governance EOL attribute: " + required_attribute)

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

        roadmap_path = root / ".workflow" / "roadmap.json"
        roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
        roadmap.update(
            {
                "current_phase": "SELFTEST",
                "phases": [
                    {
                        "id": "SELFTEST",
                        "title": "Compiler self-test",
                        "status": "CURRENT",
                        "objective": "Verify deterministic project truth compilation.",
                        "exit_criteria": [
                            "Compiler regeneration is deterministic.",
                            "Roadmap synchronization failures are detected.",
                        ],
                    },
                    {
                        "id": "COMPLETE",
                        "title": "Self-test complete",
                        "status": "PLANNED",
                        "objective": "Record successful compiler validation.",
                        "exit_criteria": ["All compiler self-test assertions pass."],
                    },
                ],
            }
        )
        write_json(roadmap_path, roadmap)

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
        if acceptance.get("truth_gates", {}).get("ROADMAP_SYNC") != "PASS":
            raise RuntimeError("ROADMAP_SYNC was not recorded PASS")

        for name in (
            "SYSTEM_OVERVIEW.md",
            "CURRENT_STATE.md",
            "ROADMAP.md",
            "PROJECT_MANIFEST.md",
        ):
            if (root / name).exists():
                raise RuntimeError("canonical docs leaked to repository root: " + name)
            if not (root / "docs" / name).is_file():
                raise RuntimeError("canonical doc missing from docs/: " + name)

        overview = root / "docs" / "SYSTEM_OVERVIEW.md"
        facts_file = root / ".workflow" / "generated" / "code_facts.json"
        overview.write_bytes(overview.read_bytes().replace(b"\n", b"\r\n"))
        facts_file.write_bytes(facts_file.read_bytes().replace(b"\n", b"\r\n"))
        run(
            root,
            sys.executable,
            str(tool_root / "generate_project_docs.py"),
            "--root",
            str(root),
            "--check",
        )
        quality_crlf = run(
            root,
            sys.executable,
            str(tool_root / "validate_doc_quality.py"),
            "--root",
            str(root),
            expect=1,
        )
        if "NON_LF_NEWLINE" not in quality_crlf:
            raise RuntimeError("doc quality did not preserve strict LF policy")
        run(
            root,
            sys.executable,
            str(tool_root / "sync_project_truth.py"),
            "--root",
            str(root),
        )

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

        # SW2-14 incremental Project Truth contract.
        control_doc = root / "docs" / "ARCHITECTURE.md"
        control_bytes = control_doc.read_bytes()
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "ACTIVE_INCREMENTAL"
        write_json(state_path, state)
        incremental_report = root / "incremental-state.json"
        run(
            root,
            sys.executable,
            str(tool_root / "generate_project_docs.py"),
            "--root", str(root),
            "--incremental",
            "--changed-path", ".workflow/state.json",
            "--report", str(incremental_report),
        )
        incremental = json.loads(incremental_report.read_text(encoding="utf-8"))
        expected_state_docs = {
            "docs/SYSTEM_OVERVIEW.md",
            "docs/PROJECT_MANIFEST.md",
            "docs/CURRENT_STATE.md",
            "docs/ROADMAP.md",
        }
        if set(incremental["generated_docs"]) != expected_state_docs:
            raise RuntimeError("incremental state dependency graph drifted: " + repr(incremental["generated_docs"]))
        if incremental["facts_affected"] or incremental["facts_recomputed"]:
            raise RuntimeError("governance-only incremental change recomputed source facts")
        if "docs/ARCHITECTURE.md" in incremental["written_docs"] or control_doc.read_bytes() != control_bytes:
            raise RuntimeError("unaffected tracked projection was rewritten")
        run(root, sys.executable, str(tool_root / "generate_project_docs.py"), "--root", str(root), "--check")

        unknown_report = root / "incremental-unknown.json"
        run(
            root,
            sys.executable,
            str(tool_root / "generate_project_docs.py"),
            "--root", str(root),
            "--check",
            "--incremental",
            "--changed-path", "future/opaque.bin",
            "--report", str(unknown_report),
        )
        unknown = json.loads(unknown_report.read_text(encoding="utf-8"))
        if not unknown["impact_broad"] or unknown["unknown_paths"] != ["future/opaque.bin"]:
            raise RuntimeError("unknown impact did not broaden fail-closed")
        if set(unknown["generated_docs"]) != set(unknown["all_generated_docs"]):
            raise RuntimeError("unknown impact did not select exhaustive projection set")

        with (root / "app.py").open("a", encoding="utf-8") as fh:
            fh.write("\ndef incremental_probe():\n    return True\n")
        source_report = root / "incremental-source.json"
        run(
            root,
            sys.executable,
            str(tool_root / "generate_project_docs.py"),
            "--root", str(root),
            "--incremental",
            "--changed-path", "app.py",
            "--report", str(source_report),
        )
        source_payload = json.loads(source_report.read_text(encoding="utf-8"))
        if not source_payload["facts_affected"] or not source_payload["facts_recomputed"] or not source_payload["facts_written"]:
            raise RuntimeError("source incremental change did not refresh facts")
        run(root, sys.executable, str(tool_root / "generate_project_docs.py"), "--root", str(root), "--check")

        repeat_report = root / "incremental-repeat.json"
        run(
            root,
            sys.executable,
            str(tool_root / "generate_project_docs.py"),
            "--root", str(root),
            "--incremental",
            "--changed-path", "app.py",
            "--report", str(repeat_report),
        )
        repeat = json.loads(repeat_report.read_text(encoding="utf-8"))
        if repeat["facts_written"] or repeat["written_docs"]:
            raise RuntimeError("byte-identical incremental rerun rewrote tracked outputs")
        print("INCREMENTAL_IMPACT_GRAPH=PASS")
        print("INCREMENTAL_SELECTIVE_WRITE=PASS")
        print("INCREMENTAL_FACT_SELECTIVITY=PASS")
        print("INCREMENTAL_UNKNOWN_BROADENING=PASS")
        print("INCREMENTAL_FULL_PARITY=PASS")
        roadmap_bytes = roadmap_path.read_bytes()
        roadmap_path.unlink()
        missing_roadmap = run(
            root,
            sys.executable,
            str(tool_root / "validate_project_docs.py"),
            "--root",
            str(root),
            expect=1,
        )
        if "roadmap.json" not in missing_roadmap:
            raise RuntimeError(
                "missing roadmap did not fail with roadmap evidence\n"
                + missing_roadmap
            )
        roadmap_path.write_bytes(roadmap_bytes)

        roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
        roadmap["current_phase"] = "DRIFTED_PHASE"
        write_json(roadmap_path, roadmap)
        phase_drift = run(
            root,
            sys.executable,
            str(tool_root / "validate_project_docs.py"),
            "--root",
            str(root),
            expect=1,
        )
        if "ROADMAP_STATE_PHASE_MISMATCH:DRIFTED_PHASE!=SELFTEST" not in phase_drift:
            raise RuntimeError(
                "roadmap phase drift was not detected\n" + phase_drift
            )
        roadmap_path.write_bytes(roadmap_bytes)

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
    print("MISSING_ROADMAP_DETECTION=PASS")
    print("ROADMAP_PHASE_DRIFT_DETECTION=PASS")
    print("ROADMAP_SYNC=PASS")
    print("REGENERATION_RECOVERY=PASS")
    print("DOC_LAYOUT=PASS")
    print("DOC_LAYOUT_DUPLICATE_DETECTION=PASS")
    print("PROJECT_DOCS_NORMALIZED=PASS")
    print("GENERATED_CRLF_COMPARATOR=PASS")
    print("GOVERNANCE_EOL_ATTRIBUTES=PASS")
    print("DOC_READABILITY=PASS")
    print("SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
