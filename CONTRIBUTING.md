# Contributing to Skill Workflow

Skill Workflow is strict governance tooling. Contributions should improve correctness, evidence quality, portability, or usability without weakening fail-closed acceptance.

## Before changing code

Read:

- `SKILL.md` for the product contract;
- `docs/handbook/README.md` for public documentation;
- `docs/CURRENT_STATE.md` and `docs/ROADMAP.md` for governed repository state.

Do not edit generated Project Truth files to make a gate pass. Change the authoritative source or structured `.workflow` input, then regenerate deterministically.

## Change scope

Keep each pull request narrow. Avoid unrelated refactors, generated-file churn, or parser rewrites that are not required by the accepted phase.

Unknown impact must broaden verification rather than silently skip checks.

## Branches and pull requests

Create changes on a branch and merge through a pull request. The default branch is governed against deletion and non-fast-forward updates, and the repository currently permits squash merge for governed changes.

A pull request is not accepted merely because GitHub allows it to merge. Required project evidence must also be green on the exact candidate SHA.

## Validation

At minimum, run the checks relevant to the change. The permanent cross-platform regression lane includes:

```text
python -m compileall -q scripts
python scripts/selftest_schema_toolchain.py
python scripts/validate_schema_toolchain.py --root .
python scripts/selftest_governance_engine.py
python scripts/selftest_analyzer_contract.py
python scripts/selftest_sequence_call_resolution.py
python scripts/selftest_sequence_human_view.py
python scripts/selftest_public_docs.py
python scripts/selftest_repository_health.py
python scripts/selftest_github_ruleset.py
python scripts/selftest_release_preflight.py
python scripts/selftest_generated_doc_presentation.py
python scripts/selftest_cross_document_regressions.py
python scripts/selftest_project_truth_compiler.py
python scripts/selftest_strict_project_workflow.py
```

For governed acceptance, use the exact-head workflow described by the current Project Truth and `governance_engine.py`.

## Documentation

Public product documentation is source-authored under `docs/handbook/`. Generated Project Truth remains under `docs/` at its canonical paths.

If a change affects behavior, commands, architecture, sequence contracts, schemas, or release operations, update the relevant public documentation in the same pull request.

## Security

Do not place vulnerability details, secrets, tokens, exploit material, or private user data in a public issue or pull request. Follow `SECURITY.md`.

## License boundary

This repository does not currently declare an Owner-approved public license. Do not add, infer, or claim a license until an accepted governance decision records the Owner's explicit choice.
