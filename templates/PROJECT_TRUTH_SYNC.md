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
