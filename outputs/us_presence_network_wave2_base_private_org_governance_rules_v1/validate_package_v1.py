from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


PACKAGE_ID = "us_presence_network_wave2_base_private_org_governance_rules_v1"
ROOT = Path(__file__).resolve().parent

EXPECTED_FILES = {
    "README.md",
    "selection_frame_v1.csv",
    "source_receipts_v1.csv",
    "public_rule_facts_v1.csv",
    "governance_relation_grammar_v1.csv",
    "regime_comparison_matrix_v1.csv",
    "bounded_report_claims_v1.csv",
    "lead_promotion_crosswalk_v1.csv",
    "scope_exclusions_v1.csv",
    "local_artifact_manifest_v1.csv",
    "unexpected_findings_register_v1.csv",
    "validate_package_v1.py",
    "artifacts/kadena_18fss_oi_34_223_1_20240205.pdf",
}

EXPECTED_COUNTS = {
    "selection_frame_v1.csv": 1,
    "source_receipts_v1.csv": 2,
    "public_rule_facts_v1.csv": 25,
    "governance_relation_grammar_v1.csv": 9,
    "regime_comparison_matrix_v1.csv": 10,
    "bounded_report_claims_v1.csv": 6,
    "lead_promotion_crosswalk_v1.csv": 10,
    "scope_exclusions_v1.csv": 5,
    "local_artifact_manifest_v1.csv": 1,
    "unexpected_findings_register_v1.csv": 0,
}

ALLOWED_RELATION_TYPES = {
    "legal_status_boundary",
    "installation_authorization",
    "administrative_monitoring",
    "compliance_reporting",
    "sanction_authority",
    "facility_license_requirement",
    "reimbursable_support_terms",
    "continuous_resale_exception",
    "private_liability_boundary",
}


def read_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def validate_text_file(path: Path, errors: list[str]) -> None:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{path.relative_to(ROOT)}: UTF-8 BOM is not allowed")
    if b"\r\n" in data or b"\r" in data:
        errors.append(f"{path.relative_to(ROOT)}: non-LF line ending detected")
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        errors.append(f"{path.relative_to(ROOT)}: expected exactly one LF at EOF")
    for line_no, line in enumerate(data.splitlines(), start=1):
        if line.endswith((b" ", b"\t")):
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: trailing whitespace")


