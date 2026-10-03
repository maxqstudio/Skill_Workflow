<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Repository governance

Skill Workflow treats GitHub repository configuration and CI evidence as separate governance surfaces.

## Current repository policy

For this repository, the Owner has explicitly chosen not to require a GitHub ruleset. The permanent CI suite remains required acceptance evidence for governed phase closure, but GitHub is not claimed to automatically block merges when those checks fail.

The permanent SW2 acceptance checks are:

- `Self Governance (ubuntu-latest)`;
- `Governance Selftest (ubuntu-latest)`;
- `Governance Selftest (windows-latest)`;
- `SW2 Sequence Evidence (ubuntu-latest)`;
- `Governance Engine Performance (ubuntu-latest)`;
- `Consumer Engine Performance (max-grounding)`.

## Evidence boundary

A successful workflow proves that a check ran and passed on the tested candidate. It does not prove GitHub enforces that check before merge.

`scripts/validate_github_ruleset.py` and the manual `SW2 Ruleset Audit` workflow remain available for repositories that choose ruleset enforcement, but SW2-07 does not require this repository to configure one.

The accepted boundary is explicit: no repository ruleset is currently configured, and project documentation must not describe merge protection as automatic.

## Owner and administrator changes

If repository-level enforcement is added later, audit the exact live configuration and update Project Truth before claiming that enforcement exists.
