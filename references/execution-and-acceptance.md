# Execution, Acceptance, Handoff, and Documentation Discipline

This is a normative bundled reference for `SKILL.md`. Read it before implementation, repair, acceptance, handoff, or documentation-impact work.

# 5. New-room startup procedure

1. Read root `AGENTS.md`.
2. Read PROJECT_PROFILE.yaml.
3. Resolve the required document set for the selected profile.
4. Read docs/SYSTEM_OVERVIEW.md for the human/domain mental model.
5. Read docs/CURRENT_STATE.md.
6. Read docs/ROADMAP.md and verify its current phase matches CURRENT_STATE.
7. Read docs/PROJECT_MANIFEST.md.
8. Read only the authority/architecture/workflow/index/contracts required by the profile.
9. Read docs/SEQUENCE_CONTRACTS.md when sequence policy is enabled.
10. Read docs/TEST_ACCEPTANCE_MATRIX.md.
11. Read docs/DOC_SYNC_MATRIX.md when required.
12. Read docs/PROJECT_TRUTH_SYNC.md when required or present for critical flows.
13. Open only exact relevant source ranges first.

Do not create or maintain documents that the profile marks not applicable.

Expand outward only if indexes are stale, incomplete, contradictory, or a full audit is explicitly required.

# 6. Task execution workflow

read PROJECT_PROFILE
→ read SYSTEM_OVERVIEW
→ understand authority
→ identify affected workflow
→ determine sequence mode (BEFORE / DURING / AFTER)
→ freeze sequence plan before coding when mode = BEFORE
→ identify affected modules
→ locate exact symbols
→ reproduce defect or establish baseline
→ implement minimum valid repair
→ generate actual sequence graph from codebase
→ validate sequence contract
→ repair mismatch until sequence acceptance passes
→ regenerate machine-derived structural facts
→ update semantic docs/contracts
→ targeted tests
→ cumulative regression
→ runtime/E2E verification when applicable
→ verify final SHA
→ final audit
→ update project state and roadmap together when the current phase changes.

Never treat source changed as equivalent to PASS.


## Fast governance execution modes

Governance Engine V2 supports three explicit execution modes for the task loop:

```text
develop
→ verify
→ finalize
```

These modes change execution breadth, not governance authority.

### develop

Use `develop` for the inner loop when changed-file impact can be classified safely.
It may run only the targeted structural/regression checks mapped to the affected
implementation area.

A `develop` PASS is intermediate evidence only. It MUST NOT be used to mark a
requirement, phase, release, or PROJECT_STATE_SYNC as accepted.

If changed-file impact is broad or not safely mapped, `develop` MUST escalate to
`verify` instead of silently skipping checks.

### verify

Use `verify` before finalization to expand from targeted checks to the affected
governance and regression scope. It includes deterministic project-document,
human-comprehension, sequence, handoff, and cross-document verification where
applicable.

A `verify` PASS is still intermediate evidence. It MUST NOT replace final
acceptance. If impact is unknown, `verify` MUST escalate to the complete
`finalize` graph.

### finalize

`finalize` is the only fast-workflow mode that may provide final acceptance
authority. It MUST:

- require the exact expected candidate HEAD;
- run the complete required regression graph;
- synchronize deterministic Project Truth;
- run human-comprehension, sequence, handoff, cross-document, and final Project
  Truth validation;
- require the governed worktree to end clean;
- preserve every required final truth gate and fail closed on any dependency.

An invocation that began as `verify` and escalated to the full graph is still
reported as intermediate evidence; automatic escalation MUST NOT silently grant
final acceptance authority.

Changed-file classification and caches are accelerators only. Unknown impact,
classifier failure, missing base authority, or provenance mismatch MUST broaden
verification or fail; they must never produce a narrower false PASS.

Typical commands:

```bash
python .workflow/tools/governance_engine.py --root . --mode develop --base <LAST_ACCEPTED_SHA>
python .workflow/tools/governance_engine.py --root . --mode verify --base <LAST_ACCEPTED_SHA>
python .workflow/tools/governance_engine.py --root . --mode finalize --base <LAST_ACCEPTED_SHA> --expected-head <EXACT_HEAD>
```

Standalone validators remain valid and fail-closed. These modes orchestrate
when they run; they do not weaken their contracts.
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

