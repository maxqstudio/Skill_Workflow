<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Skill Workflow Handbook

The handbook is the stable public documentation entry point for Skill Workflow. It explains how to install, adopt, operate, and reason about the system without mixing product guidance with this repository's generated governance state.

## Getting started

- [Installation](getting-started/installation.md) — install for one or more coding agents.
- [Adopting Skill Workflow](getting-started/adoption.md) — choose a profile, initialize Project Truth, and establish acceptance authority.

## Concepts

- [Governance model](concepts/governance-model.md) — authority, profiles, deterministic docs, exact-head evidence, and fail-closed acceptance.

## Guides

- [Troubleshooting](guides/troubleshooting.md) — diagnose common governance and documentation failures without bypassing gates.

## Reference

- [Command reference](reference/commands.md) — initializer, sync, validators, sequence tools, and governance-engine commands.
- [Schema and toolchain versioning](reference/versioning.md) — supported schema versions, explicit migration, toolchain locks, and compatibility rules.

## Architecture

- [Validation architecture](architecture/validation-engine.md) — snapshot reuse, develop/verify/finalize modes, validation DAG, and evidence boundaries.
- [Cross-language analyzer architecture](architecture/analyzer-contract.md) — normalized analyzer contract, current Python/JS/TS coverage, fail-safe fallback, and `NOT_PROVEN` dynamic behavior.

## Sequence

- [Sequence contracts and Sequence V2](sequence/README.md) — BEFORE/DURING/AFTER modes, full machine evidence, bounded human projections, and blocking Mermaid rendering.

## Repository governance state

The public handbook is not the live project-state authority for this repository. Maintainers should use [CURRENT_STATE](../CURRENT_STATE.md), [ROADMAP](../ROADMAP.md), and [PROJECT_TRUTH_SYNC](../PROJECT_TRUTH_SYNC.md) for governed development state and evidence.
