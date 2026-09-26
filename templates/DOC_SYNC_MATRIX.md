# DOCUMENTATION SYNC MATRIX

Authority SHA:
Last reviewed:
Governance profile: see PROJECT_PROFILE.yaml

This matrix defines which applicable documentation must move transactionally with source changes.

## Profile rule

PROJECT_PROFILE.yaml determines which documents are required, optional, or not applicable.

A validator must not force a not_applicable document into existence.

An existing optional contract that is actively maintained is still subject to
drift checks when related source changes.

STRICT requires explicit applicability decisions for critical optional contracts.

## Hard rule

```text
SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL
```

A source change that makes applicable project documentation stale is a project defect.

| Change type | Required documentation when applicable |
|---|---|
| Function/class/component added, moved, renamed, removed, or authority changed | SYMBOL_INDEX.md |
| File/module responsibility or ownership changed | MODULE_MAP.md + SYMBOL_INDEX.md |
| End-to-end call path changed | FLOW_INDEX.md + SYMBOL_INDEX.md |
| Lifecycle/state transition changed | SYSTEM_OVERVIEW.md when human-visible behavior changes + WORKFLOW_STATE_MACHINE.md + FLOW_INDEX.md + TEST_ACCEPTANCE_MATRIX.md |
| Public API/event contract changed | SYSTEM_OVERVIEW.md when user/domain flow changes + API_CONTRACTS.md + FLOW_INDEX.md + TEST_ACCEPTANCE_MATRIX.md |
| Database/schema/data semantics changed | SYSTEM_OVERVIEW.md when human-visible data meaning/flow changes + DATA_CONTRACTS.md + MODULE_MAP.md + TEST_ACCEPTANCE_MATRIX.md |
| UI workspace/page/action/authority changed | SYSTEM_OVERVIEW.md when main user workflow changes + UI_INFORMATION_ARCHITECTURE.md + FLOW_INDEX.md when call path changes |
| Architecture/dependency/runtime boundary changed | SYSTEM_OVERVIEW.md + ARCHITECTURE.md + SOURCE_AUTHORITY_MAP.md when authority changes |
| Runtime/start/build/recovery procedure changed | RUNBOOK.md |
| Test/evidence behavior changed | TEST_ACCEPTANCE_MATRIX.md |
| Candidate/phase/current SHA/blocker/next action changed | SYSTEM_OVERVIEW.md current-state summary + CURRENT_STATE.md |
| Source/runtime/data/UI/acceptance authority changed | SOURCE_AUTHORITY_MAP.md + CURRENT_STATE.md |
| Durable architectural/governance decision changed | DECISIONS.md |
| Confirmed/fixed defect state changed | KNOWN_DEFECTS.md |
| User-facing project history/release summary changed | CHANGELOG.md when maintained |
| New/removed critical project area | SYSTEM_OVERVIEW.md + PROJECT_MANIFEST.md + relevant maps/indexes |

## Generated structural facts

Before manually editing structural indexes, regenerate machine facts where applicable:

```bash
python scripts/generate_symbol_index.py
python scripts/generate_module_map.py
```

Generated facts reduce manual drift but do not replace semantic documentation.

## Mandatory DOC IMPACT declaration

Before source modification:

```text
DOC IMPACT
system overview: YES/NO
architecture: YES/NO
workflow/state machine: YES/NO
module map: YES/NO
symbol index: YES/NO
flow index: YES/NO
API contract: YES/NO
data contract: YES/NO
UI information architecture: YES/NO
runbook: YES/NO
test acceptance matrix: YES/NO
current state: YES
decisions: YES/NO
known defects: YES/NO
```

Every NO must be supported by the actual change scope and project profile.

## Post-change gate

Before final PASS:

1. inspect changed source files and symbols;
2. map each change using this matrix and PROJECT_PROFILE.yaml;
3. regenerate structural facts where applicable;
4. confirm every required/applicable document was updated or explicitly remains valid;
5. verify indexed symbols and flows still resolve;
6. verify CURRENT_STATE reflects actual repository/branch/SHA/phase;
7. verify TEST_ACCEPTANCE_MATRIX contains only evidence actually executed;
8. run `python scripts/validate_human_comprehension.py --require-pass`;
9. run the remaining profile-aware validators;
10. reject completion if applicable documentation is stale.

## Project Truth Synchronization

For STRICT, or when PROJECT_TRUTH_SYNC.md is present for critical flows, verify:

```text
documentation ↔ source ↔ tests ↔ runtime/E2E evidence
```

Final acceptance requires every gate required by the selected profile to pass.

## Cross-document validation gate

For final acceptance:

```bash
python scripts/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> \
  --require-base \
  --report artifacts/cross_document_sync_report.json
```

A machine PASS is necessary but not sufficient for semantic correctness.


## Human comprehension sync rule

SYSTEM_OVERVIEW.md is a human-facing semantic contract, not a marketing summary.

Update it when a change materially alters:

- project purpose or user outcome;
- major component boundaries;
- important data flow;
- main user/domain workflows;
- lifecycle semantics;
- authority boundaries;
- mutable vs immutable behavior;
- failure/recovery behavior;
- current phase, blockers, or next legal action.

Do not update it for trivial internal refactors that do not change the human
mental model.

Final documentation acceptance requires:

```text
python scripts/validate_human_comprehension.py --require-pass
```

A structural PASS is necessary but does not replace semantic review.
