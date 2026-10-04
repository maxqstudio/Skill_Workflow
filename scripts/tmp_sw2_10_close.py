from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXACT_HEAD = "0e6b1cc80682fe2adf77495359900bcd341c28df"
RUNS = {
    "self_governance": "37189710272",
    "governance_selftest": "37189710279",
    "sequence": "37189710273",
    "engine": "37189710274",
    "consumer": "37189710271",
}


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save(path: str, data: dict) -> None:
    (ROOT / path).write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    state = load(".workflow/state.json")
    state["status"] = "SW2_10_DOCUMENTATION_POLISH_ACCEPTED"
    state["working_branch"] = "main"
    state["next_authorized_actions"] = [
        "Treat the polished public documentation and synchronized Project Truth from SW2-10 as the accepted documentation baseline.",
        "Preserve the accepted v2.0.0 release target and all V2 behavioral/governance guarantees.",
        "For future documentation architecture or compatibility changes, declare a new governed acceptance boundary before implementation.",
    ]
    proof = (
        f"SW2-10 Documentation Polish & Discoverability is accepted on exact candidate {EXACT_HEAD}: "
        f"Self Governance {RUNS['self_governance']} SUCCESS; Governance Selftest {RUNS['governance_selftest']} "
        f"SUCCESS on Ubuntu and Windows; SW2 Sequence Evidence {RUNS['sequence']} SUCCESS; "
        f"Governance Engine Performance {RUNS['engine']} SUCCESS; Consumer Engine Performance {RUNS['consumer']} SUCCESS. "
        "The accepted scope corrects stale public license/release wording, improves role/task navigation, documents the public/generated/sequence documentation layers, preserves canonical generated paths, and leaves V2 behavior and the v2.0.0 release target unchanged."
    )
    if proof not in state.setdefault("proven", []):
        state["proven"].append(proof)
    save(".workflow/state.json", state)

    acceptance = load(".workflow/acceptance.json")
    for req in acceptance.get("requirements", []):
        if req.get("id") == "SW2-10-R4":
            req["status"] = "PASS"
            req["evidence"] = (
                f"Exact candidate {EXACT_HEAD} passed the complete permanent PR matrix: Self Governance "
                f"{RUNS['self_governance']} SUCCESS; Governance Selftest {RUNS['governance_selftest']} SUCCESS on Ubuntu and Windows; "
                f"SW2 Sequence Evidence {RUNS['sequence']} SUCCESS; Governance Engine Performance {RUNS['engine']} SUCCESS; "
                f"Consumer Engine Performance {RUNS['consumer']} SUCCESS. The candidate had already passed clean-worktree "
                "cross-document consistency, Project Truth validation, sequence validation, and Governance Engine finalize before PR CI."
            )
    save(".workflow/acceptance.json", acceptance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
