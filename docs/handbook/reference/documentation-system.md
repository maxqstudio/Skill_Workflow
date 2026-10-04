<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Documentation system

Skill Workflow separates documentation by authority and audience so public guidance stays readable while machine-backed governance remains deterministic.

## Documentation layers

### 1. Source-authored root and public documentation

`README.md`, root `AGENTS.md`, `docs/README.md`, and `docs/handbook/` are source-authored. `AGENTS.md` is mandatory at repository root for every governance profile and provides the coding-agent startup/operating contract; it is not generated Project Truth. The other public documents explain the product, adoption flow, operating model, architecture, and reference material.

Edit these files directly when the product guidance itself changes.

### 2. Generated Project Truth

Uppercase Markdown files in `docs/` are generated from source code, `.workflow/*.json`, and evidence. Examples include `CURRENT_STATE.md`, `ROADMAP.md`, `SYSTEM_OVERVIEW.md`, and `PROJECT_TRUTH_SYNC.md`.

Generated Markdown is a projection. Never repair these files manually. Change the authoritative source/spec, then run:

```bash
python scripts/sync_project_truth.py --root .
```

Consumer repositories normally use the vendored equivalent under `.workflow/tools/`.

### 3. Sequence evidence

`docs/sequence/sessions/` contains session contracts. `docs/sequence/generated/` contains generated JSON/Mermaid evidence. `docs/sequence/views/` contains bounded human-facing Markdown views.

## GitHub-facing sequence views

Raw `.mmd` files are machine evidence and should not be the primary link for readers. GitHub-facing navigation should point to the Markdown human view under `docs/sequence/views/`, where the Mermaid block is embedded in a page with context and evidence metadata.

The CI sequence lane regenerates the current graph, validates the machine contract, validates the human projection, and renders Mermaid with `@mermaid-js/mermaid-cli`. A render failure is blocking.

## Editing rules

| Change | Edit directly? | Then |
| --- | --- | --- |
| Root `AGENTS.md` operating contract | Yes | run root/project-doc validation |
| Public explanation / tutorial | Yes | run public-doc validation |
| `.workflow/*.json` authority | Yes, under governance | regenerate Project Truth |
| Generated uppercase Markdown | No | change authority/source and regenerate |
| Sequence session contract | Yes, under governance | regenerate actual + human views |
| Generated sequence JSON / `.mmd` | No | rerun sequence generators |

## Canonical paths

Public cleanup must not relocate canonical generated paths simply to reduce directory clutter. Existing consumers and validators may bind those paths. Improve discoverability through indexes and navigation; move canonical paths only through an explicitly versioned compatibility change.

## Validation

The public documentation layer is checked by:

```bash
python scripts/selftest_public_docs.py
python scripts/validate_public_docs.py --root .
python scripts/validate_project_docs.py --root .
python scripts/validate_cross_document_consistency.py --root .
```

Final governed acceptance still requires the full exact-head matrix; documentation checks do not replace source, sequence, or governance evidence.
