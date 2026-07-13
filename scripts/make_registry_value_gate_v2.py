from __future__ import annotations

import csv
import hashlib
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "registry_value_gate_v2"
INTERIM = ROOT / "data" / "interim" / "34_registry_value_candidates_v2.csv"
REGISTRY = ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv"
SOURCE_LOG = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"

DATE = "2026-07-13"
HUMAN_REVIEW_FIELDS = ("decision", "reviewer", "review_date", "review_note")
NW2H_MARKER = "NW2-H controlled source integration 2026-07-13"
SOURCE_SNAPSHOT_MIN = 1
SOURCE_SNAPSHOT_MAX = 294
SOURCE_SNAPSHOT_LABEL = (
    "S001–S294 build-time candidate-source integration snapshot (2026-07-13)"
)


CANDIDATE_FIELDS = [
    "candidate_id",
    "candidate_name",
    "target_gap",
    "proposed_actor_class",
    "proposed_origin_type",
    "proposed_legal_status",
    "proposed_primary_places",
    "proposed_issue_tags",
    "formal_identity_gate",
    "formal_identity_evidence",
    "continuity_gate",
    "continuity_evidence",
    "direct_phase1_connection_gate",
    "direct_phase1_connection_evidence",
    "module_repair_value_gate",
    "module_repair_value",
    "one_off_signatory_guard",
    "duplicate_risk",
    "alias_duplicate_refs",
    "source_proposal_refs",
    "machine_recommendation",
    "readiness_rank",
    "machine_count_ready",
    "hr_route",
    "proposed_evidence_level",
    "boundary_note",
]


CANDIDATES = [
    {
        "candidate_id": "RV2C001",
        "candidate_name": "宮古島地下水研究会",
        "target_gap": "Miyako/Sakishima groundwater-health-deployment interface",
        "proposed_actor_class": "local_civic_research_and_advocacy_group",
        "proposed_origin_type": "okinawa_local",
        "proposed_legal_status": "informal_research_association",
        "proposed_primary_places": "Miyakojima",
        "proposed_issue_tags": "groundwater;health_risk;life_safety;environment;administrative_collaboration",
        "formal_identity_gate": "pass",
        "formal_identity_evidence": "Official profile dated 2018-03-31 gives the exact name, founding purpose, rules, named co-representatives and a Miyakojima secretariat; the city later addresses the group by the same exact name.",
        "continuity_gate": "pass",
        "continuity_evidence": "The official activity archive spans 2018-2025; a 2020 local-news record, a 2023 city response and 2024-2025 petitions show repeated public operation. Representative names change over time and should be treated as a leadership timeline, not an identity contradiction.",
        "direct_phase1_connection_gate": "pass",
        "direct_phase1_connection_evidence": "The group explicitly identifies Self-Defense Force facility wastewater as a groundwater-risk category and proposed ordinance/monitoring coverage for such facilities. This supports an advocacy and administrative-interface role, not proof that contamination occurred.",
        "module_repair_value_gate": "pass",
        "module_repair_value": "Repairs R1/R2 groundwater and health thin layers and gives R3/R4 a sustained Miyako organization connecting hydrogeology, life safety, monitoring and municipal procedure.",
        "one_off_signatory_guard": "pass: own rules/profile, multi-year reports, research outputs and repeated petitions; not a one-off event name or signatory",
        "duplicate_risk": "medium: adjacent names C015/A012 and thematic overlap with A097, but exact identity is distinct",
        "alias_duplicate_refs": "RV2X001;RV2X002;RV2X003",
        "source_proposal_refs": "RV2SP001;RV2SP002;RV2SP003;RV2SP004;RV2SP005;RV2SP006",
        "machine_recommendation": "ready_for_human_decision",
        "readiness_rank": "1",
        "machine_count_ready": "yes_pending_human",
        "hr_route": "HR-027",
        "proposed_evidence_level": "E4 identity/continuity; E3 issue-position boundary",
        "boundary_note": "Do not merge with C015, A012 or A097. Do not convert the group's stated wastewater risk into a finding of actual SDF-caused contamination. Human review should freeze the representative timeline and decide the narrow issue scope.",
    },
    {
        "candidate_id": "RV2C002",
        "candidate_name": "宜野湾ちゅら水会",
        "target_gap": "PFAS/public-health/base-adjacent field investigation",
        "proposed_actor_class": "local_civic_health_environment_group",
        "proposed_origin_type": "okinawa_local",
        "proposed_legal_status": "informal_civic_group",
        "proposed_primary_places": "Ginowan;Futenma",
        "proposed_issue_tags": "PFAS;health_risk;groundwater;life_safety;base_environment;human_rights",
        "formal_identity_gate": "pass",
        "formal_identity_evidence": "Ginowan City Council committee records name the group, its two co-representatives and a spokesperson; city and national news repeatedly use the same exact organization name.",
        "continuity_gate": "pass",
        "continuity_evidence": "Observable public requests, commissioned sampling, council testimony, administrative-procedure use and current testing span 2021-2026; testimony says the group had worked on the water issue since the 2016 PFOS disclosure without establishing a precise formation date.",
        "direct_phase1_connection_gate": "pass",
        "direct_phase1_connection_evidence": "The group commissioned PFAS soil testing beside Futenma, requested blood/health investigation and base access, and used a pollution-mediation route. These are source-backed public roles; health causation and pollution-source attribution remain outside this gate.",
        "module_repair_value_gate": "pass",
        "module_repair_value": "Adds a hyperlocal PFAS actor whose mechanism is resident-funded sampling plus municipal/procedural requests, complementing rather than duplicating A099's prefecture-wide coordination layer.",
        "one_off_signatory_guard": "pass: named leaders and secretary, repeated requests and investigations across at least five years; not inferred from a joint statement",
        "duplicate_risk": "low-medium: short name ちゅら水会; must remain distinct from A099",
        "alias_duplicate_refs": "RV2X004;RV2X005",
        "source_proposal_refs": "RV2SP007;RV2SP008;RV2SP009;RV2SP010;RV2SP011;RV2SP012;RV2SP013",
        "machine_recommendation": "ready_for_human_decision",
        "readiness_rank": "2",
        "machine_count_ready": "yes_pending_human",
        "hr_route": "HR-027",
        "proposed_evidence_level": "E4 identity/procedure; E3 attributed issue role",
        "boundary_note": "A099 and this group are separately named in the same 2026 exchange record; do not merge or infer an alliance. Record sampling/request roles without asserting epidemiological effects or a proven military source beyond each source's wording.",
    },
    {
        "candidate_id": "RV2C004",
        "candidate_name": "全日本港湾労働組合沖縄地方本部",
        "target_gap": "labor/port-workplace channel and Sakishima port militarization",
        "proposed_actor_class": "labor_union_regional_branch",
        "proposed_origin_type": "okinawa_local",
        "proposed_legal_status": "labor_union_regional_headquarters",
        "proposed_primary_places": "Okinawa;Naha Port;Ishigaki Port;Henoko",
        "proposed_issue_tags": "labor;life_safety;peace;anti_base;Henoko;frontline_prevention",
        "formal_identity_gate": "pass",
        "formal_identity_evidence": "A Central Labour Relations Commission order formally names the Okinawa headquarters as a union party; prefectural strike-notice records repeatedly use the same exact name.",
        "continuity_gate": "pass",
        "continuity_evidence": "Official labor records document the Okinawa headquarters in 2014 and repeated strike notices from 2020 through 2026; an official union document records a 2025 Okinawa peace-march activity.",
        "direct_phase1_connection_gate": "pass",
        "direct_phase1_connection_evidence": "The headquarters held a 2015 anti-Henoko/security-law workplace action and in 2024 used a port strike around a U.S. destroyer call at Ishigaki, framing worker safety and civilian-port military use.",
        "module_repair_value_gate": "pass",
        "module_repair_value": "Repairs the labor thin layer while adding a distinct R5/R7 mechanism: workplace/strike capacity shifts base and frontline disputes into port and occupational-safety venues, including Sakishima.",
        "one_off_signatory_guard": "pass: formal union identity plus decade-spanning official records and multiple independently reported actions",
        "duplicate_risk": "low: abbreviated forms; distinct from A089-A093 labor organizations",
        "alias_duplicate_refs": "RV2X008;RV2X009;RV2X010",
        "source_proposal_refs": "RV2SP019;RV2SP020;RV2SP021;RV2SP022;RV2SP023;RV2SP024",
        "machine_recommendation": "ready_for_human_decision",
        "readiness_rank": "3",
        "machine_count_ready": "yes_pending_human",
        "hr_route": "HR-027",
        "proposed_evidence_level": "E4 identity/continuity; E3-E4 dated action role",
        "boundary_note": "Do not infer a stable alliance from common marches or statements. The 2024 strike's existence and stated rationale can be recorded; its legal status, public effects and political efficacy are not adjudicated here.",
    },
    {
        "candidate_id": "RV2C003",
        "candidate_name": "新日本婦人の会沖縄県本部",
        "target_gap": "women/human-rights/peace local organizational layer",
        "proposed_actor_class": "womens_or_human_rights_ngo_regional_branch",
        "proposed_origin_type": "okinawa_local",
        "proposed_legal_status": "prefectural_headquarters_of_national_association",
        "proposed_primary_places": "Okinawa",
        "proposed_issue_tags": "women;human_rights;peace;anti_base;referendum",
        "formal_identity_gate": "pass",
        "formal_identity_evidence": "The national association's official structure covers prefectural headquarters; official central statements and an Okinawa Prefecture administrative record explicitly name the Okinawa prefectural headquarters and its chair.",
        "continuity_gate": "pass",
        "continuity_evidence": "Okinawa Prefecture records a branch request in 2008; official association records show Okinawa-headquarters action in 2014 and a jointly signed branch request in 2024.",
        "direct_phase1_connection_gate": "pass",
        "direct_phase1_connection_evidence": "Dated local actions include requests over U.S.-military sexual violence, anti-new-base activity and a 2018 Henoko referendum-signature campaign.",
        "module_repair_value_gate": "pass",
        "module_repair_value": "Adds a sustained prefectural women-organizing channel linking military violence, human rights, peace and local referendum work; it is analytically distinct from A049, A107 and A111.",
        "one_off_signatory_guard": "pass: formal prefectural unit with public actions documented across 2008-2024; not inferred from one statement",
        "duplicate_risk": "medium: local branch of a national association and ambiguous short form 新婦人",
        "alias_duplicate_refs": "RV2X006;RV2X007",
        "source_proposal_refs": "RV2SP014;RV2SP015;RV2SP016;RV2SP017;RV2SP018",
        "machine_recommendation": "ready_for_human_decision",
        "readiness_rank": "4",
        "machine_count_ready": "yes_pending_human",
        "hr_route": "HR-027",
        "proposed_evidence_level": "E4 identity/continuity; E3-E4 dated action role",
        "boundary_note": "Human review must decide branch-level actor treatment. Do not transfer every national action to the Okinawa headquarters, and do not code party affiliation from coverage by a party newspaper.",
    },
    {
        "candidate_id": "RV2C005",
        "candidate_name": "八重山大地会",
        "target_gap": "Ishigaki local culture/war-memory opposition layer",
        "proposed_actor_class": "local_civic_group",
        "proposed_origin_type": "okinawa_local",
        "proposed_legal_status": "informal_association",
        "proposed_primary_places": "Ishigaki;Yaeyama",
        "proposed_issue_tags": "anti_military;peace;war_memory;life_safety;local_autonomy",
        "formal_identity_gate": "pass",
        "formal_identity_evidence": "Local coverage names the exact group and representative; independent event records name it as an organizer. A local chronology reports a 2015 formation.",
        "continuity_gate": "partial",
        "continuity_evidence": "Publicly indexed organization-level evidence closes a 2015-2017 activity window, but no reliable 2018-2026 continuity, dissolution or successor record was found in this online pass.",
        "direct_phase1_connection_gate": "pass",
        "direct_phase1_connection_evidence": "The group organized or co-organized Ishigaki meetings opposing SDF missile-base deployment and publicly linked the issue to war experience and local life.",
        "module_repair_value_gate": "pass",
        "module_repair_value": "Would add a culturally framed Ishigaki actor and a component-level view beneath A010, but only if organizational continuity or a bounded historical-actor policy is confirmed.",
        "one_off_signatory_guard": "pass: multiple organizer/representative observations across 2015-2017; still insufficient for current continuity",
        "duplicate_risk": "high: variant spellings and reported component relation to A010's wider coalition",
        "alias_duplicate_refs": "RV2X011;RV2X012",
        "source_proposal_refs": "RV2SP025;RV2SP026;RV2SP027;RV2SP028;RV2SP029",
        "machine_recommendation": "defer_online_continuity_gap",
        "readiness_rank": "5",
        "machine_count_ready": "no",
        "hr_route": "none_until_continuity_or_historical_scope_closes",
        "proposed_evidence_level": "E3 bounded 2015-2017 identity/action",
        "boundary_note": "Do not count as a current registry actor, merge it into A010, or treat coalition-component evidence as a stable alliance. A fresh organization-level source or an explicit historical-actor decision is needed before HR-027 routing.",
    },
]


