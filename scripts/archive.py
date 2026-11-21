#!/usr/bin/env python3
"""Create and verify atomic, content-addressed Daoshengyi forge snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"Error: {message}")


def validate_component(value: str, label: str) -> str:
    if value in {".", ".."} or not COMPONENT.fullmatch(value):
        fail(f"invalid {label}: {value!r}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def snapshot_path(archive: Path, forge_id: str, version: str) -> Path:
    root = archive.resolve()
    target = (root / validate_component(forge_id, "forge id") / validate_component(version, "version")).resolve()
    if not within(target, root):
        fail("snapshot target escapes archive root")
    return target


def load_manifest(snapshot: Path) -> dict:
    manifest_path = snapshot / "lineage.json"
    if not manifest_path.is_file():
        fail(f"lineage manifest not found: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid lineage manifest {manifest_path}: {exc}")
    if data.get("manifest_version") != "1.1":
        fail(f"unsupported manifest version in {manifest_path}")
    return data


def verify_directory(snapshot: Path, verify_parent: bool = True) -> dict:
    snapshot = snapshot.resolve()
    manifest = load_manifest(snapshot)
    expected = {entry["path"]: entry for entry in manifest.get("files", [])}
    actual: dict[str, Path] = {}
    for path in sorted(snapshot.rglob("*")):
        if path.is_symlink():
            fail(f"symlink found in snapshot: {path}")
        if path.is_file() and path.name != "lineage.json":
            actual[path.relative_to(snapshot).as_posix()] = path
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        fail(f"snapshot file set mismatch; missing={missing}, extra={extra}")
    for rel, path in actual.items():
        entry = expected[rel]
        if path.stat().st_size != entry.get("bytes"):
            fail(f"size mismatch: {rel}")
        if sha256(path) != entry.get("sha256"):
            fail(f"hash mismatch: {rel}")
    parent = manifest.get("parent_version")
    parent_hash = manifest.get("parent_manifest_sha256")
    if verify_parent and parent:
        parent_path = snapshot.parent / validate_component(parent, "parent version")
        verify_directory(parent_path, verify_parent=True)
        if sha256(parent_path / "lineage.json") != parent_hash:
            fail(f"parent manifest hash mismatch: {parent}")
    return {
        "status": "ok",
        "snapshot": str(snapshot),
        "files": len(actual),
        "manifest_sha256": sha256(snapshot / "lineage.json"),
    }


def create_snapshot(source: Path, archive: Path, forge_id: str, version: str, parent: str | None, note: str | None) -> dict:
    forge_id = validate_component(forge_id, "forge id")
    version = validate_component(version, "version")
    source = source.resolve()
    if not source.is_dir():
        fail(f"source directory not found: {source}")
    archive = archive.resolve()
    archive.mkdir(parents=True, exist_ok=True)
    if within(archive, source):
        fail("archive root must not be inside the source directory")
    target = snapshot_path(archive, forge_id, version)
    if target.exists():
        fail(f"snapshot already exists: {target}")
    forge_dir = target.parent
    forge_dir.mkdir(parents=True, exist_ok=True)

    parent_hash = None
    if parent:
        parent = validate_component(parent, "parent version")
        if parent == version:
            fail("parent version cannot equal snapshot version")
        parent_path = snapshot_path(archive, forge_id, parent)
        verify_directory(parent_path, verify_parent=True)
        parent_hash = sha256(parent_path / "lineage.json")

    staging = forge_dir / f".{version}.tmp-{uuid.uuid4().hex}"
    try:
        staging.mkdir()
        files = []
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                fail(f"source contains symlink: {path}")
            if not path.is_file():
                continue
            rel = path.relative_to(source)
            output = staging / rel
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, output)
            files.append({"path": rel.as_posix(), "sha256": sha256(output), "bytes": output.stat().st_size})
        manifest = {
            "manifest_version": "1.1",
            "forge_id": forge_id,
            "version": version,
            "parent_version": parent,
            "parent_manifest_sha256": parent_hash,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "note": note,
            "files": files,
        }
        (staging / "lineage.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staging.rename(target)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return verify_directory(target, verify_parent=True)


def list_snapshots(archive: Path, forge_id: str) -> dict:
    forge_id = validate_component(forge_id, "forge id")
    forge_dir = (archive.resolve() / forge_id).resolve()
    if not within(forge_dir, archive.resolve()):
        fail("forge path escapes archive root")
    versions = []
    if forge_dir.is_dir():
        for path in sorted(forge_dir.iterdir()):
            if path.is_dir() and not path.name.startswith(".") and (path / "lineage.json").is_file():
                manifest = load_manifest(path)
                versions.append({"version": manifest["version"], "parent_version": manifest.get("parent_version"), "created_at": manifest.get("created_at")})
    return {"status": "ok", "forge_id": forge_id, "versions": versions}


def diff_snapshots(archive: Path, forge_id: str, left: str, right: str) -> dict:
    left_path = snapshot_path(archive, forge_id, left)
    right_path = snapshot_path(archive, forge_id, right)
    verify_directory(left_path)
    verify_directory(right_path)
    left_files = {entry["path"]: entry["sha256"] for entry in load_manifest(left_path)["files"]}
    right_files = {entry["path"]: entry["sha256"] for entry in load_manifest(right_path)["files"]}
    return {
        "status": "ok",
        "left": left,
        "right": right,
        "added": sorted(set(right_files) - set(left_files)),
        "removed": sorted(set(left_files) - set(right_files)),
        "changed": sorted(path for path in set(left_files) & set(right_files) if left_files[path] != right_files[path]),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Daoshengyi forge lineage snapshots.")
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="Create an atomic snapshot")
    snap.add_argument("source", type=Path)
    snap.add_argument("--archive", type=Path, default=Path("archive"))
    snap.add_argument("--forge-id", required=True)
    snap.add_argument("--version", required=True)
    snap.add_argument("--parent")
    snap.add_argument("--note")
    verify = sub.add_parser("verify", help="Verify a snapshot and its parent chain")
    verify.add_argument("--archive", type=Path, default=Path("archive"))
    verify.add_argument("--forge-id", required=True)
    verify.add_argument("--version", required=True)
    listing = sub.add_parser("list", help="List versions")
    listing.add_argument("--archive", type=Path, default=Path("archive"))
    listing.add_argument("--forge-id", required=True)
    diff = sub.add_parser("diff", help="Compare snapshot file hashes")
    diff.add_argument("--archive", type=Path, default=Path("archive"))
    diff.add_argument("--forge-id", required=True)
    diff.add_argument("left")
    diff.add_argument("right")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "snapshot":
        result = create_snapshot(args.source, args.archive, args.forge_id, args.version, args.parent, args.note)
    elif args.command == "verify":
        result = verify_directory(snapshot_path(args.archive, args.forge_id, args.version))
    elif args.command == "list":
        result = list_snapshots(args.archive, args.forge_id)
    else:
        result = diff_snapshots(args.archive, args.forge_id, args.left, args.right)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
