#!/usr/bin/env python3
"""Build the research-only W2-E historical/literature package.

The builder deliberately reads reviewed central facts and prior research packages
without writing any central table, publication adapter, or frontend payload.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "outputs" / "us_presence_network_wave2_w2_e_v1"
SOURCE_RAW = DEFAULT_OUTPUT / "raw"
BUILD_DATE = "2026-08-22"
UNEXPECTED_FINDINGS_TEMPLATE = (
    ROOT / "data" / "metadata" / "unexpected_findings_register_template_v1.csv"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def unexpected_findings_fieldnames() -> list[str]:
    """Read the package-local lead contract from its single authoritative template."""
    with UNEXPECTED_FINDINGS_TEMPLATE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        fieldnames = next(csv.reader(handle), [])
    if len(fieldnames) != 19:
        raise ValueError(
            f"Unexpected-findings template must contain 19 columns, got {len(fieldnames)}"
        )
    return fieldnames


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def copy_raw_inputs(output_dir: Path) -> None:
    target = output_dir / "raw"
    target.mkdir(parents=True, exist_ok=True)
    expected = [
        "diet_justice_committee_1984_04_20.html",
        "international_welfare_consultation_archive_guide.html",
        "okinawa_archives_journal_23_2021.pdf",
        "okinawa_womens_history_reference_2026.pdf",
        "ryukyuan_american_welfare_council_1971_photo_record.html",
    ]
    for name in expected:
        source = SOURCE_RAW / name
        if not source.exists():
            raise FileNotFoundError(f"Missing frozen W2-E source: {source}")
        destination = target / name
        if source.resolve() != destination.resolve():
            shutil.copy2(source, destination)


def central_receipt(
    receipt_id: str,
    source_id: str,
    source_log: dict[str, dict[str, str]],
    archive: dict[str, dict[str, str]],
    supports: str,
    locator: str,
) -> dict[str, str]:
    source = source_log[source_id]
    archived = archive.get(source_id, {})
    return {
        "receipt_id": receipt_id,
        "upstream_source_ref": source_id,
        "title": source["title"],
        "publisher": "",
        "source_type": source["source_type"],
        "url": source["url"],
        "publication_date": source["year"],
        "document_coverage_period": source["year"],
        "exact_locator": locator or source.get("locator", ""),
        "supports": supports,
        "source_relationship": "central_source_reuse",
        "evidence_level": source["evidence_level"],
        "source_review_status": source["review_status"],
        "archive_status": archived.get("archive_status", "not_in_archive_manifest"),
        "local_path": archived.get("local_path", ""),
        "sha256": archived.get("sha256", ""),
        "retrieval_date": archived.get("archived_at_utc", "")[:10],
        "source_limit": "Source admission/review does not by itself approve the historical interpretation in this package.",
        "package_scope": "research_only",
        "frontend_eligibility": "not_frontend_ready",
        "central_writeback": "no",
    }


def local_receipt(
    output_dir: Path,
    receipt_id: str,
    filename: str,
    title: str,
    publisher: str,
    source_type: str,
    url: str,
    publication_date: str,
    coverage: str,
    locator: str,
    supports: str,
    limit: str,
) -> dict[str, str]:
    path = output_dir / "raw" / filename
    return {
        "receipt_id": receipt_id,
        "upstream_source_ref": "new_W2E_frozen_source",
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "url": url,
        "publication_date": publication_date,
        "document_coverage_period": coverage,
        "exact_locator": locator,
        "supports": supports,
        "source_relationship": "official_primary_or_official_retrospective",
        "evidence_level": "E4",
        "source_review_status": "ai_seeded",
        "archive_status": "local_frozen",
        "local_path": str(path.relative_to(ROOT)).replace("\\", "/") if path.is_relative_to(ROOT) else str(path),
        "sha256": sha256(path),
        "retrieval_date": BUILD_DATE,
        "source_limit": limit,
        "package_scope": "research_only",
        "frontend_eligibility": "not_frontend_ready",
        "central_writeback": "no",
    }


def build_source_receipts(output_dir: Path) -> list[dict[str, str]]:
    source_log_rows = read_csv(ROOT / "data" / "interim" / "05_source_log_initial_v0.csv")
    source_log = {row["source_id"]: row for row in source_log_rows}
    archive_rows = read_csv(ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv")
    archive = {row["source_id"]: row for row in archive_rows}

    rows = [
        local_receipt(
            output_dir,
            "W2E-S001",
            "okinawa_archives_journal_23_2021.pdf",
            "資料群紹介：国際福祉相談所文書について",
            "沖縄県公文書館",
            "official_archive_journal",
            "https://www.archives.pref.okinawa.jp/wp-content/uploads/744195554fd8a10a10b02ddfe5d4575d.pdf",
            "2021-03",
            "1955-1998 institutional history; 1972-1985 policy sequence",
            "PDF pp. 8, 10-12 (printed pp. 24, 26-28): 1972 governance shift; 1979 proposal; 1981 petition; 1983 hearing; 1984 Diet testimony; 1985 reform",
            "International Welfare Consultation Office history, care-to-rights sequence, governance shift and closure context",
            "An official archive-journal reconstruction using the deposited collection; it supports sequence and holdings, not sole causality for the 1985 law reform.",
        ),
        local_receipt(
            output_dir,
            "W2E-S002",
            "okinawa_womens_history_reference_2026.pdf",
            "沖縄の女性史 資料編（年表・人名資料）",
            "沖縄県／おきなわ女性財団",
            "official_prefectural_reference",
            "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/039/818/17_shiryouhen_t.pdf",
            "2026",
            "postwar-2024 chronology",
            "PDF p. 63 (printed p. 271) and p. 86 (printed p. 294): 1980 rename and 1998 closure/consultation-program handoff",
            "Corroborates the 1980 legal rename and records the 1998 closure plus a functional consultation-program handoff",
            "A retrospective chronology; the handoff of a consultation function is not automatic organizational succession.",
        ),
        local_receipt(
            output_dir,
            "W2E-S003",
            "international_welfare_consultation_archive_guide.html",
            "国際福祉相談所文書",
            "沖縄県公文書館",
            "official_archive_collection_guide",
            "https://www.archives.pref.okinawa.jp/okinawa_related/10752",
            "2019-05-21; current page observed 2026-08-22",
            "1958-1998",
            "Document overview; lines/HTML paragraphs describing 1972/1980 renames, 1979 proposal, holdings and closure",
            "Collection scope, organization names, 1979 proposal and surviving primary-record families",
            "The guide's wording that the proposal led to the 1985 reform is retrospective institutional attribution, not causal identification.",
        ),
        local_receipt(
            output_dir,
            "W2E-S004",
            "diet_justice_committee_1984_04_20.html",
            "第101回国会 衆議院法務委員会 第12号",
            "国立国会図書館 国会会議録検索システム",
            "official_legislative_record",
            "https://kokkai.ndl.go.jp/simple/detail?minId=110105206X01219840420",
            "1984-04-20",
            "1984 nationality-law deliberation",
            "Statements 54-57 and nearby lines: prior testimony, the 1979 Okinawa proposal and the role of Okinawa stateless-child cases in deliberation",
            "Confirms that legislators explicitly referred to the 1979 proposal and consultation-office witnesses during nationality-law deliberation",
            "The record establishes entry and acknowledged relevance; it does not show that one office alone caused the final statute.",
        ),
        local_receipt(
            output_dir,
            "W2E-S005",
            "ryukyuan_american_welfare_council_1971_photo_record.html",
            "USCAR写真資料：琉米福祉協議会／婦人クラブ活動（1971）",
            "沖縄県公文書館",
            "official_archive_photo_catalog",
            "https://www2.archives.pref.okinawa.jp/opa/SearchPics.aspx?cont_cd=A000022653",
            "1971",
            "1971 event captions",
            "Dated catalog captions for the Ryukyuan-American Welfare Council, affiliated clubs and welfare gifts",
            "Pre-reversion umbrella/event structure used only to test AWWA genealogy claims",
            "A dated affiliation snapshot is not proof of predecessor/successor identity or uninterrupted club composition.",
        ),
        {
            "receipt_id": "W2E-S006",
            "upstream_source_ref": "H2P-S16",
            "title": "Clinton Presidential Records: USMC Good Neighbor Efforts on Okinawa",
            "publisher": "U.S. National Archives / Clinton Presidential Library",
            "source_type": "official_archival_government_compilation",
            "url": "https://s3.amazonaws.com/NARAprodstorage/lz/presidential-libraries/clinton/foia/2008/2008-0703-F/42-t-7585792-20080703f-003-007-2014.pdf",
            "publication_date": "compiled 2000-07",
            "document_coverage_period": "1972 retrospective; 1992-2000 observations",
            "exact_locator": "Prior H2 transcription; current W2-E retrieval returned HTTP 403",
            "supports": "AWWA 1972 six-group retrospective, 1992-1999 aggregate giving and late-1999 Amer-Asian School material-contact lead",
            "source_relationship": "official_public_affairs_retrospective",
            "evidence_level": "E3",
            "source_review_status": "ai_seeded",
            "archive_status": "remote_403_url_only",
            "local_path": "",
            "sha256": "",
            "retrieval_date": BUILD_DATE,
            "source_limit": "Public-affairs compilation selected to display good-neighbor activity; the six-group retrospective conflicts with other five/seven-group descriptions.",
            "package_scope": "research_only",
            "frontend_eligibility": "not_frontend_ready",
            "central_writeback": "no",
        },
        {
            "receipt_id": "W2E-S007",
            "upstream_source_ref": "H2P-S11",
            "title": "平田正代と戦後沖縄の国際福祉（IMADR public-history essay）",
            "publisher": "反差別国際運動（IMADR）",
            "source_type": "scholarly_public_history_essay",
            "url": "https://imadr.net/newsletter/no-217/p2/",
            "publication_date": "2024",
            "document_coverage_period": "1958-1998",
            "exact_locator": "Passages on the 1979 proposal and the reported 1997 base-responsibility statement",
            "supports": "Biographical reconstruction of care-to-rights translation and a late-stage explicit base-responsibility claim",
            "source_relationship": "secondary_reconstruction",
            "evidence_level": "E3",
            "source_review_status": "ai_seeded",
            "archive_status": "url_only_prior_package",
            "local_path": "",
            "sha256": "",
            "retrieval_date": "2026-07-20",
            "source_limit": "Underlying speech/proposal should be located before quotation or report-level generalization.",
            "package_scope": "research_only",
            "frontend_eligibility": "not_frontend_ready",
            "central_writeback": "no",
        },
    ]

    rows.extend(
        [
            central_receipt("W2E-S008", "S072", source_log, archive, "AWWA 40-year/1972 retrospective and five-club description", "Full article"),
            central_receipt("W2E-S009", "S039", source_log, archive, "A049 post-1995 formation and activity", "Article discussion of group formation"),
            central_receipt("W2E-S010", "S155", source_log, archive, "A052 plaintiff-group history from first 1982 suit onward", "Official history page; archive attempt is 403"),
            central_receipt("W2E-S011", "S201", source_log, archive, "A111 organizational history and dated base-related women's mobilization", "Article history section"),
            central_receipt("W2E-S012", "S042", source_log, archive, "1997 Nago referendum chronology and post-result executive action", "1997 entries"),
            central_receipt("W2E-S013", "S172", source_log, archive, "1997 Nago official vote date and totals", "市民投票 sheet C1:O15"),
            central_receipt("W2E-S014", "S192", source_log, archive, "1997 Nago direct request, signatures, ordinance and vote chronology", "PDF pp. 44-47 / printed pp. 671-674"),
        ]
    )

    nr05_rows = read_csv(ROOT / "outputs" / "history_1998_2012_online_v1" / "source_candidates.csv")
    for source in nr05_rows:
        source_id = source["source_candidate_id"]
        if source_id not in {f"NR05S{i:03}" for i in range(1, 33)}:
            continue
        upstream_ids = split_refs(source.get("existing_source_id", ""))
        archived = archive.get(upstream_ids[0], {}) if len(upstream_ids) == 1 else {}
        rows.append(
            {
                "receipt_id": f"W2E-{source_id}",
                "upstream_source_ref": source_id + (";" + ";".join(upstream_ids) if upstream_ids else ""),
                "title": source["title"],
                "publisher": source["publisher"],
                "source_type": source["source_type"],
                "url": source["url"],
                "publication_date": source["source_publication_date"],
                "document_coverage_period": source["document_coverage_period"],
                "exact_locator": source["exact_locator"],
                "supports": source["support_scope"],
                "source_relationship": source["source_relationship"],
                "evidence_level": source["evidence_level_proposed"],
                "source_review_status": source["review_status"],
                "archive_status": archived.get("archive_status", source["archive_or_access_status"]),
                "local_path": archived.get("local_path", ""),
                "sha256": archived.get("sha256", ""),
                "retrieval_date": source["retrieval_date"],
                "source_limit": source["interpretation_limit"],
                "package_scope": "research_only",
                "frontend_eligibility": "not_frontend_ready",
                "central_writeback": "no",
            }
        )
    return rows


def historical_row(
    spine_id: str,
    lane: str,
    date_start: str,
    date_end: str,
    precision: str,
    actor_ids: str,
    actor_or_interface: str,
    event_type: str,
    summary: str,
    output: str,
    venue: str,
    source_receipt_ids: str,
    relationship: str,
    evidence: str,
    review_status: str,
    claim_status: str,
    interpretation: str,
    competing: str,
    limit: str,
    identity_status: str,
    figure_priority: int,
) -> dict[str, object]:
    year = int(date_start[:4])
    return {
        "spine_id": spine_id,
        "lane": lane,
        "date_start": date_start,
        "date_end": date_end,
        "date_precision": precision,
        "period_band": "1972_1997" if year <= 1997 else "1998_2012",
        "actor_ids": actor_ids,
        "actor_or_interface": actor_or_interface,
        "event_type": event_type,
        "event_summary": summary,
        "observed_output": output,
        "interface_or_venue": venue,
        "source_receipt_ids": source_receipt_ids,
        "source_relationship": relationship,
        "evidence_level": evidence,
        "review_status": review_status,
        "claim_status": claim_status,
        "interpretation_role": interpretation,
        "competing_explanation": competing,
        "claim_limit": limit,
        "historical_identity_status": identity_status,
        "figure_priority": figure_priority,
        "package_scope": "research_only",
        "frontend_eligibility": "not_frontend_ready",
        "central_writeback": "no",
    }


def build_historical_spine() -> list[dict[str, object]]:
    r = historical_row
    return [
        r("W2E-H001", "accountability", "1982", "1982", "year", "A052", "嘉手納基地爆音差止訴訟原告団", "litigation_entry", "The first Kadena noise-litigation round was filed in 1982.", "A durable plaintiff-group/case record begins.", "Japanese court/litigation system", "W2E-S010", "official_organization_retrospective_human_reviewed", "E4", "human_checked", "supported_bounded", "Long-running litigation creates a stable documentary backbone.", "Later organizational continuity is reconstructed retrospectively.", "Do not assume identical plaintiffs across rounds.", "central_actor_round_bounded", 1),
        r("W2E-H002", "accountability", "1995", "1995", "year", "A049", "基地・軍隊を許さない行動する女たちの会", "organization_formation", "The group formed after the 1995 U.S.-military sexual-violence incident.", "A women/human-rights carrier became publicly identifiable.", "movement organization", "W2E-S009", "academic_secondary_human_reviewed", "E3", "human_revised", "supported_bounded", "Women/human-rights framing becomes an organizational carrier.", "A secondary study may compress the formation process.", "No legal-form or full-period continuity claim.", "central_actor_identity_reviewed", 1),
        r("W2E-H003", "accountability", "1995", "1995", "year", "A111", "沖縄県女性団体連絡協議会", "base_related_womens_mobilization", "A long-standing women's network is retrospectively documented in 1995 base-removal mobilization.", "Women-network mobilization entered the base-accountability repertoire.", "street mobilization/public claim", "W2E-S011", "local_news_retrospective_human_reviewed", "E4", "human_checked", "supported_bounded", "Older civic infrastructure could be reactivated around base violence.", "The retrospective source may select emblematic episodes.", "Event participation is not a permanent alliance with A049.", "central_actor_historical_event_bounded", 0),
        r("W2E-H004", "accountability", "1997-06-27", "1997-10-06", "day_range", "A068", "ヘリポート基地建設の是非を問う名護市民投票推進協議会", "referendum_direct_request", "The council initiated a Local Autonomy Act direct request, submitted signatures and obtained an ordinance after council redesign.", "17,539 valid signatures and an enacted four-choice ordinance.", "municipal direct-request and council procedure", "W2E-S014", "official_primary_human_reviewed", "E4", "human_revised", "supported_bounded", "Local autonomy translated opposition into a formal vote procedure.", "Institutional actors changed the question design.", "Signature participation is not organization membership.", "central_actor_time_bounded", 1),
        r("W2E-H005", "accountability", "1997-12-21", "1997-12-24", "day_range", "A068", "1997名護市民投票", "referendum_result_and_executive_response", "The referendum produced an opposition majority; three days later the mayor accepted the project and resigned.", "A vote record and a divergent executive decision.", "municipal referendum and mayoral decision", "W2E-S012;W2E-S013", "official_primary_human_reviewed", "E4", "human_checked", "supported_bounded", "Formal participation and executive authority remained distinct.", "The vote may still have political effects not captured by legal binding force.", "Do not describe the vote as a legal veto or as meaningless.", "case_event_not_new_actor", 1),
        r("W2E-H006", "accountability", "1998", "1998", "year", "A019", "ヘリ基地反対協議会", "organization_reorganization", "The 1997 referendum carrier was reorganized into a distinct successor organization around 1998.", "A successor carrier preserved issue continuity without identity merger.", "movement organization", "W2E-S012;W2E-S014", "official_chronology_plus_human_lifecycle_review", "E4", "human_revised", "supported_bounded", "Movement functions can persist through organizational reorganization.", "Exact dissolution and formation decisions remain incompletely documented.", "A068 and A019 remain separate actors; no simple rename.", "central_successor_relation_bounded", 1),
        r("W2E-H007", "accountability", "2002", "2003", "year_range", "A053", "普天間基地爆音訴訟団", "litigation_round", "Residents filed the first Futenma noise-litigation cases across 2002 and 2003.", "Court filings produced a durable case chronology.", "Japanese court", "W2E-NR05S008;W2E-NR05S009", "official_case_record_plus_retrospective", "E4", "ai_seeded", "candidate", "Court records preserve rounds more precisely than current organization summaries.", "Organization pages may use launch year while judgments distinguish filings.", "A round is not a new actor and does not imply identical plaintiffs.", "central_actor_round_candidate", 0),
        r("W2E-H008", "accountability", "2003-09-25", "2003-09-25", "day", "A009;A020;A045;A076;A086", "Okinawa Dugong v. Rumsfeld parties/counsel", "transnational_litigation_entry", "Named organizations and counsel entered a U.S. federal NHPA venue.", "A U.S. complaint and case record.", "U.S. federal court", "W2E-NR05S010;W2E-NR05S011", "contemporaneous_primary", "E4", "ai_seeded", "candidate", "English-language legal procedure creates an unusually durable transnational trace.", "Visibility may reflect legal hosting and publication capacity.", "Case co-presence is not a stable alliance; A002/A019 remain non-parties.", "case_specific_roles", 1),
        r("W2E-H009", "accountability", "2004-02-03", "2004-03-30", "day_range", "", "913名申請人（個人集合）", "administrative_nonentry", "A pollution-mediation application was accepted, heard three times and dismissed for lack of statutory jurisdiction.", "An official nonentry/dismissal record.", "Okinawa Prefecture Pollution Review Board", "W2E-NR05S012", "official_retrospective", "E4", "ai_seeded", "candidate", "Institutional design can make exclusion itself visible.", "Jurisdictional exclusion is not evidence of weak claims or weak mobilization.", "Do not actorize the 913 applicants or attach a named organization without the file.", "anonymous_collective_not_actorized", 1),
        r("W2E-H010", "accountability", "2004-04-19", "2004-04-19", "day", "A019", "ヘリ基地反対協議会", "onsite_action", "A documented Henoko sit-in/maritime-obstruction episode began.", "A dated on-site action anchor.", "Henoko fishing port", "W2E-NR05S013;W2E-NR05S014", "retrospective_plus_secondary", "E3", "ai_seeded", "candidate", "On-site repertoires leave weaker organization records than courts and formal procedures.", "Several carriers may have shared the site.", "Do not backfill the entire later sit-in history into one unchanged actor.", "central_actor_event_candidate", 0),
        r("W2E-H011", "accountability", "2004-06-10", "2004-06-10", "day", "A004", "日本自然保護協会", "eia_formal_comment", "NACS-J submitted a dated opinion on the EIA method statement.", "A formal environmental-procedure record.", "Japanese environmental-impact assessment", "W2E-NR05S015", "contemporaneous_primary", "E4", "ai_seeded", "candidate", "Scientific/environmental claims gain durable dates through procedural submission.", "The hosted archive favors organizations with publication capacity.", "A formal comment is not project suspension or acceptance.", "central_actor_procedural_role_candidate", 1),
        r("W2E-H012", "accountability", "2005-05-20", "2005-05-20", "day", "", "泡瀬第一波公金訴訟（个人原告）", "public_funds_litigation", "Individual residents filed the first Awase public-funds lawsuit.", "A court case; A055 appears only as movement/support actor.", "Naha District Court", "W2E-NR05S016;W2E-NR05S017", "court_record_plus_near_period_report", "E4", "ai_seeded", "candidate", "Legal procedure separates plaintiff identity from movement support.", "Public spokespeople can be mistaken for organizational plaintiffs.", "Do not encode A055 as organizational plaintiff.", "individual_plaintiffs_not_actorized", 0),
        r("W2E-H013", "accountability", "2008-02-14", "2008-02-14", "day", "A115", "新日本婦人の会沖縄県本部", "administrative_request", "The prefectural branch made a request concerning a U.S.-Marine sexual-assault case.", "A dated prefectural administrative-diary entry.", "Okinawa Prefectural Government", "W2E-NR05S018", "contemporaneous_primary", "E4", "ai_seeded", "candidate", "Administrative diaries preserve occurrence while often omitting claim text and outcome.", "The branch may have a longer offline history.", "Do not transfer the action to the national parent or infer outcome.", "branch_event_candidate", 0),
        r("W2E-H014", "accountability", "2010-05-14", "2010-05-14", "day", "A005", "WWF Japan and 67 listed domestic organizations", "joint_statement_event", "A 67-organization Henoko statement was issued/submitted.", "A complete dated participant list.", "organization-hosted statement/national ministries", "W2E-NR05S019", "contemporaneous_primary", "E4", "ai_seeded", "candidate", "Hosted lists expand visible participation while overstating durable network density if read as alliances.", "Organizer hosting creates a source-cluster effect.", "Co-signing is event participation, not stable alliance.", "event_hyperedge_not_dyadic_alliance", 1),
        r("W2E-H015", "accountability", "2011-04-28", "2011-04-28", "day", "A052", "嘉手納基地爆音差止訴訟原告団", "litigation_round", "The third Kadena noise-litigation round was filed.", "A new round in a continuing plaintiff-group history.", "Japanese court", "W2E-NR05S020", "official_organization_retrospective", "E4", "ai_seeded", "candidate", "Case rounds preserve continuity and participant turnover as separate questions.", "Current official histories may simplify internal changes.", "No new actor and no identical-plaintiff inference.", "central_actor_round_candidate", 0),
        r("W2E-H016", "accountability", "2011-06-23", "2011-06-23", "day", "A096", "下地島空港の軍事利用に反対する会", "public_meeting", "A096 hosted a meeting opposing a proposed SDF use of Shimojishima Airport.", "A dated event but weak continuity evidence.", "Miyako/Shimojishima public meeting", "W2E-NR05S021", "secondary_local", "E3", "ai_seeded", "candidate", "Sakishima action is event-visible before its organizations become historically traceable.", "The carrier may predate the meeting or be temporary.", "Use only as minimum activity date.", "central_actor_event_candidate", 1),
        r("W2E-H017", "accountability", "2012", "2012", "year", "A053", "普天間基地爆音訴訟団", "litigation_round", "The second Futenma noise-litigation round began, with related filings extending into 2013.", "A second-round case chronology.", "Japanese court", "W2E-NR05S008;W2E-NR05S009", "official_case_record_plus_retrospective", "E4", "ai_seeded", "candidate", "A 2012 boundary anchor connects the historical spine to current case infrastructure.", "Website and judgment use different compression.", "Keep 2013 carryover visible; no new actor.", "central_actor_round_candidate", 0),
        r("W2E-H018", "accountability", "2012-08-25", "2012-08-25", "day", "A015", "与那国島への自衛隊配備に反対する意見広告実行委員会", "temporary_committee_formation", "A party newspaper reported a founding press conference for an anti-deployment opinion-ad committee.", "A single event/identity lead.", "Yonaguni opinion-ad campaign", "W2E-NR05S022", "lead", "E2", "needs_local_retrieval", "candidate", "Eventized Sakishima carriers are where online continuity breaks most sharply.", "The committee may be temporary and the source is not independent.", "No registry/genealogy change without the original ad and local press.", "central_actor_identity_deferred", 1),
        r("W2E-H019", "service_care", "1972", "1972", "year", "X004", "American Women's Welfare Association / AWWA", "umbrella_formation_retrospective", "Two later public histories place the AWWA umbrella in 1972 but disagree over five versus six coordinating clubs and do not resolve the 1971 council lineage.", "A dated umbrella-function hypothesis and an explicit genealogy conflict.", "military-spouse charity coordination", "W2E-S006;W2E-S008;W2E-S005", "official_public_affairs_retrospectives_plus_pre_reversion_archive", "E3", "ai_seeded", "needs_local_retrieval", "Service-side coordination is historically deep but its organization identity is not closed.", "The 1972 event may be a rename, reorganization or new umbrella after reversion.", "Do not create predecessor/successor edges or freeze member counts.", "central_actor_current_identity_historical_genealogy_open", 1),
        r("W2E-H020", "service_care", "1972-04-13", "1972-05", "bounded_range", "", "国際社会事業団沖縄代表部→国際福祉沖縄事務所", "governance_and_legal_transition", "The legal/name conversion is dated to 13 April 1972; the subsequent board initiative shifted toward Okinawan leadership in May.", "A bounded legal/name transition followed by a documented governance change.", "international welfare institution", "W2E-S001;W2E-S003", "official_archive_reconstruction", "E4", "ai_seeded", "candidate", "Reversion reorganized a base-linked welfare interface rather than simply ending it.", "This may combine localization, funding substitution and institutional rupture.", "No central actor ID or automatic continuity edge.", "research_interface_no_actorization", 1),
        r("W2E-H021", "service_care", "1979", "1979", "year", "", "国際福祉沖縄事務所", "care_to_rights_proposal", "The office issued an Okinawa proposal that converted accumulated stateless-child cases into nationality-law and reciprocal-support demands.", "A formal policy/rights claim distributed beyond Okinawa.", "proposal/public-policy arena", "W2E-S001;W2E-S003;W2E-S004", "official_archive_plus_legislative_primary", "E4", "ai_seeded", "candidate", "Care cases were aggregated and translated into rights claims.", "The proposal was one input among national and international legal changes.", "Do not claim sole causality for the 1985 reform.", "research_interface_no_actorization", 1),
        r("W2E-H022", "service_care", "1980-05", "1980-08", "bounded_range", "", "国際福祉相談所", "scope_expansion_and_organizational_rename", "The service scope broadened in May 1980; the legal/name conversion followed in August.", "A bounded scope change followed by a legal/name transition.", "social-welfare corporation", "W2E-S001;W2E-S002;W2E-S003", "official_retrospective", "E4", "ai_seeded", "candidate", "Service organizations can change scope and identity while preserving functions.", "A rename may hide changes in staff, finance and governance.", "Time-bound aliases only; no registry mutation.", "research_interface_no_actorization", 0),
        r("W2E-H023", "service_care", "1981-03", "1981-03", "month", "", "国際福祉相談所", "administrative_petition", "The office petitioned municipalities that had not applied national health insurance to stateless/foreign-national children.", "A care-derived administrative request.", "municipal administrations", "W2E-S001", "official_archive_reconstruction", "E4", "ai_seeded", "candidate", "Translation from individual welfare cases to administrative rights did not require an anti-base label.", "Municipal responses varied and are not fully reconstructed.", "Do not infer universal compliance or political alignment.", "research_interface_no_actorization", 0),
        r("W2E-H024", "service_care", "1983-03-15", "1983-03-15", "day", "", "国際福祉相談所", "national_ministry_hearing", "Two representatives presented views at a Justice Ministry hearing on an interim nationality-law proposal.", "Entry into a national legislative-policy process.", "Ministry of Justice hearing", "W2E-S001", "official_archive_reconstruction", "E4", "ai_seeded", "candidate", "The care-to-rights pathway reached a national institutional venue.", "The record does not isolate which argument changed the draft.", "Entry and testimony are not a causal effect estimate.", "research_interface_no_actorization", 1),
        r("W2E-H025", "service_care", "1984-04-06", "1984-04-20", "day_range", "", "国際福祉相談所／瀧岡直美", "diet_testimony_and_deliberation", "A consultation-office caseworker testified to the Diet; in later committee debate, one legislator explicitly called the 1979 Okinawa proposal one origin of the reform work.", "A named witness and an explicitly acknowledged agenda input in the legislative record.", "House of Representatives Justice Committee", "W2E-S001;W2E-S004", "official_legislative_primary_plus_archive", "E4", "ai_seeded", "candidate", "A welfare institution entered and informed a formal national rights-accountability agenda.", "Multiple national actors and treaty/equality pressures also shaped reform.", "Do not attribute the statute or an independent causal share to a single witness or organization.", "person_role_not_actor_registry", 1),
        r("W2E-H026", "service_care", "1985-01-01", "1985-01-01", "day", "", "日本国籍法改正", "policy_change_context", "The nationality-law reform took effect after the documented proposal, hearings and Diet testimony.", "A substantive policy change temporally connected to, but not uniquely attributable to, the office's work.", "national legislation", "W2E-S001;W2E-S004", "official_primary_plus_retrospective", "E4", "ai_seeded", "candidate", "This is a rare historical candidate for service/care work reaching beyond record creation.", "CEDAW preparation, broader equality politics and other actors were major causes.", "ATTRIBUTION remains bounded; no sole-causality claim.", "policy_context_not_actor_edge", 1),
        r("W2E-H027", "service_care", "1992", "1999", "year_range", "X004", "AWWA", "aggregate_local_giving", "A 2000 USMC compilation reports annual aggregate contributions to Japanese recipients for most years 1992-1999.", "A multi-year service/resource trace without ultimate-recipient rows.", "military public-affairs record", "W2E-S006", "official_public_affairs_retrospective", "E3", "ai_seeded", "candidate", "Service-side resource channels predate current websites and Form 990 extraction.", "Definitions, member composition and publicity selection may vary by year.", "No recipient network, annual total or funding-source inference without the original ledger.", "central_actor_historical_aggregate_candidate", 0),
        r("W2E-H028", "service_care", "1997", "1997", "year", "", "国際福祉相談所／平田正代", "base_responsibility_claim", "A public-history reconstruction reports an explicit claim that base conditions generated most cases even while operational cooperation with U.S. military offices was sometimes necessary.", "A candidate care-to-base-accountability articulation.", "public speech/publication", "W2E-S007", "secondary_reconstruction", "E3", "ai_seeded", "needs_local_retrieval", "Historical welfare practice was not inherently nonpolitical.", "This may be a late leadership statement rather than a stable organizational position.", "Underlying speech/publication required before quotation.", "person_statement_no_actorization", 1),
        r("W2E-H029", "service_care", "1998-03-31", "1998-03-31", "day", "", "国際福祉相談所→てぃるる相談室（功能交接）", "closure_and_function_handoff", "The office closed; an official chronology says a consultation function continued as a program of the Okinawa Women's Foundation.", "Institutional termination with bounded functional continuation.", "welfare/counseling administration", "W2E-S001;W2E-S002;W2E-S003", "official_retrospective", "E4", "ai_seeded", "candidate", "Functions can survive organizational closure through institutional handoff.", "People, records and responsibilities may have dispersed unevenly.", "Do not encode successor identity or unchanged governance.", "research_interface_closed_function_handoff_only", 1),
        r("W2E-H030", "service_care", "1999", "1999", "year", "", "Amer-Asian School and U.S. Marine units", "direct_material_support_lead", "A 2000 public-affairs compilation reports visits and school-material support after the consultation office closed.", "A later military-side material/contact trace in a related welfare field.", "school/community support", "W2E-S006", "official_public_affairs_retrospective", "E2", "ai_seeded", "candidate", "A service interface remained, but not as proven institutional succession.", "The story was selected for good-neighbor publicity and concerns a different institution.", "No funding edge, actor ID or continuity from the consultation office.", "research_endpoint_lead", 1),
    ]


def build_record_regimes() -> list[dict[str, str]]:
    base = {"package_scope": "research_only", "frontend_eligibility": "not_frontend_ready", "central_writeback": "no"}
    rows = [
        ("RR01", "court_and_case_records", "accountability", "complaints, judgments, case rounds, named legal roles", "informal deliberation, membership change, actions that never enter court", "Creates exact dates and durable named roles; can make lawyers/plaintiff groups look structurally central.", "Compare ENTRY/RECORD/RELIEF and keep case roles separate from alliances.", "Court visibility is not movement influence or project change."),
        ("RR02", "referendum_and_municipal_records", "accountability", "direct requests, signature validation, ordinances, vote results, executive decisions", "campaign discussions, internal coalition dynamics, post-vote informal effects", "Preserves institutional gates and makes blocked/reinterpreted participation visible.", "Model the full gate chain rather than a single referendum event.", "A vote record is not a binding veto or a complete measure of public opinion effects."),
        ("RR03", "EIA_and_formal_comment_archives", "accountability", "dated opinions, submissions, agency stages", "unsubmitted local knowledge, rejected framing, internal drafting", "Favors organizations able to write, host and preserve formal scientific/legal documents.", "Study procedural translation and source-host dependence.", "Formal submission is not acceptance or project suspension."),
        ("RR04", "official_NPO_certification_and_disclosure", "cross_cutting_context", "legal identity, certification and some annual-report obligations", "informal groups, unions, case committees, U.S. entities and organizations outside NPO status", "The December 1998 NPO-law implementation added a standardized certification/disclosure channel for one legal form; later internet publication expanded unevenly.", "Use as one document-regime anchor and compare matched legal forms rather than imposing a single visibility breakpoint.", "Certified-NPO growth is not growth/professionalization of base-accountability organizations or a universal web-visibility shift."),
        ("RR05", "welfare_casework_and_deposited_archives", "service_care", "board minutes, case files, annual reports, policy proposals and staff roles", "restricted personal case files and institutions whose records were never deposited", "Makes one care institution unusually traceable across governance, practice and rights translation.", "Use as a deep historical case with explicit archive-selection boundaries.", "One preserved collection is not the complete service ecology."),
        ("RR06", "military_public_affairs_and_good_neighbor_compilations", "service_care", "selected donations, aggregate giving, visits and relationship narratives", "failed activities, recipient dissent, non-public transfers and ordinary routine", "Systematically selects positive relationship-building episodes and may compress genealogy.", "Use for LEG0/LEG1 and as a lead for recipient-side checking.", "Public-affairs visibility is not independent evidence of legitimacy or social effect."),
        ("RR07", "tax_filings_and_financial_disclosure", "service_care", "organization totals, officers, named large recipients and some purposes", "Schedule B donor names, small/unitemized endpoints and local allocation below national organizations", "Creates a modern resource/person record that is much denser than the historical web record.", "Use in W2-A as a dated money/person ledger; never merge unlike tax periods.", "A filing amount does not disclose donor identity, political intent or recipient response."),
        ("RR08", "organization_self_histories_and_local_news", "both", "formation claims, public milestones, named events and retrospective identity", "failed organizations, internal disputes, unpublicized continuity and precise legal transitions", "Current survivors narrate their own past and can crowd out short-lived carriers.", "Cross-check against official records, archives and contemporaneous materials.", "Surviving website visibility is not historical centrality or uninterrupted continuity."),
        ("RR09", "local_ephemera_and_regional_press", "both", "temporary committees, flyers, opinion ads, meeting carriers and local wording", "Mostly absent from open web; often available only in libraries or personal archives", "Its absence creates the sharpest Sakishima and event-carrier gaps.", "Dispatch exact local retrieval tasks tied to named claims.", "Online absence is not organizational absence or inactivity."),
    ]
    return [
        {
            "regime_id": a,
            "source_family": b,
            "primary_lane": c,
            "what_is_preserved": d,
            "systematic_omissions": e,
            "visibility_effect": f,
            "analytic_use": g,
            "forbidden_inference": h,
            **base,
        }
        for a, b, c, d, e, f, g, h in rows
    ]


def build_claims() -> list[dict[str, str]]:
    rows = [
        ("W2E-C01", "record_regime_differentiation", "supported_bounded", "The two historical lanes are preserved by different institutions: courts/procedures on the accountability side, and welfare archives/public-affairs/tax records on the service side.", "W2E-H001-W2E-H030; RR01-RR09", "Observed network density must be compared within source families, not across one mixed graph.", "The denser lane is more active, influential or durable.", "principal_interpretation_required"),
        ("W2E-C02", "historical_selective_permeability", "supported_bounded", "At least one historical welfare institution translated accumulated care cases into administrative petitions, a formal proposal, ministry hearing and Diet testimony.", "W2E-H021-W2E-H026", "Use the International Welfare Consultation Office as a deep case showing that service/care and accountability were not historically sealed.", "Current spouse clubs or service NGOs share this political function; the office alone caused the 1985 reform.", "principal_interpretation_required"),
        ("W2E-C03", "institutional_handoff_without_identity_merger", "supported_bounded", "The 1972 governance shift and 1998 closure/function handoff show that functions can persist while organizations, legal forms and governance change.", "W2E-H020;W2E-H022;W2E-H029", "Separate actor continuity, function continuity and program handoff in the historical chapter.", "A rename or service handoff proves unchanged organization, people or funding.", "principal_interpretation_required"),
        ("W2E-C04", "post_1998_visibility_shift", "candidate", "The December 1998 NPO-law implementation added a standardized certification and disclosure route for organizations using that legal form; other formal venues and web publication expanded on different schedules.", "RR01-RR04; W2E-H006-W2E-H018", "Treat 1998 as one institution-specific document-regime anchor and test visibility by legal/organizational form.", "NPO law created one common origin or a universal online-visibility breakpoint for Okinawa civic organizations.", "needs_comparative_test"),
        ("W2E-C05", "awwa_genealogy_conflict", "needs_local_retrieval", "An official 1971 record describes a Ryukyuan-American Welfare Council coordinating nine women's clubs, while later official/public-affairs retrospectives describe the 1972 AWWA with five or six member organizations. The records do not resolve succession, rename, reorganization or changing snapshots.", "W2E-H019;W2E-S005;W2E-S006;W2E-S008", "Keep X004's current identity while making the historical genealogy conflict visible.", "Automatic predecessor edge, fixed member count or continuous organization from 1952/1971.", "local_primary_required"),
        ("W2E-C06", "current_two_ecologies_not_timeless", "supported_bounded", "A present-day separation hypothesis cannot be projected backward unchanged because historical care-to-rights translation and mixed institutional interfaces are documented.", "W2E-C02;W2E-C03", "Treat differentiated record regimes and selective permeability as historical hypotheses, then test present-day bridge closure separately.", "The two current ecologies are already disproved, historically identical, or known to have progressively differentiated.", "principal_interpretation_required"),
        ("W2E-C07", "service_1998_2012_visibility_gap", "supported_bounded", "The current online spine contains far fewer service/care activity anchors for 1998-2012 than accountability anchors.", "source_coverage_v1.csv", "Report this as a source-coverage gap and a retrieval priority.", "Service activity declined or disappeared after 1998.", "method_boundary_confirmed"),
    ]
    return [
        {
            "claim_id": a,
            "claim_family": b,
            "claim_status": c,
            "claim_text": d,
            "evidence_refs": e,
            "allowed_use": f,
            "forbidden_extrapolation": g,
            "decision_status": h,
            "package_scope": "research_only",
            "frontend_eligibility": "not_frontend_ready",
            "central_writeback": "no",
        }
        for a, b, c, d, e, f, g, h in rows
    ]


def build_local_tasks() -> list[dict[str, str]]:
    tasks = [
        ("W2E-LR01", "P0", "AWWA genealogy and member composition", "1952-1972", "Ryukyuan-American Welfare Council/AWWA charters, board minutes, member-club lists, legal/tax identity records", "X004;W2E-H019", "Decides predecessor/rename/reorganization semantics and whether the 1971 nine-club and 1972 five/six-member accounts are time-specific."),
        ("W2E-LR02", "P0", "International Welfare Office 1972 handoff", "1971-1973", "Board minutes, budgets, funding agreements, staff roster and incorporation documents", "W2E-H020", "Separates localization, funding substitution, governance transfer and organizational rupture."),
        ("W2E-LR03", "P0", "1979 proposal and policy-entry originals", "1979-1985", "Original 沖縄からの提言, ministry-hearing submission, Diet witness materials and internal case statistics", "W2E-H021-W2E-H026", "Raises or lowers ATTRIBUTION for the care-to-rights case."),
        ("W2E-LR04", "P1", "1997 base-responsibility statement", "1997", "Underlying speech, newsletter or publication attributed to 平田正代", "W2E-H028", "Determines whether the public base-responsibility wording can be quoted and attributed to the institution."),
        ("W2E-LR05", "P1", "1998 closure and counseling handoff", "1997-1999", "Closure resolution, personnel/record transfer and てぃるる相談室 program documents", "W2E-H029", "Distinguishes function continuation from actor succession."),
        ("W2E-LR06", "P1", "AWWA annual giving and club rosters", "1992-1999", "Annual reports, recipient tables, contributing-club rosters and accounting definitions", "W2E-H027", "Converts an aggregate public-affairs series into a deduplicated historical resource-flow ledger."),
        ("W2E-LR07", "P1", "First Kadena litigation organization", "1982-1983", "Complaint, plaintiff-group charter, branch structure and roster", "W2E-H001", "Tests continuous organization versus recurring case label and membership turnover."),
        ("W2E-LR08", "P1", "1995 women's organization formation", "1995-1997", "Founding statement, minutes, newsletters and 1995 mobilization materials for A049/A111", "W2E-H002;W2E-H003", "Separates two women-network carriers, their roles and any actual coordination."),
        ("W2E-LR09", "P1", "Nago referendum-carrier reorganization", "1997-1998", "A068 minutes, dissolution/reorganization decision and A019 founding records", "W2E-H004-W2E-H006", "Closes the predecessor/successor boundary without merging actors."),
        ("W2E-LR10", "P2", "Local/event carriers after 1998", "2004-2012", "Henoko tent logs, local flyers, Miyako meeting materials, Yonaguni opinion ad and Yaeyama/Miyako press", "W2E-H010;W2E-H016;W2E-H018", "Tests whether the observed court/procedure bias hides short-lived local carriers."),
    ]
    return [
        {
            "task_id": a,
            "priority": b,
            "target": c,
            "period": d,
            "requested_material": e,
            "affected_evidence_refs": f,
            "decision_changed_if_found": g,
            "online_status": "online_anchor_present_primary_gap_remains",
            "assignment_type": "local_archive_or_new_primary",
            "package_scope": "research_only",
            "central_writeback": "no",
        }
        for a, b, c, d, e, f, g in tasks
    ]


def build_literature_comparison() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    nr05 = {row["position_id"]: row for row in read_csv(ROOT / "outputs" / "nr05_literature_positioning_v1" / "source_crosswalk.csv")}
    for key in ["LP001", "LP003", "LP005", "LP006", "LP013"]:
        row = nr05[key]
        rows.append(
            {
                "literature_id": f"W2E-{key}",
                "citation": row["citation"],
                "year": row["year"],
                "theme": row["source_key"],
                "prior_contribution": row["prior_claim"],
                "project_increment": row["our_possible_increment"],
                "novelty_boundary": row["forbidden_novelty_claim"],
                "source_url": row["url_or_locator"],
                "verification_status": row["verification_status"],
                "source_package": "nr05_literature_positioning_v1",
            }
        )
    us_lit = {row["lit_id"]: row for row in read_csv(ROOT / "outputs" / "us_presence_literature_positioning_v1" / "bibliography_v1.csv")}
    for key in ["L002", "L003", "L004", "L005", "L008", "L009", "L018"]:
        row = us_lit[key]
        rows.append(
            {
                "literature_id": f"W2E-{key}",
                "citation": f"{row['authors']} ({row['year']}), {row['title']}",
                "year": row["year"],
                "theme": row["theme"],
                "prior_contribution": row["main_finding"],
                "project_increment": row["project_relationship"],
                "novelty_boundary": row["verification_note"],
                "source_url": row["stable_url"],
                "verification_status": "bibliography_verified",
                "source_package": "us_presence_literature_positioning_v1",
            }
        )
    h2_pos = {row["position_id"]: row for row in read_csv(ROOT / "outputs" / "research_wave_h2_recipient_permeability_v1" / "literature_positioning_v1.csv")}
    h2_sources = {row["source_key"]: row for row in read_csv(ROOT / "outputs" / "research_wave_h2_recipient_permeability_v1" / "source_registry_v1.csv")}
    for key in ["H2LP001", "H2LP005"]:
        row = h2_pos[key]
        source = h2_sources[row["source_key"]]
        rows.append(
            {
                "literature_id": f"W2E-{key}",
                "citation": source["title"],
                "year": source["date_or_period"],
                "theme": "historical_welfare_rights_interface",
                "prior_contribution": row["prior_contribution"],
                "project_increment": row["what_this_package_adds"],
                "novelty_boundary": row["what_it_rules_out"],
                "source_url": source["url"],
                "verification_status": row["claim_strength"],
                "source_package": "research_wave_h2_recipient_permeability_v1",
            }
        )
    rows.append(
        {
            "literature_id": "W2E-HD012",
            "citation": "The Electoral Return to Anti-Base Positioning in Okinawa Gubernatorial Elections, 1990-2022",
            "year": "undated; principal supplied 2026-08-22",
            "theme": "electoral_period_and_spatial_context",
            "prior_contribution": (
                "An exploratory candidate-level study (18 top-two observations) finds that the electoral association of "
                "anti-base positioning varies across 1990-1998, 2002-2010 and 2014-2022. Its post-2014 municipal layer "
                "uses 41 municipalities across three elections (123 observations) and finds place categories more "
                "descriptively informative than raw base-area share; the 2018 gubernatorial and 2019 referendum patterns "
                "are closely aligned."
            ),
            "project_increment": (
                "W2-E supplies dated organization, action and record-regime anchors that can be placed beside those "
                "electoral phases. It can test which public carriers and institutional venues were visible in each "
                "period, but it does not identify an organization-to-vote causal effect."
            ),
            "novelty_boundary": (
                "Do not infer that NGO density, a named organization, or the two-infrastructure network caused municipal "
                "vote differences. The prior study is exploratory, its candidate sample is small and anti-base position "
                "is highly collinear with opposition-coalition identity."
            ),
            "source_url": (
                "principal_attachment:98736b57-4716-4739-b070-a348646e44b5/pasted-text.txt"
            ),
            "verification_status": "principal_supplied_full_text_read",
            "source_package": "HD-012_principal_input",
        }
    )
    for row in rows:
        row.update({"package_scope": "research_only", "frontend_eligibility": "not_frontend_ready", "central_writeback": "no"})
    return rows


def build_coverage(spine: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in spine:
        grouped[(str(row["lane"]), str(row["period_band"]))].append(row)
    gap_notes = {
        ("accountability", "1972_1997"): "Strong anchors cluster in litigation, the 1995 crisis and the 1997 referendum; routine/local organizing remains underdocumented.",
        ("accountability", "1998_2012"): "Formal cases, EIA, administrative requests and hosted lists are dense; this is a venue/document advantage, not an activity count.",
        ("service_care", "1972_1997"): "One unusually well-preserved welfare archive and later AWWA retrospectives dominate; other service organizations are not comparably covered.",
        ("service_care", "1998_2012"): "Only closure/handoff and one public-affairs material-support lead are currently visible; no decline or absence inference is allowed.",
    }
    rows = []
    for key in sorted(grouped):
        members = grouped[key]
        source_refs = sorted({ref for row in members for ref in split_refs(str(row["source_receipt_ids"]))})
        statuses = Counter(str(row["review_status"]) for row in members)
        families = Counter(str(row["source_relationship"]) for row in members)
        rows.append(
            {
                "lane": key[0],
                "period_band": key[1],
                "anchor_count": len(members),
                "human_reviewed_anchor_count": statuses["human_checked"] + statuses["human_revised"],
                "candidate_or_local_anchor_count": len(members) - statuses["human_checked"] - statuses["human_revised"],
                "unique_source_receipt_count": len(source_refs),
                "review_status_mix": ";".join(f"{name}:{count}" for name, count in sorted(statuses.items())),
                "source_relationship_mix": ";".join(f"{name}:{count}" for name, count in sorted(families.items())),
                "coverage_interpretation": gap_notes[key],
                "unit_warning": "Counts are selected documentary anchors, not organization activity or population rates.",
                "package_scope": "research_only",
                "central_writeback": "no",
            }
        )
    return rows


def render_svg(spine: list[dict[str, object]], path: Path) -> None:
    width, height = 1600, 900
    x0, x1 = 150, 1510
    y_lane = {"service_care": 320, "accountability": 610}
    colors = {"service_care": "#B7791F", "accountability": "#0F6B6D"}

    def x(year: float) -> float:
        return x0 + (year - 1972) / 40 * (x1 - x0)

    # Deliberately label only the anchors needed to read the argument. The CSV
    # preserves all 30 rows; the communication figure should not become a log.
    labels = {
        "W2E-H019": ("1972：AWWA伞状组织说法／福利机构治理转移", -88, 14, "start"),
        "W2E-H021": ("1979：照护个案→政策提言", -76, 0, "middle"),
        "W2E-H025": ("1984：国会证言", 72, 0, "middle"),
        "W2E-H029": ("1998：机构关闭／功能交接", 78, -8, "middle"),
        "W2E-H001": ("1982：嘉手纳首轮诉讼", 78, 0, "middle"),
        "W2E-H002": ("1995：女性反基地组织形成", -82, -6, "middle"),
        "W2E-H004": ("1997：直接请求与条例", 76, -12, "middle"),
        "W2E-H008": ("2003：儒艮案进入美国法院", 78, -8, "middle"),
        "W2E-H009": ("2004：调停程序门前排除", -82, 12, "middle"),
        "W2E-H014": ("2010：67团体声明", -82, -10, "end"),
        "W2E-H018": ("2012：与那国临时载体", 78, -8, "end"),
    }
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1600" height="900" fill="#F7F4EC"/>',
        '<style>text{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;fill:#16343A}.title{font-size:34px;font-weight:700}.sub{font-size:17px;fill:#536A6D}.lane{font-size:23px;font-weight:700}.tick{font-size:14px;fill:#65777A}.label{font-size:14px;font-weight:600}.note{font-size:15px;fill:#6A5A45}.legend{font-size:14px;fill:#526568}</style>',
        '<text x="70" y="65" class="title">1972-2012：同一驻军周围的两条组织基础设施历史线</text>',
        '<text x="70" y="98" class="sub">圆点是有来源的时间锚；上方为服务／照护，下方为问责。密度差异首先反映记录制度，不等于活动强弱。</text>',
        f'<rect x="{x(1998)-10:.1f}" y="140" width="20" height="570" fill="#D8E1DE" opacity="0.75"/>',
        f'<text x="{x(1998)+15:.1f}" y="160" class="note">1998：NPO法新增一种认证／公开通道；不是共同起点</text>',
    ]
    for year in [1972, 1980, 1990, 1998, 2000, 2010, 2012]:
        xpos = x(year)
        svg.append(f'<line x1="{xpos:.1f}" y1="180" x2="{xpos:.1f}" y2="700" stroke="#D9DFDC" stroke-width="1"/>')
        svg.append(f'<text x="{xpos:.1f}" y="735" text-anchor="middle" class="tick">{year}</text>')
    for lane, y in y_lane.items():
        svg.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{colors[lane]}" stroke-width="3" opacity="0.55"/>')
        title = "服务／照护基础设施" if lane == "service_care" else "问责基础设施"
        svg.append(f'<text x="135" y="{y+7}" text-anchor="end" class="lane" fill="{colors[lane]}">{title}</text>')

    same_year_offsets: dict[tuple[str, int], int] = defaultdict(int)
    for row in spine:
        lane = str(row["lane"])
        year = int(str(row["date_start"])[:4])
        key = (lane, year)
        same_year_offsets[key] += 1
        jitter = (same_year_offsets[key] - 1) * 8
        xpos = x(year) + jitter
        y = y_lane[lane]
        reviewed = str(row["review_status"]) in {"human_checked", "human_revised"}
        fill = colors[lane] if reviewed else "#F7F4EC"
        dash = "" if reviewed else ' stroke-dasharray="3 2"'
        svg.append(f'<circle cx="{xpos:.1f}" cy="{y}" r="8" fill="{fill}" stroke="{colors[lane]}" stroke-width="3"{dash}/>')
        sid = str(row["spine_id"])
        if sid not in labels:
            continue
        label, dy, dx, anchor = labels[sid]
        target_y = y + dy
        line_end = target_y - 16 if dy > 0 else target_y + 7
        svg.append(f'<line x1="{xpos:.1f}" y1="{y + (10 if dy > 0 else -10)}" x2="{xpos + dx:.1f}" y2="{line_end}" stroke="{colors[lane]}" stroke-width="1.5"/>')
        svg.append(f'<text x="{xpos + dx:.1f}" y="{target_y}" text-anchor="{anchor}" class="label">{html.escape(label)}</text>')

    # Highlight the rare care-to-rights passage without presenting a deterministic causal arrow.
    svg.append(f'<path d="M {x(1979):.1f} 245 Q {x(1982):.1f} 185 {x(1985):.1f} 245" fill="none" stroke="#B7791F" stroke-width="3" stroke-dasharray="7 5"/>')
    svg.append(f'<text x="{x(1982):.1f}" y="182" text-anchor="middle" class="note">照护个案→提言→听证／国会（政策归因仍有界）</text>')
    svg.extend(
        [
            '<circle cx="1020" cy="800" r="7" fill="#0F6B6D"/><text x="1035" y="805" class="legend">既有人审锚点</text>',
            '<circle cx="1180" cy="800" r="7" fill="#F7F4EC" stroke="#0F6B6D" stroke-width="3" stroke-dasharray="3 2"/><text x="1195" y="805" class="legend">研究候选／待原件</text>',
            '<text x="70" y="845" class="sub">关键修正：功能边界并非天然封闭。至少一条福利机构路径把照护案件转成权利与政策主张；当代是否仍有桥接，需另做同口径审计。</text>',
            '</svg>',
        ]
    )
    path.write_text("\n".join(svg), encoding="utf-8")


def write_readme(output_dir: Path, counts: dict[str, int]) -> None:
    text = f"""# 对美主线第二轮 W2-E：1972-2012 历史双线 v1

