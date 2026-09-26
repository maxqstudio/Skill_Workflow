# Skill Workflow

A reusable project-handoff and codebase-orientation skill for ChatGPT rooms, coding agents, and human developers.

The goal is simple: **let a human understand the system without opening the codebase, and let a new room or coding agent continue work without rereading the entire repository from scratch.**

It focuses on:

- human-first system understanding without source-code reconstruction;
- exact project authority;
- current source/runtime state;
- architecture and workflow/state-machine mapping;
- module, symbol, and end-to-end flow indexing;
- generated sequence-contract acceptance with BEFORE / DURING / AFTER modes;
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

## Support the project

If Skill Workflow is useful for your projects, you can support ongoing development through Saweria:

**[Support MAXQ on Saweria](https://saweria.co/maxq)**

Support is optional and does not affect access to the public repository or its features.

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
PROJECT_PROFILE.yaml
→ docs/SYSTEM_OVERVIEW.md
→ docs/CURRENT_STATE.md
→ docs/PROJECT_MANIFEST.md
→ docs/<profile-required authority / architecture / workflow docs>
→ docs/SEQUENCE_CONTRACTS.md when required
→ docs/<MODULE / FLOW / SYMBOL maps>
→ docs/TEST_ACCEPTANCE_MATRIX.md
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

All required `.md` names in the profile tables resolve under `docs/`. `PROJECT_PROFILE.yaml` and `README.md` remain at repository root.

### LITE

For small, low-complexity projects.

Required:

```text
PROJECT_PROFILE.yaml
SYSTEM_OVERVIEW.md
PROJECT_MANIFEST.md
CURRENT_STATE.md
MODULE_MAP.md
TEST_ACCEPTANCE_MATRIX.md
```

### STANDARD

Default for normal multi-session / multi-agent development.

Generated documentation is required. Canonical human-facing project Markdown
lives under repository-root `docs/` and is produced by the Project Truth
Compiler rather than edited directly.

Required:

```text
PROJECT_PROFILE.yaml
SYSTEM_OVERVIEW.md
PROJECT_MANIFEST.md
CURRENT_STATE.md
SOURCE_AUTHORITY_MAP.md
ARCHITECTURE.md
WORKFLOW_STATE_MACHINE.md
SEQUENCE_CONTRACTS.md
MODULE_MAP.md
SYMBOL_INDEX.md
FLOW_INDEX.md
TEST_ACCEPTANCE_MATRIX.md
DOC_SYNC_MATRIX.md
```

### STRICT

For financial/trading, ML/research, hardware, production infrastructure, safety/audit-sensitive work, or complex multi-repository projects.

Generated documentation is required and PROJECT_DOCS_SYNC becomes part of the
truth gate.

STRICT requires all STANDARD docs plus:

```text
PROJECT_TRUTH_SYNC.md
```

It also forces explicit applicability decisions for critical optional contracts.

Profile choice is based on **risk and workflow complexity**, not simply repository size.

Ready-to-copy templates are available under `templates/`.

---

## Project Truth Compiler

For STANDARD and STRICT projects, canonical project Markdown under
repository-root `docs/` is generated deterministically instead of being
maintained by hand.

The authority model is:

```text
SOURCE CODE
    = implementation facts

.workflow/*.json
    = semantic / governance intent

tests + runtime evidence
    = behavioral truth

generated Markdown
    = human-readable projection
```

The compiler does **not** ask an LLM to rewrite documentation. It uses
deterministic Python templates and machine-readable inputs.

Recommended project structure:

```text
.workflow/
├─ project.json
├─ authority.json
├─ state.json
├─ architecture.json
├─ contracts.json
├─ claims.json
├─ acceptance.json
├─ decisions.json
├─ known_defects.json
├─ glossary.json
├─ changelog.json
├─ workflows/
│  └─ FLOW-*.json
└─ generated/
   └─ code_facts.json
```

Initialize the spec pack:

```bash
python scripts/initialize_project_truth.py
```

Initializer also vendors the runtime tool pack into:

```text
.workflow/tools/
```

so target projects do not depend on a particular agent's skill-install path.

Populate semantic/governance specs, then synchronize documentation:

```bash
python .workflow/tools/sync_project_truth.py
```

That command generates docs/facts, validates reproducibility, records only the
documentation gates `DOC_LAYOUT`, `PROJECT_DOCS_NORMALIZED`,
`DOC_READABILITY`, and `PROJECT_DOCS_SYNC` as PASS, regenerates, and
validates again.

Low-level commands remain available:

```bash
python .workflow/tools/generate_project_docs.py
python .workflow/tools/validate_project_docs.py
```

Run the compiler regression self-test with:

```bash
python scripts/selftest_project_truth_compiler.py
```

Run the full STRICT governance integration self-test with:

```bash
python scripts/selftest_strict_project_workflow.py
```

The STRICT fixture creates a temporary Git repository, generates DURING sequence evidence and `docs/`, runs the blocking validator chain, and verifies every validator is read-only on the final clean snapshot.

When generated documentation is enabled:

```text
manual edit to generated Markdown
→ NOT AUTHORITY

source/spec change
→ regenerate

generated output differs from tracked docs
→ PROJECT_DOCS_SYNC = FAIL
```

### Canonical docs layout

Target projects use one canonical human-facing documentation root:

```text
<repo>/
├─ README.md
├─ PROJECT_PROFILE.yaml
├─ .workflow/
│  ├─ *.json
│  ├─ workflows/
│  ├─ generated/
│  └─ tools/
└─ docs/
   ├─ SYSTEM_OVERVIEW.md
   ├─ CURRENT_STATE.md
   ├─ PROJECT_MANIFEST.md
   ├─ ARCHITECTURE.md
   ├─ WORKFLOW_STATE_MACHINE.md
   ├─ SEQUENCE_CONTRACTS.md
   ├─ FLOW_INDEX.md
   ├─ MODULE_MAP.md
   ├─ SYMBOL_INDEX.md
   ├─ TEST_ACCEPTANCE_MATRIX.md
   ├─ PROJECT_TRUTH_SYNC.md
   └─ sequence/
```

Canonical generated governance docs MUST NOT also exist at repository root.

```text
root/SYSTEM_OVERVIEW.md
+
root/docs/SYSTEM_OVERVIEW.md
=
DOC_LAYOUT FAIL
```

`README.md`, `PROJECT_PROFILE.yaml`, and `.workflow/` remain at repository
root.

### Deterministic cleanup and readability

The compiler applies safe deterministic Markdown normalization before writing
tracked docs:

- LF newlines;
- trailing whitespace removal;
- stable single blank-line separation outside fenced code;
- exactly one final newline;
- no semantic reordering of workflows, sequence edges, decisions, or evidence.

Then `validate_doc_quality.py` checks:

```text
DOC_LAYOUT
PROJECT_DOCS_NORMALIZED
DOC_READABILITY
```

These are structural presentation gates. Semantic readability is still decided
by the Human Comprehension Gate.

### What comes from code automatically

The fact extractor currently derives machine-observable information such as:

- source files and language inventory;
- line counts;
- test-file inventory;
- Python classes/functions/methods;
- Python decorated HTTP routes;
- Python call tokens;
- deterministic source-content digest.

It deliberately does not guess business meaning.

### What remains explicit semantic input

The compact machine-readable specs declare information that code alone cannot
reliably explain:

- project purpose and users;
- authority and mutability;
- intended workflow/lifecycle semantics;
- invariants;
- allowed/blocked next actions;
- acceptance boundaries;
- durable design decisions;
- known defects;
- glossary meaning.

The agent may edit these structured specs when the actual contract changes.
It should not duplicate the same semantic change across many Markdown files.

### PROJECT_DOCS_SYNC is independently revalidated

The value recorded in `.workflow/acceptance.json` is not trusted by itself.

Final truth validation executes the generated-doc validator again. Therefore:

```text
spec says PROJECT_DOCS_SYNC=PASS
but compiler check fails
→ final truth FAIL
```

This prevents a stale or manually forged PASS declaration from becoming
acceptance authority.

### Why JSON instead of generated prose from an LLM

JSON is used for the semantic spec layer because it is deterministic, easy to
diff, dependency-free in Python, and suitable for validation.

The canonical path is:

```text
code facts
+ semantic specs
+ test/runtime evidence declarations
→ deterministic compiler
→ all human-facing project docs
```

This reduces token usage and documentation drift without pretending that static
analysis can infer Owner intent.

---

## Human-first project understanding

`SYSTEM_OVERVIEW.md` is the first human-facing explanation of the project.

Its job is different from engineering indexes:

```text
SYSTEM_OVERVIEW
→ understand what the system is and how it works

FLOW_INDEX / MODULE_MAP / SYMBOL_INDEX
→ locate exact implementation
```

A person reading the overview should be able to explain:

- what problem the project solves;
- who uses it;
- major components;
- main data flow;
- main user/domain workflows;
- important lifecycle states;
- authority boundaries;
- mutable vs immutable state;
- failure/recovery behavior;
- current project state;
- what is proven and not proven;
- what can happen next and what is blocked.

The overview deliberately uses domain language first. Exact function names and
call chains belong in the engineering documents.

Final acceptance includes:

```text
HUMAN_COMPREHENSION_GATE = PASS
```

and:

```bash
python .workflow/tools/validate_human_comprehension.py --require-pass
```

The validator checks structural coverage and explicit gate status. It does not
prove semantic correctness or actual human understanding; that still requires
review against current authority, workflow, tests, and runtime evidence.

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
python .workflow/tools/generate_symbol_index.py
python .workflow/tools/generate_module_map.py
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

## Generated Sequence Contract acceptance

Critical workflow diagrams can be generated from machine-readable contracts and
the codebase instead of being typed manually.

The workflow has three explicit modes:

| Mode | Plan | Actual | Use |
|---|---|---|---|
| BEFORE | Frozen before implementation | Generated from code | New work where design exists before coding |
| DURING | Not applicable | Generated from current code | Governance adopted while implementation is in progress |
| AFTER | Not applicable | Generated from final code | Post-implementation reconstruction |

### BEFORE

```text
plan contract
→ generated plan Mermaid
→ freeze/commit
→ implementation
→ generated actual graph
→ generated actual Mermaid
→ PLAN vs ACTUAL
→ classify mismatch
→ repair
→ regenerate
→ accept
```

Git lineage must prove that the frozen plan existed before implementation.

### DURING / AFTER

Do not create a retrospective plan.

```text
codebase
→ generated actual graph
→ generated Mermaid
→ source/test/runtime validation
```

### Why machine-readable contracts matter

Mermaid is only the view.

The real acceptance inputs are:

```text
session contract JSON
plan graph JSON (BEFORE only)
actual graph JSON
optional runtime graph
```

Canonical Mermaid files are deterministic generated output and must not be
hand-edited.

### Source binding

Tracked generated actual graphs use a deterministic source-content digest rather
than trying to embed the final Git commit that contains themselves.

```text
ACTUAL_SOURCE_DIGEST
=
CURRENT_SOURCE_DIGEST
```

This avoids self-referential Git provenance while final HEAD remains verified
separately.

### Current vs historical sessions

Sequence evidence has an explicit scope:

```text
CURRENT
HISTORICAL
```

CURRENT actual graphs must match the current source-content digest.

HISTORICAL graphs preserve the implementation observed in an earlier accepted
phase and are not regenerated to match newer code.

### Commands

```bash
python .workflow/tools/generate_sequence_plan.py \
  --plan docs/sequence/plans/<session>.plan.json \
  --output docs/sequence/generated/<session>.plan.mmd

python .workflow/tools/generate_sequence_actual.py \
  --output-json docs/sequence/generated/<session>.actual.json \
  --output-mermaid docs/sequence/generated/<session>.actual.mmd \
  --entry <path::symbol>

python .workflow/tools/validate_sequence_contract.py \
  --session docs/sequence/sessions/<session>.json

python .workflow/tools/validate_sequence_sessions.py
```

When sequence policy is required, final acceptance requires:

```text
SEQUENCE_SYNC = PASS
```

Mismatch does not automatically mean the code is wrong. Classify first:

```text
CODE_DEFECT
PLAN_CHANGE
GENERATOR_DEFECT
```

Then repair the correct authority and regenerate.

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
- `SYSTEM_OVERVIEW.md`
- `PROJECT_MANIFEST.md`
- `CURRENT_STATE.md`
- `SOURCE_AUTHORITY_MAP.md`
- `ARCHITECTURE.md`
- `WORKFLOW_STATE_MACHINE.md`
- `SEQUENCE_CONTRACTS.md`
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

For STANDARD/STRICT, the normal edit target is **not the Markdown**. The agent
updates source code and/or the appropriate .workflow JSON authority, then
regenerates all affected documentation.

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

The agent then uses `DOC_SYNC_MATRIX.md` to determine which upstream authority
must change. In generated-documentation mode, the compiler updates the Markdown
projections transactionally.

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
python .workflow/tools/validate_handoff.py
```

The validator checks structural handoff requirements. A validator PASS does not replace semantic review, but a validator FAIL blocks completion.

The disciplined flow is:

```text
READ PROJECT_PROFILE
→ READ SYSTEM_OVERVIEW
→ READ AUTHORITY
→ DECLARE DOC IMPACT
→ EDIT SOURCE / .workflow SPEC
→ GENERATE CODE FACTS
→ GENERATE PROJECT DOCS
→ GENERATE / VALIDATE SEQUENCES
→ TEST
→ PROJECT_DOCS_SYNC CHECK
→ CROSS-DOC VALIDATION
→ RUNTIME/E2E
→ UPDATE EVIDENCE SPEC
→ REGENERATE
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
+ HUMAN COMPREHENSION
+ SEQUENCE SYNC when required
+ PROJECT DOCS SYNC when generated docs are enabled
+ DOC ↔ SOURCE ↔ TEST ↔ RUNTIME TRACEABILITY
=
PROJECT_STATE_SYNC
```

Important Git detail: a tracked document cannot reliably contain the hash of the commit that contains that exact document, because changing the document changes the commit hash.

The correct provenance proof is that source and required docs are tracked in the same tested Git HEAD, the worktree is clean, and no source/docs change occurs after final testing without a retest.

`docs/PROJECT_TRUTH_SYNC.md` is the traceability ledger for critical claims. It links each important contract to:

```text
claim
→ documents
→ source owner
→ tests
→ runtime/E2E evidence when required
```

The repository provides:

```bash
python .workflow/tools/validate_handoff.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/validate_human_comprehension.py --require-pass
python .workflow/tools/validate_sequence_sessions.py
python .workflow/tools/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base
python .workflow/tools/validate_project_truth.py
```

`validate_handoff.py`, `validate_sequence_sessions.py`, and `validate_cross_document_consistency.py` honor the project profile. `validate_human_comprehension.py` applies to every profile because `docs/SYSTEM_OVERVIEW.md` is universal. `validate_project_truth.py` becomes required for STRICT, and also runs whenever a truth ledger is present.

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
python .workflow/tools/validate_cross_document_consistency.py \
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
3. Read `docs/SYSTEM_OVERVIEW.md` for the human/domain mental model.
4. Read `docs/CURRENT_STATE.md`.
5. Read `docs/PROJECT_MANIFEST.md`.
6. Read only the required authority/architecture/workflow/index contracts.
7. Read `docs/SEQUENCE_CONTRACTS.md` when sequence policy is enabled.
8. Read `docs/TEST_ACCEPTANCE_MATRIX.md`.
9. Read `docs/DOC_SYNC_MATRIX.md` when required.
10. Read `docs/PROJECT_TRUTH_SYNC.md` when required or present.
11. Open only the exact relevant source ranges first.

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
│  ├─ initialize_project_truth.py
│  ├─ extract_project_facts.py
│  ├─ generate_project_docs.py
│  ├─ validate_project_docs.py
│  ├─ validate_doc_quality.py
│  ├─ sync_project_truth.py
│  ├─ selftest_project_truth_compiler.py
│  ├─ selftest_strict_project_workflow.py
│  ├─ generate_symbol_index.py
│  ├─ generate_module_map.py
│  ├─ sequence_contract.py
│  ├─ generate_sequence_plan.py
│  ├─ generate_sequence_actual.py
│  ├─ validate_sequence_contract.py
│  ├─ validate_sequence_sessions.py
│  ├─ validate_handoff.py
│  ├─ validate_human_comprehension.py
│  ├─ validate_cross_document_consistency.py
│  └─ validate_project_truth.py
└─ templates/
   ├─ PROJECT_PROFILE.yaml
   ├─ SYSTEM_OVERVIEW.md
   ├─ PROJECT_MANIFEST.md
   ├─ CURRENT_STATE.md
   ├─ SOURCE_AUTHORITY_MAP.md
   ├─ ARCHITECTURE.md
   ├─ WORKFLOW_STATE_MACHINE.md
   ├─ SEQUENCE_CONTRACTS.md
   ├─ SEQUENCE_SESSION.json
   ├─ SEQUENCE_PLAN.json
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
