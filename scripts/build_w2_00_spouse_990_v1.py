#!/usr/bin/env python3
"""Build the W2-00 AWWA / spouse-club official IRS anchor package.

This is an additive research-only builder.  It reads already frozen official IRS
bulk XML members and the pre-existing third-party render cache, then writes only
the dedicated W2-00 output directory.  It never assigns central source IDs or
updates central fact, relation, publication, or frontend layers.
"""

from __future__ import annotations

import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_00_spouse_990_v1"
RAW = OUT / "raw"
CACHE = ROOT / "tmp" / "service_recon_990"
RETRIEVED_AT = "2026-08-22T01:48:41+08:00"

ANCHOR_FIELDS = [
    "anchor_id",
    "case_id",
    "metric",
    "level",
    "period_start",
    "period_end",
    "period_semantics",
    "value",
    "value_text",
    "unit",
    "currency",
    "definition",
    "denominator_id",
    "source_receipt_ids",
    "exact_locator",
    "anchor_status",
    "observed_local",
    "gap_type",
    "null_model",
    "allowed_claim",
    "prohibited_inference",
    "review_status",
]

RECEIPT_FIELDS = [
    "receipt_id",
    "publisher",
    "title",
    "source_family",
    "url",
    "retrieved_at",
    "artifact_path",
    "sha256",
    "mime_type",
    "exact_locator",
    "supports_anchor_ids",
    "archive_status",
    "notes",
]

CHANGE_FIELDS = [
    "change_note_id",
    "case_id",
    "change_type",
    "trigger",
    "previous_assumption",
    "revised_treatment",
    "impact_on_numbers",
    "impact_on_claims",
    "evidence_receipt_ids",
    "requires_principal_decision",
    "status",
]

FILINGS = [
    {
        "case_id": "AWWA",
        "ein": "980227149",
        "form": "990EZ",
        "period_start": "2022-06-01",
        "period_end": "2023-05-31",
        "object_id": "202410619349200461",
        "receipt_id": "W2A-SR001",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_03A.zip",
        "artifact": "raw/awwa_fy2023_202410619349200461.xml",
    },
    {
        "case_id": "AWWA",
        "ein": "980227149",
        "form": "990EZ",
        "period_start": "2023-06-01",
        "period_end": "2024-05-31",
        "object_id": "202443189349200514",
        "receipt_id": "W2A-SR002",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11A.zip",
        "artifact": "raw/awwa_fy2024_202443189349200514.xml",
    },
    {
        "case_id": "KOSC",
        "ein": "980214323",
        "form": "990",
        "period_start": "2022-06-01",
        "period_end": "2023-05-31",
        "object_id": "202430969349301028",
        "receipt_id": "W2A-SR003",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_04A.zip",
        "artifact": "raw/kosc_fy2023_202430969349301028.xml",
    },
    {
        "case_id": "KOSC",
        "ein": "980214323",
        "form": "990",
        "period_start": "2023-06-01",
        "period_end": "2024-05-31",
        "object_id": "202500669349300300",
        "receipt_id": "W2A-SR004",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_03A.zip",
        "artifact": "raw/kosc_fy2024_202500669349300300.xml",
    },
    {
        "case_id": "KOSC",
        "ein": "980214323",
        "form": "990",
        "period_start": "2024-06-01",
        "period_end": "2025-05-31",
        "object_id": "202630129349300153",
        "receipt_id": "W2A-SR005",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_01A.zip",
        "artifact": "raw/irs_202630129349300153_public.xml",
    },
    {
        "case_id": "MOSCO",
        "ein": "460598583",
        "form": "990EZ",
        "period_start": "2022-06-01",
        "period_end": "2023-05-31",
        "object_id": "202410719349201281",
        "receipt_id": "W2A-SR006",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_03A.zip",
        "artifact": "raw/mosco_fy2023_202410719349201281.xml",
    },
    {
        "case_id": "MOSCO",
        "ein": "460598583",
        "form": "990EZ",
        "period_start": "2023-06-01",
        "period_end": "2024-05-31",
        "object_id": "202501019349201215",
        "receipt_id": "W2A-SR007",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_04A.zip",
        "artifact": "raw/mosco_fy2024_202501019349201215.xml",
    },
    {
        "case_id": "MOSCO",
        "ein": "460598583",
        "form": "990EZ",
        "period_start": "2024-06-01",
        "period_end": "2025-05-31",
        "object_id": "202621539349200807",
        "receipt_id": "W2A-SR008",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_06A.zip",
        "artifact": "raw/mosco_fy2025_202621539349200807.xml",
    },
    {
        "case_id": "NOSCO",
        "ein": "980210979",
        "form": "990",
        "period_start": "2022-07-01",
        "period_end": "2023-06-30",
        "object_id": "202411349349304281",
        "receipt_id": "W2A-SR009",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_05A.zip",
        "artifact": "raw/nosco_fy2023_202411349349304281.xml",
    },
    {
        "case_id": "NOSCO",
        "ein": "980210979",
        "form": "990",
        "period_start": "2023-07-01",
        "period_end": "2024-06-30",
        "object_id": "202530159349302288",
        "receipt_id": "W2A-SR010",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_01A.zip",
        "artifact": "raw/nosco_fy2024_202530159349302288.xml",
    },
    {
        "case_id": "NOSCO",
        "ein": "980210979",
        "form": "990",
        "period_start": "2024-07-01",
        "period_end": "2025-06-30",
        "object_id": "202533199349301708",
        "receipt_id": "W2A-SR011",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_11B.zip",
        "artifact": "raw/nosco_fy2025_202533199349301708.xml",
    },
    {
        "case_id": "OESC",
        "ein": "980346507",
        "form": "990",
        "period_start": "2022-07-01",
        "period_end": "2023-06-30",
        "object_id": "202411309349303066",
        "receipt_id": "W2A-SR012",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_05A.zip",
        "artifact": "raw/oesc_fy2023_202411309349303066.xml",
    },
    {
        "case_id": "OESC",
        "ein": "980346507",
        "form": "990",
        "period_start": "2023-07-01",
        "period_end": "2024-06-30",
        "object_id": "202403029349300610",
        "receipt_id": "W2A-SR013",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11A.zip",
        "artifact": "raw/oesc_fy2024_202403029349300610.xml",
    },
    {
        "case_id": "OESC",
        "ein": "980346507",
        "form": "990",
        "period_start": "2024-07-01",
        "period_end": "2025-06-30",
        "object_id": "202513109349302911",
        "receipt_id": "W2A-SR014",
        "zip_url": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_11D.zip",
        "artifact": "raw/oesc_fy2025_202513109349302911.xml",
    },
]

