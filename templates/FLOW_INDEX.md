# FLOW INDEX

Authority SHA:
Generated/refreshed:
Status: CURRENT

This file maps an end-to-end behavior to exact source symbols.

## Flow template

### FLOW: <name>

Purpose:

Entry point:
- file:
- symbol:

API / Event:
- file:
- symbol:

Service / Domain:
- file:
- symbol:

State transition:
- file:
- symbol:

Database / Artifact write:
- file:
- symbol:

External side effect:
- file:
- symbol:

Fail-closed / error path:
- file:
- symbol:

Tests:
-

Sequence contract:
- session:
- mode: BEFORE / DURING / AFTER
- generated actual graph:
- acceptance report:

## Flow inventory
| Flow | Entry | Authority symbol | State mutation | Tests | Sequence session | Sequence status |
|---|---|---|---|---|---|---|

## Editing order
WORKFLOW_STATE_MACHINE
→ SEQUENCE CONTRACT
→ FLOW_INDEX
→ SYMBOL_INDEX
→ exact source ranges
→ tests.


## Sequence alignment rule

Each critical flow should use the same stable FLOW ID across:

```text
WORKFLOW_STATE_MACHINE
SEQUENCE_CONTRACTS
FLOW_INDEX
PROJECT_TRUTH_SYNC
TEST_ACCEPTANCE_MATRIX
```

For BEFORE mode, the sequence session points to a frozen pre-implementation plan
plus generated actual evidence.

For DURING/AFTER, the session points only to generated actual evidence.

FLOW_INDEX remains the semantic engineering map. Generated sequence graphs are
machine observations and must agree with the semantic flow before acceptance.
