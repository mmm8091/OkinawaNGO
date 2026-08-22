from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "outputs" / "us_presence_network_wave2_leg2_originals_v1"

REQUIRED_FILES = [
    "README.md",
    "source_receipts_v1.csv",
    "endpoint_action_crosswalk_v1.csv",
    "response_evidence_excerpts_v1.csv",
    "competing_interpretations_v1.csv",
    "negative_search_log_v1.csv",
    "principal_review_queue_v1.csv",
    "principal_checkpoint_v1.md",
    "unexpected_findings_register_v1.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    checks: dict[str, object] = {}

    for name in REQUIRED_FILES:
        if not (PACKAGE / name).is_file():
            errors.append(f"missing required file: {name}")

    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1

    receipts = read_csv("source_receipts_v1.csv")
    endpoints = read_csv("endpoint_action_crosswalk_v1.csv")
    responses = read_csv("response_evidence_excerpts_v1.csv")
    review = read_csv("principal_review_queue_v1.csv")

    receipt_ids = {row["receipt_id"] for row in receipts}
    endpoint_ids = {row["endpoint_action_id"] for row in endpoints}

    if len(endpoints) != 4:
        errors.append(f"expected exactly 4 frozen endpoints, got {len(endpoints)}")
    if len(endpoint_ids) != len(endpoints):
        errors.append("duplicate endpoint_action_id")

    artifact_manifest: list[dict[str, object]] = []
    for row in receipts:
        artifact = ROOT / row["artifact_path"]
        if not artifact.is_file():
            errors.append(f"{row['receipt_id']}: missing artifact {row['artifact_path']}")
            continue
        actual = sha256(artifact)
        if actual.lower() != row["sha256"].lower():
            errors.append(
                f"{row['receipt_id']}: sha256 mismatch {actual} != {row['sha256']}"
            )
        artifact_manifest.append(
            {
                "receipt_id": row["receipt_id"],
                "path": row["artifact_path"],
                "bytes": artifact.stat().st_size,
                "sha256": actual,
            }
        )

    for row in responses:
        if row["endpoint_action_id"] not in endpoint_ids:
            errors.append(
                f"{row['response_evidence_id']}: unknown endpoint {row['endpoint_action_id']}"
            )
        for receipt_id in filter(None, row["source_receipt_ids"].split(";")):
            if receipt_id not in receipt_ids:
                errors.append(
                    f"{row['response_evidence_id']}: unknown receipt {receipt_id}"
                )
        if row["fact_status"] != "research_only":
            errors.append(f"{row['response_evidence_id']}: fact_status must be research_only")
        if row["leg3_evidence"] != "no":
            errors.append(f"{row['response_evidence_id']}: LEG3 must remain no")
        if row["response_source_role"] == "provider_original":
            errors.append(
                f"{row['response_evidence_id']}: provider material cannot be recipient response"
            )

    if any(row["fact_status"] != "research_only" for row in endpoints):
        errors.append("all endpoint rows must remain research_only")

    allowed_hr = {"HR-USN2-04a", "HR-USN2-04b", "HR-USN2-04c", "HR-USN2-05", "HR-USN2-06b"}
    for row in review:
        if row["existing_hr_item"] not in allowed_hr:
            errors.append(
                f"{row['review_input_id']}: creates or references unexpected HR item {row['existing_hr_item']}"
            )
        if row["review_status"] != "awaiting_principal":
            errors.append(
                f"{row['review_input_id']}: review_status must be awaiting_principal"
            )

    package_files = []
    for path in sorted(PACKAGE.rglob("*")):
        if not path.is_file() or path.name in {"manifest_v1.json", "validation_report_v1.json"}:
            continue
        package_files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    manifest = {
        "package_id": "us_presence_network_wave2_leg2_originals_v1",
        "status": "research_only",
        "generated_on": "2026-08-22",
        "scope": "four frozen recipient/local-response endpoints",
        "files": package_files,
    }
    (PACKAGE / "manifest_v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    checks.update(
        {
            "required_files": len(REQUIRED_FILES),
            "source_receipts": len(receipts),
            "archived_artifacts": len(artifact_manifest),
            "frozen_endpoints": len(endpoints),
            "response_evidence_rows": len(responses),
            "principal_review_inputs": len(review),
            "all_response_rows_research_only": all(
                row["fact_status"] == "research_only" for row in responses
            ),
            "all_leg3_evidence_no": all(row["leg3_evidence"] == "no" for row in responses),
            "provider_news_as_recipient_response": any(
                row["response_source_role"] == "provider_original" for row in responses
            ),
            "existing_hr_only": all(row["existing_hr_item"] in allowed_hr for row in review),
        }
    )
    report = {
        "package_id": "us_presence_network_wave2_leg2_originals_v1",
        "status": "PASS" if not errors else "FAIL",
        "research_status": "research_only",
        "checks": checks,
        "errors": errors,
        "boundaries": [
            "No W2-F synthesis, central writeback, publication adapter or frontend release.",
            "Recipient/local-response evidence does not establish LEG3 legitimacy effects.",
            "Kana-san, Ambitious and Himawari local materials do not close their referenced AWWA Form 990 rows.",
            "Marine Thrift Shop to Lions remains provider-to-intermediary only.",
        ],
    }
    (PACKAGE / "validation_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    print(
        "PASS: 4 frozen endpoints; "
        f"{len(responses)} response rows; {len(receipts)} archived source receipts; research_only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
