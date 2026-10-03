<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Repository governance

Skill Workflow treats GitHub repository configuration as runtime governance, not documentation.

## Declared default-branch policy

For this repository, the intended default-branch policy is:

- changes reach `main` through pull requests;
- direct deletion and non-fast-forward updates are blocked;
- squash is the governed merge method;
- the permanent acceptance checks are required before merge;
- repository configuration is audited independently of workflow files.

The permanent checks currently expected by SW2 governance are:

- `Self Governance (ubuntu-latest)`;
- `Governance Selftest (ubuntu-latest)`;
- `Governance Selftest (windows-latest)`;
- `SW2 Sequence Evidence (ubuntu-latest)`;
- `Governance Engine Performance (ubuntu-latest)`;
- `Consumer Engine Performance (max-grounding)`.

## Evidence boundary

A workflow file proves only that a check can run. It does not prove GitHub requires that check before merge.

`scripts/validate_github_ruleset.py` validates an exported GitHub ruleset payload against the declared policy. The manual `SW2 Ruleset Audit` workflow fetches the live repository ruleset and applies the same validator.

If the live ruleset lacks required status checks, SW2-07 merge/ruleset enforcement remains `NOT_PROVEN` even when all CI happens to be green.

## Owner and administrator changes

Changing repository rules is an administrative action. Record the exact live configuration used as acceptance evidence and rerun the audit after any ruleset modification.
