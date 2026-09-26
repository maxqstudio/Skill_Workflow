# DOCUMENTATION SYNC MATRIX

## Generated documentation mode

For STANDARD and STRICT projects, documentation is compiled from upstream
authorities instead of being maintained manually.

Canonical transaction:

```text
SOURCE CODE
+ .workflow SEMANTIC / GOVERNANCE SPECS
+ TEST / RUNTIME EVIDENCE STATE
→ PROJECT TRUTH COMPILER
→ GENERATED MARKDOWN
```

Generated Markdown is a projection. It MUST NOT be edited as the primary repair.

## Upstream change map

| Change type | Upstream authority to update | Generated projections |
|---|---|---|
| Project identity, purpose, users, outcomes | .workflow/project.json | PROJECT_MANIFEST.md + SYSTEM_OVERVIEW.md |
| Authority, mutability, invariants | .workflow/authority.json | SOURCE_AUTHORITY_MAP.md + SYSTEM_OVERVIEW.md |
| Current phase, blockers, next/blocked action | .workflow/state.json | CURRENT_STATE.md + SYSTEM_OVERVIEW.md |
| Architecture/component/data-flow meaning | .workflow/architecture.json | ARCHITECTURE.md + SYSTEM_OVERVIEW.md |
| Workflow/lifecycle semantics | .workflow/workflows/*.json | WORKFLOW_STATE_MACHINE.md + FLOW_INDEX.md + SYSTEM_OVERVIEW.md |
| Sequence policy/session | docs/sequence/* + .workflow/acceptance.json | SEQUENCE_CONTRACTS.md + TEST_ACCEPTANCE_MATRIX.md |
| API/data/UI/runbook semantics | .workflow/contracts.json | API_CONTRACTS.md / DATA_CONTRACTS.md / UI_INFORMATION_ARCHITECTURE.md / RUNBOOK.md |
| Critical truth claims and relations | .workflow/claims.json | PROJECT_TRUTH_SYNC.md |
| Test/runtime/evidence status | .workflow/acceptance.json | TEST_ACCEPTANCE_MATRIX.md + CURRENT_STATE.md + PROJECT_TRUTH_SYNC.md |
| Durable design decision | .workflow/decisions.json | DECISIONS.md |
| Known defect lifecycle | .workflow/known_defects.json | KNOWN_DEFECTS.md |
| Glossary meaning | .workflow/glossary.json | GLOSSARY.md |
| Changelog/release history | .workflow/changelog.json | CHANGELOG.md |
| Implementation structure | source code | MODULE_MAP.md + SYMBOL_INDEX.md + observed FLOW_INDEX facts |

## Required workflow

```text
declare DOC IMPACT
→ update source and/or .workflow authority
→ generate code facts
→ generate project docs
→ generate/validate sequence evidence when applicable
→ test
→ update evidence state
→ regenerate
→ validate_project_docs.py
→ cross-document validation
→ final runtime/E2E when required
→ final regeneration + validation
```

## Hard gate

When generated documentation is enabled:

```text
PROJECT_DOCS_SYNC = PASS
```

is required.

If compiler output differs from tracked docs:

```text
PROJECT_DOCS_SYNC = FAIL
OVERALL STATUS = REPAIR REQUIRED — GENERATED DOCUMENTATION DRIFT
```

Repair the upstream source/spec, then regenerate.

## Manual mode

LITE may explicitly set:

```yaml
documentation:
  generated: false
```

In manual mode, the legacy per-document freshness rules apply.

## Sequence contract sync

When sequence policy is enabled, flow-changing work is incomplete until the
applicable BEFORE / DURING / AFTER session contract is validated.

Mismatch classification:

```text
CODE_DEFECT
PLAN_CHANGE
GENERATOR_DEFECT
```

Do not blindly modify source to satisfy a generated comparison.

## Required validators

```bash
python .workflow/tools/validate_project_docs.py
python .workflow/tools/validate_handoff.py
python .workflow/tools/validate_human_comprehension.py --require-pass
python .workflow/tools/validate_sequence_sessions.py
python .workflow/tools/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> --require-base
```

For STRICT, or when PROJECT_TRUTH_SYNC.md exists:

```bash
python .workflow/tools/validate_project_truth.py
```

A validator PASS proves only its stated machine-verifiable scope. It does not
replace semantic or runtime evidence.
