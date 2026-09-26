# SYSTEM OVERVIEW

Status: CURRENT
Human comprehension status: NOT_PROVEN

This document is the human-first explanation of the project.

A reader should be able to understand what the system is, how it works, what
moves through it, who owns important decisions, what is mutable/immutable, and
what the current project state means without opening source code.

Avoid implementation-detail overload. Link to engineering documents for drill-down.

## One-minute summary

What is this project?

What problem does it solve?

Who uses it?

What is the expected outcome?

## System at a glance

Provide a simple component-level view.

Recommended form:

```text
User / External Input
        ↓
Application / Control Surface
        ↓
Core Domain / Workflow
        ↓
Data / State / Evidence
        ↓
External Runtime / Output
```

Use project-specific names.

## Major components

| Component | Purpose | Owns / Decides | Depends On |
|---|---|---|---|

Explain components in human language before naming internal modules.

## Main data flow

Explain how important information enters, moves through, is validated, is
persisted, and becomes output/evidence.

A reader should understand:

- where data originates;
- what validates it;
- where mutable state lives;
- where immutable evidence lives;
- what external systems participate;
- where final outputs go.

## Main user workflows

Describe the important end-to-end workflows in user/domain terms.

Example style:

```text
User starts action
→ system validates prerequisites
→ system performs domain operation
→ state/evidence is persisted
→ user sees resulting state
```

Do not require function names to understand the workflow.

## Lifecycle and state

Explain the important states and legal transitions.

Include only the state machines a human needs to understand system behavior.
Link to WORKFLOW_STATE_MACHINE.md for exhaustive transition detail.

## Authority model

| Concern | Authority | Meaning |
|---|---|---|

Explain who or what is allowed to decide:

- source truth;
- runtime truth;
- mutable state;
- configuration;
- irreversible/privileged actions;
- scientific/business evidence;
- user approval when applicable.

## Mutable vs immutable

### Mutable current state

What may legally change?

### Immutable history / evidence

What must never be silently rewritten?

### Configuration vs execution snapshot

If applicable, explain which settings are editable now and which values become
frozen once an execution starts.

## Failure and recovery

Explain in human language:

- what fails closed;
- what can retry safely;
- what must not auto-retry;
- what survives restart;
- how recovery preserves authority/evidence.

## Current project state

Summarize:

- current phase;
- last accepted state;
- current candidate/work;
- blockers;
- next authorized action;
- prohibited/blocked actions.

Do not duplicate large evidence logs. Link to CURRENT_STATE.md.

## Proven vs not proven

### Proven

-

### Not proven

-

Do not convert NOT_RUN or historical evidence into current PASS.

## Important limitations

-

## Glossary

Define only terms necessary to understand this overview. Link to GLOSSARY.md
when the project has a larger vocabulary.

## Where to read deeper

| Need | Document |
|---|---|
| Current live project state | CURRENT_STATE.md |
| Project identity and authorities | PROJECT_MANIFEST.md |
| Architecture | ARCHITECTURE.md |
| Full lifecycle rules | WORKFLOW_STATE_MACHINE.md |
| End-to-end engineering call paths | FLOW_INDEX.md |
| Module ownership | MODULE_MAP.md |
| Exact source symbols | SYMBOL_INDEX.md |
| APIs | API_CONTRACTS.md |
| Data semantics | DATA_CONTRACTS.md |
| Acceptance evidence | TEST_ACCEPTANCE_MATRIX.md |
| Critical truth traceability | PROJECT_TRUTH_SYNC.md |

Only link to documents applicable to the selected PROJECT_PROFILE.

## Human comprehension gate

A reviewer must be able to answer every question below using project
documentation, with SYSTEM_OVERVIEW.md as the primary source, without opening
source code.

| Question | Status | Answer location |
|---|---|---|
| What is the project and what problem does it solve? | NOT_PROVEN | |
| Who uses it and what are the primary outcomes? | NOT_PROVEN | |
| What are the major components and how do they relate? | NOT_PROVEN | |
| How does important data flow through the system? | NOT_PROVEN | |
| What are the main user/domain workflows? | NOT_PROVEN | |
| What are the important lifecycle states and transitions? | NOT_PROVEN | |
| Who/what is authoritative for important decisions? | NOT_PROVEN | |
| What is mutable and what is immutable? | NOT_PROVEN | |
| How does failure/recovery behave? | NOT_PROVEN | |
| What is the current project state? | NOT_PROVEN | |
| What is proven and what is not proven? | NOT_PROVEN | |
| What may happen next and what is blocked? | NOT_PROVEN | |

Allowed values:

```text
PASS
FAIL
NOT_PROVEN
NOT_APPLICABLE
```

Final rule:

```text
all applicable questions = PASS
+
no unresolved contradiction with current authority docs
=
HUMAN_COMPREHENSION_GATE = PASS
```

Set the document-level line:

```text
Human comprehension status: PASS
```

only after semantic review.

A machine validator may prove structural coverage, but it cannot prove that a
human truly understood the system or that the prose is semantically correct.
