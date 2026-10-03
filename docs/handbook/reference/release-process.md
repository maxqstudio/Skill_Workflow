<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Release process

Skill Workflow separates release **process evidence**, release **preflight authority**, and release **publication**.

No stable V2 release is published during SW2-07. Stable release/tag creation remains SW2-09 scope.

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
2. runs `scripts/governance_engine.py --mode verify` for that SHA;
3. runs `scripts/release_preflight.py --evidence-only`;
4. allows explicit `NOT_PROVEN` acceptance items while rejecting explicit `FAIL` or invalid statuses;
5. rejects stable versions;
6. emits JSON evidence with `publication_authority=false`.

A PASS in evidence-only mode is **not** permission to tag, publish, or claim final acceptance. Its only authority is to prove the mechanics and fail-closed behavior of the prerelease process.

### Strict publication-ready preflight

`evidence_only=false` is the strict path. It:

1. runs `scripts/governance_engine.py --mode finalize` for the exact candidate;
2. requires a successful finalize report with `final_acceptance_authority=true`;
3. requires every acceptance requirement to be `PASS`;
4. requires every truth gate to be `PASS` or `NOT_APPLICABLE`;
5. validates version syntax and tag non-existence;
6. for a stable version, requires SW2-09 to be current and every prior SW2 phase to be complete.

Only a successful strict preflight may emit `publication_authority=true`. The preflight itself is still read-only and does not create a Git tag or GitHub release.

## Evidence artifacts

The workflow uploads the governance report and release-preflight JSON together. These artifacts bind the result to the requested candidate SHA and expose whether the run was evidence-only or strict, whether the version was stable, and whether publication authority was granted.

## Publication boundary

Publication remains a separate governed action. SW2-09 must define and prove the exact tag/release transaction, rollback guidance, release notes, and post-release verification before a stable V2 release is created.

## Failure handling

Any provenance mismatch, dirty worktree, invalid version, reused tag, invalid governance report, explicit failed acceptance item, or authority-boundary violation fails closed. Strict mode additionally rejects incomplete requirements or truth gates. Repair the underlying evidence and rerun from a fresh exact candidate.
