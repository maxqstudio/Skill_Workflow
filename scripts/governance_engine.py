#!/usr/bin/env python3
"""Governance Engine V2: one immutable snapshot plus a fail-closed DAG.

SW2-01 changes orchestration only. Develop/verify/finalize execution modes remain
SW2-02. Existing standalone validators keep their full fail-closed behavior;
the engine may skip a nested check only when that check is already a successful
DAG dependency in the same process and source snapshot.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import sync_project_truth
import validate_cross_document_consistency
import validate_human_comprehension
import validate_project_docs
import validate_project_truth
from project_snapshot import ProjectSnapshot, active_project_snapshot
from script_runner import invoke_main


@dataclass(frozen=True)
class NodeResult:
    name: str
    status: str
    returncode: int
    seconds: float
    output: str
    blocked_by: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationNode:
    name: str
    dependencies: tuple[str, ...]
    action: Callable[[], tuple[int, str]]


class ValidationDAG:
    def __init__(self, nodes: list[ValidationNode]) -> None:
        self.nodes: dict[str, ValidationNode] = {}
        for node in nodes:
            if node.name in self.nodes:
                raise ValueError(f"DUPLICATE_DAG_NODE:{node.name}")
            self.nodes[node.name] = node
        for node in nodes:
            for dependency in node.dependencies:
                if dependency not in self.nodes:
                    raise ValueError(
                        f"UNKNOWN_DAG_DEPENDENCY:{node.name}:{dependency}"
                    )
        self._assert_acyclic()

    def _assert_acyclic(self) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(name: str) -> None:
            if name in visited:
                return
            if name in visiting:
                raise ValueError(f"DAG_CYCLE:{name}")
            visiting.add(name)
            for dependency in self.nodes[name].dependencies:
                visit(dependency)
            visiting.remove(name)
            visited.add(name)

        for name in self.nodes:
            visit(name)

    def run(self) -> dict[str, NodeResult]:
        results: dict[str, NodeResult] = {}

        def execute(name: str) -> NodeResult:
            existing = results.get(name)
            if existing is not None:
                return existing
            node = self.nodes[name]
            dependency_results = [execute(dep) for dep in node.dependencies]
            failed = tuple(
                result.name
                for result in dependency_results
                if result.status != "PASS"
            )
            if failed:
                result = NodeResult(
                    name=name,
                    status="BLOCKED",
                    returncode=1,
                    seconds=0.0,
                    output="",
                    blocked_by=failed,
                )
                results[name] = result
                return result

            started = time.perf_counter()
            try:
                code, output = node.action()
            except Exception as exc:
                code = 1
                output = f"DAG_NODE_EXCEPTION:{type(exc).__name__}:{exc}\n"
            result = NodeResult(
                name=name,
                status="PASS" if code == 0 else "FAIL",
                returncode=code,
                seconds=time.perf_counter() - started,
                output=output,
            )
            results[name] = result
            return result

        for name in self.nodes:
            execute(name)
        return results


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def state_base(root: Path) -> str:
    path = root / ".workflow" / "state.json"
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return str(data.get("last_accepted_sha", "")).strip()


def governed_status(root: Path) -> tuple[int, str]:
    status = git(
        root,
        "status",
        "--porcelain",
        "--untracked-files=all",
        "--",
        "PROJECT_PROFILE.yaml",
        ".workflow",
        "docs",
    )
    if status:
        return 1, "GOVERNED_STATE_DIRTY\n" + status + "\n"
    return 0, "GOVERNED_STATE_CLEAN\n"


def cli_action(
    main_func: Callable[[], int | None],
    argv: list[str],
    program: str,
) -> Callable[[], tuple[int, str]]:
    return lambda: invoke_main(main_func, argv, program=program)


def build_dag(root: Path, *, base: str, sync: bool) -> ValidationDAG:
    nodes: list[ValidationNode] = []
    if sync:
        nodes.append(
            ValidationNode(
                name="sync_project_truth",
                dependencies=(),
                action=cli_action(
                    sync_project_truth.main,
                    ["--root", str(root)],
                    "sync_project_truth.py",
                ),
            )
        )
        docs_dependency = "sync_project_truth"
    else:
        nodes.append(
            ValidationNode(
                name="validate_project_docs",
                dependencies=(),
                action=cli_action(
                    validate_project_docs.main,
                    ["--root", str(root)],
                    "validate_project_docs.py",
                ),
            )
        )
        docs_dependency = "validate_project_docs"

    nodes.append(
        ValidationNode(
            name="validate_human_comprehension",
            dependencies=(docs_dependency,),
            action=cli_action(
                validate_human_comprehension.main,
                ["--root", str(root), "--require-pass"],
                "validate_human_comprehension.py",
            ),
        )
    )
    nodes.append(
        ValidationNode(
            name="validate_cross_document_consistency",
            dependencies=("validate_human_comprehension",),
            action=cli_action(
                validate_cross_document_consistency.main,
                ["--root", str(root), "--base", base, "--require-base"],
                "validate_cross_document_consistency.py",
            ),
        )
    )
    nodes.append(
        ValidationNode(
            name="validate_project_truth",
            dependencies=("validate_cross_document_consistency",),
            action=cli_action(
                validate_project_truth.main,
                [
                    "--root", str(root),
                    "--project-docs-already-validated",
                ],
                "validate_project_truth.py",
            ),
        )
    )
    if sync:
        nodes.append(
            ValidationNode(
                name="governed_state_clean",
                dependencies=("validate_project_truth",),
                action=lambda: governed_status(root),
            )
        )
    return ValidationDAG(nodes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", default="")
    parser.add_argument("--sync", action="store_true")
    parser.add_argument("--expected-head", default="")
    parser.add_argument("--report", default="")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    base = args.base.strip() or state_base(root)
    if not base:
        print("FAIL BASE_SHA_REQUIRED")
        return 2

    snapshot = ProjectSnapshot.capture(root)
    expected_head = args.expected_head.strip()
    if expected_head and snapshot.git_head != expected_head:
        report = {
            "schema_version": 1,
            "result": "FAIL",
            "failures": [
                f"PROVENANCE_MISMATCH:observed={snapshot.git_head}:expected={expected_head}"
            ],
            "snapshot": snapshot.metrics(),
            "nodes": {},
        }
    else:
        with active_project_snapshot(snapshot):
            try:
                results = build_dag(root, base=base, sync=args.sync).run()
            except Exception as exc:
                print(f"FAIL ENGINE_DAG_ERROR:{type(exc).__name__}:{exc}")
                return 2

        failures = [
            name for name, result in results.items() if result.status != "PASS"
        ]
        report = {
            "schema_version": 1,
            "result": "FAIL" if failures else "PASS",
            "failures": failures,
            "base_sha": base,
            "expected_head": expected_head or "NOT_DECLARED",
            "snapshot": snapshot.metrics(),
            "nodes": {
                name: {
                    "status": result.status,
                    "returncode": result.returncode,
                    "seconds": result.seconds,
                    "blocked_by": list(result.blocked_by),
                    "output_tail": result.output.splitlines()[-20:],
                }
                for name, result in results.items()
            },
            "boundary": (
                "Snapshot and memoization accelerate one process only. Final acceptance authority "
                "remains exact candidate source plus all required test/validator evidence."
            ),
        }

    payload = json.dumps(report, indent=2, sort_keys=True)
    print(payload)
    if args.report:
        path = Path(args.report)
        if not path.is_absolute():
            path = root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload + "\n", encoding="utf-8")
    return 1 if report["result"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
