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
5. Re-run the source tests required by that project, then validate the restored toolchain and regenerate deterministic Project Truth:

```bash
python .workflow/tools/validate_schema_toolchain.py --root .
python .workflow/tools/sync_project_truth.py --root .
```

6. Run the project’s complete final acceptance boundary before treating the rollback as accepted.

If the previous accepted state predates schema v1 entirely, use the Skill Workflow tooling that was accepted with that state. Do not run the v1 migration again merely to make the rollback validate under newer tooling. A failed migration is repaired forward only after its root cause is understood and a fresh candidate is tested.

## Toolchain lock

Projects with vendored governance tools store `.workflow/toolchain.lock.json`. The lock records the exact `.workflow/tools/*.py` file hashes and a deterministic manifest digest. Final validation recomputes those hashes; a changed, missing, or unexpected vendored Python tool invalidates the lock.

The lock binds **exact vendored tool bytes** through a deterministic file manifest and a mandatory source-content digest. When verifiable Git metadata is available, `identity_source=GIT+CONTENT` additionally binds the producer repository and exact source SHA; a release tag is recorded only when verifiable at HEAD. For installed/copied skill packages without `.git`, `identity_source=CONTENT` records the exact content digest while Git-only repository, source SHA, and release fields are explicitly `NOT_PROVEN`—they must not be invented. A legacy `commit_hint`-only lock is **migration input, not acceptance authority**. A package copy with unchanged bytes must not downgrade an existing stronger `GIT+CONTENT` lock. Cache state, mutable upstream state, and an unlocked tool directory are never acceptance authority.

Before changing a consumer's vendored toolchain, run an explicit **read-only** upgrade inspection from the desired Skill Workflow source checkout or package:

```bash
python scripts/upgrade_governance_toolchain.py --root <project> --check
```

Review the deterministic `PLAN_JSON` and the reported file classes before applying only toolchain-owned changes:

```bash
python scripts/upgrade_governance_toolchain.py --root <project> --apply
```

`--apply` must not overwrite the consumer's `AGENTS.md`, semantic `.workflow/*.json`, application source, or project-specific configuration. Repeated apply against identical source bytes is idempotent; unknown or tampered toolchain identity must fail closed. A successful toolchain upgrade does **not** bypass the consumer's own source/runtime/governance acceptance requirements.

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

## Consumer acceptance after an upgrade

A valid toolchain lock is necessary but not sufficient for acceptance. After using `--check` and `--apply`, commit the migrated consumer snapshot and run its own complete source tests and Project Truth validators through the vendored `finalize_consumer.py` command, with the exact committed consumer HEAD and the proven last accepted ancestor:

```bash
python .workflow/tools/finalize_consumer.py --root . --base <ACCEPTED_SHA> --expected-head <NEW_HEAD>
```

This consumer path differs from the Skill Workflow **producer's** `governance_engine.py --mode finalize`, which includes source-only producer regression scripts. Consumer finalization must never assume those scripts exist in application repositories. The consumer command requires declared source tests and all mandatory project-local validators to PASS on an unchanged, clean commit; it cannot promote historical runtime evidence or claim that other consumer repositories were upgraded.
