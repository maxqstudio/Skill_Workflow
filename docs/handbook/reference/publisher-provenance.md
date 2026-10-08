<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Trusted publisher provenance (SW2-26 design boundary)

**Status:** IN PROGRESS; not accepted and no permission to publish. A bounded GitHub Actions OIDC/Sigstore smoke run successfully signed and verified both artifacts at exact candidate `fe8cf3754a477b3ac97ddbd00cf891bad93c1cf3` (run [37726441523](https://github.com/maxqstudio/Skill_Workflow/actions/runs/37726441523)). This evidence is not final helper-free acceptance.

## Problem and trust boundary

The SW2-25 detached SHA-256 manifest establishes package integrity relative to a *supplied* manifest. It cannot authenticate a publisher, a Git source commit, or a coordinated replacement of both artifacts. The new trust policy MUST be supplied independently of attacker-controlled bundle/manifest data.

## Proposed minimal implementation

1. Retain the exact-source clean Git-blob product build, deterministic ZIP bytes, detached manifest and offline SHA-256 verifier unchanged as independently tested source-integrity checks.
2. On an explicitly triggered GitHub Actions run, generate in-toto/SLSA provenance for **both** ZIP and JSON manifest using GitHub OIDC and Sigstore (native `actions/attest`). Limit `id-token: write` and `attestations: write` permissions to the attestation job only. Do not give it `contents: write` or release permissions.
3. Require a verifier backed by the actual `gh attestation verify` cryptographic check, not ad hoc JSON or a caller-provided `publisher_authenticated` boolean. The verifier requires `--expected-root-sha256` from a separate trusted policy/channel and rejects missing or mismatched root digest before asking GitHub CLI to validate attestations. Verify expected repository, trusted signer workflow, *exact* source SHA, artifact digest, and supplied trusted root for offline use. Verify both subjects independently, in addition to SW2-25 manifest content checks.
4. Treat signed provenance as identification of the executing workflow and source claim, **not** Owner release approval or a guarantee the source/build is safe. Do not interpret self-asserted predicate fields as signer-controlled certificate identity.
5. Keep `publication_authority=false`; do not automatically create stable tags, GitHub Releases or publish packages. Archive CI attestation evidence only.

## Adversarial cases

Refuse unsigned self-assertion, wrong signer, wrong repository, wrong source Git SHA, modified ZIP, changed manifest, missing/truncated signature or trust material, mismatched archive-manifest pair, replay against a separately pinned version or SHA, and unknown verifier failures. A successful mocked command is insufficient to assert cryptographic acceptance in final evidence.

## Limitations

Offline verification depends on a trust root obtained out-of-band. A stale trusted root cannot establish the latest revocation state. A cryptographically valid workflow attestation is not proof of safe code, Owner approval, or verified release publication. Source-to-binary assertions depend on the trusted builder and independently checked reproducible packaging.

## Evidence requirement

No SW2-26 PASS until GitHub Actions supplies real exact-SHA signatures and independent verification, targeted hostile fixtures, Windows/Ubuntu regression, six permanent contexts on feature and postmerge main, source-derived sequence and docs, and a separate terminal closure.

Upstream guidance: https://docs.github.com/en/actions/concepts/security/artifact-attestations ; https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline ; https://cli.github.com/manual/gh_attestation_verify

## Verified evidence versus open acceptance

- The completed smoke run verified a signed ZIP and independently signed detached manifest against exact SHA/ref, GitHub issuer, repository and signer workflow; its machine report retained `publication_authority=false` and `offline_trusted_root_freshness=NOT_PROVEN`.
- Mocked negative tests prove only code-path expectations; live signer mismatch and trust-chain negative tests must be evidenced by GitHub CI, and source-generated Project Truth must remain synchronized.
- `gh attestation verify --bundle ... --custom-trusted-root ...` supports detached offline verification after trusted root material has been obtained independently. It does **not** prove latest root revocation or the safety of the workflow's source.

## Live adversarial evidence

At exact SHA `f87586fa784a22614217121c14519637df4155dd`, [GitHub Actions run 37783624068](https://github.com/maxqstudio/Skill_Workflow/actions/runs/37783624068) generated a signed ZIP+manifest pair and independently verified both subjects. The real verifier rejected four signed negative cases: incorrect signer workflow, source ref, source SHA, and damaged attestation bundle. The current acceptance phase remains unfinished; no isolated network-offline simulation, freshness guarantee, six-context helper-free acceptance, postmerge acceptance, or terminal closure is claimed.

## Trusted-root bootstrap and limitations

For production/offline consumers, the expected SHA-256 of `trusted_root.jsonl` is an independently trusted policy input, not a digest read from the same downloaded package or unsigned manifest. The CI smoke test obtains a fresh Sigstore root using the official GitHub CLI and records its digest in the same trusted GitHub runner to exercise the pinning mechanism. That smoke test does **not** establish an independently distributed Owner trust anchor. Offline verification cannot determine whether the root has since been revoked; a previously pinned root is only as trustworthy as its initial acquisition and update process.

## Pinned-root verifier proof

GitHub Actions [run 37786698990](https://github.com/maxqstudio/Skill_Workflow/actions/runs/37786698990) exercised the new mandatory expected trusted-root SHA-256 input and verified both signed subjects, including with all HTTP(S) proxies pointed at a blocked local endpoint. Four cryptographic negative paths remained rejected. CI derives a root digest from the root fetched through official GitHub CLI, which proves verifier plumbing rather than independent Owner distribution. Production operators must obtain and pin their expected root digest through a separate trusted channel; offline checks still cannot establish subsequent revocation freshness.

## Feature acceptance evidence

At helper-free feature SHA `b10d3b8e47c96cf6025403ca7ce2542aa1a7cde5`, [permanent Governance CI run 37787819701](https://github.com/maxqstudio/Skill_Workflow/actions/runs/37787819701) passed all six contexts. This is R5 implementation evidence, **not** proof that the subsequent authority/projection synchronization commit has passed or that SW2-26 has completed postmerge or terminal closure. R6 remains pending until the separate transactions pass on their respective exact main SHAs.
