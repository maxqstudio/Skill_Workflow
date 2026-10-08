#!/usr/bin/env python3
"""SW2-26 adversarial contract: mocking gh cannot prove cryptographic signatures."""
from __future__ import annotations
import json
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch
import publisher_provenance as prov
import release_bundle


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def fixture(root):
    root.mkdir()
    git(root, "init")
    git(root, "config", "user.name", "SW2-26 Test")
    git(root, "config", "user.email", "test@example.invalid")
    for name, data in {
        "SKILL.md": "# Skill\n", "README.md": "# README\n", "LICENSE": "MIT\n",
        "scripts/core.py": "pass\n", "references/guide.md": "# Guide\n",
        "templates/basic.txt": "template\n", "docs/handbook/index.md": "# Handbook\n",
    }.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8", newline="\n")
    git(root, "add", "-A")
    git(root, "commit", "-m", "fixture")
    return git(root, "rev-parse", "HEAD")


def rejects(gate, callback):
    try:
        callback()
    except prov.ProvenanceError as exc:
        assert str(exc).startswith(gate), (gate, str(exc))
    else:
        raise AssertionError("FALSE_ACCEPT:" + gate)


def fake_verification(path):
    return json.dumps([{"verificationResult": {
        "signature": {"certificate": {"subjectAlternativeName": "MOCKED"}},
        "statement": {"predicateType": prov.PREDICATE, "subject": [
            {"name": path.name, "digest": {"sha256": prov.digest(path)}}
        ]},
    }}])


def main():
    with tempfile.TemporaryDirectory(prefix="sw2-26-tests-") as tmp:
        td = Path(tmp)
        sha = fixture(td / "repo")
        bundle, manifest = td/"product.zip", td/"manifest.json"
        attestation, trusted = td/"attestation.json", td/"trusted_root.jsonl"
        release_bundle.build(td/"repo", sha, bundle, manifest)
        unsigned = release_bundle.verify(bundle, manifest)
        assert unsigned["publisher_authenticated"] is False
        assert unsigned["publication_authority"] is False
        print("PROVENANCE_SW2_25_UNSIGNED_INTEGRITY_NOT_AUTHENTICATED=PASS")
        ref = "refs/heads/work/sw2-26-trusted-publisher-attestation"

        def verify(expected=sha, expected_ref=ref):
            return prov.verify(bundle, manifest, attestation, trusted, expected, expected_ref)

        rejects("PROVENANCE_ATTESTATION_BUNDLE_MISSING", verify)
        attestation.write_text("{}\n", encoding="utf-8")
        rejects("PROVENANCE_INDEPENDENT_TRUST_ROOT_MISSING", verify)
        trusted.write_text("{}\n", encoding="utf-8")
        rejects("PROVENANCE_EXPECTED_SHA_INVALID", lambda: verify("main"))
        rejects("PROVENANCE_EXPECTED_REF_INVALID", lambda: verify(sha, "refs/tags/v2.1.0"))
        rejects("PROVENANCE_SOURCE_SHA_MISMATCH", lambda: verify("0"*40))
        print("PROVENANCE_ABSENT_ATTESTATION_AND_WRONG_PIN_REJECTED=PASS")

        observed = []
        def mocked_gh(cmd, **kwargs):
            assert cmd[:3] == ["gh", "attestation", "verify"]
            for flag, value in {
                "--repo": prov.REPO, "--signer-workflow": prov.SIGNER,
                "--source-digest": sha, "--source-ref": ref,
                "--cert-oidc-issuer": prov.OIDC_ISSUER,
                "--predicate-type": prov.PREDICATE,
                "--bundle": str(attestation), "--custom-trusted-root": str(trusted),
            }.items():
                assert cmd[cmd.index(flag)+1] == value, (flag, cmd)
            artifact = Path(cmd[3])
            observed.append(artifact)
            return subprocess.CompletedProcess(cmd, 0, fake_verification(artifact), "")
        with patch.object(prov.subprocess, "run", side_effect=mocked_gh):
            simulated = verify()
        assert observed == [bundle, manifest]
        assert simulated["publication_authority"] is False
        assert simulated["offline_trusted_root_freshness"] == "NOT_PROVEN"
        print("PROVENANCE_CLI_SIGNER_SOURCE_AND_BOTH_SUBJECTS=PASS (MOCKED ONLY)")

        with patch.object(prov.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "invalid signature")):
            rejects("PROVENANCE_SIGNATURE_OR_SIGNER_REJECTED", verify)
        with patch.object(prov.subprocess, "run", side_effect=FileNotFoundError):
            rejects("PROVENANCE_CRYPTOGRAPHIC_VERIFIER_UNAVAILABLE", verify)
        with patch.object(prov.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "{}", "")):
            rejects("PROVENANCE_VERIFIED_OUTPUT_INVALID", verify)
        with patch.object(prov.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "[]", "")):
            rejects("PROVENANCE_VERIFIED_OUTPUT_INVALID", verify)
        with patch.object(prov.subprocess, "run", side_effect=lambda cmd, **k: subprocess.CompletedProcess(cmd, 0, fake_verification(bundle), "")):
            rejects("PROVENANCE_VERIFIED_SUBJECT_MISMATCH", verify)
        print("PROVENANCE_MOCKED_SIGNATURE_AND_SUBJECT_FAILURES_REJECTED=PASS")

        original = bundle.read_bytes()
        bundle.write_bytes(original+b"tampered")
        rejects("PROVENANCE_UNTRUSTED_BUNDLE_INTEGRITY", verify)
        bundle.write_bytes(original)
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["source_git_sha"] = "0"*40
        manifest.write_text(json.dumps(data)+"\n", encoding="utf-8")
        rejects("PROVENANCE_SOURCE_SHA_MISMATCH", verify)
        print("PROVENANCE_ZIP_AND_MANIFEST_TAMPER_REJECTED=PASS")
        print("PROVENANCE_ADVERSARIAL_CONTRACT=PASS (REAL_SIGNATURE_NOT_PROVEN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
