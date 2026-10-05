# Sequence Contract Acceptance

This is a normative bundled reference for `SKILL.md`. Read it whenever sequence policy is enabled or a governed flow changes.

# 24. Sequence Contract acceptance

Sequence diagrams are acceptance artifacts derived from machine-readable
contracts and source analysis. Canonical Mermaid must never be hand-authored or
hand-edited.

## Three modes

### BEFORE

Use only when a sequence plan truly exists before implementation begins.

```text
define intended flow
→ write machine-readable plan contract
→ generate plan Mermaid
→ commit/freeze plan
→ record frozen plan commit/hash
→ start implementation
→ generate actual graph from codebase
→ generate actual Mermaid
→ compare PLAN ↔ ACTUAL
→ classify mismatch
→ repair correct authority
→ regenerate
→ validate again
```

Git lineage must prove the direct path when commit ancestry is preserved:

```text
FROZEN_PLAN_COMMIT
is ancestor of
IMPLEMENTATION_BASE
is ancestor of
FINAL_HEAD
```

If repository policy requires squash merge, the branch ancestry is intentionally
removed from the product branch. In that case BEFORE evidence remains valid only
with explicit `merge_provenance` using `strategy = SQUASH`, and validation must
prove all of the following:

```text
FROZEN_PLAN_COMMIT
  -> IMPLEMENTATION_BASE
  -> ACCEPTED_BRANCH_HEAD

TREE(ACCEPTED_BRANCH_HEAD)
  = TREE(PRODUCT_MERGE_SHA)

PRODUCT_MERGE_SHA
  -> FINAL_HEAD
```

Tree identity is mandatory: a merely similar diff, matching message, or manually
asserted SHA is not sufficient. This bridge preserves the frozen BEFORE lineage
without pretending the squashed branch commit is a literal ancestor of main.

A plan created after implementation began is invalid as BEFORE evidence.

### DURING

Use when Skill Workflow / sequence governance is adopted while implementation is
already in progress.

```text
PLAN = NOT_APPLICABLE
current codebase
→ generated actual graph
→ generated actual Mermaid
→ source/test/runtime validation
```

Retrospective plans are forbidden.

DURING is continuous observation: regenerate actual sequence evidence as the
implementation changes.

### AFTER

Use when documenting/reconstructing a completed implementation.

```text
PLAN = NOT_APPLICABLE
final codebase
→ generated final actual graph
→ generated final actual Mermaid
→ source/test/runtime validation
```

Retrospective plans are forbidden.

## Machine-readable authority

Recommended artifacts:

```text
SEQUENCE_CONTRACTS.md
docs/sequence/sessions/<session>.json
docs/sequence/plans/<session>.plan.json          # BEFORE only
docs/sequence/generated/<session>.plan.mmd       # BEFORE only, generated
docs/sequence/generated/<session>.actual.json    # generated from code
docs/sequence/generated/<session>.actual.mmd     # generated from graph
artifacts/sequence/<session>.acceptance.json      # final evidence
```

The plan JSON is the BEFORE design contract.

The actual JSON is the machine observation of implementation.

Mermaid is only a deterministic rendering.

## Machine evidence vs human sequence view

Sequence V2 separates acceptance evidence from presentation:

```text
full machine actual.json / actual.mmd
= acceptance-relevant static evidence

separate human.json / human.mmd / docs/sequence/views/*.md
= deterministic bounded projection for humans
```

Required invariants:

- human projection MUST NOT delete, rewrite, or replace the full machine graph;
- every machine edge MUST remain accounted for by the projection, including
  edges collapsed inside one semantic component and repeated cross-component
  edges aggregated into one rendered interaction;
- semantic collapsing or subflows are preferred over exposing every helper as
  a participant;
- complexity policy MUST be deterministic, measurable, documented, and tested;
- do not invent an arbitrary global participant/interaction limit without
  baseline evidence and rationale;
- static human projection MUST NOT be described as runtime call ordering;
- inherited static-analyzer limitations remain visible evidence limitations and
  MUST NOT be hidden merely to improve the diagram.

