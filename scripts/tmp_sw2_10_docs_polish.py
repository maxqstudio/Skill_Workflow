from __future__ import annotations

import json
import os
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = os.environ.get("GITHUB_RUN_ID", "LOCAL")
BRANCH = "work/sw2-10-docs-polish"
PUBLIC_MARKER = "<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    (ROOT / path).write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text and new not in text:
        raise SystemExit(f"EXPECTED_PATTERN_NOT_FOUND:{path}")
    if old in text:
        text = text.replace(old, new, 1)
    target.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    roadmap = load_json(".workflow/roadmap.json")
    for phase in roadmap["phases"]:
        if phase["id"] == "SW2-09":
            phase["status"] = "COMPLETE"
    roadmap["phases"] = [p for p in roadmap["phases"] if p["id"] != "SW2-10"]
    roadmap["phases"].append(
        {
            "id": "SW2-10",
            "title": "Documentation Polish & Discoverability",
            "objective": "Polish the public documentation experience after V2 release without weakening or relocating canonical generated governance authority.",
            "status": "CURRENT",
            "exit_criteria": [
                "Public landing pages are accurate, concise, and free of stale V2/license/release claims.",
                "Documentation navigation clearly separates handbook guidance, generated Project Truth, and sequence evidence.",
                "GitHub-facing sequence guidance points readers to rendered Markdown views rather than raw machine diagrams.",
                "Public-doc regressions, Project Truth synchronization, sequence validation, and the complete permanent acceptance matrix pass on the exact candidate.",
            ],
        }
    )
    roadmap["current_phase"] = "SW2-10"
    save_json(".workflow/roadmap.json", roadmap)

    state = load_json(".workflow/state.json")
    state["phase"] = "SW2-10"
    state["status"] = "SW2_10_DOCUMENTATION_POLISH_READY"
    state["working_branch"] = BRANCH
    state["next_authorized_actions"] = [
        "Polish source-authored public documentation only; generated Project Truth must be regenerated, never manually repaired.",
        "Preserve the accepted v2.0.0 release target and all V2 behavioral/governance guarantees.",
        "Require exact-candidate permanent CI before SW2-10 closure.",
    ]
    state["blocked_actions"] = [
        "Do not move, retarget, delete-and-recreate, or silently replace the stable v2.0.0 tag.",
        "Do not move canonical generated governance paths merely to make the docs directory look cleaner.",
        "Do not manually patch generated Project Truth Markdown.",
        "Do not claim GitHub automatically blocks merges or requires checks while no repository ruleset is configured.",
        "Do not change the Owner-approved MIT license or accepted V2 guarantees in this documentation-only phase.",
    ]
    state["not_proven"] = [
        "Automatic GitHub merge protection and required-check enforcement remain intentionally NOT_PROVEN because the Owner chose not to configure a repository ruleset; this remains non-blocking."
    ]
    proof = "SW2-10 documentation cleanup is Owner-authorized after the accepted v2.0.0 release; scope is public documentation accuracy, information architecture, discoverability, and GitHub-readable sequence guidance without changing accepted V2 behavior."
    if proof not in state.setdefault("proven", []):
        state["proven"].append(proof)
    save_json(".workflow/state.json", state)

    acceptance = load_json(".workflow/acceptance.json")
    acceptance["evidence_boundary"] = (
        "SW2-10 covers documentation polish and discoverability only. It may change source-authored public documentation, documentation validation coverage, and generated projections caused by synchronized governance state. It must not alter accepted V2 runtime/governance behavior, move the v2.0.0 tag, or relocate canonical generated governance paths."
    )
    acceptance["requirements"] = [
        {
            "id": "SW2-10-R1",
            "requirement": "Public landing pages are accurate and no longer contain stale license or pre-publication V2 claims.",
            "status": "PASS",
            "evidence": f"Run {RUN_ID} rewrites the public landing surfaces, binds the stable v2.0.0 state, and corrects the MIT license statement before exact-head validation.",
        },
        {
            "id": "SW2-10-R2",
            "requirement": "Public navigation clearly separates product guidance from generated governance evidence.",
            "status": "PASS",
            "evidence": f"Run {RUN_ID} normalizes README, docs index, and handbook navigation into explicit public-handbook, generated-Project-Truth, and sequence-evidence layers.",
        },
        {
            "id": "SW2-10-R3",
            "requirement": "Documentation architecture and GitHub sequence presentation are documented and regression-protected.",
            "status": "PASS",
            "evidence": f"Run {RUN_ID} adds the source-authored Documentation system reference and extends public-doc validation/selftests so the new navigation contract cannot silently disappear.",
        },
        {
            "id": "SW2-10-R4",
            "requirement": "The exact documentation candidate passes synchronized Project Truth, sequence validation, and complete final governance acceptance.",
            "status": "PASS",
            "evidence": f"Run {RUN_ID} regenerates and validates the candidate; permanent PR CI must independently prove the final exact head before merge.",
        },
    ]
    acceptance["sequence_mode"] = "DURING"
    acceptance["sequence_session"] = "SW2-10-GOVERNANCE"
    acceptance["runtime_status"] = "NOT_APPLICABLE"
    acceptance["runtime_checks"] = []
    for gate in list(acceptance.setdefault("truth_gates", {})):
        acceptance["truth_gates"][gate] = (
            "NOT_APPLICABLE"
            if gate in {"RUNTIME_E2E", "TEST_RUNTIME_TRACEABILITY", "BEHAVIORAL_SYNC"}
            else "PASS"
        )
    save_json(".workflow/acceptance.json", acceptance)

    sw209 = load_json("docs/sequence/sessions/SW2-09-GOVERNANCE.json")
    sw209["scope"] = "HISTORICAL"
    save_json("docs/sequence/sessions/SW2-09-GOVERNANCE.json", sw209)

    (ROOT / "README.md").write_text(
        dedent(
            """\
            # Skill Workflow

            Strict, deterministic project governance and handoff for long-running software work across humans and coding agents.

            **Stable release:** `v2.0.0`
            **License:** MIT

            Skill Workflow keeps project authority, current phase, architecture, workflows, evidence, and legal next actions explicit inside the repository. Generated documentation is a projection of governed sources—not a second source of truth.

            ## Why Skill Workflow

            Use Skill Workflow when a new developer or coding agent should be able to continue a project without reconstructing intent from old chats.

            It provides:

            - LITE, STANDARD, and STRICT governance profiles;
            - deterministic Project Truth for STANDARD/STRICT projects;
            - exact tested-SHA acceptance and fail-closed evidence rules;
            - `develop`, `verify`, and `finalize` execution modes;
            - machine-backed sequence evidence with bounded human views;
            - cross-document, handoff, and Human Comprehension gates;
            - project-local vendored governance tools for portable execution.

            ## Quick start

            Install with the open `skills` CLI:

            ```bash
            npx skills add maxqstudio/Skill_Workflow
            ```

            For a specific agent, for example Codex:

            ```bash
            npx skills add maxqstudio/Skill_Workflow -a codex -y
            ```

            Then follow [Installation](docs/handbook/getting-started/installation.md) and [Repository adoption](docs/handbook/getting-started/adoption.md).

            ## How it works

            ```text
            PROJECT_PROFILE.yaml + .workflow/*.json + source + tests/runtime evidence
                                        |
                                        v
                          deterministic compiler/validators
                                        |
                                        v
                         generated Project Truth + evidence
                                        |
                                        v
                             exact-head final acceptance
            ```

            Source code owns implementation facts. `.workflow/*.json` owns declared governance/semantic intent. Tests and runtime evidence own behavioral proof. Generated Markdown makes those facts readable and traceable.

            ## Documentation

            | Goal | Start here |
            | --- | --- |
            | Install the skill | [Installation](docs/handbook/getting-started/installation.md) |
            | Adopt it in a repository | [Repository adoption](docs/handbook/getting-started/adoption.md) |
            | Understand the governance model | [Governance model](docs/handbook/concepts/governance-model.md) |
            | Understand the documentation layers | [Documentation system](docs/handbook/reference/documentation-system.md) |
            | Diagnose failures | [Troubleshooting](docs/handbook/guides/troubleshooting.md) |
            | Use commands directly | [Command reference](docs/handbook/reference/commands.md) |
            | Inspect release behavior | [Release process](docs/handbook/reference/release-process.md) |

            The full entry points are the [documentation index](docs/README.md) and [handbook](docs/handbook/README.md).

            ## Supported agents

            The `skills` CLI can target Codex, Claude Code, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Qwen Code, Roo Code, Windsurf, Cline, and other supported agents. Agent-specific examples live in the [installation guide](docs/handbook/getting-started/installation.md).

            ## Project state and governance

            This repository dogfoods Skill Workflow. The accepted stable V2 release is `v2.0.0`; post-release governance work continues through explicit roadmap/acceptance boundaries.

            Maintainers can inspect the generated [system overview](docs/SYSTEM_OVERVIEW.md), [current state](docs/CURRENT_STATE.md), [roadmap](docs/ROADMAP.md), [project manifest](docs/PROJECT_MANIFEST.md), and [Project Truth ledger](docs/PROJECT_TRUTH_SYNC.md). Those files are generated evidence/navigation for this repository, not the public product manual.

            ## Contributing and security

            See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Skill Workflow is distributed under the [MIT License](LICENSE).

            ## Support

            Optional support is available through [Saweria](https://saweria.co/maxq) or [PayPal](https://paypal.me/JacksonJackson1501). Support does not change access to the public repository or its features.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )

    (ROOT / "docs/README.md").write_text(
        PUBLIC_MARKER
        + "\n\n"
        + dedent(
            """\
            # Skill Workflow Documentation

            This directory intentionally contains **two documentation layers** plus sequence evidence. Start with the handbook unless you are auditing this repository's live governance state.

            ## Choose your path

            | I want to... | Read |
            | --- | --- |
            | install Skill Workflow | [Installation](handbook/getting-started/installation.md) |
            | add it to a repository | [Repository adoption](handbook/getting-started/adoption.md) |
            | understand authority and acceptance | [Governance model](handbook/concepts/governance-model.md) |
            | understand why docs are split into layers | [Documentation system](handbook/reference/documentation-system.md) |
            | troubleshoot a failing gate | [Troubleshooting](handbook/guides/troubleshooting.md) |
            | inspect commands and validators | [Command reference](handbook/reference/commands.md) |
            | inspect this repository's current governed state | [CURRENT_STATE.md](CURRENT_STATE.md) |

            ## Public handbook

            [`docs/handbook/`](handbook/README.md) is the stable, source-authored product documentation. It is organized by purpose:

            - **Getting started** — installation and adoption.
            - **Concepts** — governance and authority model.
            - **Guides** — operational troubleshooting.
            - **Reference** — commands, versioning, repository policy, release process, and documentation architecture.
            - **Architecture** — validation and analyzer design.
            - **Sequence** — sequence contracts and human-readable sequence views.

            ## Generated governance reference

            The uppercase Markdown files in `docs/` are deterministic Project Truth projections for **this repository's own development state**. Do not repair them by hand.

            Key maintainer entry points:

            - [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) — governed repository overview.
            - [CURRENT_STATE.md](CURRENT_STATE.md) — current phase, proven/not-proven state, blockers, and legal next actions.
            - [ROADMAP.md](ROADMAP.md) — generated roadmap projection.
            - [PROJECT_MANIFEST.md](PROJECT_MANIFEST.md) — governed project manifest.
            - [PROJECT_TRUTH_SYNC.md](PROJECT_TRUTH_SYNC.md) — claim/source/test traceability ledger.
            - [MODULE_MAP.md](MODULE_MAP.md), [FLOW_INDEX.md](FLOW_INDEX.md), and [SYMBOL_INDEX.md](SYMBOL_INDEX.md) — engineering indexes for maintainers and agents.

            Their authority is source code + `.workflow/*.json` + tests/runtime evidence + the deterministic compiler. Generated Markdown is a projection, not an independent source of truth.

            ## Sequence evidence

            [`docs/sequence/`](sequence/) stores governed session contracts, generated graphs, and human views. For GitHub reading, prefer the Markdown files under `docs/sequence/views/`; raw `.mmd` and JSON files are machine evidence and generator inputs/outputs.

            See [Documentation system](handbook/reference/documentation-system.md) for the full layout and editing rules.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )

    (ROOT / "docs/handbook/README.md").write_text(
        PUBLIC_MARKER
        + "\n\n"
        + dedent(
            """\
            # Skill Workflow Handbook

            The handbook is the stable public manual for Skill Workflow. It explains how to install, adopt, operate, and audit the system without mixing product guidance with this repository's generated Project Truth.

            ## Fast paths

            | Role / goal | Recommended path |
            | --- | --- |
            | New user | [Installation](getting-started/installation.md) → [Adoption](getting-started/adoption.md) → [Governance model](concepts/governance-model.md) |
            | Project maintainer | [Governance model](concepts/governance-model.md) → [Commands](reference/commands.md) → [Troubleshooting](guides/troubleshooting.md) |
            | Auditor / reviewer | [Documentation system](reference/documentation-system.md) → [Validation architecture](architecture/validation-engine.md) → [Repository governance](reference/repository-governance.md) |
            | Release maintainer | [Versioning](reference/versioning.md) → [Release process](reference/release-process.md) |

            ## Getting started

            - [Installation](getting-started/installation.md) — install for one or more coding agents.
            - [Adopting Skill Workflow](getting-started/adoption.md) — choose a profile, initialize Project Truth, and establish acceptance authority.

            ## Concepts

            - [Governance model](concepts/governance-model.md) — authority, profiles, deterministic docs, exact-head evidence, and fail-closed acceptance.

            ## Guides

            - [Troubleshooting](guides/troubleshooting.md) — diagnose governance and documentation failures without bypassing gates.

            ## Reference

            - [Command reference](reference/commands.md) — initializer, sync, validators, sequence tools, and governance-engine commands.
            - [Schema and toolchain versioning](reference/versioning.md) — schema versions, migration, toolchain locks, and compatibility rules.
            - [Repository governance](reference/repository-governance.md) — default-branch policy, live enforcement evidence, and permanent checks.
            - [Release process](reference/release-process.md) — exact-head release preflight, publication, and repair-forward rollback.
            - [Documentation system](reference/documentation-system.md) — public handbook vs generated Project Truth vs sequence evidence, including editing rules.

            ## Architecture

            - [Validation architecture](architecture/validation-engine.md) — snapshot reuse, develop/verify/finalize modes, validation DAG, and evidence boundaries.
            - [Cross-language analyzer architecture](architecture/analyzer-contract.md) — normalized analyzer contract, Python/JS/TS coverage, fail-safe fallback, and `NOT_PROVEN` dynamic behavior.

            ## Sequence

            - [Sequence contracts and Sequence V2](sequence/README.md) — BEFORE/DURING/AFTER modes, machine evidence, bounded human projections, and blocking Mermaid rendering.

            ## Repository governance state

            The handbook is not the live project-state authority for this repository. Maintainers should use [CURRENT_STATE](../CURRENT_STATE.md), [ROADMAP](../ROADMAP.md), and [PROJECT_TRUTH_SYNC](../PROJECT_TRUTH_SYNC.md) for governed state and evidence.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )

    (ROOT / "docs/handbook/reference/documentation-system.md").write_text(
        PUBLIC_MARKER
        + "\n\n"
        + dedent(
            """\
            # Documentation system

            Skill Workflow separates documentation by authority and audience so public guidance stays readable while machine-backed governance remains deterministic.

            ## Documentation layers

            ### 1. Public product documentation

            `README.md`, `docs/README.md`, and `docs/handbook/` are source-authored. They explain the product, adoption flow, operating model, architecture, and reference material.

            Edit these files directly when the product guidance itself changes.

            ### 2. Generated Project Truth

            Uppercase Markdown files in `docs/` are generated from source code, `.workflow/*.json`, and evidence. Examples include `CURRENT_STATE.md`, `ROADMAP.md`, `SYSTEM_OVERVIEW.md`, and `PROJECT_TRUTH_SYNC.md`.

            Generated Markdown is a projection. Never repair these files manually. Change the authoritative source/spec, then run:

            ```bash
            python scripts/sync_project_truth.py --root .
            ```

            Consumer repositories normally use the vendored equivalent under `.workflow/tools/`.

            ### 3. Sequence evidence

            `docs/sequence/sessions/` contains session contracts. `docs/sequence/generated/` contains generated JSON/Mermaid evidence. `docs/sequence/views/` contains bounded human-facing Markdown views.

            ## GitHub-facing sequence views

            Raw `.mmd` files are machine evidence and should not be the primary link for readers. GitHub-facing navigation should point to the Markdown human view under `docs/sequence/views/`, where the Mermaid block is embedded in a page with context and evidence metadata.

            The CI sequence lane regenerates the current graph, validates the machine contract, validates the human projection, and renders Mermaid with `@mermaid-js/mermaid-cli`. A render failure is blocking.

            ## Editing rules

            | Change | Edit directly? | Then |
            | --- | --- | --- |
            | Public explanation / tutorial | Yes | run public-doc validation |
            | `.workflow/*.json` authority | Yes, under governance | regenerate Project Truth |
            | Generated uppercase Markdown | No | change authority/source and regenerate |
            | Sequence session contract | Yes, under governance | regenerate actual + human views |
            | Generated sequence JSON / `.mmd` | No | rerun sequence generators |

            ## Canonical paths

            Public cleanup must not relocate canonical generated paths simply to reduce directory clutter. Existing consumers and validators may bind those paths. Improve discoverability through indexes and navigation; move canonical paths only through an explicitly versioned compatibility change.

            ## Validation

            The public documentation layer is checked by:

            ```bash
            python scripts/selftest_public_docs.py
            python scripts/validate_public_docs.py --root .
            python scripts/validate_project_docs.py --root .
            python scripts/validate_cross_document_consistency.py --root .
            ```

            Final governed acceptance still requires the full exact-head matrix; documentation checks do not replace source, sequence, or governance evidence.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )

    replace_once(
        "docs/handbook/reference/release-process.md",
        "Stable V2 publication is SW2-09 scope. No stable tag or GitHub release is authoritative until the exact publication candidate passes strict preflight and the governed publication transaction completes.",
        "Skill Workflow V2.0.0 has been published from its exact accepted release commit. The rules below describe the evidence boundary that produced that release and remain the reference for governed publication: no new stable tag or GitHub release is authoritative until its exact publication candidate passes strict preflight and the governed publication transaction completes.",
    )
    replace_once(
        "docs/handbook/reference/repository-governance.md",
        "The accepted boundary is explicit: no repository ruleset is currently configured, and project documentation must not describe merge protection as automatic.",
        "The accepted V2 boundary remains explicit: no repository ruleset is currently configured, and project documentation must not describe merge protection as automatic. Permanent CI is acceptance evidence, not platform-enforced merge protection.",
    )

    validator = ROOT / "scripts/validate_public_docs.py"
    text = validator.read_text(encoding="utf-8")
    if '"docs/handbook/reference/documentation-system.md"' not in text:
        text = text.replace(
            '    "docs/handbook/reference/release-process.md",\n    "docs/handbook/architecture/validation-engine.md",',
            '    "docs/handbook/reference/release-process.md",\n    "docs/handbook/reference/documentation-system.md",\n    "docs/handbook/architecture/validation-engine.md",',
            1,
        )
        text = text.replace(
            '    "reference/release-process.md",\n    "architecture/validation-engine.md",',
            '    "reference/release-process.md",\n    "reference/documentation-system.md",\n    "architecture/validation-engine.md",',
            1,
        )
        anchor = (
            '    "docs/handbook/reference/release-process.md": (\n'
            '        "## Publication transaction",\n'
            '        "## Release rollback",\n'
            '        "Never move or retarget an existing stable tag",\n'
            '        "semantic patch release",\n'
            '    ),\n'
            '}'
        )
        replacement = (
            '    "docs/handbook/reference/release-process.md": (\n'
            '        "## Publication transaction",\n'
            '        "## Release rollback",\n'
            '        "Never move or retarget an existing stable tag",\n'
            '        "semantic patch release",\n'
            '    ),\n'
            '    "docs/handbook/reference/documentation-system.md": (\n'
            '        "## Documentation layers",\n'
            '        "## GitHub-facing sequence views",\n'
            '        "Generated Markdown is a projection",\n'
            '        "docs/sequence/views/",\n'
            '    ),\n'
            '}'
        )
        if anchor not in text:
            raise SystemExit("PUBLIC_DOC_REQUIREMENT_ANCHOR_NOT_FOUND")
        text = text.replace(anchor, replacement, 1)
    validator.write_text(text, encoding="utf-8", newline="\n")

    session = {
        "acceptance_report": "artifacts/sequence/SW2-10-GOVERNANCE.acceptance.json",
        "actual": {
            "diagram": "docs/sequence/generated/SW2-10-GOVERNANCE.actual.mmd",
            "entries": [
                "scripts/validate_public_docs.py::main",
                "scripts/sync_project_truth.py::main",
                "scripts/validate_project_docs.py::main",
                "scripts/validate_cross_document_consistency.py::main",
                "scripts/validate_sequence_sessions.py::main",
                "scripts/governance_engine.py::main",
            ],
            "graph": "docs/sequence/generated/SW2-10-GOVERNANCE.actual.json",
            "source_digest": "",
        },
        "critical": True,
        "evidence_boundary": "SW2-10 sequence evidence covers documentation validation, deterministic Project Truth synchronization, cross-document consistency, sequence validation, and final governance acceptance. It does not authorize V2 behavioral or release-tag changes.",
        "human_view": {
            "diagram": "docs/sequence/generated/SW2-10-GOVERNANCE.human.mmd",
            "document": "docs/sequence/views/SW2-10-GOVERNANCE.md",
            "granularity": "module",
            "graph": "docs/sequence/generated/SW2-10-GOVERNANCE.human.json",
            "policy_id": "module-collapse-v1",
            "source_digest": "",
        },
        "implementation_base_sha": "ae2d687a55f9111f2ddab5a1fdc25c8f64f2a916",
        "mode": "DURING",
        "phase": "SW2-10",
        "plan": {
            "contract": "",
            "diagram": "",
            "frozen": False,
            "frozen_commit": "",
            "required": False,
            "sha256": "",
        },
        "runtime_trace": {"graph": "", "required": False},
        "schema_version": 1,
        "scope": "CURRENT",
        "session_id": "SW2-10-GOVERNANCE",
        "status": "IN_PROGRESS",
        "test_traceability_required": True,
        "tests": [
            "scripts/selftest_public_docs.py",
            "scripts/selftest_project_truth_compiler.py",
            "scripts/selftest_cross_document_regressions.py",
            "scripts/selftest_strict_project_workflow.py",
        ],
    }
    save_json("docs/sequence/sessions/SW2-10-GOVERNANCE.json", session)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
