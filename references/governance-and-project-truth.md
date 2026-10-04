# Governance Profiles, Project Truth Compiler, and Document Contracts

This is a normative bundled reference for `SKILL.md`. Read it when profile selection, Project Truth compilation, canonical docs layout, document responsibilities, or optional contracts are relevant.

# 2. Adaptive governance profiles

Do not impose the same documentation ceremony on every project.

Every project MUST keep a source-authored `AGENTS.md` at repository root. It is the agent startup/operating contract, is mandatory for LITE, STANDARD, and STRICT, and MUST NOT be generated or relocated under `docs/`. Existing project-specific `AGENTS.md` content is preserved by default during initialization/migration.

Every project MUST define `PROJECT_PROFILE.yaml`.

`PROJECT_PROFILE.yaml` MUST declare `schema_version: 1`. Governed `.workflow/*.json` and `.workflow/workflows/*.json` specs MUST also declare supported schema versions. Missing or unknown versions fail closed; legacy state must be migrated explicitly rather than silently reinterpreted.

Every profile-required generated `.md` document name below resolves under repository-root `docs/`. `README.md`, `AGENTS.md`, and `PROJECT_PROFILE.yaml` remain at repository root; `AGENTS.md` is mandatory source-authored operating guidance rather than generated Project Truth.

Supported profiles:

## LITE

For small, low-complexity projects with limited runtime/state complexity.

Required:

```text
PROJECT_PROFILE.yaml
SYSTEM_OVERVIEW.md
PROJECT_MANIFEST.md
CURRENT_STATE.md
ROADMAP.md
MODULE_MAP.md
TEST_ACCEPTANCE_MATRIX.md
```

Additional contracts may still be marked required when the project needs them.

## STANDARD

Default for normal multi-session or multi-agent development.

Generated documentation is REQUIRED.

The normal upstream edit targets are:

```text
source code
.workflow/*.json
tests/runtime evidence state
```

Canonical human-facing project Markdown lives under repository-root `docs/`.
It is a deterministic projection and MUST NOT be maintained manually.

Required:

```text
PROJECT_PROFILE.yaml
SYSTEM_OVERVIEW.md
PROJECT_MANIFEST.md
CURRENT_STATE.md
ROADMAP.md
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

`PROJECT_TRUTH_SYNC.md` may be added for critical flows.

## STRICT

For high-risk or audit-sensitive work such as:

- financial/trading systems;
- ML/research pipelines;
- production infrastructure;
- hardware/device integration;
- safety-sensitive behavior;
- complex multi-repository systems;
- projects with strict acceptance lineage.

Required:

```text
all STANDARD documents
+
PROJECT_TRUTH_SYNC.md
```

STRICT also requires explicit applicability decisions for critical optional
contracts. Do not leave them ambiguously optional.

Generated documentation is REQUIRED and PROJECT_DOCS_SYNC is a blocking truth
gate.

## Optional contract declarations

`PROJECT_PROFILE.yaml` may mark these as:

```text
required
optional
not_applicable
```

Supported contract categories:

```text
API_CONTRACTS.md
DATA_CONTRACTS.md
UI_INFORMATION_ARCHITECTURE.md
RUNBOOK.md
DECISIONS.md
KNOWN_DEFECTS.md
GLOSSARY.md
CHANGELOG.md
```

Profile selection is based on complexity, risk, runtime dependencies, handoff frequency, evidence requirements, and workflow/state complexity — not source-line count alone.

Validators MUST derive required documents from `PROJECT_PROFILE.yaml`; do not hardcode one universal pack.

# 2A. Project Truth Compiler

For STANDARD and STRICT projects, documentation is compiled rather than
hand-maintained.

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

Do NOT treat generated Markdown as the upstream semantic authority.

## Machine-readable semantic layer

Recommended structure:

```text
.workflow/
├─ project.json
├─ authority.json
├─ state.json
├─ roadmap.json
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

Initialize:

```bash
python scripts/initialize_project_truth.py
```

Initializer vendors runtime tools into `.workflow/tools/`. This keeps project
governance tooling project-local and independent of Codex/Claude/Cursor skill
installation paths.

The initializer also writes `.workflow/toolchain.lock.json`, binding the exact vendored Python tool bytes by SHA-256-derived manifest digest. The digest is acceptance-relevant; producer repository/commit metadata is provenance only and mutable upstream/cache state is never authority. For legacy projects, run `python scripts/migrate_governance_v1.py --root <project>` from the intended Skill Workflow source checkout. Migration is explicit, deterministic, idempotent, and rejects unknown future schema versions.

