# Skill Workflow

A reusable project-handoff and codebase-orientation skill for ChatGPT rooms, coding agents, and human developers.

The goal is simple: **let a new room or agent understand a project safely without rereading the entire codebase from scratch.**

It focuses on:

- exact project authority;
- current source/runtime state;
- architecture and workflow/state-machine mapping;
- module, symbol, and end-to-end flow indexing;
- targeted source navigation;
- evidence-based testing and acceptance;
- safe handoff between rooms, agents, and developers;
- preventing accidental redesign, stale assumptions, and false PASS results.

---

## Install

The repository uses the open `skills` CLI, which can target Codex, Claude Code, Cursor, Gemini CLI, GitHub Copilot, OpenCode, and many other supported coding agents.

Install interactively:

```bash
npx skills add maxqstudio/Skill_Workflow
```

or:

```bash
npx skills add https://github.com/maxqstudio/Skill_Workflow
```

### OpenAI Codex

Project-local:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -y
```

Global:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -g -y
```

### Claude Code

Project-local:

```bash
npx skills add maxqstudio/Skill_Workflow -a claude-code -y
```

Global:

```bash
npx skills add maxqstudio/Skill_Workflow -a claude-code -g -y
```

### Codex + Claude Code together

Project-local:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -a claude-code -y
```

Global:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -a claude-code -g -y
```

### Other common coding agents

Cursor:

```bash
npx skills add maxqstudio/Skill_Workflow -a cursor -y
```

Gemini CLI:

```bash
npx skills add maxqstudio/Skill_Workflow -a gemini-cli -y
```

GitHub Copilot:

```bash
npx skills add maxqstudio/Skill_Workflow -a github-copilot -y
```

OpenCode:

```bash
npx skills add maxqstudio/Skill_Workflow -a opencode -y
```

Qwen Code:

```bash
npx skills add maxqstudio/Skill_Workflow -a qwen-code -y
```

Roo Code:

```bash
npx skills add maxqstudio/Skill_Workflow -a roo -y
```

Windsurf:

```bash
npx skills add maxqstudio/Skill_Workflow -a windsurf -y
```

Cline:

```bash
npx skills add maxqstudio/Skill_Workflow -a cline -y
```

### Install to multiple agents

Example:

```bash
npx skills add maxqstudio/Skill_Workflow \
  -a codex \
  -a claude-code \
  -a cursor \
  -a gemini-cli \
  -a github-copilot \
  -a opencode \
  -y
```

To install all skills in this repository to all supported/detected agents:

```bash
npx skills add maxqstudio/Skill_Workflow --all
```

### Project-local vs global

Project-local is the default and is recommended when the skill should travel with one repository.

Global installation uses `-g` and makes the skill available across projects for that agent.

Examples of agent paths managed by the `skills` CLI include:

