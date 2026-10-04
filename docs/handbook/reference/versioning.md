<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Schema and toolchain versioning

Skill Workflow separates **schema compatibility** from **release naming**. The current governance contract uses schema version `1`; stable Skill Workflow V2 publication is governed by SW2-09 and remains blocked until exact release acceptance passes.

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
5. Re-run the source tests required by that project, then validate the restored toolchain and regenerate deterministic Project Truth:

```bash
python .workflow/tools/validate_schema_toolchain.py --root .
python .workflow/tools/sync_project_truth.py --root .
```

6. Run the project’s complete final acceptance boundary before treating the rollback as accepted.

If the previous accepted state predates schema v1 entirely, use the Skill Workflow tooling that was accepted with that state. Do not run the v1 migration again merely to make the rollback validate under newer tooling. A failed migration is repaired forward only after its root cause is understood and a fresh candidate is tested.

## Toolchain lock

Projects with vendored governance tools store `.workflow/toolchain.lock.json`. The lock records the exact `.workflow/tools/*.py` file hashes and a deterministic manifest digest. Final validation recomputes those hashes; a changed, missing, or unexpected vendored Python tool invalidates the lock.

Producer repository and commit fields are provenance hints. The file manifest and digest bind the actual vendored tool bytes; cache state, mutable upstream state, and an unlocked tool directory are not acceptance authority.

Validate directly with:

```bash
python .workflow/tools/validate_schema_toolchain.py --root .
```

## Compatibility policy

- Schema v1 is the only supported profile/governance-spec schema in this phase.
- Backward compatibility for legacy unversioned projects is provided through the explicit v1 migration command, not silent parser fallback.
- Unknown future versions fail closed. Existing tools never downgrade them.
- An incompatible schema change requires a new schema version, an explicit deterministic migration path, negative tests for unsupported versions, and an update to this compatibility policy.
- Stable product release/version labels are separate from schema versions and require their own exact release evidence.
