---
name: project-handoff-workflow
description: Help humans understand and agents safely orient, hand off, audit, repair, and continue software projects using human-first overviews, authority maps, architecture, workflows, indexes, and evidence-based acceptance.
---

# PROJECT HANDOFF & CODEBASE ORIENTATION SKILL

## Purpose

Use this skill to understand, continue, audit, repair, or hand off software projects safely across rooms, agents, and developers.

This skill is project-agnostic. It uses progressive disclosure: this root file is the mandatory eager operating contract; detailed normative rules live in the bundled `references/` files routed below and MUST be read when their routing condition applies.

## 1. Mandatory startup order

Do not begin by reading the entire repository blindly.

Start with the smallest authority map that can orient the task:

```text
AGENTS.md
→ PROJECT_PROFILE.yaml
→ docs/SYSTEM_OVERVIEW.md
→ docs/CURRENT_STATE.md
→ docs/ROADMAP.md
→ docs/PROJECT_MANIFEST.md
→ only profile-required authority / architecture / workflow / contract docs
→ docs/SEQUENCE_CONTRACTS.md when sequence policy is enabled
→ MODULE / FLOW / SYMBOL indexes when needed
→ docs/TEST_ACCEPTANCE_MATRIX.md
→ exact relevant source ranges
→ runtime/E2E evidence when required
```

`AGENTS.md` is mandatory, source-authored, repository-root operating guidance for LITE, STANDARD, and STRICT. Read it first. Do not generate it or relocate it under `docs/`.

`PROJECT_PROFILE.yaml` is mandatory and selects the governance profile and applicability rules. Governed schema versions are explicit; missing or unsupported versions fail closed rather than being guessed.

Do not recursively scan the repository unless navigation evidence is missing/stale/conflicting, corruption is suspected, or a full audit is explicitly requested.

## 2. Authority hierarchy and Project Truth

Treat these layers differently:

```text
SOURCE CODE
= implementation facts

.workflow/*.json
= semantic / governance intent

tests + runtime evidence
= behavioral truth

generated Markdown under docs/
= deterministic human-readable projection
```

Generated Markdown is not upstream authority. In generated-documentation mode, repair source and/or `.workflow` specs, regenerate, then validate. Manual edits to generated `docs/` contracts do not establish truth.

The canonical generator must be deterministic. Do not use LLM-produced prose as the canonical tracked projection.

The project phase contract is blocking:

```text
.workflow/state.json::phase
=
.workflow/roadmap.json::current_phase
```

Exactly one roadmap phase is `CURRENT`. Advance state and roadmap in the same project-state transaction, then regenerate Project Truth.

For the complete profile, compiler, docs-layout, and document-responsibility contract, read `references/governance-and-project-truth.md` before acting in that scope.

## 3. Non-negotiable operating invariants

Never invent authority, tests, runtime evidence, legal transitions, Owner intent, or semantic meaning.

Never treat source changed as equivalent to PASS.

Do not redesign architecture, UI, or workflow unless required by a confirmed defect, explicit Owner request, or accepted roadmap change.

Separate:

- ACTIVE STATE from HISTORICAL EVIDENCE and ARCHIVE;
- CURRENT CONFIGURATION from FROZEN EXECUTION SNAPSHOT;
- machine-observable facts from semantic claims;
- static structural evidence from runtime behavior.

Unknown impact, missing authority, parser limitations, unresolved dynamic behavior, classifier failure, or contradictory evidence must broaden verification or remain `NOT_PROVEN`; they must never create a narrower false PASS.

Documentation is part of project state:

```text
SOURCE PASS + DOC_SYNC FAIL = OVERALL FAIL
```

A source/spec change that leaves an affected contract, index, acceptance ledger, current state, or generated projection stale is a project defect.

## 4. Build and repair discipline

For every change:

```text
identify exact accepted/base SHA
→ reproduce defect or establish baseline
→ determine root cause / authorized scope
→ declare documentation and sequence impact
→ implement minimum valid change
→ add regression coverage
→ regenerate machine-derived facts / Project Truth / sequence evidence as applicable
→ run targeted tests
→ run cumulative regression
→ run runtime/E2E when required
→ finalize on the exact candidate HEAD
→ verify clean governed worktree
→ hand off with explicit evidence boundary
```

Exact-source lineage is mandatory:

```text
FINAL SOURCE SHA = TESTED SHA
```

For final acceptance across source and documentation:

```text
TESTED_HEAD = FINAL_SOURCE_HEAD = FINAL_DOCUMENTATION_HEAD
```

Do not make a report-only source commit after final testing and still claim the prior SHA as final acceptance.

For the full execution modes, defect handling, handoff fields, documentation transaction, hard gates, and final report contract, read `references/execution-and-acceptance.md` before acting in that scope.

## 5. Fast governance modes

Governance Engine V2 supports:

```text
develop → verify → finalize
```

`develop` and `verify` are intermediate evidence only. They cannot accept a requirement, phase, release, or `PROJECT_STATE_SYNC`.