| Agent | Project path | Global path |
|---|---|---|
| Codex | `.agents/skills/` | `~/.codex/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |

Update installed skills later with:

```bash
npx skills update
```

The canonical skill is:

```text
SKILL.md
```

---

## What this skill solves

Large projects become difficult to continue when a new room or agent has to reconstruct everything from:

- old chat history;
- thousands of source lines;
- stale documentation;
- unclear branch/SHA authority;
- undocumented runtime assumptions;
- incomplete test evidence.

Skill Workflow introduces a standard project map so the next room can answer:

```text
What is this project?
What is authoritative?
What exact SHA is current?
What phase is active?
What is the workflow/state machine?
Which module owns a behavior?
Which exact function/class implements it?
What is the end-to-end call path?
What has actually been tested?
What is not yet proven?
What is broken?
What action is legal next?
```

without blindly scanning the whole repository.

---

## Core reading workflow

The skill uses this orientation sequence:

```text
PROJECT_PROFILE
→ CURRENT_STATE
→ PROJECT_MANIFEST
→ profile-required authority / architecture / workflow docs
→ profile-required MODULE / FLOW / SYMBOL maps
→ TEST_ACCEPTANCE_MATRIX
→ exact relevant source ranges
→ runtime / E2E verification when required
```

The idea is to **read the map first, then the code that matters**.

---

## Adaptive governance profiles

The skill no longer forces the same document pack on every project.

Every project starts with:

```text
PROJECT_PROFILE.yaml
```

### LITE

For small, low-complexity projects.

Required:

```text
PROJECT_PROFILE.yaml
PROJECT_MANIFEST.md
CURRENT_STATE.md
MODULE_MAP.md
TEST_ACCEPTANCE_MATRIX.md
```

### STANDARD

Default for normal multi-session / multi-agent development.

Required:

```text
PROJECT_PROFILE.yaml
PROJECT_MANIFEST.md
CURRENT_STATE.md
SOURCE_AUTHORITY_MAP.md
ARCHITECTURE.md
WORKFLOW_STATE_MACHINE.md
MODULE_MAP.md
SYMBOL_INDEX.md
FLOW_INDEX.md
TEST_ACCEPTANCE_MATRIX.md
DOC_SYNC_MATRIX.md
```

### STRICT

For financial/trading, ML/research, hardware, production infrastructure, safety/audit-sensitive work, or complex multi-repository projects.

STRICT requires all STANDARD docs plus:

```text
PROJECT_TRUTH_SYNC.md
```

It also forces explicit applicability decisions for critical optional contracts.

Profile choice is based on **risk and workflow complexity**, not simply repository size.

Ready-to-copy templates are available under `templates/`.

---

## Why SYMBOL_INDEX matters

`SYMBOL_INDEX.md` acts like a **table of contents for the codebase**.

Instead of opening a 3,000-line file and searching manually, the index can point directly to:

```text
file: backend/promotion_service.py
symbol: promote_candidate()
kind: function
lines@SHA: 675-980
responsibility: Candidate → Champion promotion
reads/writes: lifecycle state + promotion evidence
tests: test_promotion.py
```

Recommended index fields:

| File | Symbol | Kind | Lines@SHA | Responsibility | Reads/Writes | Called By | Tests |
|---|---|---|---|---|---|---|---|

The symbol name is the primary locator.

Line numbers are only navigation hints and should be tied to an exact source SHA.

---

## Automatic structural indexing

Two generators reduce manual documentation overhead:

```bash
python scripts/generate_symbol_index.py
python scripts/generate_module_map.py
```

`generate_symbol_index.py`:

- prefers Universal Ctags for broad language coverage;
- falls back to Python AST when Ctags is unavailable;
- records file, symbol, kind, line range, language, and source engine;
- never invents semantic responsibility.

`generate_module_map.py` records machine-verifiable file/module facts such as path, language, line count, and directory.

Generated facts are inputs to the canonical semantic docs. The agent still owns:

- responsibility;
- authority;
- state ownership;
- side effects;
- workflow meaning;
- test/evidence interpretation.

`FLOW_INDEX.md` remains semantic-verified instead of blindly auto-generated because DI, callbacks, reflection, dynamic dispatch, and framework routing can make static call graphs misleading.

---

## Why FLOW_INDEX matters

`FLOW_INDEX.md` maps an **end-to-end behavior to its complete call chain**.

Example:

```text
FLOW: Promote Candidate

UI
frontend/CandidatesPage.tsx
  confirmPromotion()

API
backend/candidate_api.py
  promote()

SERVICE
backend/promotion_service.py
  promote_candidate()

STATE COMMIT
backend/champion_store.py
  commit_promotion_authority()

TESTS
backend/tests/test_promotion.py
```

This lets an agent immediately see which layers participate in a workflow before editing anything.

Recommended editing order:

```text
WORKFLOW_STATE_MACHINE
→ FLOW_INDEX
→ SYMBOL_INDEX
→ exact source ranges
→ relevant tests
```

---

## Included templates

### Core / profile templates

- `PROJECT_PROFILE.yaml`
- `PROJECT_MANIFEST.md`
- `CURRENT_STATE.md`
- `SOURCE_AUTHORITY_MAP.md`
- `ARCHITECTURE.md`
- `WORKFLOW_STATE_MACHINE.md`
- `MODULE_MAP.md`
- `SYMBOL_INDEX.md`
- `FLOW_INDEX.md`
- `TEST_ACCEPTANCE_MATRIX.md`
- `DOC_SYNC_MATRIX.md`
- `PROJECT_TRUTH_SYNC.md`

### Additional contracts

- `DATA_CONTRACTS.md`
- `API_CONTRACTS.md`
- `UI_INFORMATION_ARCHITECTURE.md`
- `RUNBOOK.md`
- `DECISIONS.md`
- `GLOSSARY.md`
- `KNOWN_DEFECTS.md`
- `CHANGELOG.md`

Not every project needs every optional file.

---

## Key principles

### 1. Exact authority

Always know:

```text
repository
branch
exact SHA
runtime authority
acceptance authority
data authority
UI authority
historical/reference authority
```

If two authorities conflict, do not guess.

---

### 2. Do not blindly scan the whole codebase

Use:

```text
MODULE_MAP
→ FLOW_INDEX
→ SYMBOL_INDEX
→ exact source range
```

Expand outward only when the index is stale, incomplete, contradictory, or the task requires a full audit.

---

### 3. Source changed does not mean PASS

A safe repair workflow is:

```text
identify exact parent SHA
→ reproduce defect
→ determine root cause
→ minimum valid repair
→ targeted regression
→ cumulative regression
→ runtime/E2E verification when required
→ verify final tested SHA
→ final audit
```

Critical invariant:

```text
FINAL SOURCE SHA
=
TESTED SHA
```

---

### 4. Acceptance must match the evidence

Examples:

```text
Unit PASS
≠ Runtime PASS