Use CONFIRMED, STRONG_INFERENCE, and UNVERIFIED for diagnostic certainty while investigating. These are not lifecycle states in `.workflow/known_defects.json`. The governed defect ledger uses `OPEN`, `FIXED/ACCEPTED`, `HISTORICAL`, or `NOT_PROVEN`; resolved entries require accepted resolution evidence.

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
SYSTEM_OVERVIEW.md when the human mental model/current summary changed
CURRENT_STATE.md
ROADMAP.md when phase plan/current phase changed
SOURCE_AUTHORITY_MAP.md
TEST_ACCEPTANCE_MATRIX.md
KNOWN_DEFECTS.md.

Handoff should include project, repo, branch, exact authoritative SHA, runtime authority, current phase/status, last accepted, current candidate, defects, proven/not-proven facts, blocked actions, next authorized action, and read-first order.

# 15. Handoff quality gate

A new room or human reviewer must be able to answer without reading the whole codebase:
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
1. AGENTS.md
2. PROJECT_PROFILE
3. SYSTEM_OVERVIEW
4. CURRENT_STATE
4. ROADMAP
5. PROJECT_MANIFEST
6. only profile-required authority/architecture/workflow docs
7. MODULE_MAP when required
8. FLOW_INDEX when required
9. SYMBOL_INDEX when required
10. TEST_ACCEPTANCE_MATRIX
11. DOC_SYNC_MATRIX when required
12. PROJECT_TRUTH_SYNC when required or present
13. exact relevant source ranges.

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

Never invent authority or tests, claim runtime PASS from unit tests alone, redesign without authorization, hide defects, mutate history to match current configuration, use stale SHA as current authority, allow roadmap/current-phase drift, mix unrelated project state, or rely on chat memory as the only project record.

Always use exact SHA, preserve lineage, separate active state from history, separate configuration from execution snapshots, trace workflow before changing it, verify the strongest required acceptance layer, and leave a clean handoff.

# 20. Agent discipline contract

Documentation is part of project state, not optional commentary.

Invariant:

SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL.

Before editing source, the agent MUST declare documentation impact:

```text
DOC IMPACT
system overview: YES/NO
architecture: YES/NO
workflow/state machine: YES/NO
module map: YES/NO
symbol index: YES/NO
flow index: YES/NO
sequence contract: YES/NO
API contract: YES/NO
data contract: YES/NO
UI information architecture: YES/NO
test acceptance matrix: YES/NO
current state: YES
roadmap: YES/NO
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
+
ROADMAP
=
ONE PROJECT STATE
```

Do not declare completion while any affected document remains stale.

## Required execution sequence

```text
SESSION START
→ read AGENTS.md
→ read PROJECT_PROFILE
→ read SYSTEM_OVERVIEW
→ read CURRENT_STATE
→ read ROADMAP and verify current phase synchronization
→ verify repository/branch/SHA authority
→ read workflow + sequence + module/flow/symbol indexes
→ determine sequence mode
→ freeze plan if BEFORE
→ declare DOC IMPACT
→ reproduce/baseline
→ implement minimum valid source/spec change
→ generate code facts
→ generate project docs
→ generate actual sequence graph
→ validate plan-vs-actual or actual-only contract
→ classify/repair mismatch if any
→ targeted tests
→ cumulative regression
→ update .workflow state + roadmap in one transaction when phase changes
→ update .workflow acceptance/evidence state
→ regenerate project docs
→ PROJECT_DOCS_SYNC validation
→ documentation/cross-doc validation
→ runtime/E2E when required
→ final regeneration
→ final validators
→ final handoff
```

For generated-documentation mode, do not manually update
TEST_ACCEPTANCE_MATRIX.md, CURRENT_STATE.md, FLOW_INDEX.md, or other root
Markdown. Update their upstream .workflow authority and regenerate.

## Structural index generation

Do not manually reconstruct facts that can be generated safely.

Available generators:

