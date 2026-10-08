<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Reproducible release bundle (SW2-25)

The **release bundle** is an optional, deterministic snapshot of product source from one exact clean Git commit. The normal `npx skills add maxqstudio/Skill_Workflow` installation workflow remains unchanged.

## Inputs and output

The producer script is `.github/scripts/release_bundle.py`, which requires Python 3 and Git for building. The offline **verify** subcommand requires only Python and the downloaded ZIP plus its paired manifest.

```bash
python .github/scripts/release_bundle.py build \
  --root . --expected-head <EXACT_40_CHARACTER_GIT_SHA> \
  --bundle /tmp/skill-workflow.zip \
  --manifest /tmp/skill-workflow-manifest.json

python .github/scripts/release_bundle.py verify \
  --bundle /tmp/skill-workflow.zip \
  --manifest /tmp/skill-workflow-manifest.json
```

The output paths must be **outside** the source repository. A dirty checkout, incorrect SHA, unsafe entry, missing mandatory product surface or modified archive is a failure. The script never creates tags, GitHub releases, releases notes, or package repository uploads.

The product-only allowlist includes the root `SKILL.md`, `LICENSE`, `README.md`, plus tracked `scripts/`, `references/`, `templates/`, and `docs/handbook/`. It excludes the private/unnecessary execution and governance surfaces `.git/`, `.github/`, `.workflow/`, generated phase reports, benchmarks, local settings and arbitrary tracked files. Unsafe paths, common secret filename patterns, symlinks, unsupported file modes, and case-insensitive filename collisions fail closed if they occur inside the allowlist. The denylist is a defense-in-depth safeguard, **not** an assurance that arbitrary credentials embedded in innocently named source files have been automatically identified.

Git **blob** bytes, not OS-normalized checkout bytes, are packaging authority; the source checkout must still be clean. ZIP entry ordering, metadata, timestamps, permissions and stored payload bytes are canonical. The package is uncompressed by design to avoid zlib differences between operating systems. The JSON manifest contains file paths, modes, sizes and SHA-256 digests; canonical bundle digest; toolchain-content digest; and the producing exact Git SHA.

## Offline verification and provenance limits

The ZIP and manifest are independently supplied to `verify`. A PASS means the supplied archive is **byte-consistent with that manifest**, including every payload SHA-256, archive SHA-256, exact file set and canonical metadata. Reordering, forged paths, duplicates, corrupt payloads, extra files, changed modes or missing files are rejected. The verifier needs no network, Git repository, external source checker or key.

**SHA-256 is not a signature.** An adversary who can replace *both* ZIP and manifest can generate new consistent hashes. The manifest's producing Git SHA is independently verified **only during build**; without another trusted source, offline verification reports Git identity as `NOT_PROVEN` and `publisher_authenticated=false`. A user who needs publication authentication must validate the digest against a separately authenticated upstream source. `publication_authority=false` is mandatory in both build and verify reports.

## Cross-platform and release policy

The <Link>Release Bundle Dry Run</Link> GitHub Actions workflow can be started manually with one immutable source SHA. Its Ubuntu and Windows jobs run the negative-path regression and build the same snapshot; a comparison job requires the **entire ZIP and manifest bytes to match exactly** before reporting cross-OS PASS. All artifacts are uploaded as ordinary CI evidence, **not** as GitHub Release assets. The workflow has only `contents: read`, no package publishing or release-tag authority.

The existing six Governance CI permanent contexts remain mandatory. Each Windows and Ubuntu selftest job also runs real bundle build, detached verification and adversarial tests. SW2-25 by itself **does not authorize v2.2.0, another release, or a mutable stable tag**. Stable publication requires a separately approved release phase, exact preflight and signed/attested provenance where authentication is required. The stable public product remains `v2.1.0` until an explicit future release contract is accepted.
