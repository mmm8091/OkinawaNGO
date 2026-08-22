#!/usr/bin/env python3
"""Build W2-A: spouse-club filings, resource channels and recipient-side checks.

The builder is deliberately additive.  It reads the principal-confirmed W2-00
package and locally frozen W2-A artifacts, then writes only the dedicated
research-only package.  It never assigns central source IDs or writes central
facts, the legacy 43-row relation sample, publication adapters or the frontend.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_a_v1"
W2_00 = ROOT / "outputs" / "us_presence_network_wave2_w2_00_spouse_990_v1"
FIXED_AT = "2026-08-22T17:30:00+08:00"

ACTORS = {
    "AWWA": ("X004", "American Welfare & Works Association (AWWA)"),
    "KOSC": ("X006", "Kadena Officers' Spouses' Club (KOSC)"),
    "MOSCO": ("X016", "Marine Officers' Spouses' Club Okinawa (MOSCO)"),
    "NOSCO": ("X005", "Naval Officers' Spouses' Club of Okinawa (NOSCO)"),
    "OESC": ("X007", "Okinawa Enlisted Spouses' Club (OESC)"),
    "MTS": ("X018", "Marine Thrift Shop Okinawa"),
}

CORE_FILINGS = [
    # case, start, end, form, upstream receipt, upstream artifact
    ("AWWA", "2021-06-01", "2022-05-31", "990EZ", "W2A-SR015", ""),
    ("AWWA", "2022-06-01", "2023-05-31", "990EZ", "W2A-SR001", "raw/awwa_fy2023_202410619349200461.xml"),
    ("AWWA", "2023-06-01", "2024-05-31", "990EZ", "W2A-SR002", "raw/awwa_fy2024_202443189349200514.xml"),
    ("KOSC", "2022-06-01", "2023-05-31", "990", "W2A-SR003", "raw/kosc_fy2023_202430969349301028.xml"),
    ("KOSC", "2023-06-01", "2024-05-31", "990", "W2A-SR004", "raw/kosc_fy2024_202500669349300300.xml"),
    ("KOSC", "2024-06-01", "2025-05-31", "990", "W2A-SR005", "raw/irs_202630129349300153_public.xml"),
    ("MOSCO", "2022-06-01", "2023-05-31", "990EZ", "W2A-SR006", "raw/mosco_fy2023_202410719349201281.xml"),
    ("MOSCO", "2023-06-01", "2024-05-31", "990EZ", "W2A-SR007", "raw/mosco_fy2024_202501019349201215.xml"),
    ("MOSCO", "2024-06-01", "2025-05-31", "990EZ", "W2A-SR008", "raw/mosco_fy2025_202621539349200807.xml"),
    ("NOSCO", "2022-07-01", "2023-06-30", "990", "W2A-SR009", "raw/nosco_fy2023_202411349349304281.xml"),
    ("NOSCO", "2023-07-01", "2024-06-30", "990", "W2A-SR010", "raw/nosco_fy2024_202530159349302288.xml"),
    ("NOSCO", "2024-07-01", "2025-06-30", "990", "W2A-SR011", "raw/nosco_fy2025_202533199349301708.xml"),
    ("OESC", "2022-07-01", "2023-06-30", "990", "W2A-SR012", "raw/oesc_fy2023_202411309349303066.xml"),
    ("OESC", "2023-07-01", "2024-06-30", "990", "W2A-SR013", "raw/oesc_fy2024_202403029349300610.xml"),
    ("OESC", "2024-07-01", "2025-06-30", "990", "W2A-SR014", "raw/oesc_fy2025_202513109349302911.xml"),
]

MTS_FILINGS = [
    ("MTS", "2022-01-01", "2022-12-31", "990", "W2A2-SR003", ""),
    ("MTS", "2023-01-01", "2023-12-31", "990", "W2A2-SR001", "artifacts/irs/mts_fy2023_202401989349301535.xml"),
    ("MTS", "2024-01-01", "2024-12-31", "990", "W2A2-SR002", "artifacts/irs/mts_fy2024_202510939349300851.xml"),
]

METRICS = [
    "total_revenue_usd",
    "total_expenses_usd",
    "grants_and_similar_paid_usd",
    "net_assets_or_fund_balances_eoy_usd",
]

PROTECTED = [
    ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv",
    ROOT / "data" / "interim" / "07_actor_issue_edges_initial_v0.csv",
    ROOT / "data" / "interim" / "20_funding_support_edges_v0.csv",
    ROOT / "data" / "interim" / "21_admin_collaboration_relations_v0.csv",
    ROOT / "data" / "interim" / "05_source_log_initial_v0.csv",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def lname(element: ET.Element) -> str:
    return element.tag.split("}")[-1]


def first_text(root: ET.Element, name: str) -> str:
    for element in root.iter():
        if lname(element) == name:
            return (element.text or "").strip()
    return ""


def group_values(group: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for element in group.iter():
        text = (element.text or "").strip()
        if text:
            result[lname(element)] = text
    return result


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", name.casefold()).strip()


def person_key(name: str) -> str:
    return "PN_" + hashlib.sha1(normalize_name(name).encode("utf-8")).hexdigest()[:10].upper()


def artifact_path(output: Path, relative: str) -> Path:
    if relative.startswith("raw/"):
        return W2_00 / relative
    return output / relative


def build_filing_register(output: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for cohort, filings in (("core_five", CORE_FILINGS), ("marine_thrift_shop_tracer", MTS_FILINGS)):
        for case, start, end, form, receipt, artifact in filings:
            actor_id, actor_name = ACTORS[case]
            exists = bool(artifact) and artifact_path(output, artifact).exists()
            rows.append(
                {
                    "filing_slot_id": f"FS-{case}-{end[:4]}",
                    "cohort": cohort,
                    "case_id": case,
                    "actor_id": actor_id,
                    "actor_name": actor_name,
                    "period_start": start,
                    "period_end": end,
                    "form_type": form,
                    "source_receipt_id": receipt,
                    "artifact_path": (str(artifact_path(output, artifact).relative_to(ROOT)).replace("\\", "/") if artifact else ""),
                    "coverage_status": "official_irs_xml_frozen" if exists else "official_index_only_xml_gap",
                    "fact_status": "research_only",
                    "allowed_claim": "A filing XML is locally frozen for this tax period." if exists else "The official annual index reports a filing, but no official XML is admitted for metrics in this package.",
                    "prohibited_inference": "An index-only slot has no admitted amount; filing periods are not interchangeable with calendar years or other organizations' tax periods.",
                }
            )
    return rows


def build_metric_long(output: Path, register: list[dict[str, object]]) -> list[dict[str, object]]:
    anchors = read_csv(W2_00 / "anchor_candidates_v1.csv")
    anchor_map = {
        (row["case_id"], row["period_start"], row["period_end"], row["metric"]): row
        for row in anchors
        if row["case_id"] in ACTORS and row["metric"] in METRICS
    }
    rows: list[dict[str, object]] = []
    counter = 1
    mts_tags = {
        "total_revenue_usd": "CYTotalRevenueAmt",
        "total_expenses_usd": "CYTotalExpensesAmt",
        "grants_and_similar_paid_usd": "CYGrantsAndSimilarPaidAmt",
        "net_assets_or_fund_balances_eoy_usd": "NetAssetsOrFundBalancesEOYAmt",
    }
    for slot in register:
        case = str(slot["case_id"])
        start, end = str(slot["period_start"]), str(slot["period_end"])
        for metric in METRICS:
            value = ""
            source_anchor_id = ""
            review_status = "ai_seeded"
            field_semantics = "official_xml_field"
            if case != "MTS":
                anchor = anchor_map.get((case, start, end, metric))
                if anchor:
                    value = anchor["value"]
                    source_anchor_id = anchor["anchor_id"]
                    review_status = anchor["review_status"]
                    if metric == "grants_and_similar_paid_usd" and not value:
                        field_semantics = "xml_element_absent_not_zero"
            elif slot["coverage_status"] == "official_irs_xml_frozen":
                root = ET.parse(ROOT / str(slot["artifact_path"])).getroot()
                value = first_text(root, mts_tags[metric])
            else:
                field_semantics = "index_only_no_amount"
            rows.append(
                {
                    "metric_observation_id": f"FM{counter:03d}",
                    "cohort": slot["cohort"],
                    "case_id": case,
                    "actor_id": slot["actor_id"],
                    "actor_name": slot["actor_name"],
                    "period_start": start,
                    "period_end": end,
                    "metric": metric,
                    "value": value,
                    "currency": "USD",
                    "field_semantics": field_semantics,
                    "source_anchor_id": source_anchor_id,
                    "source_receipt_id": slot["source_receipt_id"],
                    "review_status": review_status,
                    "fact_status": "research_only_official_filing_observation" if value else "research_only_explicit_gap",
                    "allowed_claim": f"The filing reports {metric}={value} for this tax period." if value else "No numeric value is admitted for this metric and tax period.",
                    "prohibited_inference": "Do not combine unlike tax periods into an annual ecology total; a missing element is not zero.",
                }
            )
            counter += 1
    return rows


def build_person_roles(output: Path, register: list[dict[str, object]]) -> list[dict[str, object]]:
    parsed: list[dict[str, object]] = []
    for slot in register:
        if slot["coverage_status"] != "official_irs_xml_frozen":
            continue
        root = ET.parse(ROOT / str(slot["artifact_path"])).getroot()
        for ordinal, group in enumerate(
            [e for e in root.iter() if lname(e) in {"Form990PartVIISectionAGrp", "OfficerDirectorTrusteeEmplGrp"}],
            1,
        ):
            values = group_values(group)
            name = values.get("PersonNm", "").strip()
            if not name:
                continue
            parsed.append(
                {
                    "person_key": person_key(name),
                    "normalized_name_key": normalize_name(name),
                    "name_as_filed": name,
                    "actor_id": slot["actor_id"],
                    "actor_name": slot["actor_name"],
                    "period_start": slot["period_start"],
                    "period_end": slot["period_end"],
                    "role_title_as_filed": values.get("TitleTxt", ""),
                    "average_hours_per_week": values.get("AverageHoursPerWeekRt", ""),
                    "reportable_compensation_usd": values.get("ReportableCompFromOrgAmt", ""),
                    "source_receipt_id": slot["source_receipt_id"],
                    "exact_locator": f"official XML Part VII/officer group [{ordinal}]",
                }
            )
    by_key: dict[str, set[str]] = defaultdict(set)
    for row in parsed:
        by_key[str(row["person_key"])].add(str(row["actor_id"]))
    rows: list[dict[str, object]] = []
    for ordinal, row in enumerate(parsed, 1):
        cross = len(by_key[str(row["person_key"])]) > 1
        rows.append(
            {
                "role_observation_id": f"PR{ordinal:03d}",
                **row,
                "identity_resolution_status": "exact_string_cross_actor_candidate_unreviewed" if cross else "string_key_only_not_person_identity",
                "cross_actor_candidate": "yes" if cross else "no",
                "review_status": "ai_seeded",
                "fact_status": "research_only_official_filing_role_observation",
                "allowed_claim": "The filing lists this exact name string and role for this tax period.",
                "prohibited_inference": "A filing period is not an exact term; exact or similar names are not confirmed person identities or cross-organization bridges without human disambiguation.",
            }
        )
    return rows


FLOW_FIELDS = [
    "flow_observation_id", "provider_case", "source_actor_id", "source_actor_name",
    "target_id", "target_name", "target_kind", "period_start", "period_end", "event_date",
    "amount", "currency", "amount_semantics", "resource_type", "purpose",
    "reporting_layer", "reconciliation_component", "dedupe_group_id", "dedupe_status",
    "included_as_relation_candidate", "endpoint_identity_status", "transaction_closure",
    "source_receipt_ids", "source_anchor_ids", "exact_locator", "evidence_level",
    "review_status", "fact_status", "leg_layer", "allowed_claim", "prohibited_inference",
]


def build_resource_ledger(output: Path, metrics: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    anchors = read_csv(W2_00 / "anchor_candidates_v1.csv")
    rows: list[dict[str, object]] = []
    counter = 1

    def add(**kwargs: object) -> None:
        nonlocal counter
        base = {field: "" for field in FLOW_FIELDS}
        base.update(kwargs)
        base["flow_observation_id"] = f"RF{counter:03d}"
        rows.append(base)
        counter += 1

    # AWWA's two filing-level buckets and six named subcomponents.  Named rows
    # are subsets of the Japanese bucket, never additional to it.
    named_anchors = {"W2A-A070", "W2A-A071", "W2A-A072", "W2A-A073", "W2A-A074", "W2A-A075"}
    bucket_metrics = {
        "reported_grant_bucket_japanese_organizations_usd": ("AGG_JAPAN_ORGS", "Japanese organizations", "recipient_bucket"),
        "reported_grant_bucket_us_military_base_affiliated_organizations_usd": ("AGG_BASE_ORGS", "U.S.-military-base-affiliated organizations", "recipient_bucket"),
    }
    for anchor in anchors:
        if anchor["case_id"] == "AWWA" and anchor["metric"] in bucket_metrics:
            target_id, target_name, target_kind = bucket_metrics[anchor["metric"]]
            add(
                provider_case="AWWA", source_actor_id="X004", source_actor_name=ACTORS["AWWA"][1],
                target_id=target_id, target_name=target_name, target_kind=target_kind,
                period_start=anchor["period_start"], period_end=anchor["period_end"], amount=anchor["value"], currency="USD",
                amount_semantics="filing_reported_aggregate_bucket", resource_type="cash_grant_bucket",
                purpose="AWWA Schedule O grant bucket", reporting_layer="aggregate_bucket",
                reconciliation_component="yes", dedupe_group_id=f"AWWA-{anchor['period_end']}-GRANTS",
                dedupe_status="component_of_grant_line_total", included_as_relation_candidate="no",
                endpoint_identity_status="aggregate_not_actor", transaction_closure="bucket_only",
                source_receipt_ids=anchor["source_receipt_ids"], source_anchor_ids=anchor["anchor_id"], exact_locator=anchor["exact_locator"],
                evidence_level="official_irs_xml", review_status=anchor["review_status"], fact_status="research_only_official_filing_bucket",
                leg_layer="LEG0", allowed_claim=anchor["allowed_claim"], prohibited_inference="Do not actorize this bucket or add named rows to it; named rows are a subset.",
            )
        if anchor["anchor_id"] in named_anchors:
            descriptor = anchor["observed_local"]
            add(
                provider_case="AWWA", source_actor_id="X004", source_actor_name=ACTORS["AWWA"][1],
                target_id="RECIP_DESC_" + anchor["anchor_id"].split("-")[-1], target_name=descriptor, target_kind="filing_recipient_descriptor",
                period_start=anchor["period_start"], period_end=anchor["period_end"], amount=anchor["value"], currency="USD",
                amount_semantics="filing_reported_named_program_service_amount", resource_type="cash_grant_candidate",
                purpose="filing program-service recipient description", reporting_layer="named_subcomponent_of_japan_bucket",
                reconciliation_component="no", dedupe_group_id=f"AWWA-{anchor['period_end']}-JAPAN",
                dedupe_status="subset_of_japanese_organizations_bucket", included_as_relation_candidate="yes_pending_identity_review",
                endpoint_identity_status="descriptor_crosswalk_pending_principal", transaction_closure="provider_filing_only",
                source_receipt_ids=anchor["source_receipt_ids"], source_anchor_ids=anchor["anchor_id"], exact_locator=anchor["exact_locator"],
                evidence_level="official_irs_xml", review_status="ai_seeded", fact_status="research_only_recipient_candidate",
                leg_layer="LEG0", allowed_claim=anchor["allowed_claim"], prohibited_inference="The English descriptor is not yet an approved Japanese legal entity crosswalk; no recipient-side amount/period closure is implied.",
            )

    filing_by_case_period = {
        (case, start, end): (receipt, artifact, form)
        for case, start, end, form, receipt, artifact in CORE_FILINGS + MTS_FILINGS
        if artifact
    }
    oesc_anchor = {
        (a["period_start"], a["period_end"], a["value"]): a
        for a in anchors if a["case_id"] == "OESC_to_AWWA"
    }
    # Official Schedule I recipient and individual-assistance groups.
    for (case, start, end), (receipt, artifact, _form) in filing_by_case_period.items():
        root = ET.parse(artifact_path(output, artifact)).getroot()
        actor_id, actor_name = ACTORS[case]
        for ordinal, group in enumerate([e for e in root.iter() if lname(e) == "RecipientTable"], 1):
            v = group_values(group)
            target = v.get("BusinessNameLine1Txt", "")
            amount = v.get("CashGrantAmt", "")
            target_ein = v.get("RecipientEIN", "")
            inherited = oesc_anchor.get((start, end, amount)) if case == "OESC" and target_ein == "980227149" else None
            add(
                provider_case=case, source_actor_id=actor_id, source_actor_name=actor_name,
                target_id=("X004" if target_ein == "980227149" else ("EIN_" + target_ein if target_ein else "RECIP_UNREGISTERED")),
                target_name=target, target_kind="organization_recipient",
                period_start=start, period_end=end, amount=amount, currency="USD", amount_semantics="schedule_i_cash_grant",
                resource_type="cash_grant", purpose=v.get("PurposeOfGrantTxt", ""), reporting_layer="named_schedule_i",
                reconciliation_component="yes", dedupe_group_id=f"{case}-{end}-GRANTS", dedupe_status="component_of_grant_line_total",
                included_as_relation_candidate="yes", endpoint_identity_status=("registered_actor" if target_ein == "980227149" else "ein_or_name_observed_not_registry_crosswalked"),
                transaction_closure="provider_filing_named_recipient", source_receipt_ids=receipt,
                source_anchor_ids=(inherited["anchor_id"] if inherited else ""), exact_locator=f"official XML Schedule I RecipientTable[{ordinal}]",
                evidence_level="official_irs_xml", review_status=(inherited["review_status"] if inherited else "ai_seeded"),
                fact_status=("research_only_principal_confirmed_anchor" if inherited else "research_only_official_filing_candidate"), leg_layer="LEG0",
                allowed_claim=f"The filing reports a USD {amount} cash grant to the named recipient for this tax period.",
                prohibited_inference="This does not identify original donors, downstream recipients, political stance or legitimation effect.",
            )
        for ordinal, group in enumerate([e for e in root.iter() if lname(e) == "GrantsOtherAsstToIndivInUSGrp"], 1):
            v = group_values(group)
            desc, amount = v.get("GrantTypeTxt", ""), v.get("CashGrantAmt", "")
            kosc_awwa_misplaced = case == "KOSC" and amount == "2580" and "Welfare Association" in desc
            add(
                provider_case=case, source_actor_id=actor_id, source_actor_name=actor_name,
                target_id="HELD_KOSC_2580" if kosc_awwa_misplaced else "AGG_INDIVIDUAL_RECIPIENTS",
                target_name=desc, target_kind="individual_assistance_group_or_misplaced_name",
                period_start=start, period_end=end, amount=amount, currency="USD", amount_semantics="schedule_i_individual_assistance_group",
                resource_type="scholarship_or_individual_assistance", purpose=desc, reporting_layer="aggregate_individual_assistance",
                reconciliation_component="yes", dedupe_group_id=f"{case}-{end}-GRANTS", dedupe_status="component_of_grant_line_total",
                included_as_relation_candidate="no_defer" if kosc_awwa_misplaced else "no_aggregate_individuals",
                endpoint_identity_status="misplaced_name_semantics_deferred" if kosc_awwa_misplaced else "aggregate_not_actor",
                transaction_closure="defer_not_flow" if kosc_awwa_misplaced else "aggregate_only",
                source_receipt_ids=receipt, source_anchor_ids="", exact_locator=f"official XML Schedule I GrantsOtherAsstToIndivInUSGrp[{ordinal}]",
                evidence_level="official_irs_xml", review_status="needs_human_semantic_review" if kosc_awwa_misplaced else "ai_seeded",
                fact_status="research_only_held_not_relation" if kosc_awwa_misplaced else "research_only_official_filing_aggregate",
                leg_layer="LEG0", allowed_claim="The amount appears in the filing's individual-assistance group; it is not an organization grant edge." if kosc_awwa_misplaced else "The filing reports an aggregate individual-assistance category.",
                prohibited_inference="Do not create individual actors or an AWWA organization flow from this group.",
            )
        for ordinal, group in enumerate([e for e in root.iter() if lname(e) == "GrantsToOrgOutsideUSGrp"], 1):
            v = group_values(group)
            add(
                provider_case=case, source_actor_id=actor_id, source_actor_name=actor_name,
                target_id="AGG_OUTSIDE_US_ORG", target_name=v.get("PurposeOfGrantTxt", "outside-U.S. organization"), target_kind="outside_us_aggregate_no_name",
                period_start=start, period_end=end, amount=v.get("CashGrantAmt", ""), currency="USD", amount_semantics="schedule_f_aggregate_cash_grant",
                resource_type="cash_grant", purpose=v.get("PurposeOfGrantTxt", ""), reporting_layer="region_aggregate",
                reconciliation_component="yes", dedupe_group_id=f"{case}-{end}-GRANTS", dedupe_status="component_of_grant_line_total",
                included_as_relation_candidate="no_unnamed_endpoint", endpoint_identity_status="unnamed_aggregate", transaction_closure="aggregate_only",
                source_receipt_ids=receipt, exact_locator=f"official XML Schedule F GrantsToOrgOutsideUSGrp[{ordinal}]",
                evidence_level="official_irs_xml", review_status="ai_seeded", fact_status="research_only_official_filing_aggregate", leg_layer="LEG0",
                allowed_claim="The filing reports an outside-U.S. aggregate grant purpose and amount.", prohibited_inference="Do not infer the final organization identity from the purpose phrase.",
            )

    # MOSCO 990-EZ program-service grant categories.  FY2025 has a program
    # expense mentioning AWWA but no grants element; it is explicitly not a flow.
    for case, start, end, _form, receipt, artifact in CORE_FILINGS:
        if case != "MOSCO" or not artifact:
            continue
        root = ET.parse(W2_00 / artifact).getroot()
        for ordinal, group in enumerate([e for e in root.iter() if lname(e) == "ProgramSrvcAccomplishmentGrp"], 1):
            v = group_values(group)
            desc = v.get("DescriptionProgramSrvcAccomTxt", "")
            grant = v.get("GrantsAndAllocationsAmt", "")
            expense = v.get("ProgramServiceExpensesAmt", "")
            if grant:
                add(
                    provider_case="MOSCO", source_actor_id="X016", source_actor_name=ACTORS["MOSCO"][1],
                    target_id="AGG_MOSCO_PROGRAM_CATEGORY", target_name=desc, target_kind="program_category_no_named_endpoint",
                    period_start=start, period_end=end, amount=grant, currency="USD", amount_semantics="990ez_program_service_grants_and_allocations",
                    resource_type="grant_category", purpose=desc, reporting_layer="program_service_category",
                    reconciliation_component="yes", dedupe_group_id=f"MOSCO-{end}-GRANTS", dedupe_status="component_of_grant_line_total",
                    included_as_relation_candidate="no_unnamed_endpoint", endpoint_identity_status="aggregate_not_actor", transaction_closure="category_only",
                    source_receipt_ids=receipt, exact_locator=f"official XML ProgramSrvcAccomplishmentGrp[{ordinal}]",
                    evidence_level="official_irs_xml", review_status="ai_seeded", fact_status="research_only_official_filing_aggregate", leg_layer="LEG0",
                    allowed_claim="The filing reports this program-service grant category and amount.", prohibited_inference="The unnamed American 501(c)(3) is not automatically crosswalked to AWWA.",
                )
            elif "AWWA" in desc:
                add(
                    provider_case="MOSCO", source_actor_id="X016", source_actor_name=ACTORS["MOSCO"][1], target_id="X004", target_name=ACTORS["AWWA"][1], target_kind="named_in_program_description",
                    period_start=start, period_end=end, amount=expense, currency="USD", amount_semantics="program_service_expense_not_payment",
                    resource_type="program_activity_expense", purpose=desc, reporting_layer="program_service_description",
                    reconciliation_component="no", dedupe_group_id=f"MOSCO-{end}-PROGRAM", dedupe_status="not_a_grant_component_grant_field_absent",
                    included_as_relation_candidate="no_semantics_deferred", endpoint_identity_status="named_but_payment_semantics_unresolved", transaction_closure="not_a_dyadic_flow",
                    source_receipt_ids=receipt, exact_locator=f"official XML ProgramSrvcAccomplishmentGrp[{ordinal}]",
                    evidence_level="official_irs_xml", review_status="needs_human_semantic_review", fact_status="research_only_held_not_relation", leg_layer="LEG0",
                    allowed_claim="The filing describes a program supporting AWWA and reports a program-service expense; it does not report a grant amount.", prohibited_inference="Do not treat the USD 7,500 program expense as money paid to AWWA or turn a missing grants element into zero.",
                )

    # Reconcile unitemized residuals against each filing grant line.  AWWA uses
    # its complete two-bucket split; named rows are already marked as subsets.
    grant_total = {
        (str(r["case_id"]), str(r["period_start"]), str(r["period_end"])): int(str(r["value"]))
        for r in metrics if r["metric"] == "grants_and_similar_paid_usd" and str(r["value"]).strip()
    }
    component_sums: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in rows:
        if row["reconciliation_component"] == "yes" and str(row["amount"]).strip():
            component_sums[(str(row["provider_case"]), str(row["period_start"]), str(row["period_end"]))] += int(str(row["amount"]))
    for key, total in sorted(grant_total.items()):
        case, start, end = key
        residual = total - component_sums.get(key, 0)
        if residual < 0:
            raise AssertionError(f"negative reconciliation residual {key}: {residual}")
        if residual:
            actor_id, actor_name = ACTORS[case]
            receipt = filing_by_case_period.get(key, ("", "", ""))[0]
            add(
                provider_case=case, source_actor_id=actor_id, source_actor_name=actor_name,
                target_id="UNITEMIZED_OR_UNPARSED", target_name="unitemized or unparsed grant remainder", target_kind="reconciliation_residual",
                period_start=start, period_end=end, amount=str(residual), currency="USD", amount_semantics="computed_residual_of_official_grant_line",
                resource_type="unitemized_grant_remainder", purpose="reconciliation only", reporting_layer="derived_residual",
                reconciliation_component="yes", dedupe_group_id=f"{case}-{end}-GRANTS", dedupe_status="fills_to_grant_line_total",
                included_as_relation_candidate="no_unknown_endpoint", endpoint_identity_status="unknown", transaction_closure="not_closed",
                source_receipt_ids=receipt, exact_locator="grant line minus admitted filing components",
                evidence_level="derived_from_official_irs_xml", review_status="ai_seeded", fact_status="research_only_derived_reconciliation", leg_layer="LEG0",
                allowed_claim="This residual is the part of the official grant line not itemized by admitted component rows.", prohibited_inference="It is not a recipient, a dyadic flow or evidence that the remainder went to Okinawa organizations.",
            )

    # MTS narrative observations are deliberately non-additive to its IRS grant
    # lines unless an exact transaction is separately closed.
    narrative = [
        ("AGG_MTS_2023", "American and Japanese recipients (aggregate)", "mixed_aggregate", "", "126000", "minimum_more_than", "cash_and_or_in_kind_aggregate", "over USD 126,000 in 2023", "W2A2-SR018", "overlap_with_MTS_2023_grant_line_do_not_add"),
        ("AGG_MTS_JAPAN_2023", "local Japanese community (aggregate)", "recipient_bucket", "", "32606", "reported_subtotal", "community_support_aggregate", "local Japanese community subtotal", "W2A2-SR018", "subset_of_annual_aggregate_possible_AWWA_overlap"),
        ("AGG_MTS_SCHOLAR_2023", "military-affiliated scholarship recipients", "individual_aggregate", "", "12000", "reported_subtotal", "scholarships", "scholarships", "W2A2-SR018", "overlaps_MTS_2023_schedule_i_individual_group"),
        ("SMP", "Single Marine Program", "installation_program", "", "3000", "reported_subtotal", "program_support", "battle-site tours", "W2A2-SR018", "subset_of_annual_aggregate"),
        ("DODEA_PTO", "DoDEA Okinawa PTOs", "organization_aggregate", "", "13000", "reported_subtotal", "school_support", "PTO starter funds", "W2A2-SR018", "possible_overlap_with_named_Kubasaki_and_annual_aggregate"),
        ("ASHIBINA_CDC", "Ashibina Child Development Center families", "program_beneficiary_group", "", "350", "reported_in_kind_value", "in_kind_support", "diapers and wipes", "W2A2-SR018", "subset_of_annual_aggregate_in_kind_not_cash"),
        ("LIONS_OKINAWA", "Lions Clubs International, Okinawa intermediary", "organization_intermediary", "2024-02-22", "10000", "reported_cash_transfer", "donation_via_intermediary", "children with medical and special-education needs", "W2A2-SR018;W2A2-SR019", "possible_component_of_MTS_2024_unitemized_grant_remainder"),
        ("AGG_MTS_SELF_2023", "organizations in and around Okinawa (self-page aggregate)", "mixed_aggregate", "", "110000", "minimum_more_than", "grant_aggregate", "self-page says over USD 110,000", "W2A2-SR016", "definition_conflict_with_DVIDS_126k_do_not_choose_or_add"),
    ]
    for target_id, target_name, target_kind, event_date, amount, amount_semantics, resource_type, purpose, receipts, dedupe in narrative:
        add(
            provider_case="MTS", source_actor_id="X018", source_actor_name=ACTORS["MTS"][1], target_id=target_id, target_name=target_name, target_kind=target_kind,
            period_start="2023-01-01" if "2023" in target_id or target_id in {"SMP", "DODEA_PTO", "ASHIBINA_CDC"} else "",
            period_end="2023-12-31" if "2023" in target_id or target_id in {"SMP", "DODEA_PTO", "ASHIBINA_CDC"} else "",
            event_date=event_date, amount=amount, currency="USD", amount_semantics=amount_semantics, resource_type=resource_type, purpose=purpose,
            reporting_layer="official_military_public_affairs" if "SR018" in receipts else "organization_self_report",
            reconciliation_component="no", dedupe_group_id="MTS-2023-NARRATIVE" if not event_date else "MTS-2024-LIONS",
            dedupe_status=dedupe, included_as_relation_candidate="yes_pending_downstream_closure" if target_id == "LIONS_OKINAWA" else "no_aggregate_or_overlap",
            endpoint_identity_status="named_intermediary_final_recipients_aggregate" if target_id == "LIONS_OKINAWA" else "aggregate_or_program",
            transaction_closure="provider_to_intermediary_only" if target_id == "LIONS_OKINAWA" else "narrative_aggregate_only",
            source_receipt_ids=receipts, exact_locator="DVIDS 2024-02-22 article / MTS grants page",
            evidence_level="E4_source_bounded", review_status="ai_seeded", fact_status="research_only_narrative_observation", leg_layer="LEG0",
            allowed_claim="The cited source reports this source-bounded amount or aggregate.", prohibited_inference="Do not add this observation to IRS grant totals, infer final beneficiaries, political stance or a legitimation effect.",
        )

    # Filing-period reconciliation summaries.
    component_sums = defaultdict(int)
    named_sums = defaultdict(int)
    for row in rows:
        key = (str(row["provider_case"]), str(row["period_start"]), str(row["period_end"]))
        if row["reconciliation_component"] == "yes" and str(row["amount"]).strip():
            component_sums[key] += int(str(row["amount"]))
        if row["included_as_relation_candidate"] in {"yes", "yes_pending_identity_review"} and str(row["amount"]).strip():
            named_sums[key] += int(str(row["amount"]))
    summaries: list[dict[str, object]] = []
    for metric in [r for r in metrics if r["metric"] == "grants_and_similar_paid_usd"]:
        key = (str(metric["case_id"]), str(metric["period_start"]), str(metric["period_end"]))
        total_text = str(metric["value"])
        total = int(total_text) if total_text else None
        comp = component_sums.get(key, 0)
        summaries.append(
            {
                "case_id": key[0], "actor_id": metric["actor_id"], "period_start": key[1], "period_end": key[2],
                "grant_line_value": total_text, "currency": "USD", "admitted_reconciliation_components": comp if total is not None else "",
                "reconciliation_difference": (total - comp) if total is not None else "",
                "named_relation_candidate_amount": named_sums.get(key, 0),
                "named_amount_share_pct": round(named_sums.get(key, 0) / total * 100, 2) if total else "",
                "closure_status": "components_reconcile_to_grant_line" if total is not None and total == comp else ("grant_field_absent_not_zero" if total is None else "reconciliation_gap"),
                "dedupe_rule": "Use the grant line once. Component, bucket, named, residual and narrative rows are nested views and are never added on top of it.",
                "fact_status": "research_only",
            }
        )
    return rows, summaries


def build_recipient_leg2() -> list[dict[str, object]]:
    data = [
        ("W2A-A070", "Children Kana-san Okinawa", "全国医療的ケアライン沖縄支部 医療的ケア児(者)家族会『かなさん沖縄』", "15,287", "2022-06-01", "2023-05-31", "W2A2-SR004;W2A2-SR005;W2A2-SR006", "recipient_self_flyer_and_local_recipient_publication", "recipient-side flyer says the 2023 photo exhibition is operated with AWWA donations; a local recipient publication records thanks", "practical_use_and_gratitude", "amount_absent_no_exact_filing_row_closure", "high_candidate_needs_principal_crosswalk"),
        ("W2A-A071", "Okinawa Nanbu Rehabilitation and Medical Center", "沖縄南部療育医療センター（社会福祉法人沖縄肢体不自由児協会）", "14,870", "2022-06-01", "2023-05-31", "W2A2-SR009", "recipient_official_identity_only", "official facility identity located; no AWWA acknowledgment located in the bounded search", "no_leg2_found", "provider_filing_only", "high_candidate_needs_principal_crosswalk"),
        ("W2A-A072", "NPO ARU", "一般社団法人ある", "13,986", "2022-06-01", "2023-05-31", "W2A2-SR010;W2A2-SR011;W2A2-SR012", "organization_site_statute_and_gbiz_identity_only", "Okinawa organization candidate located; filing's generic NPO label conflicts with Japanese legal form", "no_leg2_found", "provider_filing_only", "medium_candidate_legal_form_mismatch"),
        ("W2A-A073", "Ambitious", "認定NPO法人アンビシャス", "13,423", "2023-06-01", "2024-05-31", "W2A2-SR006;W2A2-SR007;W2A2-SR008;W2A2-SR020;W2A2-SR021", "recipient_self_reports_and_independent_local_news", "recipient materials describe repeated AWWA support, equipment use and bridge language; a June 2024 report describes a separate JPY 2m donation", "practical_use_gratitude_and_bridge_narrative", "multiple_awwa_events_and_date_amount_mismatch_no_exact_row_closure", "high_candidate_needs_principal_transaction_match"),
        ("W2A-A074", "Himawari Day Care on Ishigaki Island", "石垣市障がい児通所支援事業所ひまわり（石垣市社会福祉協議会）", "13,378", "2023-06-01", "2024-05-31", "W2A2-SR013", "recipient_operator_newsletter", "November 2024 newsletter reports an August 9 AWWA JPY 2m donation and prior exchange activities", "practical_use_and_reciprocal_exchange_narrative", "newsletter_event_appears_after_filing_period_no_exact_row_closure", "high_candidate_needs_principal_date_match"),
        ("W2A-A075", "Okinawa Southern Medical Center", "沖縄県立南部医療センター・こども医療センター", "13,072", "2023-06-01", "2024-05-31", "W2A2-SR015", "prefectural_hospital_official_identity_only", "official hospital identity located; no AWWA acknowledgment located in the bounded search", "no_leg2_found", "provider_filing_only", "high_candidate_name_translation_needs_principal"),
    ]
    rows = []
    for idx, item in enumerate(data, 1):
        anchor, desc, candidate, amount, start, end, receipts, evidence, observation, response, closure, identity = item
        rows.append(
            {
                "recipient_review_id": f"RL{idx:03d}", "source_anchor_id": anchor, "filing_descriptor": desc,
                "candidate_canonical_name": candidate, "filing_amount_usd": amount.replace(",", ""), "period_start": start, "period_end": end,
                "identity_evidence_receipt_ids": receipts, "identity_status": identity,
                "recipient_side_evidence_type": evidence, "recipient_side_observation": observation,
                "leg2_candidate_class": response, "exact_transaction_closure": closure,
                "review_status": "needs_principal_review", "fact_status": "research_only_identity_and_leg2_candidate",
                "allowed_claim": "A plausible recipient identity and the stated recipient-side evidence type have been located for review.",
                "prohibited_inference": "Do not equate a later or amount-free acknowledgment with the exact filing row; gratitude or bridge language is not LEG3 acceptance of military presence.",
            }
        )
    return rows


def build_coverage(recipient_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    amounts = {str(r["period_end"]): int(str(r["filing_amount_usd"])) for r in []}
    year_data = [
        ("2023-05-31", 44143, 91838, 125158, 3),
        ("2024-05-31", 39873, 64077, 94889, 3),
        ("combined_two_tax_periods", 84016, 155915, 220047, 6),
    ]
    ack_count = sum(1 for r in recipient_rows if r["leg2_candidate_class"] != "no_leg2_found")
    rows = []
    for period, named, japan, total, count in year_data:
        rows.append(
            {
                "coverage_scope": period, "named_descriptor_count": count, "named_descriptor_amount_usd": named,
                "japanese_organization_bucket_usd": japan, "grant_line_total_usd": total,
                "named_share_of_japanese_bucket_pct": round(named / japan * 100, 2),
                "named_share_of_total_grants_pct": round(named / total * 100, 2),
                "identity_candidates_located": count,
                "recipient_side_awwa_acknowledgment_count": ack_count if period == "combined_two_tax_periods" else sum(1 for r in recipient_rows if r["period_end"] == period and r["leg2_candidate_class"] != "no_leg2_found"),
                "exact_amount_and_period_closed_count": 0,
                "coverage_interpretation": "Amount coverage measures how much of AWWA's filing bucket is attached to named English descriptors; LEG2 coverage separately counts recipient/local acknowledgments.",
                "prohibited_inference": "Neither percentage estimates the full recipient universe, social acceptance, beneficiary impact or legitimation.",
            }
        )
    return rows


def build_mediation(ledger: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    selected = [
        r for r in ledger
        if (r["source_actor_id"] in {"X007", "X018"} and r["target_id"] == "X004")
        or (r["source_actor_id"] == "X004" and r["target_kind"] in {"recipient_bucket", "filing_recipient_descriptor"})
        or (r["source_actor_id"] == "X018" and r["target_id"] == "LIONS_OKINAWA")
    ]
    for idx, row in enumerate(selected, 1):
        if row["source_actor_id"] in {"X007", "X018"} and row["target_id"] == "X004":
            channel = "inbound_to_awwa"
        elif row["source_actor_id"] == "X018":
            channel = "bypass_via_lions"
        else:
            channel = "awwa_outbound"
        rows.append(
            {
                "mediation_step_id": f"MS{idx:03d}", "channel_family": channel,
                "source_actor_id": row["source_actor_id"], "source_actor_name": row["source_actor_name"],
                "target_id": row["target_id"], "target_name": row["target_name"],
                "period_start": row["period_start"], "period_end": row["period_end"], "event_date": row["event_date"],
                "amount_usd": row["amount"], "source_receipt_ids": row["source_receipt_ids"], "review_status": row["review_status"],
                "transaction_closure": row["transaction_closure"],
                "interpretation": "AWWA receives repeated organization-level flows and reports onward allocations." if channel == "inbound_to_awwa" else ("MTS also reports a route outside AWWA, so AWWA is not the only channel." if channel == "bypass_via_lions" else "AWWA reports this outward bucket or named descriptor."),
                "prohibited_inference": "No earmarking connects a particular inbound dollar to a downstream recipient; periods differ and components must not be summed as one annual total.",
                "fact_status": "research_only",
            }
        )
    return rows


def build_mts_tracer(ledger: list[dict[str, object]], metrics: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    idx = 1
    for metric in metrics:
        if metric["case_id"] == "MTS":
            rows.append({
                "tracer_observation_id": f"MT{idx:03d}", "observation_type": "official_filing_metric", "period_or_date": metric["period_end"],
                "subject": metric["metric"], "value": metric["value"], "unit": "USD", "source_receipt_ids": metric["source_receipt_id"],
                "evidence_status": metric["fact_status"], "dedupe_or_boundary": metric["prohibited_inference"], "leg_layer": "LEG0", "review_status": metric["review_status"],
            }); idx += 1
    for flow in ledger:
        if flow["provider_case"] == "MTS" and flow["target_id"] in {"X004", "LIONS_OKINAWA", "AGG_MTS_2023", "AGG_MTS_SELF_2023"}:
            rows.append({
                "tracer_observation_id": f"MT{idx:03d}", "observation_type": flow["resource_type"], "period_or_date": flow["event_date"] or flow["period_end"],
                "subject": flow["target_name"], "value": flow["amount"], "unit": flow["currency"], "source_receipt_ids": flow["source_receipt_ids"],
                "evidence_status": flow["fact_status"], "dedupe_or_boundary": flow["dedupe_status"], "leg_layer": flow["leg_layer"], "review_status": flow["review_status"],
            }); idx += 1
    rows.append({
        "tracer_observation_id": f"MT{idx:03d}", "observation_type": "current_board_snapshot", "period_or_date": "observed 2026-08-22",
        "subject": "current officers and board roster", "value": "", "unit": "", "source_receipt_ids": "W2A2-SR017",
        "evidence_status": "organization_self_page_snapshot", "dedupe_or_boundary": "Observation date is not a filing term and does not replace Part VII.", "leg_layer": "LEG0", "review_status": "ai_seeded",
    })
    return rows


def build_review_queue(person_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    items = [
        ("person_identity", "Brooke Epps (AWWA) / Brooke Epp (KOSC)", "Are these filings referring to the same person?", "Name, role chronology and independent roster evidence", "Changes a cross-organization person bridge."),
        ("person_identity", "Jen Yapsing (AWWA) / Jennifer Yapshing (NOSCO)", "Same person or distinct people?", "Full names, roster pages and overlapping terms", "Changes a cross-organization person bridge."),
        ("person_identity", "Amber Tracy (OESC / AWWA exact string)", "Confirm exact-string cross-filing identity and term overlap.", "Independent roster/biographical corroboration", "Could establish a service-ecology person bridge; filing periods alone do not."),
        ("person_identity", "Trinicia Kloepper (AWWA / KOSC exact string)", "Confirm exact-string cross-filing identity and contemporaneous roles.", "Independent roster/biographical corroboration", "Could establish a repeated service-ecology person bridge."),
        ("recipient_identity", "NPO ARU / 一般社団法人ある", "Approve, revise or reject the crosswalk despite the legal-form mismatch.", "Organization site, statute and gBiz record", "Determines whether W2A-A072 can become a dyadic recipient flow."),
        ("recipient_identity", "Okinawa Nanbu Rehabilitation and Medical Center", "Confirm crosswalk to 沖縄南部療育医療センター.", "Facility/operator record plus historical recipient evidence", "Determines W2A-A071 endpoint identity."),
        ("recipient_identity", "Okinawa Southern Medical Center", "Confirm crosswalk to 沖縄県立南部医療センター・こども医療センター.", "Official hospital name and historical recipient evidence", "Determines W2A-A075 endpoint identity and keeps it distinct from Nanbu rehabilitation."),
        ("transaction_match", "Himawari JPY 2m on August 9", "Is this the event represented by the AWWA USD 13,378 row, or a later separate donation?", "Event year/date, exchange date and AWWA ledger", "Current newsletter timing appears after the filing period; exact row remains unclosed."),
        ("transaction_match", "Ambitious USD 13,423 / June 2024 JPY 2m", "Treat as separate events unless a ledger closes them?", "AWWA payment date and recipient bookkeeping", "Prevents a later donation from being used to validate the earlier filing row."),
        ("transaction_match", "Kana-san USD 15,287", "Does the amount-free 2023 flyer close the exact filing row?", "Recipient accounts or AWWA allocation record", "Current evidence supports recipient-side acknowledgment but not exact amount closure."),
        ("leg2_strength", "Recipient gratitude / bridge / cross-border-support wording", "Classify as gratitude, practical use, partner narration or stronger acceptance?", "Principal reads exact recipient/local passages", "Changes LEG2 subtype; cannot create LEG3 without an effect design."),
        ("filing_semantics", "MTS >USD 110k self-page / >USD 126k DVIDS / IRS USD 125,218", "Different definitions, publication snapshots or contradiction?", "Contemporaneous MTS report and transaction ledger", "Determines wording only; none of the three totals may be added together."),
        ("downstream_recipient", "MTS→Lions USD 10k", "Can final child-health organizations and their receipt be closed?", "Lions/local recipient announcement or accounts", "Current evidence closes provider→intermediary, not intermediary→final institutions or LEG2."),
        ("filing_semantics", "KOSC USD 2,580 descriptor in individual-assistance group", "Standing decision: continue defer; no organization flow.", "Corrected filing or independent payment record", "Already gated; no new decision required unless new primary evidence appears."),
        ("filing_semantics", "MOSCO FY2025 missing grants element / USD 7,500 program expense", "Can the program expense be shown to be an amount paid to AWWA?", "Schedule O detail, recipient record or ledger", "Until then blank is not zero and USD 7,500 is not a dyadic flow."),
        ("person_identity", "Lesilee Du Fresne / Lesilee DuFresne (OESC)", "Confirm spelling variant before longitudinal person merge.", "Independent roster or filing amendment", "Affects within-actor continuity, not yet a cross-actor bridge."),
    ]
    rows = []
    for idx, (kind, subject, question, evidence, impact) in enumerate(items, 1):
        rows.append({
            "review_item_id": f"W2A-HR{idx:03d}", "review_type": kind, "subject": subject, "question": question,
            "evidence_to_read": evidence, "why_it_matters": impact,
            "current_treatment": "standing_defer_no_action" if "Standing decision" in question else "unresolved_research_only",
            "principal_decision": "", "reviewer": "", "review_date": "", "review_status": "awaiting_principal" if "Standing decision" not in question else "principal_defer_carried_forward",
            "prohibited_inference": "No identity, exact transaction, LEG2 strength or dyadic flow is approved by this queue row.",
        })
    return rows


ENDPOINT_HANDOFF_FIELDS = [
    "handoff_row_id", "endpoint_family", "subject_id", "subject_name",
    "counterpart_id", "counterpart_name", "role_or_relation",
    "period_start", "period_end", "event_date", "amount", "currency",
    "source_receipt_ids", "source_observation_ids", "adjudication_status",
    "identity_status", "bridge_status", "transaction_closure", "leg_layer",
    "allowed_claim", "prohibited_inference",
]


def build_w2d_endpoint_handoff(
    person_rows: list[dict[str, object]],
    recipient_rows: list[dict[str, object]],
    ledger: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Export typed endpoints for W2-D without promoting candidates to bridges."""

    rows: list[dict[str, object]] = []

    def add(**kwargs: object) -> None:
        base = {field: "" for field in ENDPOINT_HANDOFF_FIELDS}
        base.update(kwargs)
        base["handoff_row_id"] = f"EH{len(rows) + 1:04d}"
        rows.append(base)

    # Every filing role stays an observation.  A repeated exact string is only
    # a disambiguation candidate, never a person identity or bridge by itself.
    for role in person_rows:
        is_cross_candidate = role["cross_actor_candidate"] == "yes"
        add(
            endpoint_family="person_role_observation",
            subject_id=role["person_key"],
            subject_name=role["name_as_filed"],
            counterpart_id=role["actor_id"],
            counterpart_name=role["actor_name"],
            role_or_relation=role["role_title_as_filed"],
            period_start=role["period_start"],
            period_end=role["period_end"],
            source_receipt_ids=role["source_receipt_id"],
            source_observation_ids=role["role_observation_id"],
            adjudication_status=role["review_status"],
            identity_status=role["identity_resolution_status"],
            bridge_status="candidate_not_confirmed" if is_cross_candidate else "not_assessed_for_bridge",
            transaction_closure="filing_role_string_only",
            allowed_claim=role["allowed_claim"],
            prohibited_inference=role["prohibited_inference"],
        )

    # Near-name candidates cannot be represented by a shared string key, so
    # they receive explicit pair rows.  Exact-string pairs are repeated here as
    # a compact decision queue for W2-D.
    pair_specs = [
        ("Brooke Epps", "X004", "Brooke Epp", "X006", "near_name_cross_actor_candidate"),
        ("Jen Yapsing", "X004", "Jennifer Yapshing", "X005", "near_name_cross_actor_candidate"),
        ("Amber Tracy", "X004", "AMBER TRACY", "X007", "exact_string_cross_actor_candidate"),
        ("Trinicia Kloepper", "X004", "Trinicia Kloepper", "X006", "exact_string_cross_actor_candidate"),
        ("Lesilee Du Fresne", "X007", "Lesilee DuFresne", "X007", "near_name_within_actor_continuity_candidate"),
    ]
    for left_name, left_actor, right_name, right_actor, status in pair_specs:
        matched = [
            role for role in person_rows
            if (normalize_name(str(role["name_as_filed"])), str(role["actor_id"]))
            in {
                (normalize_name(left_name), left_actor),
                (normalize_name(right_name), right_actor),
            }
        ]
        receipts = ";".join(sorted({str(r["source_receipt_id"]) for r in matched}))
        observations = ";".join(str(r["role_observation_id"]) for r in matched)
        starts = sorted(str(r["period_start"]) for r in matched)
        ends = sorted(str(r["period_end"]) for r in matched)
        add(
            endpoint_family="person_identity_pair_candidate",
            subject_id=f"PAIR_{person_key(left_name)}_{person_key(right_name)}",
            subject_name=f"{left_name} [{left_actor}]",
            counterpart_id=right_actor,
            counterpart_name=f"{right_name} [{right_actor}]",
            role_or_relation="possible_same_person",
            period_start=starts[0] if starts else "",
            period_end=ends[-1] if ends else "",
            source_receipt_ids=receipts,
            source_observation_ids=observations,
            adjudication_status="awaiting_principal",
            identity_status=status,
            bridge_status="candidate_not_confirmed" if left_actor != right_actor else "within_actor_continuity_candidate_not_bridge",
            transaction_closure="identity_not_resolved",
            allowed_claim="The listed filing name strings form a bounded identity-disambiguation candidate.",
            prohibited_inference="Do not merge the names, create a shared-person node or infer a cross-organization bridge before principal review.",
        )

    flow_by_anchor = {
        str(flow["source_anchor_ids"]): flow
        for flow in ledger
        if str(flow["source_anchor_ids"]).startswith("W2A-A07")
    }
    for recipient in recipient_rows:
        flow = flow_by_anchor.get(str(recipient["source_anchor_id"]), {})
        receipt_ids = ";".join(
            sorted(
                {
                    item
                    for item in (
                        str(flow.get("source_receipt_ids", "")) + ";" + str(recipient["identity_evidence_receipt_ids"])
                    ).split(";")
                    if item
                }
            )
        )
        add(
            endpoint_family="recipient_candidate",
            subject_id="X004",
            subject_name=ACTORS["AWWA"][1],
            counterpart_id=f"RECIP_DESC_{str(recipient['source_anchor_id']).split('-')[-1]}",
            counterpart_name=recipient["candidate_canonical_name"],
            role_or_relation=f"recipient_candidate/{recipient['leg2_candidate_class']}",
            period_start=recipient["period_start"],
            period_end=recipient["period_end"],
            amount=recipient["filing_amount_usd"],
            currency="USD",
            source_receipt_ids=receipt_ids,
            source_observation_ids=f"{recipient['recipient_review_id']};{recipient['source_anchor_id']}",
            adjudication_status=recipient["review_status"],
            identity_status=recipient["identity_status"],
            bridge_status="endpoint_candidate_not_bridge",
            transaction_closure=recipient["exact_transaction_closure"],
            leg_layer="LEG2_candidate" if recipient["leg2_candidate_class"] != "no_leg2_found" else "LEG0_identity_candidate",
            allowed_claim=recipient["allowed_claim"],
            prohibited_inference=recipient["prohibited_inference"],
        )

    relation_states = {"yes", "yes_pending_identity_review", "yes_pending_downstream_closure"}
    for flow in ledger:
        if flow["included_as_relation_candidate"] not in relation_states:
            continue
        adjudication = str(flow["review_status"])
        add(
            endpoint_family="organization_flow_observation",
            subject_id=flow["source_actor_id"],
            subject_name=flow["source_actor_name"],
            counterpart_id=flow["target_id"],
            counterpart_name=flow["target_name"],
            role_or_relation=flow["resource_type"],
            period_start=flow["period_start"],
            period_end=flow["period_end"],
            event_date=flow["event_date"],
            amount=flow["amount"],
            currency=flow["currency"],
            source_receipt_ids=flow["source_receipt_ids"],
            source_observation_ids=flow["flow_observation_id"],
            adjudication_status=adjudication,
            identity_status=flow["endpoint_identity_status"],
            bridge_status="relation_observed_not_cross_ecology_bridge" if adjudication == "human_checked" else "candidate_not_confirmed",
            transaction_closure=flow["transaction_closure"],
            leg_layer=flow["leg_layer"],
            allowed_claim=flow["allowed_claim"],
            prohibited_inference=flow["prohibited_inference"],
        )

    return rows


