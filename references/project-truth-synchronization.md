# Project Truth Synchronization and Human Comprehension

This is a normative bundled reference for `SKILL.md`. Read it when proving project truth, traceability, semantic/behavioral sync, cross-document consistency, or human comprehension.

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
7. HUMAN COMPREHENSION
8. SEQUENCE SYNC
9. PROJECT DOCS SYNC
10. DOC ↔ SOURCE TRACEABILITY
11. DOC ↔ TEST TRACEABILITY
12. TEST ↔ RUNTIME TRACEABILITY

Overall invariant:

SOURCE TESTS PASS + DOCS IN SAME TESTED SNAPSHOT + STRUCTURAL SYNC PASS +
SEMANTIC SYNC PASS + BEHAVIORAL SYNC PASS + CROSS-DOCUMENT CONSISTENCY PASS +
HUMAN_COMPREHENSION PASS + SEQUENCE_SYNC PASS/NOT_APPLICABLE +
DOC_LAYOUT PASS/NOT_APPLICABLE + PROJECT_DOCS_NORMALIZED PASS/NOT_APPLICABLE +
DOC_READABILITY PASS/NOT_APPLICABLE + PROJECT_DOCS_SYNC PASS/NOT_APPLICABLE +
TRACEABILITY PASS =
PROJECT_STATE_SYNC PASS.

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

## Generated facts vs semantic specs

Prefer machine-generated facts for implementation-observable structure.

Purpose, authority, lifecycle meaning, invariants, legal transitions, failure
semantics, evidence interpretation, and Owner intent remain explicit semantic
inputs under .workflow.

In generated-documentation mode, these semantics are maintained once in the
structured spec layer and projected into all affected Markdown documents.

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
HUMAN_COMPREHENSION: PASS
SEQUENCE_SYNC: PASS / NOT_APPLICABLE
DOC_LAYOUT: PASS / NOT_APPLICABLE
PROJECT_DOCS_NORMALIZED: PASS / NOT_APPLICABLE
DOC_READABILITY: PASS / NOT_APPLICABLE
PROJECT_DOCS_SYNC: PASS / NOT_APPLICABLE
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

python .workflow/tools/validate_handoff.py
python .workflow/tools/validate_project_docs.py
python .workflow/tools/validate_human_comprehension.py --require-pass
python .workflow/tools/validate_sequence_sessions.py
python .workflow/tools/validate_cross_document_consistency.py --base <LAST_ACCEPTED_SHA> --require-base

For STRICT, or when PROJECT_TRUTH_SYNC.md is present:

python .workflow/tools/validate_project_truth.py

A skipped validator must be justified by PROJECT_PROFILE.yaml, never by convenience.

Structural validator PASS is necessary but not sufficient for semantic truth.

## Definition of done override

A task is DONE only when source/contract repair is complete, required
tests/runtime evidence pass, DOC_SYNC passes, HUMAN_COMPREHENSION_GATE passes,
applicable SEQUENCE_SYNC passes, DOC_LAYOUT / PROJECT_DOCS_NORMALIZED /
DOC_READABILITY / PROJECT_DOCS_SYNC pass when generated documentation is
enabled, PROJECT_STATE_SYNC passes, final tested HEAD equals
final source/documentation HEAD, and evidence boundaries are explicit.


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
python .workflow/tools/validate_cross_document_consistency.py \
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


# 23. Human-first comprehension contract

The project documentation must support two different readers:

```text
HUMAN
→ understand the system without opening code

AGENT / DEVELOPER
→ locate exact source without rereading the whole codebase
```

The intended drill-down is:

```text
SYSTEM_OVERVIEW
→ CURRENT_STATE
→ PROJECT_MANIFEST
→ ARCHITECTURE
→ WORKFLOW_STATE_MACHINE
→ FLOW_INDEX
→ MODULE_MAP / SYMBOL_INDEX
→ SOURCE CODE
```

SYSTEM_OVERVIEW.md is mandatory for every governance profile.

## Human Comprehension Gate

A reviewer must be able to answer, from documentation alone:

- What is the project and what problem does it solve?
- Who uses it and what outcomes does it produce?
- What are the major components?
- How does important data move through the system?
- What are the main user/domain workflows?
- What are the important states and legal transitions?
- Who or what is authoritative for important decisions?
- What is mutable and what is immutable?
- How does failure/recovery behave?
- What is the current project state?
- What is proven and what is not proven?
- What action is legal next and what is blocked?

If any applicable answer requires source-code reconstruction:

```text
HUMAN_COMPREHENSION_GATE = FAIL
```

Run:

```bash
python .workflow/tools/validate_human_comprehension.py --require-pass
```

The validator proves structural coverage and explicit status only.

It MUST NOT be presented as proof of semantic correctness or actual human
understanding. The final semantic review compares SYSTEM_OVERVIEW.md against
current authority, workflow, test, and runtime evidence.

## Human-first writing rule

SYSTEM_OVERVIEW.md should use domain language first.

Prefer:

```text
Owner selects a qualified candidate
→ system revalidates evidence
→ Challenger is created
```

over:

```text
OptimizerPage.tsx
→ POST /api/...
→ service.py::function()
```

The engineering call chain belongs in FLOW_INDEX.md.

The two documents must describe the same behavior at different abstraction
levels.