日期：{BUILD_DATE}

状态：`research_only / principal_checkpoint_pending / not_frontend_ready / central_writeback=no`

## 这包做了什么

- {counts['spine']} 条历史锚点：问责侧 {counts['accountability']} 条，服务／照护侧 {counts['service']} 条；
- {counts['sources']} 条来源收据，其中本轮新增冻结 5 件官方原件；
- 9 类记录制度、{counts['literature']} 条文献定位、7 条候选判断和 10 项精确当地／新一手任务；
- 一张两条泳道的历史图，不把来源密度当作活动强度。

## 当前最重要的研究修正

历史材料不支持把两套生态写成 1972 年以来始终封闭。国際福祉相談所至少留下了一条可追踪链：
照护与无国籍儿童个案被汇总为 1979 年提言，随后进入地方行政请求、法务省听证和国会证言。
1984 年国会记录还明确回指该提言和沖縄个案。这个案例支持“历史上的选择性通透”，但不能外推给
今天的 AWWA、军属俱乐部或 USO，也不能把 1985 年国籍法修改归因于单一组织。

第二个修正是：两条历史线首先由不同记录制度保存。法院、EIA、公投、福利档案、军方公共关系材料
和后来的税务申报留下的痕迹不同。1998 年 12 月施行的 NPO 法，只为采用该法人形态的组织新增了一种
标准化认证／公开通道；它不是整个冲绳 NGO 网络或互联网可见性的统一断点。历史网络密度必须按来源族比较。

