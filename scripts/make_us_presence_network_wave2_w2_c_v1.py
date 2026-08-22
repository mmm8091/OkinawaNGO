#!/usr/bin/env python3
"""Build the research-only W2-C accountability outcome package.

The package recodes the fixed 13 translation episodes onto parallel outcome
axes, keeps matched gate cases separate from project-change counterexamples,
and preserves attribution as an independently evidenced field.  It never
writes central facts, publication adapters, frontend assets, or control docs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_c_v1"
ARTIFACTS = OUT / "artifacts"
TE_PATH = (
    ROOT
    / "outputs"
    / "translation_episode_comparison_v1"
    / "translation_episode_candidates_v1.csv"
)
NEGATIVE_PATH = (
    ROOT
    / "outputs"
    / "translation_negative_cases_v1"
    / "negative_case_candidates_v1.csv"
)
SOURCE_LOG = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
ARCHIVE_MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
W200 = ROOT / "outputs" / "us_presence_network_wave2_w2_00_system_accountability_v1"
RUN_DATE = "2026-08-22"

SCOPE = {
    "package_scope": "research_only",
    "frontend_status": "not_frontend_ready",
    "central_writeback": "no",
    "review_status": "ai_seeded",
}

AXES = (
    "ENTRY",
    "RECORD",
    "RELIEF",
    "PROJECT_SCOPE",
    "PROJECT_LOCATION",
    "PROJECT_TIMING",
    "PROJECT_BUDGET",
    "PROJECT_AUTHORITY",
    "ATTRIBUTION",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_text(rows: Sequence[Mapping[str, object]], fields: Sequence[str]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return buf.getvalue()


def scoped(row: dict[str, str]) -> dict[str, str]:
    return {**row, **SCOPE}


def source_maps() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    return (
        {row["source_id"]: row for row in read_csv(SOURCE_LOG)},
        {row["source_id"]: row for row in read_csv(ARCHIVE_MANIFEST)},
    )


CENTRAL_RECEIPTS = [
    # receipt_id, central source id, publisher, exact locator, notes
    ("W2C2-SR001", "S129", "U.S. Court of Appeals for the Ninth Circuit", "opinion pp.2-4 and disposition; 2020-05-06", "Final appellate merits disposition for the selected Dugong episode."),
    ("W2C2-SR002", "S130", "Okinawa Defense Bureau", "official publication hub for the corrected EIA, posted 2013", "Official project-side record that the corrected EIA was published."),
    ("W2C2-SR003", "S133", "Fukuoka High Court Naha Branch", "judgment operative disposition and damages/injunction sections", "Third Kadena appeal judgment."),
    ("W2C2-SR004", "S135", "Naha District Court Okinawa Branch", "judgment operative disposition and plaintiff-period damages table", "Futenma noise damages judgment."),
    ("W2C2-SR005", "S137", "Naha District Court", "PDF pp.1-4: disposition, 14,263 signatures, two council rejections and duty-action holding", "Ishigaki referendum duty-action judgment."),
    ("W2C2-SR006", "S138", "Ishigaki City", "official council-result page and linked ordinance disposition", "Municipal record of the first referendum ordinance rejection."),
    ("W2C2-SR007", "S140", "Naha District Court", "PDF p.1 operative paragraphs 3-4; pp.197-198 economic-rationality and future-spending holding", "First Awase public-funds judgment; this is the direct bounded project-authority counterexample."),
    ("W2C2-SR008", "S141", "Naha District Court", "FY2017 preserved-case list", "Official existence/termination record for the later Awase wave; substantive result still uses the prior human-reviewed case package."),
    ("W2C2-SR009", "S143", "Okinawa Prefecture", "official litigation annual report, relevant Awase entry", "Official prefectural litigation context."),
    ("W2C2-SR010", "S171", "Nago City", "official election-results landing page", "Official Nago referendum-results entry point."),
    ("W2C2-SR011", "S172", "Nago City", "sheet 市民投票 C1:O15; execution date and four-option totals", "Official Nago referendum workbook."),
    ("W2C2-SR012", "S195", "Yonaguni Town", "PDF pp.1-2: 2015-02-22 referendum and 58.7 percent support statement", "Official mayoral policy statement; organization identity remains a local-material gap."),
    ("W2C2-SR013", "S187", "Okinawa Prefecture", "2019 chronology: referendum and notification to Japan/U.S.", "Official prefectural chronology."),
    ("W2C2-SR014", "S188", "Okinawa Prefecture", "gazette pp.1-4, Ordinance No.62", "Original prefectural referendum ordinance."),
    ("W2C2-SR015", "S190", "Okinawa Prefecture", "gazette pp.1-2, Ordinance No.1 amendment", "Referendum ordinance amendment."),
    ("W2C2-SR016", "S191", "Okinawa Prefecture", "2018-09-20 proposal explanation: request, approximately 93,000 signatures and budget", "Official proposal explanation."),
    ("W2C2-SR017", "S271", "Miyakojima City", "PDF p.1 title/date and pp.1-20 itemized replies", "Official municipal response to the groundwater study group."),
    ("W2C2-SR018", "S273", "Ginowan City Council", "PDF pp.5-7, petition hearing and group activity testimony", "Official committee examination record."),
    ("W2C2-SR019", "S274", "Ginowan City Council", "full opinion text", "Official PFOS/PFOA countermeasure opinion."),
    ("W2C2-SR020", "S287", "Ishigaki City Council", "resolution text: planned 2024-03-11 through 03-14 call, draft issue, anchorage and announced strike", "Proposed council resolution; the vote/disposition is not inferred from the document itself."),
    ("W2C2-SR021", "S288", "National Diet Library / House of Councillors", "statements 133-134, 2024-05-24", "Official Diet record confirms the minister understood the strike as Mar 11-13 action over U.S. vessel use and safety."),
    ("W2C2-SR022", "S283", "Shimbun Akahata", "2018-06-18 dated signature launch report", "Actor-action provenance only; not an official institutional outcome source."),
    ("W2C2-SR048", "S131", "Nature Conservation Society of Japan", "2013 statement on the corrected EIA", "Organization-primary record of its submitted opinion; project effect remains coded from official sources."),
    ("W2C2-SR049", "S132", "Nature Conservation Society of Japan", "2004 statement on the EIA method document", "Organization-primary record of its submitted opinion; not proof that the opinion was adopted."),
]

NEW_RECEIPTS = [
    # receipt, publisher, title, family, url, artifact, mime, locator, notes
    ("W2C2-SR023", "Fukuoka High Court Naha Branch", "平成25年(行コ)第11号 辺野古環境影響評価手続やり直し義務確認等・損害賠償請求控訴事件判決", "official_court_judgment", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-84693.pdf", "henoko_eia_redo_high_court_2014.pdf", "application/pdf", "PDF pp.1-2 claims; p.6 court reasoning begins; pp.11-12 confirmation suits improper, damages rejected, appeal dismissed", "Strong matched EIA judicial-gate case; it entered court but failed at justiciability/rights and relief gates."),
    ("W2C2-SR024", "Fukuoka High Court", "特別保存事件一覧表（平成26年度終局分）", "official_court_case_list", "https://www.courts.go.jp/fukuoka-h/vc-files/fukuoka-h/tokubetuhozon/20250624/syuukyoku/h26syuukyokubun.pdf", "fukuoka_high_court_preservation_2014.pdf", "application/pdf", "PDF p.2 item 22: Naha Branch, Heisei 25 (gyo-ko) 11, terminated 2014-05-27", "Independent official case-number/date cross-check."),
    ("W2C2-SR025", "U.S. Department of Defense, DVIDS / U.S. Navy", "USS Rafael Peralta Conducts Port Visit in Ishigaki, Japan", "official_military_news", "https://www.dvidshub.net/news/466161/uss-rafael-peralta-conducts-port-visit-ishigaki-japan", "uss_rafael_peralta_ishigaki_dvids.html", "text/html", "archived HTML lines 708-720: visit concluded Mar 13; first U.S. destroyer visit; tours and reception", "Closes that the military visit occurred; it does not measure civilian cargo disruption."),
    ("W2C2-SR026", "Okinawa City", "東部海浜開発土地利用計画（修正）", "official_municipal_project_plan", "https://www.city.okinawa.okinawa.jp/documents/1112/totiriyoukeikakuh30.pdf", "awase_land_use_plan_revision_2018.pdf", "application/pdf", "PDF p.4: 185ha plan, 2006 study council, 2007 mayoral policy, Aug 2008 revision start, 2010 95ha city plan, 2011 changes/restart", "The revision process started before the November 2008 district judgment; chronology alone cannot attribute the 95ha plan to litigation."),
    ("W2C2-SR027", "Okinawa Prefecture", "中城湾港（泡瀬地区）", "official_prefectural_project_timeline", "https://www.pref.okinawa.lg.jp/machizukuri/kowankuko/1013146/1022455/1013149/1013151.html", "awase_prefecture_project_timeline.html", "text/html", "archived HTML lines 396-457: project overview, 2010 area reduction, 2011 plan/permit changes and restart", "Official project chronology; it records change, not civic causation."),
    ("W2C2-SR028", "Nago City", "移設問題の動向（年表）", "official_municipal_chronology", "https://www.city.nago.okinawa.jp/kurashi/2018071900226/", "nago_frf_chronology.html", "text/html", "archived HTML lines 318-338, 385-403 and 535-575: referendum, mayoral decisions, location and 2006 V-plan sequence", "Official chronology supports sequence only; causal attribution to the referendum remains contested."),
    ("W2C2-SR029", "Nago City", "普天間飛行場代替施設に関する経緯（unadmitted PDF snapshot）", "unadmitted_source_artifact", "https://www.city.nago.okinawa.jp/kurashi/2018071900226/", "nago_frf_chronology_2018.pdf", "application/pdf", "PDF pp.1-2 mirror key chronology entries", "Preserved for provenance only. Its original direct PDF URL was not closed, so no analytical row cites this receipt; W2C2-SR028 is the admitted live-page record."),
    ("W2C2-SR030", "Ministry of Defense Japan", "令和6年版防衛白書 資料編", "official_defense_whitepaper", "https://www.mod.go.jp/j/press/wp/wp2024/pdf/R06shiryo.pdf", "mod_whitepaper_2024_reference_timeline.pdf", "application/pdf", "PDF pp.105-107, 資料31: 2016 settlement/work pause, later resumption, 2020 change application and 2024 Oura-side start", "Government/court sequence comparator; not an NGO-attribution source."),
    ("W2C2-SR031", "Miyakojima City Council", "平成28年第7回定例会上程案件处理结果", "official_municipal_council_result", "https://www.city.miyakojima.lg.jp/gyosei/gikai/files/28.dai7kaijyouteiannkennsyorikekka.pdf", "miyako_council_2016_session7_dispositions.pdf", "application/pdf", "PDF p.4, petition No.26 and 2016-09-29 non-adoption", "Formal legislative gate after docketing, not absence of entry."),
    ("W2C2-SR032", "Miyakojima City Council", "平成28年第7回宮古島市議会定例会会議録", "official_municipal_council_minutes", "https://www.city.miyakojima.lg.jp/gyosei/gikai/files/h28.9.dai7kai.kaigiroku.pdf", "miyako_council_2016_session7_minutes.pdf", "application/pdf", "case disposition table and petition No.26 deliberation", "Official processing record."),
    ("W2C2-SR033", "Fukuoka High Court Naha Branch", "令和2年(ネ)第61号 安保法制違憲国家賠償請求控訴事件判決", "official_court_judgment", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-90088.pdf", "okinawa_security_law_appeal_2021.pdf", "application/pdf", "PDF pp.1 and 4-7", "This case entered court and is excluded from the strict non-entry denominator; retained as a relief/justiciability control."),
    ("W2C2-SR034", "Fukuoka High Court", "特別保存に付した事件（令和3年終局分）", "official_court_case_list", "https://www.courts.go.jp/fukuoka-h/vc-files/fukuoka-h/tokubetuhozon/20250624/syuukyoku/r3syuukyokubun.pdf", "fukuoka_high_court_preservation_2021.pdf", "application/pdf", "case table item 13", "Case-number/date cross-check."),
    ("W2C2-SR035", "Yonaguni Town", "与那国住民説明会における質問回答", "official_municipal_qa", "https://www.town.yonaguni.okinawa.jp/docs/2023060500011/file_contents/shitumon.pdf", "yonaguni_2023_resident_meeting_qa.pdf", "application/pdf", "full Q&A", "Shows a public Q&A artifact; it does not prove item-by-item response to the earlier ten-question letter."),
    ("W2C2-SR036", "Yonaguni Town", "駐屯地への地対空誘導弾部隊の配備に関する追加質問への回答", "official_municipal_followup", "https://www.town.yonaguni.okinawa.jp/docs/2023072500016/", "yonaguni_2023_followup_qa.html", "text/html", "page and linked follow-up answer", "Shows an alternative public-response channel; linkage to the original request remains unclosed."),
    ("W2C2-SR037", "U.S. National Archives / Trump White House archive", "Stop the landfill of Henoko / Oura Bay until a referendum can be held in Okinawa", "official_archived_petition", "https://petitions.trumpwhitehouse.archives.gov/petition/stop-landfill-henoko-oura-bay-until-referendum-can-be-held-okinawa", "whitehouse_henoko_petition_archive.html", "text/html", "archived page title, creation date, 212,945 signatures and request", "Platform entry is visible; an issue-specific official response was not found in the bounded trace."),
    ("W2C2-SR038", "Trump White House archive", "About We the People", "official_platform_rules", "https://petitions.trumpwhitehouse.archives.gov/about", "whitehouse_petitions_about_archive.html", "text/html", "threshold and response-process description", "Platform rule; not proof of an issue-specific response."),
    ("W2C2-SR039", "Okinawa Prefecture", "調停とは（手続きの流れ）", "official_prefectural_procedure", "https://www.pref.okinawa.lg.jp/kensei/shingikai/1014397/1014517/1004600/1004614.html", "okinawa_pollution_mediation_procedure.html", "text/html", "procedure-flow section", "Procedure design only; the 2026 dismissal notice itself is not publicly archived in this package."),
]

W200_RECEIPTS = [
    ("W2C2-SR040", "W2C-SR009"),
    ("W2C2-SR041", "W2C-SR010"),
    ("W2C2-SR042", "W2C-SR011"),
    ("W2C2-SR043", "W2C-SR012"),
    ("W2C2-SR044", "W2C-SR013"),
    ("W2C2-SR045", "W2C-SR014"),
    ("W2C2-SR046", "W2C-SR015"),
    ("W2C2-SR047", "W2C-SR016"),
]


ANALYSIS_UNITS = [
    {
        "episode_id": "TE01", "analysis_unit_id": "TE01", "receipts": "W2C2-SR001;W2C2-SR040;W2C2-SR041;W2C2-SR042",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "yes_bounded_attorney_fee_only_pending_review",
        "entry_claim": "Federal litigation was docketed and decided.", "record_claim": "The appellate decisions and payment records are observable.",
        "relief_claim": "Official records show a case-related attorney-fee award/payment, not merits relief to the underlying project claim.",
        "projects": {}, "attribution": "not_applicable_without_confirmed_project_change",
        "notes": "Earthjustice reported USD 276,345.50 while Treasury records USD 280,000; the USD 3,654.50 difference remains unreconciled.",
    },
    {
        "episode_id": "TE02", "analysis_unit_id": "TE02", "receipts": "W2C2-SR002;W2C2-SR048;W2C2-SR049",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "no_in_reviewed_record",
        "entry_claim": "NACSJ comments are documented within the EIA process.", "record_claim": "The corrected EIA and organization comment records are observable.",
        "relief_claim": "No redo order or direct relief is established by the selected administrative-comment record.",
        "projects": {}, "attribution": "not_applicable_without_confirmed_project_change", "notes": "Formal comment is not the same as adoption of the comment.",
    },
    {
        "episode_id": "TE03", "analysis_unit_id": "TE03", "receipts": "W2C2-SR003",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "yes_bounded_past_damages",
        "entry_claim": "The third Kadena action entered civil litigation.", "record_claim": "The appellate judgment records liability and rejected claims.",
        "relief_claim": "Past noise injury received partial damages; injunction and future-damages claims were rejected.",
        "projects": {"PROJECT_AUTHORITY": ("no_requested_operational_injunction", "The requested operational injunction was not granted.")},
        "attribution": "not_applicable_without_confirmed_project_change", "notes": "Damages do not mean aircraft noise or operations ceased.",
    },
    {
        "episode_id": "TE04", "analysis_unit_id": "TE04", "receipts": "W2C2-SR004",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "yes_bounded_past_damages",
        "entry_claim": "The Futenma noise claims entered civil litigation.", "record_claim": "The judgment identifies compensated plaintiffs and periods.",
        "relief_claim": "Specified plaintiffs and periods received damages; no operational injunction is established.",
        "projects": {"PROJECT_AUTHORITY": ("no_requested_operational_injunction", "No executable restriction on flight operations is established in the selected judgment.")},
        "attribution": "not_applicable_without_confirmed_project_change", "notes": "Relief remains case- and period-specific.",
    },
    {
        "episode_id": "TE05", "analysis_unit_id": "TE05", "receipts": "W2C2-SR005;W2C2-SR006",
        "entry": "yes_multi_stage_terminal_gate_blocked", "record": "yes_selection_condition", "relief": "no_in_reviewed_record",
        "entry_claim": "The direct request entered council processing and a duty-action entered court, but the intended referendum never occurred.",
        "record_claim": "Council dispositions and the court judgment are observable.", "relief_claim": "The duty-action was procedurally dismissed and no referendum was ordered.",
        "projects": {}, "attribution": "not_applicable_without_confirmed_project_change", "notes": "Requester organization and individual plaintiffs remain distinct.",
    },
    {
        "episode_id": "TE06", "analysis_unit_id": "TE06-W1", "receipts": "W2C2-SR007",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "yes_bounded_future_spending_restriction",
        "entry_claim": "The first Awase public-funds action entered court.", "record_claim": "The district judgment is a full official record.",
        "relief_claim": "The court prohibited future public spending, contracts and obligations, subject to already-incurred liabilities.",
        "projects": {
            "PROJECT_BUDGET": ("yes_bounded", "Future public expenditure and new obligations were judicially restricted."),
            "PROJECT_AUTHORITY": ("yes_bounded", "The judgment imposed an executable restriction on prefectural and city financial authority."),
        },
        "attribution": "direct_official_bounded", "notes": "This is a real counterexample to a blanket 'record/compensation only' ceiling.",
    },
    {
        "episode_id": "TE06", "analysis_unit_id": "TE06-W2", "receipts": "W2C2-SR008;W2C2-SR009;W2C2-SR027",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "no_second_wave_relief",
        "entry_claim": "The later Awase public-funds wave entered litigation.", "record_claim": "Official case and project records establish later termination and project restart.",
        "relief_claim": "The residents lost the second wave; no continuing equivalent restriction is established.",
        "projects": {"PROJECT_AUTHORITY": ("no_continuing_restriction_established", "The later record does not preserve the first-wave restriction as a durable bar.")},
        "attribution": "not_applicable_without_confirmed_civic_project_change", "notes": "The two waves must never be collapsed into one win/loss value.",
    },
    {
        "episode_id": "TE07", "analysis_unit_id": "TE07", "receipts": "W2C2-SR010;W2C2-SR011;W2C2-SR028",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "not_applicable_referendum_output",
        "entry_claim": "The direct request produced an ordinance and advisory referendum.", "record_claim": "Official results and the post-vote municipal chronology are observable.",
        "relief_claim": "A referendum result is coded as a formal output, not individual legal relief.",
        "projects": {
            "PROJECT_LOCATION": ("candidate_change_indirect_contested", "The official chronology records later location/design decisions, but it does not attribute them to the referendum alone."),
            "PROJECT_SCOPE": ("candidate_change_indirect_contested", "The proposal evolved after the vote; referendum causation is not closed."),
        },
        "attribution": "indirect_contested", "notes": "Opposition majority did not legally bind the mayor; later local-government and intergovernmental decisions are competing causes.",
    },
    {
        "episode_id": "TE08", "analysis_unit_id": "TE08", "receipts": "W2C2-SR012",
        "entry": "yes_selection_condition_with_local_identity_gap", "record": "yes_selection_condition_with_local_identity_gap", "relief": "not_applicable_referendum_output",
        "entry_claim": "The referendum was held; organization-level carrier identity remains locally unresolved.", "record_claim": "The town policy statement records the vote and administrative interpretation.",
        "relief_claim": "The vote is a formal output rather than individual relief.", "projects": {},
        "attribution": "not_applicable_without_confirmed_project_change", "notes": "Do not upgrade A014/A015 identity from the vote record.",
    },
    {
        "episode_id": "TE09", "analysis_unit_id": "TE09", "receipts": "W2C2-SR013;W2C2-SR014;W2C2-SR015;W2C2-SR016",
        "entry": "yes_selection_condition", "record": "yes_selection_condition", "relief": "not_applicable_referendum_output",
        "entry_claim": "The direct request produced an ordinance and prefecture-wide vote.", "record_claim": "Official gazettes, legislative records and chronology preserve the output and notifications.",
        "relief_claim": "The referendum and notifications are formal outputs, not a binding stop order.", "projects": {},
        "attribution": "not_applicable_without_confirmed_project_change", "notes": "The vote did not automatically suspend construction.",
    },
    {
        "episode_id": "TE10", "analysis_unit_id": "TE10", "receipts": "W2C2-SR017",
        "entry": "candidate_pending_event_review", "record": "candidate_pending_event_review", "relief": "not_applicable_administrative_reply",
        "entry_claim": "An official itemized municipal response exists, but the event remains outside the human-reviewed central event layer.",
        "record_claim": "The official response is observable as a research-only candidate.", "relief_claim": "A written reply is not itself policy relief.",
        "projects": {}, "attribution": "unknown_pending_event_review", "notes": "Do not infer acceptance of the groundwater-risk interpretation.",
    },
    {
        "episode_id": "TE11", "analysis_unit_id": "TE11", "receipts": "W2C2-SR018;W2C2-SR019",
        "entry": "candidate_pending_event_review", "record": "candidate_pending_event_review", "relief": "unknown",
        "entry_claim": "Official council records support a petition/opinion pathway, pending event-fact review.",
        "record_claim": "Committee and opinion records are observable.", "relief_claim": "Implementation, source attribution and health causation remain unclosed.",
        "projects": {}, "attribution": "unknown_pending_event_review", "notes": "Official record does not identify the pollution source or establish implementation.",
    },
    {
        "episode_id": "TE12", "analysis_unit_id": "TE12", "receipts": "W2C2-SR020;W2C2-SR021;W2C2-SR025",
        "entry": "candidate_noninstitutional_workplace_action", "record": "candidate_pending_event_review", "relief": "not_applicable_workplace_action",
        "entry_claim": "This is a workplace/port action rather than a classic institutional-entry episode.",
        "record_claim": "Official Japanese and U.S. records confirm the strike context and completed port visit.", "relief_claim": "No individual legal relief was requested in this action.",
        "projects": {
            "PROJECT_TIMING": ("no_military_visit_change_confirmed", "The U.S. Navy reports the visit concluded on Mar 13 as scheduled within the strike window."),
            "PROJECT_LOCATION": ("not_attributable_to_strike", "Offshore anchorage/draft constraints were documented before the strike and are not attributed to the strike."),
        },
        "attribution": "no_civic_attribution_to_military_visit_change", "notes": "Civilian cargo disruption is a separate outcome and must not be rewritten as cancellation of the military visit.",
    },
    {
        "episode_id": "TE13", "analysis_unit_id": "TE13", "receipts": "W2C2-SR022",
        "entry": "candidate_participation_not_independent_venue_entry", "record": "candidate_action_record_only", "relief": "not_applicable_participation",
        "entry_claim": "The source documents a dated signature-mobilization action, not an independent institutional entry by A115.",
        "record_claim": "Only the participation channel is observable in this row.", "relief_claim": "No actor-specific relief can be assigned.",
        "projects": {}, "attribution": "not_applicable_participation_only", "notes": "Do not attribute all 92,848 signatures, the ordinance or the referendum outcome to A115.",
    },
]


NEGATIVE_ROWS = [
    ("W2C-NEG001", "TN01", "宫古2016住民投票陳情不採択", "municipal_referendum", "Miyako", "2016", "petition_for_referendum", "municipal_council", "post_entry_legislative_disposition", "yes_docketed", "yes_nonadoption_record", "W2C2-SR031;W2C2-SR032", "TE05;TE08", "strict_matched_gate", "included_matched_gate", "none", "A referendum petition was docketed and deliberated but not adopted.", "Do not describe it as never entering the council or as proof that all Miyako referendum demands were blocked."),
    ("W2C-NEG002", "TN02", "PFAS公害调停因防卫设施除外而却下", "administrative_eligibility", "Ginowan/Okinawa", "2025-2026", "pollution_mediation_application", "Okinawa pollution mediation", "pre_substantive_eligibility", "reported_received", "reported_dismissal_primary_missing", "W2C2-SR039", "TE11", "bounded_unresolved", "included_exploratory_unresolved", "application_and_dismissal_originals_missing", "The available package indicates a reported eligibility gate; the procedure design is official.", "Do not freeze the dismissal reason or any PFAS source/health finding until the application and decision originals are obtained."),
    ("W2C-NEG003", "TN03", "安保法制违宪冲绳诉讼未进入违宪判断", "judicial_legal_interest", "Okinawa", "2017-2021", "damages_litigation", "Japanese courts", "post_entry_relief_and_merits_gate", "yes_heard", "yes_judgment", "W2C2-SR033;W2C2-SR034", "TE03;TE04", "outside_strict_nonentry", "excluded_from_strict_nonentry_retained_control", "none", "The claims entered court and failed at protected-interest/damage and constitutional-merits gates.", "Do not count this as no institutional entry."),
    ("W2C-NEG004", "TN04", "与那国导弹问题书面答复被拒（对应未闭合）", "administrative_response_modality", "Yonaguni", "2023", "written_question_request", "Okinawa Defense Bureau/local briefing", "response_format_gate", "reported_received", "official_alternative_QA_exists_linkage_unclosed", "W2C2-SR035;W2C2-SR036", "TE08;TE10", "bounded_unresolved", "included_exploratory_unresolved", "original_letter_and_official_refusal_missing", "Public Q&A channels existed, while the requested written-response linkage remains unclosed.", "Do not call this total administrative silence or transfer the 15 signers to A016."),
    ("W2C-NEG005", "TN05", "边野古白宫请愿达标后政策回应未闭合", "transnational_petition_response", "Henoko/Oura Bay", "2018-2019", "online_petition", "White House We the People", "post_entry_policy_response_trace", "yes_threshold_met", "yes_petition_record_response_not_located", "W2C2-SR037;W2C2-SR038", "TE01;TE09", "response_trace_control", "included_bounded_response_trace", "issue_specific_response_not_found_in_bounded_archive", "The official archive preserves 212,945 signatures; no issue-specific policy update was located in the bounded trace.", "Do not claim that no response ever existed or that the petition changed/failed to change construction."),
    ("W2C-NEG006", "", "边野古EIA重做义务确认诉讼被程序性驳回", "administrative_EIA_judicial", "Henoko/Oura Bay", "2009-2014", "confirmation_and_damages_litigation", "Fukuoka High Court Naha Branch", "post_entry_justiciability_and_relief_gate", "yes_heard", "yes_official_judgment", "W2C2-SR023;W2C2-SR024", "TE02", "strict_matched_judicial_gate", "included_matched_gate", "none", "The redo/illegality confirmation suits were held improper and damages were rejected; the appeal was dismissed.", "Do not treat this as rejection of all EIA comment participation or as proof the EIA itself had no environmental effects."),
]


PROJECT_ROWS = [
    ("W2C-PC001", "Awase public-funds litigation first wave", "Awase/Okinawa City", "2008", "PROJECT_BUDGET;PROJECT_AUTHORITY", "Future spending and new obligations legally available", "Court prohibited future spending/contracts/obligations except liabilities already incurred", "Naha District Court", "W2C2-SR007", "TE06-W1", "resident_public_funds_litigation", "action preceded judgment", "direct_official_bounded", "operative order expressly responds to plaintiffs' request", "none needed for the existence of the order; durability is tested separately", "confirmed_bounded_counterexample", "The first-wave judgment imposed an executable future-spending/authority restriction.", "Do not infer permanent cancellation or attribute the later area reduction to this order."),
    ("W2C-PC002", "Awase land-use plan", "Awase/Okinawa City", "2006-2011", "PROJECT_SCOPE", "Approximately 185ha land-use plan", "Current approximately 95ha plan; official plan/permit changes in 2011", "Okinawa City/Okinawa Prefecture", "W2C2-SR026;W2C2-SR027", "TE06", "litigation overlaps project-review period", "municipal review started 2006; revision work Aug 2008; judgment later in 2008", "chronology_not_causal", "No official source reviewed attributes the reduction to the lawsuit", "study council, mayoral policy and administrative plan review began before judgment", "confirmed_change_nonattributed", "Official project records show a 185ha-to-95ha scope change.", "Do not infer the court or NGO caused the area reduction from temporal proximity."),
    ("W2C-PC003", "Futenma Replacement Facility ground-improvement revision", "Henoko/Oura Bay", "2019-2024", "PROJECT_SCOPE;PROJECT_TIMING;PROJECT_BUDGET", "Earlier construction plan and cost basis", "Ground-improvement/change application and rough total estimate about JPY 930bn", "Ministry of Defense/Okinawa Defense Bureau", "W2C2-SR030;W2C2-SR043;W2C2-SR044", "TE01;TE02;TE09", "civic actions occurred in same project arena", "official change application identifies ground/security work", "none_official_to_civic_action", "Technical/geotechnical and security design factors are stated", "technical/geotechnical project requirements", "confirmed_change_non_civic_comparator", "The project changed in scope/cost/time for officially stated technical reasons.", "Do not attribute this change to NGO action or call JPY 930bn cumulative expenditure."),
    ("W2C-PC004", "Futenma Replacement Facility 2016 pause/resumption", "Henoko/Oura Bay", "2016-2017", "PROJECT_TIMING", "Construction underway/disputed", "Work paused under national-prefectural court settlement and later resumed after government/court sequence", "Japan/Okinawa intergovernmental litigation and Ministry of Defense", "W2C2-SR030", "TE01;TE02;TE09", "civic movement is background but not a party to the settlement", "official chronology names settlement and later resumption", "none_official_to_civic_action", "Government-to-government legal conflict", "intergovernmental dispute and judicial/administrative decisions", "confirmed_change_non_civic_comparator", "Official records show a temporary project-timing change.", "Do not attribute the pause to NGO activity without party/causal evidence."),
    ("W2C-PC005", "Nago/FRF location and design evolution", "Nago/Henoko", "1997-2006", "PROJECT_LOCATION;PROJECT_SCOPE", "Sea-based heliport proposal", "Henoko coastal waters, conditional local acceptance, then coastal V-shaped plan", "Okinawa governor/Nago mayor/Japan-U.S. governments", "W2C2-SR028", "TE07", "1997 referendum opposition majority preceded later decisions", "referendum, mayoral acceptance, governor decisions and intergovernmental agreements occur in sequence", "indirect_contested", "No reviewed official source assigns the whole design evolution to the referendum", "local-government negotiation, elections, Japan-U.S. agreement and technical planning", "candidate_change_attribution_review", "The official chronology documents design/location evolution after the referendum.", "Do not write that the referendum caused the V-shaped design or relocation decision."),
    ("W2C-PC006", "USS Rafael Peralta Ishigaki port call", "Ishigaki Port", "2024-03-11/2024-03-13", "PROJECT_TIMING;PROJECT_LOCATION", "Planned first destroyer visit with draft/anchorage constraints", "Visit completed Mar 13; no military-visit cancellation or timing change confirmed", "U.S. Navy; Japanese Diet record", "W2C2-SR020;W2C2-SR021;W2C2-SR025", "TE12", "port workers struck during the visit window", "strike and completed visit overlap", "no_civic_change_confirmed", "Official U.S. record confirms completion; Japanese record confirms strike context", "Draft/berth constraints and separate civilian cargo effects", "falsified_as_military_project_change", "The strike did not prevent the documented military visit.", "Do not erase civilian logistics disruption or attribute offshore anchorage to the strike."),
]


def build_positive_rows(te_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    units_by_episode: dict[str, list[str]] = defaultdict(list)
    for unit in ANALYSIS_UNITS:
        units_by_episode[unit["episode_id"]].append(unit["analysis_unit_id"])
    rows = []
    for index, te in enumerate(te_rows, start=1):
        eid = te["episode_id"]
        rows.append(scoped({
            "sample_id": f"W2C-POS{index:03d}",
            "selection_frame_id": "USF-W2C-ENTRY13-2026-08-22",
            "episode_id": eid,
            "analysis_unit_ids": ";".join(units_by_episode[eid]),
            "short_label": te["short_label"],
            "route_family": te["route_family"],
            "place": te["place"],
            "action_type": te["route_family"],
            "intended_venue": te["venue"],
            "source_review_status": te["review_status"],
            "entry_condition": "selected_on_documented_or_candidate_formal_pathway",
            "record_condition": "selected_on_observable_or_candidate_output",
            "split_rule": "split_into_first_and_second_litigation_waves" if eid == "TE06" else "one_analysis_unit",
            "legacy_source_refs": te["source_refs"],
            "inclusion_status": "fixed_positive_frame_retained",
            "selection_bias": "ENTRY/RECORD are selection conditions; this frame cannot estimate an entry success rate.",
            "notes": "TE10-TE13 remain candidate event facts; retention does not upgrade them." if eid in {"TE10", "TE11", "TE12", "TE13"} else "No new central fact approval is created.",
        }))
    return rows


def build_negative_rows() -> list[dict[str, str]]:
    rows = []
    for raw in NEGATIVE_ROWS:
        (
            negative_id, legacy_case_id, label, route, place, period, action,
            venue, gate, entry, record, receipts, matches, frame_fit, inclusion,
            gap, allowed, prohibited,
        ) = raw
        rows.append(scoped({
            "negative_id": negative_id,
            "selection_frame_id": "USF-W2C-NONENTRY-MATCHED-2026-08-22",
            "legacy_case_id": legacy_case_id,
            "short_label": label,
            "route_family": route,
            "place": place,
            "period": period,
            "action_type": action,
            "intended_venue": venue,
            "gate_position": gate,
            "entry_status": entry,
            "record_status": record,
            "match_to_episode_ids": matches,
            "matching_variables": "route_family;place;period;action_type;intended_venue",
            "source_receipt_ids": receipts,
            "secondary_source_refs": legacy_case_id,
            "frame_fit": frame_fit,
            "inclusion_status": inclusion,
            "authority_gap": gap,
            "allowed_claim": allowed,
            "prohibited_inference": prohibited,
        }))
    return rows


def build_project_rows() -> list[dict[str, str]]:
    rows = []
    for raw in PROJECT_ROWS:
        (
            pid, project, place, period, axes, pre_state, post_state, authority,
            receipts, episodes, action, order, attribution, evidence, competing,
            disposition, allowed, prohibited,
        ) = raw
        rows.append(scoped({
            "project_change_id": pid,
            "selection_frame_id": "USF-W2C-PROJECTCHANGE-COUNTEREX-2026-08-22",
            "project": project,
            "place": place,
            "period": period,
            "change_axes": axes,
            "pre_state": pre_state,
            "post_state": post_state,
            "decision_authority": authority,
            "source_receipt_ids": receipts,
            "related_episode_ids": episodes,
            "civic_action_candidate": action,
            "temporal_order": order,
            "attribution_status": attribution,
            "attribution_evidence": evidence,
            "competing_explanation": competing,
            "candidate_disposition": disposition,
            "allowed_claim": allowed,
            "prohibited_inference": prohibited,
        }))
    return rows


def build_outcomes(te_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    te_map = {row["episode_id"]: row for row in te_rows}
    rows: list[dict[str, str]] = []
    counter = 1
    for unit in ANALYSIS_UNITS:
        te = te_map[unit["episode_id"]]
        for axis in AXES:
            if axis == "ENTRY":
                status, claim, selection = unit["entry"], unit["entry_claim"], "yes"
            elif axis == "RECORD":
                status, claim, selection = unit["record"], unit["record_claim"], "yes"
            elif axis == "RELIEF":
                status, claim, selection = unit["relief"], unit["relief_claim"], "no"
            elif axis == "ATTRIBUTION":
                status = unit["attribution"]
                claim = (
                    "Attribution is coded independently from chronology and project change; "
                    f"current unit status is {status}."
                )
                selection = "no"
            else:
                status, claim = unit["projects"].get(
                    axis,
                    (
                        "not_demonstrated_in_reviewed_record",
                        "The reviewed record does not establish this project-axis change; this is not proof that no change occurred.",
                    ),
                )
                selection = "no"
            rows.append(scoped({
                "outcome_id": f"W2C-OUT{counter:03d}",
                "selection_frame_id": "USF-W2C-ENTRY13-2026-08-22",
                "episode_id": unit["episode_id"],
                "analysis_unit_id": unit["analysis_unit_id"],
                "short_label": te["short_label"],
                "route_family": te["route_family"],
                "place": te["place"],
                "axis": axis,
                "axis_status": status,
                "status_basis": claim,
                "observation_unit": "action_x_venue" if axis in {"ENTRY", "RECORD", "RELIEF"} else "project_x_decision",
                "source_receipt_ids": unit["receipts"],
                "legacy_source_refs": te["source_refs"],
                "exact_locator": "See source_receipts_v1.csv; row-specific locators remain source-bound.",
                "evidence_status": "candidate_event_pending" if te["review_status"].startswith("analytic_candidate") else "official_or_formal_record_research_recode",
                "attribution_status": unit["attribution"],
                "allowed_claim": claim,
                "prohibited_inference": "Do not infer causation from temporal order, count ENTRY/RECORD as success, or generalize beyond the selected episode.",
                "selection_condition": selection,
                "notes": unit["notes"],
            }))
            counter += 1
    return rows


def build_causal_evidence(project_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, project in enumerate(project_rows, start=1):
        rows.append(scoped({
            "causal_evidence_id": f"W2C-CE{index:03d}",
            "project_change_id": project["project_change_id"],
            "action_evidence": project["civic_action_candidate"],
            "decision_evidence": project["post_state"],
            "time_order_evidence": project["temporal_order"],
            "causal_statement_evidence": project["attribution_evidence"],
            "source_receipt_ids": project["source_receipt_ids"],
            "attribution_status": project["attribution_status"],
            "missing_causal_link": "none_for_bounded_order" if project["project_change_id"] == "W2C-PC001" else "official_civic_attribution_not_closed",
            "principal_attention": "yes" if project["project_change_id"] in {"W2C-PC001", "W2C-PC005"} else "no",
            "notes": project["prohibited_inference"],
        }))
    return rows


def build_inclusion_log(positive: list[dict[str, str]], negative: list[dict[str, str]], projects: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    index = 1
    for row in positive:
        rows.append(scoped({
            "log_id": f"W2C-IE{index:03d}", "selection_frame_id": row["selection_frame_id"],
            "unit_id": row["episode_id"], "unit_type": "positive_episode", "decision": "include_fixed_input",
            "inclusion_reason": row["inclusion_status"], "exclusion_reason": "",
            "matching_variables": "route;place;period;venue", "decision_date": RUN_DATE,
            "change_trigger": row["split_rule"], "notes": row["selection_bias"],
        })); index += 1
    for row in negative:
        decision = "exclude_strict_keep_control" if row["inclusion_status"].startswith("excluded") else "include_bounded"
        rows.append(scoped({
            "log_id": f"W2C-IE{index:03d}", "selection_frame_id": row["selection_frame_id"],
            "unit_id": row["negative_id"], "unit_type": "matched_gate_candidate", "decision": decision,
            "inclusion_reason": row["frame_fit"], "exclusion_reason": row["authority_gap"] if decision.startswith("exclude") else "",
            "matching_variables": row["matching_variables"], "decision_date": RUN_DATE,
            "change_trigger": "prior negative package reclassified by gate position", "notes": row["prohibited_inference"],
        })); index += 1
    for row in projects:
        rows.append(scoped({
            "log_id": f"W2C-IE{index:03d}", "selection_frame_id": row["selection_frame_id"],
            "unit_id": row["project_change_id"], "unit_type": "project_change_candidate", "decision": row["candidate_disposition"],
            "inclusion_reason": "official before/after or decision record available", "exclusion_reason": "",
            "matching_variables": "project;place;period;axis;decision authority", "decision_date": RUN_DATE,
            "change_trigger": "counterexample search", "notes": row["prohibited_inference"],
        })); index += 1
    return rows


def build_negative_search_log() -> list[dict[str, str]]:
    raw = [
        ("international_legal", "TE01/TE09", "White House petition archive; federal appellate records", "bounded_complete_for_named_candidates", "Threshold-entry case found; issue-specific response trace not closed", "No unmatched no-entry denominator can be claimed."),
        ("administrative_EIA", "TE02", "official EIA hub; court judgments/case lists", "matched_gate_found", "EIA redo/illegality confirmation litigation dismissed and damages rejected", "Administrative comment entry and judicial redo gate are distinct venues."),
        ("noise_civil_litigation", "TE03/TE04", "official court judgments and case search", "no_defensible_nonentry_match_found", "Reviewed candidates entered and received judgments", "Absence of a matched candidate is not a zero rate."),
        ("public_funds_litigation", "TE06", "first judgment, later case record, project timeline", "within_episode_wave_contrast", "Opposite waves occur within TE06", "Do not double-count the second wave as an independent actor/case denominator."),
        ("referendum_ordinance", "TE05/TE07/TE08/TE09", "council dispositions, ordinances, court and election records", "matched_gates_found", "Miyako petition and Ishigaki terminal referendum gate identified", "Council processing is entry even when the requested referendum is blocked."),
        ("local_administrative", "TE10/TE11", "official response/Q&A/procedure pages", "mixed_primary_coverage", "PFAS dismissal original missing; Yonaguni response linkage unclosed", "Keep both cases unresolved."),
        ("labor_workplace", "TE12", "Diet, council and U.S. Navy records", "effect_trace_closed_for_military_visit", "Strike occurred; destroyer visit completed", "Civilian cargo disruption remains outside military project-change axis."),
        ("membership_mobilization", "TE13", "dated organization/party report and prefectural referendum record", "not_independent_entry_case", "Actor-specific mobilization found but no separate venue entry", "Do not manufacture a negative institutional case from participation-only evidence."),
    ]
    rows = []
    for index, item in enumerate(raw, start=1):
        stratum, match, families, status, result, limit = item
        rows.append(scoped({
            "search_log_id": f"W2C-NS{index:03d}", "search_stratum": stratum,
            "matched_episode_ids": match, "official_source_families_checked": families,
            "search_status": status, "result": result, "bounded_limit": limit,
            "search_date": RUN_DATE, "searcher": "AI research pass; principal review pending",
            "notes": "Negative search is a documented design, not proof of real-world absence.",
        }))
    return rows


def build_competing_explanations() -> list[dict[str, str]]:
    raw = [
        ("venue_design", "Formal rules may admit, redirect or exclude claims independently of their substantive evidence.", "TN01;TN02;W2C-NEG006"),
        ("justiciability_claim_fit", "Standing, confirmation interest, protected interest or remedy design can stop adjudication before project merits.", "TE05;W2C-NEG003;W2C-NEG006"),
        ("project_action_unit_mismatch", "An action-level record or damages award need not map to facility-level change.", "TE01;TE03;TE04;TE09"),
        ("technical_geotechnical_change", "Project scope/cost/timing can change for ground, engineering or safety reasons rather than civic action.", "W2C-PC003"),
        ("intergovernmental_conflict", "National-prefectural litigation and settlement can change project timing without NGO party status.", "W2C-PC004"),
        ("local_government_negotiation", "Mayoral, gubernatorial and Japan-U.S. bargaining can alter location/design after a referendum.", "W2C-PC005"),
        ("preexisting_plan_review", "Administrative plan review that starts before judgment weakens later post hoc attribution.", "W2C-PC002"),
        ("archive_visibility", "Official online preservation differs by venue, year and record type; missing response is not no response.", "W2C-NEG002;W2C-NEG004;W2C-NEG005"),
        ("actor_document_capacity", "Organizations with litigation counsel or durable websites leave more linkable records than short-lived carriers.", "all_frames"),
    ]
    return [scoped({
        "explanation_id": f"W2C-XP{i:03d}", "explanation_family": family,
        "mechanism": mechanism, "applies_to_units": units,
        "observable_discriminator": "Compare official gate/decision language, time order and source-family coverage before assigning causation.",
        "current_status": "live_competing_explanation", "notes": "Not a fact edge or causal conclusion.",
    }) for i, (family, mechanism, units) in enumerate(raw, start=1)]


def build_review_queue() -> list[dict[str, str]]:
    raw = [
        ("P0", "TE01", "Does the attorney-fee award/payment count as bounded RELIEF while remaining distinct from merits relief?", "Earthjustice FY2021 Form 990; Treasury API/workbook; appellate opinion", "USD 276,345.50 versus USD 280,000 remains unreconciled", "accept_bounded;revise;defer_primary;reject"),
        ("P0", "TE06-W1", "Confirm PROJECT_BUDGET=yes_bounded and PROJECT_AUTHORITY=yes_bounded from the first-wave operative order.", "S140/W2C2-SR007 pp.1,197-198", "Durability and later project course must remain separate", "accept;revise;defer;reject"),
        ("P0", "W2C-PC002", "Confirm that the 185ha-to-95ha scope change cannot currently be attributed to the lawsuit.", "W2C2-SR026;W2C2-SR027;W2C2-SR007", "Revision process began before judgment; causal statement absent", "accept_nonattribution;revise;defer"),
        ("P0", "W2C-PC005", "How strongly may the Nago/FRF design evolution be linked to the 1997 referendum?", "W2C2-SR028 plus any explicit decision memo", "Chronology is clear; civic attribution is not", "indirect_contested;defer_primary;reject_link"),
        ("P0", "W2C-NEG006", "Accept the EIA redo lawsuit as a matched judicial gate case rather than a no-entry case?", "W2C2-SR023;W2C2-SR024", "It entered court and failed at justiciability/relief", "accept_gate;revise;exclude"),
        ("P0", "W2C-NEG002", "Can the PFAS mediation dismissal reason be frozen?", "Original application and dismissal notice", "Decisive primary documents absent", "accept_candidate;defer_primary;reject"),
        ("P1", "W2C-NEG004", "Can the ten-question letter be mapped to the later official Q&A?", "Original letter, formal refusal and item-level crosswalk", "Refusal currently resident-attributed; alternative Q&A exists", "accept_narrow;revise;defer_primary;reject"),
        ("P0", "TE10;TE11;TE12;TE13", "Which candidate event facts and outcome axes may be human-approved?", "Official rows listed in source receipts; actor-action sources where needed", "Central event gate is still pending", "accept_each;revise_each;defer_each;reject_each"),
        ("P0", "TE12", "Confirm that the destroyer visit completed and no military-visit timing change is attributable to the strike.", "W2C2-SR020;W2C2-SR021;W2C2-SR025", "Civilian cargo effect is separate", "accept;revise;defer"),
        ("P0", "SYNTHESIS", "Replace the blanket result-ceiling claim with the bounded formulation proposed in README?", "outcome ledger, project-change table and competing explanations", "One direct budget/authority counterexample weakens the blanket claim", "accept_revised_claim;revise;defer"),
    ]
    rows = []
    for i, (priority, unit, question, material, gap, decisions) in enumerate(raw, start=1):
        rows.append({
            "review_item_id": f"W2C-HR{i:03d}", "priority": priority,
            "unit_ids": unit, "review_question": question, "required_material": material,
            "current_gap": gap, "allowed_decisions": decisions,
            "provisional_status": "ai_seeded_research_only_not_frontend_ready",
            "central_writeback": "no", "human_decision": "", "human_reviewer": "",
            "review_date": "", "review_note": "",
        })
    return rows


def build_resource_anchor_crosswalk() -> list[dict[str, str]]:
    raw = [
        ("W2C-A020", "W2C2-SR040", "USD 276,345.50", "Earthjustice filing amount; tax-period semantics"),
        ("W2C-A021", "W2C2-SR041;W2C2-SR042", "USD 280,000.00", "Treasury payment; 2021-03-05"),
        ("W2C-A022", "W2C2-SR040;W2C2-SR041;W2C2-SR042", "USD 3,654.50", "Unreconciled arithmetic difference; no mechanism assigned"),
        ("W2C-A030", "W2C2-SR043;W2C2-SR044;W2C2-SR045", "about JPY 930bn", "Official rough project estimate, not expenditure"),
        ("W2C-A041", "W2C2-SR045", "about JPY 648.3bn", "Reporter premise only; underlying official spending table not closed"),
        ("W2C-A042;W2C-A043", "W2C2-SR046", "FY2024 JPY 161.4bn contract basis / 72.6bn budget basis", "Annual bases are not additive streams or cumulative outturn"),
        ("W2C-A044;W2C-A045", "W2C2-SR047", "FY2025 JPY 200.6bn contract basis / 72.5bn budget basis", "Annual bases are not additive streams or cumulative outturn"),
    ]
    return [scoped({
        "crosswalk_id": f"W2C-RA{i:03d}", "w2_00_anchor_ids": anchors,
        "source_receipt_ids": receipts, "value_text": value, "preserved_semantics": semantics,
        "allowed_use": "system-scale or case-resource context only",
        "prohibited_inference": "Do not make an NGO-to-project influence ratio or close an unreconciled amount by assumption.",
    }) for i, (anchors, receipts, value, semantics) in enumerate(raw, start=1)]


def make_receipts(supports: Mapping[str, set[str]]) -> list[dict[str, str]]:
    source_log, manifest = source_maps()
    rows: list[dict[str, str]] = []
    for rid, sid, publisher, locator, notes in CENTRAL_RECEIPTS:
        src = source_log[sid]
        arc = manifest[sid]
        path = ROOT / arc["local_path"]
        rows.append({
            "receipt_id": rid, "publisher": publisher, "title": src["title"],
            "source_family": src["source_type"], "url": src["url"], "retrieved_at": RUN_DATE,
            "artifact_path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path),
            "mime_type": arc["content_type"], "exact_locator": locator,
            "supports_ids": ";".join(sorted(supports.get(rid, set()))), "archive_status": arc["archive_status"],
            "central_source_id": sid, "notes": notes,
        })
    for rid, publisher, title, family, url, name, mime, locator, notes in NEW_RECEIPTS:
        path = ARTIFACTS / name
        rows.append({
            "receipt_id": rid, "publisher": publisher, "title": title,
            "source_family": family, "url": url, "retrieved_at": RUN_DATE,
            "artifact_path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path),
            "mime_type": mime, "exact_locator": locator,
            "supports_ids": ";".join(sorted(supports.get(rid, set()))), "archive_status": "archived_local",
            "central_source_id": "", "notes": notes,
        })
    w2_receipts = {row["receipt_id"]: row for row in read_csv(W200 / "source_receipts_v1.csv")}
    for rid, old_id in W200_RECEIPTS:
        old = w2_receipts[old_id]
        rows.append({
            "receipt_id": rid, "publisher": old["publisher"], "title": old["title"],
            "source_family": old["source_family"], "url": old["url"], "retrieved_at": old["retrieved_at"],
            "artifact_path": old["artifact_path"], "sha256": old["sha256"], "mime_type": old["mime_type"],
            "exact_locator": old["exact_locator"], "supports_ids": ";".join(sorted(supports.get(rid, set()))),
            "archive_status": old["archive_status"], "central_source_id": "",
            "notes": f"Reused W2-00 receipt {old_id}; {old['notes']}",
        })
    return sorted(rows, key=lambda row: row["receipt_id"])


def collect_supports(tables: Iterable[tuple[Sequence[Mapping[str, str]], str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for rows, id_field in tables:
        for row in rows:
            for rid in row.get("source_receipt_ids", "").split(";"):
                if rid:
                    result[rid].add(row[id_field])
    return result


POS_FIELDS = ["sample_id", "selection_frame_id", "episode_id", "analysis_unit_ids", "short_label", "route_family", "place", "action_type", "intended_venue", "source_review_status", "entry_condition", "record_condition", "split_rule", "legacy_source_refs", "inclusion_status", "selection_bias", "package_scope", "frontend_status", "central_writeback", "review_status", "notes"]
NEG_FIELDS = ["negative_id", "selection_frame_id", "legacy_case_id", "short_label", "route_family", "place", "period", "action_type", "intended_venue", "gate_position", "entry_status", "record_status", "match_to_episode_ids", "matching_variables", "source_receipt_ids", "secondary_source_refs", "frame_fit", "inclusion_status", "authority_gap", "allowed_claim", "prohibited_inference", "package_scope", "frontend_status", "central_writeback", "review_status"]
PROJECT_FIELDS = ["project_change_id", "selection_frame_id", "project", "place", "period", "change_axes", "pre_state", "post_state", "decision_authority", "source_receipt_ids", "related_episode_ids", "civic_action_candidate", "temporal_order", "attribution_status", "attribution_evidence", "competing_explanation", "candidate_disposition", "allowed_claim", "prohibited_inference", "package_scope", "frontend_status", "central_writeback", "review_status"]
OUTCOME_FIELDS = ["outcome_id", "selection_frame_id", "episode_id", "analysis_unit_id", "short_label", "route_family", "place", "axis", "axis_status", "status_basis", "observation_unit", "source_receipt_ids", "legacy_source_refs", "exact_locator", "evidence_status", "attribution_status", "allowed_claim", "prohibited_inference", "selection_condition", "package_scope", "frontend_status", "central_writeback", "review_status", "notes"]
RECEIPT_FIELDS = ["receipt_id", "publisher", "title", "source_family", "url", "retrieved_at", "artifact_path", "sha256", "mime_type", "exact_locator", "supports_ids", "archive_status", "central_source_id", "notes"]
SEARCH_FIELDS = ["search_log_id", "search_stratum", "matched_episode_ids", "official_source_families_checked", "search_status", "result", "bounded_limit", "search_date", "searcher", "package_scope", "frontend_status", "central_writeback", "review_status", "notes"]
CAUSAL_FIELDS = ["causal_evidence_id", "project_change_id", "action_evidence", "decision_evidence", "time_order_evidence", "causal_statement_evidence", "source_receipt_ids", "attribution_status", "missing_causal_link", "principal_attention", "package_scope", "frontend_status", "central_writeback", "review_status", "notes"]
EXPLANATION_FIELDS = ["explanation_id", "explanation_family", "mechanism", "applies_to_units", "observable_discriminator", "current_status", "package_scope", "frontend_status", "central_writeback", "review_status", "notes"]
INCLUSION_FIELDS = ["log_id", "selection_frame_id", "unit_id", "unit_type", "decision", "inclusion_reason", "exclusion_reason", "matching_variables", "decision_date", "change_trigger", "package_scope", "frontend_status", "central_writeback", "review_status", "notes"]
REVIEW_FIELDS = ["review_item_id", "priority", "unit_ids", "review_question", "required_material", "current_gap", "allowed_decisions", "provisional_status", "central_writeback", "human_decision", "human_reviewer", "review_date", "review_note"]
ANCHOR_XW_FIELDS = ["crosswalk_id", "w2_00_anchor_ids", "source_receipt_ids", "value_text", "preserved_semantics", "allowed_use", "prohibited_inference", "package_scope", "frontend_status", "central_writeback", "review_status"]


def build_tables() -> dict[str, tuple[list[dict[str, str]], list[str]]]:
    te_rows = read_csv(TE_PATH)
    positive = build_positive_rows(te_rows)
    negative = build_negative_rows()
    projects = build_project_rows()
    outcomes = build_outcomes(te_rows)
    causal = build_causal_evidence(projects)
    inclusion = build_inclusion_log(positive, negative, projects)
    searches = build_negative_search_log()
    explanations = build_competing_explanations()
    review = build_review_queue()
    anchor_xw = build_resource_anchor_crosswalk()
    supports = collect_supports([
        (negative, "negative_id"), (projects, "project_change_id"),
        (outcomes, "outcome_id"), (causal, "causal_evidence_id"),
        (anchor_xw, "crosswalk_id"),
    ])
    receipts = make_receipts(supports)
    return {
        "positive_entry_sample_v1.csv": (positive, POS_FIELDS),
        "nonentry_negative_sample_v1.csv": (negative, NEG_FIELDS),
        "project_change_counterexample_sample_v1.csv": (projects, PROJECT_FIELDS),
        "accountability_outcome_ledger_v1.csv": (outcomes, OUTCOME_FIELDS),
        "source_receipts_v1.csv": (receipts, RECEIPT_FIELDS),
        "negative_search_log_v1.csv": (searches, SEARCH_FIELDS),
        "project_change_causal_evidence_v1.csv": (causal, CAUSAL_FIELDS),
        "competing_explanations_v1.csv": (explanations, EXPLANATION_FIELDS),
        "principal_review_queue_v1.csv": (review, REVIEW_FIELDS),
        "inclusion_exclusion_log_v1.csv": (inclusion, INCLUSION_FIELDS),
        "resource_anchor_crosswalk_v1.csv": (anchor_xw, ANCHOR_XW_FIELDS),
    }


def validate(tables: Mapping[str, tuple[list[dict[str, str]], list[str]]]) -> list[str]:
    checks: list[str] = []
    positive = tables["positive_entry_sample_v1.csv"][0]
    negative = tables["nonentry_negative_sample_v1.csv"][0]
    projects = tables["project_change_counterexample_sample_v1.csv"][0]
    outcomes = tables["accountability_outcome_ledger_v1.csv"][0]
    receipts = tables["source_receipts_v1.csv"][0]
    review = tables["principal_review_queue_v1.csv"][0]
    anchor_xw = tables["resource_anchor_crosswalk_v1.csv"][0]

    expected_episodes = {f"TE{i:02d}" for i in range(1, 14)}
    assert {row["episode_id"] for row in positive} == expected_episodes
    assert len(positive) == 13
    checks.append("PASS: fixed positive frame contains TE01-TE13 exactly once")
    assert len({row["analysis_unit_id"] for row in outcomes}) == 14
    assert {row["axis"] for row in outcomes} == set(AXES)
    assert len(outcomes) == 14 * len(AXES)
    checks.append("PASS: 13 episodes expand to 14 analysis units and 126 parallel-axis rows")
    assert len([row for row in outcomes if row["selection_condition"] == "yes"]) == 14 * 2
    checks.append("PASS: only ENTRY and RECORD are marked as selection conditions")
    assert any(row["analysis_unit_id"] == "TE06-W1" and row["axis"] == "PROJECT_AUTHORITY" and row["axis_status"] == "yes_bounded" for row in outcomes)
    assert any(row["analysis_unit_id"] == "TE06-W1" and row["axis"] == "PROJECT_BUDGET" and row["axis_status"] == "yes_bounded" for row in outcomes)
    checks.append("PASS: Awase first-wave budget/authority counterexample is explicit")
    assert any(row["negative_id"] == "W2C-NEG003" and row["inclusion_status"].startswith("excluded_from_strict") for row in negative)
    assert any(row["negative_id"] == "W2C-NEG006" and row["frame_fit"] == "strict_matched_judicial_gate" for row in negative)
    checks.append("PASS: non-entry frame separates entered relief controls from matched formal gates")
    assert all(row["attribution_status"] for row in projects)
    assert any(row["project_change_id"] == "W2C-PC002" and row["attribution_status"] == "chronology_not_causal" for row in projects)
    checks.append("PASS: every project-change row carries independent attribution coding")

    receipt_ids = {row["receipt_id"] for row in receipts}
    used: dict[str, set[str]] = defaultdict(set)
    for filename, id_field in [
        ("nonentry_negative_sample_v1.csv", "negative_id"),
        ("project_change_counterexample_sample_v1.csv", "project_change_id"),
        ("accountability_outcome_ledger_v1.csv", "outcome_id"),
        ("project_change_causal_evidence_v1.csv", "causal_evidence_id"),
        ("resource_anchor_crosswalk_v1.csv", "crosswalk_id"),
    ]:
        for row in tables[filename][0]:
            for rid in row.get("source_receipt_ids", "").split(";"):
                if rid:
                    assert rid in receipt_ids, (filename, row[id_field], rid)
                    used[rid].add(row[id_field])
    for receipt in receipts:
        path = ROOT / receipt["artifact_path"]
        assert path.is_file(), path
        assert sha256(path) == receipt["sha256"], receipt["receipt_id"]
        assert set(filter(None, receipt["supports_ids"].split(";"))) == used.get(receipt["receipt_id"], set())
    checks.append("PASS: receipt artifacts/hashes exist and every row↔receipt crosswalk closes bidirectionally")

    assert all(
        row["review_status"] == "ai_seeded"
        for name, (rows, _) in tables.items()
        if name not in {"principal_review_queue_v1.csv", "source_receipts_v1.csv"}
        for row in rows
    )
    assert all(row.get("package_scope") == "research_only" and row.get("frontend_status") == "not_frontend_ready" and row.get("central_writeback") == "no" for name, (rows, _) in tables.items() if name not in {"source_receipts_v1.csv", "principal_review_queue_v1.csv"} for row in rows)
    assert all(not row["human_decision"] and not row["human_reviewer"] and not row["review_date"] for row in review)
    checks.append("PASS: research-only gates and blank principal decisions are preserved")

    xw = {row["w2_00_anchor_ids"]: row for row in anchor_xw}
    assert xw["W2C-A020"]["value_text"] == "USD 276,345.50"
    assert xw["W2C-A021"]["value_text"] == "USD 280,000.00"
    assert xw["W2C-A022"]["value_text"] == "USD 3,654.50"
    assert "Reporter premise only" in xw["W2C-A041"]["preserved_semantics"]
    checks.append("PASS: Earthjustice/Treasury difference and JPY 648.3bn reporter-premise semantics remain unclosed")
    assert not any("success rate" in row["allowed_claim"].lower() for row in outcomes)
    checks.append("PASS: no success rate or chronology-only civic attribution is generated")
    return checks


def readme(tables: Mapping[str, tuple[list[dict[str, str]], list[str]]]) -> str:
    positive = tables["positive_entry_sample_v1.csv"][0]
    negative = tables["nonentry_negative_sample_v1.csv"][0]
    projects = tables["project_change_counterexample_sample_v1.csv"][0]
    outcomes = tables["accountability_outcome_ledger_v1.csv"][0]
    receipts = tables["source_receipts_v1.csv"][0]
    return f"""# W2-C 问责结果、负案例与项目改变反例 v1

