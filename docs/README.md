<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

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