## 主文件

- `historical_spine_v1.csv`：两条历史线的 30 个锚点；
- `record_regime_comparison_v1.csv`：9 类记录制度及其系统性遗漏；
- `source_receipts_v1.csv`：来源、locator、本地路径与 SHA-256；
- `source_coverage_v1.csv`：按泳道／时期显示覆盖，不作为活动计数；
- `literature_comparison_v1.csv`：先行研究、项目增量与不可声称的新颖性；
- `claim_table_v1.csv`：候选结论、允许表述与禁止外推；
- `local_retrieval_candidates_v1.csv`：取到后会改变哪条判断；
- `fig_w2e_two_spines_v1.svg`：历史双线图；
- `principal_checkpoint_v1.md`：负责人只需处理四项解释性判断；
- `validation_report_v1.json` 与 `manifest.json`：结构、引用与哈希验证。

## 边界

本包没有给国際福祉相談所、琉米福祉協議会、Amer-Asian School 等历史接口分配 actor ID，
没有建立 AWWA 前身关系，也没有改中央表、publication adapter 或前端。`ai_seeded` 锚点仍需负责人
判断；来源是官方原件，也不自动把解释升级成人审结论。

## 意外发现登记

- `unexpected_findings_register_v1.csv`：本轮 {counts['unexpected_findings']} 条；本次构建没有登记新的偶发线索。
- 登记项全部使用 `lead_only`，不进入本包结论、中央事实层或前端，也不触发人工复核。
- 每条根线索最多向外追查 3 步，每包最多 10 条新观察；空表不表示现实中不存在其他关系或材料。

