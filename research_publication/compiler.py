from __future__ import annotations

"""Compile method-approved research material into a static publication snapshot.

The compiler is the only supported seam between research outputs and the
frontend.  It deliberately does not infer whether a result is publishable from
filenames, prose, or the mere existence of a figure.  Eligibility comes from
the publication catalog and release profile.
"""

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from research_publication.adapters import (
    build_r10_official_universe_exhibit,
    build_r4_sakishima_exhibit,
    build_r5_repeat_participation_exhibit,
)
from scripts.build_exploration_system_data_v1 import (
    build_exploration_system_data,
)


PROFILE_PATH = Path("data/metadata/publication_release_profiles_v1.json")
CATALOG_PATH = Path("data/metadata/research_publication_catalog_v1.json")
CORE_SURFACE_PATH = Path(
    "data/metadata/research_publication_core_surfaces_v1.json"
)
COMPILER_SCHEMA_VERSION = "research_publication_snapshot_v1"
PUBLIC_CATALOG_FIELDS = {
    "id",
    "title",
    "research_question",
    "analysis_unit",
    "selection_boundary",
    "method_status",
    "claim_status",
    "target_views",
    "allowed_wording",
    "interpretation_limit",
    "publication_object_path",
}
PUBLICATION_ADAPTERS = {
    "PUB-MR-004": build_r4_sakishima_exhibit,
    "PUB-MR-005": build_r5_repeat_participation_exhibit,
    "PUB-MR-012": build_r10_official_universe_exhibit,
}
PUBLICATION_ADAPTER_SOURCES = {
    "PUB-MR-004": Path("research_publication/adapters/r4_sakishima.py"),
    "PUB-MR-005": Path(
        "research_publication/adapters/r5_repeat_participation.py"
    ),
    "PUB-MR-012": Path(
        "research_publication/adapters/r10_official_universe.py"
    ),
}
PUBLIC_CORE_SURFACE_STATUSES = {
    "architecture_required",
    "module_integrated",
    "partial_bounded",
}
SAFE_CORE_OWNER_FRONTEND_STATUSES = {
    "integrated",
    "adapter_needed_partial_existing",
}


