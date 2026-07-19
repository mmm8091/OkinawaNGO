from __future__ import annotations

"""Synchronize HR-018 decisions into the central relation/support sample.

R10 remains the authoritative normalized administrative layer. This script
only repairs eleven pre-existing F rows whose older wording or status would
otherwise contradict the completed HR-018 review. It does not add R10
relations to the F sample and it treats the six HR-033 rows as immutable.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENTRAL = Path("data/interim/15_funding_or_support_edges_sample_v0.csv")
R10_RELATIONS = Path("data/interim/21_admin_collaboration_relations_v0.csv")
HR018_QUEUE = Path(
    "outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv"
)
OUT = Path("outputs/hr018_main_relation_sync_v1")

PROTECTED_HR033 = {"F006", "F007", "F021", "F022", "F023", "F025"}

EXTRA_FIELDS = [
    "hr018_relation_observation_ids",
    "temporal_status",
    "observed_active_at",
    "current_status",
    "target_display_name",
    "target_identity_status",
    "target_operator",
    "historical_target_label",
    "possible_locator_candidate",
    "locator_approved",
    "local_context",
    "support_types",
    "sponsor_tier",
    "reported_at",
]

OBSERVATION_MAP = {
    "F024": ["R10R028"],
    "F027": ["R10R030"],
    "F028": ["R10R031"],
    "F029": ["R10R032"],
    "F030": ["R10R033"],
    "F031": ["R10R006", "R10R007"],
    "F032": ["R10R005"],
    "F033": ["R10R002", "R10R003", "R10R004"],
    "F034": ["R10R020"],
    "F035": ["R10R021"],
    "F036": ["R10R034"],
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ensure_fields(fields: list[str], additions: list[str]) -> list[str]:
    return fields + [field for field in additions if field not in fields]


def unique_index(
    rows: list[dict[str, str]], key: str
) -> dict[str, dict[str, str]]:
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate {key}")
    return result


def joined(rows: list[dict[str, str]], field: str) -> str:
    values: list[str] = []
    for row in rows:
        value = row.get(field, "").strip()
        if value and value not in values:
            values.append(value)
    return ";".join(values)


def common_review_update(
    edge: dict[str, str],
    observations: list[dict[str, str]],
    queue_by_relation: dict[str, dict[str, str]],
) -> None:
    relation_ids = [row["relation_observation_id"] for row in observations]
    queue_rows = [queue_by_relation[relation_id] for relation_id in relation_ids]
    statuses = {row["review_status"] for row in observations}
    if len(statuses) != 1:
        raise ValueError(f"mixed review status for {edge['edge_id']}: {statuses}")
    status = next(iter(statuses))
    human_decisions = {
        row["human_decision"] for row in observations if row["human_decision"]
    }
    if status == "needs_local_retrieval":
        human_decision = "defer"
    elif "revise" in human_decisions:
        human_decision = "revise"
    else:
        human_decision = "accept"

    edge.update(
        {
            "review_status": status,
            "human_decision": human_decision,
            "review_task_id": joined(queue_rows, "review_item_id"),
            "human_reviewer": "project_principal_user",
            "review_date": "2026-07-20",
            "review_scope": (
                "relation_existence;endpoint_identity;time_period;"
                "amount_semantics;interpretation_boundary"
            ),
            "reviewed_fields": (
                "relation_type;event_or_program;review_status;claim_status;"
                "graph_eligibility;amount;amount_semantics;event_date;"
                "interpretation_limit"
            ),
            "hr018_relation_observation_ids": ";".join(relation_ids),
            "interpretation_limit": joined(
                observations, "interpretation_limit"
            ),
        }
    )


def apply_specific_updates(edge: dict[str, str]) -> None:
    edge_id = edge["edge_id"]
    if edge_id == "F031":
        edge.update(
            {
                "event_or_program": (
                    "ONC as MOFA-designated NGO consultant "
                    "(FY2024 commission; FY2026 designation continuity)"
                ),
                "review_status": "human_checked",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "MOFA commission in FY2024 and official designated-role "
                    "continuity in FY2026."
                ),
                "missing_scope": "A public contract/payment amount is not available.",
                "graph_eligibility": "administrative_record",
                "source_role": "commissioned_organization",
                "target_role": "public_program",
                "amount": "",
                "currency": "",
                "amount_semantics": "organization_project_cost_not_payment",
                "observed_active_at": "FY2024;FY2026",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018: ONC's MOFA NGO consultant role is confirmed. "
                    "JPY 2,894,630 is an organization-side project-category cost, "
                    "not a contract payment."
                ),
            }
        )
    elif edge_id == "F032":
        edge.update(
            {
                "event_or_program": (
                    "Okinawa Prefecture multicultural policy-conference "
                    "support commission FY2024"
                ),
                "review_status": "human_checked",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "FY2024 prefectural commission and attached secretariat role."
                ),
                "missing_scope": (
                    "The two public project-cost observations are not a "
                    "contract/payment amount."
                ),
                "graph_eligibility": "administrative_record",
                "source_role": "commissioned_organization",
                "target_role": "prefectural_program",
                "amount": "",
                "currency": "",
                "amount_semantics": "whole_program_project_cost_not_actor_payment",
                "observed_active_at": "FY2024",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018: the commission and secretariat function are confirmed; "
                    "JPY 5.140m and 5.530234m are separate project-cost observations, "
                    "not contract/payment amounts."
                ),
            }
        )
    elif edge_id == "F033":
        edge.update(
            {
                "event_or_program": (
                    "Okinawa City Koza International Plaza management commissions "
                    "(FY2019, FY2020 and FY2024 observations)"
                ),
                "review_status": "human_checked",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "Named ONC commission flows are confirmed for FY2019, FY2020 "
                    "and FY2024 in the normalized R10 amount layer."
                ),
                "missing_scope": (
                    "This summary edge does not carry one amount across multiple "
                    "fiscal years."
                ),
                "graph_eligibility": "administrative_record",
                "source_role": "commissioned_organization",
                "target_role": "municipal_facility_program",
                "amount": "",
                "currency": "",
                "amount_semantics": (
                    "multi_year_named_commission_flows_in_R10_amount_table"
                ),
                "observed_active_at": "FY2019;FY2020;FY2024",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018: annual named commission flows and parallel project "
                    "costs are kept separately in R10; this summary edge must not "
                    "collapse them into one payment."
                ),
            }
        )
    elif edge_id == "F034":
        edge.update(
            {
                "event_or_program": "MBC Okinawa — USO Okinawa Platinum Sponsor",
                "review_status": "human_checked",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "Mediatti Broadband Communications, Inc. is publicly listed "
                    "as a current USO Okinawa Platinum Sponsor."
                ),
                "missing_scope": (
                    "Relation amount, cash/in-kind split and registry actor "
                    "crosswalk are not available."
                ),
                "graph_eligibility": "research_lead",
                "source_role": "corporate_sponsor_provisional",
                "target_role": "sponsored_service_organization",
                "amount": "",
                "currency": "",
                "amount_semantics": "sponsor_tier_and_support_types_no_amount",
                "target_display_name": "USO Okinawa",
                "support_types": "cash_and_in_kind_unvalued",
                "sponsor_tier": "Platinum Sponsor",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018: sponsor tier and support types are confirmed; no "
                    "amount is inferred and no base-policy stance is assigned."
                ),
            }
        )
    elif edge_id == "F035":
        edge.update(
            {
                "target_actor_id": "P_R10_USO_INDO_PACIFIC",
                "event_or_program": "Matson — USO Indo-Pacific Mission Partner",
                "review_status": "human_revised",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "Matson is a publicly listed USO Indo-Pacific Mission Partner."
                ),
                "missing_scope": (
                    "No amount or Okinawa-specific allocation is publicly stated; "
                    "endpoints remain provisional for actor graphing."
                ),
                "graph_eligibility": "research_lead",
                "source_role": "regional_sponsor_provisional",
                "target_role": "regional_USO_program_provisional",
                "amount": "",
                "currency": "",
                "amount_semantics": "sponsor_tier_no_amount_or_local_allocation",
                "target_display_name": "USO Indo-Pacific",
                "local_context": "listed_on_USO_Okinawa_sponsor_page",
                "sponsor_tier": "Mission Partner",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018 revision: this is a regional USO Indo-Pacific sponsor "
                    "relation, not proof of locally directed funding to USO Okinawa."
                ),
            }
        )
    elif edge_id == "F024":
        edge.update(
            {
                "event_or_program": (
                    "Army Community Group of Okinawa as historical AWWA member"
                ),
                "review_status": "human_revised",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "ACGO is listed as an AWWA member in 2012 and 2015 sources."
                ),
                "missing_scope": (
                    "Exact exit date and current organization continuity remain "
                    "unconfirmed."
                ),
                "graph_eligibility": "dyadic_relation",
                "source_role": "umbrella_network",
                "target_role": "historical_member",
                "amount": "",
                "currency": "",
                "amount_semantics": "not_funding_relation",
                "temporal_status": "historical_membership",
                "observed_active_at": "2012;2015",
                "current_status": "not_listed_on_current_AWWA_member_page",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018 revision: historical membership is confirmed at two "
                    "observed dates. Current non-listing is not a dissolution or "
                    "precise exit-date finding."
                ),
            }
        )
    elif edge_id == "F027":
        edge.update(
            {
                "relation_type": "aggregate_history",
                "review_status": "needs_local_retrieval",
                "human_decision": "defer",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "A source reports approximately JPY 800 million in aggregate "
                    "AWWA support over roughly 40 years."
                ),
                "missing_scope": (
                    "Annual values and named-recipient allocation require annual "
                    "reports, Form 990 or equivalent records."
                ),
                "graph_eligibility": "aggregate_observation",
                "source_role": "aggregate_donor",
                "target_role": "unresolved_recipient_universe",
                "amount": "800000000",
                "currency": "JPY",
                "amount_semantics": (
                    "approximate_40_year_aggregate_no_recipient_or_year_allocation"
                ),
                "funding_relation_confidence": "confirmed_contribution",
                "needs_local_retrieval": "yes",
                "notes": (
                    "HR-018 deferred decomposition: the approximate forty-year "
                    "aggregate cannot be assigned to a year or recipient and does "
                    "not enter the organization relation graph."
                ),
            }
        )
    elif edge_id == "F028":
        edge.update(
            {
                "event_or_program": (
                    "Wheelchair-accessible van donated to よみたん救護園"
                ),
                "review_status": "human_revised",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "AWWA donated one wheelchair-accessible van valued at "
                    "JPY 2,000,000 on 2015-12-02."
                ),
                "missing_scope": (
                    "Item value is not cash/payment and does not establish "
                    "continuing support."
                ),
                "graph_eligibility": "administrative_record",
                "source_role": "in_kind_donor",
                "target_role": "recipient_welfare_facility",
                "amount": "2000000",
                "currency": "JPY",
                "amount_semantics": "in_kind_item_value_not_cash",
                "event_date": "2015-12-02",
                "target_display_name": "よみたん救護園",
                "target_identity_status": "facility_identity_confirmed",
                "target_operator": "社会福祉法人沖縄県社会福祉事業団",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018 revision: the recipient facility and operator are "
                    "crosswalked; JPY 2m is the van's in-kind value, not cash."
                ),
            }
        )
    elif edge_id == "F029":
        edge.update(
            {
                "event_or_program": (
                    "Wheelchair-accessible van donated to "
                    "社会福祉法人うるま市社会福祉協議会"
                ),
                "review_status": "human_revised",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "A 2012 source confirms an accessible-van donation to the "
                    "named social welfare council."
                ),
                "missing_scope": (
                    "The specific subordinate facility and item value are not "
                    "identified."
                ),
                "graph_eligibility": "administrative_record",
                "source_role": "in_kind_donor",
                "target_role": "recipient_social_welfare_council",
                "amount": "",
                "currency": "",
                "amount_semantics": "in_kind_item_no_amount",
                "event_date": "",
                "reported_at": "2012-04-23",
                "target_display_name": "社会福祉法人うるま市社会福祉協議会",
                "target_identity_status": (
                    "legal_entity_confirmed_specific_facility_unresolved"
                ),
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018 revision: the legal recipient name is corrected; "
                    "no amount or subordinate facility is inferred."
                ),
            }
        )
    elif edge_id == "F030":
        edge.update(
            {
                "relation_type": "in_kind_acquisition_assistance",
                "event_or_program": (
                    "AWWA helped Far East Council acquire kayaks; date and "
                    "quantity unstated"
                ),
                "review_status": "human_revised",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "AWWA helped the then Boy Scouts of America Far East Council "
                    "acquire kayaks."
                ),
                "missing_scope": (
                    "Event date, quantity, amount, AWWA share and Okinawa-specific "
                    "allocation are unknown."
                ),
                "graph_eligibility": "administrative_record",
                "source_role": "acquisition_helper",
                "target_role": "overseas_scouting_council",
                "amount": "",
                "currency": "",
                "amount_semantics": "no_amount_no_quantity_no_share_allocation",
                "event_date": "",
                "reported_at": "2012-04-23",
                "target_display_name": "Far East Council, Scouting America",
                "historical_target_label": (
                    "Boy Scouts of America Far East Council"
                ),
                "target_identity_status": "historical_to_current_name_crosswalk",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018 revision: 2012 is the reporting date, not a proven "
                    "event date; this is acquisition assistance, not a dated "
                    "standalone donation."
                ),
            }
        )
    elif edge_id == "F036":
        edge.update(
            {
                "relation_type": "joint_in_kind_contribution",
                "event_or_program": (
                    "Joint delivery of three industrial cooling fans to an "
                    "unidentified Heshikiya-area after-school childcare center"
                ),
                "review_status": "human_revised",
                "claim_status": "supported_bounded",
                "confirmed_scope": (
                    "NOSCO was one of four named contributing groups in the "
                    "2025-08-15 delivery event."
                ),
                "missing_scope": (
                    "Recipient legal name, item value and each contributor's "
                    "share are unresolved."
                ),
                "graph_eligibility": "event_participation",
                "source_role": "one_of_four_named_contributing_groups",
                "target_role": "provisional_descriptive_recipient",
                "amount": "",
                "currency": "",
                "amount_semantics": "no_amount_no_contributor_share_allocation",
                "event_date": "2025-08-15",
                "target_display_name": (
                    "平敷屋地区の放課後児童クラブ（正式名称未確認）"
                ),
                "target_identity_status": "provisional_descriptive_recipient",
                "possible_locator_candidate": (
                    "きむたかこどもセンター学童クラブ"
                ),
                "locator_approved": "no",
                "needs_local_retrieval": "no",
                "notes": (
                    "HR-018 revision: do not attribute all three devices or their "
                    "value to NOSCO, and do not infer an alliance from joint delivery."
                ),
            }
        )
    else:
        raise ValueError(f"no main-sample update defined for {edge_id}")


def apply_hr018_main_relation_sample(root: Path = ROOT) -> dict[str, int]:
    fields, central_rows = read_csv(root / CENTRAL)
    fields = ensure_fields(fields, EXTRA_FIELDS)
    _, r10_rows = read_csv(root / R10_RELATIONS)
    _, queue_rows = read_csv(root / HR018_QUEUE)

    central = unique_index(central_rows, "edge_id")
    r10 = unique_index(r10_rows, "relation_observation_id")
    queue = unique_index(queue_rows, "relation_observation_id")
    protected_before = {
        edge_id: central[edge_id].copy() for edge_id in PROTECTED_HR033
    }

    for edge_id, relation_ids in OBSERVATION_MAP.items():
        observations = [r10[relation_id] for relation_id in relation_ids]
        common_review_update(central[edge_id], observations, queue)
        apply_specific_updates(central[edge_id])

    for edge_id, before in protected_before.items():
        if central[edge_id] != before:
            raise ValueError(f"HR-033 protected row changed: {edge_id}")

    write_csv(root / CENTRAL, fields, central_rows)
    summary = {
        "central_rows_unchanged": len(central_rows),
        "updated_main_edges": len(OBSERVATION_MAP),
        "hr033_protected_edges": len(PROTECTED_HR033),
        "new_main_edges": 0,
    }
    write_csv(
        root / OUT / "merge_summary_v1.csv",
        ["metric", "value"],
        [
            {"metric": metric, "value": str(value)}
            for metric, value in summary.items()
        ],
    )
    (root / OUT / "README.md").write_text(
        "# HR-018 central relation-sample synchronization\n\n"
        "Eleven pre-existing F rows are synchronized with the completed HR-018 "
        "review. No new F edge is created; normalized administrative facts remain "
        "in the R10 tables.\n\n"
        "- F031–F033 no longer present organization-side or whole-program project "
        "costs as payments.\n"
        "- F035 is corrected to a regional USO Indo-Pacific sponsor relation.\n"
        "- F024 is a dated historical membership, not a current or funding edge.\n"
        "- F028–F030 and F036 preserve in-kind/event limits and corrected recipient "
        "identity boundaries.\n"
        "- F027 remains an unallocable aggregate requiring local/internal records.\n"
        "- Six HR-033 rows are byte-for-field protected from this merge.\n",
        encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    result = apply_hr018_main_relation_sample()
    print(
        "HR-018 main relation sync complete: "
        f"{result['updated_main_edges']} updated rows; "
        f"{result['hr033_protected_edges']} HR-033 rows protected."
    )
