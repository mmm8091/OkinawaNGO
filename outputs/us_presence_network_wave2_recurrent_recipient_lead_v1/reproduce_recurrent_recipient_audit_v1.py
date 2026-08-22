from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable


PACKAGE_ID = "us_presence_network_wave2_recurrent_recipient_lead_v1"
REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = Path(__file__).resolve().parent
DISCOVERED_ON = "2026-08-22"


INPUTS = {
    "w2a_flows": REPO_ROOT
    / "outputs/us_presence_network_wave2_w2_a_v1/resource_flow_ledger_v1.csv",
    "w2a_recipient_crosswalk": REPO_ROOT
    / "outputs/us_presence_network_wave2_w2_a_v1/awwa_recipient_identity_leg2_v1.csv",
    "leg2_actions": REPO_ROOT
    / "outputs/us_presence_network_wave2_leg2_originals_v1/endpoint_action_crosswalk_v1.csv",
    "central_relations": REPO_ROOT
    / "data/interim/15_funding_or_support_edges_sample_v0.csv",
    "service_recipients": REPO_ROOT
    / "outputs/us_presence_service_recon_v1/service_recipient_candidates_v1.csv",
    "service_review": REPO_ROOT
    / "outputs/us_presence_service_recon_v1/human_review_queue_v1.csv",
    "mts_grants": REPO_ROOT
    / "outputs/us_presence_network_wave2_w2_a_v1/artifacts/tracer/mts_grants.html",
    "dvids_heshikiya": REPO_ROOT / "source_docs/source_archive/S102/raw.html",
    "aru_official": PACKAGE_DIR / "artifacts/aru_about_official.html",
    "kimutaka_official": PACKAGE_DIR / "artifacts/uruma_kimutaka_club_official.pdf",
}


