<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Skill Workflow Documentation

This directory contains two intentionally different documentation layers.

## Public handbook

Use the [Skill Workflow handbook](handbook/README.md) to learn and use the project:

- [Installation](handbook/getting-started/installation.md)
- [Repository adoption](handbook/getting-started/adoption.md)
- [Governance model](handbook/concepts/governance-model.md)
- [Troubleshooting](handbook/guides/troubleshooting.md)
- [Command reference](handbook/reference/commands.md)
- [Validation architecture](handbook/architecture/validation-engine.md)
- [Sequence contracts](handbook/sequence/README.md)

These files are source-authored product guidance.

## Generated governance reference

The uppercase Markdown files beside this README are deterministic Project Truth projections for **this repository's own development state**. They are not the public tutorial/manual and must not be edited as independent semantic authority.

Useful maintainer entry points:

- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) — governed repository overview
- [CURRENT_STATE.md](CURRENT_STATE.md) — current phase, proven/not-proven state, and legal next actions
- [ROADMAP.md](ROADMAP.md) — generated roadmap projection
- [PROJECT_TRUTH_SYNC.md](PROJECT_TRUTH_SYNC.md) — traceability ledger
- [MODULE_MAP.md](MODULE_MAP.md), [FLOW_INDEX.md](FLOW_INDEX.md), and [SYMBOL_INDEX.md](SYMBOL_INDEX.md) — engineering navigation indexes
- [sequence/](sequence/) — machine and human sequence acceptance evidence

The authority for generated files is source plus `.workflow/*.json`, tests/runtime evidence, and the deterministic compiler—not manual edits to generated Markdown.
