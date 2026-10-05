from pathlib import Path

path = Path('scripts/validate_sequence_sessions.py')
text = path.read_text(encoding='utf-8')

old_build = '''        for rel in evidence_paths(root, session_path, data):
            path = root / rel
            if not path.is_file():
                raise ValueError(f"HISTORICAL_EVIDENCE_MISSING:{rel}")
            current = path.read_bytes()
            try:
                frozen = git_show_bytes(root, frozen_commit, rel)
            except subprocess.CalledProcessError as exc:
                raise ValueError(f"HISTORICAL_EVIDENCE_NOT_IN_FROZEN_COMMIT:{rel}") from exc
            current_sha = sha256_bytes(current)
            frozen_sha = sha256_bytes(frozen)
            if current_sha != frozen_sha:
                raise ValueError(
                    f"HISTORICAL_EVIDENCE_FROZEN_MISMATCH:{rel}:{current_sha}!={frozen_sha}"
                )
            previous = seen_files.get(rel)
            if previous is not None and previous != current_sha:
                raise ValueError(f"HISTORICAL_EVIDENCE_IDENTITY_CONFLICT:{rel}")
            seen_files[rel] = current_sha
            files.append({
                "path": rel,
                "sha256": current_sha,
                "bytes": len(current),
            })
'''
new_build = '''        for rel in evidence_paths(root, session_path, data):
            path = root / rel
            if not path.is_file():
                try:
                    git_show_bytes(root, frozen_commit, rel)
                except subprocess.CalledProcessError:
                    files.append({"path": rel, "present": False})
                    continue
                raise ValueError(f"HISTORICAL_EVIDENCE_CURRENTLY_MISSING:{rel}")
            current = path.read_bytes()
            try:
                frozen = git_show_bytes(root, frozen_commit, rel)
            except subprocess.CalledProcessError as exc:
                raise ValueError(f"HISTORICAL_EVIDENCE_NOT_IN_FROZEN_COMMIT:{rel}") from exc
            current_sha = sha256_bytes(current)
            frozen_sha = sha256_bytes(frozen)
            if current_sha != frozen_sha:
                raise ValueError(
                    f"HISTORICAL_EVIDENCE_FROZEN_MISMATCH:{rel}:{current_sha}!={frozen_sha}"
                )
            previous = seen_files.get(rel)
            if previous is not None and previous != current_sha:
                raise ValueError(f"HISTORICAL_EVIDENCE_IDENTITY_CONFLICT:{rel}")
            seen_files[rel] = current_sha
            files.append({
                "path": rel,
                "present": True,
                "sha256": current_sha,
                "bytes": len(current),
            })
'''
if text.count(old_build) != 1:
    raise RuntimeError('ABSENT_BUILD_ANCHOR')
text = text.replace(old_build, new_build, 1)

old_verify = '''            path = root / rel
            if not path.is_file():
                failures.append(f"HISTORICAL_EVIDENCE_MISSING:{rel}")
                continue
            payload = path.read_bytes()
            expected_sha = str(record.get("sha256", ""))
            if sha256_bytes(payload) != expected_sha:
                failures.append(f"HISTORICAL_CURRENT_HASH_MISMATCH:{rel}")
            if len(payload) != record.get("bytes"):
                failures.append(f"HISTORICAL_CURRENT_SIZE_MISMATCH:{rel}")
            if frozen_commit:
                try:
                    frozen = git_show_bytes(root, frozen_commit, rel)
                except subprocess.CalledProcessError:
                    failures.append(f"HISTORICAL_FROZEN_FILE_MISSING:{rel}")
                else:
                    if sha256_bytes(frozen) != expected_sha:
                        failures.append(f"HISTORICAL_FROZEN_HASH_MISMATCH:{rel}")
                    if len(frozen) != record.get("bytes"):
                        failures.append(f"HISTORICAL_FROZEN_SIZE_MISMATCH:{rel}")
'''
new_verify = '''            path = root / rel
            expected_present = bool(record.get("present", True))
            if not expected_present:
                if path.exists():
                    failures.append(f"HISTORICAL_ABSENT_EVIDENCE_APPEARED:{rel}")
                if frozen_commit:
                    try:
                        git_show_bytes(root, frozen_commit, rel)
                    except subprocess.CalledProcessError:
                        pass
                    else:
                        failures.append(f"HISTORICAL_FROZEN_ABSENCE_MISMATCH:{rel}")
                continue
            if not path.is_file():
                failures.append(f"HISTORICAL_EVIDENCE_MISSING:{rel}")
                continue
            payload = path.read_bytes()
            expected_sha = str(record.get("sha256", ""))
            if sha256_bytes(payload) != expected_sha:
                failures.append(f"HISTORICAL_CURRENT_HASH_MISMATCH:{rel}")
            if len(payload) != record.get("bytes"):
                failures.append(f"HISTORICAL_CURRENT_SIZE_MISMATCH:{rel}")
            if frozen_commit:
                try:
                    frozen = git_show_bytes(root, frozen_commit, rel)
                except subprocess.CalledProcessError:
                    failures.append(f"HISTORICAL_FROZEN_FILE_MISSING:{rel}")
                else:
                    if sha256_bytes(frozen) != expected_sha:
                        failures.append(f"HISTORICAL_FROZEN_HASH_MISMATCH:{rel}")
                    if len(frozen) != record.get("bytes"):
                        failures.append(f"HISTORICAL_FROZEN_SIZE_MISMATCH:{rel}")
'''
if text.count(old_verify) != 1:
    raise RuntimeError('ABSENT_VERIFY_ANCHOR')
text = text.replace(old_verify, new_verify, 1)
path.write_text(text, encoding='utf-8', newline='\n')
print('HISTORICAL_ABSENCE_IDENTITY_PATCH=PASS')
