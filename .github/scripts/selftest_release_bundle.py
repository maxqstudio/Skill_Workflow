#!/usr/bin/env python3
"""Reproducible release dry-run and deliberately hostile offline bundle tests."""
from __future__ import annotations
import io
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
import release_bundle as bundle


def run(root:Path,*args:str)->str:
    r=subprocess.run(["git","-C",str(root),*args],text=True,
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True)
    return r.stdout.strip()


def put(root:Path,name:str,data:str)->None:
    p=root/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(data,encoding="utf-8",newline="\n")


def commit(root:Path,msg="fixture")->str:
    run(root,"add","-A")
    run(root,"commit","-m",msg)
    return run(root,"rev-parse","HEAD")


def raises(fragment:str,fn)->None:
    try:
        fn()
    except bundle.BundleError as e:
        if fragment not in str(e):
            raise AssertionError("unexpected gate "+str(e)+" expected "+fragment) from e
    else:
        raise AssertionError("FALSE_PASS:"+fragment)


def main()->int:
    with tempfile.TemporaryDirectory(prefix="sw2-25-release-") as td:
        root=Path(td)/"repo"
        root.mkdir()
        run(root,"init")
        run(root,"config","user.email","test@example.invalid")
        run(root,"config","user.name","SW2-25 Test")
        for name,text in {
            "SKILL.md":"# Example skill\n","README.md":"# Readme\n","LICENSE":"MIT\n",
            "scripts/core.py":"print('source')\n",
            "references/guide.md":"# Guide\n",
            "templates/project.txt":"template\n",
            "docs/handbook/adoption.md":"# Adoption\n",
            ".github/private-workflow.yml":"not distributed\n",
            ".env":"TRACKED_PRIVATE_NOT_TO_BE_PACKAGED\n",
        }.items():
            put(root,name,text)
        head=commit(root)
        first=Path(td)/"first.zip"
        second=Path(td)/"second.zip"
        manifest=Path(td)/"first.json"
        manifest2=Path(td)/"second.json"
        report=bundle.build(root,head,first,manifest)
        report2=bundle.build(root,head,second,manifest2)
        assert first.read_bytes()==second.read_bytes()
        assert manifest.read_bytes()==manifest2.read_bytes()
        assert report["archive_sha256"]==report2["archive_sha256"]
        assert report["source_git_sha"]==head
        assert report["publication_authority"] is False
        assert report["offline_source_git_identity"]=="NOT_PROVEN"
        assert bundle.verify(first,manifest)["result"]=="PASS"
        with zipfile.ZipFile(first) as z:
            assert ".env" not in z.namelist()
            assert not any(x.startswith(".github/") for x in z.namelist())
            assert "SKILL.md" in z.namelist() and "scripts/core.py" in z.namelist()
        print("BUNDLE_REPRODUCIBLE_IDENTICAL_BYTES=PASS")
        print("BUNDLE_EXCLUDE_TRACKED_PRIVATE_SURFACES=PASS")
        raises("EXPECTED_HEAD_NOT_EXACT_SHA",lambda:bundle.build(root,"main",second,manifest2))
        raises("BUNDLE_SOURCE_HEAD_MISMATCH",lambda:bundle.build(root,"0"*40,second,manifest2))
        put(root,"DIRTY.txt","dirty")
        raises("BUNDLE_SOURCE_DIRTY",lambda:bundle.build(root,head,second,manifest2))
        (root/"DIRTY.txt").unlink()
        raises("BUNDLE_OUTPUT_MUST_BE_EXTERNAL",lambda:bundle.build(root,head,root/"bundle.zip",manifest2))
        print("BUNDLE_EXACT_SHA_DIRTY_AND_OUTPUT_BOUNDARY=PASS")

        mutated=Path(td)/"tampered.zip"
        mutated.write_bytes(first.read_bytes()+b"x")
        raises("BUNDLE_ARCHIVE_SIZE_MISMATCH",lambda:bundle.verify(mutated,manifest))
        mutated.write_bytes(first.read_bytes()[:-10]+b"0000000000")
        raises("BUNDLE_ARCHIVE_DIGEST_MISMATCH",lambda:bundle.verify(mutated,manifest))
        print("BUNDLE_TAMPER_REJECTED=PASS")

        original=json.loads(manifest.read_text())
        candidate=Path(td)/"tampered-manifest.json"
        def expect_manipulation(fragment,change):
            data=json.loads(json.dumps(original))
            change(data)
            candidate.write_text(json.dumps(data),encoding="utf-8")
            raises(fragment,lambda:bundle.verify(first,candidate))
        expect_manipulation("BUNDLE_ARCHIVE_DIGEST_MISMATCH",lambda d:d.update(archive_sha256="0"*64))
        expect_manipulation("BUNDLE_MANIFEST_AUTHORITY_OR_SCHEMA_INVALID",lambda d:d.update(publication_authority=True))
        expect_manipulation("BUNDLE_MANIFEST_AUTHORITY_OR_SCHEMA_INVALID",lambda d:d.update(offline_source_git_identity="GIT+CONTENT"))
        expect_manipulation("BUNDLE_CONTENT_DIGEST_MISMATCH",lambda d:d.update(content_digest="0"*64))
        expect_manipulation("BUNDLE_TOOLCHAIN_DIGEST_MISMATCH",lambda d:d.update(consumer_toolchain_digest="0"*64))
        expect_manipulation("BUNDLE_MANIFEST_UNEXPECTED_OR_DUPLICATE_FILE",lambda d:d["files"].append(d["files"][-1].copy()))
        expect_manipulation("BUNDLE_UNSAFE_PATH",lambda d:d["files"][0].update(path="../escape.txt"))
        expect_manipulation("BUNDLE_MANIFEST_REQUIRED_FILES_MISSING",lambda d:d["files"].__setitem__(slice(None),[x for x in d["files"] if x["path"]!="LICENSE"]))
        print("BUNDLE_MANIFEST_AUTHORITY_PATH_AND_SWAP_REJECTED=PASS")

        put(root,"templates/id_rsa","fake")
        secret_head=commit(root,"tracked secret")
        raises("BUNDLE_SECRET_FILENAME",lambda:bundle.build(root,secret_head,second,manifest2))
        print("BUNDLE_SECRET_FILENAME_REJECTED=PASS")
        (root/"templates/id_rsa").unlink()
        fixed=commit(root,"remove secret")
        put(root,"references/path.pem","fake")
        other=commit(root,"forbidden credential type")
        raises("BUNDLE_SECRET_FILENAME",lambda:bundle.build(root,other,second,manifest2))
        (root/"references/path.pem").unlink()
        fixed=commit(root,"fix")
        with tempfile.TemporaryDirectory(prefix="sw2-25-checkout-") as clone_dir:
            clone=Path(clone_dir)/"clone"
            subprocess.run(["git","clone","--quiet",str(root),str(clone)],check=True)
            clone_head=run(clone,"rev-parse","HEAD")
            copied=Path(td)/"clone.zip"
            copied_manifest=Path(td)/"clone.json"
            bundle.build(clone,clone_head,copied,copied_manifest)
            bundle.build(root,fixed,second,manifest2)
            assert copied.read_bytes()==second.read_bytes()
            assert copied_manifest.read_bytes()==manifest2.read_bytes()
            print("BUNDLE_SECOND_CLEAN_CHECKOUT_EQUAL_BYTES=PASS")
        print("RESULT=PASS")
        return 0


if __name__=="__main__":
    raise SystemExit(main())
