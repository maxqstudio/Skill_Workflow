<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Validation Architecture

Skill Workflow V2 improves speed by reusing work **inside one execution** while preserving fresh final acceptance.

## Immutable process-local snapshot

The engine can discover source files, read bytes, calculate digests, and derive facts once per execution. Reuse is an acceleration mechanism, not authority.

```text
cache/snapshot hit != PASS
```

Final acceptance starts from an exact candidate and must re-establish the evidence required by the project contract.

## Execution modes

### Develop

Runs targeted work only when changed-file impact can be classified safely. Unknown impact escalates.

### Verify

Produces intermediate, read-only evidence. It cannot claim complete acceptance.

### Finalize

Runs the complete required validation DAG and is the only final acceptance authority.

## Validation DAG

The V2 engine avoids repeated nested validators by sharing one snapshot and executing required gates through dependency-aware orchestration. It optimizes duplicate work rather than deleting gates.

Typical final concerns include:

```text
source facts / tests
→ generated Project Truth
→ doc structure + reproducibility
→ sequence evidence when required
→ cross-document consistency
→ Human Comprehension
→ project-state/provenance truth
→ runtime/E2E when required
→ exact-head / clean-worktree final boundary
```

## Evidence boundaries

Every validator should state what it proves and what it does not. Static structure does not automatically prove runtime ordering, and a documentation layout PASS does not prove semantic understanding.

## Documentation layers in this repository

`docs/handbook/` is the public product layer. Generated uppercase files under `docs/` remain the self-governed Project Truth layer. Keeping those layers separate avoids forcing a breaking path migration onto consumer projects merely to improve this repository's public presentation.
