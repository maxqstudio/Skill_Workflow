import json
import subprocess
import sys
from pathlib import Path

root = Path(".").resolve()
acceptance = json.loads((root / ".workflow/acceptance.json").read_text(encoding="utf-8"))
session_id = str(acceptance.get("sequence_session", "")).strip()
if not session_id:
    raise SystemExit("CURRENT_SEQUENCE_SESSION_MISSING")
session_path = root / "docs/sequence/sessions" / f"{session_id}.json"
session = json.loads(session_path.read_text(encoding="utf-8"))
actual = session["actual"]
cmd = [
    sys.executable,
    "scripts/generate_sequence_actual.py",
    "--root",
    ".",
    "--output-json",
    actual["graph"],
    "--output-mermaid",
    actual["diagram"],
]
for entry in actual.get("entries", []):
    cmd += ["--entry", entry]
subprocess.run(cmd, check=True)
graph = json.loads((root / actual["graph"]).read_text(encoding="utf-8"))
digest = graph["source_digest"]
session["actual"]["source_digest"] = digest
human = session.get("human_view") or {}
if human:
    session["human_view"]["source_digest"] = digest
session_path.write_text(
    json.dumps(session, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)
if human:
    subprocess.run(
        [
            sys.executable,
            "scripts/sequence_human_view.py",
            "--root",
            ".",
            "--actual-json",
            actual["graph"],
            "--actual-mermaid",
            actual["diagram"],
            "--output-json",
            human["graph"],
            "--output-mermaid",
            human["diagram"],
            "--output-markdown",
            human["document"],
            "--session-id",
            session_id,
        ],
        check=True,
    )
subprocess.run(
    [
        sys.executable,
        "scripts/validate_sequence_contract.py",
        "--root",
        ".",
        "--session",
        session_path.as_posix(),
        "--report",
        session["acceptance_report"],
    ],
    check=True,
)
subprocess.run(
    [sys.executable, "scripts/validate_sequence_sessions.py", "--root", "."],
    check=True,
)
print(f"CURRENT_SEQUENCE_SESSION={session_id}")
print("CURRENT_SEQUENCE_GENERATION=PASS")