SOURCE_FIELDS = [
    "proposal_id",
    "candidate_id",
    "title",
    "url",
    "publisher",
    "source_type",
    "publication_or_record_date",
    "locator",
    "support_scope",
    "suggested_evidence_level",
    "source_log_match",
    "relation_or_claim_approved",
    "caveat",
]

PROVENANCE_FIELDS = [
    "proposal_id",
    "candidate_id",
    "normalized_url",
    "historical_source_log_match",
    "snapshot_scope",
    "snapshot_source_id",
    "snapshot_source_state",
    "snapshot_source_review_status",
    "relation_or_claim_approved",
]


def source(
    proposal_id: str,
    candidate_id: str,
    title: str,
    url: str,
    publisher: str,
    source_type: str,
    publication_or_record_date: str,
    locator: str,
    support_scope: str,
    suggested_evidence_level: str,
    source_log_match: str = "",
    caveat: str = "",
) -> dict[str, str]:
    return {
        "proposal_id": proposal_id,
        "candidate_id": candidate_id,
        "title": title,
        "url": url,
        "publisher": publisher,
        "source_type": source_type,
        "publication_or_record_date": publication_or_record_date,
        "locator": locator,
        "support_scope": support_scope,
        "suggested_evidence_level": suggested_evidence_level,
        "source_log_match": source_log_match,
        "relation_or_claim_approved": "no",
        "caveat": caveat,
    }