## 复现

```powershell
python scripts/build_us_presence_network_wave2_w2_e_v1.py
python -m unittest tests.test_build_us_presence_network_wave2_w2_e_v1
python scripts/validate_research_work_package_v1.py outputs/us_presence_network_wave2_w2_e_v1
```
"""
    (output_dir / "README.md").write_text(text, encoding="utf-8")


def write_checkpoint(output_dir: Path) -> None:
    text = f"""# W2-E 负责人解释检查点 v1

日期：{BUILD_DATE}

状态：`principal_review_pending`。这里只需要判断历史章怎么解释；逐行事实、中央落库和前端发布均不在本检查点。

## 先读什么

1. `fig_w2e_two_spines_v1.svg`；
2. `claim_table_v1.csv` 的 W2E-C01、C02、C05、C06；
3. `raw/okinawa_archives_journal_23_2021.pdf` 的 PDF 8、10-12 页；
4. `raw/diet_justice_committee_1984_04_20.html` 中关于 1979 提言、瀧岡参考人和沖縄无国籍儿童的段落。

## 四项判断

### E-PR01：历史主句

建议采用：**现有历史锚点首先显示两种记录制度：问责行动多由法院、行政和公投保存，服务／照护活动多由福利档案和军方公共关系材料保存。至少一个福利机构同时开展照护与权利倡议，说明功能边界并非天然封闭；是否逐步分化为两套组织网络，仍待更多历史关系材料检验。**

