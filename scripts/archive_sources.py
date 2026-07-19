from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse, urlunparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE_LOG = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
ARCHIVE_ROOT = ROOT / "source_docs" / "source_archive"
MANIFEST = ARCHIVE_ROOT / "source_archive_manifest.csv"

TIMEOUT_SECONDS = 30
USER_AGENT = (
    "Mozilla/5.0 (compatible; OkinawaNGOResearchBot/0.1; "
    "+https://github.com/mmm8091/OkinawaNGO)"
)
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)


def read_sources() -> list[dict[str, str]]:
    with SOURCE_LOG.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_manifest_rows() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return value.strip("._") or "source"


def extension_for(url: str, content_type: str | None) -> str:
    if content_type:
        media_type = content_type.split(";", 1)[0].strip().lower()
        if media_type == "text/html":
            return ".html"
        guessed = mimetypes.guess_extension(media_type)
        if guessed:
            return guessed

    suffix = Path(urlparse(url).path).suffix
    if suffix:
        return suffix[:12]
    return ".bin"


def is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def iri_to_uri(url: str) -> str:
    parsed = urlparse(url)
    path = quote(parsed.path, safe="/%")
    query = quote(parsed.query, safe="=&?/%:+,;@")
    fragment = quote(parsed.fragment, safe="=&?/%:+,;@")
    return urlunparse((parsed.scheme, parsed.netloc, path, parsed.params, query, fragment))


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def validate_body(url: str, body: bytes, content_type: str) -> str | None:
    path = urlparse(url).path.lower()
    media_type = content_type.split(";", 1)[0].strip().lower()
    if path.endswith(".pdf") or media_type == "application/pdf":
        if not body.startswith(b"%PDF"):
            return "Expected PDF but downloaded non-PDF response."
    return None


def request_headers(url: str) -> dict[str, str]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.8,en;q=0.6,zh-CN;q=0.5",
    }
    parsed = urlparse(url)
    if (
        parsed.netloc.lower() == "researchmap.jp"
        and parsed.path.endswith("/attachment_file.pdf")
    ):
        headers["User-Agent"] = BROWSER_USER_AGENT
        headers["Referer"] = url.rsplit("/", 1)[0]
    return headers


def fetch(url: str) -> tuple[bytes, dict[str, str]]:
    request = Request(
        iri_to_uri(url),
        headers=request_headers(url),
    )
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        body = response.read()
        headers = {
            "final_url": response.geturl(),
            "status_code": str(getattr(response, "status", "")),
            "content_type": response.headers.get("Content-Type", ""),
            "content_length": response.headers.get("Content-Length", ""),
            "last_modified": response.headers.get("Last-Modified", ""),
        }
    return body, headers