Synchronize code facts and generated docs:

```bash
python .workflow/tools/sync_project_truth.py
```

This command:

```text
validate roadmap/state phase contract
→ generate
→ validate
→ record ROADMAP_SYNC / DOC_LAYOUT / PROJECT_DOCS_NORMALIZED / DOC_READABILITY / PROJECT_DOCS_SYNC = PASS
→ regenerate
→ validate again
```

Low-level commands:

```bash
python .workflow/tools/generate_project_docs.py
python .workflow/tools/validate_project_docs.py
```

Executable compiler regression self-test:

```bash
python scripts/selftest_project_truth_compiler.py
```

Full STRICT governance integration self-test:

```bash
python scripts/selftest_strict_project_workflow.py
```

The STRICT self-test must prove the canonical `docs/` layout, DURING sequence acceptance, the complete validator chain, read-only validation, and a clean final Git worktree.

## What the compiler may derive from code

Machine-observable facts may include:

- source file inventory;
- languages/extensions;
- source line counts;
- test file inventory;
- Python classes/functions/methods;
- Python decorated HTTP routes;
- Python call tokens;
- deterministic source-content digest;
- other language facts when a supported parser/indexer exists.

## Structural analyzer evidence contract

Supported structural analyzers MUST expose a language-independent normalized result contract rather than making governance semantics depend on one parser implementation. An analyzer may report only facts supported by deterministic evidence and MUST declare its claimed file extensions, semantic level, parse failures, limitations, and evidence strength.

Unsupported languages or unsupported semantic levels MUST use an explicit inventory-only fallback. Inventory-only fallback MAY prove that a source file exists, but MUST NOT fabricate symbols, routes, calls, sequence participants, or sequence edges.

Static analyzers MUST keep dynamic dispatch, dependency injection, reflection, unresolved callbacks/events, framework magic, runtime ordering, and unresolved cross-language behavior `NOT_PROVEN` unless stronger runtime or semantic evidence exists. Adding a parser or recognizing a file extension does not upgrade those claims.

Compatibility rule: introducing or replacing an analyzer MUST preserve already-accepted output semantics unless a separately versioned migration changes the contract explicitly.

## What the compiler MUST NOT invent

The compiler must not infer missing:

- project purpose;
- Owner intent;
- business/scientific authority;
- lifecycle meaning;
- mutability rules;
- legal transitions;
- invariants;
- failure semantics;
- next authorized action;
- blocked action;
- acceptance status;
- design rationale.

Those belong in machine-readable semantic/governance specs.

## Generated-doc rule

When generated documentation is enabled:

```text
manual Markdown edit
≠ authority
```

The correct repair path is:

```text
change source and/or .workflow spec
→ regenerate
→ validate
```

If tracked generated Markdown differs from deterministic compiler output:

```text
PROJECT_DOCS_SYNC = FAIL
```

## Deterministic generator rule

The canonical compiler must not use an LLM to generate final tracked docs.

Allowed:

```text
AST / parser
structured semantic specs
deterministic templates
test/runtime evidence declarations
```

Not canonical:

```text
source → LLM prose → tracked docs
```

An LLM may help a human/agent propose semantic spec changes, but the final
documentation projection must be deterministic.

## Recorded gate is not trusted alone

A declared:

```text
PROJECT_DOCS_SYNC = PASS
```

is not sufficient evidence.

When generated documentation is enabled,
`validate_project_truth.py` executes the Project Truth Compiler validator again.

Therefore:

```text
recorded PASS
+ executable compiler check FAIL
=
PROJECT_STATE_SYNC FAIL
```

This prevents a stale or manually forged acceptance flag from bypassing the
actual deterministic check.

## LITE compatibility

LITE may use manual Markdown when PROJECT_PROFILE explicitly has:

```text
documentation.generated: false
```

Do not force compiler ceremony onto genuinely small projects.

# 2B. Canonical docs layout and normalization

All canonical human-facing project documentation lives under:

```text
<repo>/docs/
```

Repository-root exceptions are intentionally limited to:

```text
README.md
AGENTS.md
PROJECT_PROFILE.yaml
.workflow/
```

