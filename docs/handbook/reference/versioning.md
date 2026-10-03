<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Schema and toolchain versioning

Skill Workflow separates **schema compatibility** from **release naming**. The current governance contract uses schema version `1`; a stable Skill Workflow V2 release/tag is intentionally deferred to SW2-09.

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
- Stable product release/version labels are separate from schema versions and remain SW2-09 scope.
