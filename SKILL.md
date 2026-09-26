---
name: project-handoff-workflow
description: Safely orient, hand off, audit, repair, and continue software projects using authority maps, architecture, workflow/state machines, module/symbol/flow indexes, and evidence-based acceptance.
---

# PROJECT HANDOFF & CODEBASE ORIENTATION SKILL

## Purpose

Use this skill to understand, continue, audit, repair, or hand off software projects safely across rooms, agents, and developers.

Goals:
- reduce context loss;
- prevent accidental redesign;
- prevent authority confusion;
- avoid stale assumptions;
- avoid blind full-codebase rescans;
- preserve exact tested-source lineage;
- make runtime and acceptance evidence explicit.

This skill is project-agnostic.

# 1. Core principle

Do not begin by reading the entire repository blindly.

Build a project map first:

PROJECT_PROFILE
→ CURRENT_STATE
→ PROJECT_MANIFEST
→ SOURCE_AUTHORITY_MAP
→ ARCHITECTURE
→ WORKFLOW_STATE_MACHINE
→ MODULE_MAP
→ FLOW_INDEX
→ SYMBOL_INDEX
→ TEST_ACCEPTANCE_MATRIX
→ exact relevant source ranges
→ runtime/E2E verification when required.

The documents are navigation and contract aids. Source and runtime remain evidence and may expose stale documentation.

# 2. Adaptive governance profiles

Do not impose the same documentation ceremony on every project.

Every project MUST define `PROJECT_PROFILE.yaml`.

Supported profiles:

## LITE

For small, low-complexity projects with limited runtime/state complexity.

Required:

```text
PROJECT_PROFILE.yaml
PROJECT_MANIFEST.md
CURRENT_STATE.md
MODULE_MAP.md
TEST_ACCEPTANCE_MATRIX.md
```

Additional contracts may still be marked required when the project needs them.

## STANDARD

Default for normal multi-session or multi-agent development.

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

STRICT also requires explicit applicability decisions for critical optional contracts. Do not leave them ambiguously optional.

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

# 3. Document responsibilities

## PROJECT_PROFILE.yaml

Machine-readable governance policy.

It selects LITE, STANDARD, or STRICT and declares which optional contracts are required, optional, or not applicable.

Agents must read this before deciding which project documents are mandatory.

## PROJECT_MANIFEST.md
Project entry point. Identify purpose, repositories, branch, source authority, runtime authority, acceptance authority, stack, entry points, important directories, external systems, required reading order, and non-negotiable constraints.

## CURRENT_STATE.md
Short live handoff snapshot. Include current phase, exact authoritative SHA, last accepted SHA, current candidate, blockers, known defects, proven/not-proven facts, next authorized action, and blocked actions. Never mix historical status with current status.

## SOURCE_AUTHORITY_MAP.md
Map each concern to its canonical authority and location. Cover source, runtime, data, configuration, UI, workflow, database, artifact/model, deployment, tests, historical reference, and documentation. If authorities conflict, do not guess.

## ARCHITECTURE.md
Describe components, boundaries, dependencies, data flow, persistence, runtime processes, external systems, and security boundaries.

## WORKFLOW_STATE_MACHINE.md
Document every meaningful lifecycle. For each state define entry condition, legal actions, legal transitions, exit condition, owner/authority, side effects, artifacts, failure behavior, and rollback behavior. Write invariants explicitly. Never infer workflow only from UI labels.

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

# 5. New-room startup procedure

1. Read PROJECT_PROFILE.yaml.
2. Resolve the required document set for the selected profile.
3. Read CURRENT_STATE.md.
4. Read PROJECT_MANIFEST.md.
5. Read only the authority/architecture/workflow/index/contracts required by the profile.
6. Read TEST_ACCEPTANCE_MATRIX.md.
7. Read DOC_SYNC_MATRIX.md when required.
8. Read PROJECT_TRUTH_SYNC.md when required or present for critical flows.
9. Open only exact relevant source ranges first.

Do not create or maintain documents that the profile marks not applicable.

Expand outward only if indexes are stale, incomplete, contradictory, or a full audit is explicitly required.

# 6. Task execution workflow

read PROJECT_PROFILE
→ understand authority
→ identify affected workflow
→ identify affected modules
→ locate exact symbols
→ reproduce defect or establish baseline
→ implement minimum valid repair
→ regenerate machine-derived structural facts
→ update semantic docs/contracts
→ targeted tests
→ cumulative regression
→ runtime/E2E verification when applicable
→ verify final SHA
→ final audit
→ update project state.

