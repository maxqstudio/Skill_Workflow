<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Adopting Skill Workflow

Adoption starts by making project authority explicit before adding more process.

## 1. Choose the governance profile

Every governed project defines `PROJECT_PROFILE.yaml`.

- **LITE** — small, low-complexity projects; manual Markdown may be allowed when explicitly configured.
- **STANDARD** — normal multi-session/multi-agent work; deterministic generated Project Truth is required.
- **STRICT** — audit-sensitive, production, financial/trading, research/ML, hardware, or complex multi-repository systems; full truth-ledger discipline is required.

Choose by risk, workflow complexity, runtime dependencies, and evidence requirements—not source-line count alone.

## 2. Initialize Project Truth

From a Skill Workflow checkout/package, run the initializer against the target repository:

```bash
python scripts/initialize_project_truth.py --root /path/to/project
```

The initializer creates the profile/spec skeleton and vendors the runtime tools under `.workflow/tools/`.

### Toolchain identity and later upgrades

Initialization records a content manifest and exact source-content identity in `.workflow/toolchain.lock.json`. A Git checkout records stronger `GIT+CONTENT` provenance with repository/SHA/release; a copied skill/package without `.git` records `CONTENT` identity and explicitly marks Git-only fields `NOT_PROVEN`. Updating an installed agent skill does not silently replace the vendored governance tools already committed in a consumer repository. To inspect a later Skill Workflow checkout/package against an existing consumer, run `scripts/upgrade_governance_toolchain.py --root <project> --check` from that source and review the machine-readable plan before using `--apply`. Legacy hint-only locks require this explicit migration path, and weaker package metadata must not downgrade stronger provenance for identical content.

## 3. Populate semantic authority

Code can reveal structure, but it cannot safely invent Owner intent, legal state transitions, authority precedence, acceptance meaning, or design rationale. Declare those facts in `.workflow/*.json`.

```text
source code                  = implementation facts
.workflow/*.json             = semantic/governance intent
tests + runtime evidence     = behavioral truth
generated Markdown           = deterministic human projection
```

## 4. Synchronize generated documentation

```bash
python .workflow/tools/sync_project_truth.py --root .
```

For STANDARD/STRICT projects, do not repair generated Markdown by hand. Change source and/or the structured authority, then regenerate.

## 5. Work in the right execution mode

- `develop` may run targeted work based on safely classified impact.
- `verify` is intermediate, read-only evidence.
- `finalize` is the only complete final acceptance authority.

Unknown impact escalates rather than silently skipping required work.

## 6. Accept only exact evidence

A safe final boundary requires the tested source, generated docs, evidence, and final Git HEAD to agree. `NOT_RUN`, `NOT_PROVEN`, or a failed required gate cannot be rewritten as PASS.

Read the [governance model](../concepts/governance-model.md) before tightening a project to STRICT.
