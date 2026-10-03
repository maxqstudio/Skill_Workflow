<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Sequence Contracts and Sequence V2

Sequence evidence makes important flow assumptions explicit and auditable.

## Three modes

- **BEFORE** — a real plan exists before implementation and is frozen, then compared with generated actual behavior.
- **DURING** — implementation already exists/in progress; retrospective plan creation is forbidden.
- **AFTER** — final behavior is reconstructed after implementation; retrospective plan creation is also forbidden.

## Full machine evidence stays intact

Sequence V2 does not make acceptance graphs smaller by deleting evidence. The full static machine graph remains independently available as `actual.json` / `actual.mmd`.

## Human projection is separate

A bounded human view is derived from the machine graph. `module-collapse-v1` groups helper-level nodes into semantic modules/external boundaries and aggregates repeated directed component interactions.

Every machine edge must still be accounted for as either an internal edge collapsed inside one semantic component or a cross-component edge represented in an aggregated human interaction. The human projection is presentation, not replacement evidence.

## No invented universal size limit

Sequence complexity policy must be measurable and deterministic. Sequence V2 uses structural module/pair ceilings rather than pretending one arbitrary participant count is universally readable.

## Mermaid rendering is blocking

Generated Mermaid text is not sufficient proof. Governed human views must pass an actual parser/renderer check and produce non-empty render output.

## Static evidence is not runtime ordering

Static AST/module evidence proves source-visible structure only. Reflection, dynamic dispatch, framework behavior, and actual runtime order may require stronger runtime or semantic evidence when the project contract demands it.

For the repository's current governed sequence state, see [SEQUENCE_CONTRACTS](../../SEQUENCE_CONTRACTS.md) and the [sequence evidence directory](../../sequence/).
