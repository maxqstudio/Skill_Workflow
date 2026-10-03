<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Release process

Skill Workflow separates release **preflight** from release **publication**.

No stable V2 release is published during SW2-07. Stable release/tag creation remains SW2-09 scope.

## Release candidate inputs

A release preflight is bound to:

- one exact candidate commit SHA;
- one semantic version tag in `vMAJOR.MINOR.PATCH` form, optionally with a prerelease suffix;
- one successful `scripts/governance_engine.py --mode finalize` report for that exact SHA;
- a clean worktree.

Cache state and mutable upstream state are never release authority.

## Automated preflight

The manual `Release Preflight` workflow checks out the exact requested candidate, runs finalize governance, and then runs `scripts/release_preflight.py`.

The preflight validates:

1. exact Git HEAD provenance;
2. semantic version syntax and tag non-existence;
3. clean repository state;
4. complete current acceptance requirements and truth gates;
5. a successful finalize report with `final_acceptance_authority=true`;
6. for a stable version, SW2-09 must be the current release phase and every prior SW2 phase must already be complete.

The script is read-only except for the explicitly requested JSON report path. It never creates a tag or GitHub release.

## Publication boundary

After preflight passes, publication is still a separate governed action. SW2-09 must define and prove the exact tag/release transaction, rollback guidance, release notes, and post-release verification before a stable V2 release is created.

## Failure handling

Any provenance mismatch, dirty worktree, incomplete governance requirement, failing truth gate, reused tag, or invalid finalize report fails closed. Repair the underlying evidence and rerun from a fresh exact candidate.
