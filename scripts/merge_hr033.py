from __future__ import annotations

"""Merge the project-principal HR-033 legacy relation decisions.

The merge is deliberately narrow:

* normalize the six legacy ``verified`` rows;
* preserve F025 as a bounded KOSC→AWWA dyadic relation without an amount;
* accept the separate USD 102,000 mixed-recipient aggregate observation;
* synchronize the directly corresponding R10 observations;
* add one batch-level human-review log record and a typed frontend handoff.

It does not approve any other relation candidate and is idempotent.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = Path("data/interim")
OUT = Path("outputs/hr033_integration_v1")

HR033_IDS = ("F006", "F007", "F021", "F022", "F023", "F025")

V1_FIELDS = [
    "human_decision",
    "review_task_id",
    "human_reviewer",
    "review_date",
    "review_scope",
    "reviewed_fields",
    "claim_status",
    "confirmed_scope",
    "missing_scope",
    "graph_eligibility",
    "source_role",
    "target_role",
    "amount",
    "currency",
    "amount_semantics",
    "event_date",
    "publication_date",
    "interpretation_limit",
]

MEMBERSHIP_REVIEW_SCOPE = (
    "endpoint_identity;relation_existence;direction;time_period;interpretation_boundary"
)

MEMBERSHIP_REVIEWED_FIELDS = (
    "source_actor_id;target_actor_id;relation_type;source_role;target_role;"
    "source_ref;evidence_level;date_or_period;interpretation_limit"
)

COMMON_MEMBERSHIP = {
    "human_decision": "accept",
    "review_task_id": "HR-033",
    "human_reviewer": "project_principal_user",
    "review_date": "2026-07-20",
    "review_status": "human_checked",
    "review_scope": MEMBERSHIP_REVIEW_SCOPE,
    "reviewed_fields": MEMBERSHIP_REVIEWED_FIELDS,
    "claim_status": "supported",
    "graph_eligibility": "dyadic_relation",
    "source_role": "umbrella_coordination_association",
    "target_role": "member_club",
    "amount": "",
    "currency": "",
    "amount_semantics": "not_applicable_membership",
    "event_date": "",
    "publication_date": "",
    "needs_local_retrieval": "no",
}

DECISIONS: dict[str, dict[str, str]] = {
    "F006": {
        **COMMON_MEMBERSHIP,
        "confirmed_scope": (
            "AWWA is an umbrella coordination association and NOSCO is a named member club; "
            "the relation is visible in 2012 material and the current NOSCO page."
        ),
        "missing_scope": (
            "Formal charter terms, legal control, and exact effective or termination dates were not reviewed."
        ),
        "interpretation_limit": (
            "The structural arrow does not show control, funding, political alliance, common policy position, "
            "or influence direction; this row does not establish a current fixed total of five clubs."
        ),
    },
    "F007": {
        **COMMON_MEMBERSHIP,
        "confirmed_scope": (
            "AWWA is an umbrella coordination association and KOSC is a named member club or participating club."
        ),
        "missing_scope": (
            "Formal charter terms, representative-seat count, and exact membership period were not reviewed."
        ),
        "interpretation_limit": (
            "Membership is not funding; KOSC→AWWA financial contribution is separately encoded in F025; "
            "this relation does not show political alliance or control."
        ),
    },
    "F021": {
        "human_decision": "revise",
        "review_task_id": "HR-033",
        "human_reviewer": "project_principal_user",
        "review_date": "2026-07-20",
        "review_status": "human_revised",
        "review_scope": (
            "endpoint_identity;relation_existence;direction;amount;time_period;interpretation_boundary"
        ),
        "reviewed_fields": (
            "source_actor_id;target_actor_id;relation_type;funding_relation_confidence;"
            "amount;currency;amount_semantics;event_date;publication_date;source_ref;"
            "evidence_level;interpretation_limit"
        ),
        "relation_type": "donation",
        "funding_relation_confidence": "confirmed_donation",
        "claim_status": "supported",
        "confirmed_scope": (
            "OESC donated USD 3,250 to USO Okinawa on 2025-12-02 for its Okinawa service programs."
        ),
        "missing_scope": (
            "Settlement date, accounting classification, and program-level expenditure detail were not reviewed."
        ),
        "graph_eligibility": "dyadic_relation",
        "source_role": "donor",
        "target_role": "recipient_service_organization",
        "amount": "3250",
        "currency": "USD",
        "amount_semantics": "direct_charitable_donation",
        "event_date": "2025-12-02",
        "publication_date": "2025-12-12",
        "needs_local_retrieval": "no",
        "interpretation_limit": (
            "One charitable donation does not establish long-term sponsorship, a stable alliance, "
            "a base-policy position, or political influence."
        ),
    },
    "F022": {
        **COMMON_MEMBERSHIP,
        "reviewed_fields": MEMBERSHIP_REVIEWED_FIELDS.replace(
            "source_ref;", "duplicate_crosswalk;source_ref;"
        ),
        "confirmed_scope": (
            "AWWA is an umbrella coordination association and OESC is a named member club; "
            "F008 is a rejected duplicate and must not generate a second relation."
        ),
        "missing_scope": "Formal charter terms and exact membership period were not reviewed.",
        "interpretation_limit": (
            "Membership is not funding; F008 must not be restored; this relation does not show "
            "political alliance or a common policy position."
        ),
    },
    "F023": {
        **COMMON_MEMBERSHIP,
        "reviewed_fields": MEMBERSHIP_REVIEWED_FIELDS.replace(
            "source_ref;", "actor_alias;source_ref;"
        ),
        "confirmed_scope": (
            "AWWA is an umbrella coordination association and MOSCO or MOSC is a named member club."
        ),
        "missing_scope": (
            "Formal charter terms, representative seats, and exact membership period were not reviewed."
        ),
        "interpretation_limit": (
            "MOSC and MOSCO are name forms of the same organization and do not create another actor; "
            "membership is not funding, control, or political alliance."
        ),
    },
    "F025": {
        "human_decision": "revise",
        "review_task_id": "HR-033",
        "human_reviewer": "project_principal_user",
        "review_date": "2026-07-20",
        "review_status": "human_revised",
        "review_scope": (
            "endpoint_identity;relation_existence;direction;amount;time_period;interpretation_boundary"
        ),
        "reviewed_fields": (
            "source_actor_id;target_actor_id;relation_type;source_role;target_role;amount;currency;"
            "amount_semantics;date_or_period;source_ref;evidence_level;claim_status;"
            "graph_eligibility;interpretation_limit"
        ),
        "relation_type": "funding_contribution",
        "funding_relation_confidence": "confirmed_contribution",
        "claim_status": "supported_bounded",
        "confirmed_scope": (
            "KOSC's official page states that KOSC charitable funds are distributed to or through AWWA, "
            "supporting a named KOSC→AWWA contribution relation."
        ),
        "missing_scope": (
            "AWWA allocation, scholarship recipients and itemized amounts, the exact fiscal year denoted by "
            "'last year', transfer date, and full annual detail."
        ),
        "graph_eligibility": "dyadic_relation",
        "source_role": "contributing_member_club",
        "target_role": "umbrella_coordination_association",
        "amount": "",
        "currency": "USD",
        "amount_semantics": "named_contribution_amount_unknown",
        "event_date": "",
        "publication_date": "",
        "needs_local_retrieval": "no",
        "interpretation_limit": (
            "The graph may show a KOSC→AWWA contribution with amount not public; USD 102,000 must not be attached "
            "to this edge, scholarships are not one actor, and the contribution does not imply alliance or control."
        ),
    },
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


def index_unique(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    indexed = {row[key]: row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"Duplicate values in {key}")
    return indexed


def upsert(
    rows: list[dict[str, str]],
    addition: dict[str, str],
    keys: tuple[str, ...],
) -> None:
    matches = [
        row for row in rows if all(row.get(key, "") == addition.get(key, "") for key in keys)
    ]
    if len(matches) > 1:
        raise ValueError(f"Duplicate existing key for {keys}: {addition}")
    if matches:
        matches[0].update(addition)
    else:
        rows.append(dict(addition))


def typed_handoff_rows(relations: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for edge_id in HR033_IDS:
        row = relations[edge_id]
        family = (
            "structural_affiliation"
            if row["relation_type"] == "network_membership"
            else "resources_funding"
        )
        date_or_period = ""
        if edge_id == "F021":
            date_or_period = row["event_date"]
        elif edge_id in {"F006", "F007"}:
            date_or_period = "2012 and current official page"
        rows.append(
            {
                "id": edge_id,
                "observation_kind": "dyadic_relation",
                "relation_family": family,
                "relation_type": row["relation_type"],
                "source_endpoint": row["source_actor_id"],
                "target_endpoint": row["target_actor_id"],
                "source_role": row["source_role"],
                "target_role": row["target_role"],
                "scope_kind": "relation",
                "scope_id": "",
                "evidence_level": row["evidence_level"],
                "review_status": row["review_status"],
                "human_decision": row["human_decision"],
                "review_scope": row["review_scope"],
                "reviewed_fields": row["reviewed_fields"],
                "claim_status": row["claim_status"],
                "confirmed_scope": row["confirmed_scope"],
                "missing_scope": row["missing_scope"],
                "graph_eligibility": row["graph_eligibility"],
                "display_tier": "reviewed",
                "source_ids": row["source_ref"],
                "interpretation_limit": row["interpretation_limit"],
                "amount": row["amount"],
                "currency": row["currency"],
                "amount_semantics": row["amount_semantics"],
                "date_or_period": date_or_period,
            }
        )

    rows.append(
        {
            "id": "R10R029",
            "observation_kind": "aggregate_observation",
            "relation_family": "resources_funding",
            "relation_type": "aggregate_financial_contribution",
            "source_endpoint": "X006",
            "target_endpoint": "P_R10_KOSC_MIXED_RECIPIENTS",
            "source_role": "donor_reporting_aggregate",
            "target_role": "composite_recipient_scope",
            "scope_kind": "composite_recipient_scope",
            "scope_id": "P_R10_KOSC_MIXED_RECIPIENTS",
            "evidence_level": "E4",
            "review_status": "human_revised",
            "human_decision": "revise",
            "review_scope": "amount;time_period;endpoint_identity;interpretation_boundary",
            "reviewed_fields": (
                "source_endpoint;target_endpoint;target_role;relation_type;amount;currency;"
                "amount_semantics;date_or_period;claim_status;graph_eligibility;interpretation_limit"
            ),
            "claim_status": "supported_bounded",
            "confirmed_scope": (
                "KOSC reports a prior-year aggregate USD 102,000 donation to scholarships and AWWA."
            ),
            "missing_scope": (
                "Exact fiscal year, recipient list, and allocation between scholarships and AWWA."
            ),
            "graph_eligibility": "aggregate_observation",
            "display_tier": "reviewed",
            "source_ids": "S075",
            "interpretation_limit": (
                "The aggregate cannot be allocated to AWWA, any scholarship recipient, or any inferred single "
                "recipient; it does not enter the organization relation graph."
            ),
            "amount": "102000",
            "currency": "USD",
            "amount_semantics": "aggregate_mixed_recipient_no_allocation",
            "date_or_period": "prior year stated on undated/current webpage",
        }
    )
    return rows


def apply_hr033(root: Path = ROOT) -> dict[str, int]:
    data = root / DATA
    out = root / OUT

    relation_path = data / "15_funding_or_support_edges_sample_v0.csv"
    relation_fields, relation_rows = read_csv(relation_path)
    relation_fields = ensure_fields(relation_fields, V1_FIELDS)
    relations = index_unique(relation_rows, "edge_id")
    missing = set(HR033_IDS) - set(relations)
    if missing:
        raise ValueError(f"Missing HR-033 relations: {sorted(missing)}")
    for edge_id, decision in DECISIONS.items():
        relations[edge_id].update(decision)
    write_csv(relation_path, relation_fields, relation_rows)

    r10_path = data / "21_admin_collaboration_relations_v0.csv"
    r10_fields, r10_rows = read_csv(r10_path)
    r10 = index_unique(r10_rows, "relation_observation_id")
    mirror_statuses = {
        "R10R022": ("human_revised", "F021"),
        "R10R024": ("human_checked", "F006"),
        "R10R025": ("human_checked", "F007"),
        "R10R026": ("human_checked", "F022"),
        "R10R027": ("human_checked", "F023"),
    }
    for relation_id, (status, edge_id) in mirror_statuses.items():
        r10[relation_id]["review_status"] = status
        r10[relation_id]["merge_disposition"] = f"hr033_merged_main_{edge_id}"
    r10["R10R029"].update(
        {
            "relation_type": "aggregate_financial_contribution",
            "mechanism_label": "汇总资金贡献",
            "mechanism_detail": (
                "KOSC reports a prior-year aggregate USD 102,000 donation to scholarships and AWWA."
            ),
            "review_status": "human_revised",
            "merge_disposition": "hr033_accepted_aggregate_observation",
            "interpretation_limit": (
                "The aggregate cannot be allocated to AWWA, any scholarship recipient, or any single actor; "
                "it does not enter the organization relation graph."
            ),
        }
    )
    write_csv(r10_path, r10_fields, r10_rows)

    amount_path = data / "22_admin_amount_observations_v0.csv"
    amount_fields, amount_rows = read_csv(amount_path)
    amounts = index_unique(amount_rows, "amount_observation_id")
    amounts["R10AM024"].update(
        {
            "review_status": "human_revised",
            "interpretation_limit": (
                "合计 102,000 美元不能分配给 AWWA、任一 scholarship recipient 或任何单一 actor；"
                "明确财年与分项金额仍缺失。"
            ),
        }
    )
    write_csv(amount_path, amount_fields, amount_rows)

    function_path = data / "23_admin_function_observations_v0.csv"
    function_fields, function_rows = read_csv(function_path)
    functions = index_unique(function_rows, "function_observation_id")
    functions["R10FN037"].update(
        {
            "review_status": "human_revised",
            "interpretation_limit": (
                "这是 scholarships 与 AWWA 的混合 recipient 汇总披露，不是 AWWA 或任一 recipient "
                "获得 102,000 美元的记录，也不上组织关系图。"
            ),
        }
    )
    write_csv(function_path, function_fields, function_rows)

    log_path = data / "human_review_log_v0.csv"
    log_fields, log_rows = read_csv(log_path)
    upsert(
        log_rows,
        {
            "task_id": "HR-033",
            "object_id": ";".join(HR033_IDS),
            "review_date": "2026-07-20",
            "human_reviewer": "project_principal_user",
            "review_status": "human_revised",
            "evidence_level_final": "E4",
            "publishable_claim": "bounded",
            "decision": "4_accept_2_revise",
            "review_note": (
                "F006/F007/F022/F023 accepted as umbrella-member structure; F021 revised to direct donation; "
                "F025 retained as amount-unknown dyadic contribution and R10R029 accepted as a separate aggregate."
            ),
            "next_steps": (
                "Expose through typed builder gates; never infer funding from membership or allocate USD 102,000 "
                "to AWWA or a scholarship recipient."
            ),
        },
        ("task_id", "object_id"),
    )
    write_csv(log_path, log_fields, log_rows)

    typed_fields = [
        "id",
        "observation_kind",
        "relation_family",
        "relation_type",
        "source_endpoint",
        "target_endpoint",
        "source_role",
        "target_role",
        "scope_kind",
        "scope_id",
        "evidence_level",
        "review_status",
        "human_decision",
        "review_scope",
        "reviewed_fields",
        "claim_status",
        "confirmed_scope",
        "missing_scope",
        "graph_eligibility",
        "display_tier",
        "source_ids",
        "interpretation_limit",
        "amount",
        "currency",
        "amount_semantics",
        "date_or_period",
    ]
    write_csv(out / "typed_relation_observations_v1.csv", typed_fields, typed_handoff_rows(relations))
    write_csv(
        out / "integration_summary_v1.csv",
        ["metric", "value", "note"],
        [
            {"metric": "hr033_rows", "value": "6", "note": "all legacy verified rows decided"},
            {"metric": "accepted", "value": "4", "note": "F006 F007 F022 F023"},
            {"metric": "revised", "value": "2", "note": "F021 F025"},
            {"metric": "dyadic_relations", "value": "6", "note": "all registry-resolved; not alliances"},
            {
                "metric": "aggregate_observations",
                "value": "1",
                "note": "R10R029; USD 102000 mixed recipient; not a graph edge",
            },
            {"metric": "legacy_verified_remaining", "value": "0", "note": "within HR-033 scope"},
        ],
    )

    illegal = [
        edge_id for edge_id in HR033_IDS if relations[edge_id]["review_status"] == "verified"
    ]
    if illegal:
        raise ValueError(f"Legacy verified values remain: {illegal}")
    if relations["F025"]["amount"]:
        raise ValueError("F025 must not carry the USD 102,000 aggregate amount")
    if amounts["R10AM024"]["amount_value"] != "102000":
        raise ValueError("R10AM024 must preserve the aggregate USD 102,000 observation")

    return {"accepted": 4, "revised": 2, "aggregate_observations": 1}


def main() -> None:
    result = apply_hr033(ROOT)
    print(
        "HR-033 merged: "
        f"accepted={result['accepted']}; revised={result['revised']}; "
        f"aggregate_observations={result['aggregate_observations']}"
    )


if __name__ == "__main__":
    main()