不要采用“1972 年以来始终是两张互不相交的网”，也不要把有限锚点写成完整组织演化史。

### E-PR02：是否把国際福祉相談所作为历史深描案例

建议纳入。它能把抽象的“社会再生产／问责”落到同一机构的可观察变化：照护、调查、提言、行政请求、听证、国会证言。
1984 年审议中，一名议员把 1979 年提言称为推动改法工作的“原点之一”；这支持议程进入和影响，不能识别该机构对 1985 年改法的独立因果份额。

### E-PR03：1998 的解释

建议把 1998 写成一个**制度特定的记录锚点**：12 月施行的 NPO 法，为采用该法人形态的组织新增了标准化认证和公开通道。
它不是整个冲绳 NGO 网络或互联网可见性的统一断点；临时委员会、工会、诉讼团、美国法人、现场行动与先岛地方材料并不共同受这一制度覆盖。

### E-PR04：当地材料优先级

建议先取两组：AWWA 1952／1971／1972 谱系与成员名单（W2E-LR01）；1979 提言及 1983-84 听证／国会原件（W2E-LR03）。
前者决定服务侧谱系能不能画，后者决定历史“选择性通透”能写到多强。

## 你确认后会发生什么

四项只会固定报告历史章和 W2-E claim table。若要把任何历史组织、人物、谱系或关系写进中央表，仍需另开受控人工复核与 W2-G 授权。
"""
    (output_dir / "principal_checkpoint_v1.md").write_text(text, encoding="utf-8")


def write_search_log(output_dir: Path) -> None:
    text = f"""# W2-E search and retrieval log