```bash
python scripts/initialize_project_truth.py
python .workflow/tools/extract_project_facts.py
python .workflow/tools/generate_project_docs.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/sync_project_truth.py
python scripts/selftest_project_truth_compiler.py

python .workflow/tools/generate_symbol_index.py
python .workflow/tools/generate_module_map.py
python .workflow/tools/generate_sequence_plan.py --plan <plan.json> --output <plan.mmd>
python .workflow/tools/generate_sequence_actual.py --output-json <actual.json> --output-mermaid <actual.mmd>
python .workflow/tools/validate_sequence_contract.py --session <session.json>
python .workflow/tools/validate_sequence_sessions.py
```

The Project Truth Compiler is the preferred documentation path for
STANDARD/STRICT. Legacy individual index generators remain useful for targeted
inspection and LITE/manual compatibility.

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

- root `AGENTS.md` is missing, generated, or malformed;
- `.workflow/roadmap.json` is missing;
- `.workflow/state.json::phase` differs from `.workflow/roadmap.json::current_phase`;
- ROADMAP_SYNC is not PASS for generated-documentation mode;
- generated-documentation mode is enabled but PROJECT_DOCS_SYNC is not PASS;
- a generated `docs/` Markdown contract was manually edited instead of changing its upstream authority;
- source/spec changed but generated docs are stale;
- human-visible behavior changed but SYSTEM_OVERVIEW is stale;
- sequence-required workflow changed but generated actual sequence evidence is stale;
- BEFORE implementation exists without a proven pre-implementation frozen plan;
- DURING/AFTER contains a retrospective plan;
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

- SYSTEM_OVERVIEW still matches the current human/domain mental model;
- applicable sequence session uses the correct BEFORE/DURING/AFTER mode;
- generated actual sequence graph matches current source-content digest;
- BEFORE plan lineage predates implementation;
- every changed authority-bearing symbol is indexed;
- every changed call path is reflected in FLOW_INDEX;
- line-range hints are refreshed or marked STALE;
- current authority SHA/state is correct;
- roadmap current phase equals project current phase and exactly one roadmap phase is CURRENT;
- acceptance evidence matches tests actually executed;
- known defects are current;
- no required document is silently skipped;
- generated docs reproduce exactly from current source + semantic specs.

When available, run:

```bash
python .workflow/tools/validate_handoff.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/validate_doc_quality.py
python .workflow/tools/validate_human_comprehension.py --require-pass
python .workflow/tools/validate_sequence_sessions.py
python .workflow/tools/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base
```

All required validators are blocking gates. The human-comprehension validator checks coverage/status, while the cross-document validator scans all project Markdown, stable claims, local references, selected authority fields, and required doc freshness from the accepted/base SHA.

A validator PASS does not prove semantic correctness, but validator FAIL blocks completion.

## Final report documentation block

Every build/repair final report MUST include:

```text
DOCUMENTATION SYNC:
PASS / FAIL

SYSTEM_OVERVIEW:
UPDATED / NO IMPACT

HUMAN_COMPREHENSION_GATE:
PASS / FAIL / NOT_PROVEN

SEQUENCE_MODE:
BEFORE / DURING / AFTER / NOT_APPLICABLE

SEQUENCE_SYNC:
PASS / FAIL / NOT_PROVEN / NOT_APPLICABLE

ROADMAP_SYNC:
PASS / FAIL / NOT_PROVEN

PROJECT_DOCS_SYNC:
PASS / FAIL / NOT_PROVEN / NOT_APPLICABLE

PROJECT TRUTH COMPILER:
PASS / FAIL / NOT_AVAILABLE

CURRENT_STATE:
UPDATED / NO IMPACT

ROADMAP:
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

HUMAN COMPREHENSION VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

SEQUENCE CONTRACT VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

CROSS-DOCUMENT VALIDATOR:
PASS / FAIL / NOT_AVAILABLE

STALE REQUIRED DOCS:
0 / <count>
```

If a required documentation item is stale, final status cannot be PASS.

# 21. Definition of done

A task is DONE only when source/contract repair is complete, regression exists,
required runtime/E2E ran, documentation sync passes, HUMAN_COMPREHENSION_GATE
passes, applicable SEQUENCE_SYNC passes, DOC_LAYOUT /
PROJECT_DOCS_NORMALIZED / DOC_READABILITY / PROJECT_DOCS_SYNC pass when
generated documentation is enabled, affected projections/contracts are current, final
tested SHA is known, and evidence boundary is explicit.

A handoff is DONE only when the next room can continue safely without reconstructing authority from old chat messages.