日期：{RUN_DATE}

状态：`research_only` / `not_frontend_ready` / `central_writeback=no` / `review_status=ai_seeded`。

## 结论先行

原先“制度只能记录、认定、补偿，不能进一步改变项目”的**笼统结果上限判断被削弱**。

原因不是出现了基地取消或迁移，而是泡濑第一波公金诉讼提供了一个明确、可执行、可归因的反例：那霸地裁禁止县与市继续作未来公金支出、签订合同或负担新义务（已经发生的支付义务除外）。因此它同时落在 `PROJECT_BUDGET=yes_bounded` 与 `PROJECT_AUTHORITY=yes_bounded`。

目前仍可保留的窄结论是：在这组选择性案例中，民间行动较稳定地留下制度入口与正式记录，部分案件获得过去损害赔偿或程序性产出；除泡濑第一波的有界财政／权限限制外，尚无经负责人复核的案例证明民间行动造成了军事设施／部署的持久取消、迁移或核心运行改变。观察到的其他项目变化，多数有技术、行政审查、地方政府协商或政府间争议等竞争解释。

这不是成功率，也不是冲绳全部民间行动的总体结论。13 个正向 episode 本来就是按可观察入口／记录选出的。

## 三组样本

- 正向入口框：{len(positive)} 个 source episode；泡濑拆为两波，共 14 个分析单元。
- 匹配闸门框：{len(negative)} 行；其中包含严格匹配闸门、有界未决、回应追踪控制，以及 1 个明确排除出严格“未入场”框但保留作司法救济控制的案件。
- 项目改变／反例框：{len(projects)} 行，逐项分开事实改变与 civic attribution。
- 并列结果账本：{len(outcomes)} 行（14 分析单元 × 9 轴）。
- 来源收据：{len(receipts)} 条；每个在表中使用的 receipt 均有本地文件、SHA-256 和双向 row↔receipt crosswalk。