# Normalized matches copied exactly from official annual index rows.  The table is
# an audit excerpt, not a byte-for-byte archive of the very large annual indexes.
INDEX_MATCHES = [
    ("AWWA", "980227149", "202105", 2021, "990EZ", "AMERICAN WELFARE AND WORKS ASSOCIATION", "202122889349200212", ""),
    ("AWWA", "980227149", "202205", 2022, "990EZ", "AMERICAN WELFARE AND WORKS ASSOCIATION", "202202899349200300", "2022_TEOS_XML_01A"),
    ("AWWA", "980227149", "202305", 2024, "990EZ", "AMERICAN WELFARE AND WORKS ASSOCIATION", "202410619349200461", "2024_TEOS_XML_03A"),
    ("AWWA", "980227149", "202405", 2024, "990EZ", "AMERICAN WELFARE AND WORKS ASSOCIATION", "202443189349200514", "2024_TEOS_XML_11A"),
    ("KOSC", "980214323", "202005", 2021, "990", "KADENA OFFICERS SPOUSES CLUB", "202111469349300626", ""),
    ("KOSC", "980214323", "202105", 2022, "990", "Kadena Officers' Spouses' Club", "202202769349300500", ""),
    ("KOSC", "980214323", "202305", 2024, "990", "Kadena Officers' Spouses' Club", "202430969349301028", "2024_TEOS_XML_04A"),
    ("KOSC", "980214323", "202405", 2025, "990", "Kadena Officers' Spouses' Club", "202500669349300300", "2025_TEOS_XML_03A"),
    ("KOSC", "980214323", "202505", 2026, "990", "Kadena Officers Spouses Club", "202630129349300153", "2026_TEOS_XML_01A"),
    ("MOSCO", "460598583", "202105", 2021, "990EZ", "MARINE OFFICERS SPOUSES CLUB OKINAWA", "202132639349200408", ""),
    ("MOSCO", "460598583", "202205", 2023, "990EZ", "MARINE OFFICERS SPOUSES CLUB OKINAWA", "202300259349200905", "2023_TEOS_XML_01A"),
    ("MOSCO", "460598583", "202305", 2024, "990EZ", "MARINE OFFICERS SPOUSES CLUB OKINAWA", "202410719349201281", "2024_TEOS_XML_03A"),
    ("MOSCO", "460598583", "202405", 2025, "990EZ", "MARINE OFFICERS SPOUSES CLUB OKINAWA", "202501019349201215", "2025_TEOS_XML_04A"),
    ("MOSCO", "460598583", "202505", 2026, "990EZ", "MARINE OFFICERS SPOUSES CLUB OKINAWA", "202621539349200807", "2026_TEOS_XML_06A"),
    ("NOSCO", "980210979", "202106", 2022, "990", "Naval Officers' Spouses' Club of Okinawa", "202223199349301707", ""),
    ("NOSCO", "980210979", "202206", 2022, "990", "Naval Officers' Spouses' Club of Okinawa", "202243219349300204", ""),
    ("NOSCO", "980210979", "202306", 2024, "990", "Naval Officers' Spouses' Club of Okinawa", "202411349349304281", "2024_TEOS_XML_05A"),
    ("NOSCO", "980210979", "202406", 2025, "990", "Naval Officers' Spouses' Club of Okinawa", "202530159349302288", "2025_TEOS_XML_01A"),
    ("NOSCO", "980210979", "202506", 2025, "990", "Naval Officers' Spouses' Club of Okinawa", "202533199349301708", "2025_TEOS_XML_11B"),
    ("OESC", "980346507", "202006", 2022, "990", "OKINAWA ENLISTED SPOUSES CLUB", "202200619349300520", ""),
    ("OESC", "980346507", "202106", 2022, "990", "OKINAWA ENLISTED SPOUSES CLUB", "202221109349300107", ""),
    ("OESC", "980346507", "202206", 2024, "990", "OKINAWA ENLISTED SPOUSES CLUB", "202400179349301205", "2024_TEOS_XML_01A"),
    ("OESC", "980346507", "202306", 2024, "990", "OKINAWA ENLISTED SPOUSES CLUB", "202411309349303066", "2024_TEOS_XML_05A"),
    ("OESC", "980346507", "202406", 2024, "990", "OKINAWA ENLISTED SPOUSES CLUB", "202403029349300610", "2024_TEOS_XML_11A"),
    ("OESC", "980346507", "202506", 2025, "990", "OKINAWA ENLISTED SPOUSES CLUB", "202513109349302911", "2025_TEOS_XML_11D"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def local_name(element: ET.Element) -> str:
    return element.tag.split("}")[-1]


def first_text(root: ET.Element, tag: str) -> str:
    for element in root.iter():
        if local_name(element) == tag:
            return (element.text or "").strip()
    return ""


def body_node(root: ET.Element, form: str) -> ET.Element:
    target = "IRS990EZ" if form == "990EZ" else "IRS990"
    for element in root.iter():
        if local_name(element) == target:
            return element
    raise AssertionError(f"missing {target}")


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def build_index_excerpt() -> tuple[list[dict[str, object]], Path]:
    extracted = {filing["object_id"]: filing["artifact"] for filing in FILINGS}
    rows = []
    for case_id, ein, tax_period, year, form, name, object_id, archive_key in INDEX_MATCHES:
        index_url = f"https://apps.irs.gov/pub/epostcard/990/xml/{year}/index_{year}.csv"
        if object_id in extracted:
            status = "official_bulk_xml_member_frozen"
            artifact = extracted[object_id]
        elif object_id == "202202899349200300":
            status = "index_match_bulk_member_not_present_on_2026-08-22"
            artifact = ""
        else:
            status = "index_match_adjacent_period_not_extracted_this_round"
            artifact = ""
        rows.append(
            {
                "case_id": case_id,
                "ein": ein,
                "tax_period_yyyymm": tax_period,
                "index_year": year,
                "return_type": form,
                "organization_name_as_indexed": name,
                "object_id": object_id,
                "official_index_url": index_url,
                "bulk_archive_key": archive_key,
                "xml_receipt_status": status,
                "local_artifact_path": artifact,
            }
        )
    path = OUT / "official_index_matches_v1.csv"
    write_csv(path, list(rows[0]), rows)
    return rows, path


def new_anchor(anchors: list[dict[str, object]], **values: object) -> str:
    anchor_id = f"W2A-A{len(anchors) + 1:03d}"
    row = {field: "" for field in ANCHOR_FIELDS}
    row.update(values)
    row["anchor_id"] = anchor_id
    anchors.append(row)
    return anchor_id


def direct_metric_anchor(
    anchors: list[dict[str, object]],
    filing: dict[str, str],
    metric: str,
    tag: str,
    value: str,
    definition: str,
) -> str:
    form_node = "IRS990EZ" if filing["form"] == "990EZ" else "IRS990"
    if value:
        value_text = f"USD {int(value):,}"
        status = "official_irs_bulk_xml_verified"
        gap = ""
        allowed = f"The {filing['case_id']} filing reports {definition.lower()} of USD {int(value):,} for this tax period."
        review = "ai_seeded"
    else:
        value_text = "XML element absent; no positive amount encoded on this line"
        status = "official_irs_bulk_xml_field_absent"
        gap = "xml_zero_or_blank_semantics"
        allowed = "The official XML does not encode a positive amount for this filing line."
        review = "ai_seeded"
    return new_anchor(
        anchors,
        case_id=filing["case_id"],
        metric=metric,
        level="organization_filing",
        period_start=filing["period_start"],
        period_end=filing["period_end"],
        period_semantics="organization tax period; one filing snapshot",
        value=value,
        value_text=value_text,
        unit="USD",
        currency="USD",
        definition=f"{definition}; EIN {filing['ein']}; Form {filing['form']}; IRS object {filing['object_id']}",
        denominator_id="",
        source_receipt_ids=filing["receipt_id"],
        exact_locator=f"XML local-name XPath /Return/ReturnData/{form_node}/{tag}",
        anchor_status=status,
        observed_local=f"official filing for {filing['case_id']}",
        gap_type=gap,
        null_model="",
        allowed_claim=allowed,
        prohibited_inference=(
            "Do not extrapolate one filing into a trend, an annual five-organization ecology total, "
            "Okinawa-wide welfare spending, political alignment, or recipient-level flow."
            if value
            else "Do not force the missing XML element to numeric zero without a documented filing-semantics decision."
        ),
        review_status=review,
    )


def build_anchors(index_receipt_id: str) -> list[dict[str, object]]:
    anchors: list[dict[str, object]] = []
    parsed: dict[str, dict[str, str]] = {}

    for filing in FILINGS:
        path = OUT / filing["artifact"]
        root = ET.parse(path).getroot()
        assert first_text(root, "EIN") == filing["ein"]
        assert first_text(root, "TaxPeriodBeginDt") == filing["period_start"]
        assert first_text(root, "TaxPeriodEndDt") == filing["period_end"]
        body = body_node(root, filing["form"])
        metric_tags = (
            {
                "total_revenue_usd": ("TotalRevenueAmt", "Total revenue"),
                "total_expenses_usd": ("TotalExpensesAmt", "Total expenses"),
                "grants_and_similar_paid_usd": ("GrantsAndSimilarAmountsPaidAmt", "Grants and similar amounts paid"),
                "net_assets_or_fund_balances_eoy_usd": ("NetAssetsOrFundBalancesEOYAmt", "End-of-period net assets or fund balances"),
            }
            if filing["form"] == "990EZ"
            else {
                "total_revenue_usd": ("CYTotalRevenueAmt", "Current-year total revenue"),
                "total_expenses_usd": ("CYTotalExpensesAmt", "Current-year total expenses"),
                "grants_and_similar_paid_usd": ("CYGrantsAndSimilarPaidAmt", "Current-year grants and similar amounts paid"),
                "net_assets_or_fund_balances_eoy_usd": ("NetAssetsOrFundBalancesEOYAmt", "End-of-period net assets or fund balances"),
                "total_assets_eoy_usd": ("TotalAssetsEOYAmt", "End-of-period total assets"),
            }
        )
        values = {local_name(e): (e.text or "").strip() for e in body.iter()}
        parsed[filing["receipt_id"]] = values
        for metric, (tag, definition) in metric_tags.items():
            direct_metric_anchor(anchors, filing, metric, tag, values.get(tag, ""), definition)

    # AWWA's two official 990-EZ filings explicitly partition Part I line 10.
    awwa_buckets = [
        ("AWWA", "2022-06-01", "2023-05-31", "W2A-SR001", "japanese_organizations", 91838),
        ("AWWA", "2022-06-01", "2023-05-31", "W2A-SR001", "us_military_base_affiliated_organizations", 33320),
        ("AWWA", "2023-06-01", "2024-05-31", "W2A-SR002", "japanese_organizations", 64077),
        ("AWWA", "2023-06-01", "2024-05-31", "W2A-SR002", "us_military_base_affiliated_organizations", 30812),
    ]
    for case_id, start, end, receipt_id, bucket, amount in awwa_buckets:
        new_anchor(
            anchors,
            case_id=case_id,
            metric=f"reported_grant_bucket_{bucket}_usd",
            level="organization_filing_allocation_bucket",
            period_start=start,
            period_end=end,
            period_semantics="Form 990-EZ tax period; Schedule O Part I line 10 bucket",
            value=amount,
            value_text=f"USD {amount:,}",
            unit="USD",
            currency="USD",
            definition="AWWA filing-reported allocation bucket; not a recipient-complete Schedule I table",
            denominator_id="",
            source_receipt_ids=receipt_id,
            exact_locator="XML local-name XPath /Return/ReturnData/IRS990ScheduleO/SupplementalInformationDetail[FormAndLineReferenceDesc='Part I, line 10']/ExplanationTxt",
            anchor_status="official_irs_bulk_xml_verified_bucket",
            observed_local=bucket,
            gap_type="recipient_endpoints_incomplete" if bucket == "japanese_organizations" else "recipient_endpoints_aggregate_only",
            null_model="",
            allowed_claim=f"AWWA reports USD {amount:,} in this named allocation bucket for this tax period.",
            prohibited_inference="Do not treat the bucket as a complete recipient list, a five-club total, or evidence of recipient political alignment.",
            review_status="ai_seeded",
        )

    # Named AWWA program-service rows are official observations but remain
    # research-only until recipient identity and relation semantics are reviewed.
    awwa_named_rows = [
        ("2022-06-01", "2023-05-31", "W2A-SR001", "Children Kana-san Okinawa", 15287, 1),
        ("2022-06-01", "2023-05-31", "W2A-SR001", "Okinawa Nanbu Rehabilitation and Medical Center", 14870, 2),
        ("2022-06-01", "2023-05-31", "W2A-SR001", "NPO ARU", 13986, 3),
        ("2023-06-01", "2024-05-31", "W2A-SR002", "Ambitious", 13423, 1),
        ("2023-06-01", "2024-05-31", "W2A-SR002", "Himawari Day Care on Ishigaki Island", 13378, 2),
        ("2023-06-01", "2024-05-31", "W2A-SR002", "Okinawa Southern Medical Center", 13072, 3),
    ]
    for start, end, receipt_id, recipient_label, amount, ordinal in awwa_named_rows:
        new_anchor(
            anchors,
            case_id="AWWA",
            metric="filing_reported_named_program_service_grant_usd",
            level="organization_to_named_recipient_descriptor",
            period_start=start,
            period_end=end,
            period_semantics="Form 990-EZ tax period; program-service accomplishment row",
            value=amount,
            value_text=f"USD {amount:,}",
            unit="USD",
            currency="USD",
            definition="Filing-reported grants/allocation amount paired with the recipient descriptor in the program-service text",
            denominator_id="",
            source_receipt_ids=receipt_id,
            exact_locator=f"XML local-name XPath /Return/ReturnData/IRS990EZ/ProgramSrvcAccomplishmentGrp[{ordinal}]/DescriptionProgramSrvcAccomTxt + GrantsAndAllocationsAmt",
            anchor_status="official_irs_bulk_xml_verified_research_only_recipient_candidate",
            observed_local=recipient_label,
            gap_type="recipient_identity_crosswalk_pending",
            null_model="",
            allowed_claim=f"The filing pairs the descriptor '{recipient_label}' with USD {amount:,} for this tax period.",
            prohibited_inference="Do not create a central recipient actor or stable funding edge until identity and payment semantics receive human review.",
            review_status="ai_seeded",
        )

    # OESC Schedule I provides a clean three-period series to AWWA.  Only the
    # latest row has already received the principal's earlier fact decision.
    oesc_awwa = [
        ("2022-07-01", "2023-06-30", "W2A-SR012", 16308, "ai_seeded"),
        ("2023-07-01", "2024-06-30", "W2A-SR013", 14371, "ai_seeded"),
        ("2024-07-01", "2025-06-30", "W2A-SR014", 8479, "human_checked"),
    ]
    for start, end, receipt_id, amount, review in oesc_awwa:
        new_anchor(
            anchors,
            case_id="OESC_to_AWWA",
            metric="cash_grant_usd",
            level="organization_to_organization",
            period_start=start,
            period_end=end,
            period_semantics="OESC Form 990 tax period; Schedule I recipient row",
            value=amount,
            value_text=f"USD {amount:,}",
            unit="USD",
            currency="USD",
            definition="OESC Schedule I cash grant to AMERICAN WELFARE AND WORKS ASSOCIATION, recipient EIN 980227149",
            denominator_id="",
            source_receipt_ids=receipt_id,
            exact_locator="XML local-name XPath /Return/ReturnData/IRS990ScheduleI/RecipientTable[RecipientEIN='980227149']/CashGrantAmt",
            anchor_status="official_irs_bulk_xml_verified_research_only_flow",
            observed_local="OESC (EIN 980346507) -> AWWA (EIN 980227149)",
            gap_type="" if review == "human_checked" else "principal_flow_review_pending",
            null_model="",
            allowed_claim=f"OESC reports a USD {amount:,} Schedule I cash grant to AWWA for this tax period.",
            prohibited_inference="Do not infer downstream recipients, donor sources, political alignment, or automatic recurrence beyond the observed periods.",
            review_status=review,
        )

    # A third adjacent AWWA filing exists in the IRS index, but its XML member is
    # not present in the current official 2022 bulk archive.  Preserve the gap.
    new_anchor(
        anchors,
        case_id="AWWA",
        metric="official_irs_index_filing_presence",
        level="organization_filing_index",
        period_start="",
        period_end="2022-05-31",
        period_semantics="tax-period end derived from IRS index YYYYMM; period begin not frozen",
        value=1,
        value_text="IRS annual index match",
        unit="filing_record",
        currency="",
        definition="IRS 2022 annual index lists AWWA EIN 980227149, tax period 202205, object 202202899349200300",
        denominator_id="",
        source_receipt_ids=index_receipt_id,
        exact_locator="official_index_matches_v1.csv row case_id=AWWA, tax_period_yyyymm=202205",
        anchor_status="official_irs_index_only_xml_member_unavailable",
        observed_local="adjacent filing located; monetary fields not frozen",
        gap_type="official_bulk_member_not_present",
        null_model="",
        allowed_claim="The IRS annual index contains an AWWA filing record ending May 2022.",
        prohibited_inference="Do not carry monetary values from the third-party render cache into the authoritative anchor layer.",
        review_status="ai_seeded",
    )

    # Mixed-period diagnostics are explicit calculations, not one-year totals.
    latest_receipts = ["W2A-SR002", "W2A-SR005", "W2A-SR008", "W2A-SR011", "W2A-SR014"]
    latest_values = {receipt: parsed[receipt] for receipt in latest_receipts}
    mixed = [
        ("five_filing_mixed_period_gross_revenue_usd", sum(int(v.get("TotalRevenueAmt") or v.get("CYTotalRevenueAmt")) for v in latest_values.values()), "sum of the five latest filing revenue lines"),
        ("five_filing_mixed_period_gross_expenses_usd", sum(int(v.get("TotalExpensesAmt") or v.get("CYTotalExpensesAmt")) for v in latest_values.values()), "sum of the five latest filing expense lines"),
        (
            "five_filing_mixed_period_reported_grants_lower_bound_usd",
            sum(int(v.get("GrantsAndSimilarAmountsPaidAmt") or v.get("CYGrantsAndSimilarPaidAmt") or 0) for v in latest_values.values()),
            "sum of positive grants-and-similar-paid XML fields; MOSCO's current field is absent",
        ),
        ("five_filing_mixed_period_net_assets_or_fund_balances_eoy_usd", sum(int(v["NetAssetsOrFundBalancesEOYAmt"]) for v in latest_values.values()), "sum of the comparable net-assets/fund-balances EOY field"),
    ]
    for metric, amount, definition in mixed:
        new_anchor(
            anchors,
            case_id="AWWA_five_selected_organizations",
            metric=metric,
            level="selected_filing_set_diagnostic",
            period_start="2023-06-01",
            period_end="2025-06-30",
            period_semantics="five latest available filings with different tax periods; diagnostic snapshot only",
            value=amount,
            value_text=f"USD {amount:,}",
            unit="USD",
            currency="USD",
            definition=definition,
            denominator_id="",
            source_receipt_ids=";".join(latest_receipts),
            exact_locator="mechanical sum of filing-level anchors listed in source_receipt_ids",
            anchor_status="derived_mixed_period_diagnostic",
            observed_local="AWWA, KOSC, MOSCO, NOSCO and OESC latest available filing snapshots",
            gap_type="mixed_tax_periods;internal_transfers_not_netted" + (";one_grants_field_absent" if "grants" in metric else ""),
            null_model="descriptive scale check only; no population denominator",
            allowed_claim=f"Across the five selected latest filing snapshots, {definition} equals USD {amount:,}.",
            prohibited_inference="Do not call this an annual ecosystem total, per-capita measure, consolidated budget, or Okinawa-wide service spending.",
            review_status="ai_seeded",
        )

    return anchors


def build_receipts(anchors: list[dict[str, object]], index_path: Path) -> list[dict[str, object]]:
    supported: dict[str, list[str]] = defaultdict(list)
    for anchor in anchors:
        for receipt_id in str(anchor["source_receipt_ids"]).split(";"):
            if receipt_id:
                supported[receipt_id].append(str(anchor["anchor_id"]))
    rows = []
    for filing in FILINGS:
        artifact = OUT / filing["artifact"]
        rows.append(
            {
                "receipt_id": filing["receipt_id"],
                "publisher": "Internal Revenue Service (IRS)",
                "title": f"{filing['case_id']} Form {filing['form']} XML, tax period {filing['period_start']} to {filing['period_end']}",
                "source_family": "official_irs_bulk_xml",
                "url": filing["zip_url"],
                "retrieved_at": RETRIEVED_AT,
                "artifact_path": artifact.relative_to(ROOT).as_posix(),
                "sha256": sha256(artifact),
                "mime_type": "application/xml",
                "exact_locator": f"bulk ZIP member {filing['object_id']}_public.xml; EIN {filing['ein']}; IRS object {filing['object_id']}",
                "supports_anchor_ids": ";".join(supported[filing["receipt_id"]]),
                "archive_status": "archived_official_member_sha256_and_zip_crc_verified",
                "notes": "Extracted from the official IRS bulk ZIP by HTTP byte ranges; the member size and ZIP CRC-32 were verified before SHA-256 freezing.",
            }
        )
    rows.append(
        {
            "receipt_id": "W2A-SR015",
            "publisher": "Internal Revenue Service (IRS)",
            "title": "Filtered official annual index matches for five spouse-club/AWWA EINs, 2021-2026",
            "source_family": "official_irs_annual_index_derived_excerpt",
            "url": "https://www.irs.gov/charities-non-profits/form-990-series-downloads",
            "retrieved_at": RETRIEVED_AT,
            "artifact_path": index_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(index_path),
            "mime_type": "text/csv",
            "exact_locator": "official annual index URLs are recorded row by row in official_index_matches_v1.csv",
            "supports_anchor_ids": ";".join(supported["W2A-SR015"]),
            "archive_status": "derived_filtered_excerpt_sha256_frozen",
            "notes": "This is a normalized filtered excerpt, not a byte-for-byte copy of the very large annual index files. It supports filing discovery only; monetary anchors require the official XML receipts above.",
        }
    )
    return rows


def build_cache_inventory() -> list[dict[str, object]]:
    rows = []
    for path in sorted(CACHE.glob("*")):
        if not path.is_file():
            continue
        is_text_extract = path.suffix.lower() == ".txt"
        rows.append(
            {
                "filename": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "cache_role": "derived_text_extract" if is_text_extract else "third_party_visual_render",
                "admission_status": "lead_cache_not_authoritative_receipt",
                "notes": (
                    "Derived text extraction from a third-party visual render."
                    if is_text_extract
                    else "ProPublica-hosted IRS e-file visual render cached during reconnaissance; useful for locating fields, but not admitted as the official W2-00 receipt."
                ),
            }
        )
    return rows


def build_change_notes() -> list[dict[str, object]]:
    return [
        {
            "change_note_id": "W2A-CN001",
            "case_id": "AWWA_five_selected_organizations",
            "change_type": "source_admission",
            "trigger": "tmp/service_recon_990 contains ProPublica-hosted visual renders rather than official IRS artifacts",
            "previous_assumption": "Cached renders could provisionally stand in for filing receipts.",
            "revised_treatment": "Cache remains a lead/indexing aid; 14 official IRS bulk XML members now provide monetary anchors.",
            "impact_on_numbers": "No value is promoted solely from the cache.",
            "impact_on_claims": "Authoritative filing claims cite official bulk XML; cache cannot support a central relation or funding fact.",
            "evidence_receipt_ids": "W2A-SR001;W2A-SR002;W2A-SR003;W2A-SR004;W2A-SR005;W2A-SR006;W2A-SR007;W2A-SR008;W2A-SR009;W2A-SR010;W2A-SR011;W2A-SR012;W2A-SR013;W2A-SR014",
            "requires_principal_decision": "no",
            "status": "applied_research_only",
        },
        {
            "change_note_id": "W2A-CN002",
            "case_id": "AWWA",
            "change_type": "adjacent_period_gap",
            "trigger": "IRS 2022 index lists object 202202899349200300, but that member is absent from the current official 2022 bulk ZIP central directory",
            "previous_assumption": "Three consecutive official XML periods would be immediately available for all five organizations.",
            "revised_treatment": "Freeze two AWWA XML periods and one index-only adjacent filing; do not import its monetary values from the third-party cache.",
            "impact_on_numbers": "AWWA trend metrics have two XML-observed periods, not three.",
            "impact_on_claims": "AWWA continuity beyond two filing periods remains bounded; the missing XML is an explicit archive-layer gap.",
            "evidence_receipt_ids": "W2A-SR001;W2A-SR002;W2A-SR015",
            "requires_principal_decision": "no",
            "status": "gap_logged_and_scoped",
        },
        {
            "change_note_id": "W2A-CN003",
            "case_id": "KOSC;NOSCO;OESC",
            "change_type": "official_archive_transport",
            "trigger": "Some IRS index archive keys use lowercase 'a' while live URLs are case-sensitive; NOSCO 2025 XML uses ZIP method 9 (Deflate64)",
            "previous_assumption": "All official members could be extracted with archive-key casing and Python standard-library Deflate.",
            "revised_treatment": "Use the canonical uppercase URLs shown on the IRS download page; use optional inflate64 only for the one Deflate64 member, then verify CRC-32 and SHA-256.",
            "impact_on_numbers": "No numerical change.",
            "impact_on_claims": "Transport quirks no longer block official receipt freezing and are not treated as evidence gaps.",
            "evidence_receipt_ids": "W2A-SR003;W2A-SR009;W2A-SR011;W2A-SR012",
            "requires_principal_decision": "no",
            "status": "applied_research_only",
        },
        {
            "change_note_id": "W2A-CN004",
            "case_id": "AWWA_five_selected_organizations",
            "change_type": "mixed_period_scale",
            "trigger": "The five latest filings span 2023-06-01 through 2025-06-30 and include possible internal transfers.",
            "previous_assumption": "The rough sums might be described as a single-year ecology scale.",
            "revised_treatment": "Retain only explicitly labeled mixed-period gross diagnostics; no population denominator and no consolidated budget.",
            "impact_on_numbers": "Revenue USD 1,010,655; expenses USD 1,145,622; visible grants-line lower bound USD 239,424; comparable net assets/fund balances USD 625,527.",
            "impact_on_claims": "These values describe five selected filing snapshots, not annual ecosystem totals or per-capita service intensity.",
            "evidence_receipt_ids": "W2A-SR002;W2A-SR005;W2A-SR008;W2A-SR011;W2A-SR014",
            "requires_principal_decision": "yes_if_used_in_report",
            "status": "derived_diagnostic_pending_principal_use_decision",
        },
        {
            "change_note_id": "W2A-CN005",
            "case_id": "AWWA_five_selected_organizations",
            "change_type": "asset_metric_correction",
            "trigger": "The earlier approximately USD 668k figure combines TotalAssetsEOYAmt for Form 990 filers with NetAssetsOrFundBalancesEOYAmt for Form 990-EZ filers.",
            "previous_assumption": "A single 'ending assets' sum was comparable across forms.",
            "revised_treatment": "Keep total assets and net assets as separate filing metrics; use only the common net-assets/fund-balances field for the five-filing diagnostic.",
            "impact_on_numbers": "Comparable mixed-period net assets/fund balances are USD 625,527; the mixed-definition USD 668,387 total is retired.",
            "impact_on_claims": "No report may call the retired USD 668,387 figure five-organization assets.",
            "evidence_receipt_ids": "W2A-SR002;W2A-SR005;W2A-SR008;W2A-SR011;W2A-SR014",
            "requires_principal_decision": "no",
            "status": "correction_applied_research_only",
        },
        {
            "change_note_id": "W2A-CN006",
            "case_id": "MOSCO",
            "change_type": "xml_blank_semantics",
            "trigger": "MOSCO FY2025 official 990-EZ XML omits GrantsAndSimilarAmountsPaidAmt although the reconnaissance summary treated the line as zero.",
            "previous_assumption": "The FY2025 grants line was confirmed at USD 0.",
            "revised_treatment": "Record an absent XML element and do not force numeric zero without a filing-semantics decision.",
            "impact_on_numbers": "The mixed-period grants diagnostic is labeled a lower bound, not a complete sum.",
            "impact_on_claims": "MOSCO FY2025 may be described as having no positive amount encoded on that XML line, not conclusively as paying zero grants.",
            "evidence_receipt_ids": "W2A-SR008",
            "requires_principal_decision": "yes_if_zero_is_needed",
            "status": "gap_logged",
        },
        {
            "change_note_id": "W2A-CN007",
            "case_id": "KOSC_to_AWWA",
            "change_type": "relation_gate_preserved",
            "trigger": "KOSC FY2025 Schedule I contains 'American Womens Welfare Association' USD 2,580 inside an individual-assistance group rather than a clean organization RecipientTable.",
            "previous_assumption": "Name and amount might be promoted to a KOSC-to-AWWA funding flow.",
            "revised_treatment": "Do not create an anchor-level flow or central relation; preserve the prior defer pending filing/crosswalk semantics.",
            "impact_on_numbers": "USD 2,580 is excluded from relation counts and internal-transfer calculations.",
            "impact_on_claims": "No KOSC-to-AWWA grant claim is authorized by this package.",
            "evidence_receipt_ids": "W2A-SR005",
            "requires_principal_decision": "yes",
            "status": "defer_preserved",
        },
        {
            "change_note_id": "W2A-CN008",
            "case_id": "OESC_to_AWWA",
            "change_type": "adjacent_period_extension",
            "trigger": "Official OESC Schedule I rows report AWWA cash grants in three consecutive periods: USD 16,308; USD 14,371; USD 8,479.",
            "previous_assumption": "Only the latest USD 8,479 period had a frozen, clean candidate flow.",
            "revised_treatment": "Keep all three as research-only anchors; the latest retains human_checked, while the two earlier rows remain ai_seeded pending principal relation review.",
            "impact_on_numbers": "Three period-specific amounts are available; no cross-period total is created.",
            "impact_on_claims": "The filings support repeated OESC-to-AWWA reporting across three observed periods, but not recurrence outside them or downstream allocation.",
            "evidence_receipt_ids": "W2A-SR012;W2A-SR013;W2A-SR014",
            "requires_principal_decision": "yes_for_two_earlier_flow_rows",
            "status": "research_only_candidates_added",
        },
    ]


def validate(
    anchors: list[dict[str, object]],
    receipts: list[dict[str, object]],
    changes: list[dict[str, object]],
    cache_rows: list[dict[str, object]],
) -> dict[str, object]:
    anchor_ids = [str(row["anchor_id"]) for row in anchors]
    receipt_ids = [str(row["receipt_id"]) for row in receipts]
    assert len(anchor_ids) == len(set(anchor_ids))
    assert len(receipt_ids) == len(set(receipt_ids))
    assert all(anchor.startswith("W2A-A") for anchor in anchor_ids)
    assert all(receipt.startswith("W2A-SR") for receipt in receipt_ids)
    assert all(str(row["change_note_id"]).startswith("W2A-CN") for row in changes)
    receipt_set = set(receipt_ids)
    for anchor in anchors:
        assert set(str(anchor["source_receipt_ids"]).split(";")) <= receipt_set
    for receipt in receipts:
        artifact = ROOT / str(receipt["artifact_path"])
        assert artifact.is_file()
        assert sha256(artifact) == receipt["sha256"]
    assert not any(
        row["case_id"] == "KOSC_to_AWWA" and str(row["value"]) == "2580"
        for row in anchors
    )
    assert not any("annual ecosystem total" in str(row["allowed_claim"]).lower() for row in anchors)
    return {
        "status": "PASS_RESEARCH_ONLY_W2_00_SPOUSE_990",
        "anchor_count": len(anchors),
        "source_receipt_count": len(receipts),
        "official_bulk_xml_receipt_count": sum(row["source_family"] == "official_irs_bulk_xml" for row in receipts),
        "change_note_count": len(changes),
        "cache_inventory_count": len(cache_rows),
        "organization_xml_periods": {
            case_id: sum(filing["case_id"] == case_id for filing in FILINGS)
            for case_id in ["AWWA", "KOSC", "MOSCO", "NOSCO", "OESC"]
        },
        "oesc_awwa_flow_anchor_count": sum(row["case_id"] == "OESC_to_AWWA" for row in anchors),
        "kosc_2580_flow_anchor_count": 0,
        "central_writeback": False,
        "frontend_or_publication_adapter": False,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _, index_path = build_index_excerpt()
    anchors = build_anchors("W2A-SR015")
    receipts = build_receipts(anchors, index_path)
    changes = build_change_notes()
    cache_rows = build_cache_inventory()

    write_csv(OUT / "anchor_candidates_v1.csv", ANCHOR_FIELDS, anchors)
    write_csv(OUT / "source_receipts_v1.csv", RECEIPT_FIELDS, receipts)
    write_csv(OUT / "change_notes_v1.csv", CHANGE_FIELDS, changes)
    write_csv(
        OUT / "cache_inventory_v1.csv",
        ["filename", "bytes", "sha256", "cache_role", "admission_status", "notes"],
        cache_rows,
    )

    report = validate(anchors, receipts, changes, cache_rows)
    validation_path = OUT / "validation_report_v1.json"
    validation_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest_rows = []
    for path in sorted(OUT.rglob("*")):
        if not path.is_file() or path.name == "package_manifest_v1.csv":
            continue
        manifest_rows.append(
            {
                "artifact_path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    write_csv(
        OUT / "package_manifest_v1.csv",
        ["artifact_path", "bytes", "sha256"],
        manifest_rows,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
