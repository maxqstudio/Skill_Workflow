# SEQUENCE CONTRACTS

Status: CURRENT

This document is the project-level index for machine-generated sequence acceptance.

Sequence diagrams are generated artifacts. Do not hand-edit canonical plan or
actual Mermaid files.

## Modes

| Mode | Use when | Plan | Actual | Primary acceptance |
|---|---|---|---|---|
| BEFORE | Contract exists before implementation starts | Required and frozen | Generated from implementation | PLAN ↔ ACTUAL |
| DURING | Workflow adoption begins while implementation is already in progress | Not applicable | Generated from current code | ACTUAL ↔ SOURCE / TEST / RUNTIME |
| AFTER | Workflow is reconstructed after implementation is complete | Not applicable | Generated from final code | FINAL ACTUAL ↔ SOURCE / TEST / RUNTIME |

## Anti-retroactive-plan rule

A BEFORE plan is valid only when Git lineage proves that the frozen plan
preceded implementation work.

A plan created after implementation started is not a BEFORE plan.

When that happens, use DURING or AFTER.

Never create a retrospective plan merely to make PLAN_ACTUAL_MATCH pass.

## Canonical machine artifacts

Recommended structure:

```text
docs/sequence/
  sessions/
    <phase>-<session>.json
  plans/
    <phase>-<session>.plan.json
  generated/
    <phase>-<session>.plan.mmd
    <phase>-<session>.actual.json
    <phase>-<session>.actual.mmd
  runtime/
    <phase>-<session>.runtime.json
  reports/
    <phase>-<session>.acceptance.json
```

Plan Mermaid is generated from the frozen machine-readable plan.

Actual JSON and Mermaid are generated from the codebase and optional runtime
trace.

Generated Mermaid files are views, not editable authority.

## Flow inventory

| Session / Flow | Phase | Mode | Critical | Session contract | Status |
|---|---|---|---|---|---|

## BEFORE acceptance

Required:

```text
PLAN_EXISTS
PLAN_FROZEN
PLAN_PRECEDES_IMPLEMENTATION
PLAN_HASH_MATCH
PLAN_DIAGRAM_GENERATED
ACTUAL_GRAPH_GENERATED
ACTUAL_DIAGRAM_GENERATED
PLAN_ACTUAL_MATCH
MISSING_REQUIRED_EDGES = 0
FORBIDDEN_EDGES_PRESENT = 0
UNRESOLVED_CRITICAL_BINDINGS = 0
SEQUENCE_SYNC = PASS
```

If runtime sequence evidence is required by project/session policy, runtime
comparison is also blocking.

## DURING acceptance

Plan is NOT_APPLICABLE.

Required:

```text
ACTUAL_GRAPH_GENERATED
ACTUAL_DIAGRAM_GENERATED
ACTUAL_SOURCE_SHA = FINAL_SOURCE_SHA
SOURCE_ACTUAL_SYNC = PASS
TEST_TRACEABILITY = PASS when required
RUNTIME_ACTUAL_SYNC = PASS / NOT_APPLICABLE
UNRESOLVED_CRITICAL_EDGES = 0
SEQUENCE_SYNC = PASS
```

Do not synthesize a historical plan.

## AFTER acceptance

Plan is NOT_APPLICABLE.

Required:

```text
FINAL_ACTUAL_GRAPH_GENERATED
FINAL_ACTUAL_DIAGRAM_GENERATED
FINAL_SOURCE_BINDING = PASS
TEST_TRACEABILITY = PASS when required
RUNTIME_ACTUAL_SYNC = PASS / NOT_APPLICABLE
UNRESOLVED_CRITICAL_EDGES = 0
SEQUENCE_SYNC = PASS
```

## Mismatch handling

A mismatch is not automatically a code defect.

Classify first:

```text
CODE_DEFECT
PLAN_CHANGE
GENERATOR_DEFECT
```

Then:

```text
classify
→ repair the correct authority
→ regenerate
→ validate again
```

PLAN_CHANGE in BEFORE mode requires explicit authorized plan revision. Freeze a
new plan version before implementing that revised behavior.

## Generated-file rule

Canonical Mermaid files must be reproducible from their machine-readable graph.

If a generated Mermaid file differs from deterministic renderer output:

```text
GENERATED_DIAGRAM_TAMPERED = FAIL
```

## Evidence boundary

Static analysis cannot perfectly resolve dependency injection, reflection,
dynamic dispatch, callbacks, framework magic, or all cross-language edges.

Therefore:

- unresolved critical edges block acceptance;
- runtime trace may be required for dynamic critical paths;
- generator PASS does not itself prove behavioral correctness.