Never treat source changed as equivalent to PASS.

# 7. Build/repair contract

For every repair:
1. identify exact parent SHA;
2. reproduce or prove defect;
3. determine root cause;
4. repair minimum scope;
5. add regression coverage;
6. run targeted tests;
7. run cumulative tests;
8. run runtime/E2E when required;
9. confirm final source SHA equals tested SHA;
10. only then mark candidate ready for audit.

Do not make a report-only commit after final testing if it changes the tested SHA.

Invariant:
FINAL SOURCE SHA = TESTED SHA.

# 8. Acceptance rule

Acceptance reflects only the strongest evidence actually executed.

Unit PASS does not imply runtime PASS.
Runtime start does not imply UI E2E PASS.
UI E2E does not imply physical-device PASS.
Historical physical proof does not imply current physical execution.
Build success does not imply scientific validity.

Always state the evidence boundary.

# 9. Defect handling

For a confirmed defect record:
root cause
→ affected contract
→ affected modules/symbols
→ repair scope
→ regression test
→ runtime retest when required.

Use CONFIRMED, STRONG_INFERENCE, UNVERIFIED.

# 10. Redesign prevention

Architecture, UI, or workflow changes require a defect repair, explicit owner request, or accepted roadmap change. Otherwise do not redesign.

# 11. Active state vs history

Separate ACTIVE STATE, HISTORICAL EVIDENCE, and ARCHIVE. Promotion should normally remove an object from the prior active list while preserving evidence.

# 12. Configuration vs execution snapshot

Separate CURRENT CONFIGURATION from FROZEN EXECUTION SNAPSHOT. Editable configuration must not rewrite historical evidence. Running execution keeps values captured at start.

# 13. UI truth contract

Correct:
backend/domain authority
→ API
→ semantic user-facing representation
→ UI.

Do not hardcode dynamic authority, eligibility, execution counts, promotion state, runtime availability, or phase completion in presentation code.

# 14. Handoff procedure

Before handoff update at minimum:
CURRENT_STATE.md
SOURCE_AUTHORITY_MAP.md
TEST_ACCEPTANCE_MATRIX.md
KNOWN_DEFECTS.md.

Handoff should include project, repo, branch, exact authoritative SHA, runtime authority, current phase/status, last accepted, current candidate, defects, proven/not-proven facts, blocked actions, next authorized action, and read-first order.

# 15. Handoff quality gate

A new room must be able to answer without reading the whole codebase:
what is the project;
what is current authority;
what phase is active;
what exact SHA is current;
what is the workflow/state machine;
which modules and symbols own critical behavior;
what are the critical call paths;
what data/state is authoritative;
what is proven/not proven;
what is broken;
what may happen next;
what is forbidden.

# 16. Fast orientation mode

Read:
1. PROJECT_PROFILE
2. CURRENT_STATE
3. PROJECT_MANIFEST
4. only profile-required authority/architecture/workflow docs
5. MODULE_MAP when required
6. FLOW_INDEX when required
7. SYMBOL_INDEX when required
8. TEST_ACCEPTANCE_MATRIX
9. DOC_SYNC_MATRIX when required
10. PROJECT_TRUTH_SYNC when required or present
11. exact relevant source ranges.

Do not recursively scan the repository unless docs/indexes are missing or conflicting, corruption is suspected, or a full audit is explicitly requested.

# 17. Document drift check

Verify critical claims against source/runtime when they affect authority, state transitions, data semantics, acceptance, or when docs predate the candidate.

If docs disagree with implementation:
identify conflict
→ determine canonical authority
→ repair stale documentation.

# 18. Index freshness

MODULE_MAP, SYMBOL_INDEX, and FLOW_INDEX are navigation accelerators.

Refresh them when files/symbols move, workflow ownership changes, API routing changes, state-transition logic moves, major refactors change call paths, or line ranges drift materially.

Preferred model:
machine-generated structure
+
human-maintained semantic responsibility
+
exact SHA binding.

If stale:
mark STALE
→ locate by symbol name
→ refresh ranges/call paths
→ do not trust stale line numbers blindly.

# 19. Non-negotiables

Never invent authority or tests, claim runtime PASS from unit tests alone, redesign without authorization, hide defects, mutate history to match current configuration, use stale SHA as current authority, mix unrelated project state, or rely on chat memory as the only project record.

