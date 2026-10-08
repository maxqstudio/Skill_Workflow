<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Release process

Skill Workflow separates release **process evidence**, release **preflight authority**, and release **publication**.

The current stable release is `v2.1.0`, published from its exact accepted release commit. `v2.0.0` remains historical immutable release evidence. The rules below describe the governed publication boundary: no new stable tag or GitHub release is authoritative until its exact publication candidate passes strict preflight and the governed publication transaction completes.

## Release candidate inputs

Every preflight is bound to:

- one exact candidate commit SHA;
- one semantic version tag in `vMAJOR.MINOR.PATCH` form, optionally with a prerelease suffix;
- one clean worktree;
- one governance report produced for that exact SHA.

Cache state and mutable upstream state are never release authority.

## Two preflight modes

The manual `Release Preflight` workflow exposes two deliberately different modes.

### Evidence-only dry run

`evidence_only=true` exists to prove that the release process is repeatable before final acceptance is complete. It:

1. checks out the exact requested candidate;
2. requests `scripts/governance_engine.py --mode verify` for that SHA;
3. permits the governance engine to escalate execution breadth to `effective_mode=finalize` when impact is broad or unknown, while requiring `requested_mode=verify` and `final_acceptance_authority=false`;
4. runs `scripts/release_preflight.py --evidence-only`;
5. allows explicit `NOT_PROVEN` acceptance items while rejecting explicit `FAIL` or invalid statuses;
6. rejects stable versions;
7. emits JSON evidence with `publication_authority=false`.

A PASS in evidence-only mode is **not** permission to tag, publish, or claim final acceptance. Its only authority is to prove the mechanics and fail-closed behavior of the prerelease process. Escalating validation breadth does not upgrade authority.

### Strict publication-ready preflight

`evidence_only=false` is the strict path. It:

1. requests `scripts/governance_engine.py --mode finalize` for the exact candidate;
2. requires `requested_mode=finalize`, `effective_mode=finalize`, and `final_acceptance_authority=true`;
3. requires every non-publication acceptance requirement to be `PASS`;
4. requires every truth gate to be `PASS` or `NOT_APPLICABLE`;
5. validates version syntax and tag non-existence;
6. for a stable version, requires the current phase to have an explicit stable-release contract in `scripts/release_preflight.py` and every prior SW2 phase to be complete;
7. allows only that active release phase's declared publication requirement to remain `NOT_PROVEN` during stable preflight, because creation of the exact versioned tag/release is the publication action being authorized.

The publication requirement is publication-pending, not waived. Any `FAIL`, any other `NOT_PROVEN` requirement, a missing phase release requirement, an unauthorized stable-release phase, or any unproven truth gate blocks publication authority. After the exact tag/release is created, the publication requirement must be promoted from the resulting publication evidence.

Only a successful strict preflight may emit `publication_authority=true`. The preflight itself is still read-only and does not create a Git tag or GitHub release.

## Deterministic package dry-run (SW2-25)

Before approving a future publication, maintainers can run the independent [Reproducible release bundle](release-bundle.md) process against an exact clean commit. It generates a content-addressed product ZIP and detached per-file SHA-256 manifest, re-verifies the complete artifact offline, and compares Windows/Ubuntu bytes. This is a **non-publishing** prerequisite for artifact reproducibility, not an alternative to the strict preflight. Both its manifest and CI dry-run enforce `publication_authority=false`. An unsigned manifest does not authenticate the publisher.

## Evidence artifacts

The workflow uploads the governance report and release-preflight JSON together. These artifacts bind the result to the requested candidate SHA and expose the requested/effective governance modes, whether the run was evidence-only or strict, whether the version was stable, the publication-requirement state, and whether publication authority was granted.

## Publication transaction

Publication is a separate governed action after strict preflight. The stable tag and GitHub release must both point to the exact tested publication commit. Release notes must identify that commit and the accepted compatibility/migration boundary. Publication must fail closed if the requested tag already exists or the repository HEAD no longer matches the accepted publication candidate.

After publication, verify that the tag target and GitHub release target both resolve to the preflight-authorized commit before promoting the active phase's publication requirement to PASS. A publication record that points anywhere else is not acceptable evidence.

## Release rollback

A stable release is immutable evidence. Never move or retarget an existing stable tag to a different commit.

If a published release is found defective:

1. Stop recommending or automating adoption of the defective version and record the affected tag, exact commit, and failure evidence.
2. Consumers should pin the last known-good release or accepted commit while the repair is prepared.
3. Repair forward on a new branch and run the full governance, migration, compatibility, and strict release-preflight gates again.
4. Publish a new semantic patch release from the newly tested commit. Do not overwrite release assets or silently replace the original tag target.
5. Update the defective release notes to point users to the corrective release when GitHub metadata can be changed without altering the tag target.

Deleting or recreating a stable tag is not the normal rollback path. If publication itself was incomplete before any supported release was communicated, treat cleanup as an incident and preserve an auditable record of what was removed and why.

Project schema rollback is separate from release rollback; follow the [schema and toolchain versioning](versioning.md#rollback-after-migration) procedure for migrated consumer repositories.

## Failure handling

Any provenance mismatch, dirty worktree, invalid version, reused tag, invalid governance report, explicit failed acceptance item, or authority-boundary violation fails closed. Strict mode additionally rejects incomplete non-publication requirements or truth gates. Repair the underlying evidence and rerun from a fresh exact candidate.
