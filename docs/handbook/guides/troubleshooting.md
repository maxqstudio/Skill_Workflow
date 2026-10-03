<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Troubleshooting

Repair the failing authority or evidence. Do not bypass the gate just to obtain green output.

## Project docs are stale

Typical signal: `PROJECT_DOCS_SYNC = FAIL`.

```text
identify changed source/spec authority
→ update the correct .workflow JSON or source
→ run sync_project_truth.py
→ rerun validators
```

Do not hand-edit generated Project Truth as the fix.

## Roadmap and current phase disagree

Typical signal: `ROADMAP_SYNC = FAIL`.

Update `.workflow/state.json` and `.workflow/roadmap.json` in the same phase-transition transaction. Exactly one roadmap phase must remain `CURRENT`.

## Cross-document validation fails

Use the reported broken path, symbol, claim, or stale-document relation. A structurally valid link does not prove semantic correctness; after mechanical repair, review the mapped source/tests as well.

## Sequence validation fails

Classify the mismatch before changing anything: `CODE_DEFECT`, `PLAN_CHANGE` (BEFORE mode only), or `GENERATOR_DEFECT`. For human Sequence V2 views, full machine evidence remains acceptance evidence. Do not delete machine edges to make a diagram prettier.

## Mermaid text exists but rendering fails

Rendering failure is still failure. Governed human-facing Mermaid must pass the parser/renderer gate and produce non-empty output.

## A fast mode passes but final acceptance does not

This is expected when intermediate evidence is insufficient. `develop` and `verify` cannot replace `finalize`.

## A validator reports PASS but behavior is uncertain

Respect the validator's evidence boundary. Structural/project-state validators do not prove runtime, scientific, UI, device, or semantic behavior unless that evidence is explicitly part of their contract.