Runtime starts
≠ UI/E2E PASS

UI/E2E PASS
≠ Physical-device PASS

Historical physical proof
≠ Current physical execution

Build success
≠ Scientific validity
```

Never convert `NOT_RUN` into `PASS`.

---

### 5. Active state is not history

Keep these concepts separate:

```text
ACTIVE STATE
HISTORICAL EVIDENCE
ARCHIVE
```

Historical evidence should usually remain immutable even when an object leaves an active workflow.

---

### 6. Configuration is not execution history

Separate:

```text
CURRENT CONFIGURATION
from
FROZEN EXECUTION SNAPSHOT
```

Changing a setting should not rewrite evidence from an execution that already happened.

---

### 7. Frontend should display truth, not create truth

Correct:

```text
backend/domain authority
→ API
→ semantic user-facing representation
→ UI
```

Wrong:

```text
frontend hardcoded lifecycle state
→ apparent project truth
```

---

### 8. Prevent accidental redesign

Architecture, UI, or workflow changes should require one of:

- a confirmed defect;
- an explicit owner request;
- an accepted roadmap change.

Otherwise, preserve the accepted design.

---

## Agent discipline: docs are a hard gate

This skill treats documentation as **part of project state**, not as optional notes.

The core invariant is:

```text
SOURCE PASS + DOC_SYNC FAIL
=
OVERALL FAIL
```

Before changing source, an agent declares documentation impact:

```text
architecture: YES/NO
workflow/state machine: YES/NO
module map: YES/NO
symbol index: YES/NO
flow index: YES/NO
API contract: YES/NO
data contract: YES/NO
UI information architecture: YES/NO
test acceptance matrix: YES/NO
current state: YES
decisions: YES/NO
known defects: YES/NO
```

The agent then uses `DOC_SYNC_MATRIX.md` to determine which documents MUST be updated.

Examples:

| Source change | Required docs |
|---|---|
| function/class added, moved, renamed, or authority changed | `SYMBOL_INDEX.md` |
| module responsibility changes | `MODULE_MAP.md` |
| call chain changes | `FLOW_INDEX.md` |
| lifecycle/state transition changes | `WORKFLOW_STATE_MACHINE.md` + `FLOW_INDEX.md` |
| endpoint contract changes | `API_CONTRACTS.md` + `FLOW_INDEX.md` |
| database/schema/data semantics change | `DATA_CONTRACTS.md` |
| UI page/action/authority changes | `UI_INFORMATION_ARCHITECTURE.md` |
| architecture/dependency changes | `ARCHITECTURE.md` |
| test/evidence changes | `TEST_ACCEPTANCE_MATRIX.md` |
| candidate/phase/blocker changes | `CURRENT_STATE.md` |
| durable architectural decision changes | `DECISIONS.md` |

Before final PASS, the agent performs a **documentation drift audit**.

The repository includes:

```bash
python scripts/validate_handoff.py
```

The validator checks structural handoff requirements. A validator PASS does not replace semantic review, but a validator FAIL blocks completion.

The disciplined flow is:

```text
READ PROJECT_PROFILE
→ READ AUTHORITY
→ DECLARE DOC IMPACT
→ EDIT
→ REGENERATE STRUCTURAL FACTS
→ UPDATE SEMANTIC DOCS + INDEXES
→ TEST
→ DOC DRIFT VALIDATION
→ RUNTIME/E2E
→ UPDATE ACCEPTANCE MATRIX
→ UPDATE CURRENT STATE
→ FINAL HANDOFF
```

---

## Project Truth Synchronization

Matching a documentation SHA to a repository revision is not enough.

This skill now requires a broader truth gate:

```text
PROVENANCE
+ REFERENCES
+ STRUCTURE
+ SEMANTICS
+ BEHAVIOR
+ CROSS-DOCUMENT CONSISTENCY
+ DOC ↔ SOURCE ↔ TEST ↔ RUNTIME TRACEABILITY
=
PROJECT_STATE_SYNC
```

Important Git detail: a tracked document cannot reliably contain the hash of the commit that contains that exact document, because changing the document changes the commit hash.

The correct provenance proof is that source and required docs are tracked in the same tested Git HEAD, the worktree is clean, and no source/docs change occurs after final testing without a retest.

`PROJECT_TRUTH_SYNC.md` is the traceability ledger for critical claims. It links each important contract to:

```text
claim
→ documents
→ source owner
→ tests
→ runtime/E2E evidence when required
```

The repository provides:

```bash
python scripts/validate_handoff.py
python scripts/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base
python scripts/validate_project_truth.py
```

The first two validators are profile-aware. `validate_project_truth.py` becomes required for STRICT, and also runs whenever a truth ledger is present.

The truth validator checks machine-verifiable provenance, references, and structure. Semantic correctness still requires inspection of the mapped source/tests/runtime. A structural PASS must never be reported as semantic proof.

---

## Cross-document consistency validator

The repository includes a validator that scans **all project Markdown documents**, not only the code indexes.

It checks machine-verifiable problems such as:

- broken Markdown/local references;
- broken `path::symbol` references;
- unknown or conflicting stable `TRUTH-*` claims;
- missing claim backlinks;
- conflicting claim status/text;
- duplicate core docs;
- explicit stale markers;
- selected repository/branch/SHA conflicts between core docs;
- source changes whose required docs were not updated since the accepted/base SHA.

For final acceptance:

```bash
python scripts/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> \
  --require-base \
  --report artifacts/cross_document_sync_report.json
