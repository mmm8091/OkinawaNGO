from __future__ import annotations

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


def read_sources() -> list[dict[str, str]]:
    with SOURCE_LOG.open("r", encoding="utf-8-sig", newline="") as f:
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


def fetch(url: str) -> tuple[bytes, dict[str, str]]:
    request = Request(
        iri_to_uri(url),
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.8,en;q=0.6,zh-CN;q=0.5",
        },
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


def archive_source(row: dict[str, str]) -> dict[str, str]:
    source_id = row["source_id"]
    url = row["url"].strip()
    source_dir = ARCHIVE_ROOT / safe_name(source_id)
    source_dir.mkdir(parents=True, exist_ok=True)
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


def main() -> None:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_rows = [archive_source(row) for row in read_sources()]
    write_manifest(manifest_rows)
    counts: dict[str, int] = {}
    for row in manifest_rows:
        status = row["archive_status"]
        counts[status] = counts.get(status, 0) + 1
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))
    print(MANIFEST.relative_to(ROOT))


if __name__ == "__main__":
    main()