Generated governance documents MUST NOT exist both at repository root and under
`docs/`.

Example invalid state:

```text
SYSTEM_OVERVIEW.md
docs/SYSTEM_OVERVIEW.md
```

This is:

```text
DOC_LAYOUT = FAIL
```

## Canonical target layout

```text
<repo>/
├─ README.md
├─ AGENTS.md
├─ PROJECT_PROFILE.yaml
├─ .workflow/
│  ├─ project.json
│  ├─ authority.json
│  ├─ state.json
│  ├─ architecture.json
│  ├─ contracts.json
│  ├─ claims.json
│  ├─ acceptance.json
│  ├─ decisions.json
│  ├─ known_defects.json
│  ├─ glossary.json
│  ├─ changelog.json
│  ├─ workflows/
│  ├─ generated/
│  └─ tools/
└─ docs/
   ├─ SYSTEM_OVERVIEW.md
   ├─ PROJECT_MANIFEST.md
   ├─ CURRENT_STATE.md
   ├─ ROADMAP.md
   ├─ SOURCE_AUTHORITY_MAP.md
   ├─ ARCHITECTURE.md
   ├─ WORKFLOW_STATE_MACHINE.md
   ├─ SEQUENCE_CONTRACTS.md
   ├─ MODULE_MAP.md
   ├─ SYMBOL_INDEX.md
   ├─ FLOW_INDEX.md
   ├─ TEST_ACCEPTANCE_MATRIX.md
   ├─ DOC_SYNC_MATRIX.md
   ├─ PROJECT_TRUTH_SYNC.md
   ├─ API_CONTRACTS.md
   ├─ DATA_CONTRACTS.md
   ├─ UI_INFORMATION_ARCHITECTURE.md
   ├─ RUNBOOK.md
   ├─ DECISIONS.md
   ├─ KNOWN_DEFECTS.md
   ├─ GLOSSARY.md
   ├─ CHANGELOG.md
   └─ sequence/
```

## Deterministic normalization

Project Truth Compiler output is normalized before it is written.

Normalization is formatting-only:

- normalize line endings to LF;
- remove trailing whitespace;
- collapse repeated blank lines outside fenced code;
- ensure one final newline;
- preserve semantic ordering.

Do NOT automatically reorder:

- lifecycle transitions;
- workflow steps;
- sequence edges;
- decision chronology;
- evidence chronology;
- authority-precedence declarations.

## Documentation quality gate

Run:

```bash
python .workflow/tools/validate_doc_quality.py
```

Blocking machine-verifiable outputs:

```text
DOC_LAYOUT = PASS
PROJECT_DOCS_NORMALIZED = PASS
DOC_READABILITY = PASS
```

`DOC_READABILITY` proves presentation structure only. It does not prove
semantic understanding. HUMAN_COMPREHENSION remains the semantic human-facing
gate.

# 3. Document responsibilities

## AGENTS.md

Mandatory source-authored repository-root operating contract for coding agents. It defines the project-specific read order, non-negotiable operating constraints, generated-document handling, acceptance discipline, and handoff expectations. It is read before `PROJECT_PROFILE.yaml`. It must not duplicate machine-readable project state or pretend to replace `.workflow/*.json`; if it conflicts with current authority/evidence, stop and resolve the conflict rather than guessing.

## PROJECT_PROFILE.yaml

Machine-readable governance policy.

It selects LITE, STANDARD, or STRICT; declares optional contract applicability;
and selects generated-documentation / sequence policy.

Agents must read this before deciding which project documents are mandatory or
whether Markdown is editable at all.

## SYSTEM_OVERVIEW.md

Human-first project explanation.

A reader must be able to understand the project purpose, major components,
main data flow, user/domain workflows, lifecycle/state, authority model,
mutable vs immutable state, failure/recovery behavior, current project state,
and proven/not-proven boundaries without opening source code.

Keep implementation details out of the primary explanation. Link to engineering
documents for drill-down.

SYSTEM_OVERVIEW.md contains the Human Comprehension Gate.

## PROJECT_MANIFEST.md
Project entry point. Identify purpose, repositories, branch, source authority, runtime authority, acceptance authority, stack, entry points, important directories, external systems, required reading order, and non-negotiable constraints.

## CURRENT_STATE.md
Short live handoff snapshot. Include current phase, exact authoritative SHA, last accepted SHA, current candidate, blockers, known defects, proven/not-proven facts, next authorized action, and blocked actions. Never mix historical status with current status.