```

The base SHA matters: it lets the validator identify documentation that was left behind by the source changes in the candidate.

This is still a machine-verifiable gate, not semantic proof. If the docs and code disagree in meaning but the contradiction cannot be proven structurally, semantic review remains required.

---

## New-room startup procedure

When entering an existing project:

1. Read `PROJECT_PROFILE.yaml`.
2. Resolve the required document set for the selected profile.
3. Read `CURRENT_STATE.md`.
4. Read `PROJECT_MANIFEST.md`.
5. Read only the required authority/architecture/workflow/index contracts.
6. Read `TEST_ACCEPTANCE_MATRIX.md`.
7. Read `DOC_SYNC_MATRIX.md` when required.
8. Read `PROJECT_TRUTH_SYNC.md` when required or present.
9. Open only the exact relevant source ranges first.

This is the default fast-orientation mode.

---

## Handoff quality gate

A handoff is not complete until a new room can determine, without reconstructing old chats:

```text
project identity
current authority
current exact SHA
current phase
workflow/state machine
module ownership
symbol ownership
critical call paths
authoritative data/state
proven evidence
unproven evidence
known defects
next legal action
blocked actions
```

---

## Repository structure

```text
Skill_Workflow/
├─ README.md
├─ SKILL.md
├─ scripts/
│  ├─ project_profile.py
│  ├─ generate_symbol_index.py
│  ├─ generate_module_map.py
│  ├─ validate_handoff.py
│  ├─ validate_cross_document_consistency.py
│  └─ validate_project_truth.py
└─ templates/
   ├─ PROJECT_PROFILE.yaml
   ├─ PROJECT_MANIFEST.md
   ├─ CURRENT_STATE.md
   ├─ SOURCE_AUTHORITY_MAP.md
   ├─ ARCHITECTURE.md
   ├─ WORKFLOW_STATE_MACHINE.md
   ├─ MODULE_MAP.md
   ├─ SYMBOL_INDEX.md
   ├─ FLOW_INDEX.md
   ├─ TEST_ACCEPTANCE_MATRIX.md
   ├─ DOC_SYNC_MATRIX.md
   ├─ PROJECT_TRUTH_SYNC.md
   ├─ DATA_CONTRACTS.md
   ├─ API_CONTRACTS.md
   ├─ UI_INFORMATION_ARCHITECTURE.md
   ├─ RUNBOOK.md
   ├─ DECISIONS.md
   ├─ GLOSSARY.md
   ├─ KNOWN_DEFECTS.md
   └─ CHANGELOG.md
```

---

## Use cases

This workflow is useful for:

- large long-running software projects;
- projects frequently moved between AI rooms or coding agents;
- multi-repository systems;
- Android/iOS applications;
- web/backend platforms;
- ML/AI research pipelines;
- trading/research systems;
- data engineering projects;
- hardware/device integration;
- projects requiring strict audit lineage;
- teams that need durable AI-assisted development handoff.

---

## Contributing

Improvements are welcome.

Useful contributions include:

- better templates;
- language-specific symbol index generators;
- AST-based indexing tools;
- workflow/call-chain extractors;
- documentation drift detectors;
- handoff validators;
- acceptance-matrix tooling.

The main requirement is that additions preserve the core goal: **faster orientation without sacrificing project authority, workflow integrity, or evidence quality.**
