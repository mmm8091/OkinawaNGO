from __future__ import annotations

"""Bind a production Vite build to one verified publication snapshot."""

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = PROJECT_ROOT / "prototypes/nr3_explorer"
DIST_ROOT = FRONTEND_ROOT / "dist"
CHANNEL_PATH = PROJECT_ROOT / "outputs/publication_channels_v1/client_preview.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def files_below(root: Path, *, excluded: set[str] | None = None) -> Iterable[Path]:
    excluded = excluded or set()
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file() and path.relative_to(root).as_posix() not in excluded
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def tree_hashes(root: Path, *, excluded: set[str] | None = None) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in files_below(root, excluded=excluded)
    }


def git_source_state() -> dict[str, object]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty_rows = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return {
        "commit": commit,
        "dirty": bool(dirty_rows),
        "dirty_path_count": len(dirty_rows),
    }


def main() -> None:
    if not DIST_ROOT.exists():
        raise SystemExit("Vite dist is missing; run this script only after vite build")
    channel = json.loads(CHANNEL_PATH.read_text(encoding="utf-8"))
    data_manifest = json.loads((DIST_ROOT / "manifest.json").read_text(encoding="utf-8"))
    if channel["release_id"] != data_manifest.get("release_id"):
        raise SystemExit("Vite output does not match the active publication channel")
    if channel["profile"] != "client_preview":
        raise SystemExit("Deployable frontend requires the client_preview channel")
    if channel["manifest_sha256"] != sha256(DIST_ROOT / "manifest.json"):
        raise SystemExit("Vite output manifest hash does not match the active channel")
    if data_manifest.get("public") is not True:
        raise SystemExit("Only a public publication profile may become a deployable site")
    if (DIST_ROOT / "internal").exists() or (DIST_ROOT / "validation_report.md").exists():
        raise SystemExit("Internal publication material leaked into the deployable site")

    frontend_inputs = [
        *files_below(FRONTEND_ROOT / "src"),
        FRONTEND_ROOT / "index.html",
        FRONTEND_ROOT / "package.json",
        FRONTEND_ROOT / "package-lock.json",
        FRONTEND_ROOT / "vite.config.mjs",
    ]
    frontend_hashes = {
        path.relative_to(FRONTEND_ROOT).as_posix(): sha256(path)
        for path in sorted(frontend_inputs, key=lambda item: item.as_posix())
    }
    excluded = {"release.json", "site_checksums.json"}
    site_hashes = tree_hashes(DIST_ROOT, excluded=excluded)
    base_path = os.environ.get("VITE_BASE_PATH", "/")
    source_state = git_source_state()
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "publication_release_id": channel["release_id"],
                "publication_manifest_sha256": sha256(DIST_ROOT / "manifest.json"),
                "frontend_inputs": frontend_hashes,
                "site_payload": site_hashes,
                "base_path": base_path,
                "source_state": source_state,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    release = {
        "schema_version": "static_site_release_v1",
        "site_release_id": f"site-{fingerprint[:16]}",
        "publication_release_id": channel["release_id"],
        "publication_profile": channel["profile"],
        "publication_manifest_sha256": sha256(DIST_ROOT / "manifest.json"),
        "frontend_tree_hash": hashlib.sha256(
            json.dumps(frontend_hashes, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest(),
        "base_path": base_path,
        "source_commit": source_state["commit"],
        "source_dirty": source_state["dirty"],
        "source_dirty_path_count": source_state["dirty_path_count"],
        "deterministic": True,
        "validation": {
            "status": "pass",
            "internal_leak_count": 0,
            "payload_file_count": len(site_hashes),
        },
    }
    write_json(DIST_ROOT / "release.json", release)
    write_json(
        DIST_ROOT / "site_checksums.json",
        tree_hashes(DIST_ROOT, excluded={"site_checksums.json"}),
    )
    print(
        json.dumps(
            {
                "site_release_id": release["site_release_id"],
                "publication_release_id": release["publication_release_id"],
                "validation": "pass",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
