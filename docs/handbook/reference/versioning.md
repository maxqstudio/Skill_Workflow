<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Schema and toolchain versioning

Skill Workflow separates **schema compatibility** from **release naming**. The current governance contract uses schema version `1`, and the current stable product release is `v2.1.0`. The active governance phase is authoritative in `.workflow/roadmap.json` and is projected for readers in generated `docs/CURRENT_STATE.md`; this source-authored reference intentionally does not hard-code the mutable phase identifier. Stable product publication is authorized only by an explicit stable-release phase contract and exact release evidence; schema versioning does not grant publication authority.

## Supported schema

`PROJECT_PROFILE.yaml` must declare:

```yaml
schema_version: 1
```

Every governed JSON semantic spec under `.workflow/*.json` and `.workflow/workflows/*.json` must declare integer `schema_version: 1`. Missing, malformed, or unknown future versions fail closed. Tooling must never guess that an unknown schema is compatible.

## Explicit migration

Legacy unversioned governance state is migrated from the intended Skill Workflow source checkout:

```bash
python scripts/migrate_governance_v1.py --root <project>
```

The v1 migration adds only missing v1 schema metadata to governance profile/spec files, synchronizes the governed vendored tool set, and writes a toolchain lock. Running the same migration again is byte-stable for the governed migration targets. A project declaring an unsupported future version is rejected without being downgraded or silently rewritten.

Use check mode when auditing before mutation:

```bash
python scripts/migrate_governance_v1.py --root <project> --check
```

## Rollback after migration

Skill Workflow does not provide or infer a reverse schema migration. Rollback means returning the project to a previously accepted repository state, not deleting version metadata by hand.

1. Stop further governance or release mutation and preserve the failed candidate SHA plus its evidence.
2. Identify the last accepted project commit or release that predates the migration.
3. Revert the migration commit with normal version-control history (for example, `git revert <migration-commit>`) or restore the governed files from that known-good commit on a recovery branch. Do not force-reset shared history.
4. Restore the matching vendored `.workflow/tools/` files and `.workflow/toolchain.lock.json` from the same known-good state. Do not mix a previous schema/spec state with a newer toolchain lock.
5. Run the full governance acceptance path on the restored state, including `validate_schema_toolchain.py`, Project Truth synchronization, sequence validation when required, and the project acceptance suite.
6. Record the rollback/revert evidence through normal repair-forward project history. Never move an existing stable tag backward to make the rollback appear to be the original release.

After migration or rollback, regenerate Project Truth with `sync_project_truth.py` and validate the resulting repository state before claiming acceptance.

## Toolchain identity

`migrate_governance_v1.py` records a deterministic toolchain lock for governed `.workflow/tools/*.py` files. Exact file hashes and an aggregate manifest digest are the enforceable identity. Producer repository/commit fields are provenance hints only; they are not acceptance authority.

Cache state, Python bytecode, mutable upstream `main`, or package-manager cache contents must not be treated as toolchain identity.

## Compatibility and release naming

Schema v1 is the current compatibility contract. Product release tags such as `v2.0.0` and `v2.1.0` identify accepted product snapshots; they do not change the meaning of `schema_version: 1` unless an explicit migration says otherwise.

Unknown future schema versions remain fail-closed until a deliberate migration path is added and accepted.