## 这轮最重要的校正

1. `ENTRY` 与 `RECORD` 是正向框的入选条件，不是发现，不能拿 13/13 算成功率。
2. TE05 不是简单的“进入”：请求进入议会、诉讼进入法院，但目标公投被正式闸门挡住。
3. TE06 必须分 `TE06-W1` 与 `TE06-W2`；两波结果相反。
4. TE12 的罢工真实发生并影响民用物流，但美国海军官方记录确认军舰访问仍完成；不能把物流扰动写成军事访问被阻止。
5. 泡濑面积由约 185ha 缩为约 95ha 是项目改变，但市方审查／修订在判决前已启动；不能从前后顺序推断诉讼造成缩减。
6. Henoko 约 JPY 930bn 是 2019 年官方粗略总成本估计；JPY 648.3bn 仍只是 2025 记者提问中的累计支出前提，未由底层官方支出表闭合。
7. Earthjustice 申报 USD 276,345.50，Treasury 付款记录 USD 280,000；差额 USD 3,654.50 保留为 `unreconciled difference`，不猜解释。

## 文件

- `positive_entry_sample_v1.csv`：固定 13 episode 与 14 分析单元。
- `nonentry_negative_sample_v1.csv`：按闸门位置重分的负／控制案例。
- `project_change_counterexample_sample_v1.csv`：项目改变与独立 attribution。
- `accountability_outcome_ledger_v1.csv`：9 个并列结果轴。
- `source_receipts_v1.csv`：来源、locator、本地路径、哈希与反向支持行。
- `negative_search_log_v1.csv`：每条 route family 的有界检索结果。
- `project_change_causal_evidence_v1.csv`：行动、决定、时间顺序、因果陈述四项证据。
- `competing_explanations_v1.csv`：竞争解释。
- `principal_review_queue_v1.csv`：负责人需要判断的高影响项目，决定栏全部留白。
- `inclusion_exclusion_log_v1.csv`：三组样本的冻结纳入／排除记录。
- `resource_anchor_crosswalk_v1.csv`：W2-00 金额与预算口径原样保留。
- `artifacts/`：本轮新增或重新冻结的官方原件。

