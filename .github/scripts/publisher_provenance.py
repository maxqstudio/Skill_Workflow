#!/usr/bin/env python3
"""Trusted publisher verification: never trust unsigned manifest identity."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import release_bundle

REPO = "maxqstudio/Skill_Workflow"
SIGNER = "maxqstudio/Skill_Workflow/.github/workflows/trusted-bundle-attestation.yml"
PREDICATE = "https://slsa.dev/provenance/v1"
OIDC_ISSUER = "https://token.actions.githubusercontent.com"
SHA = re.compile(r"[0-9a-f]{40}\Z")
REF = re.compile(r"refs/heads/[A-Za-z0-9][A-Za-z0-9/_.-]*\Z")


class ProvenanceError(Exception):
    pass


def fail(code):
    raise ProvenanceError(code)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_subject(artifact, attestation, trusted_root, expected_sha, expected_ref):
    cmd = [
        "gh", "attestation", "verify", str(artifact),
        "--repo", REPO, "--signer-workflow", SIGNER,
        "--source-digest", expected_sha, "--source-ref", expected_ref,
        "--cert-oidc-issuer", OIDC_ISSUER, "--deny-self-hosted-runners",
        "--predicate-type", PREDICATE, "--bundle", str(attestation),
        "--custom-trusted-root", str(trusted_root), "--format", "json",
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              check=False, text=True, timeout=90)
    except (OSError, subprocess.TimeoutExpired):
        fail("PROVENANCE_CRYPTOGRAPHIC_VERIFIER_UNAVAILABLE")
    if proc.returncode != 0:
        fail("PROVENANCE_SIGNATURE_OR_SIGNER_REJECTED")
    try:
        results = json.loads(proc.stdout)
    except (ValueError, UnicodeError):
        fail("PROVENANCE_VERIFIED_OUTPUT_INVALID")
    if not isinstance(results, list) or not results:
        fail("PROVENANCE_VERIFIED_OUTPUT_INVALID")
    matches = 0
    for item in results:
        if not isinstance(item, dict) or not isinstance(item.get("verificationResult"), dict):
            fail("PROVENANCE_VERIFIED_OUTPUT_INVALID")
        result = item["verificationResult"]
        signature = result.get("signature")
        statement = result.get("statement")
        if not isinstance(signature, dict) or not signature.get("certificate"):
            fail("PROVENANCE_VERIFIED_CERTIFICATE_MISSING")
        if not isinstance(statement, dict) or statement.get("predicateType") != PREDICATE:
            fail("PROVENANCE_VERIFIED_PREDICATE_INVALID")
        subjects = statement.get("subject")
        if not isinstance(subjects, list):
            fail("PROVENANCE_VERIFIED_SUBJECT_INVALID")
        for subject in subjects:
            if not isinstance(subject, dict) or not isinstance(subject.get("digest"), dict):
                fail("PROVENANCE_VERIFIED_SUBJECT_INVALID")
            if subject.get("name") == artifact.name and subject["digest"].get("sha256") == digest(artifact):
                matches += 1
    if matches == 0:
        fail("PROVENANCE_VERIFIED_SUBJECT_MISMATCH")


def verify(bundle, manifest, attestation, trusted_root, expected_sha, expected_ref, expected_root_sha256):
    if not SHA.fullmatch(expected_sha):
        fail("PROVENANCE_EXPECTED_SHA_INVALID")
    if not REF.fullmatch(expected_ref) or ".." in expected_ref or "//" in expected_ref:
        fail("PROVENANCE_EXPECTED_REF_INVALID")
    if not attestation.is_file() or not attestation.stat().st_size:
        fail("PROVENANCE_ATTESTATION_BUNDLE_MISSING")
    if not trusted_root.is_file() or not trusted_root.stat().st_size:
        fail("PROVENANCE_INDEPENDENT_TRUST_ROOT_MISSING")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_root_sha256):
        fail("PROVENANCE_TRUST_ROOT_PIN_INVALID")
    if digest(trusted_root) != expected_root_sha256:
        fail("PROVENANCE_TRUST_ROOT_PIN_MISMATCH")
    try:
        integrity = release_bundle.verify(bundle, manifest)
    except (release_bundle.BundleError, OSError, ValueError) as exc:
        fail("PROVENANCE_UNTRUSTED_BUNDLE_INTEGRITY:" + str(exc))
    if integrity["source_git_sha_claimed"] != expected_sha:
        fail("PROVENANCE_SOURCE_SHA_MISMATCH")
    # SHA/ref are supplied independently of the unsigned manifest and predicate.
    for artifact in (bundle, manifest):
        verify_subject(artifact, attestation, trusted_root, expected_sha, expected_ref)
    return {
        "result": "PASS", "publisher_authenticated": True, "publication_authority": False,
        "repository": REPO, "signer_workflow": SIGNER,
        "source_sha": expected_sha, "source_ref": expected_ref,
        "archive_sha256": digest(bundle), "manifest_sha256": digest(manifest),
        "offline_trusted_root_freshness": "NOT_PROVEN",
        "trusted_root_sha256": expected_root_sha256, "first_failed_gate": "",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for k in ("bundle", "manifest", "attestation", "trusted-root", "expected-sha", "expected-ref", "expected-root-sha256"):
        ap.add_argument("--"+k, required=True)
    a = ap.parse_args()
    try:
        result = verify(Path(a.bundle), Path(a.manifest), Path(a.attestation),
                        Path(a.trusted_root), a.expected_sha, a.expected_ref, a.expected_root_sha256)
    except ProvenanceError as exc:
        print("PROVENANCE_RESULT=FAIL")
        print("FIRST_FAILED_GATE="+str(exc))
        return 1
    print("PROVENANCE_VERIFY=PASS")
    print("PROVENANCE_REPORT_JSON="+json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
