#!/usr/bin/env python3
"""Regression tests for Governance Engine V2 primitives."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from extract_project_facts import extract_project_facts
from governance_engine import ValidationDAG, ValidationNode
from project_snapshot import ProjectSnapshot, active_project_snapshot
from sequence_contract import compute_source_digest, source_files


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def snapshot_parity_and_immutability() -> None:
    with tempfile.TemporaryDirectory(prefix="sw2-snapshot-") as td:
        root = Path(td).resolve()
        git(root, "init")
        git(root, "config", "user.email", "sw2@example.invalid")
        git(root, "config", "user.name", "SW2 Test")
        (root / ".gitignore").write_text("ignored.py\n", encoding="utf-8")
        source = root / "app.py"
        source.write_bytes(b"def value():\r\n    return 1\r\n")
        (root / "ignored.py").write_text("raise RuntimeError()\n", encoding="utf-8")
        git(root, "add", ".gitignore", "app.py")
        git(root, "commit", "-m", "fixture")

        legacy_files = source_files(root)
        legacy_digest = compute_source_digest(root)
        snapshot = ProjectSnapshot.capture(root)
        require(
            [p.resolve().relative_to(root).as_posix() for p in legacy_files]
            == [p.resolve().relative_to(root).as_posix() for p in snapshot.source_files()],
            "snapshot inventory differs from accepted standalone inventory",
        )
        require(snapshot.source_digest == legacy_digest, "snapshot digest parity failed")
        require(b"\r\n" not in snapshot.read_bytes("app.py"), "CRLF was not canonicalized")
        require("ignored.py" not in [item.relative_path for item in snapshot.files], "ignored source leaked into snapshot")

        old_digest = snapshot.source_digest
        old_text = snapshot.read_text("app.py")
        source.write_text("def value():\n    return 2\n", encoding="utf-8")
        require(snapshot.source_digest == old_digest, "snapshot digest mutated")
        require(snapshot.read_text("app.py") == old_text, "snapshot bytes mutated")
        fresh = ProjectSnapshot.capture(root)
        require(fresh.source_digest != old_digest, "fresh snapshot missed source change")
        print("SNAPSHOT_PARITY_IMMUTABILITY=PASS")


def snapshot_fact_reuse() -> None:
    with tempfile.TemporaryDirectory(prefix="sw2-reuse-") as td:
        root = Path(td).resolve()
        (root / "app.py").write_text(
            "def helper():\n    return 1\n\ndef main():\n    return helper()\n",
            encoding="utf-8",
        )
        snapshot = ProjectSnapshot.capture(root)
        with active_project_snapshot(snapshot):
            first = extract_project_facts(root)
            second = extract_project_facts(root)
            digest = compute_source_digest(root)
        require(first is second, "derived facts were not memoized")
        require(digest == snapshot.source_digest, "active digest did not reuse snapshot")
        metrics = snapshot.metrics()
        require(metrics["source_enumerations"] == 1, "source inventory repeated")
        require(metrics["file_reads"] == 1, "source file reads repeated")
        require(metrics["derived_cache_misses"] == 1, "facts should be computed once")
        require(metrics["derived_cache_hits"] >= 1, "facts cache was not reused")
        print("SNAPSHOT_FACT_REUSE=PASS")


def dag_executes_once() -> None:
    calls = {"a": 0, "b": 0, "c": 0}

    def action(name: str):
        def run() -> tuple[int, str]:
            calls[name] += 1
            return 0, name + "=PASS\n"
        return run

    results = ValidationDAG(
        [
            ValidationNode("a", (), action("a")),
            ValidationNode("b", ("a",), action("b")),
            ValidationNode("c", ("a", "b"), action("c")),
        ]
    ).run()
    require(all(item.status == "PASS" for item in results.values()), "DAG did not pass")
    require(calls == {"a": 1, "b": 1, "c": 1}, f"duplicate DAG execution: {calls}")
    print("DAG_EXECUTE_ONCE=PASS")


def dag_fail_closed() -> None:
    downstream_calls = 0

    def fail() -> tuple[int, str]:
        return 1, "EXPECTED_FAILURE\n"

    def downstream() -> tuple[int, str]:
        nonlocal downstream_calls
        downstream_calls += 1
        return 0, "UNEXPECTED\n"

    results = ValidationDAG(
        [
            ValidationNode("fail", (), fail),
            ValidationNode("downstream", ("fail",), downstream),
        ]
    ).run()
    require(results["fail"].status == "FAIL", "failure node did not fail")
    require(results["downstream"].status == "BLOCKED", "downstream was not blocked")
    require(downstream_calls == 0, "blocked node executed")

    for nodes, marker in (
        ([ValidationNode("broken", ("missing",), downstream)], "UNKNOWN_DAG_DEPENDENCY"),
        ([ValidationNode("x", ("y",), downstream), ValidationNode("y", ("x",), downstream)], "DAG_CYCLE"),
    ):
        try:
            ValidationDAG(nodes)
        except ValueError as exc:
            require(marker in str(exc), f"wrong DAG error: {exc}")
        else:
            raise AssertionError(marker + " not rejected")
    print("DAG_FAIL_CLOSED=PASS")


def main() -> int:
    snapshot_parity_and_immutability()
    snapshot_fact_reuse()
    dag_executes_once()
    dag_fail_closed()
    print("GOVERNANCE_ENGINE_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
