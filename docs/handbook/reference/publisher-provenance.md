<!-- SOURCE-AUTHORED PUBLIC DESIGN NOTE; SW2-26 BEFORE/RED, NOT ACCEPTED -->

# Trusted publisher provenance (SW2-26 design boundary)

**Status:** IN PROGRESS; no authenticated publisher claim or permission to publish.

## Problem and trust boundary

The SW2-25 detached SHA-256 manifest establishes package integrity relative to a *supplied* manifest. It cannot authenticate a publisher, a Git source commit, or a coordinated replacement of both artifacts. The new trust policy MUST be supplied independently of attacker-controlled bundle/manifest data.

## Proposed minimal implementation

1. Retain the exact-source clean Git-blob product build, deterministic ZIP bytes, detached manifest and offline SHA-256 verifier unchanged as independently tested source-integrity checks.
2. On an explicitly triggered GitHub Actions run, generate in-toto/SLSA provenance for **both** ZIP and JSON manifest using GitHub OIDC and Sigstore (native `actions/attest`). Limit `id-token: write` and `attestations: write` permissions to the attestation job only. Do not give it `contents: write` or release permissions.
3. Require a verifier backed by the actual `gh attestation verify` cryptographic check, not ad hoc JSON or a caller-provided `publisher_authenticated` boolean. Verify expected repository, trusted signer workflow, *exact* source SHA, artifact digest, and supplied trusted root for offline use. Verify both subjects independently, in addition to SW2-25 manifest content checks.
4. Treat signed provenance as identification of the executing workflow and source claim, **not** Owner release approval or a guarantee the source/build is safe. Do not interpret self-asserted predicate fields as signer-controlled certificate identity.
5. Keep `publication_authority=false`; do not automatically create stable tags, GitHub Releases or publish packages. Archive CI attestation evidence only.

## Adversarial cases

Refuse unsigned self-assertion, wrong signer, wrong repository, wrong source Git SHA, modified ZIP, changed manifest, missing/truncated signature or trust material, mismatched archive-manifest pair, replay against a separately pinned version or SHA, and unknown verifier failures. A successful mocked command is insufficient to assert cryptographic acceptance in final evidence.

## Limitations

Offline verification depends on a trust root obtained out-of-band. A stale trusted root cannot establish the latest revocation state. A cryptographically valid workflow attestation is not proof of safe code, Owner approval, or verified release publication. Source-to-binary assertions depend on the trusted builder and independently checked reproducible packaging.

## Evidence requirement

No SW2-26 PASS until GitHub Actions supplies real exact-SHA signatures and independent verification, targeted hostile fixtures, Windows/Ubuntu regression, six permanent contexts on feature and postmerge main, source-derived sequence and docs, and a separate terminal closure.

Upstream guidance: https://docs.github.com/en/actions/concepts/security/artifact-attestations ; https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline ; https://cli.github.com/manual/gh_attestation_verify