## ROADMAP.md
Deterministic human-facing projection of `.workflow/roadmap.json`. The machine-readable roadmap is mandatory project governance authority. `.workflow/state.json::phase` MUST equal `.workflow/roadmap.json::current_phase`; exactly one roadmap phase MUST be marked `CURRENT`; that phase id MUST equal `current_phase`; phase ids MUST be unique. When phase advances, update `state.json` and `roadmap.json` in the same project-state transaction and run `sync_project_truth.py`. Missing roadmap authority or phase drift is a blocking failure.

## SOURCE_AUTHORITY_MAP.md
Map each concern to its canonical authority and location. Cover source, runtime, data, configuration, UI, workflow, database, artifact/model, deployment, tests, historical reference, and documentation. If authorities conflict, do not guess.

## ARCHITECTURE.md
Describe components, boundaries, dependencies, data flow, persistence, runtime processes, external systems, and security boundaries.

## WORKFLOW_STATE_MACHINE.md
Document every meaningful lifecycle. For each state define entry condition, legal actions, legal transitions, exit condition, owner/authority, side effects, artifacts, failure behavior, and rollback behavior. Write invariants explicitly. Never infer workflow only from UI labels.

## SEQUENCE_CONTRACTS.md

Machine-backed sequence acceptance index.

For each phase/session, declare one mode:

- BEFORE — a plan contract is frozen before implementation, then generated
  actual behavior is compared against it.
- DURING — implementation already exists/in progress; retrospective plan is
  forbidden and only generated actual behavior is accepted.
- AFTER — post-implementation reconstruction; retrospective plan is forbidden
  and only final generated actual behavior is accepted.

Full machine sequence evidence is generated and MUST remain independently auditable.
Do not hand-edit generated machine or human Mermaid artifacts.

When a governed flow needs a human-facing diagram, generate a separate bounded
human projection from the full machine graph. The human projection is a
presentation artifact, not a replacement for `actual.json` / `actual.mmd`, and
it MUST explicitly state that static structure does not prove runtime ordering.

The machine-readable sequence session and plan contracts live under
`docs/sequence/` (recommended), acceptance reports should live under
`artifacts/sequence/`, and GitHub-readable human views should live under
`docs/sequence/views/`.

## MODULE_MAP.md
Fast file-level navigation map. Recommended columns: Module/File | Responsibility | Called By | Calls/Depends On | State Touched | Tests.

## SYMBOL_INDEX.md
Codebase table of contents. Index authority-bearing functions, classes, methods, API handlers, UI components, workers, state-transition functions, DB mutation functions, validators, and artifact readers/writers.

Recommended columns:
File | Symbol | Kind | Lines@SHA | Responsibility | Reads/Writes | Called By | Tests.

Use file path + symbol name + line-range hint. Symbol name is primary. Line numbers are hints tied to an exact SHA.

Prefer machine-generated structure plus human-maintained semantic responsibility. Do not index every trivial helper.

## FLOW_INDEX.md
End-to-end call-chain index. For each important behavior map:
entry point
→ API/event
→ service/domain handler
→ state transition
→ DB/artifact write
→ external side effect
→ fail-closed/error path
→ tests.

Before editing a flow:
WORKFLOW_STATE_MACHINE
→ FLOW_INDEX
→ SYMBOL_INDEX
→ exact source ranges
→ relevant tests.

## TEST_ACCEPTANCE_MATRIX.md
Map requirements to unit, integration, runtime, UI/E2E, physical, and production evidence. Use explicit states such as PASS, FAIL, NOT_RUN, NOT_APPLICABLE, NOT_PROVEN, BLOCKED. Never convert NOT_RUN into PASS.

# 4. Optional contracts

DATA_CONTRACTS documents schema, meaning, source of truth, mutability, versioning, lineage, retention, legal mutation, and validation.

API_CONTRACTS documents endpoint purpose, input/output, authority, side effects, errors, idempotency, and mutation scope.

UI_INFORMATION_ARCHITECTURE documents each workspace/page, backend authority, visible data, actions, forbidden actions, and technical data hidden from normal user surfaces.

RUNBOOK contains exact setup, build, start, stop, test, diagnose, recover, reset, and deploy commands plus environment details.

DECISIONS records durable decisions with date, context, reason, alternatives, impact, and authority.