def build_negative_log() -> list[dict[str, object]]:
    rows = [
        ("Children Kana-san Okinawa", "recipient site + flyer + local recipient publication", "AWWA; 米国福祉; 寄付", "recipient_acknowledgment_found_amount_not_found", "Exact USD amount and bookkeeping period remain absent."),
        ("Okinawa Nanbu Rehabilitation and Medical Center", "facility/operator site", "AWWA; 米国福祉; American Welfare", "identity_found_no_awwa_acknowledgment", "Current official page is not a historical archive; absence is not proof of no donation."),
        ("NPO ARU", "organization site + statute + gBiz", "AWWA; 米国福祉; American Welfare", "identity_candidate_found_no_awwa_acknowledgment", "Legal-form mismatch remains unresolved."),
        ("Ambitious", "recipient publications + 2024 report + Ryukyu Shimpo", "AWWA; 米国福祉; 寄付", "multiple_acknowledgments_found_exact_filing_row_not_closed", "Repeated support creates event-matching ambiguity."),
        ("Himawari Ishigaki", "operator newsletter + municipal-directory attempt", "AWWA; 200万円; ひまわり", "recipient_acknowledgment_found_timing_mismatch", "Municipal PDF URL returned HTML and was not used as a source."),
        ("Okinawa Southern Medical Center", "prefectural hospital site", "AWWA; 米国福祉; American Welfare", "identity_found_no_awwa_acknowledgment", "No historical recipient ledger was exposed by the current site."),
        ("MTS Lions downstream", "DVIDS bilingual article + bounded exact-name probes", "Cancer Childrens Parents Association; Lions; Marine Thrift", "provider_to_intermediary_found_final_recipient_acknowledgment_not_found", "Do not synthesize a Lions→recipient edge."),
        ("MTS FY2022 official XML", "IRS 2023 annual index and 2023 bulk archive", "EIN 38-3924106; object 202301329349300730", "index_row_found_xml_not_admitted", "No FY2022 amount enters this package."),
    ]
    return [
        {
            "search_log_id": f"NS{idx:03d}", "subject": subject, "source_families_checked": families,
            "query_terms": query, "bounded_result": result, "remaining_gap": gap,
            "search_date": "2026-08-22", "search_scope": "bounded_online_followup_not_exhaustive",
            "allowed_claim": "The stated source families were checked with this bounded result.",
            "prohibited_inference": "A no-hit result is not evidence that no donation, relationship, response or record exists.",
        }
        for idx, (subject, families, query, result, gap) in enumerate(rows, 1)
    ]


