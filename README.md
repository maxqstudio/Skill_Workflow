# Skill Workflow

Reusable workflow skill for understanding, handing off, auditing, repairing, and continuing software projects across ChatGPT rooms, coding agents, and human developers.

## Start here

Use **`SKILL.md`** as the current canonical version.

The skill defines a documentation and execution contract built around:

- project authority and exact source revisions;
- architecture and workflow/state-machine mapping;
- module, symbol, and end-to-end flow indexes;
- targeted source navigation instead of blind full-codebase rescans;
- test/acceptance evidence boundaries;
- runtime/E2E verification;
- safe project handoff between rooms or agents.

## Core handoff pack

The canonical skill recommends these project documents:

```text
PROJECT_MANIFEST.md
CURRENT_STATE.md
SOURCE_AUTHORITY_MAP.md
ARCHITECTURE.md
WORKFLOW_STATE_MACHINE.md
MODULE_MAP.md
SYMBOL_INDEX.md
FLOW_INDEX.md
TEST_ACCEPTANCE_MATRIX.md
```

Additional contracts such as data, API, UI information architecture, runbooks, decisions, glossary, defects, and changelog can be added as needed.

## Versions

- `SKILL.md` — current canonical skill.
- `versions/SKILL_V1.md` — original version before symbol/flow indexing was added.

## Design goal

A new room or agent should be able to understand where authority lives, what the current state is, which exact code symbols implement a workflow, what has actually been proven, and what action is legal next — without reconstructing the project from old chat history or reading the entire codebase blindly.