SOURCES = [
    source(
        "RV2SP001",
        "RV2C001",
        "宮古島地下水研究会・研究会について",
        "https://miyakojima-tikasui.com/about_us.html",
        "宮古島地下水研究会",
        "organization_website",
        "2018-03-31 profile; accessed 2026-07-13",
        "設立趣旨; lines/paragraphs naming 2018 co-representatives, rules and secretariat",
        "Exact identity, founding purpose, formal rules, named leadership and local secretariat",
        "E4",
        "S158",
        "The profile's 2018 representatives are a dated leadership observation, not a permanent roster.",
    ),
    source(
        "RV2SP002",
        "RV2C001",
        "宮古島地下水研究会 公式サイト",
        "https://miyakojima-tikasui.com/",
        "宮古島地下水研究会",
        "organization_website",
        "2019-2025 activity archive; accessed 2026-07-13",
        "top page activity, report and news indexes",
        "Current operation and repeated research, petition and public-learning outputs",
        "E4",
        "S204",
        "Self-published continuity evidence; individual scientific claims require claim-level review.",
    ),
    source(
        "RV2SP003",
        "RV2C001",
        "地下水の危機とは？",
        "https://miyakojima-tikasui.com/crisis.html",
        "宮古島地下水研究会",
        "organization_issue_page",
        "current page; accessed 2026-07-13",
        "自衛隊施設の排水 section",
        "The group's explicit framing of SDF-facility water use/wastewater as a groundwater-risk category",
        "E3",
        "",
        "Supports the group's public position, not a finding that contamination or a health effect occurred.",
    ),
    source(
        "RV2SP004",
        "RV2C001",
        "水道水源保全区域を宮古島市全域に拡大する理由",
        "https://miyakojima-tikasui.com/report_activity/2021-10-08-04.pdf",
        "宮古島地下水研究会",
        "organization_policy_document",
        "2021-10-08",
        "p.1, items 1 and 3-5",
        "A dated ordinance/monitoring proposal explicitly covering SDF-facility wastewater risks",
        "E3",
        "",
        "Policy advocacy evidence; it does not independently verify the asserted environmental risk level.",
    ),
    source(
        "RV2SP005",
        "RV2C001",
        "宮古島地下水研究会の見解に対する回答書",
        "https://www.city.miyakojima.lg.jp/kurashi/seikatsu/kankyohozen/files/tikasui.pdf",
        "宮古島市",
        "municipal_official_response",
        "2023-02",
        "title and response sections",
        "Independent municipal recognition of the group as a repeated administrative interlocutor",
        "E4",
        "",
        "Supports identity and recipient-side procedure, not agreement with the group's scientific interpretation.",
    ),
    source(
        "RV2SP006",
        "RV2C001",
        "宮古島の地下水施策 市長選立候補予定者の回答公表",
        "https://ryukyushimpo.jp/news/entry-1254033.html",
        "琉球新報",
        "local_news",
        "2020-12-27",
        "lead naming three co-representatives and three-question questionnaire",
        "Independent 2020 identity, leadership and local-policy intervention",
        "E3",
        "",
        "An election questionnaire is a dated public intervention, not proof of later policy effect.",
    ),
    source(
        "RV2SP007",
        "RV2C002",
        "宜野湾市議会 福祉教育常任委員会審査記録（請願第1号）",
        "https://www.city.ginowan.lg.jp/material/files/group/61/hukusi_202212.pdf",
        "宜野湾市議会",
        "municipal_legislative_record",
        "2022-12 hearings; report dated 2023-08-31",
        "pp.5-8, especially testimony naming 町田直美・仲松典子 and activity history",
        "Exact identity, named co-representatives, PFAS work history and health-investigation request",
        "E4",
        "",
        "The testimony says work began with the 2016 PFOS disclosure; it does not give a precise legal formation date.",
    ),
    source(
        "RV2SP008",
        "RV2C002",
        "有機フッ素化合物PFOS及びPFOA汚染の対策を求める意見書",
        "https://www.city.ginowan.lg.jp/material/files/group/61/ikensyo1.pdf",
        "宜野湾市議会",
        "municipal_resolution",
        "2022-11-25",
        "full one-page resolution",
        "Official recognition of the group's sampling and its consequence for a municipal opinion",
        "E4",
        "",
        "The resolution uses probability language for a base source; do not strengthen it to established causation.",
    ),
    source(
        "RV2SP009",
        "RV2C002",
        "学校敷地から化学物質PFOS 沖縄米軍基地に隣接",
        "https://www.asahi.com/articles/ASQ9S5J0LQ96TPOB004.html",
        "朝日新聞",
        "national_news",
        "2022-09-25",
        "paragraphs describing fundraising, commissioned sampling and published results",
        "Independent direct-role evidence for resident-funded field sampling",
        "E3",
        "",
        "Paywalled after the visible evidence; preserve the visible locator and do not infer beyond it.",
    ),
    source(
        "RV2SP010",
        "RV2C002",
        "米軍PFAS汚染で血液検査を要請 宜野湾ちゅら水会",
        "https://ryukyushimpo.jp/news/entry-1421139.html",
        "琉球新報",
        "local_news",
        "2021-11-09",
        "lead naming 仲松典子共同代表 and city request",
        "2021 organization identity and request for disclosure/health investigation",
        "E3",
        "",
        "A request does not establish that the requested blood testing was performed.",
    ),
    source(
        "RV2SP011",
        "RV2C002",
        "PFAS汚染 米軍との意見交換に市民の参加を",
        "https://ryukyushimpo.jp/news/entry-1730706.html",
        "琉球新報",
        "local_news",
        "2023-06-17",
        "lead and image caption naming 町田直美共同代表",
        "2023 continuity and request for citizen participation in a city-base meeting",
        "E3",
        "",
        "Documents a request, not its acceptance or an institutional partnership.",
    ),
    source(
        "RV2SP012",
        "RV2C002",
        "泡が消えた後に残った白い粉からPFAS検出",
        "https://newsdig.tbs.co.jp/articles/-/2642471?display=1",
        "琉球放送／TBS NEWS DIG",
        "broadcast_news",
        "2026-05-05",
        "paragraph naming 照屋正史事務局長 and commissioned expert analysis",
        "Current 2026 identity/continuity and a bounded sampling role",
        "E3",
        "",
        "The expert explicitly says the sample cannot be converted to foam volume or sewer concentration.",
    ),
    source(
        "RV2SP013",
        "RV2C002",
        "沖縄の米軍基地PFAS汚染 全国交流集会",
        "https://www.jcp.or.jp/akahata/aik25/2026-02-16/2026021611_01_0.php",
        "しんぶん赤旗",
        "party_news",
        "2026-02-16",
        "paragraph separately naming A099 and 宜野湾ちゅら水会",
        "Name-level evidence that the two PFAS groups were treated as separate organizations in one event",
        "E3",
        "",
        "Use only for identity separation and attributed participation; co-participation is not an alliance.",
    ),
    source(
        "RV2SP014",
        "RV2C003",
        "新婦人の紹介",
        "https://www.shinfujin.gr.jp/about/organization/",
        "新日本婦人の会中央本部",
        "organization_website",
        "current page; accessed 2026-07-13",
        "name, purposes, 1962 formation and nationwide structure",
        "National association identity and prefectural-headquarters organizational structure",
        "E4",
        "",
        "National identity alone does not transfer every national action to the Okinawa headquarters.",
    ),
    source(
        "RV2SP015",
        "RV2C003",
        "沖縄県知事選で圧勝の民意に応え ただちに新基地建設中止を",
        "https://www.shinfujin.gr.jp/2943/",
        "新日本婦人の会中央本部",
        "organization_statement",
        "2014-11-19",
        "paragraph explicitly describing Okinawa-headquarters member action",
        "Official national-body attribution of dated Okinawa-headquarters anti-new-base activity",
        "E4",
        "",
        "Supports the branch's attributed activity; election commentary must not become a causal claim.",
    ),
    source(
        "RV2SP016",
        "RV2C003",
        "沖縄米兵少女暴行事件とその隠蔽につよく抗議し根本的対策を求める要請",
        "https://www.shinfujin.gr.jp/wp-content/uploads/2024/06/%E7%B1%B3%E5%85%B5%E5%B0%91%E5%A5%B3%E6%9A%B4%E8%A1%8C%E4%BA%8B%E4%BB%B6%E3%80%80%E5%86%85%E9%96%A3%E7%B7%8F%E7%90%86%E5%A4%A7%E8%87%A3%E5%B2%B8%E7%94%B0%E6%96%87%E9%9B%84%E6%A7%981.pdf",
        "新日本婦人の会中央本部・沖縄県本部",
        "organization_request",
        "2024-06-27",
        "signature block and request text",
        "Exact local-unit name, chair and direct military-violence/human-rights request role",
        "E4",
        "",
        "Joint signature with the central body proves a bounded request, not all-purpose identity equivalence.",
    ),
    source(
        "RV2SP017",
        "RV2C003",
        "沖縄県行政記録 平成20年",
        "https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/014/905/h20gyouseikiroku.pdf",
        "沖縄県",
        "prefectural_administrative_record",
        "2008",
        "p.4, 2008-02-14 entry",
        "Independent official record of an Okinawa-headquarters request over a U.S.-Marine sexual-assault case",
        "E4",
        "",
        "An administrative diary entry confirms a request, not the full content or outcome.",
    ),
    source(
        "RV2SP018",
        "RV2C003",
        "沖縄県民投票条例へ 新婦人が署名開始",
        "https://www.jcp.or.jp/akahata/aik18/2018-06-18/2018061801_03_1.html",
        "しんぶん赤旗",
        "party_news",
        "2018-06-18",
        "lead and chair quotation",
        "Okinawa-headquarters organization identity and Henoko referendum-signature campaign role",
        "E3",
        "",
        "Use for the dated public role only; do not code party affiliation or a stable alliance.",
    ),
    source(
        "RV2SP019",
        "RV2C004",
        "中央労働委員会命令書 沖縄セメント工業事件",
        "https://www.mhlw.go.jp/churoi/meirei_db/mei/pdf/m11367.pdf",
        "中央労働委員会／厚生労働省",
        "official_labor_decision",
        "2014-03-13",
        "pp.1-2, party identity",
        "Formal exact identity and regional-union party status",
        "E4",
        "",
        "Use for identity and legal procedure only; the merits are unrelated to Phase-1 issue coding.",
    ),
    source(
        "RV2SP020",
        "RV2C004",
        "争議行為の届出と予告",
        "https://www.pref.okinawa.lg.jp/shigoto/koyorodo/1012030/1012056.html",
        "沖縄県",
        "prefectural_labor_record",
        "2020-2026 records; accessed 2026-07-13",
        "沖縄県公表 list naming the headquarters repeatedly",
        "Current exact identity and repeated organizational operation through official notices",
        "E4",
        "",
        "Generic strike notices establish continuity, not Phase-1 political positions.",
    ),
    source(
        "RV2SP021",
        "RV2C004",
        "全港湾沖縄が安保法案反対訴え抗議集会",
        "https://ryukyushimpo.jp/news/prentry-249100.html",
        "琉球新報",
        "local_news",
        "2015-09-18",
        "lead naming the Okinawa headquarters and workplace action",
        "Direct anti-Henoko/security-law labor action and port-workplace framing",
        "E3",
        "",
        "Participant count is organizer-reported; the event does not establish alliance ties.",
    ),
    source(
        "RV2SP022",
        "RV2C004",
        "米海軍ミサイル駆逐艦ラファエル・ペラルタ寄港反対決議",
        "https://www.city.ishigaki.okinawa.jp/material/files/group/33/giin-2024-3.pdf",
        "石垣市議会",
        "municipal_resolution",
        "2024-03-04",
        "p.2, paragraph naming the union strike decision and worker-safety rationale",
        "Official recipient-side record of the union's Ishigaki/Naha port action plan and stated safety frame",
        "E4",
        "",
        "The resolution recounts the plan; it is not a union membership record or legal judgment.",
    ),
    source(
        "RV2SP023",
        "RV2C004",
        "第213回国会参議院特別委員会 第5号",
        "https://kokkai.ndl.go.jp/simple/detail?minId=121315359X00520240524",
        "国立国会図書館 国会会議録検索システム",
        "official_parliamentary_record",
        "2024-05-24",
        "statements 133-134",
        "Independent official acknowledgment that the Okinawa headquarters carried out the Ishigaki Port strike",
        "E4",
        "",
        "The record contains contested characterizations of legality; this gate records occurrence and attributed rationale only.",
    ),
    source(
        "RV2SP024",
        "RV2C004",
        "2025 5.15平和行進 全港湾沖縄地方本部報告",
        "https://www.zenkowan.org/wp-content/uploads/2025/06/%E6%B2%96%E7%B8%84%E5%9C%B0%E6%96%B9%E3%80%80%E6%AF%94%E5%98%89%E5%8B%81%E5%B8%8C.pdf",
        "全日本港湾労働組合",
        "union_activity_report",
        "2025-05-17 to 2025-05-18",
        "full one-page participant report",
        "Current branch-level peace-march and base-issue learning activity",
        "E3",
        "",
        "A participant report supports a bounded activity observation, not the position of every union member.",
    ),
    source(
        "RV2SP025",
        "RV2C005",
        "やいまタイム地域年表 2015年12月23日",
        "https://yaimatime.com/schedule/archive/2302/12/23/",
        "やいまタイム",
        "local_chronology",
        "2015-12-23 event entry; accessed 2026-07-13",
        "entry stating 八重山大地会 was formed to oppose SDF deployment through cultural activity",
        "A formation-date lead and issue purpose",
        "E2",
        "",
        "Archive URL metadata is unusual; verify the original local-newspaper record before freezing the formation date.",
    ),
    source(
        "RV2SP026",
        "RV2C005",
        "陸自配備反対を決議 石垣、住民180人が緊急集会",
        "https://ryukyushimpo.jp/news/entry-209354.html",
        "琉球新報",
        "local_news",
        "2016-01-24",
        "paragraph naming 八重山大地会 and 八重洋一郎代表",
        "Exact identity, representative and anti-deployment organizer role",
        "E3",
        "",
        "The wider meeting had multiple organizers; do not infer a stable alliance.",
    ),
    source(
        "RV2SP027",
        "RV2C005",
        "陸自配備で受け入れ表明 住民裏切りの石垣市長",
        "https://www.kinyobi.co.jp/kinyobinews/2017/01/25/%E9%99%B8%E8%87%AA%E9%85%8D%E5%82%99%E3%81%A7%E3%80%8C%E5%8F%97%E3%81%91%E5%85%A5%E3%82%8C%E3%80%8D%E8%A1%A8%E6%98%8E%E2%80%95%E2%80%95%E4%BD%8F%E6%B0%91%E8%A3%8F%E5%88%87%E3%82%8A%E3%81%AE%E7%9F%B3/",
        "週刊金曜日",
        "magazine_news",
        "2017-01-25",
        "paragraph naming 潮平正道共同代表",
        "2017 identity/leadership and war-memory framing of SDF deployment",
        "E3",
        "",
        "Attributed statement only; publisher has an advocacy position.",
    ),
    source(
        "RV2SP028",
        "RV2C005",
        "石垣島市政と陸自ミサイル部隊配備を語るバガケーラの集い",
        "https://iwj.co.jp/wj/open/archives/374937",
        "IWJ Independent Web Journal",
        "event_report",
        "2017-04-21",
        "event metadata naming 八重山大地会 as co-organizer",
        "A second 2017 organizer observation tied directly to SDF deployment",
        "E3",
        "",
        "Co-organization is event-level and does not establish a permanent alliance.",
    ),
    source(
        "RV2SP029",
        "RV2C005",
        "石垣島への陸上自衛隊配備をめぐる組織関係図",
        "https://researchmap.jp/teppy/presentations/10378736/attachment_file.pdf",
        "researchmap academic presentation attachment",
        "academic_presentation_material",
        "undated attachment; accessed 2026-07-13",
        "organization map listing やいま大地会 and A010's component composition",
        "Alias lead and possible component relation to A010",
        "E2",
        "",
        "Analytical diagram, not an official membership roster; the component relation needs human or primary confirmation.",
    ),
]


