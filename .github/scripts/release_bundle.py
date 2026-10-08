#!/usr/bin/env python3
"""Deterministic release bundle dry-run and independently consumable integrity report.

Build uses an exact clean git HEAD and an explicit product-only include contract.
Verify needs no git repo, Python packages, network, signing key or release API.
A checksum manifest is content integrity evidence, NOT a cryptographic identity
signature or authority to publish.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

SCHEMA = 1
ALGORITHM = "sha256"
REQUIRED = {"SKILL.md", "LICENSE", "README.md"}
INCLUDED_PREFIXES = ("scripts/", "references/", "templates/", "docs/handbook/")
SOURCE_ONLY = {
    "initialize_project_truth.py", "migrate_governance_v1.py",
    "selftest_project_truth_compiler.py", "upgrade_governance_toolchain.py",
}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
COMPRESSION = zipfile.ZIP_STORED  # Deliberately avoid OS/zlib-dependent DEFLATE byte streams.
WINDOWS_RESERVED = {"CON","PRN","AUX","NUL",*[f"COM{i}" for i in range(1,10)],
                    *[f"LPT{i}" for i in range(1,10)]}
SHA_RE = re.compile(r"[0-9a-f]{40}", re.ASCII)
HEX_RE = re.compile(r"[0-9a-f]{64}", re.ASCII)


class BundleError(Exception):
    pass


def fail(code: str) -> None:
    raise BundleError(code)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git(root: Path, *args: str) -> bytes:
    p = subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
    if p.returncode:
        fail("GIT_COMMAND_FAILED:" + args[0])
    return p.stdout


def checked_head(root: Path, expected_head: str) -> None:
    if not SHA_RE.fullmatch(expected_head):
        fail("EXPECTED_HEAD_NOT_EXACT_SHA")
    if git(root,"rev-parse","HEAD").decode().strip()!=expected_head:
        fail("BUNDLE_SOURCE_HEAD_MISMATCH")
    if git(root,"status","--porcelain","--untracked-files=all").strip():
        fail("BUNDLE_SOURCE_DIRTY")


def include_path(name: str) -> bool:
    return name in REQUIRED or any(name.startswith(prefix) for prefix in INCLUDED_PREFIXES)


def validate_path(name: str) -> None:
    if not name or name.startswith("/") or "\\" in name or ":" in name or "\0" in name:
        fail("BUNDLE_UNSAFE_PATH")
    parts = name.split("/")
    if any(part in ("",".","..") or part.endswith((".", " "))
           or any(ord(c)<32 for c in part) for part in parts):
        fail("BUNDLE_UNSAFE_PATH")
    for part in parts:
        if part.split(".",1)[0].upper() in WINDOWS_RESERVED:
            fail("BUNDLE_WINDOWS_UNSAFE_NAME")
    leaf = parts[-1].lower()
    if leaf in {"id_rsa","id_ed25519","credentials.json","service-account.json",
                "secrets.json","secrets.yaml","secrets.yml",".env",".npmrc",".pypirc"}:
        fail("BUNDLE_SECRET_FILENAME")
    if (leaf.startswith(".env.") or leaf.endswith((".pem",".p12",".pfx",".key"))
            or leaf.startswith("secret_") or leaf.endswith("_private_key")):
        fail("BUNDLE_SECRET_FILENAME")


def source_tree(root: Path) -> list[tuple[str,str,bytes]]:
    paths = []
    casefold: set[str] = set()
    found: set[str] = set()
    payload = git(root,"ls-tree","-r","-z","--full-tree","HEAD")
    for item in payload.split(b"\0"):
        if not item:
            continue
        try:
            header,name_bytes=item.split(b"\t",1)
            mode,kind,oid=header.decode("ascii").split(" ")
            name=name_bytes.decode("utf-8","strict")
        except (ValueError,UnicodeDecodeError):
            fail("BUNDLE_INVALID_GIT_TREE_RECORD")
        if not include_path(name):
            continue
        validate_path(name)
        folded=name.casefold()
        if folded in casefold:
            fail("BUNDLE_CASE_COLLISION")
        casefold.add(folded)
        if kind!="blob" or mode not in {"100644","100755"}:
            fail("BUNDLE_UNSAFE_GIT_MODE:"+name)
        blob=git(root,"cat-file","blob",oid)
        if len(blob)>MAX_FILE_BYTES:
            fail("BUNDLE_FILE_TOO_LARGE:"+name)
        current=(root/name)
        if not current.is_file() or current.is_symlink() or current.read_bytes()!=blob:
            fail("BUNDLE_WORKTREE_SOURCE_MISMATCH:"+name)
        paths.append((name,mode,blob))
        found.add(name)
    missing=REQUIRED-found
    if missing:
        fail("BUNDLE_REQUIRED_FILE_MISSING:"+",".join(sorted(missing)))
    if not any(name.startswith("scripts/") for name in found):
        fail("BUNDLE_REQUIRED_TOOLCHAIN_MISSING")
    if not any(name.startswith("references/") for name in found):
        fail("BUNDLE_REQUIRED_REFERENCES_MISSING")
    if not any(name.startswith("templates/") for name in found):
        fail("BUNDLE_REQUIRED_TEMPLATES_MISSING")
    paths.sort(key=lambda v:v[0])
    if sum(len(blob) for _,_,blob in paths)>MAX_ARCHIVE_BYTES:
        fail("BUNDLE_TOTAL_SIZE_EXCEEDED")
    return paths


def digest_manifest(files: dict[str,str]) -> str:
    encoded=json.dumps(files,sort_keys=True,separators=(",",":"),
                       ensure_ascii=False).encode("utf-8")
    return sha(encoded)


def toolchain_digest(entries: list[dict]) -> str:
    paths={entry["path"].split("/",1)[1]:entry["sha256"] for entry in entries
           if entry["path"].startswith("scripts/") and
           entry["path"].endswith(".py") and
           entry["path"].rsplit("/",1)[-1] not in SOURCE_ONLY}
    return digest_manifest(paths)


def write_zip(items: list[tuple[str,str,bytes]]) -> bytes:
    output=io.BytesIO()
    with zipfile.ZipFile(output,mode="w",compression=COMPRESSION,
                         compresslevel=9,allowZip64=False) as z:
        for name,mode,blob in items:
            info=zipfile.ZipInfo(name,ZIP_TIMESTAMP)
            info.create_system=3
            info.compress_type=COMPRESSION
            info.external_attr=((0o100755 if mode=="100755" else 0o100644)<<16)
            info.comment=b""
            info.extra=b""
            z.writestr(info,blob,compress_type=COMPRESSION,compresslevel=9)
    return output.getvalue()


def build(root: Path, expected_head: str, bundle_path: Path, manifest_path: Path) -> dict:
    root=root.resolve()
    checked_head(root,expected_head)
    bundle_path=bundle_path.resolve()
    manifest_path=manifest_path.resolve()
    if bundle_path==manifest_path or bundle_path.is_relative_to(root) or manifest_path.is_relative_to(root):
        fail("BUNDLE_OUTPUT_MUST_BE_EXTERNAL")
    items=source_tree(root)
    payload=write_zip(items)
    if len(payload)>MAX_ARCHIVE_BYTES:
        fail("BUNDLE_ARCHIVE_SIZE_EXCEEDED")
    entries=[{"path":name,"mode":mode,"size":len(blob),"sha256":sha(blob)}
             for name,mode,blob in items]
    manifest={
        "schema_version":SCHEMA,
        "format":"skill-workflow-source-zip-v1",
        "hash_algorithm":ALGORITHM,
        "source_git_sha":expected_head,
        "source_git_identity":"VERIFIED_DURING_BUILD_ONLY",
        "offline_source_git_identity":"NOT_PROVEN",
        "publication_authority":False,
        "release_tag":"NOT_PROVEN",
        "archive_sha256":sha(payload),
        "archive_size":len(payload),
        "consumer_toolchain_digest":toolchain_digest(entries),
        "content_digest":digest_manifest({x["path"]:x["sha256"] for x in entries}),
        "files":entries,
        "boundary":"Deterministic exact Git source snapshot and detached SHA-256 integrity. This document is unsigned, self-asserted offline and cannot authenticate publisher or authorize publication."
    }
    bundle_path.parent.mkdir(parents=True,exist_ok=True)
    manifest_path.parent.mkdir(parents=True,exist_ok=True)
    bundle_path.write_bytes(payload)
    manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",
                             encoding="utf-8",newline="\n")
    verify(bundle_path,manifest_path)
    checked_head(root,expected_head)
    return manifest


def verify(bundle_path: Path, manifest_path: Path) -> dict:
    if not bundle_path.is_file() or not manifest_path.is_file():
        fail("BUNDLE_OR_MANIFEST_MISSING")
    try:
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError,UnicodeError,ValueError):
        fail("BUNDLE_MANIFEST_INVALID_JSON")
    if not isinstance(manifest,dict) or manifest.get("schema_version")!=SCHEMA or (
        manifest.get("format")!="skill-workflow-source-zip-v1"
        or manifest.get("hash_algorithm")!=ALGORITHM
        or manifest.get("publication_authority") is not False
        or manifest.get("offline_source_git_identity")!="NOT_PROVEN"
        or manifest.get("source_git_identity")!="VERIFIED_DURING_BUILD_ONLY"
        or manifest.get("release_tag")!="NOT_PROVEN"
        or not SHA_RE.fullmatch(str(manifest.get("source_git_sha","")))
    ):
        fail("BUNDLE_MANIFEST_AUTHORITY_OR_SCHEMA_INVALID")
    payload=bundle_path.read_bytes()
    if len(payload)>MAX_ARCHIVE_BYTES or len(payload)!=manifest.get("archive_size"):
        fail("BUNDLE_ARCHIVE_SIZE_MISMATCH")
    if sha(payload)!=manifest.get("archive_sha256"):
        fail("BUNDLE_ARCHIVE_DIGEST_MISMATCH")
    entries=manifest.get("files")
    if not isinstance(entries,list) or not entries:
        fail("BUNDLE_MANIFEST_FILE_LIST_INVALID")
    seen=set()
    for entry in entries:
        if not isinstance(entry,dict) or set(entry)!={"path","mode","size","sha256"}:
            fail("BUNDLE_MANIFEST_FILE_RECORD_INVALID")
        name=entry["path"]
        if not isinstance(name,str):
            fail("BUNDLE_MANIFEST_PATH_INVALID")
        validate_path(name)
        if not include_path(name) or name.casefold() in seen:
            fail("BUNDLE_MANIFEST_UNEXPECTED_OR_DUPLICATE_FILE")
        seen.add(name.casefold())
        if entry["mode"] not in {"100644","100755"} or not isinstance(entry["size"],int) or (
            isinstance(entry["size"],bool) or entry["size"]<0 or entry["size"]>MAX_FILE_BYTES
        ) or not HEX_RE.fullmatch(str(entry["sha256"])):
            fail("BUNDLE_MANIFEST_FILE_METADATA_INVALID")
    names=[entry["path"] for entry in entries]
    if names!=sorted(names):
        fail("BUNDLE_MANIFEST_ORDER_INVALID")
    if not REQUIRED.issubset(set(names)):
        fail("BUNDLE_MANIFEST_REQUIRED_FILES_MISSING")
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as z:
            infos=z.infolist()
            if len(infos)!=len(entries) or [info.filename for info in infos]!=names:
                fail("BUNDLE_ARCHIVE_FILE_SET_MISMATCH")
            for info,entry in zip(infos,entries):
                if (info.is_dir() or info.date_time!=ZIP_TIMESTAMP
                    or info.create_system!=3
                    or info.compress_type!=COMPRESSION
                    or info.comment!=b"" or info.extra!=b""
                    or (info.external_attr>>16)!=(0o100755 if entry["mode"]=="100755" else 0o100644)
                    or info.file_size!=entry["size"]):
                    fail("BUNDLE_ARCHIVE_NONCANONICAL_METADATA:"+entry["path"])
                blob=z.read(info)
                if sha(blob)!=entry["sha256"]:
                    fail("BUNDLE_PAYLOAD_FILE_DIGEST_MISMATCH:"+entry["path"])
    except (zipfile.BadZipFile,EOFError,RuntimeError,OSError):
        fail("BUNDLE_CORRUPT_ZIP")
    if digest_manifest({x["path"]:x["sha256"] for x in entries})!=manifest.get("content_digest"):
        fail("BUNDLE_CONTENT_DIGEST_MISMATCH")
    if toolchain_digest(entries)!=manifest.get("consumer_toolchain_digest"):
        fail("BUNDLE_TOOLCHAIN_DIGEST_MISMATCH")
    return {"schema_version":1,"result":"PASS","archive_sha256":sha(payload),
            "file_count":len(entries),"source_git_sha_claimed":manifest["source_git_sha"],
            "publisher_authenticated":False,"publication_authority":False,
            "first_failed_gate":"","evidence_boundary":"Offline byte integrity only; source Git/publisher identity NOT_PROVEN without independent trusted evidence."}


def main()->int:
    parser=argparse.ArgumentParser()
    modes=parser.add_subparsers(dest="mode",required=True)
    b=modes.add_parser("build")
    b.add_argument("--root",required=True)
    b.add_argument("--expected-head",required=True)
    b.add_argument("--bundle",required=True)
    b.add_argument("--manifest",required=True)
    v=modes.add_parser("verify")
    v.add_argument("--bundle",required=True)
    v.add_argument("--manifest",required=True)
    args=parser.parse_args()
    try:
        if args.mode=="build":
            report=build(Path(args.root),args.expected_head,Path(args.bundle),Path(args.manifest))
            print("BUNDLE_BUILD=PASS")
            print("BUNDLE_DIGEST="+report["archive_sha256"])
        else:
            report=verify(Path(args.bundle),Path(args.manifest))
            print("BUNDLE_VERIFY=PASS")
        summary={k:report[k] for k in ("archive_sha256","source_git_sha","publication_authority","consumer_toolchain_digest","archive_size") if k in report}
        summary["file_count"]=len(report["files"]) if "files" in report else report.get("file_count",0)
        print("BUNDLE_REPORT_JSON="+json.dumps(summary,sort_keys=True,separators=(",",":")))
        return 0
    except (BundleError,ValueError) as exc:
        print("BUNDLE_RESULT=FAIL")
        print("FIRST_FAILED_GATE="+str(exc))
        return 1


if __name__=="__main__":
    raise SystemExit(main())
