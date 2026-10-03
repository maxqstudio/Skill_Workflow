# Security Policy

## Supported code

Until a versioned stable release exists, security fixes target the current `main` branch. Historical commits and untagged development snapshots are not maintained as separate supported releases.

## Reporting a vulnerability

Do not publish exploitable details, credentials, tokens, private data, or a proof of concept in a public issue.

Use GitHub's private vulnerability-reporting or Security Advisory flow for this repository when that option is available. If the repository UI does not offer a private channel, open a public issue containing only a request to establish a private contact path; do not include sensitive technical details there.

Include, when safe to share privately:

- affected component and commit or version;
- impact and realistic attack preconditions;
- minimal reproduction information;
- whether secrets or user data may have been exposed;
- any known mitigation.

## Handling

Maintainers should reproduce the report, define the affected scope, repair the smallest correct surface, add regression coverage, and rerun governed acceptance before release.

Security fixes do not bypass Project Truth, exact-head provenance, or required regression gates.

## Disclosure

Coordinate public disclosure only after a fix or mitigation is available and the affected scope is understood. Do not expose third-party secrets or personal data in release notes or issue history.