CROSSWALK_FIELDS = [
    "crosswalk_id",
    "candidate_id",
    "candidate_string",
    "normalized_string",
    "comparison_object_id",
    "comparison_name",
    "comparison_type",
    "machine_disposition",
    "evidence_basis",
    "source_proposal_refs",
    "human_check_needed",
    "boundary_note",
]


CROSSWALK = [
    {
        "crosswalk_id": "RV2X001",
        "candidate_id": "RV2C001",
        "candidate_string": "宮古島地下水研究会",
        "normalized_string": "宮古島地下水研究会",
        "comparison_object_id": "C015",
        "comparison_name": "宮古島・命の水・自衛隊配備について考える会",
        "comparison_type": "prior_deferred_candidate",
        "machine_disposition": "distinct_entity_do_not_merge",
        "evidence_basis": "Exact names and documented leaders differ; HR-011 already warned against merger.",
        "source_proposal_refs": "RV2SP001;RV2SP006",
        "human_check_needed": "yes",
        "boundary_note": "C015 remains under HR-011 and must not be resolved by absorbing it into this candidate.",
    },
    {
        "crosswalk_id": "RV2X002",
        "candidate_id": "RV2C001",
        "candidate_string": "宮古島地下水研究会",
        "normalized_string": "宮古島地下水研究会",
        "comparison_object_id": "A012",
        "comparison_name": "宮古島いのちの水を守ろう！",
        "comparison_type": "existing_actor",
        "machine_disposition": "unresolved_relation_not_alias",
        "evidence_basis": "The registry's A012 exact name and source history differ; no succession/identity record was found.",
        "source_proposal_refs": "RV2SP001;RV2SP002",
        "human_check_needed": "yes",
        "boundary_note": "Do not create an alias, successor or alliance relation without a source that addresses the relationship.",
    },
    {
        "crosswalk_id": "RV2X003",
        "candidate_id": "RV2C001",
        "candidate_string": "宮古島地下水研究会",
        "normalized_string": "宮古島地下水研究会",
        "comparison_object_id": "A097",
        "comparison_name": "宮古島環境クラブ",
        "comparison_type": "existing_actor",
        "machine_disposition": "distinct_entity_thematic_overlap",
        "evidence_basis": "Names and organizational descriptions are different; both address Miyako environment/groundwater issues.",
        "source_proposal_refs": "RV2SP001;RV2SP002",
        "human_check_needed": "no",
        "boundary_note": "Shared issue/place does not establish affiliation.",
    },
    {
        "crosswalk_id": "RV2X004",
        "candidate_id": "RV2C002",
        "candidate_string": "ちゅら水会",
        "normalized_string": "ちゅら水会",
        "comparison_object_id": "RV2C002",
        "comparison_name": "宜野湾ちゅら水会",
        "comparison_type": "short_name_candidate",
        "machine_disposition": "probable_alias_pending_human",
        "evidence_basis": "Local reporting repeatedly shortens the exact name to ちゅら水会 in the same article/context.",
        "source_proposal_refs": "RV2SP010;RV2SP011",
        "human_check_needed": "yes",
        "boundary_note": "The short form is not globally unique; retain the locality in canonical display.",
    },
    {
        "crosswalk_id": "RV2X005",
        "candidate_id": "RV2C002",
        "candidate_string": "宜野湾ちゅら水会",
        "normalized_string": "宜野湾ちゅら水会",
        "comparison_object_id": "A099",
        "comparison_name": "有機フッ素化合物（PFAS）汚染から市民の生命を守る連絡会",
        "comparison_type": "existing_actor",
        "machine_disposition": "separate_entities_same_field",
        "evidence_basis": "A 2026 exchange record names both groups separately; their geographic scale and public mechanisms also differ.",
        "source_proposal_refs": "RV2SP007;RV2SP013",
        "human_check_needed": "yes",
        "boundary_note": "Co-participation does not create an alliance or membership relation.",
    },
    {
        "crosswalk_id": "RV2X006",
        "candidate_id": "RV2C003",
        "candidate_string": "新婦人",
        "normalized_string": "新婦人",
        "comparison_object_id": "RV2C003",
        "comparison_name": "新日本婦人の会沖縄県本部",
        "comparison_type": "ambiguous_short_name",
        "machine_disposition": "do_not_add_unqualified_alias",
        "evidence_basis": "新婦人 is the national association's short name and can refer to the parent body, not only the Okinawa headquarters.",
        "source_proposal_refs": "RV2SP014;RV2SP018",
        "human_check_needed": "yes",
        "boundary_note": "Prefer 新婦人沖縄県本部 only if a source uses that exact branch-specific form.",
    },
    {
        "crosswalk_id": "RV2X007",
        "candidate_id": "RV2C003",
        "candidate_string": "新日本婦人の会沖縄県本部",
        "normalized_string": "新日本婦人の会沖縄県本部",
        "comparison_object_id": "A049;A105;A107;A111",
        "comparison_name": "existing women/YWCA actors",
        "comparison_type": "existing_actor_cluster",
        "machine_disposition": "distinct_entity_same_function_layer",
        "evidence_basis": "Exact names, governance and public records are distinct; the candidate is a prefectural unit of a separate national association.",
        "source_proposal_refs": "RV2SP014;RV2SP016;RV2SP017",
        "human_check_needed": "yes",
        "boundary_note": "Functional overlap in women/peace/human-rights work is analytically valuable and not a duplicate by itself.",
    },
    {
        "crosswalk_id": "RV2X008",
        "candidate_id": "RV2C004",
        "candidate_string": "全港湾沖縄地方本部",
        "normalized_string": "全港湾沖縄地方本部",
        "comparison_object_id": "RV2C004",
        "comparison_name": "全日本港湾労働組合沖縄地方本部",
        "comparison_type": "documented_abbreviation",
        "machine_disposition": "probable_alias_pending_human",
        "evidence_basis": "The national union's 2025 PDF uses the abbreviated branch name while official government records use the full name.",
        "source_proposal_refs": "RV2SP019;RV2SP024",
        "human_check_needed": "yes",
        "boundary_note": "Canonical should use the full official form.",
    },
    {
        "crosswalk_id": "RV2X009",
        "candidate_id": "RV2C004",
        "candidate_string": "全港湾沖縄",
        "normalized_string": "全港湾沖縄",
        "comparison_object_id": "RV2C004",
        "comparison_name": "全日本港湾労働組合沖縄地方本部",
        "comparison_type": "media_short_name",
        "machine_disposition": "probable_alias_pending_human",
        "evidence_basis": "Local-news headline and text use 全港湾沖縄 for the full organization.",
        "source_proposal_refs": "RV2SP021",
        "human_check_needed": "yes",
        "boundary_note": "Do not confuse the Okinawa branch with the national union.",
    },
    {
        "crosswalk_id": "RV2X010",
        "candidate_id": "RV2C004",
        "candidate_string": "全日本港湾労働組合沖縄地方本部",
        "normalized_string": "全日本港湾労働組合沖縄地方本部",
        "comparison_object_id": "A089;A090;A091;A092;A093",
        "comparison_name": "existing labor/education union actors",
        "comparison_type": "existing_actor_cluster",
        "machine_disposition": "distinct_union_same_layer",
        "evidence_basis": "Exact union identity and port-sector jurisdiction are distinct.",
        "source_proposal_refs": "RV2SP019;RV2SP020",
        "human_check_needed": "no",
        "boundary_note": "Common labor or peace events do not establish federation membership or alliance.",
    },
    {
        "crosswalk_id": "RV2X011",
        "candidate_id": "RV2C005",
        "candidate_string": "八重山大地（やいまうふづぃー）会;やいま大地会",
        "normalized_string": "八重山大地会;やいま大地会",
        "comparison_object_id": "RV2C005",
        "comparison_name": "八重山大地会",
        "comparison_type": "spelling_reading_variants",
        "machine_disposition": "alias_set_needs_primary_confirmation",
        "evidence_basis": "Local news gives 八重山大地（やいまうふづぃー）会; an analytical diagram gives やいま大地会.",
        "source_proposal_refs": "RV2SP026;RV2SP029",
        "human_check_needed": "yes",
        "boundary_note": "Do not freeze canonical spelling from the lower-grade diagram alone.",
    },
    {
        "crosswalk_id": "RV2X012",
        "candidate_id": "RV2C005",
        "candidate_string": "八重山大地会",
        "normalized_string": "八重山大地会",
        "comparison_object_id": "A010",
        "comparison_name": "石垣島に軍事基地をつくらせない市民連絡会",
        "comparison_type": "possible_coalition_component",
        "machine_disposition": "not_duplicate_component_relation_unfrozen",
        "evidence_basis": "An analytical organization map places やいま大地会 inside A010's wider composition; no official membership record was found.",
        "source_proposal_refs": "RV2SP026;RV2SP029",
        "human_check_needed": "yes",
        "boundary_note": "Do not merge the organizations or create a stable membership edge before primary/human confirmation.",
    },
]