`finalize` is the only fast-workflow mode that may provide final acceptance authority. It requires exact-head provenance, the complete required regression graph, synchronized deterministic Project Truth, applicable human/sequence/handoff/cross-document gates, and a clean governed worktree.

Escalation from `verify` to a full graph does not silently convert the invocation into final acceptance authority.

## 6. Acceptance and evidence boundary

Acceptance reflects only the strongest evidence actually executed.

```text
unit PASS ≠ runtime PASS
runtime start ≠ UI E2E PASS
UI E2E PASS ≠ physical-device PASS
historical physical proof ≠ current physical execution
build success ≠ scientific validity
```

Use explicit states such as `PASS`, `FAIL`, `NOT_RUN`, `NOT_APPLICABLE`, `NOT_PROVEN`, and `BLOCKED`. Never convert missing evidence into PASS.

A validator PASS proves only its declared machine-verifiable boundary. Structural checks do not prove semantic correctness; static analysis does not prove runtime ordering.

Before final PASS, prove all gates required by `PROJECT_PROFILE.yaml` and state the evidence boundary.

## 7. Sequence governance core

When sequence policy is enabled, determine exactly one mode:

- `BEFORE`: a machine-readable plan is genuinely frozen before implementation; lineage must prove the frozen plan precedes implementation.
- `DURING`: implementation exists or is in progress; retrospective plans are forbidden; regenerate actual evidence as implementation changes.
- `AFTER`: completed implementation is reconstructed from final actual evidence; retrospective plans are forbidden.

Canonical plan/actual Mermaid is generated, never hand-authored. Human sequence views are separate bounded projections and must not replace full machine evidence or hide analyzer limitations.

`CURRENT` sequence sessions bind to the current source-content digest. Accepted prior sessions become `HISTORICAL` and are not regenerated to match later source.

Critical unresolved dynamic paths require runtime trace or a stronger project-specific extractor; do not guess.

For plan semantics, artifact layout, human projection rules, renderer gate, source-content binding, mismatch classification, commands, and final sequence gate, read `references/sequence-contracts.md` before acting in that scope.

## 8. Project Truth synchronization core

A matching SHA label alone is never sufficient. Project truth requires applicable provenance, reference, structural, semantic, behavioral, cross-document, human-comprehension, sequence, generated-doc, and traceability gates.

Provenance is established by testing an exact Git HEAD, requiring a clean final governed worktree, proving required source/docs are tracked in that same HEAD, and recording acceptance evidence externally or in a way that does not self-mutate the tested snapshot.

Required references must resolve. Broken required references fail closed.

Critical claims should trace bidirectionally:

```text
CLAIM / CONTRACT
↔ DOCUMENT(S)
↔ SOURCE OWNER
↔ TEST(S)
↔ RUNTIME/E2E EVIDENCE when required
```

If required behavioral evidence was not executed, keep behavioral truth `NOT_PROVEN` unless explicitly `NOT_APPLICABLE`.

For the complete truth-gate model, traceability relations, cross-document consistency, profile selection discipline, and Human Comprehension Gate, read `references/project-truth-synchronization.md` before acting in that scope.

## 9. Deterministic bundled reference routing

The following bundled references are normative extensions of this root contract. They are one-level paths relative to the skill root. When a task matches a routing condition, read the linked reference before acting; do not treat it as optional background.

| Task / concern | Required bundled reference |
|---|---|
| Profile selection, Project Truth Compiler, canonical docs layout, document responsibilities, optional contracts | [governance-and-project-truth](references/governance-and-project-truth.md) |
| Implementation/repair loop, develop/verify/finalize detail, acceptance, defects, redesign prevention, handoff, docs transaction, Definition of Done | [execution-and-acceptance](references/execution-and-acceptance.md) |
| Provenance/reference/structural/semantic/behavioral sync, cross-document consistency, traceability, human comprehension | [project-truth-synchronization](references/project-truth-synchronization.md) |
| BEFORE/DURING/AFTER sequence behavior, plan/actual evidence, human projection, Mermaid rendering, sequence validation | [sequence-contracts](references/sequence-contracts.md) |

Do not create multi-hop chains for required operating rules. Root `SKILL.md` must link required bundled references directly.

Public handbook pages explain the product to humans; they are not substitutes for these bundled agent-facing normative references.

## 10. Final operating rule

Before claiming completion:

1. verify exact repository / branch / accepted base / candidate HEAD authority;
2. verify affected `.workflow` authority and generated docs are synchronized;
3. verify roadmap/current-phase synchronization;
4. verify sequence policy and current session when applicable;
5. run targeted and cumulative regression;
6. run required runtime/E2E evidence;
7. run final profile-required validators against the accepted/base SHA;
8. require exact-head provenance and a clean governed worktree;
9. leave current state, acceptance evidence, and handoff synchronized.

If a required gate is `FAIL`, `NOT_PROVEN`, unresolved, or stale, final status cannot be PASS.