Canonical tools when vendored by the initializer:

```bash
python .workflow/tools/sequence_human_view.py ...
python .workflow/tools/validate_sequence_human_view.py ...
python .workflow/tools/validate_sequence_sessions.py --root .
```

A human-facing Mermaid diagram is not accepted merely because text was
generated. CI MUST run an actual Mermaid parser/renderer (or equivalent
parser-backed render check) and fail if rendering fails. Renderer absence,
syntax failure, or empty render output MUST NOT be converted into PASS.

Therefore:

```text
MACHINE_EVIDENCE_PASS
+ HUMAN_PROJECTION_PASS
+ MERMAID_RENDER_FAIL
=
SEQUENCE_PRESENTATION FAIL
```

## Source-content binding

Do not require a tracked generated graph to contain the final commit SHA of the
commit that contains itself.

Actual graphs bind to a deterministic SOURCE_CONTENT_DIGEST calculated from
source files while excluding generated documentation/artifacts.

Final validation recomputes the digest and requires:

```text
ACTUAL_SOURCE_DIGEST = CURRENT_SOURCE_DIGEST
```

Git HEAD remains final provenance evidence separately.

## Plan edge semantics

Plan edges may use:

```text
MUST
MAY
MUST_NOT
```

and verification scope:

```text
SOURCE
RUNTIME
BOTH
DOCUMENT
```

Acceptance must not fail merely because harmless internal helper calls exist.

It must fail when required critical edges are missing, forbidden edges appear,
authority/order semantics are violated where verifiable, or critical bindings
remain unresolved.

## Mismatch classification

Never blindly repair code because a generated comparison failed.

First classify:

```text
CODE_DEFECT
PLAN_CHANGE
GENERATOR_DEFECT
```

Then repair the correct authority.

PLAN_CHANGE in BEFORE mode requires explicit authorization and a newly frozen
plan version before implementing the revised behavior.

## Generated-only diagram rule

Canonical plan/actual Mermaid files are generated.

If deterministic re-rendering does not match the stored Mermaid:

```text
GENERATED_DIAGRAM_TAMPERED = FAIL
```

## Required commands

BEFORE plan rendering:

```bash
python .workflow/tools/generate_sequence_plan.py \
  --plan docs/sequence/plans/<session>.plan.json \
  --output docs/sequence/generated/<session>.plan.mmd
```

Actual extraction:

```bash
python .workflow/tools/generate_sequence_actual.py \
  --output-json docs/sequence/generated/<session>.actual.json \
  --output-mermaid docs/sequence/generated/<session>.actual.mmd \
  --entry <path::symbol>
```

Per-session validation:

```bash
python .workflow/tools/validate_sequence_contract.py \
  --session docs/sequence/sessions/<session>.json
```

All-session acceptance:

```bash
python .workflow/tools/validate_sequence_sessions.py
```

## Current vs historical sequence evidence

Each sequence session is either:

```text
CURRENT
HISTORICAL
```

CURRENT sessions must match the current source-content digest.

HISTORICAL sessions preserve earlier accepted flow evidence and must not be
regenerated to match later source.

When a new phase/session becomes authoritative:

```text
previous accepted CURRENT
→ HISTORICAL

new phase/session
→ CURRENT
```

The aggregate validator may validate both, but only CURRENT sessions are bound
to today's source digest.

## Static-analysis boundary

The generic extractor currently provides machine-verifiable structural coverage
for Python AST calls/routes and JS/TS HTTP module edges.

It cannot perfectly infer every dependency-injection edge, reflection target,
callback/event, framework-generated dispatch, or dynamic runtime path.

For critical unresolved paths:

```text
do not guess
→ runtime trace or stronger project-specific extractor
→ regenerate
→ revalidate
```

A generated diagram is evidence only to the strength of the extractor/runtime
evidence that produced it.

## Sequence final gate

When sequence policy is required:

```text
SEQUENCE_SYNC = PASS
```

is required before PROJECT_STATE_SYNC may be PASS.