HR_FIELDS = [
    "task_id",
    "hr_parent",
    "candidate_id",
    "candidate_name",
    "machine_recommendation",
    "readiness_rank",
    "four_gate_summary",
    "source_proposal_refs",
    "alias_duplicate_refs",
    "module_value_question",
    "key_human_question",
    "decision",
    "reviewer",
    "review_date",
    "review_note",
]


def refs(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).lower()
    return re.sub(r"[\s・･!！?？「」『』（）()\[\]【】,，、/／:：;；'\"“”‘’]+", "", value)


def normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="raise", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def stable_hr027_id(candidate_id: str) -> str:
    return f"HR027-{candidate_id}"


def merge_hr027_human_fields(
    generated: list[dict[str, str]],
    existing: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Preserve human work across deterministic task regeneration.

    New rows use candidate-derived stable task IDs.  The candidate-ID fallback
    migrates the legacy rank-derived IDs (HR027-001 etc.) once without losing
    completed review fields.
    """
    by_task: dict[str, dict[str, str]] = {}
    by_candidate: dict[str, dict[str, str]] = {}
    for row in existing:
        task_id = row.get("task_id", "").strip()
        candidate_id = row.get("candidate_id", "").strip()
        require(task_id and task_id not in by_task, f"duplicate existing HR-027 task ID: {task_id}")
        require(
            candidate_id and candidate_id not in by_candidate,
            f"duplicate existing HR-027 candidate ID: {candidate_id}",
        )
        by_task[task_id] = row
        by_candidate[candidate_id] = row

    generated_candidates = {row["candidate_id"] for row in generated}
    orphaned = set(by_candidate) - generated_candidates
    require(not orphaned, f"existing HR-027 rows would be orphaned: {sorted(orphaned)}")

    merged: list[dict[str, str]] = []
    for seed in generated:
        prior = by_task.get(seed["task_id"]) or by_candidate.get(seed["candidate_id"])
        row = dict(seed)
        if prior:
            require(
                prior["candidate_id"] == seed["candidate_id"],
                f"HR-027 stable ID/candidate mismatch: {seed['task_id']}",
            )
            for field in HUMAN_REVIEW_FIELDS:
                row[field] = prior.get(field, "")
        merged.append(row)
    return merged


def build_source_log_provenance(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    source_log_rows = read_csv(SOURCE_LOG)
    snapshot_rows = [
        row
        for row in source_log_rows
        if SOURCE_SNAPSHOT_MIN <= int(row["source_id"][1:]) <= SOURCE_SNAPSHOT_MAX
    ]
    require(
        len(snapshot_rows) == SOURCE_SNAPSHOT_MAX - SOURCE_SNAPSHOT_MIN + 1,
        f"source snapshot must contain S001–S294 exactly, got {len(snapshot_rows)} rows",
    )
    require(
        {row["source_id"] for row in snapshot_rows}
        == {f"S{number:03d}" for number in range(SOURCE_SNAPSHOT_MIN, SOURCE_SNAPSHOT_MAX + 1)},
        "source snapshot IDs are not the complete S001–S294 range",
    )
    by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in snapshot_rows:
        url = row.get("url", "").strip()
        if url.startswith("http://") or url.startswith("https://"):
            by_url[normalize_url(url)].append(row)

    provenance: list[dict[str, str]] = []
    for proposal in sources:
        matches = by_url.get(normalize_url(proposal["url"]), [])
        require(
            len(matches) == 1,
            f"{proposal['proposal_id']} must map to one S001–S294 snapshot row, got {[row['source_id'] for row in matches]}",
        )
        snapshot = matches[0]
        source_number = int(snapshot["source_id"][1:])
        if snapshot["source_id"] in {"S158", "S204"}:
            state = "preexisting_reuse"
        else:
            require(248 <= source_number <= 294, f"unexpected NW2-C source ID: {snapshot['source_id']}")
            require(NW2H_MARKER in snapshot["notes"], f"{snapshot['source_id']} lacks NW2-H provenance marker")
            state = "nw2h_provisional_source_index"
        provenance.append(
            {
                "proposal_id": proposal["proposal_id"],
                "candidate_id": proposal["candidate_id"],
                "normalized_url": normalize_url(proposal["url"]),
                "historical_source_log_match": proposal["source_log_match"],
                "snapshot_scope": SOURCE_SNAPSHOT_LABEL,
                "snapshot_source_id": snapshot["source_id"],
                "snapshot_source_state": state,
                "snapshot_source_review_status": snapshot["review_status"],
                "relation_or_claim_approved": "no",
            }
        )
    return provenance


def normalize_output_svg_whitespace(root: Path) -> int:
    """Strip trailing spaces/tabs from any SVG assets in this package."""
    changed = 0
    for path in sorted(root.rglob("*.svg")):
        original = path.read_text(encoding="utf-8")
        had_terminal_newline = original.endswith(("\n", "\r"))
        cleaned = "\n".join(line.rstrip(" \t") for line in original.splitlines())
        if had_terminal_newline:
            cleaned += "\n"
        if cleaned != original:
            path.write_text(cleaned, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def count_svg_trailing_whitespace(root: Path) -> tuple[int, int]:
    files = list(root.rglob("*.svg"))
    bad_lines = sum(
        1
        for path in files
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.rstrip(" \t") != line
    )
    return len(files), bad_lines


def build_gate_matrix() -> list[dict[str, str]]:
    matrix: list[dict[str, str]] = []
    rules = {
        "formal_identity": "Exact organization name plus organizational form, named office/representative, rules, official record or equivalent organization-level evidence; an event label is insufficient.",
        "continuity": "At least two dated organization-level observations separated in time, or formal current status plus recent activity; one signature/event is insufficient.",
        "direct_phase1_connection": "At least one dated public role directly tied to a Phase-1 issue such as base/SDF, PFAS/health, groundwater, autonomy, legal procedure or military violence.",
        "module_repair_value": "Adds a missing place, actor function, issue bridge, venue or action mechanism that can change a named module explanation; number-filling is insufficient.",
    }
    mappings = [
        ("formal_identity", "formal_identity_gate", "formal_identity_evidence"),
        ("continuity", "continuity_gate", "continuity_evidence"),
        ("direct_phase1_connection", "direct_phase1_connection_gate", "direct_phase1_connection_evidence"),
        ("module_repair_value", "module_repair_value_gate", "module_repair_value"),
    ]
    for candidate in sorted(CANDIDATES, key=lambda row: int(row["readiness_rank"])):
        for gate, status_field, evidence_field in mappings:
            matrix.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_name": candidate["candidate_name"],
                    "gate": gate,
                    "status": candidate[status_field],
                    "pass_rule": rules[gate],
                    "evidence_summary": candidate[evidence_field],
                    "source_proposal_refs": candidate["source_proposal_refs"],
                    "boundary": candidate["boundary_note"],
                }
            )
    return matrix


def build_hr_rows() -> list[dict[str, str]]:
    questions = {
        "RV2C001": (
            "Does a sustained Miyako groundwater research/advocacy actor materially repair R2-R4 beyond A012/A097?",
            "Approve add/defer/reject, exact actor class and narrow issue scope; confirm that C015/A012 remain separate and freeze the leadership timeline without treating stated SDF wastewater risk as proven contamination.",
        ),
        "RV2C002": (
            "Does the hyperlocal resident-sampling and municipal-request mechanism warrant a distinct PFAS actor beside A099?",
            "Approve add/defer/reject and alias; keep A099 separate, and bound claims to sampling/request/procedure roles without asserting epidemiological effect or proven source causation.",
        ),
        "RV2C004": (
            "Does the union's port/workplace capacity add a needed labor and Sakishima venue mechanism to R5/R7?",
            "Approve add/defer/reject, branch aliases and issue scope; record the 2015/2024 actions without adjudicating strike legality/effect or inferring alliances.",
        ),
        "RV2C003": (
            "Does the Okinawa prefectural headquarters merit a branch-level actor as a sustained women/human-rights channel distinct from A049/A107/A111?",
            "Approve add/defer/reject and branch-level actor policy; do not transfer all parent-body actions or infer party affiliation from coverage.",
        ),
    }
    rows: list[dict[str, str]] = []
    for candidate in sorted(CANDIDATES, key=lambda row: int(row["readiness_rank"])):
        if candidate["machine_recommendation"] != "ready_for_human_decision":
            continue
        module_question, human_question = questions[candidate["candidate_id"]]
        rows.append(
            {
                "task_id": stable_hr027_id(candidate["candidate_id"]),
                "hr_parent": "HR-027",
                "candidate_id": candidate["candidate_id"],
                "candidate_name": candidate["candidate_name"],
                "machine_recommendation": candidate["machine_recommendation"],
                "readiness_rank": candidate["readiness_rank"],
                "four_gate_summary": "identity=pass;continuity=pass;direct_phase1=pass;module_value=pass",
                "source_proposal_refs": candidate["source_proposal_refs"],
                "alias_duplicate_refs": candidate["alias_duplicate_refs"],
                "module_value_question": module_question,
                "key_human_question": human_question,
                "decision": "",
                "reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )
    return rows


def build_readme(ready: list[dict[str, str]], provenance: list[dict[str, str]]) -> str:
    reviewed = sum(bool(row["decision"].strip()) for row in ready)
    provisional = sum(
        row["snapshot_source_state"] == "nw2h_provisional_source_index"
        for row in provenance
    )
    return f"""# Registry value gate v2

日期：{DATE}

这个包执行 NW2-C，只做组织级候选的机器证据门控。它没有修改 actor registry、source log、issue/place/event/relation 中央表，没有分配 A 号，也没有把候选关系写成事实边。

## 结果

- 完整评估 5 个组织级候选；首要对象 `宮古島地下水研究会` 已完成四门核查。
- 4 个达到 `ready_for_human_decision`：宮古島地下水研究会、宜野湾ちゅら水会、全日本港湾労働組合沖縄地方本部、新日本婦人の会沖縄県本部。
- 1 个 `defer_online_continuity_gap`：八重山大地会。它有 2015–2017 组织级证据，但缺 2018–2026 的持续／解散／承继记录，不送 HR-027。
- `ready_for_human_decision` 不是 add 决定。四个候选仍须由 HR-027 人工选择 add/defer/reject，并冻结 alias、actor class、issue scope 和边界措辞。

## 文件

- `registry_value_gate_v2.csv`：五候选四门、排序、机器建议与边界。
- `four_gate_evidence_matrix_v2.csv`：5 × 4 = 20 条逐门证据矩阵。
- `alias_duplicate_crosswalk_v2.csv`：12 条别名／近名／既有 actor 去重记录。
- `source_proposals_v2.csv`：29 条历史 source proposal；原始 `source_log_match` 只标 S158/S204，29/29 `relation_or_claim_approved=no`。
- `source_log_provenance_v2.csv`：建包时的候选来源整合快照（S001–S294）中的 29/29 URL 交叉表；其中 {provisional} 条为 NW2-H provisional source index。S295 属于该批完成后的补充来源，明确不纳入本候选来源批快照；快照索引存在不批准 actor、edge 或 claim。
- `HR027_registry_value_review_v0.csv`：{len(ready)} 条真正达到人工决定门槛的任务；按稳定候选任务号保留人审字段，当前已填写 decision {reviewed} 条。
- `registry_value_gate_brief_v2.md`：排序、解释增量与强制边界。
- `validation_report_v2.md`：脚本内机械校验结果。

中央可消费的候选副本为 `data/interim/34_registry_value_candidates_v2.csv`，内容与本包 gate 表逐字节一致。

## 明确排除

- A073 的退出／保留继续由 HR-024 控制；本包不重复创建任务。
- C015 继续属于 HR-011；宮古島地下水研究会的证据不能替代 C015 身份复核。
- 一次署名、一般公益使命、共同参与或单场活动均未被当作持续组织证据。
- 来源提案不批准 actor 入表、alias、edge、联盟、资金或因果解释。
"""


def build_brief() -> str:
    return f"""# Registry 价值驱动补样 brief v2

日期：{DATE}

## 结论先行

本轮不是从 118 向 120 的数字填空，而是检验候选能否修复当前解释薄层。五个候选中有四个闭合了正式身份、持续性、一期直接连接、模块修复价值四道门；八重山大地会只闭合前三项中的身份和直接连接，持续性仍停在 2015–2017，因此暂缓。

机器优先级如下：

1. **宮古島地下水研究会**：最强增量。2018 年组织概要、2018–2025 活动档案、2023 年宫古岛市正式回应和多次政策材料共同闭合身份与持续性；它把宫古地下水从一般环境议题推进到“监测—条例—行政回应—生命安全”机制。组织公开材料把自卫队设施排水列为风险类别，但本项目只能编码其提出该风险和监管主张，不能写成已证实污染。
2. **宜野湾ちゅら水会**：PFAS／健康薄层的高价值补点。它的特征不是共同署名，而是居民筹资委托采样、健康调查请求、市议会请愿和公害调停等可区分渠道。2026 年同场资料把该会与 A099 分列，故不能合并；共同出现也不构成联盟。
3. **全日本港湾労働組合沖縄地方本部**：劳工与场域机制增量最大。正式劳工记录闭合 2014–2026 的组织持续性；2015 年边野古／安保行动和 2024 年石垣港军舰寄港争议显示，港湾劳动能力会把基地争议转入工作场所、民用港与职业安全。记录事件存在和公开理由即可，不能在本包裁断罢工合法性、效果或联盟关系。
4. **新日本婦人の会沖縄県本部**：女性／人权层的持续地方单位。2008、2014、2018、2024 的组织级记录显示它并非一次声明节点；价值在于把美军性暴力、女性人权、边野古和公投动员连接起来。人工仍须决定全国组织的县本部是否作为独立 actor，并禁止把中央本部全部行动自动转移给地方单位。
5. **八重山大地会**：有意义但暂缓。2015 成立线索、2016/2017 具名代表和组织活动可核，且能补石垣战争记忆／文化性反部署框架；但网上未找到 2018–2026 的持续、解散或承继材料。分析图还提示它可能是 A010 的组成团体，不能据此合并或写稳定成员边。

## 四门定义

| 门 | 通过条件 | 本轮结果 |
|---|---|---|
| 正式身份 | 确切名称＋组织形式／规则／办公室／具名负责人／官方记录之一组组织级证据；活动名称不够 | 5 pass |
| 持续性 | 跨时点组织级观察，或持续法律身份＋近期活动；一次署名／单场活动不够 | 4 pass，1 partial |
| 一期直接连接 | 有日期的基地、自卫队、PFAS/健康、地下水、自治、程序或军事暴力公开角色 | 5 pass |
| 模块修复价值 | 新增地点、功能、桥接、场域或行动机制，能改变明确模块解释 | 5 pass |

## 人工决定时最关键的边界

- **代表人时间线**：宮古島地下水研究会 2018 概要与 2020–2025 材料出现不同共同代表，这是可解释的领导变动，不应强行固定成单一永久名单；人审只需确认入表所用的时间化说明。
- **科学与因果**：采样、风险主张、要请和政府回应是可编码行动；PFAS 健康因果、自卫队设施实际污染、项目效果均不是本 gate 的结论。
- **组织单位**：县本部／地方本部可以因持续的本地行动成为 actor，但不能把全国母体全部行为继承下来。
- **近名去重**：宮古島地下水研究会不解决 C015，也不自动成为 A012 的别名；宜野湾ちゅら水会与 A099 分开；八重山大地会与 A010 的组成关系仍未冻结。
- **共同参与**：共同请求、共同集会、共同调停、同一游行或同一报告出现都不生成稳定联盟边。

## 对 120 下限的含义

若人工从前四名中批准至少两个组织级 actor，registry 可恢复到合同最低 120；但批准理由必须分别是模块修复，而不是“需要两个数”。即使达到 120，R1–R11 仍未饱和时也不应停止价值驱动补样。

## A073 与后续

A073 完全不在本包候选或 HR-027 中，退出／保留继续由 HR-024 决定。八重山大地会也不另建人工任务；只有持续性或历史 actor 范围被新证据闭合后，才进入下一轮人审。
"""


def validate(
    candidates: list[dict[str, str]],
    sources: list[dict[str, str]],
    crosswalk: list[dict[str, str]],
    matrix: list[dict[str, str]],
    hr_rows: list[dict[str, str]],
    provenance: list[dict[str, str]],
    svg_stats: tuple[int, int],
) -> str:
    expected_ids = {"RV2C001", "RV2C002", "RV2C003", "RV2C004", "RV2C005"}
    candidate_ids = [row["candidate_id"] for row in candidates]
    require(set(candidate_ids) == expected_ids, f"candidate IDs differ: {candidate_ids}")
    require(len(candidate_ids) == len(set(candidate_ids)) == 5, "candidate IDs must be unique")
    require(candidate_ids == ["RV2C001", "RV2C002", "RV2C004", "RV2C003", "RV2C005"], "ranked order drifted")
    require(not any("A073" in "|".join(row.values()) for row in candidates), "A073 duplicated in candidate gate")
    require(not any(re.fullmatch(r"A\d{3}", row["candidate_id"]) for row in candidates), "an A-number was assigned")
    require(all(row["one_off_signatory_guard"].startswith("pass:") for row in candidates), "one-off shortcut found")

    ready = [row for row in candidates if row["machine_recommendation"] == "ready_for_human_decision"]
    require(len(ready) == 4, f"ready count drifted: {len(ready)}")
    for row in ready:
        require(
            all(
                row[field] == "pass"
                for field in (
                    "formal_identity_gate",
                    "continuity_gate",
                    "direct_phase1_connection_gate",
                    "module_repair_value_gate",
                )
            ),
            f"{row['candidate_id']} is ready without four pass gates",
        )
        require(row["hr_route"] == "HR-027", f"{row['candidate_id']} has wrong HR route")
        require(row["machine_count_ready"] == "yes_pending_human", f"{row['candidate_id']} count-ready drift")
    deferred = next(row for row in candidates if row["candidate_id"] == "RV2C005")
    require(deferred["continuity_gate"] == "partial", "Yaeyama continuity must remain partial")
    require(deferred["machine_count_ready"] == "no", "Yaeyama must not be count-ready")
    require(deferred["hr_route"].startswith("none_"), "Yaeyama must not enter HR-027")

    target_text = " ".join(row["target_gap"] for row in candidates).lower()
    require("pfas" in target_text, "PFAS/health layer missing")
    require("sakishima" in target_text or "ishigaki" in target_text, "Sakishima local layer missing")
    require("women" in target_text and "labor" in target_text, "women/labor thin layers missing")

    proposal_ids = [row["proposal_id"] for row in sources]
    require(len(proposal_ids) == len(set(proposal_ids)) == 29, "source proposal IDs/count drifted")
    proposal_set = set(proposal_ids)
    require(all(row["relation_or_claim_approved"] == "no" for row in sources), "a source proposal approved a claim/relation")
    urls = [normalize_url(row["url"]) for row in sources]
    require(len(urls) == len(set(urls)), "duplicate normalized source proposal URL")
    by_candidate_sources: dict[str, int] = Counter(row["candidate_id"] for row in sources)
    require(all(by_candidate_sources[candidate_id] >= 5 for candidate_id in expected_ids), "a candidate has fewer than five source proposals")

    crosswalk_ids = [row["crosswalk_id"] for row in crosswalk]
    require(len(crosswalk_ids) == len(set(crosswalk_ids)) == 12, "crosswalk IDs/count drifted")
    crosswalk_set = set(crosswalk_ids)
    for row in candidates:
        missing_sources = refs(row["source_proposal_refs"]) - proposal_set
        require(not missing_sources, f"{row['candidate_id']} missing sources {sorted(missing_sources)}")
        missing_crosswalk = refs(row["alias_duplicate_refs"]) - crosswalk_set
        require(not missing_crosswalk, f"{row['candidate_id']} missing crosswalk {sorted(missing_crosswalk)}")
    for row in crosswalk:
        require(row["candidate_id"] in expected_ids, f"unknown crosswalk candidate {row['candidate_id']}")
        missing_sources = refs(row["source_proposal_refs"]) - proposal_set
        require(not missing_sources, f"{row['crosswalk_id']} missing sources {sorted(missing_sources)}")

    require(len(matrix) == 20, "four-gate matrix must have 20 rows")
    gate_counts = Counter(row["gate"] for row in matrix)
    require(set(gate_counts.values()) == {5}, f"gate matrix counts drifted: {gate_counts}")

    hr_candidate_ids = {row["candidate_id"] for row in hr_rows}
    require(hr_candidate_ids == {row["candidate_id"] for row in ready}, "HR-027 differs from ready candidates")
    require(len(hr_rows) == 4, "HR-027 row count drifted")
    for row in hr_rows:
        require(
            row["task_id"] == stable_hr027_id(row["candidate_id"]),
            f"unstable HR-027 task ID: {row['task_id']}",
        )
        for field in HUMAN_REVIEW_FIELDS:
            require(field in row, f"{row['task_id']} lacks human field {field}")
        require(not "A073" in "|".join(row.values()), "A073 duplicated in HR-027")
        require(not (refs(row["source_proposal_refs"]) - proposal_set), f"{row['task_id']} missing source refs")

    registry = read_csv(REGISTRY)
    existing_names = {normalize_text(row["canonical_name"]): row["actor_id"] for row in registry}
    exact_collisions = {
        row["candidate_id"]: existing_names.get(normalize_text(row["candidate_name"]), "")
        for row in candidates
        if normalize_text(row["candidate_name"]) in existing_names
    }
    require(not exact_collisions, f"unresolved exact registry collision: {exact_collisions}")

    source_log = {row["source_id"]: row for row in read_csv(SOURCE_LOG)}
    matched = [row for row in sources if row["source_log_match"]]
    require({row["source_log_match"] for row in matched} == {"S158", "S204"}, "existing source match set drifted")
    for row in matched:
        source_id = row["source_log_match"]
        require(source_id in source_log, f"missing main source match {source_id}")
        require(
            normalize_url(source_log[source_id]["url"]) == normalize_url(row["url"]),
            f"source match URL mismatch for {source_id}",
        )

    require(len(provenance) == 29, "source-log provenance must cover all 29 proposals")
    require(
        {row["proposal_id"] for row in provenance} == proposal_set,
        "source-log provenance proposal coverage drifted",
    )
    require(
        all(row["relation_or_claim_approved"] == "no" for row in provenance),
        "source-log provenance approved a claim/relation",
    )
    require(
        {row["snapshot_scope"] for row in provenance} == {SOURCE_SNAPSHOT_LABEL},
        "source-log provenance must retain one explicit build-time snapshot scope",
    )
    require(
        all(
            SOURCE_SNAPSHOT_MIN <= int(row["snapshot_source_id"][1:]) <= SOURCE_SNAPSHOT_MAX
            for row in provenance
        ),
        "source-log provenance escaped the S001–S294 build-time snapshot",
    )
    require(
        all(row["snapshot_source_id"] != "S295" for row in provenance),
        "S295 must not enter the NW2-C/NW2-H candidate-source snapshot",
    )
    provenance_counts = Counter(row["snapshot_source_state"] for row in provenance)
    require(
        provenance_counts
        == Counter({"nw2h_provisional_source_index": 27, "preexisting_reuse": 2}),
        f"S001–S294 build-time snapshot provenance state drifted: {provenance_counts}",
    )
    require(
        all(row["snapshot_source_review_status"] in {"ai_seeded", "human_checked"} for row in provenance),
        "unexpected snapshot source review status",
    )

    require(sha256(OUT / "registry_value_gate_v2.csv") == sha256(INTERIM), "interim/output gate bytes differ")
    svg_files, svg_bad_lines = svg_stats
    require(svg_bad_lines == 0, f"registry package SVG trailing whitespace lines: {svg_bad_lines}")

    recommendation_counts = Counter(row["machine_recommendation"] for row in candidates)
    populated_decisions = sum(bool(row["decision"].strip()) for row in hr_rows)
    return f"""# Registry value gate v2 validation

- candidates: {len(candidates)} (unique: {len(set(candidate_ids))})
- ready_for_human_decision: {recommendation_counts['ready_for_human_decision']}
- defer_online_continuity_gap: {recommendation_counts['defer_online_continuity_gap']}
- four-gate matrix: {len(matrix)} rows (5 candidates × 4 gates)
- source proposals: {len(sources)} unique URLs; claim/relation approvals: 0
- alias/duplicate crosswalk: {len(crosswalk)} rows
- HR-027 rows: {len(hr_rows)}; stable candidate-derived task IDs; populated decisions preserved: {populated_decisions}
- exact canonical collisions with the current registry: 0
- existing source reuse: S158 and S204 URL-matched
- build-time S001–S294 candidate-source snapshot provenance: 29/29 mapped (2 preexisting reuse; 27 NW2-H provisional indexes); S295 excluded by scope
- source provenance claim/relation approvals: 0
- package SVG files checked: {svg_files}; trailing-whitespace lines: {svg_bad_lines}
- one-off signatory/general-mission shortcuts: 0
- A numbers assigned: 0
- A073 duplicate task rows: 0
- central actor/source/edge writes: 0
- interim/output gate SHA-256 match: yes
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ordered_candidates = sorted(CANDIDATES, key=lambda row: int(row["readiness_rank"]))
    ordered_sources = sorted(SOURCES, key=lambda row: int(row["proposal_id"].replace("RV2SP", "")))
    ordered_crosswalk = sorted(CROSSWALK, key=lambda row: int(row["crosswalk_id"].replace("RV2X", "")))
    matrix = build_gate_matrix()
    hr_path = OUT / "HR027_registry_value_review_v0.csv"
    existing_hr_rows = read_csv(hr_path) if hr_path.exists() else []
    hr_rows = merge_hr027_human_fields(build_hr_rows(), existing_hr_rows)
    provenance = build_source_log_provenance(ordered_sources)

    gate_path = OUT / "registry_value_gate_v2.csv"
    write_csv(gate_path, ordered_candidates, CANDIDATE_FIELDS)
    shutil.copyfile(gate_path, INTERIM)
    write_csv(
        OUT / "four_gate_evidence_matrix_v2.csv",
        matrix,
        ["candidate_id", "candidate_name", "gate", "status", "pass_rule", "evidence_summary", "source_proposal_refs", "boundary"],
    )
    write_csv(OUT / "alias_duplicate_crosswalk_v2.csv", ordered_crosswalk, CROSSWALK_FIELDS)
    write_csv(OUT / "source_proposals_v2.csv", ordered_sources, SOURCE_FIELDS)
    write_csv(OUT / "source_log_provenance_v2.csv", provenance, PROVENANCE_FIELDS)
    write_csv(hr_path, hr_rows, HR_FIELDS)
    (OUT / "README.md").write_text(build_readme(hr_rows, provenance), encoding="utf-8")
    (OUT / "registry_value_gate_brief_v2.md").write_text(build_brief(), encoding="utf-8")

    normalize_output_svg_whitespace(OUT)
    svg_stats = count_svg_trailing_whitespace(OUT)
    report = validate(
        ordered_candidates,
        ordered_sources,
        ordered_crosswalk,
        matrix,
        hr_rows,
        provenance,
        svg_stats,
    )
    (OUT / "validation_report_v2.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
