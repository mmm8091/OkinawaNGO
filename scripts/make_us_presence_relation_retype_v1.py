"""Build a no-new-facts crosswalk from the legacy 43-row relation sample.

The output proposes which US-presence multilayer table can receive each legacy
observation.  It never changes the central row, its review state, or its claim
status.  The mapping itself remains AI-seeded until the principal reviews it.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/interim/15_funding_or_support_edges_sample_v0.csv"
OUT = ROOT / "outputs/us_presence_relation_retype_v1"


MAPPING = {
    "donation": ("USN02", "money_flows", "direct_resource_transfer"),
    "sponsorship": ("USN02", "money_flows", "sponsorship_resource_flow"),
    "grant": ("USN02", "money_flows", "grant_resource_flow"),
    "aggregate_financial_history_observation": (
        "USN02",
        "money_flows",
        "aggregate_multi_recipient_observation",
    ),
    "in_kind_donation": ("USN04", "service_recipient", "in_kind_transfer"),
    "in_kind_acquisition_assistance": (
        "USN04",
        "service_recipient",
        "acquisition_assistance",
    ),
    "joint_in_kind_contribution": (
        "USN04",
        "service_recipient",
        "joint_in_kind_transfer",
    ),
    "network_membership": ("USN05", "affiliation_control", "umbrella_membership"),
    "organizational_affiliation": (
        "USN05",
        "affiliation_control",
        "organizational_affiliation",
    ),
    "legal_counsel": ("USN06", "action_institution", "case_specific_counsel"),
    "legal_support": ("USN06", "action_institution", "legal_support_role"),
    "commission": ("USN06", "action_institution", "public_commission_role"),
    "administrative_collaboration": (
        "USN06",
        "action_institution",
        "administrative_collaboration",
    ),
    "event_collaboration": (
        "USN06",
        "action_institution",
        "event_participation_or_role",
    ),
    "event_affiliation": (
        "USN06",
        "action_institution",
        "event_participation_or_role",
    ),
    "partner_action": ("USN06", "action_institution", "event_participation_or_role"),
    "coordination": ("USN06", "action_institution", "coordination_observation"),
    "partnership": ("USN06", "action_institution", "program_partnership_role"),
    "co_presence_observation": (
        "USN06",
        "action_institution",
        "co_presence_observation",
    ),
    "site_presence": ("USN06", "action_institution", "service_site_presence"),
    "service": ("USN06", "action_institution", "service_site_presence"),
    "grant_opportunity": ("LEAD", "research_lead", "opportunity_not_award"),
    "deprecated_nonrelation": ("EXCLUDE", "history_only", "rejected_duplicate"),
}


FIELDS = [
    "edge_id",
    "selection_frame_id",
    "mapping_rule_id",
    "source_actor_id",
    "target_actor_id",
    "original_relation_type",
    "original_review_status",
    "original_claim_status",
    "original_graph_eligibility",
    "proposed_usn_table_id",
    "proposed_table_name",
    "proposed_record_family",
    "mapping_review_status",
    "mapping_decision",
    "fact_status_carry_rule",
    "amount_gate",
    "endpoint_gate",
    "network_gate",
    "source_refs",
    "interpretation_limit",
]

RULE_ID_BY_TABLE = {
    "USN02": "USN-RT-R01",
    "USN04": "USN-RT-R02",
    "USN05": "USN-RT-R03",
    "USN06": "USN-RT-R04",
    "LEAD": "USN-RT-R05",
    "EXCLUDE": "USN-RT-R06",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def amount_gate(row: dict[str, str], table_id: str) -> str:
    if table_id != "USN02":
        return "not_applicable"
    if row["relation_type"] == "aggregate_financial_history_observation":
        return "retain_aggregate_semantics;do_not_attach_to_named_recipient"
    if row["amount"]:
        return "retain_amount_currency_and_amount_semantics;human_review_direction"
    return "relation_may_stand;amount_remains_unknown;do_not_impute_from_notes"


def endpoint_gate(row: dict[str, str], table_id: str) -> str:
    target = row["target_actor_id"]
    if table_id == "EXCLUDE":
        return "history_only"
    if target.startswith("unknown") or target.startswith("R_") or target.startswith("P_R10_"):
        return "retain_raw_endpoint;resolve_via_USN08_before_dyadic_graph"
    if target.startswith("P") or target in {
        "MOFA_ngo_consultant_program",
        "Okinawa_Pref_multicultural_project",
        "Okinawa_City",
    }:
        return "typed_non_actor_endpoint;never_promote_for_graph_convenience"
    return "registry_actor_endpoint_or_existing_label;identity_status_unchanged"


def network_gate(table_id: str, row: dict[str, str]) -> str:
    if table_id == "USN02":
        return "money_layer_only_after_direction_and_semantics_review"
    if table_id == "USN04":
        return "service_recipient_layer;no_alliance_projection"
    if table_id == "USN05":
        return "affiliation_layer;membership_not_control_or_funding"
    if table_id == "USN06":
        return "retain_case_event_program_or_place_node;no_co_participant_dyad"
    if table_id == "LEAD":
        return "off_graph_until_named_award_or_recipient_fact"
    return "excluded"


def build_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in source_rows:
        relation_type = row["relation_type"]
        if relation_type not in MAPPING:
            raise ValueError(f"Unmapped relation_type: {relation_type}")
        table_id, table_name, family = MAPPING[relation_type]
        output.append(
            {
                "edge_id": row["edge_id"],
                "selection_frame_id": "USF-EXISTING43-2026-08-19",
                "mapping_rule_id": RULE_ID_BY_TABLE[table_id],
                "source_actor_id": row["source_actor_id"],
                "target_actor_id": row["target_actor_id"],
                "original_relation_type": relation_type,
                "original_review_status": row["review_status"],
                "original_claim_status": row["claim_status"],
                "original_graph_eligibility": row["graph_eligibility"],
                "proposed_usn_table_id": table_id,
                "proposed_table_name": table_name,
                "proposed_record_family": family,
                "mapping_review_status": "ai_seeded",
                "mapping_decision": "",
                "fact_status_carry_rule": (
                    "preserve_original_fact_review_and_claim_axes;mapping_approval_does_not_upgrade_fact"
                ),
                "amount_gate": amount_gate(row, table_id),
                "endpoint_gate": endpoint_gate(row, table_id),
                "network_gate": network_gate(table_id, row),
                "source_refs": row["source_ref"],
                "interpretation_limit": (
                    "This row only proposes a semantic destination for an existing observation. "
                    "It adds no fact, relation, amount, endpoint identity, continuity, or function finding."
                ),
            }
        )
    return sorted(output, key=lambda item: item["edge_id"])


def main() -> None:
    source_rows = read_csv(INPUT)
    rows = build_rows(source_rows)
    if len(source_rows) != 43 or len(rows) != 43:
        raise ValueError("The central relation sample must remain exactly 43 rows")
    if len({row["edge_id"] for row in rows}) != 43:
        raise ValueError("edge_id must be unique")
    if any(row["mapping_decision"] for row in rows):
        raise ValueError("AI build must not fill principal mapping decisions")

    OUT.mkdir(parents=True, exist_ok=True)
    output_csv = OUT / "relation_retype_crosswalk_v1.csv"
    write_csv(output_csv, rows, FIELDS)

    counts = Counter(row["proposed_usn_table_id"] for row in rows)
    type_counts = Counter(row["original_relation_type"] for row in rows)
    summary_rows = [
        {"dimension": "target_table", "value": key, "count": str(value)}
        for key, value in sorted(counts.items())
    ] + [
        {"dimension": "original_relation_type", "value": key, "count": str(value)}
        for key, value in sorted(type_counts.items())
    ]
    summary_csv = OUT / "mapping_summary_v1.csv"
    write_csv(summary_csv, summary_rows, ["dimension", "value", "count"])

    rule_rows = []
    for table_id, rule_id in RULE_ID_BY_TABLE.items():
        matching = [row for row in rows if row["proposed_usn_table_id"] == table_id]
        rule_rows.append(
            {
                "mapping_rule_id": rule_id,
                "proposed_usn_table_id": table_id,
                "proposed_table_name": matching[0]["proposed_table_name"],
                "row_count": str(len(matching)),
                "edge_ids": ";".join(row["edge_id"] for row in matching),
                "decision": "",
                "principal_note_or_exceptions": "",
                "reviewer": "",
                "review_date": "",
            }
        )
    rule_csv = OUT / "HR_USN_relation_retype_rules_v1.csv"
    write_csv(
        rule_csv,
        rule_rows,
        [
            "mapping_rule_id",
            "proposed_usn_table_id",
            "proposed_table_name",
            "row_count",
            "edge_ids",
            "decision",
            "principal_note_or_exceptions",
            "reviewer",
            "review_date",
        ],
    )

    validation = {
        "input_rows": len(source_rows),
        "output_rows": len(rows),
        "unique_edge_ids": len({row["edge_id"] for row in rows}),
        "all_relation_types_mapped": set(type_counts) == set(MAPPING),
        "blank_principal_decisions": all(not row["mapping_decision"] for row in rows),
        "blank_rule_decisions": all(not row["decision"] for row in rule_rows),
        "mapping_rule_rows": len(rule_rows),
        "central_writeback": False,
        "target_table_counts": dict(sorted(counts.items())),
    }
    (OUT / "validation_report_v1.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest = {
        "package": "us_presence_relation_retype_v1",
        "generated_on": "2026-08-19",
        "status": "research_only_ai_seeded_mapping_no_new_facts",
        "input": {"path": str(INPUT.relative_to(ROOT)), "sha256": sha256(INPUT)},
        "outputs": {
            output_csv.name: {"rows": len(rows), "sha256": sha256(output_csv)},
            summary_csv.name: {"rows": len(summary_rows), "sha256": sha256(summary_csv)},
            rule_csv.name: {"rows": len(rule_rows), "sha256": sha256(rule_csv)},
        },
        "validation": validation,
    }
    readme = OUT / "README.md"
    if readme.exists():
        manifest["documentation"] = {
            "README.md": {"sha256": sha256(readme)},
        }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
