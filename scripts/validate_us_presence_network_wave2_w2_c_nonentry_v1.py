#!/usr/bin/env python3
"""Validate the bounded W2-C matched non-entry audit package.

This script never changes central facts or upstream W2-C files.  With
``--write-receipts`` it writes only the package-local validation report and
manifest.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_c_nonentry_v1"
TEMPLATE = ROOT / "data" / "metadata" / "unexpected_findings_register_template_v1.csv"

REQUIRED = {
    "README.md",
    "selection_rules_v1.csv",
    "candidate_screen_v1.csv",
    "selection_matching_table_v1.csv",
    "outcome_table_v1.csv",
    "arm_status_v1.csv",
    "gate_control_comparison_v1.csv",
    "negative_search_log_v1.csv",
    "source_receipts_v1.csv",
    "change_notes_v1.csv",
    "principal_checkpoint_v1.md",
    "unexpected_findings_register_v1.csv",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def validate() -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    checks: dict[str, object] = {}

    missing = sorted(name for name in REQUIRED if not (OUT / name).is_file())
    if missing:
        errors.append(f"missing required files: {missing}")
    checks["required_files_present"] = not missing
    if missing:
        return errors, checks

    readme = (OUT / "README.md").read_text(encoding="utf-8")
    checks["readme_scope"] = all(
        token in readme
        for token in ("research_only", "arm_not_established", "## 意外发现登记")
    )
    if not checks["readme_scope"]:
        errors.append("README scope/status/unexpected-findings section incomplete")

    arm_fields, arm_rows = read_csv(OUT / "arm_status_v1.csv")
    checks["arm_rows"] = len(arm_rows)
    if len(arm_rows) != 1 or arm_rows[0].get("status") != "arm_not_established":
        errors.append("arm_status must contain exactly one arm_not_established row")
    if arm_rows and arm_rows[0].get("admitted_rows") != "0":
        errors.append("arm_status admitted_rows must be 0")

    outcome_fields, outcome_rows = read_csv(OUT / "outcome_table_v1.csv")
    checks["outcome_rows"] = len(outcome_rows)
    if outcome_rows:
        errors.append("outcome_table must remain header-only when arm is not established")
    if not outcome_fields or "axis" not in outcome_fields:
        errors.append("outcome_table schema missing axis")

    _, candidates = read_csv(OUT / "candidate_screen_v1.csv")
    by_candidate = {row["candidate_id"]: row for row in candidates}
    checks["candidate_rows"] = len(candidates)
    c001 = by_candidate.get("W2CNE-C001", {})
    c002 = by_candidate.get("W2CNE-C002", {})
    if c001.get("admission_status") != "exclude_gate_control_only":
        errors.append("2004 mediation case must remain gate-control only")
    if c001.get("processing_observed") != "receipt_and_three_committee_meetings":
        errors.append("2004 mediation entry evidence is not preserved")
    if c002.get("admission_status") != "exclude_unmatched_and_source_gate":
        errors.append("2018 corporate refusal must remain excluded")

    _, controls = read_csv(OUT / "gate_control_comparison_v1.csv")
    if len(controls) != 1 or controls[0].get("gate_position") != "post_entry_pre_substantive_gate":
        errors.append("gate-control table must contain one post-entry/pre-substantive row")
    checks["gate_control_rows"] = len(controls)

    template_fields, _ = read_csv(TEMPLATE)
    register_fields, register_rows = read_csv(OUT / "unexpected_findings_register_v1.csv")
    checks["unexpected_findings_rows"] = len(register_rows)
    if register_fields != template_fields:
        errors.append("unexpected-findings register does not match 19-column template")
    if register_rows:
        errors.append("unexpected-findings register must be header-only in this package")

    scoped_files = [
        "selection_rules_v1.csv",
        "candidate_screen_v1.csv",
        "arm_status_v1.csv",
        "gate_control_comparison_v1.csv",
        "negative_search_log_v1.csv",
        "source_receipts_v1.csv",
    ]
    scoped_rows = 0
    for name in scoped_files:
        _, rows = read_csv(OUT / name)
        for row in rows:
            scoped_rows += 1
            if row.get("package_scope") != "research_only":
                errors.append(f"{name}: package_scope leak")
            if row.get("frontend_status") != "not_frontend_ready":
                errors.append(f"{name}: frontend status leak")
            if row.get("central_writeback") != "no":
                errors.append(f"{name}: central writeback leak")
    checks["scoped_rows_checked"] = scoped_rows

    _, receipts = read_csv(OUT / "source_receipts_v1.csv")
    verified = 0
    for row in receipts:
        artifact = row.get("artifact_path", "").strip()
        expected = row.get("sha256", "").strip()
        if not artifact:
            continue
        path = ROOT / artifact
        if not path.is_file():
            errors.append(f"missing receipt artifact: {artifact}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"receipt hash mismatch: {artifact}")
            continue
        verified += 1
    checks["receipt_artifact_hashes_verified"] = verified
    checks["receipt_rows"] = len(receipts)

    upstream = {
        ROOT / "outputs/us_presence_network_wave2_w2_c_v1/selected_episode_comparison_frame_v1.csv":
            "c75f46f02e14e8372284e5354215008f76d6f29ba0df012fc75b27aa78b1d868",
        ROOT / "outputs/us_presence_network_wave2_w2_c_v1/gate_control_frame_v1.csv":
            "9709ffaa5ede327075b42bc830982fd2ad05590631272648eb54357345c48863",
        ROOT / "outputs/us_presence_network_wave2_w2_c_v1/negative_search_log_v1.csv":
            "fe59fbf1396c40e50ca1d00604a899d047a841a33798fbe087ac9db87599ffa6",
    }
    for path, expected in upstream.items():
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"upstream W2-C drift: {path.relative_to(ROOT)}")
    checks["upstream_w2c_hashes_verified"] = len(upstream)

    checks["status"] = "PASS" if not errors else "FAIL"
    return errors, checks


def write_receipts(checks: dict[str, object]) -> None:
    report = {
        "package": "us_presence_network_wave2_w2_c_nonentry_v1",
        "validated_on": "2026-08-22",
        "status": checks.get("status"),
        "checks": checks,
        "interpretive_result": "arm_not_established",
        "central_writeback": "no",
        "frontend_status": "not_frontend_ready",
    }
    report_path = OUT / "validation_report_v1.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    entries = []
    for path in sorted(OUT.rglob("*")):
        if not path.is_file() or path.name == "manifest.json":
            continue
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "package": "us_presence_network_wave2_w2_c_nonentry_v1",
        "generated_on": "2026-08-22",
        "status": "research_only_arm_not_established",
        "files": entries,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipts", action="store_true")
    args = parser.parse_args()

    errors, checks = validate()
    if args.write_receipts and not errors:
        write_receipts(checks)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS us_presence_network_wave2_w2_c_nonentry_v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
