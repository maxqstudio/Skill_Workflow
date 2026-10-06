<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Command Reference

Commands below assume a governed target repository with tools vendored under `.workflow/tools/` unless noted otherwise.

## Initialize

From the Skill Workflow package/checkout:

```bash
python scripts/initialize_project_truth.py --root /path/to/project
```

## Toolchain provenance and upgrade

Run upgrade inspection from the Skill Workflow checkout/package that should become the consumer's toolchain source:

```bash
python scripts/upgrade_governance_toolchain.py --root /path/to/project --check
```

`--check` is read-only and exits non-zero when an upgrade or provenance migration is required. Review the emitted `PLAN_JSON`, then apply only the vendored toolchain surfaces:

```bash
python scripts/upgrade_governance_toolchain.py --root /path/to/project --apply
```

Apply may change only `.workflow/tools/*.py` owned by the prior/current toolchain and `.workflow/toolchain.lock.json`. It does not rewrite `AGENTS.md`, project semantic `.workflow/*.json`, source code, or project-specific configuration.

## Synchronize Project Truth

```bash
python .workflow/tools/sync_project_truth.py --root .
```

## Documentation validation

```bash
python .workflow/tools/validate_project_docs.py --root .
python .workflow/tools/validate_doc_quality.py --root .
python .workflow/tools/validate_human_comprehension.py --root . --require-pass
python .workflow/tools/validate_cross_document_consistency.py --root . --base <LAST_ACCEPTED_SHA> --require-base
```

## Project truth and handoff

```bash
python .workflow/tools/validate_handoff.py --root .
python .workflow/tools/validate_project_truth.py --root .
```

## Sequence evidence

```bash
python .workflow/tools/generate_sequence_actual.py --root . --output-json <actual.json> --output-mermaid <actual.mmd> --entry <path::symbol>
python .workflow/tools/sequence_human_view.py --root . --actual-json <actual.json> --actual-mermaid <actual.mmd> --output-json <human.json> --output-mermaid <human.mmd> --output-markdown <view.md> --session-id <session>
python .workflow/tools/validate_sequence_contract.py --root . --session <session.json>
python .workflow/tools/validate_sequence_human_view.py --root . --session <session.json>
python .workflow/tools/validate_sequence_sessions.py --root .
```

## Governance Engine V2

```text
develop  = targeted intermediate work
verify   = read-only intermediate evidence
finalize = complete final acceptance
```

For final acceptance, provide the accepted base and exact expected candidate HEAD when the project contract requires them.

## Skill Workflow repository hardening

The following commands apply to this producer repository rather than ordinary consumers:

```bash
python scripts/validate_public_docs.py --root .
python scripts/validate_repository_health.py --root .
python scripts/selftest_repository_health.py
python scripts/selftest_github_ruleset.py
python scripts/selftest_release_preflight.py
```

A live GitHub ruleset payload can be checked with:

```bash
python scripts/validate_github_ruleset.py --ruleset <ruleset.json>
```

Release preflight requires an exact finalized candidate and never publishes a release itself:

```bash
python scripts/release_preflight.py \
  --root . \
  --expected-head <EXACT_HEAD> \
  --version <vMAJOR.MINOR.PATCH[-PRERELEASE]> \
  --governance-report <finalize.json>
```

## Upstream regression tests

The Skill Workflow repository includes compiler, STRICT-workflow, governance-engine, cross-document, sequence-resolution, human-sequence, public-documentation, repository-health, live-ruleset-policy, and release-preflight regressions. Consumer projects should run the validators and tests required by their own `PROJECT_PROFILE.yaml` and acceptance contract rather than copying upstream CI blindly.