def main() -> int:
    errors: list[str] = []

    for relative in sorted(EXPECTED_FILES):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    rows_by_file = {name: read_rows(name) for name in EXPECTED_COUNTS}
    for name, expected in EXPECTED_COUNTS.items():
        actual = len(rows_by_file[name])
        if actual != expected:
            errors.append(f"{name}: expected {expected} rows, got {actual}")

    facts = rows_by_file["public_rule_facts_v1.csv"]
    fact_ids = [row.get("fact_id", "") for row in facts]
    if len(set(fact_ids)) != len(fact_ids):
        errors.append("public_rule_facts_v1.csv: duplicate fact_id")
    regime_counts = Counter(row.get("regime_id", "") for row in facts)
    if regime_counts != Counter({"BGR-RG01": 14, "BGR-RG02": 11}):
        errors.append(f"public_rule_facts_v1.csv: regime counts are {dict(regime_counts)}")

    source_ids = {row["source_id"] for row in rows_by_file["source_receipts_v1.csv"]}
    grammar_types = {
        row["relation_type"] for row in rows_by_file["governance_relation_grammar_v1.csv"]
    }
    if grammar_types != ALLOWED_RELATION_TYPES:
        errors.append(
            "governance_relation_grammar_v1.csv: relation vocabulary differs from approved set"
        )

    for row in facts:
        fact_id = row.get("fact_id", "<blank>")
        if row.get("relation_type") not in ALLOWED_RELATION_TYPES:
            errors.append(f"{fact_id}: invalid relation_type {row.get('relation_type')!r}")
        if row.get("source_id") not in source_ids:
            errors.append(f"{fact_id}: unknown source_id {row.get('source_id')!r}")
        expected = {
            "evidence_level": "E4",
            "review_status": "ai_seeded",
            "claim_status": "supported_bounded",
            "network_metric_eligibility": "not_eligible",
            "package_scope": "research_only",
            "frontend_status": "not_frontend_ready",
            "central_writeback": "no",
        }
        for field, value in expected.items():
            if row.get(field) != value:
                errors.append(f"{fact_id}: {field} must be {value!r}")
        if row.get("human_decision"):
            errors.append(f"{fact_id}: human_decision must remain blank")
        if row.get("graph_eligibility") != "administrative_record":
            errors.append(f"{fact_id}: illegal graph_eligibility")
        for field in ("confirmed_scope", "missing_scope", "interpretation_limit", "locator"):
            if not row.get(field, "").strip():
                errors.append(f"{fact_id}: {field} must not be blank")

    f021 = next((row for row in facts if row.get("fact_id") == "BGR-F021"), None)
    f022 = next((row for row in facts if row.get("fact_id") == "BGR-F022"), None)
    f025 = next((row for row in facts if row.get("fact_id") == "BGR-F025"), None)
    if not f021 or f021.get("object_actor_id") != "X006":
        errors.append("BGR-F021 must preserve the exact KOSC X006 crosswalk")
    if not f022 or f022.get("object_actor_id"):
        errors.append("BGR-F022 must keep Kadena Enlisted entity unresolved")
    if any(row.get("object_actor_id") == "X007" for row in facts):
        errors.append("X007 must not inherit the Kadena Enlisted resale authorization")
    if not f025 or "Dissolution of the PO" not in f025.get("rule_summary", ""):
        errors.append("BGR-F025 must preserve the exact fourth-occurrence 'Dissolution of the PO' wording")
    if f025 and "do not reduce it to operating-status revocation" not in f025.get(
        "interpretation_limit", ""
    ):
        errors.append("BGR-F025 must not reduce dissolution to operating-status revocation")
    if f025 and not all(
        phrase in f025.get("missing_scope", "")
        for phrase in ("actual execution", "legal effect outside installation")
    ):
        errors.append("BGR-F025 must leave actual execution and outside-installation legal effect unresolved")

    grammar_rows = rows_by_file["governance_relation_grammar_v1.csv"]
    for row in grammar_rows:
        grammar_id = row.get("grammar_id", "<blank>")
        if row.get("graph_eligibility") != "administrative_record":
            errors.append(f"{grammar_id}: grammar cannot create a dyadic organization edge")
        if row.get("network_metric_eligibility") != "not_eligible":
            errors.append(f"{grammar_id}: network metrics must remain ineligible")
        if row.get("funding_relation_confidence") != "not_funding_relation":
            errors.append(f"{grammar_id}: must be explicitly non-funding")
        if row.get("relation_type") in {"funding", "affiliation", "governance_control"}:
            errors.append(f"{grammar_id}: prohibited collapsed relation type")

    g05 = next((row for row in grammar_rows if row.get("grammar_id") == "BGR-G05"), None)
    if not g05 or "Dissolution of the PO" not in g05.get("allowed_statement", ""):
        errors.append("BGR-G05 must preserve the rule's exact dissolution wording")
    if g05 and not all(
        phrase in g05.get("forbidden_inference", "")
        for phrase in ("Do not reduce", "actual dissolution", "legal-entity extinction")
    ):
        errors.append("BGR-G05 must prohibit both semantic reduction and unsupported juridical expansion")

    comparisons = rows_by_file["regime_comparison_matrix_v1.csv"]
    c06 = next((row for row in comparisons if row.get("comparison_id") == "BGR-C06"), None)
    if not c06 or "Dissolution of the PO" not in c06.get("Kadena_rule", ""):
        errors.append("BGR-C06 must preserve the Kadena fourth-occurrence wording")
    if c06 and "legal effect outside installation" not in c06.get("missing_scope", ""):
        errors.append("BGR-C06 must leave outside-installation legal effect unresolved")

    claims = rows_by_file["bounded_report_claims_v1.csv"]
    for row in claims:
        claim_id = row.get("claim_id", "<blank>")
        expected = {
            "claim_status": "supported_bounded",
            "review_status": "ai_seeded",
            "report_use_status": "internal_report_candidate",
            "package_scope": "research_only",
            "frontend_status": "not_frontend_ready",
            "central_writeback": "no",
        }
        for field, value in expected.items():
            if row.get(field) != value:
                errors.append(f"{claim_id}: {field} must be {value!r}")
        if row.get("human_decision"):
            errors.append(f"{claim_id}: human_decision must remain blank")
        for fact_id in filter(None, row.get("fact_ids", "").split(";")):
            if fact_id not in set(fact_ids):
                errors.append(f"{claim_id}: unknown fact reference {fact_id}")
        for source_id in filter(None, row.get("source_ids", "").split(";")):
            if source_id not in source_ids:
                errors.append(f"{claim_id}: unknown source reference {source_id}")
        for field in ("confirmed_scope", "missing_scope", "interpretation_limit", "disconfirming_evidence"):
            if not row.get(field, "").strip():
                errors.append(f"{claim_id}: {field} must not be blank")

    cl002 = next((row for row in claims if row.get("claim_id") == "BGR-CL002"), None)
    if not cl002 or "Dissolution of the PO" not in cl002.get("report_candidate_text", ""):
        errors.append("BGR-CL002 must preserve the exact dissolution wording")
    if cl002 and not all(
        phrase in cl002.get("interpretation_limit", "")
        for phrase in ("Do not reduce", "observed dissolution", "legal-entity extinction")
    ):
        errors.append("BGR-CL002 must prohibit both semantic reduction and unsupported juridical expansion")

    crosswalk = rows_by_file["lead_promotion_crosswalk_v1.csv"]
    by_lead = {row["lead_id"]: row for row in crosswalk}
    for lead_id in ("UF-BPG-003", "UF-BPG-004", "UF-BPG-005", "UF-BPG-006", "UF-BPG-007"):
        if by_lead.get(lead_id, {}).get("lead_status_after_promotion") != "lead_only":
            errors.append(f"{lead_id}: unpromoted retrieval/transaction scope must remain lead_only")

    exclusions = {row["exclusion_id"]: row for row in rows_by_file["scope_exclusions_v1.csv"]}
    if exclusions.get("BGR-X002", {}).get("does_not_block_package") != "yes":
        errors.append("BGR-X002: administrative-record retrieval must not block this package")

    lead_rows = rows_by_file["unexpected_findings_register_v1.csv"]
    if lead_rows:
        errors.append("unexpected_findings_register_v1.csv must remain header-only for this package")

    artifact = ROOT / "artifacts/kadena_18fss_oi_34_223_1_20240205.pdf"
    expected_hash = "DE86FABE38283F250FCB2547A5190E9A93DB128728C3094EFEDD9C595CD6EB61"
    if sha256(artifact) != expected_hash:
        errors.append("Kadena PDF hash mismatch")
    if not artifact.read_bytes().startswith(b"%PDF"):
        errors.append("Kadena artifact does not have PDF magic")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in (
        "## 意外发现登记",
        "不把取得这些材料写成交付预期，也不以其缺失阻断本包",
        "没有发送信息公开请求",
        "不生成组织—组织边",
    ):
        if phrase not in readme:
            errors.append(f"README.md: missing boundary phrase {phrase!r}")

    for relative in sorted(EXPECTED_FILES):
        path = ROOT / relative
        if path.suffix.lower() in {".md", ".csv", ".py"}:
            validate_text_file(path, errors)

    manifest_files = []
    for relative in sorted(EXPECTED_FILES):
        path = ROOT / relative
        manifest_files.append(
            {
                "path": relative.replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    status = "PASS" if not errors else "FAIL"
    now = "2026-08-22"
    manifest = {
        "package_id": PACKAGE_ID,
        "schema_version": "BGR-1.0.0",
        "generated_at": now,
        "status": "research_only",
        "review_status": "ai_seeded",
        "frontend_status": "not_frontend_ready",
        "central_writeback": "no",
        "files": manifest_files,
    }
    report = {
        "package_id": PACKAGE_ID,
        "validated_at": now,
        "status": status,
        "counts": {
            "selection_frames": len(rows_by_file["selection_frame_v1.csv"]),
            "sources": len(rows_by_file["source_receipts_v1.csv"]),
            "rule_facts": len(facts),
            "mcipac_facts": regime_counts.get("BGR-RG01", 0),
            "kadena_facts": regime_counts.get("BGR-RG02", 0),
            "relation_grammars": len(rows_by_file["governance_relation_grammar_v1.csv"]),
            "comparison_units": len(rows_by_file["regime_comparison_matrix_v1.csv"]),
            "bounded_report_claims": len(claims),
            "scope_exclusions": len(rows_by_file["scope_exclusions_v1.csv"]),
            "unexpected_findings": len(lead_rows),
        },
        "checks": {
            "no_dyadic_org_edges": not any(
                row.get("graph_eligibility") == "dyadic_relation" for row in facts
            ),
            "no_government_funder_or_control_type": not any(
                row.get("relation_type") in {"funding", "affiliation", "governance_control"}
                for row in facts
            ),
            "records_retrieval_remains_lead_only": by_lead.get("UF-BPG-003", {}).get(
                "lead_status_after_promotion"
            )
            == "lead_only",
            "unexpected_register_empty": len(lead_rows) == 0,
            "kadena_pdf_hash_verified": sha256(artifact) == expected_hash,
            "kadena_dissolution_wording_preserved": bool(
                f025
                and g05
                and c06
                and cl002
                and all(
                    "Dissolution of the PO" in value
                    for value in (
                        f025.get("rule_summary", ""),
                        g05.get("allowed_statement", ""),
                        c06.get("Kadena_rule", ""),
                        cl002.get("report_candidate_text", ""),
                    )
                )
            ),
            "kadena_external_legal_effect_unresolved": bool(
                f025
                and c06
                and "legal effect outside installation" in f025.get("missing_scope", "")
                and "legal effect outside installation" in c06.get("missing_scope", "")
            ),
        },
        "errors": errors,
    }

    (ROOT / "manifest_v1.json").write_bytes(
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    (ROOT / "validation_report_v1.json").write_bytes(
        (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "PASS: 25 official-rule facts, 9 relation grammars, 10 comparison units, "
        "6 bounded claims; central/publication/frontend remain untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
