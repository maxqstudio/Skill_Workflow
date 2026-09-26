# PROJECT TRUTH SYNC

Generated/refreshed:
Status: IN_PROGRESS

This document is the canonical traceability ledger for critical project claims.

## Provenance policy

Final acceptance binds source and documentation by the exact tested Git HEAD.

Do not attempt to make this tracked file contain the hash of the commit that contains itself.

Acceptance must prove:

TESTED_HEAD = FINAL_SOURCE_HEAD = FINAL_DOCUMENTATION_HEAD
WORKTREE = CLEAN

Record the actual HEAD in generated/external acceptance evidence.

## Truth gates

| Gate | Status | Evidence / Notes |
|---|---|---|
| SOURCE_TESTS | NOT_PROVEN | |
| RUNTIME_E2E | NOT_PROVEN | |
| PROVENANCE_SYNC | NOT_PROVEN | |
| REFERENCE_SYNC | NOT_PROVEN | |
| STRUCTURAL_SYNC | NOT_PROVEN | |
| SEMANTIC_SYNC | NOT_PROVEN | |
| BEHAVIORAL_SYNC | NOT_PROVEN | |
| CROSS_DOCUMENT_CONSISTENCY | NOT_PROVEN | |
| HUMAN_COMPREHENSION | NOT_PROVEN | SYSTEM_OVERVIEW.md + human comprehension validator |
| SEQUENCE_SYNC | NOT_PROVEN | SEQUENCE_CONTRACTS.md + per-session sequence acceptance reports |
| PROJECT_DOCS_SYNC | NOT_PROVEN | Project Truth Compiler check |
| DOC_SOURCE_TRACEABILITY | NOT_PROVEN | |
| DOC_TEST_TRACEABILITY | NOT_PROVEN | |
| TEST_RUNTIME_TRACEABILITY | NOT_PROVEN | |
| PROJECT_STATE_SYNC | NOT_PROVEN | |

Allowed terminal gate values:

PASS
FAIL
NOT_APPLICABLE
NOT_PROVEN

PROJECT_STATE_SYNC may be PASS only when every required upstream gate is PASS or explicitly NOT_APPLICABLE.

## Critical claim traceability

Use stable IDs for authority-bearing claims only.

| Claim ID | Claim | Documents | Source owner(s) | Test(s) | Runtime/E2E evidence | Status |
|---|---|---|---|---|---|---|
| TRUTH-EXAMPLE-001 | Replace with a critical project claim | WORKFLOW_STATE_MACHINE.md | path/to/file.py::symbol | tests/test_file.py | evidence reference or NOT_APPLICABLE | NOT_PROVEN |

### Reference format

Preferred source reference:

relative/path/to/file.ext::symbol_name

Preferred document/test reference:

relative/path/to/file.ext

Multiple references may be separated with semicolons.

## Claim relations

Use this table when two critical claims have an explicit logical relationship.

Allowed relations:

```text
CONFLICTS_WITH
REQUIRES
SAME_AS
SUPERSEDES
```

| Claim ID | Relation | Other Claim ID | Notes |
|---|---|---|---|
| | | | |

Rules:

- `CONFLICTS_WITH`: both claims may not be PASS simultaneously.
- `REQUIRES`: if the first claim is PASS, the required claim must also be PASS.
- `SAME_AS`: terminal PASS/FAIL states must agree.
- `SUPERSEDES`: if the new claim is PASS, the superseded claim must not remain PASS.

## Cross-document consistency audit

| Claim / Area | Documents compared | Result | Notes |
|---|---|---|---|
| | | NOT_PROVEN | |

## Broken / unresolved references

| Reference | Type | Reason | Status |
|---|---|---|---|
| | | | |

## Contradictions

| ID | Document A | Document B / Source | Contradiction | Status |
|---|---|---|---|---|
| | | | | |

## Final counters

STALE_DOCUMENTS:
BROKEN_REFERENCES:
UNRESOLVED_CONTRACTS:
CONTRADICTORY_CLAIMS:

All must be zero for PROJECT_STATE_SYNC=PASS.


## Validator evidence

For final acceptance, record or reference generated reports:

```text
HANDOFF_VALIDATOR:
HUMAN_COMPREHENSION_VALIDATOR:
SEQUENCE_CONTRACT_VALIDATOR:
CROSS_DOCUMENT_VALIDATOR:
PROJECT_TRUTH_VALIDATOR:
CROSS_DOCUMENT_REPORT:
PROJECT_TRUTH_REPORT:
```

Required command for cross-document freshness:

```bash
python scripts/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> \
  --require-base \
  --report artifacts/cross_document_sync_report.json
```

CROSS_DOCUMENT_CONSISTENCY may be set to PASS only when the machine validator passes and semantic/cross-document review finds no unresolved contradiction.


## Human comprehension truth rule

HUMAN_COMPREHENSION may be set to PASS only when:

- SYSTEM_OVERVIEW.md is structurally complete;
- every applicable Human Comprehension Gate question is PASS;
- the overview agrees with CURRENT_STATE, PROJECT_MANIFEST, authority maps,
  workflow/state documentation, and acceptance evidence;
- a reviewer can explain the project without opening source code.

Run:

```bash
python scripts/validate_human_comprehension.py --require-pass
```

Machine validation checks coverage and explicit statuses only. It does not prove
the prose is semantically correct or that a real reader understood it.


## Sequence synchronization truth rule

SEQUENCE_SYNC applies according to PROJECT_PROFILE.yaml.

For each critical phase/session flow:

- BEFORE requires a frozen plan that Git proves existed before implementation,
  generated plan Mermaid, generated actual graph/diagram, and PLAN ↔ ACTUAL
  acceptance.
- DURING forbids retrospective plans and requires generated ACTUAL ↔ SOURCE /
  TEST / RUNTIME evidence.
- AFTER forbids retrospective plans and requires generated FINAL ACTUAL ↔
  SOURCE / TEST / RUNTIME evidence.

Canonical Mermaid diagrams are generated files and must not be hand-edited.

Run each applicable session through:

```bash
python scripts/validate_sequence_contract.py \
  --session docs/sequence/sessions/<session>.json
```

SEQUENCE_SYNC may be PASS only when every required critical sequence session
passes and no unresolved critical edge/binding remains.

A mismatch must first be classified as one of:

```text
CODE_DEFECT
PLAN_CHANGE
GENERATOR_DEFECT
```

Then repair the correct authority, regenerate, and validate again.


## Generated documentation truth rule

When PROJECT_PROFILE.yaml enables generated documentation:

- canonical project Markdown under `docs/` is a deterministic projection;
- semantic/governance intent lives under .workflow/;
- implementation facts come from source extractors;
- manual edits to generated Markdown are not authority;
- python scripts/validate_project_docs.py must PASS.

PROJECT_DOCS_SYNC may be PASS only when the compiler reproduces tracked
documentation and generated code facts exactly from the current upstream inputs.
