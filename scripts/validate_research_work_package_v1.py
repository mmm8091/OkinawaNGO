from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_COLUMNS = [
    "lead_id",
    "package_id",
    "record_kind",
    "chain_id",
    "parent_lead_id",
    "recon_step",
    "discovered_on",
    "lead_title",
    "observation",
    "why_unexpected",
    "source_or_query_locator",
    "next_test",
    "potential_value",
    "stop_reason",
    "workflow_status",
    "claim_eligibility",
    "central_writeback",
    "human_review_trigger",
    "publication_eligibility",
]

FIXED_VALUES = {
    "workflow_status": "lead_only",
    "claim_eligibility": "no",
    "central_writeback": "no",
    "human_review_trigger": "no",
    "publication_eligibility": "no",
}


def validate_package(package_dir: Path) -> list[str]:
    errors: list[str] = []
    readme = package_dir / "README.md"
    register = package_dir / "unexpected_findings_register_v1.csv"

    if not readme.is_file():
        errors.append(f"{package_dir}: missing README.md")
    elif "## 意外发现登记" not in readme.read_text(encoding="utf-8"):
        errors.append(f"{package_dir}: README lacks '## 意外发现登记'")

    if not register.is_file():
        errors.append(f"{package_dir}: missing unexpected_findings_register_v1.csv")
        return errors

    with register.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        if columns != REQUIRED_COLUMNS:
            errors.append(
                f"{register}: columns differ from required template; "
                f"expected {REQUIRED_COLUMNS}, got {columns}"
            )
            return errors
        rows = list(reader)

    if len(rows) > 10:
        errors.append(f"{register}: {len(rows)} observations exceed per-package maximum 10")

    by_id: dict[str, dict[str, str]] = {}
    steps: dict[str, int] = {}
    package_ids = {row["package_id"].strip() for row in rows}
    if "" in package_ids:
        errors.append(f"{register}: package_id must not be blank")
    if len(package_ids - {""}) > 1:
        errors.append(f"{register}: contains more than one package_id: {sorted(package_ids)}")

    for line_number, row in enumerate(rows, start=2):
        lead_id = row["lead_id"].strip()
        if not lead_id:
            errors.append(f"{register}:{line_number}: lead_id must not be blank")
            continue
        if lead_id in by_id:
            errors.append(f"{register}:{line_number}: duplicate lead_id {lead_id}")
        by_id[lead_id] = row

        kind = row["record_kind"].strip()
        if kind not in {"origin_observation", "followup_observation"}:
            errors.append(f"{register}:{line_number}: invalid record_kind {kind!r}")

        try:
            step = int(row["recon_step"])
        except ValueError:
            errors.append(f"{register}:{line_number}: recon_step must be an integer")
            continue
        steps[lead_id] = step
        if not 0 <= step <= 3:
            errors.append(f"{register}:{line_number}: recon_step {step} outside 0..3")
        if kind == "origin_observation" and (step != 0 or row["parent_lead_id"].strip()):
            errors.append(
                f"{register}:{line_number}: origin_observation requires step 0 and blank parent"
            )
        if kind == "followup_observation" and (step == 0 or not row["parent_lead_id"].strip()):
            errors.append(
                f"{register}:{line_number}: followup_observation requires step 1..3 and a parent"
            )

        for field, expected in FIXED_VALUES.items():
            if row[field].strip() != expected:
                errors.append(
                    f"{register}:{line_number}: {field} must be {expected!r}, "
                    f"got {row[field].strip()!r}"
                )
        for field in (
            "chain_id",
            "discovered_on",
            "lead_title",
            "observation",
            "why_unexpected",
            "source_or_query_locator",
            "next_test",
            "potential_value",
        ):
            if not row[field].strip():
                errors.append(f"{register}:{line_number}: {field} must not be blank")

    for lead_id, row in by_id.items():
        if row["record_kind"].strip() != "followup_observation":
            continue
        parent_id = row["parent_lead_id"].strip()
        parent = by_id.get(parent_id)
        if parent is None:
            errors.append(f"{register}: {lead_id} references missing parent {parent_id}")
            continue
        if lead_id not in steps or parent_id not in steps:
            continue
        if row["chain_id"].strip() != parent["chain_id"].strip():
            errors.append(f"{register}: {lead_id} and parent {parent_id} have different chain_id")
        if steps[lead_id] != steps[parent_id] + 1:
            errors.append(
                f"{register}: {lead_id} step must be exactly one greater than parent {parent_id}"
            )

    parent_ids = {
        row["parent_lead_id"].strip()
        for row in by_id.values()
        if row["record_kind"].strip() == "followup_observation"
        and row["parent_lead_id"].strip()
    }
    for lead_id, row in by_id.items():
        if lead_id not in parent_ids and not row["stop_reason"].strip():
            errors.append(f"{register}: terminal observation {lead_id} requires stop_reason")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the mandatory unexpected-findings register for research packages."
    )
    parser.add_argument("package_dirs", nargs="+", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    for package_dir in args.package_dirs:
        errors.extend(validate_package(package_dir.resolve()))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(args.package_dirs)} research work package(s) satisfy lead-only protocol")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