def write_metadata(path: Path, metadata: dict[str, object]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
        f.write("\n")


def verified_local_sha(
    metadata: dict[str, object],
    metadata_path: Path,
    *,
    reconcile_cache_hashes: bool,
) -> str | None:
    """Return the preserved artifact SHA, refusing silent cache drift."""

    local_path = str(metadata.get("local_path", ""))
    if not local_path:
        return None
    artifact_path = ROOT / local_path
    if not artifact_path.exists():
        return None

    actual_sha = sha256_bytes(artifact_path.read_bytes())
    recorded_sha = str(metadata.get("sha256", ""))
    if recorded_sha == actual_sha:
        return actual_sha
    if not reconcile_cache_hashes:
        source_id = metadata.get("source_id", metadata_path.parent.name)
        raise RuntimeError(
            f"{source_id}: cached artifact SHA does not match metadata; "
            "inspect the preserved artifact, then run --reconcile-cache-hashes "
            "only if the local artifact is the intended archive copy"
        )

    history = metadata.get("sha256_reconciliation_history", [])
    if not isinstance(history, list):
        history = []
    history.append(
        {
            "previous_sha256": recorded_sha,
            "artifact_sha256": actual_sha,
            "reconciled_at_utc": datetime.now(timezone.utc).isoformat(),
            "method": "local_artifact_no_refetch",
        }
    )
    metadata["sha256_reconciliation_history"] = history
    metadata["sha256"] = actual_sha
    write_metadata(metadata_path, metadata)
    return actual_sha


def existing_manual_archive(
    row: dict[str, str],
    source_dir: Path,
    *,
    reconcile_cache_hashes: bool,
) -> dict[str, str] | None:
    metadata_path = source_dir / "metadata.json"
    if not metadata_path.exists():
        return None
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if metadata.get("archive_status") != "manual_archived":
        return None
    local_path = metadata.get("local_path", "")
    if local_path and not (ROOT / local_path).exists():
        return None
    actual_sha = verified_local_sha(
        metadata,
        metadata_path,
        reconcile_cache_hashes=reconcile_cache_hashes,
    )
    return {
        "source_id": row["source_id"],
        "title": row.get("title", ""),
        "url": row.get("url", ""),
        "archive_status": "manual_archived",
        "local_path": local_path,
        "metadata_path": str(metadata_path.relative_to(ROOT)),
        "sha256": actual_sha or metadata.get("sha256", ""),
        "content_type": metadata.get("content_type", ""),
        "http_status": metadata.get("http_status", ""),
        "archived_at_utc": metadata.get("archived_at_utc", ""),
        "note": metadata.get("note", "Preserved existing manual archive."),
    }


def existing_cached_archive(
    row: dict[str, str],
    source_dir: Path,
    *,
    retry_failed: bool,
    reconcile_cache_hashes: bool,
) -> dict[str, str] | None:
    """Reuse a prior result when the source URL and local artifact are unchanged."""

    metadata_path = source_dir / "metadata.json"
    if not metadata_path.exists():
        return None
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    status = str(metadata.get("archive_status", ""))
    if status == "manual_archived":
        return None  # handled by existing_manual_archive
    if str(metadata.get("url", "")).strip() != row.get("url", "").strip():
        return None
    if status == "failed" and retry_failed:
        return None
    if status not in {
        "archived",
        "failed",
        "skipped_inferred_url",
        "skipped_non_url_reference",
    }:
        return None

    local_path = str(metadata.get("local_path", ""))
    if status == "archived" and (not local_path or not (ROOT / local_path).exists()):
        return None
    actual_sha = None
    if status == "archived":
        actual_sha = verified_local_sha(
            metadata,
            metadata_path,
            reconcile_cache_hashes=reconcile_cache_hashes,
        )
    return {
        "source_id": row["source_id"],
        "title": row.get("title", ""),
        "url": row.get("url", "").strip(),
        "archive_status": status,
        "local_path": local_path,
        "metadata_path": str(metadata_path.relative_to(ROOT)),
        "sha256": actual_sha or str(metadata.get("sha256", "")),
        "content_type": str(metadata.get("content_type", "")),
        "http_status": str(metadata.get("http_status", "")),
        "archived_at_utc": str(metadata.get("archived_at_utc", "")),
        "note": str(metadata.get("note", "")),
    }


def archive_source(
    row: dict[str, str],
    *,
    retry_failed: bool = False,
    refresh_all: bool = False,
    reconcile_cache_hashes: bool = False,
) -> dict[str, str]:
    source_id = row["source_id"]
    url = row["url"].strip()
    source_dir = ARCHIVE_ROOT / safe_name(source_id)
    source_dir.mkdir(parents=True, exist_ok=True)
    manual = existing_manual_archive(
        row,
        source_dir,
        reconcile_cache_hashes=reconcile_cache_hashes,
    )
    if manual:
        return manual
    if not refresh_all:
        cached = existing_cached_archive(
            row,
            source_dir,
            retry_failed=retry_failed,
            reconcile_cache_hashes=reconcile_cache_hashes,
        )
        if cached:
            return cached
    archived_at = datetime.now(timezone.utc).isoformat()

    base = {
        "source_id": source_id,
        "title": row.get("title", ""),
        "url": url,
        "archive_status": "",
        "local_path": "",
        "metadata_path": str((source_dir / "metadata.json").relative_to(ROOT)),
        "sha256": "",
        "content_type": "",
        "http_status": "",
        "archived_at_utc": archived_at,
        "note": "",
    }

    if not url or url.startswith("inferred_url:"):
        metadata = {**row, **base, "archive_status": "skipped_inferred_url"}
        write_metadata(source_dir / "metadata.json", metadata)
        return {**base, "archive_status": "skipped_inferred_url", "note": "URL placeholder needs verification before archiving."}

    if not is_http_url(url):
        metadata = {**row, **base, "archive_status": "skipped_non_url_reference"}
        write_metadata(source_dir / "metadata.json", metadata)
        return {**base, "archive_status": "skipped_non_url_reference", "note": "Non-URL reference needs manual bibliographic archive."}

    try:
        body, headers = fetch(url)
        validation_error = validate_body(headers.get("final_url") or url, body, headers.get("content_type", ""))
        if validation_error:
            raise ValueError(validation_error)
        ext = extension_for(headers.get("final_url") or url, headers.get("content_type"))
        raw_path = source_dir / f"raw{ext}"
        raw_path.write_bytes(body)
        digest = sha256_bytes(body)
        metadata = {
            **row,
            **base,
            "archive_status": "archived",
            "local_path": str(raw_path.relative_to(ROOT)),
            "sha256": digest,
            "content_type": headers.get("content_type", ""),
            "http_status": headers.get("status_code", ""),
            "response_headers": headers,
        }
        write_metadata(source_dir / "metadata.json", metadata)
        return {
            **base,
            "archive_status": "archived",
            "local_path": str(raw_path.relative_to(ROOT)),
            "sha256": digest,
            "content_type": headers.get("content_type", ""),
            "http_status": headers.get("status_code", ""),
        }
    except HTTPError as exc:
        note = f"HTTPError {exc.code}: {exc.reason}"
    except URLError as exc:
        note = f"URLError: {exc.reason}"
    except TimeoutError:
        note = "TimeoutError"
    except Exception as exc:  # noqa: BLE001
        note = f"{type(exc).__name__}: {exc}"

    metadata = {**row, **base, "archive_status": "failed", "note": note}
    write_metadata(source_dir / "metadata.json", metadata)
    return {**base, "archive_status": "failed", "note": note}


def write_manifest(rows: list[dict[str, str]]) -> None:
    fields = [
        "source_id",
        "title",
        "url",
        "archive_status",
        "local_path",
        "metadata_path",
        "sha256",
        "content_type",
        "http_status",
        "archived_at_utc",
        "note",
    ]
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive source-log URLs locally.")
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry unchanged sources whose previous archive status was failed.",
    )
    parser.add_argument(
        "--refresh-all",
        action="store_true",
        help="Refetch every non-manual HTTP source instead of using cached archives.",
    )
    parser.add_argument(
        "--reconcile-cache-hashes",
        action="store_true",
        help=(
            "After manual inspection, update stale metadata SHA values to the "
            "current preserved local artifacts without refetching; records history."
        ),
    )
    parser.add_argument(
        "--from-id",
        type=int,
        help="Archive only source IDs at or above this numeric S-ID (preserves other manifest rows).",
    )
    parser.add_argument(
        "--to-id",
        type=int,
        help="Archive only source IDs at or below this numeric S-ID (preserves other manifest rows).",
    )
    return parser.parse_args()