Always use exact SHA, preserve lineage, separate active state from history, separate configuration from execution snapshots, trace workflow before changing it, verify the strongest required acceptance layer, and leave a clean handoff.

# 20. Agent discipline contract

Documentation is part of project state, not optional commentary.

Invariant:

SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL.

Before editing source, the agent MUST declare documentation impact:

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
test acceptance matrix: YES/NO
current state: YES
decisions: YES/NO
known defects: YES/NO
```

Every NO must be defensible from the actual change scope.

The agent must use DOC_SYNC_MATRIX.md to determine required documentation updates.

A source change that invalidates project documentation is itself a project defect.

## Documentation transaction rule

Source, contracts, indexes, test evidence, and current project state are one transaction:

```text
CODE
+
DOC CONTRACT
+
INDEX
+
TEST EVIDENCE
+
CURRENT STATE
=
ONE PROJECT STATE
```

Do not declare completion while any affected document remains stale.

## Required execution sequence

```text
SESSION START
→ read CURRENT_STATE
→ verify repository/branch/SHA authority
→ read workflow + module/flow/symbol indexes
→ declare DOC IMPACT
→ reproduce/baseline
→ implement minimum valid change
→ regenerate structural facts where applicable
→ update affected semantic docs/indexes
→ targeted tests
→ cumulative regression
→ documentation drift validation
→ runtime/E2E when required
→ update TEST_ACCEPTANCE_MATRIX
→ update CURRENT_STATE
→ final handoff
```

## Structural index generation

Do not manually reconstruct facts that can be generated safely.

Available generators:

```bash
python scripts/generate_symbol_index.py
python scripts/generate_module_map.py
```

`generate_symbol_index.py` prefers Universal Ctags for broad language coverage and falls back to Python AST when Ctags is unavailable.

Generated outputs contain facts only:

- file path;
- symbol;
- kind;
- line range;
- language;
- file/module size/location.

They MUST NOT invent:

- responsibility;
- authority;
- lifecycle semantics;
- side effects;
- legal transitions.

The agent merges generated facts into semantic project documentation and verifies ownership.

FLOW_INDEX remains semantic-verified. Do not automatically claim an end-to-end call graph is authoritative merely from static call discovery.

## Hard documentation gates

The task is NOT DONE if any applies:

- source changed but affected docs are stale;
- workflow changed but WORKFLOW_STATE_MACHINE or FLOW_INDEX is stale;
- function/class moved or changed ownership but SYMBOL_INDEX is stale;
- module responsibility changed but MODULE_MAP is stale;
- API behavior changed but API_CONTRACTS is stale;
- data/schema semantics changed but DATA_CONTRACTS is stale;
- UI authority/action changed but UI_INFORMATION_ARCHITECTURE is stale;
- architecture/dependency changed but ARCHITECTURE is stale;
- acceptance evidence changed but TEST_ACCEPTANCE_MATRIX is stale;
- current candidate/phase/blocker changed but CURRENT_STATE is stale;
- durable design decision changed but DECISIONS is stale.

If documentation drift is detected:

```text
DOC_SYNC = FAIL
OVERALL STATUS = REPAIR REQUIRED — DOCUMENTATION DRIFT
```

Do not downgrade this to a warning.

## Post-change drift audit

Before final PASS, inspect the source diff and compare it with DOC_SYNC_MATRIX.md.

Verify:

- every changed authority-bearing symbol is indexed;
- every changed call path is reflected in FLOW_INDEX;
- line-range hints are refreshed or marked STALE;
- current authority SHA/state is correct;
- acceptance evidence matches tests actually executed;
- known defects are current;
- no required document is silently skipped.

When available, run:

```bash
python scripts/validate_handoff.py
python scripts/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base
```

Both validators are blocking gates. The cross-document validator scans all project Markdown, stable claims, local references, selected authority fields, and required doc freshness from the accepted/base SHA.

A validator PASS does not prove semantic correctness, but validator FAIL blocks completion.

## Final report documentation block

Every build/repair final report MUST include:

```text
DOCUMENTATION SYNC:
PASS / FAIL

CURRENT_STATE:
UPDATED / NO IMPACT

WORKFLOW_STATE_MACHINE:
UPDATED / NO IMPACT

MODULE_MAP:
UPDATED / NO IMPACT

SYMBOL_INDEX:
UPDATED / NO IMPACT

