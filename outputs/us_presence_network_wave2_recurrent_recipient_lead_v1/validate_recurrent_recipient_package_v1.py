from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
RAW_ARTIFACT_HASHES = {
    "artifacts/aru_about_official.html": "d2f3ca0f86451d5491c42de6b66b54d3386d5dc6f9282db22c11985b1cc21925",
    "artifacts/uruma_kimutaka_club_official.pdf": "61325fb9f8519c8a33622576cb999b7737159883561d1a089cb95c59441b1d47",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_text_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        errors.append(f"{path.name}: missing final LF")
    if data.endswith(b"\n\n"):
        errors.append(f"{path.name}: more than one final LF")
    if b"\r" in data:
        errors.append(f"{path.name}: contains CR; package text must use LF")
    for match in re.finditer(rb"[ \t]+\n", data):
        line = data[: match.start()].count(b"\n") + 1
        errors.append(f"{path.name}:{line}: trailing horizontal whitespace")
    try:
        data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        errors.append(f"{path.name}: not UTF-8 decodable: {exc}")
    return errors


def main() -> int:
    errors: list[str] = []

    for relative, expected_hash in RAW_ARTIFACT_HASHES.items():
        path = PACKAGE_DIR / relative
        if not path.is_file():
            errors.append(f"missing raw artifact: {relative}")
        elif sha256(path) != expected_hash:
            errors.append(f"raw artifact changed: {relative}")

    text_suffixes = {".md", ".py", ".csv", ".json"}
    for path in sorted(PACKAGE_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower() in text_suffixes:
            errors.extend(check_text_file(path))

    manifest_path = PACKAGE_DIR / "manifest_v1.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") != "lead_only":
            errors.append("manifest status is not lead_only")
        for row in manifest.get("outputs", []):
            path = PACKAGE_DIR / row["path"]
            if not path.is_file():
                errors.append(f"manifest output missing: {row['path']}")
                continue
            if sha256(path) != row["sha256"]:
                errors.append(f"manifest hash mismatch: {row['path']}")
            if path.stat().st_size != row["bytes"]:
                errors.append(f"manifest byte-count mismatch: {row['path']}")
        for row in manifest.get("control_files", []):
            path = PACKAGE_DIR / row["path"]
            if not path.is_file():
                errors.append(f"manifest control file missing: {row['path']}")
                continue
            if sha256(path) != row["sha256"]:
                errors.append(f"manifest control-file hash mismatch: {row['path']}")
    else:
        errors.append("missing manifest_v1.json")

    validation_path = PACKAGE_DIR / "validation_report_v1.json"
    if not validation_path.is_file():
        errors.append("missing validation_report_v1.json")
    else:
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if validation.get("status") != "PASS":
            errors.append("validation_report_v1.json is not PASS")
        counts = validation.get("counts", {})
        if counts.get("confirmed_independent_multi_provider_groups") != 0:
            errors.append("confirmed independent multi-provider count changed from zero")
        if counts.get("eligible_endpoint_groups") != 11:
            errors.append("eligible endpoint group count changed from 11")

    register_path = PACKAGE_DIR / "unexpected_findings_register_v1.csv"
    if not register_path.is_file():
        errors.append("missing unexpected_findings_register_v1.csv")
    else:
        with register_path.open("r", encoding="utf-8-sig", newline="") as handle:
            register = list(csv.DictReader(handle))
        if len(register) != 8:
            errors.append(f"unexpected register row count is {len(register)}, expected 8")
        if any(row.get("workflow_status") != "lead_only" for row in register):
            errors.append("unexpected register contains a non-lead_only row")
        for field in (
            "claim_eligibility",
            "central_writeback",
            "human_review_trigger",
            "publication_eligibility",
        ):
            if any(row.get(field) != "no" for row in register):
                errors.append(f"unexpected register contains {field} other than no")

    audit_path = PACKAGE_DIR / "recurrent_recipient_audit_v1.csv"
    if not audit_path.is_file():
        errors.append("missing recurrent_recipient_audit_v1.csv")
    else:
        with audit_path.open("r", encoding="utf-8-sig", newline="") as handle:
            audit = list(csv.DictReader(handle))
        if len(audit) != 11:
            errors.append(f"endpoint audit row count is {len(audit)}, expected 11")
        if any(row.get("confirmed_independent_multi_provider") != "no" for row in audit):
            errors.append("endpoint audit contains a confirmed independent multi-provider row")
        if any(row.get("fact_status") != "lead_only" for row in audit):
            errors.append("endpoint audit contains a non-lead_only row")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "PASS: recurrent-recipient package hashes, manifest, text whitespace/EOF, "
        "lead-only gates and endpoint counts are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