def build_change_notes() -> list[dict[str, object]]:
    items = [
        ("official_source_upgrade", "MTS third-party IRS display", "Two official IRS bulk XML filings replace the display for FY2023/FY2024 amounts; FY2022 remains index-only.", "No third-party amount is promoted."),
        ("coverage_boundary", "five organizations × three periods", "Keep 14/15 official XML slots and one AWWA index-only gap; do not fill from third-party values.", "Trend claims for AWWA remain two-period."),
        ("identity_transaction_split", "English recipient descriptor resembled a Japanese entity", "Record identity candidate, recipient-side acknowledgment and exact amount/period closure as separate fields.", "Six candidates located; three acknowledgments; zero exact row closures."),
        ("dedupe_rule", "MTS self/DVIDS/IRS totals differ", "Retain each source-bounded observation and prohibit addition or silent selection.", "No synthetic MTS annual total is produced."),
        ("channel_overlap", "MTS 2024 Lions donation may sit inside an IRS residual", "Keep the dated route as a narrative candidate and mark possible overlap.", "The USD 10k is not added on top of the IRS grant line."),
        ("person_identity", "exact and near-name repetitions", "Create string keys only and route cross-actor/near-name candidates to principal review.", "No confirmed person bridge is produced."),
        ("missing_semantics", "MOSCO FY2025 grants element absent", "Keep blank and separate the USD 7,500 program expense description from payment semantics.", "No MOSCO→AWWA cash flow is produced."),
        ("standing_defer", "KOSC USD 2,580 sits in an individual-assistance group", "Carry the principal's defer; include only as a held filing component for reconciliation.", "It closes arithmetic but creates no organization relation."),
        ("period_alignment", "inbound and outbound filings use unlike tax periods", "Show dated steps without earmarking or annual aggregation.", "Five inbound observations cannot be summed as one annual AWWA inflow."),
        ("failed_fetch", "Ishigaki municipal PDF URL returned HTML", "Retain the artifact hash as a failed retrieval receipt but do not use it for identity evidence.", "Himawari identity relies on the operator newsletter in this package."),
    ]
    return [
        {
            "change_note_id": f"W2A-CN{idx:03d}", "change_type": kind, "trigger": trigger,
            "revised_treatment": treatment, "impact_on_results": impact,
            "requires_principal_decision": "yes" if kind in {"identity_transaction_split", "person_identity"} else "no",
            "status": "applied_research_only", "date": "2026-08-22",
        }
        for idx, (kind, trigger, treatment, impact) in enumerate(items, 1)
    ]


