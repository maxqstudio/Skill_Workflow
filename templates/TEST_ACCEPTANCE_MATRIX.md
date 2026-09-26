# TEST ACCEPTANCE MATRIX

Authority SHA:
Last executed:

| Requirement | Unit | Integration | Runtime | UI/E2E | Physical | Production | Status | Evidence |
|---|---|---|---|---|---|---|---|---|

Allowed status vocabulary:
PASS
FAIL
NOT_RUN
NOT_APPLICABLE
NOT_PROVEN
BLOCKED

## Evidence boundary
State explicitly what the current evidence proves and does not prove.

## Final tested source
Final source SHA:
Tested SHA:
Match:


## Human comprehension evidence

SYSTEM_OVERVIEW status:
HUMAN_COMPREHENSION_GATE:
Reviewer / audit authority:
Validator:

Required command:

```bash
python scripts/validate_human_comprehension.py --require-pass
```

A validator PASS proves structural coverage and explicit checklist status only.
Semantic review must confirm the overview agrees with current project authority,
workflow, tests, and runtime evidence.


## Sequence contract evidence

Sequence policy: see PROJECT_PROFILE.yaml
Sequence mode for this phase/session: BEFORE / DURING / AFTER
Sequence session contract:
Sequence acceptance report:
SEQUENCE_SYNC: PASS / FAIL / NOT_PROVEN / NOT_APPLICABLE

BEFORE requires:

```text
PLAN_EXISTS
PLAN_FROZEN
PLAN_PRECEDES_IMPLEMENTATION
PLAN_HASH_MATCH
PLAN_DIAGRAM_GENERATED
ACTUAL_GRAPH_GENERATED
ACTUAL_DIAGRAM_GENERATED
PLAN_ACTUAL_MATCH
```

DURING and AFTER require:

```text
PLAN = NOT_APPLICABLE
ACTUAL_GRAPH_GENERATED
ACTUAL_DIAGRAM_GENERATED
ACTUAL_SOURCE_DIGEST = CURRENT_SOURCE_DIGEST
SOURCE_ACTUAL_SYNC = PASS
```

For critical flows also record test traceability and runtime sequence evidence
when required by project/session policy.

Required validator:

```bash
python scripts/validate_sequence_contract.py \
  --session docs/sequence/sessions/<session>.json
```

Generated Mermaid is a view of machine-readable graph state. Do not use manual
diagram edits as acceptance evidence.


## Project Truth Compiler evidence

Documentation mode:
Semantic spec root:
Generated source facts:
PROJECT_DOCS_SYNC: PASS / FAIL / NOT_PROVEN / NOT_APPLICABLE

Required command when generated documentation is enabled:

    python scripts/validate_project_docs.py

This gate proves deterministic projection/freshness only. It does not create
missing semantic intent and does not replace source/test/runtime verification.