def numeric_source_id(source_id: str) -> int:
    if not source_id.startswith("S") or not source_id[1:].isdigit():
        raise ValueError(f"Expected numeric S-ID, got {source_id!r}")
    return int(source_id[1:])


def main() -> None:
    args = parse_args()
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    sources = read_sources()
    subset_mode = args.from_id is not None or args.to_id is not None
    selected_sources = [
        row
        for row in sources
        if (args.from_id is None or numeric_source_id(row["source_id"]) >= args.from_id)
        and (args.to_id is None or numeric_source_id(row["source_id"]) <= args.to_id)
    ]
    selected_rows = [
        archive_source(
            row,
            retry_failed=args.retry_failed,
            refresh_all=args.refresh_all,
            reconcile_cache_hashes=args.reconcile_cache_hashes,
        )
        for row in selected_sources
    ]
    if subset_mode:
        if not MANIFEST.exists():
            raise FileNotFoundError("Subset archiving requires an existing complete manifest")
        existing_by_id = {row["source_id"]: row for row in read_manifest_rows()}
        selected_by_id = {row["source_id"]: row for row in selected_rows}
        missing = [
            row["source_id"]
            for row in sources
            if row["source_id"] not in selected_by_id and row["source_id"] not in existing_by_id
        ]
        if missing:
            raise ValueError(f"Existing manifest lacks unselected source rows: {missing}")
        manifest_rows = [
            (
                selected_by_id[row["source_id"]]
                if row["source_id"] in selected_by_id
                else existing_by_id[row["source_id"]]
            )
            for row in sources
        ]
    else:
        manifest_rows = selected_rows
    write_manifest(manifest_rows)
    counts: dict[str, int] = {}
    for row in manifest_rows:
        status = row["archive_status"]
        counts[status] = counts.get(status, 0) + 1
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))
    print(MANIFEST.relative_to(ROOT))


if __name__ == "__main__":
    main()