NEW_RECEIPTS = [
    ("W2A2-SR001", "Internal Revenue Service (IRS)", "Marine Thrift Shop Form 990 XML, tax year 2023", "official_irs_bulk_xml", "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_07A.zip", "artifacts/irs/mts_fy2023_202401989349301535.xml", "application/xml", "object 202401989349301535; EIN 38-3924106", "admitted"),
    ("W2A2-SR002", "Internal Revenue Service (IRS)", "Marine Thrift Shop Form 990 XML, tax year 2024", "official_irs_bulk_xml", "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_04A.zip", "artifacts/irs/mts_fy2024_202510939349300851.xml", "application/xml", "object 202510939349300851; EIN 38-3924106", "admitted"),
    ("W2A2-SR003", "Internal Revenue Service (IRS)", "Marine Thrift Shop FY2022 official index row", "official_irs_annual_index", "https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv", "", "text/csv", "EIN 38-3924106; object 202301329349300730", "index_only_xml_not_admitted"),
    ("W2A2-SR004", "かなさん沖縄", "親の会について", "recipient_organization_site", "https://kanasanokinawa.com/aboutus/", "artifacts/recipient/kanasan_about.html", "text/html", "全国医療的ケアライン沖縄支部・医療的ケア児(者)家族会", "admitted"),
    ("W2A2-SR005", "かなさん沖縄", "2023写真展募集チラシ", "recipient_organization_flyer", "https://kanasanokinawa.com/wp-content/uploads/2023/06/%E3%81%8B%E3%81%AA%E3%81%95%E3%82%93%E5%86%99%E7%9C%9F%E5%B1%952023-%E5%86%99%E7%9C%9F%E5%8B%9F%E9%9B%86%E3%83%81%E3%83%A9%E3%82%B7.pdf", "artifacts/recipient/kanasan_awwa_flyer_2023.pdf", "application/pdf", "page 1: AWWA寄付金によって運営", "admitted"),
    ("W2A2-SR006", "認定NPO法人アンビシャス", "難病情報誌アンビシャス253号", "recipient_publication", "https://www.ambitious.or.jp/magazine/253/", "artifacts/recipient/ambitious_magazine_253.html", "text/html", "AWWA lunch, recipient thanks and prior support", "admitted"),
    ("W2A2-SR007", "認定NPO法人アンビシャス", "2024年度活動報告", "recipient_annual_report", "https://www.ambitious.or.jp/userfiles/files/Activty2024.pdf", "artifacts/recipient/ambitious_activity_2024.pdf", "application/pdf", "pp.10,22: AWWA-supported equipment and historical line", "admitted"),
    ("W2A2-SR008", "琉球新報", "難病者への蓄電池貸出を可能に", "independent_local_news", "https://ryukyushimpo.jp/living/entry-3159307.html", "artifacts/recipient/ryukyu_ambitious_awwa_20240604.html", "text/html", "2024-06-04: JPY 2m and 33 power units", "admitted"),
    ("W2A2-SR009", "社会福祉法人沖縄肢体不自由児協会", "沖縄南部療育医療センター", "recipient_operator_site", "https://www.okishikyo.jp/nanbu/", "artifacts/recipient/nanbu_official.html", "text/html", "facility canonical identity", "admitted_identity_only"),
    ("W2A2-SR010", "一般社団法人ある", "公式サイト", "recipient_organization_site", "https://aru-okinawa.jp/", "artifacts/recipient/aru_official.html", "text/html", "organization name and activities", "admitted_identity_only"),
    ("W2A2-SR011", "一般社団法人ある", "定款", "recipient_organization_statute", "https://aru-okinawa.jp/wp-content/uploads/2025/01/teikan20201110.pdf", "artifacts/recipient/aru_statute.pdf", "application/pdf", "pp.1,6: legal name, Okinawa office and registration", "admitted_identity_only"),
    ("W2A2-SR012", "経済産業省 gBizINFO", "法人番号2360005006351", "official_corporate_registry", "https://info.gbiz.go.jp/hojin/ichiran?hojinBango=2360005006351", "artifacts/recipient/aru_gbizinfo.html", "text/html", "corporate number lookup", "admitted_identity_only"),
    ("W2A2-SR013", "石垣市社会福祉協議会", "社協通信 2024年11月", "recipient_operator_newsletter", "https://ros-cdn.s3.ap-northeast-1.amazonaws.com/hp/img/ros_keiyaku/14586/shakyo_2411.pdf", "artifacts/recipient/ishigaki_shakyo_news_202411.pdf", "application/pdf", "p.3: AWWA寄付金贈呈式, Aug 9, JPY 2m", "admitted"),
    ("W2A2-SR014", "石垣市", "障害福祉事業所一覧 URL retrieval", "official_directory_failed_fetch", "https://www.city.ishigaki.okinawa.jp/material/files/group/19/r7-jigyousyosyougai.pdf", "artifacts/recipient/ishigaki_city_disability_services_r7.pdf", "text/html", "URL returned HTML, not a PDF", "not_admitted_http_html_response"),
    ("W2A2-SR015", "沖縄県立南部医療センター・こども医療センター", "公式サイト", "prefectural_hospital_site", "https://nanbuweb.hosp.pref.okinawa.jp/", "artifacts/recipient/southern_medical_center_official.html", "text/html", "hospital canonical identity", "admitted_identity_only"),
    ("W2A2-SR016", "Marine Thrift Shop Okinawa", "Grants", "organization_self_report", "https://marinethriftshopokinawa.org/grants/", "artifacts/tracer/mts_grants.html", "text/html", "AWWA member/contributor statement and 2023 recipient roster", "admitted_source_bounded"),
    ("W2A2-SR017", "Marine Thrift Shop Okinawa", "Board members", "organization_roster", "https://marinethriftshopokinawa.org/board-members/", "artifacts/tracer/mts_board.html", "text/html", "current observation-day roster", "admitted_snapshot"),
    ("W2A2-SR018", "Marine Corps Installations Pacific / DVIDS", "Marine Thrift Shop donates $10,000", "official_military_public_affairs", "https://www.dvidshub.net/news/465683/marine-thrift-shop-donates-10000-support-okinawa-childrens-hospitals", "artifacts/tracer/dvids_mts_lions_20240222.html", "text/html", "2024-02-22 article and 2023 giving summary", "admitted_source_bounded"),
    ("W2A2-SR019", "Marine Corps Installations Pacific / DVIDS", "Bilingual article PDF", "official_military_public_affairs", "https://d34w7g4gy10iej.cloudfront.net/pubs/pdf_71034.pdf", "artifacts/tracer/dvids_mts_lions_bilingual.pdf", "application/pdf", "Marine Thrift Shop→Lions account", "admitted_source_bounded"),
    ("W2A2-SR020", "認定NPO法人アンビシャス", "難病情報誌アンビシャス212号", "recipient_publication", "https://www.ambitious.or.jp/magazine/212/", "artifacts/recipient/ambitious_magazine_212.html", "text/html", "AWWA support observation", "admitted"),
    ("W2A2-SR021", "認定NPO法人アンビシャス", "難病情報誌アンビシャス265号", "recipient_publication", "https://www.ambitious.or.jp/magazine/265/", "artifacts/recipient/ambitious_magazine_265.html", "text/html", "AWWA support observation", "admitted"),
]


