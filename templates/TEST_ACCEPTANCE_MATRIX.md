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