FLOW_INDEX:
UPDATED / NO IMPACT

API_CONTRACTS:
UPDATED / NO IMPACT

DATA_CONTRACTS:
UPDATED / NO IMPACT

UI_INFORMATION_ARCHITECTURE:
UPDATED / NO IMPACT

TEST_ACCEPTANCE_MATRIX:
UPDATED

DOC VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

CROSS-DOCUMENT VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

STALE REQUIRED DOCS:
0 / <count>
```

If a required documentation item is stale, final status cannot be PASS.

# 21. Definition of done

A task is DONE only when source/contract repair is complete, regression exists, required runtime/E2E ran, documentation sync passes, affected indexes/contracts are current, final tested SHA is known, evidence boundary is explicit, and CURRENT_STATE is updated.

A handoff is DONE only when the next room can continue safely without reconstructing authority from old chat messages.

# 22. Project Truth Synchronization

Documentation sync is broader than index freshness or matching a revision label.

A project is synchronized only when important claims in documentation are consistent with the current source, tests, and runtime evidence.

Required truth layers:

1. PROVENANCE SYNC
2. REFERENCE SYNC
3. STRUCTURAL SYNC
4. SEMANTIC SYNC
5. BEHAVIORAL SYNC
6. CROSS-DOCUMENT CONSISTENCY
7. DOC ↔ SOURCE TRACEABILITY
8. DOC ↔ TEST TRACEABILITY
9. TEST ↔ RUNTIME TRACEABILITY

Overall invariant:

SOURCE TESTS PASS + DOCS IN SAME TESTED SNAPSHOT + STRUCTURAL SYNC PASS + SEMANTIC SYNC PASS + BEHAVIORAL SYNC PASS + CROSS-DOCUMENT CONSISTENCY PASS + TRACEABILITY PASS = PROJECT_STATE_SYNC PASS.

A matching SHA label alone is never sufficient.

## Provenance rule

Do not require a tracked document to contain the hash of the commit that contains that same document. Git commit hashes are derived from the tree, so this creates a self-reference problem.

Instead prove provenance by:
- testing an exact Git HEAD;
- requiring a clean worktree for final acceptance;
- verifying source and required docs are tracked in that same HEAD;
- recording the tested HEAD in generated/external acceptance evidence;
- forbidding source or documentation changes after final testing without retest.

Therefore the invariant is:

TESTED_HEAD = FINAL_SOURCE_HEAD = FINAL_DOCUMENTATION_HEAD.

The generated truth report may record the actual HEAD after checkout/testing. It is acceptance evidence and should not be committed back into the same snapshot if doing so would change the HEAD being reported.

## Reference sync

All authoritative references must resolve where machine-verifiable: files, indexed symbols, tests, routes/schemas/components where supported, and required evidence references.

A broken required reference means PROJECT_STATE_SYNC FAIL.

## Structural sync

The documented structure must match implementation structure. MODULE_MAP ownership, SYMBOL_INDEX symbols, FLOW_INDEX call paths, API contracts, data contracts, and UI architecture must point to real implementation authority.

## Semantic sync

Existence is not enough. The stated responsibility, authority, transition, side effect, invariant, and failure semantics must match the code.

Example: if docs say Candidate → Challenger but code implements Candidate → Champion, structural resolution may pass while SEMANTIC_SYNC must fail.

Generic scripts cannot fully prove semantics. The agent must inspect the exact authority-bearing implementation and relevant tests, then record traceability in PROJECT_TRUTH_SYNC.md.

Do not claim semantic PASS from path/symbol existence checks alone.

## Behavioral sync

Where documentation describes runtime behavior, prove it with the strongest required executable evidence: lifecycle tests, runtime/API verification, browser/device E2E, integration evidence, or actual runbook execution as applicable.

If required behavioral evidence was not executed, BEHAVIORAL_SYNC is NOT_PROVEN and overall PROJECT_STATE_SYNC cannot be PASS unless the behavior is explicitly NOT_APPLICABLE.

## Cross-document consistency

Documents must agree with each other. Contradictions between WORKFLOW_STATE_MACHINE, FLOW_INDEX, API_CONTRACTS, CURRENT_STATE, TEST_ACCEPTANCE_MATRIX, SOURCE_AUTHORITY_MAP, PROJECT_MANIFEST, KNOWN_DEFECTS, or other authority docs are project defects.

## Bidirectional truth traceability

For every critical project claim maintain:

CLAIM / CONTRACT ↔ DOCUMENT(S) ↔ SOURCE OWNER ↔ TEST(S) ↔ RUNTIME/E2E EVIDENCE when required.

Use stable claim IDs for authority-bearing behavior and invariants where practical, for example TRUTH-PROMOTION-001. Do not add IDs to trivial helpers.

For critical claim-to-claim logic, PROJECT_TRUTH_SYNC.md may declare explicit relations:

```text
CONFLICTS_WITH
REQUIRES
SAME_AS
SUPERSEDES
```

The cross-document validator must reject impossible terminal combinations, such as two mutually conflicting claims both marked PASS.

PROJECT_TRUTH_SYNC.md is the canonical traceability ledger.

## Generated facts vs maintained semantics

Prefer machine-generated facts for file paths, symbol names, line hints, signatures, routes, imports/dependencies, schema/table names, and test names.

Human/agent-maintained semantics remain required for purpose, authority, responsibility, lifecycle meaning, invariants, legal transitions, failure semantics, and evidence interpretation.

Machine verification of facts does not replace semantic audit.

## Required final truth gates

SOURCE_TESTS: PASS
RUNTIME_E2E: PASS / NOT_APPLICABLE
PROVENANCE_SYNC: PASS
REFERENCE_SYNC: PASS
STRUCTURAL_SYNC: PASS
SEMANTIC_SYNC: PASS
BEHAVIORAL_SYNC: PASS / NOT_APPLICABLE
CROSS_DOCUMENT_CONSISTENCY: PASS
DOC_SOURCE_TRACEABILITY: PASS
DOC_TEST_TRACEABILITY: PASS
TEST_RUNTIME_TRACEABILITY: PASS / NOT_APPLICABLE
STALE_DOCUMENTS: 0
BROKEN_REFERENCES: 0
UNRESOLVED_CONTRACTS: 0
CONTRADICTORY_CLAIMS: 0
PROJECT_STATE_SYNC: PASS

If any required gate is FAIL, NOT_PROVEN, or unresolved, final status cannot be PASS.

Run validators required by the selected profile:

python scripts/validate_handoff.py
python scripts/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base

For STRICT, or when PROJECT_TRUTH_SYNC.md is present:

python scripts/validate_project_truth.py

A skipped validator must be justified by PROJECT_PROFILE.yaml, never by convenience.

Structural validator PASS is necessary but not sufficient for semantic truth.

## Definition of done override

A task is DONE only when source/contract repair is complete, required tests/runtime evidence pass, DOC_SYNC passes, PROJECT_STATE_SYNC passes, affected indexes/contracts are current, final tested HEAD equals final source/documentation HEAD, evidence boundaries are explicit, and CURRENT_STATE is updated.


## Cross-document validator gate

Final acceptance must include a full documentation-consistency scan.

The validator must scan all project Markdown documents, not only indexes.

Minimum machine-checkable scope:

- broken Markdown/local file references;
- broken path::symbol references;
- unknown stable TRUTH claim IDs;
- canonical claim backlinks;
- duplicate/conflicting claim text;
- conflicting claim statuses;
- duplicate core documentation files;
- explicit Status: STALE markers;
- selected repository/branch/authority mismatches;
- source changes that require documentation updates according to change type;
- required docs that were not updated since the accepted/base SHA.

For final acceptance, run against the exact accepted parent/base SHA:

```bash
python scripts/validate_cross_document_consistency.py \
  --base <LAST_ACCEPTED_SHA> \
  --require-base \
  --report artifacts/cross_document_sync_report.json
```

Do not use an inferred HEAD parent for milestone/final acceptance when the accepted base SHA is known.

A cross-document validator FAIL blocks PROJECT_STATE_SYNC.

Machine checks do not prove semantic correctness. Semantic conflicts that cannot be established mechanically still require source/test/runtime audit and must remain NOT_PROVEN until resolved.


## Profile selection discipline

Do not choose LITE merely because a repository is small.

Choose the profile from actual project risk and complexity.

Escalate to STANDARD or STRICT when any of these materially apply:

- multiple agents/rooms frequently hand off work;
- complex state machines;
- external runtimes or devices;
- financial or scientific correctness;
- immutable evidence/lineage;
- production mutation;
- multi-repository authority;
- difficult rollback/recovery;
- strong runtime/E2E acceptance needs.

Downgrading a governance profile requires an explicit documented decision. It must not be used to bypass documentation or validation failures.