def build_receipts(output: Path) -> list[dict[str, object]]:
    upstream = read_csv(W2_00 / "source_receipts_v1.csv")
    rows: list[dict[str, object]] = []
    for r in upstream:
        rows.append({
            "receipt_id": r["receipt_id"], "publisher": r["publisher"], "title": r["title"], "source_family": r["source_family"],
            "url": r["url"], "retrieved_at": r["retrieved_at"], "artifact_path": r["artifact_path"], "sha256": r["sha256"],
            "mime_type": r["mime_type"], "exact_locator": r["exact_locator"], "archive_status": r["archive_status"],
            "supports_outputs": "filing_period_register;filing_metric_long;person_actor_role_time;resource_flow_ledger", "notes": "Inherited byte-for-byte receipt metadata from the principal-confirmed W2-00 package.",
        })
    for receipt_id, publisher, title, family, url, rel, mime, locator, status in NEW_RECEIPTS:
        path = output / rel if rel else None
        rows.append({
            "receipt_id": receipt_id, "publisher": publisher, "title": title, "source_family": family, "url": url,
            "retrieved_at": FIXED_AT, "artifact_path": (str(path.relative_to(ROOT)).replace("\\", "/") if path else ""),
            "sha256": sha256(path) if path and path.exists() else "", "mime_type": mime, "exact_locator": locator,
            "archive_status": status, "supports_outputs": "recipient_identity_leg2;marine_thrift_shop_tracer;resource_flow_ledger",
            "notes": "Research-only source receipt; inclusion does not approve an actor, relation, transaction match, LEG2 subtype or LEG3 effect.",
        })
    return rows


