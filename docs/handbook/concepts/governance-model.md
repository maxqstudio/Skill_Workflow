<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Governance Model

Skill Workflow separates **authority**, **projection**, and **evidence** so documentation can help orientation without becoming a competing truth source.

## Authority layers

```text
source code
= implementation

.workflow/*.json
= semantic and governance contract

tests / runtime / physical evidence
= observed behavior

generated Project Truth Markdown
= deterministic projection for humans
```

When these layers disagree, repair the layer that is actually wrong. Do not edit a generated projection to hide a source/spec conflict.

## Profiles are adaptive

LITE, STANDARD, and STRICT exist because a small utility and an audit-sensitive trading system should not carry identical ceremony. Validators derive required documents from `PROJECT_PROFILE.yaml` rather than one universal pack.

## Roadmap authority is mandatory

`.workflow/roadmap.json` is the machine-readable roadmap authority. Exactly one phase is `CURRENT`, and `.workflow/state.json::phase` must match `roadmap.current_phase`. Phase drift blocks acceptance.

## Fail-closed acceptance

```text
source changed    != source tests passed
unit PASS         != runtime PASS
runtime starts    != UI/E2E PASS
historical proof  != current execution
recorded PASS     != executable validator PASS
```

Final acceptance binds exact source provenance, required validation, project state, documentation sync, sequence sync when applicable, and runtime/E2E evidence when required.

## Generated documentation

STANDARD and STRICT use deterministic compilation. An LLM can propose structured spec changes, but canonical tracked Project Truth must be reproducible from machine-readable inputs.

## Public documentation vs project state

In the Skill Workflow repository itself, `docs/handbook/` is source-authored product documentation. The uppercase generated files in `docs/` are this repository's governed Project Truth. This separation is repository product information architecture; it does **not** move or weaken the canonical generated-doc layout used by consumer projects.
