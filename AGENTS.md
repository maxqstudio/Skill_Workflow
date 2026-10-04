# AGENTS.md

## Purpose

This is the repository-root operating contract for agents modifying Skill Workflow itself.

Skill Workflow dogfoods its own governance. This file is source-authored, mandatory at repository root, and is read before `PROJECT_PROFILE.yaml` or generated Project Truth.

## Required startup order

1. Read this `AGENTS.md`.
2. Read `PROJECT_PROFILE.yaml`.
3. Read `docs/SYSTEM_OVERVIEW.md`, `docs/CURRENT_STATE.md`, and `docs/ROADMAP.md`.
4. Read `docs/PROJECT_MANIFEST.md` and the exact authority/architecture/workflow documents relevant to the task.
5. Read `SKILL.md` when changing the public skill contract.
6. Inspect exact source/test ranges only after scope and authority are established.

## Non-negotiable rules

- Work from the latest accepted `main` authority on a task branch.
- Keep changes minimum-scope and avoid unrelated cleanup.
- Do not manually edit generated uppercase Project Truth Markdown under `docs/`.
- Change source and/or `.workflow` authority, then regenerate and validate.
- Do not claim PASS from partial testing or from a workflow definition alone.
- Preserve exact tested-head lineage and keep the governed worktree clean at final acceptance.
- `develop` and `verify` are intermediate evidence; only `finalize` may grant final acceptance authority.
- Preserve the stable `v2.0.0` tag target unless a separately authorized release/migration explicitly supersedes it.
- Do not claim GitHub merge enforcement when no repository ruleset is configured.

## SW2 roadmap discipline

`.workflow/roadmap.json` and `.workflow/state.json` must move together. Exactly one roadmap phase is `CURRENT`. A new phase must define explicit requirements and evidence boundaries before implementation is accepted.

## Documentation and sequence

`README.md`, `AGENTS.md`, and `docs/handbook/` are source-authored public/operating guidance. Uppercase Markdown under `docs/` is deterministic Project Truth. Current sequence evidence must be generated and validated; historical sessions remain immutable evidence.

## Final acceptance

Before merge, require the exact candidate to pass the permanent acceptance matrix, including Ubuntu and Windows Governance Selftest, Self Governance, Sequence Evidence, Engine Performance, and Consumer Performance when applicable.