REGISTER_COLUMNS = [
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


INVENTORY_COLUMNS = [
    "observation_id",
    "source_layer",
    "source_row_id",
    "provider_id",
    "provider_name",
    "recipient_label",
    "canonical_endpoint_id",
    "endpoint_display_name",
    "recipient_domain",
    "period_or_date",
    "flow_structure",
    "directness",
    "amount",
    "currency",
    "identity_status",
    "evidence_status",
    "source_receipt_ids",
    "overlap_candidate_group",
    "dedup_class",
    "eligibility_for_independent_provider_count",
    "boundary_note",
    "fact_status",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def index_rows(rows: Iterable[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if value in indexed:
            raise AssertionError(f"duplicate {key}: {value}")
        indexed[value] = row
    return indexed


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def text_has_one_final_lf_and_no_trailing_whitespace(path: Path) -> bool:
    data = path.read_bytes()
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        return False
    if b"\r" in data or re.search(rb"[ \t]+\n", data):
        return False
    try:
        data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    return True


def write_csv(path: Path, columns: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            missing = set(columns) - set(row)
            extra = set(row) - set(columns)
            if missing or extra:
                raise AssertionError(
                    f"{path.name} row schema mismatch; missing={missing}, extra={extra}"
                )
            writer.writerow(row)


def inv(
    observation_id: str,
    source_layer: str,
    source_row_id: str,
    provider_id: str,
    provider_name: str,
    recipient_label: str,
    canonical_endpoint_id: str,
    endpoint_display_name: str,
    recipient_domain: str,
    period_or_date: str,
    flow_structure: str,
    directness: str,
    amount: str,
    currency: str,
    identity_status: str,
    evidence_status: str,
    source_receipt_ids: str,
    overlap_candidate_group: str,
    dedup_class: str,
    eligibility: str,
    boundary_note: str,
) -> dict[str, object]:
    return {
        "observation_id": observation_id,
        "source_layer": source_layer,
        "source_row_id": source_row_id,
        "provider_id": provider_id,
        "provider_name": provider_name,
        "recipient_label": recipient_label,
        "canonical_endpoint_id": canonical_endpoint_id,
        "endpoint_display_name": endpoint_display_name,
        "recipient_domain": recipient_domain,
        "period_or_date": period_or_date,
        "flow_structure": flow_structure,
        "directness": directness,
        "amount": amount,
        "currency": currency,
        "identity_status": identity_status,
        "evidence_status": evidence_status,
        "source_receipt_ids": source_receipt_ids,
        "overlap_candidate_group": overlap_candidate_group,
        "dedup_class": dedup_class,
        "eligibility_for_independent_provider_count": eligibility,
        "boundary_note": boundary_note,
        "fact_status": "lead_only",
    }


def main() -> int:
    for name, path in INPUTS.items():
        if not path.is_file():
            raise FileNotFoundError(f"missing input {name}: {path}")

    w2a_rows = read_csv(INPUTS["w2a_flows"])
    w2a = index_rows(w2a_rows, "flow_observation_id")
    recipient_rows = read_csv(INPUTS["w2a_recipient_crosswalk"])
    recipients = index_rows(recipient_rows, "recipient_review_id")
    leg2_rows = read_csv(INPUTS["leg2_actions"])
    leg2 = index_rows(leg2_rows, "endpoint_action_id")
    central_rows = read_csv(INPUTS["central_relations"])
    central = index_rows(central_rows, "edge_id")
    service_rows = read_csv(INPUTS["service_recipients"])
    service = index_rows(service_rows, "observation_id")
    review_rows = read_csv(INPUTS["service_review"])
    review = index_rows(review_rows, "hr_id")

    expected_fields = {
        "RF005": ("X004", "Children Kana-san Okinawa"),
        "RF006": ("X004", "Okinawa Nanbu Rehabilitation and Medical Center"),
        "RF007": ("X004", "NPO ARU"),
        "RF008": ("X004", "Ambitious"),
        "RF009": ("X004", "Himawari Day Care on Ishigaki Island"),
        "RF010": ("X004", "Okinawa Southern Medical Center"),
        "RF020": ("X007", "AMERICAN WELFARE AND WORKS ASSOCIATION"),
        "RF026": ("X018", "AMERICAN WELFARE AND WORKS ASSOCIATION"),
        "RF041": ("X016", "American Welfare & Works Association (AWWA)"),
        "RF053": ("X018", "Ashibina Child Development Center families"),
        "RF054": ("X018", "Lions Clubs International, Okinawa intermediary"),
    }
    for row_id, expected in expected_fields.items():
        actual = (w2a[row_id]["source_actor_id"], w2a[row_id]["target_name"])
        if actual != expected:
            raise AssertionError(f"{row_id} changed: expected {expected!r}, got {actual!r}")

    for row_id in ("RL001", "RL002", "RL003", "RL004", "RL005", "RL006"):
        if row_id not in recipients:
            raise AssertionError(f"missing W2-A recipient crosswalk {row_id}")
    for row_id in ("EA001", "EA002", "EA003", "EA004"):
        if row_id not in leg2:
            raise AssertionError(f"missing LEG2 crosswalk {row_id}")
    for row_id in ("F002", "F021", "F025", "F026", "F028", "F029", "F036"):
        if row_id not in central:
            raise AssertionError(f"missing central relation {row_id}")
    for row_id in ("SR004", "SR006", "SR007", "SR010", "SR011"):
        if row_id not in service:
            raise AssertionError(f"missing service recipient row {row_id}")
    if "SR006=defer_identity" not in review["SR-HR-013"]["principal_decision"]:
        raise AssertionError("SR-HR-013 no longer preserves the ARU defer decision")

    endpoint_map = {
        "RF005": ("EP_KANA", "かなさん沖縄", "child/family medical care"),
        "RF006": ("EP_NANBU_REHAB", "沖縄南部療育医療センター", "medical/welfare"),
        "RF007": ("EP_ARU", "一般社団法人ある（候选）", "youth/welfare"),
        "RF008": ("EP_AMBITIOUS", "認定NPO法人アンビシャス", "medical/welfare"),
        "RF009": ("EP_HIMAWARI", "石垣市障がい児通所支援事業所ひまわり", "child/welfare"),
        "RF010": ("EP_SOUTHERN_MEDICAL", "沖縄県立南部医療センター・こども医療センター", "medical/child"),
    }

    inventory: list[dict[str, object]] = []
    next_id = 1

    def add(**kwargs: str) -> None:
        nonlocal next_id
        inventory.append(inv(observation_id=f"ROI{next_id:03d}", **kwargs))
        next_id += 1

    for flow_id, (endpoint_id, endpoint_name, domain) in endpoint_map.items():
        row = w2a[flow_id]
        add(
            source_layer="W2-A resource_flow_ledger",
            source_row_id=flow_id,
            provider_id=row["source_actor_id"],
            provider_name=row["source_actor_name"],
            recipient_label=row["target_name"],
            canonical_endpoint_id=endpoint_id,
            endpoint_display_name=endpoint_name,
            recipient_domain=domain,
            period_or_date=f'{row["period_start"]}/{row["period_end"]}',
            flow_structure="provider_to_recipient_descriptor",
            directness="provider_filing_only",
            amount=row["amount"],
            currency=row["currency"],
            identity_status=row["endpoint_identity_status"],
            evidence_status=row["review_status"],
            source_receipt_ids=row["source_receipt_ids"],
            overlap_candidate_group=endpoint_id,
            dedup_class="single_provider_observation",
            eligibility="yes_direct_candidate",
            boundary_note=row["prohibited_inference"],
        )

    leg2_map = {
        "EA001": ("EP_KANA", "かなさん沖縄", "child/family medical care"),
        "EA002": ("EP_AMBITIOUS", "認定NPO法人アンビシャス", "medical/welfare"),
        "EA003": ("EP_HIMAWARI", "石垣市障がい児通所支援事業所ひまわり", "child/welfare"),
    }
    for action_id, (endpoint_id, endpoint_name, domain) in leg2_map.items():
        row = leg2[action_id]
        add(
            source_layer="LEG2 endpoint_action_crosswalk",
            source_row_id=action_id,
            provider_id=row["provider_actor_id"],
            provider_name=row["provider_name"],
            recipient_label=row["recipient_endpoint"],
            canonical_endpoint_id=endpoint_id,
            endpoint_display_name=endpoint_name,
            recipient_domain=domain,
            period_or_date=row["event_date_or_period"],
            flow_structure=row["flow_or_action_type"],
            directness="recipient_side_action_same_provider",
            amount=row["value"],
            currency=row["currency_or_unit"],
            identity_status="recipient_side_identity_candidate",
            evidence_status=row["review_status"],
            source_receipt_ids=row["source_receipt_ids"],
            overlap_candidate_group=endpoint_id,
            dedup_class="same_provider_recurrence",
            eligibility="yes_direct_candidate_same_provider",
            boundary_note=row["prohibited_inference"],
        )

    central_endpoint_map = {
        "F028": (
            "EP_YOMITAN_QUEGOEN",
            "よみたん救護園",
            "welfare",
        ),
        "F029": (
            "EP_URUMA_WELFARE",
            "社会福祉法人うるま市社会福祉協議会",
            "welfare",
        ),
    }
    for edge_id, (endpoint_id, endpoint_name, domain) in central_endpoint_map.items():
        row = central[edge_id]
        add(
            source_layer="central relation sample",
            source_row_id=edge_id,
            provider_id=row["source_actor_id"],
            provider_name="American Welfare & Works Association (AWWA)",
            recipient_label=row["target_display_name"] or row["target_actor_id"],
            canonical_endpoint_id=endpoint_id,
            endpoint_display_name=endpoint_name,
            recipient_domain=domain,
            period_or_date=row["event_date"] or row["reported_at"] or "source-bounded year",
            flow_structure=row["relation_type"],
            directness="direct_named_recipient",
            amount=row["amount"],
            currency=row["currency"],
            identity_status=row["target_identity_status"],
            evidence_status=row["review_status"],
            source_receipt_ids=row["source_ref"],
            overlap_candidate_group=endpoint_id,
            dedup_class="single_provider_observation",
            eligibility="yes_direct_reviewed",
            boundary_note=row["interpretation_limit"],
        )

    service_endpoint_map = {
        "SR006": (
            "EP_ARU",
            "一般社団法人ある（候选）",
            "youth/welfare",
            "multihop_label_not_direct_recipient",
            "english_near_name_candidate",
            "no_indirect_and_identity_unresolved",
        ),
        "SR007": (
            "EP_TINSAKU",
            "沖縄小児在宅医療基金 てぃんさぐの会",
            "medical/child",
            "organization_page_recipient_label",
            "single_provider_observation",
            "yes_direct_candidate",
        ),
        "SR010": (
            "EP_OKI_HANDS",
            "一般社団法人Ｏｋｉ Ｈａｎｄｓ Ｏｋｉ Ｈｅａｒｔｓ",
            "welfare/community",
            "organization_page_outreach_label",
            "single_provider_observation",
            "yes_direct_candidate",
        ),
    }
    for row_id, values in service_endpoint_map.items():
        endpoint_id, endpoint_name, domain, directness, dclass, eligible = values
        row = service[row_id]
        add(
            source_layer="service recon recipient candidates",
            source_row_id=row_id,
            provider_id="X018" if row["provider_id_or_candidate"] == "CAND_MTS" else row["provider_id_or_candidate"],
            provider_name=row["provider_name"],
            recipient_label=row["recipient_name"],
            canonical_endpoint_id=endpoint_id,
            endpoint_display_name=endpoint_name,
            recipient_domain=domain,
            period_or_date=row["event_or_fiscal_date"],
            flow_structure=row["service_or_resource"],
            directness=directness,
            amount=row["amount"],
            currency=row["currency"],
            identity_status=row["recipient_identity_status"],
            evidence_status=row["review_status"],
            source_receipt_ids="RRL-SR001" if row_id in {"SR006", "SR007"} else row["url"],
            overlap_candidate_group=endpoint_id,
            dedup_class=dclass,
            eligibility=eligible,
            boundary_note=(
                review["SR-HR-013"]["principal_note"]
                if row_id == "SR006"
                else row["interpretation_limit"]
            ),
        )

    heshikiya_providers = [
        ("X005", "Naval Officers' Spouses' Club of Okinawa (NOSCO)"),
        ("NODE_CFAO", "Commander, Fleet Activities Okinawa"),
        ("NODE_VP9", "Patrol Squadron 9"),
        ("NODE_CFAO_CPOA", "CFAO Chief Petty Officers' Association"),
    ]
    for provider_id, provider_name in heshikiya_providers:
        add(
            source_layer="central relation + archived DVIDS expansion",
            source_row_id="F036/S102",
            provider_id=provider_id,
            provider_name=provider_name,
            recipient_label="Heshikiya-area after-school childcare center",
            canonical_endpoint_id="EP_HESHIKIYA_PROVISIONAL",
            endpoint_display_name="平敷屋地区の放課後児童クラブ（正式名称未确认）",
            recipient_domain="child/education",
            period_or_date="2025-08-15",
            flow_structure="joint_in_kind_contribution_event",
            directness="same_event_joint_contributor",
            amount="",
            currency="",
            identity_status="provisional_descriptive_recipient",
            evidence_status="human_revised_event_boundary",
            source_receipt_ids="RRL-SR002/S102",
            overlap_candidate_group="EP_HESHIKIYA_PROVISIONAL",
            dedup_class="same_event_joint_contribution",
            eligibility="yes_provider_but_one_joint_event_only",
            boundary_note="All four contributors and all three fans belong to one event; no contributor share or second event is documented.",
        )

    for label, period in (
        ("AWWA-JP / Miyako Facilities", "2023 grants-page display"),
        ("AWWA-JP / Ishigaki Facilities", "2023 grants-page display"),
    ):
        add(
            source_layer="MTS grants page",
            source_row_id="MTS page route label",
            provider_id="X018",
            provider_name="Marine Thrift Shop Okinawa",
            recipient_label=label,
            canonical_endpoint_id="UNRESOLVED_AWWA_LOCAL_BUCKET",
            endpoint_display_name=label,
            recipient_domain="welfare unspecified",
            period_or_date=period,
            flow_structure="provider_to_awwa_to_unspecified_facilities",
            directness="same_chain_via_awwa_generic_only",
            amount="",
            currency="",
            identity_status="generic_facility_bucket_no_endpoint_crosswalk",
            evidence_status="organization_self_page",
            source_receipt_ids="RRL-SR001",
            overlap_candidate_group="AWWA_DOWNSTREAM_FAMILY",
            dedup_class="same_chain_via_awwa",
            eligibility="no_no_named_final_endpoint_or_earmark",
            boundary_note="The label names AWWA-JP as the channel and a regional facility bucket; it cannot be assigned to any named AWWA recipient.",
        )

    upstream_to_awwa = [
        ("F025", "X006", "Kadena Officers' Spouses' Club (KOSC)", "central relation sample"),
        ("RF020", "X007", "Okinawa Enlisted Spouses' Club (OESC)", "W2-A resource_flow_ledger"),
        ("RF026", "X018", "Marine Thrift Shop Okinawa", "W2-A resource_flow_ledger"),
        ("RF041", "X016", "Marine Officers' Spouses' Club Okinawa (MOSCO)", "W2-A resource_flow_ledger"),
    ]
    for row_id, provider_id, provider_name, layer in upstream_to_awwa:
        row = central[row_id] if row_id.startswith("F") else w2a[row_id]
        add(
            source_layer=layer,
            source_row_id=row_id,
            provider_id=provider_id,
            provider_name=provider_name,
            recipient_label="American Welfare & Works Association (AWWA)",
            canonical_endpoint_id="NODE_AWWA_INTERMEDIARY",
            endpoint_display_name="American Welfare & Works Association (AWWA)",
            recipient_domain="base-side intermediary",
            period_or_date=(
                row.get("event_date")
                or "/".join(x for x in (row.get("period_start"), row.get("period_end")) if x)
                or "period not closed"
            ),
            flow_structure="provider_to_awwa_intermediary",
            directness="direct_to_intermediary_not_to_local_recipient",
            amount=row.get("amount", ""),
            currency=row.get("currency", ""),
            identity_status="named_intermediary",
            evidence_status=row.get("review_status", ""),
            source_receipt_ids=row.get("source_ref", "") or row.get("source_receipt_ids", ""),
            overlap_candidate_group="AWWA_DOWNSTREAM_FAMILY",
            dedup_class="same_chain_via_awwa",
            eligibility="no_intermediary_endpoint",
            boundary_note="An upstream contribution to AWWA is not a direct contribution to every downstream AWWA recipient; no earmark closes the chain.",
        )

    uso_inputs = [
        ("F002", "central relation sample", "AEC"),
        ("F021", "central relation sample", "OESC"),
        ("F026", "central relation sample", "AWWA"),
        ("SR004", "service recon recipient candidates", "MTS"),
    ]
    for row_id, layer, provider_short in uso_inputs:
        if row_id.startswith("F"):
            row = central[row_id]
            provider_id = row["source_actor_id"]
            amount = row["amount"]
            currency = row["currency"]
            period = row["event_date"] or row["reported_at"] or row["publication_date"]
            source_ids = row["source_ref"]
            provider_name = provider_short
        else:
            row = service[row_id]
            provider_id = "X018"
            amount = row["amount"]
            currency = row["currency"]
            period = row["event_or_fiscal_date"]
            source_ids = row["url"]
            provider_name = row["provider_name"]
        add(
            source_layer=layer,
            source_row_id=row_id,
            provider_id=provider_id,
            provider_name=provider_name,
            recipient_label="USO Okinawa / Kinser",
            canonical_endpoint_id="NODE_USO_BASE_SERVICE",
            endpoint_display_name="USO Okinawa",
            recipient_domain="base-side service organization",
            period_or_date=period,
            flow_structure="provider_to_base_service_node",
            directness="direct_but_outside_local_recipient_frame",
            amount=amount,
            currency=currency,
            identity_status="named_base_service_node",
            evidence_status=row["review_status"],
            source_receipt_ids=source_ids,
            overlap_candidate_group="NODE_USO_BASE_SERVICE",
            dedup_class="excluded_base_side_node",
            eligibility="no_not_local_welfare_child_medical_education_recipient",
            boundary_note="USO is a base-side service organization, not a local Okinawa welfare/child/medical/education recipient in this audit denominator.",
        )

    for row_id, endpoint_id, name, exclusion in (
        (
            "RF053",
            "NODE_ASHIBINA_BASE_BENEFICIARIES",
            "Ashibina Child Development Center families",
            "program beneficiary group at a base-side childcare facility",
        ),
        (
            "RF054",
            "NODE_LIONS_INTERMEDIARY",
            "Lions Clubs International, Okinawa intermediary",
            "named intermediary; final child-health endpoints unclosed",
        ),
    ):
        row = w2a[row_id]
        add(
            source_layer="W2-A resource_flow_ledger",
            source_row_id=row_id,
            provider_id=row["source_actor_id"],
            provider_name=row["source_actor_name"],
            recipient_label=row["target_name"],
            canonical_endpoint_id=endpoint_id,
            endpoint_display_name=name,
            recipient_domain="excluded or unclosed",
            period_or_date=row["event_date"] or f'{row["period_start"]}/{row["period_end"]}',
            flow_structure=row["resource_type"],
            directness=row["transaction_closure"],
            amount=row["amount"],
            currency=row["currency"],
            identity_status=row["endpoint_identity_status"],
            evidence_status=row["review_status"],
            source_receipt_ids=row["source_receipt_ids"],
            overlap_candidate_group=endpoint_id,
            dedup_class="excluded_base_side_or_intermediary",
            eligibility="no_outside_or_unclosed_final_recipient",
            boundary_note=exclusion,
        )

    write_csv(PACKAGE_DIR / "recipient_observation_inventory_v1.csv", INVENTORY_COLUMNS, inventory)

    eligible_endpoint_ids = {
        "EP_KANA",
        "EP_NANBU_REHAB",
        "EP_ARU",
        "EP_AMBITIOUS",
        "EP_HIMAWARI",
        "EP_SOUTHERN_MEDICAL",
        "EP_YOMITAN_QUEGOEN",
        "EP_URUMA_WELFARE",
        "EP_TINSAKU",
        "EP_OKI_HANDS",
        "EP_HESHIKIYA_PROVISIONAL",
    }
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in inventory:
        if row["canonical_endpoint_id"] in eligible_endpoint_ids:
            grouped[str(row["canonical_endpoint_id"])].append(row)

    endpoint_audit: list[dict[str, object]] = []
    for endpoint_id in sorted(eligible_endpoint_ids):
        rows = grouped[endpoint_id]
        if not rows:
            raise AssertionError(f"no observations generated for {endpoint_id}")
        all_providers = sorted({str(row["provider_id"]) for row in rows})
        countable_providers = sorted(
            {
                str(row["provider_id"])
                for row in rows
                if str(row["eligibility_for_independent_provider_count"]).startswith("yes")
            }
        )
        direct_events = {
            str(row["period_or_date"])
            for row in rows
            if str(row["eligibility_for_independent_provider_count"]).startswith("yes")
        }
        if endpoint_id == "EP_ARU":
            overlap_type = "english_near_name_candidate"
            independent_status = "no; MTS label is multi-hop and identity is unresolved"
        elif endpoint_id == "EP_HESHIKIYA_PROVISIONAL":
            overlap_type = "same_event_joint_contribution"
            independent_status = "no; four contributors belong to one joint event"
        elif len(all_providers) == 1 and len(rows) > 1:
            overlap_type = "same_provider_recurrence"
            independent_status = "no; repeated observations have one provider"
        else:
            overlap_type = "single_provider"
            independent_status = "no; only one direct provider is observed"
        endpoint_audit.append(
            {
                "canonical_endpoint_id": endpoint_id,
                "endpoint_display_name": rows[0]["endpoint_display_name"],
                "recipient_domain": rows[0]["recipient_domain"],
                "observation_count": len(rows),
                "all_observed_provider_ids": ";".join(all_providers),
                "countable_direct_provider_ids": ";".join(countable_providers),
                "countable_direct_provider_count": len(countable_providers),
                "distinct_countable_event_or_period_count": len(direct_events),
                "observation_ids": ";".join(str(row["observation_id"]) for row in rows),
                "overlap_class": overlap_type,
                "independent_multi_provider_status": independent_status,
                "confirmed_independent_multi_provider": "no",
                "fact_status": "lead_only",
                "boundary": "Provider count is endpoint- and event-aware; indirect AWWA chains, near names and one joint event do not establish repeated independent inflows.",
            }
        )
    endpoint_audit_columns = list(endpoint_audit[0])
    write_csv(
        PACKAGE_DIR / "recurrent_recipient_audit_v1.csv",
        endpoint_audit_columns,
        endpoint_audit,
    )

    dedup_rows = [
        {
            "dedup_case_id": "DG001",
            "candidate_endpoint_or_family": "AWWA downstream local-recipient family",
            "observed_paths": "KOSC/OESC/MOSCO/MTS -> AWWA; AWWA -> named or bucketed local recipients",
            "required_three_way_class": "same_chain_via_awwa",
            "same_recipient_status": "not established for any upstream provider",
            "same_event_status": "not applicable across filing periods",
            "earmark_or_chain_closure": "no earmark; periods differ; downstream allocation cannot be assigned upstream",
            "provider_count_after_dedup": "1 at each named downstream endpoint (AWWA only)",
            "independent_inflow_status": "not confirmed",
            "supporting_rows": "F025;RF020;RF026;RF041;RF005-RF010;F028;F029",
            "stop_reason": "Existing ledgers explicitly prohibit earmarking and transitive projection.",
            "fact_status": "lead_only",
        },
        {
            "dedup_case_id": "DG002",
            "candidate_endpoint_or_family": "MTS 'AWWA-JP / Miyako Facilities' and 'AWWA-JP / Ishigaki Facilities'",
            "observed_paths": "MTS -> AWWA-JP -> regional facility bucket",
            "required_three_way_class": "same_chain_via_awwa",
            "same_recipient_status": "generic regional buckets; no named endpoint crosswalk",
            "same_event_status": "page display only",
            "earmark_or_chain_closure": "unclosed beyond AWWA and generic facility labels",
            "provider_count_after_dedup": "not computable for a named endpoint",
            "independent_inflow_status": "not confirmed",
            "supporting_rows": "MTS grants page lines 654-655,661,701",
            "stop_reason": "The page does not identify a final named recipient or an independently documented transfer.",
            "fact_status": "lead_only",
        },
        {
            "dedup_case_id": "DG003",
            "candidate_endpoint_or_family": "NPO ARU / 一般社団法人ある candidate",
            "observed_paths": "AWWA filing -> 'NPO ARU'; MTS page route text -> 'NPO/ARU/Halfway House for Teenage Girls'",
            "required_three_way_class": "english_near_name_candidate",
            "same_recipient_status": "unresolved; legal-form mismatch and route syntax remain",
            "same_event_status": "no shared event closure",
            "earmark_or_chain_closure": "AWWA filing direct descriptor only; MTS record is multi-hop",
            "provider_count_after_dedup": "1 direct candidate (AWWA); MTS excluded as indirect/unresolved",
            "independent_inflow_status": "not confirmed",
            "supporting_rows": "RF007;RL003;SR006;SR-HR-013;MTS page lines 666,669",
            "stop_reason": "Official ARU page closes a plausible organization identity but not the English descriptor or a receipt from either provider.",
            "fact_status": "lead_only",
        },
        {
            "dedup_case_id": "DG004",
            "candidate_endpoint_or_family": "Heshikiya after-school childcare center",
            "observed_paths": "CFAO + VP-9 + CFAO CPOA + NOSCO -> three fans -> one unnamed center",
            "required_three_way_class": "same_event_joint_contribution",
            "same_recipient_status": "one provisional descriptive endpoint",
            "same_event_status": "yes; all contributors belong to 2025-08-15 delivery",
            "earmark_or_chain_closure": "no contributor shares; recipient legal name unresolved",
            "provider_count_after_dedup": "4 contributors but 1 event; zero repeated independent events",
            "independent_inflow_status": "not confirmed",
            "supporting_rows": "F036;S102",
            "stop_reason": "Uruma's Kimutaka listing is only a geographic candidate and no local receipt record was located.",
            "fact_status": "lead_only",
        },
        {
            "dedup_case_id": "DG005",
            "candidate_endpoint_or_family": "USO Okinawa",
            "observed_paths": "AEC/OESC/AWWA/MTS -> USO Okinawa or Kinser",
            "required_three_way_class": "independent_provider_to_recipient_outside_scope",
            "same_recipient_status": "base-side service node, not a local Okinawa welfare/child/medical/education recipient",
            "same_event_status": "multiple records",
            "earmark_or_chain_closure": "not evaluated in this recipient audit",
            "provider_count_after_dedup": "excluded from denominator",
            "independent_inflow_status": "outside this research question",
            "supporting_rows": "F002;F021;F026;SR004",
            "stop_reason": "Including USO would answer a different question and inflate local-recipient convergence.",
            "fact_status": "lead_only",
        },
    ]
    write_csv(
        PACKAGE_DIR / "endpoint_dedup_disambiguation_v1.csv",
        list(dedup_rows[0]),
        dedup_rows,
    )

    summary_rows = [
        {
            "metric": "input_csv_rows_inspected",
            "value": sum(
                len(rows)
                for rows in (
                    w2a_rows,
                    recipient_rows,
                    leg2_rows,
                    central_rows,
                    service_rows,
                    review_rows,
                )
            ),
            "unit": "rows",
            "interpretation": "Mechanical audit denominator across six existing tables before endpoint filtering.",
        },
        {
            "metric": "inventory_observations",
            "value": len(inventory),
            "unit": "observations",
            "interpretation": "Selected direct, indirect, same-event and explicit exclusion observations used by this endpoint audit.",
        },
        {
            "metric": "eligible_unique_local_endpoint_groups",
            "value": len(eligible_endpoint_ids),
            "unit": "endpoint groups",
            "interpretation": "Named or provisional Okinawa welfare/child/medical/education endpoints after excluding AWWA, USO, base-side beneficiary groups and generic buckets.",
        },
        {
            "metric": "apparent_multi_provider_endpoint_groups_before_event_chain_identity_gates",
            "value": 2,
            "unit": "endpoint groups",
            "interpretation": "ARU and Heshikiya appear multi-provider before route/identity and event-aware deduplication.",
        },
        {
            "metric": "confirmed_independent_multi_provider_local_recipients_after_dedup",
            "value": 0,
            "unit": "endpoint groups",
            "interpretation": "No named local endpoint currently has two independently closed provider-to-recipient inflows.",
        },
        {
            "metric": "same_provider_recurrence_endpoint_groups",
            "value": 3,
            "unit": "endpoint groups",
            "interpretation": "Kana-san, Ambitious and Himawari recur in AWWA-only records; recurrence is not cross-provider convergence.",
        },
        {
            "metric": "bounded_online_followup_observations",
            "value": 6,
            "unit": "follow-up observations",
            "interpretation": "Three follow-up steps each for ARU and Heshikiya/Kimutaka, within the package limit.",
        },
    ]
    write_csv(PACKAGE_DIR / "audit_summary_v1.csv", list(summary_rows[0]), summary_rows)

    followup_rows = [
        {
            "followup_id": "OF001",
            "chain_id": "ARU",
            "recon_step": 1,
            "target": "MTS grant-page route syntax",
            "source_or_query": "RRL-SR001; local lines 666 and 669",
            "observation": "The page prints 'Kubasaki High School- US/ Month of the Military Child Benefit NPO/ARU/ Halfway House for Teenage Girls' as one slash-delimited route label.",
            "classification": "english_near_name_candidate; multi-hop label",
            "effect_on_overlap": "MTS is not counted as a direct provider to ARU.",
            "stop_or_next": "Check the plausible Japanese organization's identity and recipient-side acknowledgment.",
            "fact_status": "lead_only",
        },
        {
            "followup_id": "OF002",
            "chain_id": "ARU",
            "recon_step": 2,
            "target": "一般社団法人ある official identity",
            "source_or_query": "RRL-SR003; local HTML lines 403,407,423,443",
            "observation": "The official site identifies 一般社団法人ある, incorporated in December 2020, with youth/mother and shared-house welfare programs.",
            "classification": "plausible semantic candidate; legal-form mismatch persists",
            "effect_on_overlap": "Identity is not closed to the filing's 'NPO ARU' or MTS route label.",
            "stop_or_next": "Search the recipient site and exact-name web results for AWWA/MTS receipt evidence.",
            "fact_status": "lead_only",
        },
        {
            "followup_id": "OF003",
            "chain_id": "ARU",
            "recon_step": 3,
            "target": "ARU recipient-side acknowledgment",
            "source_or_query": "NS001-NS002",
            "observation": "Bounded official-site and exact-name searches located no ARU-side AWWA or Marine Thrift Shop acknowledgment.",
            "classification": "not_found_in_bounded_search",
            "effect_on_overlap": "No second direct provider-to-recipient flow is confirmed.",
            "stop_or_next": "Stop at package limit; a future task would need an annual report, receipt, or donor/recipient original naming both endpoints.",
            "fact_status": "lead_only",
        },
        {
            "followup_id": "OF004",
            "chain_id": "HESHIKIYA",
            "recon_step": 1,
            "target": "2025-08-15 fan delivery",
            "source_or_query": "RRL-SR002; local HTML lines 596 and 708",
            "observation": "DVIDS names CFAO, VP-9, CFAO CPOA and NOSCO in one delivery of three fans to one unnamed Heshikiya after-school center.",
            "classification": "same_event_joint_contribution",
            "effect_on_overlap": "Four contributors do not constitute repeated independent inflows.",
            "stop_or_next": "Check the municipality's official after-school club directory for the endpoint identity.",
            "fact_status": "lead_only",
        },
        {
            "followup_id": "OF005",
            "chain_id": "HESHIKIYA",
            "recon_step": 2,
            "target": "Kimutaka club identity candidate",
            "source_or_query": "RRL-SR004; PDF p.1",
            "observation": "Uruma lists the public Kimutaka Child Center after-school club at 3607 Heshikiya, capacity 34, serving Heshikiya Elementary School.",
            "classification": "geographic_identity_candidate_only",
            "effect_on_overlap": "The official listing does not say it was the 2025 donation recipient.",
            "stop_or_next": "Search municipality/recipient-side records for the delivery or fan receipt.",
            "fact_status": "lead_only",
        },
        {
            "followup_id": "OF006",
            "chain_id": "HESHIKIYA",
            "recon_step": 3,
            "target": "Heshikiya/Kimutaka recipient-side receipt",
            "source_or_query": "NS003-NS004",
            "observation": "Bounded city-site and exact-name searches located no local acknowledgment tying Kimutaka to the fan delivery.",
            "classification": "not_found_in_bounded_search",
            "effect_on_overlap": "Recipient legal identity and any second independent event remain unclosed.",
            "stop_or_next": "Stop at package limit; local club records, city correspondence or a dated receipt would be required.",
            "fact_status": "lead_only",
        },
    ]
    write_csv(
        PACKAGE_DIR / "lead_only_online_followup_v1.csv",
        list(followup_rows[0]),
        followup_rows,
    )

    source_receipts = [
        {
            "receipt_id": "RRL-SR001",
            "publisher": "Marine Thrift Shop Okinawa",
            "title": "Grants",
            "source_family": "organization_self_page",
            "url": "https://marinethriftshopokinawa.org/grants/",
            "retrieved_at": "inherited W2-A archive; audited 2026-08-22",
            "artifact_path": rel(INPUTS["mts_grants"]),
            "sha256": sha256(INPUTS["mts_grants"]),
            "mime_type": "text/html",
            "exact_locator": "local HTML lines 654-655, 661, 666, 669, 701",
            "archive_status": "archived_existing_sha256_verified",
            "supports_rows": "ROI012;ROI019;ROI020;OF001;DG002;DG003",
            "boundary_note": "Slash-delimited labels are treated as routes/categories, not automatic direct recipient edges.",
        },
        {
            "receipt_id": "RRL-SR002",
            "publisher": "Defense Visual Information Distribution Service (DVIDS)",
            "title": "U.S. Navy Sailors Help Okinawan Childcare Center Beat the Heat",
            "source_family": "official_military_public_affairs",
            "url": "https://www.dvidshub.net/news/546868/us-navy-sailors-help-okinawan-childcare-center-beat-heat",
            "retrieved_at": "inherited S102 archive; audited 2026-08-22",
            "artifact_path": rel(INPUTS["dvids_heshikiya"]),
            "sha256": sha256(INPUTS["dvids_heshikiya"]),
            "mime_type": "text/html",
            "exact_locator": "local HTML lines 596 and 708",
            "archive_status": "archived_existing_sha256_verified",
            "supports_rows": "ROI015-ROI018;OF004;DG004",
            "boundary_note": "Names four contributors in one event; no share allocation or recipient legal name.",
        },
        {
            "receipt_id": "RRL-SR003",
            "publisher": "一般社団法人ある",
            "title": "あるについて",
            "source_family": "recipient_candidate_official_site",
            "url": "https://aru-okinawa.jp/%E3%81%82%E3%82%8B%E3%80%82%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/",
            "retrieved_at": "2026-08-22T20:42:32+08:00",
            "artifact_path": rel(INPUTS["aru_official"]),
            "sha256": sha256(INPUTS["aru_official"]),
            "mime_type": "text/html",
            "exact_locator": "local HTML lines 403, 407, 423, 443",
            "archive_status": "archived_new_sha256_verified",
            "supports_rows": "OF002;DG003",
            "boundary_note": "Closes current Japanese organization identity and programs only; does not crosswalk the English donor descriptors or a receipt.",
        },
        {
            "receipt_id": "RRL-SR004",
            "publisher": "うるま市",
            "title": "きむたかこどもセンター学童クラブ",
            "source_family": "municipal_official_directory",
            "url": "https://www.city.uruma.lg.jp/documents/1381/k3_kimutaka.pdf",
            "retrieved_at": "2026-08-22T20:42:41+08:00",
            "artifact_path": rel(INPUTS["kimutaka_official"]),
            "sha256": sha256(INPUTS["kimutaka_official"]),
            "mime_type": "application/pdf",
            "exact_locator": "p.1: public club, 3607 Heshikiya, capacity 34, Heshikiya Elementary catchment",
            "archive_status": "archived_new_sha256_verified",
            "supports_rows": "OF005;DG004",
            "boundary_note": "Geographic identity candidate only; the PDF does not mention the fan donation.",
        },
    ]
    write_csv(PACKAGE_DIR / "source_receipts_v1.csv", list(source_receipts[0]), source_receipts)

    negative_search_rows = [
        {
            "search_id": "NS001",
            "chain_id": "ARU",
            "observed_on": DISCOVERED_ON,
            "query_or_scope": "site:aru-okinawa.jp (AWWA OR 米国福祉事業協会 OR Marine Thrift Shop OR 米軍) 寄付",
            "source_family_searched": "recipient candidate official domain",
            "result": "No relevant acknowledgment located in bounded search.",
            "what_it_does_not_prove": "Search-engine and site visibility are incomplete; absence is not proof that no support occurred.",
            "stop_reason": "Third-step bounded reconnaissance exhausted for this chain.",
            "fact_status": "lead_only",
        },
        {
            "search_id": "NS002",
            "chain_id": "ARU",
            "observed_on": DISCOVERED_ON,
            "query_or_scope": "exact-name searches for Okinawa 'NPO ARU' / 'NPO法人ある' / Halfway House for Teenage Girls with AWWA or Marine Thrift Shop",
            "source_family_searched": "open web exact-name and recipient-side results",
            "result": "No independent identity/transaction closure located.",
            "what_it_does_not_prove": "The English label may refer to an unindexed program or a different entity.",
            "stop_reason": "Third-step bounded reconnaissance exhausted for this chain.",
            "fact_status": "lead_only",
        },
        {
            "search_id": "NS003",
            "chain_id": "HESHIKIYA",
            "observed_on": DISCOVERED_ON,
            "query_or_scope": "site:city.uruma.lg.jp 'きむたかこどもセンター' '扇風機'; 平敷屋 NOSCO 寄贈",
            "source_family_searched": "municipal official domain",
            "result": "Official club listing located; no fan-delivery acknowledgment located.",
            "what_it_does_not_prove": "The DVIDS recipient could be Kimutaka or another Heshikiya-area club; the identity remains unresolved.",
            "stop_reason": "Third-step bounded reconnaissance exhausted for this chain.",
            "fact_status": "lead_only",
        },
        {
            "search_id": "NS004",
            "chain_id": "HESHIKIYA",
            "observed_on": DISCOVERED_ON,
            "query_or_scope": "Heshikiya/Kimutaka exact-name searches with NOSCO, 米海軍, cooling fans, 寄贈",
            "source_family_searched": "open web local/recipient-side results",
            "result": "No recipient-side receipt or separate second event located.",
            "what_it_does_not_prove": "A non-indexed newsletter, correspondence file or local print report may exist.",
            "stop_reason": "Third-step bounded reconnaissance exhausted for this chain.",
            "fact_status": "lead_only",
        },
    ]
    write_csv(
        PACKAGE_DIR / "negative_search_log_v1.csv",
        list(negative_search_rows[0]),
        negative_search_rows,
    )

    register = [
        {
            "lead_id": "RRL001",
            "package_id": PACKAGE_ID,
            "record_kind": "origin_observation",
            "chain_id": "ARU",
            "parent_lead_id": "",
            "recon_step": 0,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "ARU appears under AWWA and MTS labels",
            "observation": "RF007 names 'NPO ARU' under AWWA while SR006/MTS contains 'NPO/ARU/Halfway House for Teenage Girls'.",
            "why_unexpected": "A mechanical name match creates the strongest apparent repeated local recipient in the current tables.",
            "source_or_query_locator": "RF007;RL003;SR006;SR-HR-013",
            "next_test": "Inspect the MTS page's route syntax.",
            "potential_value": "Tests whether a recipient receives independent flows or only appears in a multi-hop label.",
            "stop_reason": "",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL002",
            "package_id": PACKAGE_ID,
            "record_kind": "followup_observation",
            "chain_id": "ARU",
            "parent_lead_id": "RRL001",
            "recon_step": 1,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "MTS wording is a multi-hop route label",
            "observation": "The archived page joins Kubasaki High School, a Month of the Military Child benefit, NPO/ARU and a teenage-girls halfway house with slash-delimited route text.",
            "why_unexpected": "The existing candidate row visually resembles a direct MTS-to-ARU grant although the underlying page does not close that edge.",
            "source_or_query_locator": "RRL-SR001, local HTML lines 666 and 669",
            "next_test": "Check the plausible Japanese organization's official identity.",
            "potential_value": "Prevents double-counting MTS and AWWA as independent providers.",
            "stop_reason": "",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL003",
            "package_id": PACKAGE_ID,
            "record_kind": "followup_observation",
            "chain_id": "ARU",
            "parent_lead_id": "RRL002",
            "recon_step": 2,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "ARU identity remains a legal-form mismatch",
            "observation": "一般社団法人ある is a plausible Okinawa welfare organization, but its official legal form is not NPO and the site does not connect it to the two English descriptors.",
            "why_unexpected": "Program fit is strong enough to tempt an alias merge, while the legal-form and transaction evidence still disagree.",
            "source_or_query_locator": "RRL-SR003, local HTML lines 403,407,423,443",
            "next_test": "Search the recipient site and exact-name results for AWWA/MTS acknowledgments.",
            "potential_value": "Separates semantic similarity from an evidenced recipient identity.",
            "stop_reason": "",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL004",
            "package_id": PACKAGE_ID,
            "record_kind": "followup_observation",
            "chain_id": "ARU",
            "parent_lead_id": "RRL003",
            "recon_step": 3,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "No ARU-side receipt closure located",
            "observation": "Bounded official-site and exact-name searches found no recipient-side acknowledgment of AWWA or Marine Thrift Shop support.",
            "why_unexpected": "The strongest apparent overlap remains visible only from donor-side English labels.",
            "source_or_query_locator": "NS001-NS002",
            "next_test": "A separate future task would request an annual report, receipt or donor/recipient original.",
            "potential_value": "Would decide whether ARU is one shared recipient, an alias error or a multi-hop downstream beneficiary.",
            "stop_reason": "Three-step reconnaissance limit reached; no independent provider-to-recipient closure.",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL005",
            "package_id": PACKAGE_ID,
            "record_kind": "origin_observation",
            "chain_id": "HESHIKIYA",
            "parent_lead_id": "",
            "recon_step": 0,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "Heshikiya endpoint has four named contributors",
            "observation": "F036 records NOSCO as one of four groups contributing three cooling fans to an unnamed Heshikiya after-school center.",
            "why_unexpected": "Provider counts alone make this look like a local recipient receiving multiple inflows.",
            "source_or_query_locator": "F036;S102",
            "next_test": "Inspect the event source for timing and allocation.",
            "potential_value": "Tests whether multi-provider counts survive event-aware deduplication.",
            "stop_reason": "",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL006",
            "package_id": PACKAGE_ID,
            "record_kind": "followup_observation",
            "chain_id": "HESHIKIYA",
            "parent_lead_id": "RRL005",
            "recon_step": 1,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "All four contributors belong to one event",
            "observation": "DVIDS places CFAO, VP-9, CFAO CPOA and NOSCO in the same 2025-08-15 delivery, with no contributor shares.",
            "why_unexpected": "The apparent network convergence is event co-participation, not repeated independent support.",
            "source_or_query_locator": "RRL-SR002, local HTML lines 596 and 708",
            "next_test": "Check the municipal club directory for the recipient identity.",
            "potential_value": "Prevents one ceremony from being counted as four separate longitudinal inflows.",
            "stop_reason": "",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL007",
            "package_id": PACKAGE_ID,
            "record_kind": "followup_observation",
            "chain_id": "HESHIKIYA",
            "parent_lead_id": "RRL006",
            "recon_step": 2,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "Kimutaka is only a geographic identity candidate",
            "observation": "Uruma's official PDF lists Kimutaka Child Center after-school club at 3607 Heshikiya but contains no fan-delivery reference.",
            "why_unexpected": "Place and service type align closely enough to invite a premature recipient merge.",
            "source_or_query_locator": "RRL-SR004, PDF p.1",
            "next_test": "Search recipient/municipal records for a dated delivery acknowledgment.",
            "potential_value": "Could close the provisional Heshikiya endpoint without relying on geography alone.",
            "stop_reason": "",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
        {
            "lead_id": "RRL008",
            "package_id": PACKAGE_ID,
            "record_kind": "followup_observation",
            "chain_id": "HESHIKIYA",
            "parent_lead_id": "RRL007",
            "recon_step": 3,
            "discovered_on": DISCOVERED_ON,
            "lead_title": "No local receipt or second event located",
            "observation": "Bounded city-site and exact-name searches found no local acknowledgment tying Kimutaka to the fans and no separate repeated inflow.",
            "why_unexpected": "The only visible record remains a military public-affairs account with an unnamed recipient.",
            "source_or_query_locator": "NS003-NS004",
            "next_test": "A future local task would request club records, city correspondence or a dated receipt.",
            "potential_value": "Would close the endpoint identity and distinguish a one-off ceremony from repeated support.",
            "stop_reason": "Three-step reconnaissance limit reached; recipient identity and repeated flow remain unclosed.",
            "workflow_status": "lead_only",
            "claim_eligibility": "no",
            "central_writeback": "no",
            "human_review_trigger": "no",
            "publication_eligibility": "no",
        },
    ]
    write_csv(PACKAGE_DIR / "unexpected_findings_register_v1.csv", REGISTER_COLUMNS, register)

    input_manifest = []
    csv_row_counts = {
        "w2a_flows": len(w2a_rows),
        "w2a_recipient_crosswalk": len(recipient_rows),
        "leg2_actions": len(leg2_rows),
        "central_relations": len(central_rows),
        "service_recipients": len(service_rows),
        "service_review": len(review_rows),
    }
    for name, path in INPUTS.items():
        input_manifest.append(
            {
                "input_id": name,
                "path": rel(path),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "row_count_if_csv": csv_row_counts.get(name, ""),
                "role": (
                    "mechanical_audit_input"
                    if name in csv_row_counts
                    else "archived_source_or_followup_artifact"
                ),
            }
        )
    write_csv(PACKAGE_DIR / "input_manifest_v1.csv", list(input_manifest[0]), input_manifest)

    output_files = [
        "recipient_observation_inventory_v1.csv",
        "recurrent_recipient_audit_v1.csv",
        "endpoint_dedup_disambiguation_v1.csv",
        "audit_summary_v1.csv",
        "lead_only_online_followup_v1.csv",
        "source_receipts_v1.csv",
        "negative_search_log_v1.csv",
        "unexpected_findings_register_v1.csv",
        "input_manifest_v1.csv",
    ]
    output_manifest = [
        {
            "path": (PACKAGE_DIR / name).name,
            "sha256": sha256(PACKAGE_DIR / name),
            "bytes": (PACKAGE_DIR / name).stat().st_size,
        }
        for name in output_files
    ]
    control_names = [
        "README.md",
        "reproduce_recurrent_recipient_audit_v1.py",
        "validate_recurrent_recipient_package_v1.py",
    ]
    control_manifest = [
        {
            "path": name,
            "sha256": sha256(PACKAGE_DIR / name),
            "bytes": (PACKAGE_DIR / name).stat().st_size,
        }
        for name in control_names
    ]
    manifest = {
        "package_id": PACKAGE_ID,
        "generated_on": DISCOVERED_ON,
        "status": "lead_only",
        "central_writeback": "no",
        "human_review_trigger": "no",
        "publication_eligibility": "no",
        "frontend_eligibility": "no",
        "input_count": len(input_manifest),
        "output_count": len(output_manifest),
        "outputs": output_manifest,
        "control_files": control_manifest,
    }
    (PACKAGE_DIR / "manifest_v1.json").write_bytes(
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )

    checks = {
        "all_inputs_exist": all(path.is_file() for path in INPUTS.values()),
        "inventory_rows_nonzero": len(inventory) > 0,
        "eligible_endpoint_group_count_is_11": len(eligible_endpoint_ids) == 11,
        "all_endpoint_groups_generated": set(grouped) == eligible_endpoint_ids,
        "independent_multi_provider_count_is_zero": all(
            row["confirmed_independent_multi_provider"] == "no" for row in endpoint_audit
        ),
        "required_dedup_classes_present": {
            "same_chain_via_awwa",
            "english_near_name_candidate",
            "same_event_joint_contribution",
        }.issubset({str(row["required_three_way_class"]) for row in dedup_rows}),
        "followup_observation_count_within_10": len(followup_rows) <= 10,
        "unexpected_register_count_within_10": len(register) <= 10,
        "all_package_rows_lead_only": all(
            row.get("fact_status") == "lead_only"
            for rows in (
                inventory,
                endpoint_audit,
                dedup_rows,
                followup_rows,
                negative_search_rows,
            )
            for row in rows
        ),
        "new_artifact_hashes_match_expected": (
            sha256(INPUTS["aru_official"])
            == "d2f3ca0f86451d5491c42de6b66b54d3386d5dc6f9282db22c11985b1cc21925"
            and sha256(INPUTS["kimutaka_official"])
            == "61325fb9f8519c8a33622576cb999b7737159883561d1a089cb95c59441b1d47"
        ),
        "derived_text_has_no_trailing_whitespace_and_one_final_lf": all(
            text_has_one_final_lf_and_no_trailing_whitespace(PACKAGE_DIR / name)
            for name in output_files
            + control_names
            + ["manifest_v1.json"]
        ),
    }
    validation = {
        "package_id": PACKAGE_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "counts": {
            "inventory_observations": len(inventory),
            "eligible_endpoint_groups": len(eligible_endpoint_ids),
            "apparent_multi_provider_groups": 2,
            "confirmed_independent_multi_provider_groups": 0,
            "same_provider_recurrence_groups": 3,
            "online_followup_observations": len(followup_rows),
            "unexpected_register_observations": len(register),
        },
        "boundary": "PASS validates package mechanics and boundaries; it does not approve a research finding, central fact, HR decision or publication claim.",
    }
    (PACKAGE_DIR / "validation_report_v1.json").write_bytes(
        (json.dumps(validation, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    if validation["status"] != "PASS":
        raise SystemExit("validation failed")
    print(json.dumps(validation["counts"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