def render_mediation_svg(rows: list[dict[str, object]], output: Path) -> None:
    inbound = sum(1 for r in rows if r["channel_family"] == "inbound_to_awwa")
    outbound = sum(1 for r in rows if r["channel_family"] == "awwa_outbound")
    bypass = sum(1 for r in rows if r["channel_family"] == "bypass_via_lions")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620">
<rect width="1200" height="620" fill="#f7f5ef"/><style>text{{font-family:Arial,"Noto Sans CJK SC",sans-serif;fill:#12343b}} .h{{font-size:27px;font-weight:700}} .b{{font-size:18px}} .s{{font-size:14px;fill:#536d72}} .box{{fill:#FFFFFF;stroke:#84a8a8;stroke-width:2}} .a{{stroke:#147d80;stroke-width:4;fill:none;marker-end:url(#m)}} .d{{stroke:#c58a29;stroke-width:4;stroke-dasharray:9 7;fill:none;marker-end:url(#m2)}}</style>
<defs><marker id="m" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#147d80"/></marker><marker id="m2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#c58a29"/></marker></defs>
<text x="55" y="55" class="h">AWWA intermediary structure — research-only observations</text><text x="55" y="83" class="s">Tax periods differ; arrows are filing observations, not earmarked dollar chains.</text>
<rect x="60" y="155" width="250" height="95" rx="14" fill="#FFFFFF" stroke="#84a8a8" stroke-width="2"/><text x="85" y="195" class="b">OESC (3 filing periods)</text><text x="85" y="223" class="s">official Schedule I → AWWA</text>
<rect x="60" y="315" width="250" height="95" rx="14" fill="#FFFFFF" stroke="#84a8a8" stroke-width="2"/><text x="85" y="355" class="b">Marine Thrift Shop (2)</text><text x="85" y="383" class="s">official Schedule I → AWWA</text>
<rect x="465" y="220" width="270" height="130" rx="18" fill="#e6f2ef" stroke="#147d80" stroke-width="3"/><text x="525" y="270" class="h">AWWA</text><text x="495" y="305" class="s">allocation intermediary</text>
<rect x="875" y="135" width="255" height="95" rx="14" fill="#FFFFFF" stroke="#84a8a8" stroke-width="2"/><text x="900" y="176" class="b">Japanese-org bucket</text><text x="900" y="204" class="s">6 named descriptors inside</text>
<rect x="875" y="300" width="255" height="95" rx="14" fill="#FFFFFF" stroke="#84a8a8" stroke-width="2"/><text x="900" y="341" class="b">Base-affiliated bucket</text><text x="900" y="369" class="s">aggregate only</text>
<rect x="465" y="455" width="270" height="90" rx="14" fill="#FFFFFF" stroke="#84a8a8" stroke-width="2"/><text x="495" y="493" class="b">Lions intermediary</text><text x="495" y="521" class="s">final recipients not closed</text>
<path d="M310 202 C380 202,390 255,465 270" class="a"/><path d="M310 362 C390 362,395 320,465 300" class="a"/><path d="M735 270 C805 245,820 190,875 185" class="a"/><path d="M735 305 C805 315,820 345,875 348" class="a"/><path d="M310 380 C380 430,405 480,465 495" class="d"/>
<text x="55" y="585" class="s">Observed steps: {inbound} inbound · {outbound} AWWA outbound bucket/named rows · {bypass} bypass candidate. No LEG3 effect is measured.</text></svg>'''
    (output / "fig_awwa_mediation_structure_v1.svg").write_text(svg, encoding="utf-8")


def build_readme(output: Path, counts: dict[str, int]) -> None:
    text = f"""# W2-A：军属俱乐部资源网络与受赠端核查 v1

日期：2026-08-22  
状态：`research_only / principal_review_pending`。本包没有写回中央事实、旧 43 行、publication adapter、前端或控制文档。

## 1. 完成状态

- 五家核心组织登记 **15 个目标税期**，其中 **14 份官方 IRS XML** 可用；AWWA 第三税期维持官方 index-only gap。
- Marine Thrift Shop 渠道 tracer 新增 **2 份官方 IRS XML**，第三期只见官方索引。
- `filing_metric_long_v1.csv` 有 **{counts['metric_rows']} 条**组织×税期×指标长表记录。
- `person_actor_role_time_v1.csv` 有 **{counts['person_rows']} 条** filing-role observations；它们是姓名字符串×组织×申报期，不是已消歧人物网络。
- `resource_flow_ledger_v1.csv` 有 **{counts['resource_rows']} 条**类型化资金／物资／服务观察，所有总额、子项、bucket、residual 与宣传口径均带去重字段。
- 六个 AWWA 英文 recipient descriptor 均找到日文实体候选；**3/6** 找到 recipient 自身或地方侧 AWWA 回应；**0/6** 闭合到同一申报行的金额与税期。
- 建立 **{counts['review_items']} 项**负责人复核队列和 **{counts['negative_logs']} 条**有界负检索日志。

验证：`validation_report_v1.json` = `PASS_RESEARCH_ONLY_W2_A`。

## 2. 目前最强、但仍有边界的发现

### AWWA 是重复出现的分配中介，不是唯一渠道

官方申报现在显示两种重复输入：OESC 连续三期向 AWWA 报告 USD 16,308、14,371、8,479；Marine Thrift Shop 两期向 AWWA 报告 USD 41,183、19,669。AWWA 自身两期又把拨出分成日本组织与基地关联组织两个桶。因此可以把 AWWA 描述为**多家军属组织反复使用的分配中介**。

但这不是一条可追踪的“某笔上游钱→某个下游 recipient”链：各组织税期不同，AWWA 申报不提供 earmarking。五笔输入不能相加成某一年度收入，也不能分摊给六个具名 recipient。

Marine Thrift Shop 另有一条 2024-02-22 经 Lions 的 USD 10,000 路径；行动方明确说这是首次绕开 AWWA 直接选择地方组织。它支持“AWWA 重要但并非唯一渠道”，但当前只闭合 MTS→Lions，未闭合 Lions→最终机构。

### AWWA 的具名端点只覆盖拨出的一部分

两期六个具名描述合计 USD 84,016，占日本组织桶 USD 155,915 的 **53.89%**，占两期 grant line USD 220,047 的 **38.18%**。分期分别为：FY ending 2023，48.06%／35.27%；FY ending 2024，62.23%／42.02%。其余部分仍是汇总桶或未具名端点。

这两个百分比是**申报可见度**，不是受益覆盖、地方接受度或完整 recipient universe。

### recipient 回应能做到 LEG2，但不能越级为合法性效果

Kana-san 的自有传单说明写真展由 AWWA 捐款运营；Ambitious 的自有材料记录设备、会报和彩印等具体用途，并出现“冲绳与美国的桥”叙事；石垣市社协的 2024 年通讯记录向“ひまわり”赠款及既有交流。它们支持 practical use、gratitude、bridge narrative 等 LEG2 候选。

Ambitious 与 Himawari 的金额／日期并不与当前 AWWA 申报行直接闭合；这些话语也没有测量地方对美军存在的态度变化。因此本包不生成 LEG3。

## 3. 什么证据会削弱或推翻当前解释

1. AWWA 或 recipient 账簿若表明 OESC／MTS 输入全部指定给基地内部项目，会削弱“跨基地—地方中介”的范围。
2. 若六个英文 descriptor 中的日文实体 crosswalk 被否决，具名端点与 LEG2 覆盖率都应下调。
3. 若 MTS→Lions 的最终 recipient 无法核实，绕行路径只能停在中介层；若实际仍由 AWWA 决定，则“绕开”解释应撤回。
4. recipient 侧若把捐赠明确重释为权利、补偿或行政责任，或拒绝伙伴叙事，会削弱“关系建构叙事被接受”的机制。
5. 独立调查若显示服务曝光与态度无变化／反向变化，将反驳任何合法性效果；本包目前没有这类 LEG3 设计。
6. 同期原始账簿若解释 MTS 的 >110k、>126k 与 IRS 125,218 为不同口径，当前“口径冲突”可收紧；否则不得任选一个当真值。

## 4. 负责人必须判断

`principal_review_queue_v1.csv` 集中列出：4 组跨组织人物／近名消歧、3 个 recipient name crosswalk、Kana-san／Ambitious／Himawari 的 exact transaction match、LEG2 分类强度、MTS 三种 2023 总额口径、Lions 下游、MOSCO USD 7,500 语义与 KOSC USD 2,580 standing defer。

在负责人处理前：exact-string 人名只算候选，六个 recipient 不进入中央关系，KOSC 2,580 不生成 flow，MOSCO blank 不改成 0。

## 5. 文件

| 文件 | 用途 |
|---|---|
| `filing_period_register_v1.csv` | 五家 15 槽 + MTS 三槽覆盖 |
| `filing_metric_long_v1.csv` | 组织×税期×四指标长表 |
| `person_actor_role_time_v1.csv` | 官方申报中的姓名—组织—职务—税期观察 |
| `resource_flow_ledger_v1.csv` | 类型化资金／物资／服务观察与去重字段 |
| `resource_flow_dedup_summary_v1.csv` | 各申报 grant line 的组件闭合 |
| `awwa_recipient_identity_leg2_v1.csv` | 六端点身份、受赠端证据和 LEG2 候选 |
| `recipient_coverage_v1.csv` | named/bucket/total 与回应覆盖率 |
| `awwa_mediation_structure_v1.csv` | AWWA 输入、输出与 MTS 绕行步骤 |
| `marine_thrift_shop_tracer_v1.csv` | MTS filing 与渠道观察 |
| `negative_search_log_v1.csv` | no-hit 与未闭合端点，不作现实零关系 |
| `principal_review_queue_v1.csv` | 正式负责人判断队列 |
| `w2d_endpoint_handoff_v1.csv` | 给 W2-D 的人物、recipient 与组织流端点；候选不升格为 bridge |
| `source_receipts_v1.csv` | 官方 IRS、recipient、地方与 tracer 收据／哈希 |
| `change_notes_v1.csv` | 口径调整与影响 |
| `fig_awwa_mediation_structure_v1.svg` | 中介结构解释图 |

## 6. 复现

```powershell
python scripts/build_us_presence_network_wave2_w2_a_v1.py
python -m unittest tests.test_build_us_presence_network_wave2_w2_a_v1
```

脚本只重建本包的派生 CSV／SVG／README／validation／manifest，原始网络收据已冻结在 `artifacts/`；W2-00 的 14 份核心 IRS XML 通过原包路径与哈希引用。

## 7. 不得误读为

- 不是五家组织的合并年度财报或全冲绳生态总额；
- 不是上游捐款到下游 recipient 的 earmarked money trail；
- 不是六个 recipient identity、人物桥或 KOSC/MOSCO 敏感语义的人审结果；
- 不是 recipient 感谢等于对军事存在的接受；
- 不是中央写回、publication 或前端发布授权。
"""
    (output / "README.md").write_text(text, encoding="utf-8")


def write_manifest(output: Path) -> dict[str, object]:
    files = []
    for path in sorted(p for p in output.rglob("*") if p.is_file() and p.name != "manifest.json"):
        files.append({"path": str(path.relative_to(output)).replace("\\", "/"), "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {
        "package": "us_presence_network_wave2_w2_a_v1",
        "generated_at": FIXED_AT,
        "status": "research_only_principal_review_pending",
        "files": files,
        "prohibited_writes": ["central facts", "legacy 43 rows", "publication adapter", "frontend", "control documents"],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def build(output: Path = DEFAULT_OUT) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    protected_before = {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p) for p in PROTECTED if p.exists()}

    register = build_filing_register(output)
    metrics = build_metric_long(output, register)
    people = build_person_roles(output, register)
    ledger, dedup = build_resource_ledger(output, metrics)
    recipient = build_recipient_leg2()
    coverage = build_coverage(recipient)
    mediation = build_mediation(ledger)
    tracer = build_mts_tracer(ledger, metrics)
    review = build_review_queue(people)
    endpoint_handoff = build_w2d_endpoint_handoff(people, recipient, ledger)
    negative = build_negative_log()
    changes = build_change_notes()
    receipts = build_receipts(output)

    write_csv(output / "filing_period_register_v1.csv", list(register[0]), register)
    write_csv(output / "filing_metric_long_v1.csv", list(metrics[0]), metrics)
    write_csv(output / "person_actor_role_time_v1.csv", list(people[0]), people)
    write_csv(output / "resource_flow_ledger_v1.csv", FLOW_FIELDS, ledger)
    write_csv(output / "resource_flow_dedup_summary_v1.csv", list(dedup[0]), dedup)
    write_csv(output / "awwa_recipient_identity_leg2_v1.csv", list(recipient[0]), recipient)
    write_csv(output / "recipient_coverage_v1.csv", list(coverage[0]), coverage)
    write_csv(output / "awwa_mediation_structure_v1.csv", list(mediation[0]), mediation)
    write_csv(output / "marine_thrift_shop_tracer_v1.csv", list(tracer[0]), tracer)
    write_csv(output / "principal_review_queue_v1.csv", list(review[0]), review)
    write_csv(output / "w2d_endpoint_handoff_v1.csv", ENDPOINT_HANDOFF_FIELDS, endpoint_handoff)
    write_csv(output / "negative_search_log_v1.csv", list(negative[0]), negative)
    write_csv(output / "change_notes_v1.csv", list(changes[0]), changes)
    write_csv(output / "source_receipts_v1.csv", list(receipts[0]), receipts)
    render_mediation_svg(mediation, output)

    counts = {
        "filing_slots": len(register),
        "core_five_target_slots": sum(r["cohort"] == "core_five" for r in register),
        "core_five_official_xml": sum(r["cohort"] == "core_five" and r["coverage_status"] == "official_irs_xml_frozen" for r in register),
        "mts_official_xml": sum(r["cohort"] == "marine_thrift_shop_tracer" and r["coverage_status"] == "official_irs_xml_frozen" for r in register),
        "metric_rows": len(metrics), "person_rows": len(people), "resource_rows": len(ledger),
        "recipient_rows": len(recipient), "recipient_side_awwa_acknowledgments": sum(r["leg2_candidate_class"] != "no_leg2_found" for r in recipient),
        "exact_recipient_transaction_closures": sum("no_exact" not in str(r["exact_transaction_closure"]) and r["exact_transaction_closure"] not in {"provider_filing_only"} for r in recipient),
        "mediation_rows": len(mediation), "review_items": len(review), "w2d_endpoint_handoff_rows": len(endpoint_handoff),
        "negative_logs": len(negative), "source_receipts": len(receipts),
    }
    build_readme(output, counts)

    artifact_receipts = [r for r in receipts if r["artifact_path"]]
    hash_ok = all((ROOT / str(r["artifact_path"])).exists() and sha256(ROOT / str(r["artifact_path"])) == r["sha256"] for r in artifact_receipts)
    protected_after = {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p) for p in PROTECTED if p.exists()}
    oesc_awwa = [r for r in ledger if r["source_actor_id"] == "X007" and r["target_id"] == "X004" and r["transaction_closure"] == "provider_filing_named_recipient"]
    mts_awwa = [r for r in ledger if r["source_actor_id"] == "X018" and r["target_id"] == "X004" and r["transaction_closure"] == "provider_filing_named_recipient"]
    kosc_2580 = [r for r in ledger if r["target_id"] == "HELD_KOSC_2580"]
    mosco_latest = [r for r in metrics if r["case_id"] == "MOSCO" and r["period_end"] == "2025-05-31" and r["metric"] == "grants_and_similar_paid_usd"]
    checks = {
        "core_five_14_of_15_official_xml": counts["core_five_target_slots"] == 15 and counts["core_five_official_xml"] == 14,
        "mts_2_of_3_official_xml": counts["mts_official_xml"] == 2,
        "six_recipient_candidates": counts["recipient_rows"] == 6,
        "three_recipient_side_acknowledgments": counts["recipient_side_awwa_acknowledgments"] == 3,
        "zero_exact_recipient_row_closures": counts["exact_recipient_transaction_closures"] == 0,
        "oesc_three_principal_confirmed_anchors": len(oesc_awwa) == 3 and all(r["review_status"] == "human_checked" for r in oesc_awwa),
        "mts_two_official_candidate_flows_to_awwa": len(mts_awwa) == 2 and all(r["review_status"] == "ai_seeded" for r in mts_awwa),
        "kosc_2580_held_not_relation": len(kosc_2580) == 1 and kosc_2580[0]["included_as_relation_candidate"] == "no_defer",
        "mosco_latest_blank_not_zero": len(mosco_latest) == 1 and mosco_latest[0]["value"] == "" and mosco_latest[0]["field_semantics"] == "xml_element_absent_not_zero",
        "no_leg3_rows": not any(str(r.get("leg_layer", "")).upper() == "LEG3" for r in ledger + tracer),
        "w2d_candidates_not_promoted_to_bridges": not any(
            r["bridge_status"] in {"confirmed_bridge", "audited_public_record_zero"}
            for r in endpoint_handoff
        ),
        "source_artifact_hashes_match": hash_ok,
        "protected_central_hashes_unchanged": protected_before == protected_after,
        "all_dedup_summaries_close_or_explicit_blank": all(r["closure_status"] in {"components_reconcile_to_grant_line", "grant_field_absent_not_zero"} for r in dedup),
    }
    status = "PASS_RESEARCH_ONLY_W2_A" if all(checks.values()) else "FAIL_W2_A_VALIDATION"
    report = {"status": status, "generated_at": FIXED_AT, "counts": counts, "checks": checks, "protected_hashes": protected_after}
    (output / "validation_report_v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_manifest(output)
    if status.startswith("FAIL"):
        raise AssertionError(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2))
