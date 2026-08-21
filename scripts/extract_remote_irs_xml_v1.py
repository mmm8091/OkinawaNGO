#!/usr/bin/env python3
"""Extract one IRS Form 990 XML member from an official bulk ZIP via HTTP ranges.

The IRS distributes recent e-filed returns in very large monthly/yearly ZIP files.
This helper reads only the end-of-central-directory record, the central directory,
the target member header, and that member's compressed bytes.  It refuses servers
that ignore byte ranges so a failed lookup cannot silently download a multi-GB ZIP.
"""

from __future__ import annotations

import argparse
import binascii
import hashlib
import struct
import sys
import urllib.request
import zlib
from pathlib import Path


USER_AGENT = "Okinawa-NGO-Research/1.0 (official IRS filing receipt archival)"


def request(url: str, *, byte_range: tuple[int, int] | None = None):
    headers = {"User-Agent": USER_AGENT, "Accept-Encoding": "identity"}
    if byte_range is not None:
        headers["Range"] = f"bytes={byte_range[0]}-{byte_range[1]}"
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120)


def content_length(url: str) -> int:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        length = response.headers.get("Content-Length")
        if not length:
            raise RuntimeError("official ZIP did not expose Content-Length")
        return int(length)


def fetch_range(url: str, start: int, end: int) -> bytes:
    with request(url, byte_range=(start, end)) as response:
        if response.status != 206:
            raise RuntimeError(
                f"server ignored Range request ({response.status}); refusing full ZIP download"
            )
        data = response.read()
        expected = end - start + 1
        if len(data) != expected:
            raise RuntimeError(f"short range read: expected {expected}, received {len(data)}")
        return data


def central_directory(url: str, size: int) -> bytes:
    tail_size = min(size, 131_072)
    tail_start = size - tail_size
    tail = fetch_range(url, tail_start, size - 1)
    signature = b"PK\x05\x06"
    eocd_at = tail.rfind(signature)
    if eocd_at < 0:
        raise RuntimeError("ZIP end-of-central-directory record not found")
    if eocd_at + 22 > len(tail):
        raise RuntimeError("truncated ZIP end-of-central-directory record")
    (
        _signature,
        disk_no,
        cd_disk,
        entries_disk,
        entries_total,
        cd_size,
        cd_offset,
        comment_length,
    ) = struct.unpack_from("<4s4H2LH", tail, eocd_at)
    if disk_no or cd_disk or entries_disk != entries_total:
        raise RuntimeError("multi-disk ZIPs are not supported")
    if cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        raise RuntimeError("ZIP64 central directory is not supported")
    if eocd_at + 22 + comment_length > len(tail):
        raise RuntimeError("truncated ZIP comment")
    return fetch_range(url, cd_offset, cd_offset + cd_size - 1)


def find_member(cd: bytes, object_id: str) -> dict[str, int | str]:
    pos = 0
    candidates: list[dict[str, int | str]] = []
    while pos + 46 <= len(cd):
        if cd[pos : pos + 4] != b"PK\x01\x02":
            raise RuntimeError(f"unexpected central-directory signature at byte {pos}")
        flags = struct.unpack_from("<H", cd, pos + 8)[0]
        method = struct.unpack_from("<H", cd, pos + 10)[0]
        crc32 = struct.unpack_from("<L", cd, pos + 16)[0]
        compressed_size = struct.unpack_from("<L", cd, pos + 20)[0]
        uncompressed_size = struct.unpack_from("<L", cd, pos + 24)[0]
        name_len = struct.unpack_from("<H", cd, pos + 28)[0]
        extra_len = struct.unpack_from("<H", cd, pos + 30)[0]
        comment_len = struct.unpack_from("<H", cd, pos + 32)[0]
        local_offset = struct.unpack_from("<L", cd, pos + 42)[0]
        name_bytes = cd[pos + 46 : pos + 46 + name_len]
        encoding = "utf-8" if flags & 0x800 else "cp437"
        name = name_bytes.decode(encoding)
        if object_id in Path(name).name and name.lower().endswith(".xml"):
            candidates.append(
                {
                    "name": name,
                    "flags": flags,
                    "method": method,
                    "crc32": crc32,
                    "compressed_size": compressed_size,
                    "uncompressed_size": uncompressed_size,
                    "local_offset": local_offset,
                }
            )
        pos += 46 + name_len + extra_len + comment_len
    if len(candidates) != 1:
        names = ", ".join(str(item["name"]) for item in candidates) or "none"
        raise RuntimeError(f"expected one XML member for {object_id}; found {names}")
    return candidates[0]


def extract(url: str, object_id: str) -> tuple[bytes, str, int, int]:
    size = content_length(url)
    cd = central_directory(url, size)
    member = find_member(cd, object_id)
    local_offset = int(member["local_offset"])
    local = fetch_range(url, local_offset, local_offset + 29)
    if local[:4] != b"PK\x03\x04":
        raise RuntimeError("invalid local-file header signature")
    name_len = struct.unpack_from("<H", local, 26)[0]
    extra_len = struct.unpack_from("<H", local, 28)[0]
    compressed_size = int(member["compressed_size"])
    data_start = local_offset + 30 + name_len + extra_len
    compressed = fetch_range(url, data_start, data_start + compressed_size - 1)
    method = int(member["method"])
    if method == 0:
        raw = compressed
    elif method == 8:
        raw = zlib.decompress(compressed, -15)
    elif method == 9:
        try:
            from inflate64 import Inflater
        except ImportError as exc:
            raise RuntimeError(
                "ZIP member uses Deflate64 (method 9); install the optional "
                "'inflate64' package or expose it through PYTHONPATH"
            ) from exc
        raw = Inflater().inflate(compressed)
    else:
        raise RuntimeError(f"unsupported ZIP compression method {method}")
    expected_size = int(member["uncompressed_size"])
    if len(raw) != expected_size:
        raise RuntimeError(f"size mismatch: expected {expected_size}, extracted {len(raw)}")
    crc = binascii.crc32(raw) & 0xFFFFFFFF
    if crc != int(member["crc32"]):
        raise RuntimeError("CRC-32 mismatch")
    return raw, str(member["name"]), size, len(cd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="official IRS bulk ZIP URL")
    parser.add_argument("--object-id", required=True, help="IRS OBJECT_ID from the annual index")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    raw, member_name, zip_size, cd_size = extract(args.url, args.object_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    print(f"member={member_name}")
    print(f"output={args.output}")
    print(f"bytes={len(raw)}")
    print(f"sha256={digest}")
    print(f"official_zip_bytes={zip_size}")
    print(f"central_directory_bytes={cd_size}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - command-line diagnostic
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
