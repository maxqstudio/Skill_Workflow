# DOCUMENTATION SYNC MATRIX

Authority SHA:
Last reviewed:

This matrix defines which documentation must move transactionally with source changes.

## Hard rule

```text
SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL
```

A source change that makes project documentation stale is a project defect.

| Change type | Required documentation |
|---|---|
| Function/class/component added, moved, renamed, removed, or authority changed | SYMBOL_INDEX.md |
| File/module responsibility or ownership changed | MODULE_MAP.md + SYMBOL_INDEX.md |
| End-to-end call path changed | FLOW_INDEX.md + SYMBOL_INDEX.md |
| Lifecycle/state transition changed | WORKFLOW_STATE_MACHINE.md + FLOW_INDEX.md + TEST_ACCEPTANCE_MATRIX.md |
| Public API/event contract changed | API_CONTRACTS.md + FLOW_INDEX.md + TEST_ACCEPTANCE_MATRIX.md |
| Database/schema/data semantics changed | DATA_CONTRACTS.md + MODULE_MAP.md + TEST_ACCEPTANCE_MATRIX.md |
| UI workspace/page/action/authority changed | UI_INFORMATION_ARCHITECTURE.md + FLOW_INDEX.md when call path changes |
| Architecture/dependency/runtime boundary changed | ARCHITECTURE.md + SOURCE_AUTHORITY_MAP.md when authority changes |
| Runtime/start/build/recovery procedure changed | RUNBOOK.md |
| Test/evidence behavior changed | TEST_ACCEPTANCE_MATRIX.md |
| Candidate/phase/current SHA/blocker/next action changed | CURRENT_STATE.md |
| Source/runtime/data/UI/acceptance authority changed | SOURCE_AUTHORITY_MAP.md + CURRENT_STATE.md |
| Durable architectural/governance decision changed | DECISIONS.md |
| Confirmed/fixed defect state changed | KNOWN_DEFECTS.md |
| User-facing project history/release summary changed | CHANGELOG.md when maintained by project |
| New/removed critical project area | PROJECT_MANIFEST.md + relevant maps/indexes |

## Mandatory DOC IMPACT declaration

Before source modification:

```text
DOC IMPACT
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

Every NO must be supported by the actual change scope.

## Post-change gate

Before final PASS:

1. inspect changed source files and symbols;
2. map each change using this matrix;
3. confirm every required document was updated or explicitly remains valid;
4. verify SYMBOL_INDEX symbols still resolve;
5. verify FLOW_INDEX call paths still resolve;
6. verify CURRENT_STATE reflects actual repository/branch/SHA/phase;
7. verify TEST_ACCEPTANCE_MATRIX contains only evidence actually executed;
8. run the handoff validator when available;
9. reject completion if required documentation is stale.

## Final status

```text
DOC_SYNC = PASS
```

is required for overall PASS.

## Project Truth Synchronization requirement

DOC_SYNC is necessary but not sufficient.

After applying this matrix, the agent must also maintain PROJECT_TRUTH_SYNC.md and verify affected critical claims across:

documentation ↔ source ↔ tests ↔ runtime/E2E evidence when required.

For every change that affects an authority-bearing behavior, invariant, lifecycle, external contract, data meaning, or runtime behavior:

- update or add the affected truth claim;
- verify source owner references;
- verify relevant tests;
- verify runtime evidence when required;
- check related documents for contradictions;
- reject PASS if semantics are NOT_PROVEN.

Final acceptance requires both:

DOC_SYNC = PASS
PROJECT_STATE_SYNC = PASS


## Cross-document validation gate

Before final PASS, run the cross-document validator against the accepted/base SHA:

```bash
python scripts/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> \
  --require-base \
  --report artifacts/cross_document_sync_report.json
```

The validator checks the whole Markdown documentation set for references, stable-claim conflicts, duplicate core docs, selected authority conflicts, explicit stale markers, and required documentation left behind by source changes.

A machine PASS is necessary but not sufficient for semantic correctness.

Final acceptance requires:

```text
DOC_SYNC = PASS
CROSS_DOCUMENT_CONSISTENCY = PASS
PROJECT_STATE_SYNC = PASS
```
