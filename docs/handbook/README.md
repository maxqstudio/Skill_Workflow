<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

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