class PublicationError(RuntimeError):
    """Raised when a research package cannot safely become a release."""


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublicationError(f"Required publication input is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PublicationError(f"Invalid JSON publication input: {path}: {exc}") from exc


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_files(root: Path) -> list[Path]:
    return sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def _tree_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    excluded = exclude or set()
    return {
        path.relative_to(root).as_posix(): _sha256(path)
        for path in _tree_files(root)
        if path.relative_to(root).as_posix() not in excluded
    }


def _sanitize(value: Any, stripped_fields: set[str]) -> Any:
    if isinstance(value, list):
        return [_sanitize(item, stripped_fields) for item in value]
    if isinstance(value, dict):
        return {
            key: _sanitize(item, stripped_fields)
            for key, item in value.items()
            if key not in stripped_fields
        }
    return value


def _contains_key(value: Any, forbidden: set[str]) -> bool:
    if isinstance(value, list):
        return any(_contains_key(item, forbidden) for item in value)
    if isinstance(value, dict):
        return any(
            key in forbidden or _contains_key(item, forbidden)
            for key, item in value.items()
        )
    return False


def _load_profiles(project_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = _read_json(project_root / PROFILE_PATH)
    profiles = raw.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise PublicationError("Release profile file requires a non-empty profiles object")
    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            raise PublicationError(f"Release profile {profile_id} must be an object")
        for field in (
            "public",
            "include_research_candidates",
            "include_internal_audit",
            "catalog_release_profile",
            "strip_fields",
        ):
            if field not in profile:
                raise PublicationError(
                    f"Release profile {profile_id} is missing required field {field}"
                )
    return raw, profiles


def _load_catalog(project_root: Path) -> dict[str, Any]:
    raw = _read_json(project_root / CATALOG_PATH)
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise PublicationError("Publication catalog requires an entries array")
    ids: set[str] = set()
    required = {
        "id",
        "title",
        "category",
        "research_question",
        "analysis_unit",
        "selection_boundary",
        "method_status",
        "claim_status",
        "review_status",
        "frontend_status",
        "release_profiles",
        "target_views",
        "assets",
        "allowed_wording",
        "interpretation_limit",
        "next_gate",
    }
    for entry in entries:
        if not isinstance(entry, dict):
            raise PublicationError("Every publication catalog entry must be an object")
        missing = sorted(required - set(entry))
        if missing:
            raise PublicationError(
                f"Catalog entry {entry.get('id', '<unknown>')} is missing: {missing}"
            )
        if entry["id"] in ids:
            raise PublicationError(f"Duplicate publication catalog id: {entry['id']}")
        ids.add(entry["id"])
        if not isinstance(entry["release_profiles"], list):
            raise PublicationError(
                f"Catalog entry {entry['id']} release_profiles must be an array"
            )
        if not isinstance(entry["assets"], list):
            raise PublicationError(f"Catalog entry {entry['id']} assets must be an array")
    return raw


def _load_core_surfaces(project_root: Path) -> dict[str, Any]:
    raw = _read_json(project_root / CORE_SURFACE_PATH)
    surfaces = raw.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise PublicationError(
            "Core surface registry requires a non-empty surfaces array"
        )
    required = {
        "surface_id",
        "source_path",
        "output_path",
        "json_pointer",
        "surface_status",
        "owner_pub_ids",
        "release_profiles",
        "frontend_consumers",
        "interpretation_limit",
    }
    ids: set[str] = set()
    output_paths: set[str] = set()
    for surface in surfaces:
        if not isinstance(surface, dict):
            raise PublicationError("Every core surface row must be an object")
        missing = sorted(required - set(surface))
        if missing:
            raise PublicationError(
                f"Core surface {surface.get('surface_id', '<unknown>')} "
                f"is missing: {missing}"
            )
        surface_id = str(surface["surface_id"])
        if surface_id in ids:
            raise PublicationError(f"Duplicate core surface id: {surface_id}")
        ids.add(surface_id)
        output_path = str(surface["output_path"])
        if output_path in output_paths:
            raise PublicationError(
                f"Duplicate core surface output path: {output_path}"
            )
        output_paths.add(output_path)
        for field in (
            "owner_pub_ids",
            "release_profiles",
            "frontend_consumers",
        ):
            if not isinstance(surface[field], list):
                raise PublicationError(
                    f"Core surface {surface_id} {field} must be an array"
                )
    return raw


def _validate_catalog_gates(
    catalog: dict[str, Any],
    profile_ids: set[str],
) -> None:
    for entry in catalog["entries"]:
        entry_id = entry["id"]
        unknown_profiles = sorted(set(entry["release_profiles"]) - profile_ids)
        if unknown_profiles:
            raise PublicationError(
                f"Catalog entry {entry_id} uses unknown release profiles: "
                f"{unknown_profiles}"
            )
        if entry["category"] == "retired_prohibited":
            if entry["release_profiles"]:
                raise PublicationError(
                    f"Retired catalog entry {entry_id} must have no release profile"
                )
            if entry["frontend_status"] != "retired_prohibited":
                raise PublicationError(
                    f"Retired catalog entry {entry_id} has an unsafe frontend status"
                )
        if entry["frontend_status"] == "integrated":
            if entry["category"] == "retired_prohibited":
                raise PublicationError(
                    f"Retired catalog entry {entry_id} cannot be integrated"
                )
            if entry["method_status"] not in {
                "method_ready",
                "method_ready_bounded",
            }:
                raise PublicationError(
                    f"Integrated entry {entry_id} has not passed its method gate"
                )
            if entry["claim_status"] in {"candidate_hypothesis", "prohibited"}:
                raise PublicationError(
                    f"Integrated entry {entry_id} has an ineligible claim status"
                )
            if not entry["release_profiles"]:
                raise PublicationError(
                    f"Integrated entry {entry_id} has no eligible release profile"
                )
            if not entry.get("publication_object_path"):
                raise PublicationError(
                    f"Integrated entry {entry_id} has no publication object path"
                )
            if entry["category"] == "method_ready_adapter_needed":
                raise PublicationError(
                    f"Integrated entry {entry_id} still claims that an adapter "
                    "is needed"
                )
        if (
            entry["category"] == "method_ready_integrated"
            and entry["frontend_status"] != "integrated"
        ):
            raise PublicationError(
                f"Catalog entry {entry_id} is categorized as integrated but "
                "is not frontend-integrated"
            )


def _safe_relative_path(value: str, *, label: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise PublicationError(f"{label} is unsafe: {value}")
    return relative


def _validate_core_surface_gates(
    core_surfaces: dict[str, Any],
    catalog: dict[str, Any],
    profile_ids: set[str],
) -> None:
    catalog_by_id = {entry["id"]: entry for entry in catalog["entries"]}
    for surface in core_surfaces["surfaces"]:
        surface_id = surface["surface_id"]
        status = surface["surface_status"]
        if status not in {
            "architecture_required",
            "module_integrated",
            "partial_bounded",
            "internal_only",
        }:
            raise PublicationError(
                f"Core surface {surface_id} has unknown status {status!r}"
            )
        _safe_relative_path(
            str(surface["source_path"]),
            label=f"Core surface {surface_id} source path",
        )
        _safe_relative_path(
            str(surface["output_path"]),
            label=f"Core surface {surface_id} output path",
        )
        unknown_profiles = sorted(
            set(surface["release_profiles"]) - profile_ids
        )
        if unknown_profiles:
            raise PublicationError(
                f"Core surface {surface_id} uses unknown profiles: "
                f"{unknown_profiles}"
            )
        owners = surface["owner_pub_ids"]
        if status in {"module_integrated", "partial_bounded"} and not owners:
            raise PublicationError(
                f"Research surface {surface_id} requires a catalog owner"
            )
        if status == "architecture_required" and owners:
            raise PublicationError(
                f"Architecture surface {surface_id} cannot hide catalog owners"
            )
        if status == "internal_only" and set(
            surface["release_profiles"]
        ) - {"internal"}:
            raise PublicationError(
                f"Internal-only surface {surface_id} has a public profile"
            )
        for owner_id in owners:
            owner = catalog_by_id.get(owner_id)
            if owner is None:
                raise PublicationError(
                    f"Core surface {surface_id} has unknown owner {owner_id}"
                )
            if owner["method_status"] not in {
                "method_ready",
                "method_ready_bounded",
            }:
                raise PublicationError(
                    f"Core surface {surface_id} owner {owner_id} has not "
                    "passed its method gate"
                )
            if owner["claim_status"] in {
                "candidate_hypothesis",
                "prohibited",
            }:
                raise PublicationError(
                    f"Core surface {surface_id} owner {owner_id} has an "
                    "ineligible claim status"
                )
            if owner["frontend_status"] not in SAFE_CORE_OWNER_FRONTEND_STATUSES:
                raise PublicationError(
                    f"Core surface {surface_id} owner {owner_id} is not "
                    "integrated or explicitly partial"
                )
            invalid_profiles = sorted(
                set(surface["release_profiles"])
                - set(owner["release_profiles"])
            )
            if invalid_profiles:
                raise PublicationError(
                    f"Core surface {surface_id} exceeds owner {owner_id} "
                    f"profiles: {invalid_profiles}"
                )


def _asset_path(asset: Any) -> str:
    if isinstance(asset, str):
        return asset
    if isinstance(asset, dict):
        for key in ("path", "asset", "source_path"):
            if asset.get(key):
                return str(asset[key])
    raise PublicationError(f"Catalog asset must carry a repository path: {asset!r}")


def _validate_catalog_assets(project_root: Path, entries: list[dict[str, Any]]) -> None:
    for entry in entries:
        for asset in entry["assets"]:
            relative = Path(_asset_path(asset))
            if relative.is_absolute():
                raise PublicationError(
                    f"Catalog entry {entry['id']} uses an absolute asset path: {relative}"
                )
            if not (project_root / relative).exists():
                raise PublicationError(
                    f"Catalog entry {entry['id']} references a missing asset: {relative}"
                )


def _assert_core_builder_contract(
    core_dir: Path,
    *,
    manifested_paths: set[str],
) -> None:
    actual_paths = {
        path.relative_to(core_dir).as_posix() for path in _tree_files(core_dir)
    }
    expected_paths = set(manifested_paths) | {"manifest.json"}
    if actual_paths != expected_paths:
        raise PublicationError(
            "Core builder emitted files outside its manifest contract: "
            f"missing={sorted(expected_paths - actual_paths)} "
            f"unexpected={sorted(actual_paths - expected_paths)}"
        )


def _json_pointer(value: Any, pointer: str, *, surface_id: str) -> Any:
    if pointer in {"", "/"}:
        return value
    if not pointer.startswith("/"):
        raise PublicationError(
            f"Core surface {surface_id} has invalid JSON pointer: {pointer}"
        )
    current = value
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            if index >= len(current):
                raise PublicationError(
                    f"Core surface {surface_id} JSON pointer is out of range: "
                    f"{pointer}"
                )
            current = current[index]
        else:
            raise PublicationError(
                f"Core surface {surface_id} JSON pointer is missing: {pointer}"
            )
    return current


def _apply_profile_row_filter(
    value: Any,
    surface: dict[str, Any],
    *,
    profile: str,
) -> Any:
    rules = surface.get("profile_row_filters", {})
    rule = rules.get(profile) if isinstance(rules, dict) else None
    if rule is None:
        return value
    if not isinstance(value, list):
        raise PublicationError(
            f"Core surface {surface['surface_id']} row filter requires an array"
        )
    field = rule.get("field")
    include = rule.get("include")
    if not isinstance(field, str) or not isinstance(include, list):
        raise PublicationError(
            f"Core surface {surface['surface_id']} has an invalid row filter"
        )
    allowed = set(include)
    return [
        row
        for row in value
        if isinstance(row, dict) and row.get(field) in allowed
    ]


def _catalog_public_fields(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in entry.items()
        if key in PUBLIC_CATALOG_FIELDS
    }


def _publication_envelope(
    entry: dict[str, Any],
    *,
    profile: str,
) -> dict[str, Any]:
    return {
        "catalog_id": entry["id"],
        "release_profile": profile,
        "method_status": entry["method_status"],
        "claim_status": entry["claim_status"],
        "analysis_unit": entry["analysis_unit"],
        "selection_boundary": entry["selection_boundary"],
        "allowed_wording": entry["allowed_wording"],
        "interpretation_limit": entry["interpretation_limit"],
    }


def _compile_core_surfaces(
    core_dir: Path,
    snapshot_dir: Path,
    *,
    core_manifest: dict[str, Any],
    registry: dict[str, Any],
    catalog: dict[str, Any],
    profile: str,
    strip_fields: set[str],
) -> dict[str, Any]:
    """Project explicitly approved core surfaces into a release profile.

    The exploration builder's manifest proves provenance only.  This registry
    decides which exact file or JSON pointer may become a publication surface.
    """

    manifested_paths = set(core_manifest["output_hashes"])
    _assert_core_builder_contract(
        core_dir,
        manifested_paths=manifested_paths,
    )
    registered_sources = {
        str(surface["source_path"]) for surface in registry["surfaces"]
    }
    if registered_sources != manifested_paths:
        raise PublicationError(
            "Core surface registry does not decide every builder output: "
            f"missing={sorted(manifested_paths - registered_sources)} "
            f"unknown={sorted(registered_sources - manifested_paths)}"
        )

    catalog_by_id = {entry["id"]: entry for entry in catalog["entries"]}
    selected = [
        surface
        for surface in registry["surfaces"]
        if profile in surface["release_profiles"]
    ]
    projection_cache: dict[str, Any] = {}
    public_rows: list[dict[str, Any]] = []
    for surface in selected:
        surface_id = surface["surface_id"]
        source_relative = _safe_relative_path(
            str(surface["source_path"]),
            label=f"Core surface {surface_id} source path",
        )
        output_relative = _safe_relative_path(
            str(surface["output_path"]),
            label=f"Core surface {surface_id} output path",
        )
        source = core_dir / source_relative
        target = snapshot_dir / output_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        record_count: int | None = None
        if source.suffix.lower() in {".json", ".geojson"}:
            source_key = source_relative.as_posix()
            if source_key not in projection_cache:
                projection_cache[source_key] = _read_json(source)
            value = _json_pointer(
                projection_cache[source_key],
                str(surface["json_pointer"]),
                surface_id=surface_id,
            )
            value = _apply_profile_row_filter(
                value,
                surface,
                profile=profile,
            )
            if isinstance(value, list):
                record_count = len(value)
            _write_json(target, _sanitize(value, strip_fields))
        else:
            shutil.copy2(source, target)

        if surface["surface_status"] != "internal_only":
            owners = [
                _catalog_public_fields(catalog_by_id[owner_id])
                for owner_id in surface["owner_pub_ids"]
            ]
            public_rows.append(
                {
                    "surface_id": surface_id,
                    "path": output_relative.as_posix(),
                    "surface_status": surface["surface_status"],
                    "owner_pub_ids": surface["owner_pub_ids"],
                    "frontend_consumers": surface["frontend_consumers"],
                    "interpretation_limit": surface["interpretation_limit"],
                    "record_count": record_count,
                    "owners": owners,
                }
            )

    projection = {
        "schema_version": "compiled_core_surfaces_v1",
        "release_profile": profile,
        "entries": public_rows,
    }
    _write_json(snapshot_dir / "views/core_surfaces.json", projection)

    integrated_ids = {
        owner_id
        for row in public_rows
        for owner_id in row["owner_pub_ids"]
        if catalog_by_id[owner_id]["frontend_status"] == "integrated"
    }
    for owner_id in sorted(integrated_ids):
        entry = catalog_by_id[owner_id]
        object_path = entry.get("publication_object_path")
        if not isinstance(object_path, str) or not object_path.startswith(
            "views/core_surfaces/"
        ):
            continue
        owner_rows = [
            {
                key: value
                for key, value in row.items()
                if key != "owners"
            }
            for row in public_rows
            if owner_id in row["owner_pub_ids"]
        ]
        descriptor = {
            "schema_version": "core_surface_publication_object_v1",
            "publication": _publication_envelope(entry, profile=profile),
            "surfaces": owner_rows,
        }
        _write_json(snapshot_dir / object_path, descriptor)
    return projection


def _public_catalog(
    catalog: dict[str, Any],
    catalog_profile: str,
    *,
    public: bool,
) -> dict[str, Any]:
    eligible = [
        entry
        for entry in catalog["entries"]
        if catalog_profile in entry["release_profiles"]
        and entry["frontend_status"] == "integrated"
    ]
    entries = (
        [
            {
                key: value
                for key, value in entry.items()
                if key in PUBLIC_CATALOG_FIELDS
            }
            for entry in eligible
        ]
        if public
        else eligible
    )
    return {
        "schema_version": catalog.get("schema_version", "unknown"),
        "release_profile": catalog_profile,
        "entries": entries,
    }


def _safe_publication_path(entry: dict[str, Any]) -> Path:
    relative = Path(str(entry["publication_object_path"]))
    if relative.is_absolute() or ".." in relative.parts:
        raise PublicationError(
            f"Catalog entry {entry['id']} uses an unsafe publication object "
            f"path: {relative}"
        )
    return relative


def _exhibit_catalog_id(exhibit: dict[str, Any]) -> str | None:
    for key in ("catalog_id", "exhibit_id", "id"):
        value = exhibit.get(key)
        if isinstance(value, str) and value.startswith("PUB-"):
            return value
    return None


def _compile_publication_objects(
    project_root: Path,
    snapshot_dir: Path,
    published_catalog: dict[str, Any],
    *,
    strip_fields: set[str],
) -> dict[str, Any]:
    """Compile every catalog-approved object and build its public index.

    A catalog row is not merely a menu label: it must resolve to one physical
    object in the release.  Adapter-backed exhibits are rebuilt from formal
    tables.  Core objects, such as lifecycle anchors, must already have been
    copied from the validated core package.
    """

    index_entries: list[dict[str, Any]] = []
    for entry in published_catalog["entries"]:
        entry_id = entry["id"]
        relative = _safe_publication_path(entry)
        target = snapshot_dir / relative
        adapter = PUBLICATION_ADAPTERS.get(entry_id)
        payload_kind = "core"
        if adapter is not None:
            exhibit = adapter(project_root)
            if not isinstance(exhibit, dict):
                raise PublicationError(
                    f"Publication adapter {entry_id} did not return an object"
                )
            if _exhibit_catalog_id(exhibit) != entry_id:
                raise PublicationError(
                    f"Publication adapter {entry_id} returned a mismatched "
                    f"catalog identity"
                )
            exhibit["publication"] = _publication_envelope(
                entry,
                profile=str(published_catalog["release_profile"]),
            )
            _write_json(target, _sanitize(exhibit, strip_fields))
            payload_kind = "exhibit"
        elif not target.exists():
            raise PublicationError(
                f"Integrated catalog entry {entry_id} has neither an adapter "
                f"nor an existing core object at {relative.as_posix()}"
            )
        else:
            core_object = _read_json(target)
            publication = (
                core_object.get("publication")
                if isinstance(core_object, dict)
                else None
            )
            expected = _publication_envelope(
                entry,
                profile=str(published_catalog["release_profile"]),
            )
            if publication != expected:
                raise PublicationError(
                    f"Core publication object {entry_id} has a mismatched "
                    "publication envelope"
                )

        index_entries.append(
            {
                "catalog_id": entry_id,
                "path": relative.as_posix(),
                "payload_kind": payload_kind,
                "target_views": entry["target_views"],
                "method_status": entry["method_status"],
                "claim_status": entry["claim_status"],
                "selection_boundary": entry["selection_boundary"],
                "interpretation_limit": entry["interpretation_limit"],
            }
        )

    index = {
        "schema_version": "publication_object_index_v1",
        "entries": index_entries,
    }
    _write_json(snapshot_dir / "views/exhibits.json", index)
    return index


def _store_immutable_release(
    staged_snapshot: Path,
    release_root: Path,
    *,
    profile: str,
    release_id: str,
) -> Path:
    """Store one verified snapshot without overwriting any earlier release."""

    profile_root = release_root / profile
    profile_root.mkdir(parents=True, exist_ok=True)
    target = profile_root / release_id
    if target.exists():
        existing = verify_publication_snapshot(target)
        if existing["status"] != "pass":
            raise PublicationError(
                f"Existing immutable release is invalid: {target}: "
                + "; ".join(existing["errors"])
            )
        staged_manifest = _read_json(staged_snapshot / "manifest.json")
        existing_manifest = _read_json(target / "manifest.json")
        if staged_manifest != existing_manifest:
            raise PublicationError(
                f"Release identity collision with different manifest: {release_id}"
            )
        shutil.rmtree(staged_snapshot)
        return target
    staged_snapshot.rename(target)
    return target


def _activate_channel(
    channel_file: Path,
    *,
    project_root: Path,
    release_dir: Path,
    profile: str,
    release_id: str,
) -> None:
    """Atomically point a channel at an already verified immutable release."""

    try:
        snapshot_path = release_dir.relative_to(project_root).as_posix()
    except ValueError as exc:
        raise PublicationError(
            "The activated release must live below the project root"
        ) from exc
    payload = {
        "schema_version": "publication_channel_v1",
        "channel": channel_file.stem,
        "profile": profile,
        "release_id": release_id,
        "snapshot_path": snapshot_path,
        "manifest_sha256": _sha256(release_dir / "manifest.json"),
    }
    channel_file.parent.mkdir(parents=True, exist_ok=True)
    temporary = channel_file.with_name(f".{channel_file.name}.new")
    _write_json(temporary, payload)
    os.replace(temporary, channel_file)


def compile_publication_snapshot(
    project_root: Path,
    output_dir: Path,
    *,
    profile: str = "client_preview",
    channel_file: Path | None = None,
) -> dict[str, Any]:
    """Compile a deterministic snapshot into an immutable profile release.

    ``output_dir`` is the release store root.  If ``channel_file`` is provided,
    it is atomically updated only after the immutable release verifies.
    """

    project_root = project_root.resolve()
    output_dir = output_dir.resolve()
    profile_document, profiles = _load_profiles(project_root)
    if profile not in profiles:
        raise PublicationError(
            f"Unknown release profile {profile!r}; choose one of {sorted(profiles)}"
        )
    selected = profiles[profile]
    catalog = _load_catalog(project_root)
    core_surfaces = _load_core_surfaces(project_root)
    _validate_catalog_gates(catalog, set(profiles))
    _validate_core_surface_gates(
        core_surfaces,
        catalog,
        set(profiles),
    )
    _validate_catalog_assets(project_root, catalog["entries"])

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    work_root = Path(
        tempfile.mkdtemp(prefix=f".{output_dir.name}.build-", dir=output_dir.parent)
    )
    core_dir = work_root / "core"
    snapshot_dir = work_root / "snapshot"
    try:
        core_manifest = build_exploration_system_data(project_root, core_dir)
        snapshot_dir.mkdir(parents=True)
        strip_fields = set(selected["strip_fields"])
        core_surface_projection = _compile_core_surfaces(
            core_dir,
            snapshot_dir,
            core_manifest=core_manifest,
            registry=core_surfaces,
            catalog=catalog,
            profile=profile,
            strip_fields=strip_fields,
        )

        catalog_profile = str(selected["catalog_release_profile"])
        published_catalog = _public_catalog(
            catalog,
            catalog_profile,
            public=bool(selected["public"]),
        )
        publication_object_index = _compile_publication_objects(
            project_root,
            snapshot_dir,
            published_catalog,
            strip_fields=strip_fields,
        )
        _write_json(snapshot_dir / "views/publication_catalog.json", published_catalog)
        if selected["include_internal_audit"]:
            _write_json(snapshot_dir / "internal/publication_catalog_audit.json", catalog)

        compiler_inputs = {
            "core_data_build_id": core_manifest["build_id"],
            "core_output_hashes": core_manifest["output_hashes"],
            "catalog_sha256": _sha256(project_root / CATALOG_PATH),
            "core_surface_registry_sha256": _sha256(
                project_root / CORE_SURFACE_PATH
            ),
            "profile_document_sha256": _sha256(project_root / PROFILE_PATH),
            "compiler_sha256": _sha256(Path(__file__)),
            "core_builder_sha256": _sha256(
                project_root / "scripts/build_exploration_system_data_v1.py"
            ),
            "publication_adapter_sha256": {
                entry_id: _sha256(project_root / source_path)
                for entry_id, source_path in PUBLICATION_ADAPTER_SOURCES.items()
                if any(
                    row["id"] == entry_id
                    for row in published_catalog["entries"]
                )
            },
            "profile": profile,
        }
        payload_hashes = _tree_hashes(snapshot_dir)
        release_fingerprint = hashlib.sha256(
            json.dumps(
                {
                    "compiler_inputs": compiler_inputs,
                    "payload_hashes": payload_hashes,
                },
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        release_id = f"{profile}-{release_fingerprint[:16]}"
        manifest = {
            "artifact": COMPILER_SCHEMA_VERSION,
            "schema_version": "1.0.0",
            "release_id": release_id,
            "build_id": release_id,
            "data_build_id": core_manifest["build_id"],
            "as_of_date": core_manifest["as_of_date"],
            "release_profile": profile,
            "public": bool(selected["public"]),
            "deterministic": True,
            "capabilities": {
                "research_candidates": bool(
                    selected["include_research_candidates"]
                ),
                "internal_audit": bool(selected["include_internal_audit"]),
                "publication_catalog": True,
                "publication_objects": True,
            },
            "counts": core_manifest["counts"],
            "counts_scope": (
                "core_builder_source_universe; profile-specific row counts "
                "are in core_surface_record_counts"
            ),
            "core_surface_record_counts": {
                row["surface_id"]: row["record_count"]
                for row in core_surface_projection["entries"]
                if row["record_count"] is not None
            },
            "catalog": {
                "eligible_entry_count": len(published_catalog["entries"]),
                "publication_object_count": len(
                    publication_object_index["entries"]
                ),
                "catalog_profile": catalog_profile,
                "core_surface_count": len(
                    core_surface_projection["entries"]
                ),
            },
            "compiler_inputs": compiler_inputs,
            "output_hashes": payload_hashes,
            "validation": {"status": "pending"},
        }
        _write_json(snapshot_dir / "manifest.json", manifest)
        verification = verify_publication_snapshot(
            snapshot_dir,
            profile_document=profile_document,
        )
        if verification["status"] != "pass":
            raise PublicationError(
                "Publication snapshot validation failed: "
                + "; ".join(verification["errors"])
            )
        manifest["validation"] = {
            "status": "pass",
            "check_count": verification["check_count"],
        }
        _write_json(snapshot_dir / "manifest.json", manifest)
        checksums = _tree_hashes(snapshot_dir, exclude={"checksums.json"})
        _write_json(snapshot_dir / "checksums.json", checksums)

        # Verify once more with the final manifest and checksums before activation.
        final_verification = verify_publication_snapshot(
            snapshot_dir,
            profile_document=profile_document,
        )
        if final_verification["status"] != "pass":
            raise PublicationError(
                "Final publication snapshot validation failed: "
                + "; ".join(final_verification["errors"])
            )
        release_dir = _store_immutable_release(
            snapshot_dir,
            output_dir,
            profile=profile,
            release_id=release_id,
        )
        if channel_file is not None:
            channel_file = channel_file.resolve()
            _activate_channel(
                channel_file,
                project_root=project_root,
                release_dir=release_dir,
                profile=profile,
                release_id=release_id,
            )
        return manifest
    finally:
        if work_root.exists():
            shutil.rmtree(work_root)


def verify_publication_snapshot(
    snapshot_dir: Path,
    *,
    profile_document: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify profile isolation, checksums, and public-field boundaries."""

    snapshot_dir = snapshot_dir.resolve()
    errors: list[str] = []
    checks = 0
    manifest_path = snapshot_dir / "manifest.json"
    if not manifest_path.exists():
        return {
            "status": "fail",
            "check_count": 1,
            "errors": ["manifest.json is missing"],
        }
    manifest = _read_json(manifest_path)
    checks += 1
    if manifest.get("artifact") != COMPILER_SCHEMA_VERSION:
        errors.append("manifest artifact does not match the publication compiler")

    if profile_document is None:
        project_root = Path(__file__).resolve().parents[1]
        profile_document = _read_json(project_root / PROFILE_PATH)
    profiles = profile_document.get("profiles", {})
    profile_id = manifest.get("release_profile")
    profile = profiles.get(profile_id)
    checks += 1
    if not isinstance(profile, dict):
        errors.append(f"unknown release profile in manifest: {profile_id!r}")
        return {"status": "fail", "check_count": checks, "errors": errors}

    required = {
        "core/entities/actors.json",
        "core/entities/places.json",
        "core/entities/issues.json",
        "core/map/geometry.geojson",
        "core/presentation/rules.json",
        "core/lifecycle/anchors.json",
        "views/core_surfaces.json",
        "views/exhibits.json",
        "views/publication_catalog.json",
    }
    missing = sorted(path for path in required if not (snapshot_dir / path).exists())
    checks += len(required)
    if missing:
        errors.append(f"required publication files are missing: {missing}")

    catalog_path = snapshot_dir / "views/publication_catalog.json"
    object_index_path = snapshot_dir / "views/exhibits.json"
    if catalog_path.exists() and object_index_path.exists():
        published_catalog = _read_json(catalog_path)
        object_index = _read_json(object_index_path)
        catalog_entries = published_catalog.get("entries", [])
        index_entries = object_index.get("entries", [])
        catalog_ids = {
            entry.get("id")
            for entry in catalog_entries
            if isinstance(entry, dict)
        }
        indexed_ids = {
            entry.get("catalog_id")
            for entry in index_entries
            if isinstance(entry, dict)
        }
        checks += 1
        if catalog_ids != indexed_ids:
            errors.append(
                "publication catalog and object index have different ids"
            )
        for entry in index_entries:
            if not isinstance(entry, dict):
                errors.append("publication object index contains a non-object row")
                continue
            relative = Path(str(entry.get("path", "")))
            checks += 1
            if (
                not relative.parts
                or relative.is_absolute()
                or ".." in relative.parts
                or not (snapshot_dir / relative).exists()
            ):
                errors.append(
                    "publication object is missing or unsafe: "
                    f"{entry.get('catalog_id')}: {relative}"
                )
                continue
            payload = _read_json(snapshot_dir / relative)
            publication = (
                payload.get("publication")
                if isinstance(payload, dict)
                else None
            )
            catalog_entry = next(
                (
                    row
                    for row in catalog_entries
                    if isinstance(row, dict)
                    and row.get("id") == entry.get("catalog_id")
                ),
                None,
            )
            checks += 1
            expected_envelope = (
                _publication_envelope(
                    catalog_entry,
                    profile=str(manifest.get("release_profile")),
                )
                if isinstance(catalog_entry, dict)
                else None
            )
            if publication != expected_envelope:
                errors.append(
                    "publication object envelope does not match its catalog: "
                    f"{entry.get('catalog_id')}"
                )

    core_surface_path = snapshot_dir / "views/core_surfaces.json"
    if core_surface_path.exists():
        core_surface_projection = _read_json(core_surface_path)
        surface_entries = core_surface_projection.get("entries", [])
        checks += 1
        if core_surface_projection.get("release_profile") != profile_id:
            errors.append("core surface projection profile mismatch")
        for row in surface_entries:
            if not isinstance(row, dict):
                errors.append("core surface projection contains a non-object row")
                continue
            relative = Path(str(row.get("path", "")))
            checks += 1
            if (
                not relative.parts
                or relative.is_absolute()
                or ".." in relative.parts
                or not (snapshot_dir / relative).exists()
            ):
                errors.append(
                    f"core surface is missing or unsafe: {row.get('surface_id')}"
                )
            if row.get("surface_status") not in PUBLIC_CORE_SURFACE_STATUSES:
                errors.append(
                    f"public core surface has unsafe status: "
                    f"{row.get('surface_id')}"
                )

    research_path = snapshot_dir / "research"
    checks += 1
    if bool(profile["include_research_candidates"]) != research_path.exists():
        errors.append("research candidate payload does not match the release profile")

    checks += 1
    if profile["public"] and (snapshot_dir / "internal").exists():
        errors.append("public profile contains an internal directory")
    checks += 1
    if (
        not profile["include_internal_audit"]
        and (snapshot_dir / "internal").exists()
    ):
        errors.append("non-internal profile contains internal core material")

    forbidden = set(profile["strip_fields"])
    if forbidden:
        for path in _tree_files(snapshot_dir):
            if path.suffix.lower() not in {".json", ".geojson"}:
                continue
            if path.name in {"manifest.json", "checksums.json"}:
                continue
            checks += 1
            if _contains_key(_read_json(path), forbidden):
                errors.append(
                    f"public field boundary failed for {path.relative_to(snapshot_dir)}"
                )

    output_hashes = manifest.get("output_hashes", {})
    if not isinstance(output_hashes, dict):
        errors.append("manifest output_hashes must be an object")
    else:
        for relative, expected in output_hashes.items():
            checks += 1
            relative_path = Path(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                errors.append(f"manifest output path is unsafe: {relative}")
                continue
            path = snapshot_dir / relative_path
            if not path.exists():
                errors.append(f"manifest output is missing: {relative}")
            elif _sha256(path) != expected:
                errors.append(f"manifest output hash mismatch: {relative}")

    checksum_path = snapshot_dir / "checksums.json"
    actual_files = {
        path.relative_to(snapshot_dir).as_posix()
        for path in _tree_files(snapshot_dir)
    }
    if checksum_path.exists():
        checksum_rows = _read_json(checksum_path)
        if not isinstance(checksum_rows, dict):
            errors.append("checksums.json must be an object")
        else:
            expected_files = set(checksum_rows) | {"checksums.json"}
            checks += 1
            if actual_files != expected_files:
                errors.append(
                    "snapshot file set differs from checksums contract: "
                    f"missing={sorted(expected_files - actual_files)} "
                    f"unexpected={sorted(actual_files - expected_files)}"
                )
            for relative, expected in checksum_rows.items():
                checks += 1
                relative_path = Path(relative)
                if relative_path.is_absolute() or ".." in relative_path.parts:
                    errors.append(f"checksum path is unsafe: {relative}")
                    continue
                path = snapshot_dir / relative_path
                if not path.exists():
                    errors.append(f"checksummed file is missing: {relative}")
                elif _sha256(path) != expected:
                    errors.append(f"checksum mismatch: {relative}")
    elif isinstance(output_hashes, dict):
        expected_files = set(output_hashes) | {"manifest.json"}
        checks += 1
        if actual_files != expected_files:
            errors.append(
                "staged snapshot file set differs from manifest contract: "
                f"missing={sorted(expected_files - actual_files)} "
                f"unexpected={sorted(actual_files - expected_files)}"
            )

    return {
        "status": "pass" if not errors else "fail",
        "check_count": checks,
        "errors": errors,
    }


def verify_publication_channel(
    project_root: Path,
    channel_file: Path,
    *,
    expected_profile: str | None = None,
) -> dict[str, Any]:
    """Verify a channel pointer and the immutable snapshot it activates."""

    project_root = project_root.resolve()
    channel_file = channel_file.resolve()
    errors: list[str] = []
    checks = 0
    try:
        channel = _read_json(channel_file)
    except PublicationError as exc:
        return {
            "status": "fail",
            "check_count": 1,
            "errors": [str(exc)],
        }
    checks += 1
    if channel.get("schema_version") != "publication_channel_v1":
        errors.append("channel schema_version is invalid")
    profile = channel.get("profile")
    checks += 1
    if expected_profile is not None and profile != expected_profile:
        errors.append(
            f"channel profile {profile!r} does not match "
            f"{expected_profile!r}"
        )
    snapshot_text = channel.get("snapshot_path")
    try:
        snapshot_relative = _safe_relative_path(
            str(snapshot_text),
            label="Channel snapshot path",
        )
        snapshot_dir = (project_root / snapshot_relative).resolve()
        snapshot_dir.relative_to(project_root)
    except (PublicationError, ValueError) as exc:
        errors.append(str(exc))
        return {
            "status": "fail",
            "check_count": checks + 1,
            "errors": errors,
        }
    checks += 1
    snapshot_report = verify_publication_snapshot(snapshot_dir)
    checks += snapshot_report["check_count"]
    errors.extend(snapshot_report["errors"])
    manifest_path = snapshot_dir / "manifest.json"
    if manifest_path.exists():
        manifest = _read_json(manifest_path)
        checks += 3
        if manifest.get("release_id") != channel.get("release_id"):
            errors.append("channel release_id does not match snapshot manifest")
        if manifest.get("release_profile") != profile:
            errors.append("channel profile does not match snapshot manifest")
        if _sha256(manifest_path) != channel.get("manifest_sha256"):
            errors.append("channel manifest_sha256 does not match snapshot")
    return {
        "status": "pass" if not errors else "fail",
        "check_count": checks,
        "errors": errors,
        "profile": profile,
        "release_id": channel.get("release_id"),
        "snapshot_path": snapshot_relative.as_posix(),
    }