## 复现与验证

```powershell
python scripts\\make_us_presence_network_wave2_w2_c_v1.py
python scripts\\make_us_presence_network_wave2_w2_c_v1.py --check
python -m unittest tests.test_make_us_presence_network_wave2_w2_c_v1
```

本包不修改中央事实、publication adapter、前端或控制文档。负责人复核前，任何结论都不得提升为正式 publication claim。
"""


def validation_report(checks: Sequence[str], tables: Mapping[str, tuple[list[dict[str, str]], list[str]]]) -> str:
    return "\n".join([
        "# W2-C validation report v1", "", f"Date: {RUN_DATE}", "", "Overall: **PASS**", "",
        *[f"- {check}" for check in checks], "",
        f"- positive episodes: {len(tables['positive_entry_sample_v1.csv'][0])}",
        f"- analysis units: {len({r['analysis_unit_id'] for r in tables['accountability_outcome_ledger_v1.csv'][0]})}",
        f"- outcome rows: {len(tables['accountability_outcome_ledger_v1.csv'][0])}",
        f"- matched gate/control rows: {len(tables['nonentry_negative_sample_v1.csv'][0])}",
        f"- project-change rows: {len(tables['project_change_counterexample_sample_v1.csv'][0])}",
        f"- source receipts: {len(tables['source_receipts_v1.csv'][0])}", "",
        "No central, publication-adapter, frontend or control-document write occurred.", "",
    ])


def payloads() -> dict[str, str]:
    tables = build_tables()
    checks = validate(tables)
    result = {name: csv_text(rows, fields) for name, (rows, fields) in tables.items()}
    result["README.md"] = readme(tables)
    result["validation_report_v1.md"] = validation_report(checks, tables)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = payloads()
    if args.check:
        mismatches = []
        for name, text in expected.items():
            path = OUT / name
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                mismatches.append(name)
        if mismatches:
            print("FAIL stale/missing outputs: " + ", ".join(mismatches), file=sys.stderr)
            return 1
        print("PASS us_presence_network_wave2_w2_c_v1")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in expected.items():
        (OUT / name).write_text(text, encoding="utf-8", newline="")
    print("BUILT us_presence_network_wave2_w2_c_v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