Date: {BUILD_DATE}

## Completed bounded tracks

- Reused the complete NR-05 1998-2012 historical anchor/source package rather than repeating broad search.
- Reused the H2 recipient-permeability historical timeline and literature boundaries.
- Frozen the Okinawa Prefectural Archives collection guide and 2021 archive-journal article on the International Welfare Consultation Office.
- Frozen the National Diet 1984-04-20 Justice Committee record; located explicit references to the 1979 Okinawa proposal and consultation-office testimony.
- Frozen the 2026 Okinawa women's-history reference chronology; located the 1980 rename and 1998 closure/function-handoff entries.
- Frozen a 1971 USCAR photo-catalog page for the Ryukyuan-American Welfare Council/member-club genealogy conflict.

## Failed or bounded retrieval

- The NARA/Clinton USMC Good Neighbor compilation returned HTTP 403 in this pass. Its prior H2 transcription remains a research lead; no new local artifact or upgraded claim was created.
- AWWA public histories conflict on 1952/1971/1972 lineage and five/six/seven member counts. Online material is not sufficient for a genealogy edge.
- The reported 1997 base-responsibility statement remains secondary until the underlying speech/publication is retrieved.

## Negative-search meaning

Sparse service/care anchors in 1998-2012 are recorded as a source-coverage gap. They do not establish organizational decline, inactivity or absence.
"""
    (output_dir / "search_log.md").write_text(text, encoding="utf-8")


def validate(
    output_dir: Path,
    spine: list[dict[str, object]],
    receipts: list[dict[str, str]],
    claims: list[dict[str, str]],
    unexpected_findings: list[dict[str, str]],
) -> dict[str, object]:
    receipt_ids = {row["receipt_id"] for row in receipts}
    allowed_statuses = {"human_checked", "human_revised", "ai_seeded", "needs_local_retrieval"}
    register_path = output_dir / "unexpected_findings_register_v1.csv"
    with register_path.open("r", encoding="utf-8-sig", newline="") as handle:
        register_reader = csv.DictReader(handle)
        register_fieldnames = register_reader.fieldnames or []
        written_unexpected_findings = list(register_reader)
    required_lead_values = {
        "workflow_status": "lead_only",
        "claim_eligibility": "no",
        "central_writeback": "no",
        "human_review_trigger": "no",
        "publication_eligibility": "no",
    }
    checks: dict[str, bool] = {
        "unique_spine_ids": len({str(row["spine_id"]) for row in spine}) == len(spine),
        "unique_receipt_ids": len(receipt_ids) == len(receipts),
        "two_lanes_only": {str(row["lane"]) for row in spine} == {"accountability", "service_care"},
        "both_periods_each_lane": all(any(row["lane"] == lane and row["period_band"] == band for row in spine) for lane in ["accountability", "service_care"] for band in ["1972_1997", "1998_2012"]),
        "dates_within_contract": all(1972 <= int(str(row["date_start"])[:4]) <= 2012 for row in spine),
        "all_source_refs_resolve": all(ref in receipt_ids for row in spine for ref in split_refs(str(row["source_receipt_ids"]))),
        "review_status_legal": all(str(row["review_status"]) in allowed_statuses for row in spine),
        "no_central_writeback": all(str(row["central_writeback"]) == "no" for row in spine + claims) and all(row["central_writeback"] == "no" for row in receipts),
        "no_frontend_release": all(str(row["frontend_eligibility"]) == "not_frontend_ready" for row in spine + claims) and all(row["frontend_eligibility"] == "not_frontend_ready" for row in receipts),
        "no_genealogy_relation_type": all(str(row["event_type"]) not in {"predecessor_of", "successor_of", "same_actor"} for row in spine),
        "unexpected_findings_register_contract": (
            register_fieldnames == unexpected_findings_fieldnames()
            and written_unexpected_findings == unexpected_findings
            and len(unexpected_findings) <= 10
            and all(
                row.get(field, "") == expected
                for row in unexpected_findings
                for field, expected in required_lead_values.items()
            )
        ),
        "local_receipt_hashes_match": True,
        "svg_parses": True,
    }
    for row in receipts:
        if row["archive_status"] != "local_frozen":
            continue
        path = ROOT / row["local_path"] if not Path(row["local_path"]).is_absolute() else Path(row["local_path"])
        if output_dir != DEFAULT_OUTPUT:
            path = output_dir / "raw" / Path(row["local_path"]).name
        checks["local_receipt_hashes_match"] &= path.exists() and sha256(path) == row["sha256"]
    try:
        ElementTree.parse(output_dir / "fig_w2e_two_spines_v1.svg")
    except ElementTree.ParseError:
        checks["svg_parses"] = False
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "generated_date": BUILD_DATE,
        "checks": checks,
        "counts": {
            "historical_spine_rows": len(spine),
            "accountability_rows": sum(row["lane"] == "accountability" for row in spine),
            "service_care_rows": sum(row["lane"] == "service_care" for row in spine),
            "human_reviewed_rows": sum(row["review_status"] in {"human_checked", "human_revised"} for row in spine),
            "source_receipts": len(receipts),
            "locally_frozen_new_sources": sum(row["archive_status"] == "local_frozen" for row in receipts),
            "claims": len(claims),
            "unexpected_findings_rows": len(unexpected_findings),
        },
        "boundaries": {
            "package_scope": "research_only",
            "central_writeback": "no",
            "publication_adapter": "not_created",
            "frontend_release": "not_created",
            "historical_actorization": "not_created",
        },
    }


def write_manifest(output_dir: Path) -> None:
    files = []
    for path in sorted(p for p in output_dir.rglob("*") if p.is_file() and p.name != "manifest.json"):
        files.append(
            {
                "path": str(path.relative_to(output_dir)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "package": "us_presence_network_wave2_w2_e_v1",
        "generated_date": BUILD_DATE,
        "status": "research_only_principal_checkpoint_pending",
        "files": files,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    copy_raw_inputs(output_dir)
    receipts = build_source_receipts(output_dir)
    spine = build_historical_spine()
    regimes = build_record_regimes()
    claims = build_claims()
    local_tasks = build_local_tasks()
    literature = build_literature_comparison()
    coverage = build_coverage(spine)
    unexpected_findings: list[dict[str, str]] = []

    write_csv(output_dir / "historical_spine_v1.csv", spine, list(spine[0]))
    write_csv(output_dir / "record_regime_comparison_v1.csv", regimes, list(regimes[0]))
    write_csv(output_dir / "source_receipts_v1.csv", receipts, list(receipts[0]))
    write_csv(output_dir / "source_coverage_v1.csv", coverage, list(coverage[0]))
    write_csv(output_dir / "literature_comparison_v1.csv", literature, list(literature[0]))
    write_csv(output_dir / "claim_table_v1.csv", claims, list(claims[0]))
    write_csv(output_dir / "local_retrieval_candidates_v1.csv", local_tasks, list(local_tasks[0]))
    write_csv(
        output_dir / "unexpected_findings_register_v1.csv",
        unexpected_findings,
        unexpected_findings_fieldnames(),
    )
    render_svg(spine, output_dir / "fig_w2e_two_spines_v1.svg")
    counts = {
        "spine": len(spine),
        "accountability": sum(row["lane"] == "accountability" for row in spine),
        "service": sum(row["lane"] == "service_care" for row in spine),
        "sources": len(receipts),
        "literature": len(literature),
        "unexpected_findings": len(unexpected_findings),
    }
    write_readme(output_dir, counts)
    write_checkpoint(output_dir)
    write_search_log(output_dir)
    validation = validate(output_dir, spine, receipts, claims, unexpected_findings)
    (output_dir / "validation_report_v1.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if validation["status"] != "PASS":
        raise RuntimeError(json.dumps(validation, ensure_ascii=False, indent=2))
    write_manifest(output_dir)
    return validation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build(args.output_dir.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
