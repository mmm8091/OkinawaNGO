from __future__ import annotations

"""Build the research-only H3 v2 package.

This package tests two claims without writing to central data:

1. whether a formal cross-regional carrier has emerged around the language of
   preventing war/frontline conversion; and
2. whether the 2025 declaration and 2026 petition construct a shared document-
   level object from bases, missiles, depots, transport infrastructure and
   evacuation plans.

The builder deliberately keeps common frame, common object, dated
participating-group listings, event endorsement and independent adoption
separate.  It writes only to
``outputs/research_wave_h3_frontline_memory_v2`` (or an explicitly supplied
output directory).
"""

import csv
import hashlib
import json
import sys
from collections import Counter
from html import escape
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "outputs" / "research_wave_h3_frontline_memory_v2"

COMMON = {
    "data_layer": "research_only",
    "claim_status": "candidate",
    "review_status": "ai_seeded",
    "frontend_eligibility": "not_frontend_ready",
    "central_writeback": "no",
}

PROTECTED_INPUTS = (
    ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv",
    ROOT / "data" / "interim" / "05_source_log_initial_v0.csv",
    ROOT / "outputs" / "research_wave_h3_frontline_memory_v1"
    / "event_participant_candidates_v1.csv",
    ROOT / "outputs" / "research_wave_h3_frontline_memory_v1"
    / "source_observations_v1.csv",
)

STALE_OUTPUT_FILENAMES = (
    "network_membership_candidates_v2.csv",
    "four_island_petition_entities_v2.csv",
    "four_island_issue_family_coverage_v2.csv",
    "scale_shift_case_A010_v2.csv",
)


def guarded(row: dict[str, str], **overrides: str) -> dict[str, str]:
    return {**row, **COMMON, **overrides}


SOURCES = [
    {
        "source_id": "S003",
        "central_source_id": "S003",
        "date": "2010",
        "source_owner": "WWF Japan and listed signatories",
        "source_type": "organization-authored joint statement",
        "title": "67団体がジュゴンの生息地辺野古への基地建設反対に共同声明",
        "url": "https://www.wwf.or.jp/activities/statement/3436.html",
        "authority": "organization_primary",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive",
        "use_scope": "matched negative control for an environmental joint statement",
        "boundary": "No target term in this document is a genre-bounded negative, not a society-wide absence.",
    },
    {
        "source_id": "S004",
        "central_source_id": "S004",
        "date": "2015",
        "source_owner": "Nature Conservation Society of Japan and listed signatories",
        "source_type": "organization-authored joint statement",
        "title": "辺野古の海を守れ NGO 31団体が緊急共同声明",
        "url": "https://www.nacsj.or.jp/statement/50827/",
        "authority": "organization_primary",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive",
        "use_scope": "matched negative control for an environmental joint statement",
        "boundary": "No target term in this document is a genre-bounded negative, not a society-wide absence.",
    },
    {
        "source_id": "S006",
        "central_source_id": "S006",
        "date": "2020",
        "source_owner": "Okinawa Environmental Justice Project / petition participants",
        "source_type": "organization-authored international request",
        "title": "OEJP 71 organizations Marine Mammal Commission request",
        "url": "https://okinawaejp.blogspot.com/2020/07/",
        "authority": "organization_primary",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive",
        "use_scope": "matched negative control for an international environmental request",
        "boundary": "English-language term scan is document-bounded and cannot establish a historical trend.",
    },
    {
        "source_id": "S022",
        "central_source_id": "S022",
        "date": "2022-12-07",
        "source_owner": "沖縄対話プロジェクト",
        "source_type": "organization site",
        "title": "沖縄対話プロジェクト 公式ページ",
        "url": "https://okinawataiwa.net/",
        "authority": "organization_primary",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive_metadata_correction_pending",
        "use_scope": "pre-network Okinawa memory / Taiwan-contingency framing",
        "boundary": "Project framing does not prove participant consensus or diffusion.",
    },
    {
        "source_id": "S023",
        "central_source_id": "S023",
        "date": "2022-03-21",
        "source_owner": "QAB reporting A018",
        "source_type": "local news",
        "title": "ノーモア沖縄戦 命どぅ宝の会 結成",
        "url": "https://www.qab.co.jp/news/20220321148994.html",
        "authority": "independent_local_news",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive",
        "use_scope": "attributed pre-network public position of A018",
        "boundary": "Media attribution is not an organization-authored full statement.",
    },
    {
        "source_id": "S036",
        "central_source_id": "S036",
        "date": "2017-02-28",
        "source_owner": "Ryukyu Shimpo reporting four civic groups",
        "source_type": "local news",
        "title": "南西諸島四団体政府交渉",
        "url": "https://ryukyushimpo.jp/news/entry-452562.html",
        "authority": "independent_local_news",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive_metadata_correction_pending",
        "use_scope": "older cross-island government-negotiation baseline",
        "boundary": "The central source title/year mismatch remains gated; event participation is not alliance.",
    },
    {
        "source_id": "S119",
        "central_source_id": "S119",
        "date": "2022-11-29",
        "source_owner": "Ryukyu Shimpo reporting A100",
        "source_type": "local news",
        "title": "うるま市民の会発足報道",
        "url": "https://ryukyushimpo.jp/news/entry-1623776.html",
        "authority": "independent_local_news",
        "full_text_status": "local_residual_archive",
        "archive_status": "central_archive_reconciliation_pending",
        "use_scope": "attributed pre-network public position of A100",
        "boundary": "Archive reconciliation and source-log date correction remain required.",
    },
    {
        "source_id": "S146",
        "central_source_id": "S146",
        "date": "2023",
        "source_owner": "沖縄を再び戦場にさせない県民の会",
        "source_type": "organization site",
        "title": "沖縄を再び戦場にさせない県民の会 公式サイト",
        "url": "https://kenminnokai.okinawa/",
        "authority": "organization_primary",
        "full_text_status": "organization_site",
        "archive_status": "central_archive",
        "use_scope": "prefectural carrier formation and program",
        "boundary": "A 63-group umbrella does not automatically create dyadic alliance edges.",
    },
    {
        "source_id": "S148",
        "central_source_id": "S148",
        "date": "2023-07-26",
        "source_owner": "Ryukyu Shimpo reporting A108 formation",
        "source_type": "local news",
        "title": "沖縄を再び戦場にさせない県民の会 発足報道",
        "url": "https://ryukyushimpo.jp/news/entry-1754082.html",
        "authority": "independent_local_news",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive",
        "use_scope": "formation carrier and named organizing-center evidence",
        "boundary": "A named organizer or speaker cannot transfer a position to every participant.",
    },
    {
        "source_id": "S246",
        "central_source_id": "S246",
        "date": "2023-11-12",
        "source_owner": "沖縄・琉球弧の声を届ける会",
        "source_type": "organization event record",
        "title": "第1回連続講座",
        "url": "https://ryukyukohp.jimdofree.com/%E3%83%9B%E3%83%BC%E3%83%A0/%E7%AC%AC1%E5%9B%9E-2023-11-12/",
        "authority": "organization_primary",
        "full_text_status": "complete_archived_text",
        "archive_status": "central_archive",
        "use_scope": "pre-network event master frame and 13 endorsers",
        "boundary": "Endorsement is event participation, not independent adoption or alliance.",
    },
    {
        "source_id": "H3V2S001",
        "central_source_id": "",
        "date": "2016-05-22",
        "source_owner": "日本YWCA",
        "source_type": "organization-authored protest statement",
        "title": "米軍属女性暴行殺害事件への抗議声明",
        "url": "https://www.ywca.or.jp/wp-content/uploads/2016/05/0522.pdf",
        "authority": "organization_primary",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "national women-organization war-memory baseline",
        "boundary": "Links Okinawa-war memory to bases/sexual violence; does not use the later distributed-system object.",
    },
    {
        "source_id": "H3V2S002",
        "central_source_id": "",
        "date": "2021-06",
        "source_owner": "東京YWCA newsletter; named contributor",
        "source_type": "organization newsletter contribution",
        "title": "平和創造―野尻湖から辺野古へ",
        "url": "https://www.tokyo.ywca.or.jp/docs/2021%E5%B9%B46%E6%9C%88%E5%8F%B7%E3%80%80%E5%B9%B3%E5%92%8C%E5%89%B5%E9%80%A0~%E9%87%8E%E5%B0%BB%E6%B9%96%E3%81%8B%E3%82%89%E8%BE%BA%E9%87%8E%E5%8F%A4%E3%81%B8~.pdf",
        "authority": "organization_publication_named_author",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "mainland publication connecting war remains, Sakishima buildup and renewed battlefield risk",
        "boundary": "A named contributor in a newsletter is not the position of all YWCA units.",
    },
    {
        "source_id": "H3V2S003",
        "central_source_id": "",
        "date": "2021-07",
        "source_owner": "日本原水協 world-conference materials; named speakers",
        "source_type": "conference proceedings",
        "title": "原水爆禁止2021年世界大会 国際会議資料",
        "url": "https://www.antiatom.org/Gpress/wp-content/uploads/2021/07/3cc464eaf2a793a6f3abbb2d26a56197.pdf",
        "authority": "organization_conference_material",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "national anti-nuclear venue using Taiwan/Sakishima battlefield language",
        "boundary": "Speaker text in conference proceedings is not adoption by every participant or affiliate.",
    },
    {
        "source_id": "H3V2S004",
        "central_source_id": "",
        "date": "2019",
        "source_owner": "石垣島に軍事基地をつくらせない市民連絡会 petition account",
        "source_type": "online petition",
        "title": "石垣島にミサイル基地はいらない",
        "url": "https://www.change.org/p/%E7%B7%8A%E6%80%A5-%E7%9F%B3%E5%9E%A3%E5%B3%B6%E3%81%AB%E3%83%9F%E3%82%B5%E3%82%A4%E3%83%AB%E5%9F%BA%E5%9C%B0%E3%81%AF%E3%81%84%E3%82%89%E3%81%AA%E3%81%84-%E5%8D%97%E3%81%AE%E6%A5%BD%E5%9C%92%E3%82%92%E5%AE%88%E3%82%8B%E3%81%9F%E3%82%81%E9%85%8D%E5%82%99%E3%81%AE%E4%B8%AD%E6%AD%A2%E3%82%92%E6%B1%82%E3%82%81%E3%81%BE%E3%81%99",
        "authority": "organization_public_petition_candidate",
        "full_text_status": "public_petition_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "pre-installation old-name A010 local-object baseline",
        "boundary": "Petition-account ownership and exact version date require human confirmation.",
    },
    {
        "source_id": "H3V2S005",
        "central_source_id": "",
        "date": "2023-02-09",
        "source_owner": "old-name A010 request reproduced by Shimbun Akahata",
        "source_type": "party press reproducing organization request",
        "title": "台湾有事を想定した避難・外交に関する石垣市民連絡会陳情",
        "url": "https://www.jcp.or.jp/akahata/aik22/2023-02-09/2023020904_02_0.html",
        "authority": "full_request_reproduced_by_party_press",
        "full_text_status": "reported_full_or_substantial_text",
        "archive_status": "not_archived_in_project",
        "use_scope": "pre-network old-name A010 Taiwan/evacuation/diplomacy frame",
        "boundary": "Party-hosted reproduction is not a neutral account; wording must be checked against the original request.",
    },
    {
        "source_id": "H3V2S006",
        "central_source_id": "",
        "date": "2023-02-25",
        "source_owner": "A100 request reproduced by Shimbun Akahata",
        "source_type": "party press reproducing organization request",
        "title": "うるま市民の会申し入れ",
        "url": "https://www.jcp.or.jp/akahata/aik22/2023-02-25/2023022504_08_0.html",
        "authority": "request_reproduced_by_party_press",
        "full_text_status": "reported_substantial_text",
        "archive_status": "not_archived_in_project",
        "use_scope": "pre-network A100 Okinawa-war/attack-target frame",
        "boundary": "Wording must be checked against the original request before central use.",
    },
    {
        "source_id": "H3V2S007",
        "central_source_id": "",
        "date": "2022-06-28",
        "source_owner": "Miyako civic group quoted by Shimbun Akahata",
        "source_type": "party press attributed statement",
        "title": "宮古島での戦場化反対発言",
        "url": "https://www.jcp.or.jp/akahata/aik22/2022-06-28/2022062815_01_0.html",
        "authority": "attributed_party_press",
        "full_text_status": "reported_excerpt",
        "archive_status": "not_archived_in_project",
        "use_scope": "pre-network Miyako language-use candidate",
        "boundary": "Not an organization-authored complete document.",
    },
    {
        "source_id": "H3V2S008",
        "central_source_id": "",
        "date": "2025-02-22 onward",
        "source_owner": "戦争止めよう！沖縄・西日本ネットワーク",
        "source_type": "organization site",
        "title": "戦争止めよう！沖縄・西日本ネットワーク 公式サイト",
        "url": "https://okinishi-net.org/",
        "authority": "organization_primary",
        "full_text_status": "organization_site",
        "archive_status": "not_archived_in_project",
        "use_scope": "identity, formation date, continuing activity and public information infrastructure",
        "boundary": "The organization is not a central-registry actor until a human decision.",
    },
    {
        "source_id": "H3V2S009",
        "central_source_id": "",
        "date": "2025-02-22",
        "source_owner": "戦争止めよう！沖縄・西日本ネットワーク",
        "source_type": "formation declaration",
        "title": "結成宣言",
        "url": "https://cpnet.bona.jp/data25/250303_1.pdf",
        "authority": "organization_primary",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "formation-declaration document frame and distributed war-preparation object",
        "boundary": "The document supports document-level coding; drafter, participating-group contributions and independent adoption are unknown.",
        "publisher_or_host": "formation-material host associated with the network",
        "document_author_or_drafter": "unknown in bounded public file",
        "speaker_or_subject": "",
        "attribution_status": "formation_declaration_document_not_participating_group_adoption",
    },
    {
        "source_id": "H3V2S010",
        "central_source_id": "",
        "date": "2025-02-22",
        "source_owner": "formation-meeting organizers",
        "source_type": "formation proposal and governance material",
        "title": "沖縄・西日本ネットワークの結成提案・活動の骨子",
        "url": "https://isfweb.org/wp-content/uploads/2025/02/f5a7a37028f6be15e2a2e11181aac569.pdf",
        "authority": "organization_primary",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "proposed governance, regional operators, co-chairs, secretariat and communication infrastructure",
        "boundary": "The proposal documents intended governance; implementation, division of labor and retention are unverified.",
    },
    {
        "source_id": "H3V2S011",
        "central_source_id": "",
        "date": "2025-05-06",
        "source_owner": "戦争止めよう！沖縄・西日本ネットワーク",
        "source_type": "action flyer and dated participating-group list",
        "title": "東京行動第二報・参加団体35団体",
        "url": "https://www.jca.apc.org/no-g7-hiroshima/wp-content/uploads/2025/05/202506tokyo-v2.pdf",
        "authority": "organization_primary",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "35 participating/constituent groups as listed on 2025-05-06 and self-narrated event sequence",
        "boundary": "The source says 参加団体／構成団体; it does not prove legal membership, retention, active division of labor or dyadic alliances.",
    },
    {
        "source_id": "H3V2S012",
        "central_source_id": "",
        "date": "2025-05-28",
        "source_owner": "A018",
        "source_type": "organization self-report",
        "title": "沖縄・西日本ネットワーク東京行動のお知らせ",
        "url": "https://nomore-okinawasen.org/38273/",
        "authority": "organization_self_narrative",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "organizer attribution of the 2023 rally as a trigger",
        "boundary": "Self-attributed trigger is not causal proof of diffusion.",
    },
    {
        "source_id": "H3V2S013",
        "central_source_id": "",
        "date": "2025-06-23",
        "source_owner": "independent video journalist report",
        "source_type": "independent civic-media report",
        "title": "沖縄・西日本ネットワーク 対政府集会に200人",
        "url": "https://yumo.blue/?p=3847",
        "authority": "independent_report",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "first government action, 35-group count and 200 reported participants",
        "boundary": "Attendance is report-specific; it does not establish durable mobilization.",
    },
    {
        "source_id": "H3V2S014",
        "central_source_id": "",
        "date": "2026-02-10",
        "source_owner": "Shukan Kinyobi",
        "source_type": "independent magazine report",
        "title": "日本の軍事化に危機感抱く市民団体が防衛省に新年度予算撤回要求",
        "url": "https://www.kinyobi.co.jp/kinyobinews/2026/02/10/antena-1718/",
        "authority": "independent_report",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "second government action; 38-group and 440-participant reported counts; issue bundle",
        "boundary": "35-to-38 is not a growth estimate without comparable dated rosters.",
    },
    {
        "source_id": "H3V2S015",
        "central_source_id": "",
        "date": "2023-04",
        "source_owner": "Okinawa Times",
        "source_type": "local news",
        "title": "基地反対市民ら 組織名称を変更 石垣で会見",
        "url": "https://www.okinawatimes.co.jp/articles/-/1140575",
        "authority": "independent_local_news_paywalled",
        "full_text_status": "search_snippet_and_title",
        "archive_status": "not_archived_in_project",
        "use_scope": "news-reported exact rename from old-name A010 to the new-name organization",
        "boundary": "This is a source-level reported rename fact. It conflicts with the current HR-012 lifecycle account, so central canonical/alias/lifecycle writeback remains human-pending.",
    },
    {
        "source_id": "H3V2S016",
        "central_source_id": "",
        "date": "2024-03-17",
        "source_owner": "Okinawa Times",
        "source_type": "local news",
        "title": "分断あおる動きに危機感 市民連絡会・藤井事務局長",
        "url": "https://www.okinawatimes.co.jp/articles/-/1326388",
        "authority": "independent_local_news_paywalled",
        "full_text_status": "search_snippet_and_metadata",
        "archive_status": "not_archived_in_project",
        "use_scope": "later report on the new-name organization and partial participant turnover",
        "boundary": "Source-level continuity does not override HR-012 centrally and does not support an installation-caused scale shift.",
    },
    {
        "source_id": "H3V2S017",
        "central_source_id": "",
        "date": "2025-03-22",
        "source_owner": "Ryukyu Shimpo",
        "source_type": "local news",
        "title": "長射程弾配備、撤回を 九州検討で石垣市民ら声明",
        "url": "https://ryukyushimpo.jp/national/entry-4077152.html",
        "authority": "independent_local_news",
        "full_text_status": "complete_search_result_text",
        "archive_status": "not_archived_in_project",
        "use_scope": "new-name Ishigaki organization statement on Kyushu deployment; continuity with A010 is a candidate",
        "boundary": "One reported statement proves neither A010 identity continuity, durable alliance, independent object shift nor diffusion direction.",
    },
    {
        "source_id": "H3V2S018",
        "central_source_id": "",
        "date": "2026-03-24",
        "source_owner": "Ryukyu Shimpo",
        "source_type": "local news",
        "title": "陸自石垣駐屯地の3周年行事、一般開放「中止を」",
        "url": "https://ryukyushimpo.jp/national/entry-5142618.html",
        "authority": "independent_local_news",
        "full_text_status": "complete_search_result_metadata",
        "archive_status": "not_archived_in_project",
        "use_scope": "continued local monitoring/action by the reported new-name Ishigaki organization",
        "boundary": "One report proves neither continuity with A010 nor organizational strength, retention or scale shift.",
    },
    {
        "source_id": "H3V2S019",
        "central_source_id": "",
        "date": "2024-03-06",
        "source_owner": "external participant report quoting Miyako organizers",
        "source_type": "movement press report",
        "title": "自衛隊宮古島駐屯地開設5周年記念式典反対",
        "url": "https://www.jrcl.jp/okinawa/28042-1/",
        "authority": "external_movement_report",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "speaker-specific Miyako battlefield/dialogue attribution before the 2025 participating-group list",
        "boundary": "External movement press attributes battlefield/dialogue language to a named A013 co-representative; evacuation/life-safety remarks come from other speakers.",
        "publisher_or_host": "週刊かけはし",
        "document_author_or_drafter": "尾形淳",
        "speaker_or_subject": "仲里共同代表ほか複数の別人発言者",
        "attribution_status": "speaker_specific_media_attribution",
    },
    {
        "source_id": "H3V2S020",
        "central_source_id": "",
        "date": "2024-10-02",
        "source_owner": "Miyakojima City",
        "source_type": "official meeting minutes",
        "title": "令和6年度第1回宮古島地域連絡会議事録",
        "url": "https://miyakojima.cmskit.jp/soshiki/shityo/kikaku/hisyokouhou/oshirase/20241002gijiroku.pdf",
        "authority": "government_primary",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "official record that a similar-name civic entity submitted opinions/requests and received responses",
        "boundary": "The record does not prove meeting attendance, exact crosswalk to A013 or adoption of the government's frame.",
        "publisher_or_host": "宮古島市",
        "document_author_or_drafter": "宮古島地域連絡会事務局",
        "speaker_or_subject": "ミサイル基地いらない住民連絡会（surface form; A013 crosswalk unresolved）",
        "attribution_status": "official_request_submission_record_not_attendance",
    },
    {
        "source_id": "H3V2S021",
        "central_source_id": "",
        "date": "2023 onward",
        "source_owner": "大分敷戸ミサイル弾薬庫問題を考える市民の会",
        "source_type": "organization site",
        "title": "敷戸ミサイル弾薬庫問題を考える",
        "url": "https://shikidoshimin.wixsite.com/shikido",
        "authority": "organization_primary",
        "full_text_status": "organization_site",
        "archive_status": "not_archived_in_project",
        "use_scope": "independent pre-network West Japan local frame and organization history",
        "boundary": "The site proves local adoption before the formal network, not a diffusion path.",
    },
    {
        "source_id": "H3V2S022",
        "central_source_id": "",
        "date": "2023-12-28",
        "source_owner": "大分敷戸ミサイル弾薬庫問題を考える市民の会",
        "source_type": "organization-authored protest statement",
        "title": "9棟弾薬庫建設計画への緊急抗議声明",
        "url": "https://ankei.jp/yuji/file/2403/002859_f1.pdf",
        "authority": "organization_primary_copy",
        "full_text_status": "complete_web_pdf",
        "archive_status": "not_archived_in_project",
        "use_scope": "pre-network link among residential risk, IHL, Sakishima logistics and evacuation",
        "boundary": "A hosted copy should be checked against the organization's original file.",
    },
    {
        "source_id": "H3V2S023",
        "central_source_id": "",
        "date": "2026-05-16",
        "event_or_submission_date": "2026-05-07",
        "publication_date": "2026-05-16",
        "source_owner": "A018 site publishing the joint petition",
        "source_type": "petition text dated/submitted 2026-05-07, page published 2026-05-16, with 35 endorsing groups",
        "title": "沖縄を最前線とする戦争準備に反対する請願",
        "url": "https://nomore-okinawasen.org/55871/",
        "authority": "organization_primary_event_document",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "common petition text plus three island-specific request sections; four-place action/speaking hyperedge; 35 endorsing groups",
        "boundary": "The petition was submitted on 2026-05-07 and published here on 2026-05-16. Endorsement, local-request authorship, speaking and first-action attribution remain separate.",
        "publisher_or_host": "ノーモア沖縄戦 命どぅ宝の会 website",
        "document_author_or_drafter": "unknown for common text and each island-specific section",
        "speaker_or_subject": "three section headings and four-place event speakers are separate",
        "attribution_status": "published_complete_document_drafter_unknown",
    },
    {
        "source_id": "H3V2S024",
        "central_source_id": "",
        "date": "2026-05-09",
        "event_or_submission_date": "2026-05-07",
        "publication_date": "2026-05-09",
        "source_owner": "Shimbun Akahata",
        "source_type": "party press event report",
        "title": "沖縄の島々を要塞化するな",
        "url": "https://www.jcp.or.jp/akahata/aik26/2026-05-09/2026050901_02_0.php",
        "authority": "external_report_party_press",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "party-press confirmation of the 2026-05-07 four-place action and attribution that it was a first joint initiative",
        "boundary": "Party press confirms occurrence but the 'first' description is reporter/organizer attribution, not an independently established universal first.",
    },
    {
        "source_id": "H3V2S025",
        "central_source_id": "",
        "date": "2023-04-30",
        "source_owner": "Ryukyu Shimpo",
        "source_type": "local news",
        "title": "「戦場になること前提にした戦争準備」PAC3配備に市民団体が抗議声明",
        "url": "https://ryukyushimpo.jp/news/entry-1702799.html",
        "authority": "independent_local_news",
        "full_text_status": "complete_web_page",
        "archive_status": "not_archived_in_project",
        "use_scope": "reports 2023-04-15 general-meeting rename, partial representative turnover and 2023-04-28 statement by the new-name organization",
        "boundary": "This supports reported_exact_rename at source level but does not override HR-012 centrally or prove installation-caused scale shift.",
        "publisher_or_host": "琉球新報",
        "document_author_or_drafter": "照屋大哲 (news article); organization statement drafter unknown",
        "speaker_or_subject": "石垣島の平和と自然を守る市民連絡会",
        "attribution_status": "independent_news_reported_exact_rename",
    },
]


HYPOTHESES = [
    guarded(
        {
            "hypothesis_id": "H3a",
            "claim": "反战／前线化／台湾有事词汇在冲绳民间组织中随时间增长",
            "unit_of_analysis": "comparable organization-authored document",
            "current_assessment": "not_testable_with_current_unbalanced_corpus",
            "support": "Three older complete environmental documents provide genre controls only.",
            "falsifier_or_competing_explanation": "Source/genre/organization entry imbalance can produce apparent growth.",
            "next_test": "Period × genre matched corpus with document-level denominators.",
        }
    ),
    guarded(
        {
            "hypothesis_id": "H3b",
            "claim": "跨地区组织形成了可观察的共同框架",
            "unit_of_analysis": "formation-declaration document, request or event text with ownership status",
            "current_assessment": "supported_for_formation_declaration_document_not_participating_group_adoption",
            "support": "The 2025 formation-declaration document joins war memory, everyday harm, evacuation, rights and peace diplomacy; its drafter is unverified.",
            "falsifier_or_competing_explanation": "Unknown drafters may aggregate already existing frames without changing participating groups' language.",
            "next_test": "Independent before/after texts for the same listed organizations plus text-ownership evidence.",
        }
    ),
    guarded(
        {
            "hypothesis_id": "H3c",
            "claim": "2025结成宣言与2026请愿在共同文件层构造／并置分布式战争准备对象",
            "unit_of_analysis": "common document × named infrastructure/process node",
            "current_assessment": "supported_at_common_document_layer_only",
            "support": "The two common texts connect bases, missiles, depots, civilian ports/airports/roads, transport, deployment and evacuation.",
            "falsifier_or_competing_explanation": "The broad object may be produced by drafters/secretariat aggregation; listed organizations' independent adoption and before/after change are unproven.",
            "next_test": "Establish text ownership, then compare same-organization local documents before/after participation.",
        }
    ),
    guarded(
        {
            "hypothesis_id": "H3d",
            "claim": "共同文件至少获得持续到2026年初的正式行动载体",
            "unit_of_analysis": "governance record, dated roster and repeated formal action",
            "current_assessment": "formal_action_carrier_supported_through_2026_01_without_institutionalization_claim",
            "support": "A governance proposal, 35 participating/constituent groups as-of 2025-05-06, communication infrastructure and two government actions are documented.",
            "falsifier_or_competing_explanation": "Repeated actions may depend on a small drafting/secretariat core; retention, actual division of labor and full governance execution are unmeasured.",
            "next_test": "Obtain dated lists/minutes and evidence of retention, task execution and participating-group activity.",
        }
    ),
    guarded(
        {
            "hypothesis_id": "H3e",
            "claim": "共同框架由冲绳向西日本发生了方向明确的扩散",
            "unit_of_analysis": "same-organization before/after text plus transmission evidence",
            "current_assessment": "unconfirmed_and_aggregation_is_equally_plausible",
            "support": "Several local organizations used related frames before the 2025 umbrella.",
            "falsifier_or_competing_explanation": "Independent local responses to the same national policy can converge without diffusion.",
            "next_test": "Trace explicit citations, workshops, drafts or actor testimony about adoption.",
        }
    ),
    guarded(
        {
            "hypothesis_id": "H3f",
            "claim": "新闻来源明确报道旧名称A010改称新名，但中央生命周期与HR-012冲突；且无安装后尺度上移证据",
            "unit_of_analysis": "reported rename × central lifecycle conflict × pre/post public texts",
            "current_assessment": "reported_exact_rename_central_lifecycle_human_pending_no_scale_shift_claim",
            "support": "Okinawa Times reports a name change; Ryukyu Shimpo reports a 2023-04-15 general-meeting rename and partial representative turnover. Old-name A010 had already used Taiwan/evacuation/diplomacy framing before the 2023-03-16 garrison opening.",
            "falsifier_or_competing_explanation": "HR-012's current lifecycle account conflicts with the news reports; national policy change and pre-existing broad framing defeat an installation-caused scale-shift inference.",
            "next_test": "Human-reconcile the reported rename with HR-012; compare texts without treating the garrison opening as the cause.",
        }
    ),
    guarded(
        {
            "hypothesis_id": "H3g",
            "claim": "共同框架与共同正式组织并不等价",
            "unit_of_analysis": "language evidence × dated formal roster × later event participation",
            "current_assessment": "supported_as_boundary_case",
            "support": "Media attributes battlefield/dialogue language to a named A013 co-representative. A similar-name entity appears as an opinion/request submitter in an official record; exact A013 crosswalk and attendance are unverified. A013 is absent from the dated 2025 list and appears as a 2026 endorser.",
            "falsifier_or_competing_explanation": "Roster omission may be clerical or temporary; absence is only as-of the dated list.",
            "next_test": "Obtain Miyako organization-authored text and ask both sides about participation timing and role.",
        }
    ),
]


NETWORK_PARTICIPATING_GROUPS = [
    ("Okinawa", "与那国島の明るい未来を願うイソバの会", "A016", "candidate_alias_match"),
    ("Okinawa", "石垣島の平和と自然を守る市民連絡会", "A010", "reported_exact_rename_crosswalk_central_lifecycle_human_pending"),
    ("Okinawa", "ノーモア沖縄戦 命どぅ宝の会", "A018", "exact_name"),
    ("Okinawa", "沖縄・琉球弧の声を届ける会", "A101", "exact_name"),
    ("Okinawa", "ミサイル配備から命を守るうるま市民の会", "A100", "exact_name"),
    ("Kagoshima", "戦争しない！かごしま実行委員会", "", "no_current_registry_match"),
    ("Kagoshima", "さつま町の弾薬庫問題を考える会", "", "no_current_registry_match"),
    ("Kagoshima", "「どんたちの馬毛島を返してや」馬毛島基地反対住民訴訟原告団", "", "no_current_registry_match"),
    ("Kumamoto", "平和を求め軍拡を許さない女たちの会・熊本", "", "no_current_registry_match"),
    ("Kumamoto", "反戦反核くまもとアクション", "", "no_current_registry_match"),
    ("Saga", "オスプレイストップ！９条実施アクション佐賀", "", "no_current_registry_match"),
    ("Oita", "大分敷戸ミサイル弾薬庫問題を考える市民の会", "", "no_current_registry_match"),
    ("Oita", "草の根の会・中津", "", "no_current_registry_match"),
    ("Oita", "湯布院駐屯地「敵基地攻撃」ミサイル問題を考えるネットワーク", "", "no_current_registry_match"),
    ("Oita", "ローカルネット大分・日出生台", "", "no_current_registry_match"),
    ("Fukuoka", "築城基地の米軍基地化を許さない！京築住民会議", "", "no_current_registry_match"),
    ("Fukuoka", "平和といのちをみつめる会", "", "no_current_registry_match"),
    ("Fukuoka", "戦争政権に反対し行動する実行委員会", "", "no_current_registry_match"),
    ("Fukuoka", "辺野古土砂ストップ北九州", "", "no_current_registry_match"),
    ("Kochi", "平和資料館・草の家", "", "no_current_registry_match"),
    ("Kochi", "須崎港の軍港化に反対する会", "", "no_current_registry_match"),
    ("Kochi", "郷土の軍事化に反対する高知県民ネットワーク", "", "no_current_registry_match"),
    ("Ehime", "ノーモア沖縄戦 えひめの会", "", "no_current_registry_match"),
    ("Hiroshima/Yamaguchi", "ピースリンク広島・呉・岩国", "", "no_current_registry_match"),
    ("Hiroshima", "市民運動交流センターふくやま", "", "no_current_registry_match"),
    ("Hiroshima", "日鉄呉跡地問題を考える会", "", "no_current_registry_match"),
    ("Osaka/Hyogo", "沖縄を再び戦場にさせない実行委員会", "", "no_current_registry_match"),
    ("Osaka", "リブインピース９＋２５", "", "no_current_registry_match"),
    ("Osaka", "平和を求め軍拡を許さない女たちの会・関西", "", "no_current_registry_match"),
    ("Osaka", "祝園弾薬庫 高槻・島本ネットワーク", "", "no_current_registry_match"),
    ("Osaka", "南京大虐殺６０カ年大阪実行委員会", "", "no_current_registry_match"),
    ("Kyoto", "反戦・反貧困・反差別共同行動 in 京都", "", "no_current_registry_match"),
    ("Kyoto", "米軍Ｘバンドレーダー基地反対・京都連絡会", "", "no_current_registry_match"),
    ("Nara", "いのちと平和を考える会", "", "no_current_registry_match"),
    ("Kyoto/Osaka/Nara", "京都・祝園ミサイル弾薬庫問題を考える住民ネットワーク", "", "no_current_registry_match"),
]


PETITION_ENDORSING_GROUPS = [
    ("Yonaguni", "与那国の明るい未来を願うイソバの会", "A016", "candidate_alias_match", "local_frontline_life_autonomy", "listed_endorser"),
    ("Ishigaki", "石垣島の平和と自然を守る市民連絡会", "A010", "reported_exact_rename_crosswalk_central_lifecycle_human_pending", "local_frontline_life_autonomy", "listed_endorser"),
    ("Ishigaki", "基地いらないチーム石垣", "", "no_current_registry_match", "local_frontline_life_autonomy", "listed_endorser"),
    ("Miyako", "ミサイル基地いらない宮古島住民連絡会", "A013", "exact_name", "local_frontline_life_autonomy", "listed_endorser"),
    ("Uruma", "ミサイル配備から命を守るうるま市民の会", "A100", "exact_name", "local_frontline_life_autonomy", "listed_endorser"),
    ("Okinawa", "沖縄平和サポート", "", "no_current_registry_match", "peace_antiwar_civic", "listed_endorser"),
    ("Okinawa", "沖縄平和市民連絡会", "A071", "likely_alias_match", "peace_antiwar_civic", "listed_endorser"),
    ("Okinawa", "沖縄県平和委員会", "", "no_current_registry_match", "peace_antiwar_civic", "listed_endorser"),
    ("Okinawa", "ノーモア沖縄戦 命どぅ宝の会", "A018", "exact_name", "peace_antiwar_civic", "listed_endorser;publisher_site_owner"),
    ("Okinawa/transnational", "沖縄・韓国民衆連帯", "", "no_current_registry_match", "transnational_human_rights", "listed_endorser"),
    ("Okinawa/international", "ＶＦＰ（平和を求める退役軍人の会）琉球・沖縄支部", "A070", "likely_alias_match", "transnational_human_rights", "listed_endorser"),
    ("Okinawa", "監視社会ならん！市民ネット沖縄", "", "no_current_registry_match", "transnational_human_rights", "listed_endorser"),
    ("Henoko", "あつまれ辺野古", "", "no_current_registry_match", "Henoko_local_anti_base", "listed_endorser"),
    ("Okinawa/international", "日中友好協会沖縄県支部", "", "no_current_registry_match", "transnational_human_rights", "listed_endorser"),
    ("Okinawa/Ryukyu Arc", "沖縄・琉球弧の声を届ける会", "A101", "exact_name", "peace_antiwar_civic", "listed_endorser"),
    ("Okinawa/transnational", "琉球・パレスチナの平和を求める会", "", "no_current_registry_match", "transnational_human_rights", "listed_endorser"),
    ("Okinawa", "沖縄県統一連", "A058", "likely_alias_match", "constitutional_political", "listed_endorser"),
    ("Okinawa", "NPO法人沖縄恨之碑の会", "", "no_current_registry_match", "transnational_human_rights", "listed_endorser"),
    ("Okinawa", "フェミブリッジ沖縄", "", "no_current_registry_match", "women_gender", "listed_endorser"),
    ("Futenma", "第３次普天間米軍基地爆音訴訟団", "A053", "round_specific_match", "legal_noise", "listed_endorser"),
    ("Kadena", "嘉手納ピースアクション", "", "no_current_registry_match", "peace_antiwar_civic", "listed_endorser"),
    ("Okinawa", "反基地ネット", "", "no_current_registry_match", "Henoko_local_anti_base", "listed_endorser"),
    ("Northern Okinawa", "八重岳を守る会", "", "no_current_registry_match", "Henoko_local_anti_base", "listed_endorser"),
    ("Motobu", "本部町島ぐるみ会議", "", "no_current_registry_match", "Henoko_local_anti_base", "listed_endorser"),
    ("Okinawa", "沖縄環境ネットワーク", "A056", "exact_name", "environment_health", "listed_endorser"),
    ("Okinawa", "新日本婦人の会沖縄県本部", "A115", "exact_name", "women_gender", "listed_endorser"),
    ("Urasoe", "浦添西海岸の未来を考える会", "", "no_current_registry_match", "environment_health", "listed_endorser"),
    ("Okinawa", "LandBack.Okinawa", "", "no_current_registry_match", "environment_health", "listed_endorser"),
    ("Okinawa", "沖縄県憲法普及協議会", "", "no_current_registry_match", "constitutional_political", "listed_endorser"),
    ("Haebaru", "南風原戦争させない有志の会", "", "no_current_registry_match", "peace_antiwar_civic", "listed_endorser"),
    ("Okinawa", "PFAS汚染から市民の命を守る連絡会", "A099", "likely_alias_match", "environment_health", "listed_endorser"),
    ("Okinawa", "沖縄YWCA", "A107", "exact_name", "peace_antiwar_civic", "listed_endorser"),
    ("Futenma", "普天間基地ゲート前でゴスペルを歌う会", "", "no_current_registry_match", "Henoko_local_anti_base", "listed_endorser"),
    ("Okinawa", "夜回りチーム結", "", "no_current_registry_match", "transnational_human_rights", "listed_endorser"),
    ("Okinawa/West Japan", "戦争止めよう！沖縄・西日本ネットワーク", "", "network_actor_candidate_not_in_registry", "cross_regional_carrier", "listed_endorser;cross_regional_network"),
]


THREE_ISLAND_REQUEST_SECTIONS = [
    (
        "RS01",
        "Yonaguni",
        "「与那国島について」",
        "3",
        "unknown",
        "unknown",
        "section_heading_and_request_text_only",
    ),
    (
        "RS02",
        "Ishigaki",
        "「石垣島について」",
        "9",
        "unknown",
        "unknown",
        "section_heading_and_request_text_only",
    ),
    (
        "RS03",
        "Miyako",
        "「宮古島について」",
        "6",
        "unknown",
        "unknown",
        "section_heading_and_request_text_only",
    ),
]


EVENT_SPEAKER_ATTRIBUTIONS = [
    (
        "SA01",
        "2024-03-06",
        "H3V2S019",
        "週刊かけはし",
        "尾形淳",
        "仲里（A013共同代表として報道）",
        "A013",
        "battlefield_prevention;dialogue",
        "speaker_specific_media_attribution",
        "Do not transfer other speakers' evacuation or life-safety remarks to A013.",
    ),
    (
        "SA02",
        "2024-03-06",
        "H3V2S019",
        "週刊かけはし",
        "尾形淳",
        "下地茜（宮古島市議として報道）",
        "",
        "evacuation;life_safety",
        "speaker_specific_media_attribution",
        "Individual speaker statement; no organization crosswalk or frame transfer.",
    ),
    (
        "SA03",
        "2024-03-06",
        "H3V2S019",
        "週刊かけはし",
        "尾形淳",
        "上里清美（発言者として報道）",
        "",
        "no_place_to_flee;life_safety",
        "speaker_specific_media_attribution",
        "Individual speaker statement; no organization crosswalk or frame transfer.",
    ),
]


ADOPTION_PANEL = [
    ("A018", "ノーモア沖縄戦 命どぅ宝の会", "Okinawa", "yes_attributed", "S023", "okinawa_war_memory;frontline_prevention;Taiwan_contingency", "media-attributed formation position", "core organizer"),
    ("A100", "ミサイル配備から命を守るうるま市民の会", "Uruma", "yes_attributed", "S119;H3V2S006", "frontline_prevention;Taiwan_contingency;life_safety", "media/request reproduction", "2025 listed participating group and 2026 endorser"),
    ("A101", "沖縄・琉球弧の声を届ける会", "Okinawa/Ryukyu Arc", "yes_organization_text", "S246", "new_prewar;frontline_prevention;human_rights", "organization event page", "2025 listed participating group and 2026 endorser"),
    ("A010", "石垣島に軍事基地をつくらせない市民連絡会", "Ishigaki", "yes_substantial_request_old_name", "H3V2S004;H3V2S005", "Taiwan_contingency;evacuation;diplomacy;local_autonomy", "old-name petition/request reproduction", "news reports exact rename; central lifecycle human-pending; pre-opening broad frame defeats installation-caused scale-shift inference"),
    ("A016", "与那国島の明るい未来を願うイソバの会", "Yonaguni", "unknown_in_this_pass", "", "", "dated participating-group list and later event only", "do not code absence as non-adoption"),
    ("", "大分敷戸ミサイル弾薬庫問題を考える市民の会", "Oita", "yes_organization_text", "H3V2S021;H3V2S022", "residential_safety;IHL;Sakishima_logistics;evacuation", "organization site and statement", "pre-existing local frame supports aggregation explanation"),
    ("", "京都・祝園ミサイル弾薬庫問題を考える住民ネットワーク", "Kyoto", "yes_secondary_attribution", "H3V2S010", "local_safety;anti_war;explanation_right", "formation material names co-chair; full own-text pair missing", "not sufficient for lexical adoption test"),
    ("A013", "ミサイル基地いらない宮古島住民連絡会", "Miyako", "media_attributed_not_organization_authored", "H3V2S007;H3V2S019", "battlefield_prevention;dialogue", "speaker-specific external media attribution", "absent from 2025 participating-group list; 2026 endorser; no transfer of other speakers' life-safety remarks"),
    ("", "ミサイル基地いらない住民連絡会（official-record surface form）", "Miyako", "official_request_submission_record_crosswalk_unresolved", "H3V2S020", "", "official minutes name a request/opinion submitter and responses", "exact A013 crosswalk and attendance unverified; no frame transfer"),
    ("", "ノーモア沖縄戦 えひめの会", "Ehime", "unknown_in_this_pass", "", "", "2025 listed group/co-chair only", "no own pre-network text found in bounded pass"),
    ("", "さつま町の弾薬庫問題を考える会", "Kagoshima", "unknown_in_this_pass", "", "", "2025 participating-group list only", "no own pre-network text found in bounded pass"),
    ("", "馬毛島基地反対住民訴訟原告団", "Kagoshima", "unknown_in_this_pass", "", "", "2025 participating-group list only", "no own pre-network text found in bounded pass"),
    ("", "日鉄呉跡地問題を考える会", "Hiroshima", "unknown_in_this_pass", "", "", "2024 contact sequence and 2025 participating-group list only", "no own matched text found in bounded pass"),
]


COMPARABLE_CORPUS = [
    ("HC01", "2010", "S003", "WWF Japan joint statement", "environmental_joint_statement", "Henoko", "environment;dugong;base", "single_project", "complete", "negative_control_genre"),
    ("HC02", "2015", "S004", "NACSJ joint statement", "environmental_joint_statement", "Henoko", "environment;coral;base", "single_project", "complete", "negative_control_genre"),
    ("HC03", "2016-05-22", "H3V2S001", "日本YWCA", "protest_statement", "Okinawa/national", "okinawa_war_memory;sexual_violence;bases", "base_system_in_Okinawa", "complete", "older_memory_baseline"),
    ("HC04", "2017-02-28", "S036", "four reported civic groups", "government_request_event", "Sakishima", "evacuation;life_safety;frontline_prevention", "cross_island_deployment", "attributed", "older_carrier_baseline"),
    ("HC05", "2019", "H3V2S004", "old-name A010 petition account", "online_petition", "Ishigaki", "nature;peace;security", "single_installation", "ownership_candidate", "pre_installation_old_name"),
    ("HC06", "2020", "S006", "OEJP/MMC request", "international_environment_request", "Henoko/international", "environment;dugong;international_advocacy", "single_project", "complete", "negative_control_genre"),
    ("HC07", "2021-06", "H3V2S002", "Tokyo YWCA newsletter contributor", "newsletter_article", "national/Okinawa/Sakishima", "okinawa_war_memory;war_remains;again_battlefield", "Henoko_plus_Sakishima_buildup", "complete_named_author", "national_memory_bridge"),
    ("HC08", "2021-07", "H3V2S003", "Japan Gensuikyo conference speaker", "conference_text", "national/Sakishima", "Taiwan_contingency;Sakishima_battlefield;nuclear_risk", "regional_security_system", "complete_named_speaker", "national_anti_nuclear_bridge"),
    ("HC09", "2022-03-21", "S023", "A018", "formation_report", "Okinawa/Sakishima", "okinawa_war_memory;Taiwan_contingency;frontline_prevention", "island_chain_operations", "attributed", "pre_network_independent"),
    ("HC10", "2022-11-29", "S119", "A100", "formation_report", "Uruma/Sakishima", "Taiwan_contingency;frontline_prevention;life_safety", "missile_deployment_and_island_chain", "attributed_archive_gate", "pre_network_independent"),
    ("HC11", "2022-12-07", "S022", "A017", "organization_program", "Okinawa/Taiwan", "okinawa_war_memory;sacrificial_island;dialogue", "regional_conflict_risk", "complete_metadata_gate", "pre_network_independent"),
    ("HC12", "2023-02-09", "H3V2S005", "old-name A010", "request_reproduced_by_party_press", "Ishigaki", "Taiwan_contingency;evacuation;diplomacy;autonomy", "installation_plus_evacuations", "substantial_reproduction_original_pending", "pre_network_old_name"),
    ("HC13", "2023-02-25", "H3V2S006", "A100", "request_reproduced", "Uruma", "okinawa_war_memory;attack_target;life_safety", "missile_deployment", "substantial_reproduction", "pre_network_independent"),
    ("HC14", "2023-07", "S146", "A108", "organization_program", "Okinawa prefecture", "anti_war;frontline_prevention;peace", "prefectural_military_buildup", "organization_site", "prefectural_carrier"),
    ("HC15", "2023-08 onward", "H3V2S021", "Oita Shikido group", "organization_site", "Oita", "anti_war;residential_safety;diplomacy", "missile_depot", "complete_site", "pre_network_independent"),
    ("HC16", "2023-11-12", "S246", "A101", "organization_event_text", "Ryukyu Arc", "new_prewar;frontline_prevention;human_rights", "island_chain_buildup", "complete", "pre_network_independent"),
    ("HC17", "2023-12-28", "H3V2S022", "Oita Shikido group", "protest_statement", "Oita/Sakishima", "IHL;residential_safety;evacuation", "depot_transport_Sakishima_logistics", "complete_copy", "pre_network_independent"),
    ("HC18", "2024-03-06", "H3V2S019", "A013 co-representative attributed by movement press", "protest_event_report", "Miyako", "battlefield_prevention;dialogue", "local_base_and_training", "speaker_specific_media_attribution_not_organization_authored", "A013_frame_only_other_speakers_separate"),
    ("HC19", "2024-10-02", "H3V2S020", "similar-name Miyako entity in official minutes", "official_request_submission_record", "Miyako", "opinion_and_request_submission", "base_expansion_and_training", "complete_official_crosswalk_unresolved", "not_attendance_not_A013_frame"),
    ("HC20", "2025-02-22", "H3V2S009", "formation-declaration document; drafter unknown", "formation_declaration", "Okinawa/West Japan/national", "anti_war;war_memory;life_safety;rights;environment", "bases_missiles_depots_ports_airports_roads_transport_evacuation", "complete_document_drafter_unknown", "common_document_frame_and_object_not_group_adoption"),
    ("HC21", "2025-02-22", "H3V2S010", "Okinawa-West Japan Network", "governance_proposal", "Okinawa/West Japan", "coordination;information_sharing;joint_action", "regional_military_buildup", "complete", "formal_carrier"),
    ("HC22", "2025-03-22", "H3V2S017", "source-reported renamed Ishigaki organization; central lifecycle human-pending", "solidarity_statement_report", "Ishigaki/Kyushu/Japan", "attack_target;life_safety;solidarity", "long_range_missile_distribution", "reported_substantial", "reported_rename_no_installation_caused_change"),
    ("HC23", "2025-05-06", "H3V2S011", "Okinawa-West Japan Network", "dated_participating_group_list", "Okinawa/West Japan", "participating_or_constituent_groups_as_listed", "cross_regional_action_carrier", "complete", "as_of_list_not_membership"),
    ("HC24", "2025-06-06", "H3V2S013", "Okinawa-West Japan Network", "government_negotiation", "national government", "explanation_right;depot_safety;missile_deployment", "distributed_policy_nodes", "independent_report", "repeat_action_1"),
    ("HC25", "2026-01-26", "H3V2S014", "Okinawa-West Japan Network", "government_negotiation", "national government", "budget;missiles;depots;exercises;evacuation;resident_response", "distributed_policy_nodes", "independent_report", "repeat_action_2"),
    ("HC26", "2026-03-24", "H3V2S018", "source-reported renamed Ishigaki organization; central lifecycle human-pending", "local_statement_report", "Ishigaki", "anti_training;public_access", "post_installation_operation", "reported", "continued_local_action_no_scale_shift_inference"),
    ("HC27", "2026-05-07 submission / 2026-05-16 publication", "H3V2S023", "common petition document / 35 endorsing groups", "joint_petition", "three island request sections; four-place action context", "frontline_prevention;Taiwan_contingency;autonomy;life_safety;environment;rights", "bases_missiles_depots_ports_airports_roads_exercises_evacuation", "complete_common_text_text_ownership_unresolved", "three_island_requests_four_place_event_hyperedge"),
    ("HC28", "2026-05-09", "H3V2S024", "party-press report of four-place action", "event_report", "Yonaguni/Ishigaki/Miyako/Okinawa main island", "frontline_prevention;life_safety;diplomacy", "four_place_action", "external_party_report", "event_occurrence_and_first_action_attribution"),
]


FRAME_OBJECT_OBSERVATIONS = [
    guarded(
        {
            "observation_id": "FO01",
            "date": "2024-03-06",
            "source_id": "H3V2S019",
            "actor_or_event": "A013 / Miyako protest (media attribution)",
            "text_ownership_status": "external_media_attribution_not_organization_authored",
            "common_frame": "媒体归因给 A013 共同代表：防止战场化；对话",
            "common_object": "宫古驻屯地、训练、弹药库与本地生活",
            "object_scale": "local_installation_and_operations",
            "formal_common_organization_status": "not_listed_in_2025_35_participating_group_list",
            "interpretation_limit": "This is speaker-specific media attribution, not an organization-authored text. Evacuation/life-safety remarks by other speakers cannot be transferred to A013; dated-list absence is not permanent non-participation.",
        }
    ),
    guarded(
        {
            "observation_id": "FO02",
            "date": "2025-02-22",
            "source_id": "H3V2S009",
            "actor_or_event": "formation-declaration document; drafter unknown",
            "text_ownership_status": "formation_declaration_document_drafter_unknown",
            "common_frame": "反战；冲绳战记忆；生活、人权、环境；拒绝疏开",
            "common_object": "基地、导弹、弹药库、住宅邻接、港机场、公路、运输、避难",
            "object_scale": "distributed_war_preparation_system",
            "formal_common_organization_status": "formal_action_carrier_common_document",
            "interpretation_limit": "The formation-declaration document constructs this object at document level. Its drafter, participating groups' independent adoption and governance execution are unproven.",
        }
    ),
    guarded(
        {
            "observation_id": "FO03",
            "date": "2025-03-22",
            "source_id": "H3V2S017",
            "actor_or_event": "source-reported renamed Ishigaki organization statement; central lifecycle human-pending",
            "text_ownership_status": "reported_statement_text_not_directly_archived",
            "common_frame": "攻击目标；居民生命财产；反长射程导弹",
            "common_object": "从石垣驻屯地上移到九州乃至日本各地的导弹部署",
            "object_scale": "cross_regional_distribution",
            "formal_common_organization_status": "source_reported_rename_central_lifecycle_human_pending",
            "interpretation_limit": "One reported statement does not prove organizational frame change; old-name A010 already used a broad frame before the garrison opened.",
        }
    ),
    guarded(
        {
            "observation_id": "FO04",
            "date": "2026-05-07 submission; 2026-05-16 publication",
            "source_id": "H3V2S023",
            "actor_or_event": "common petition document / four-place action",
            "text_ownership_status": "publisher_page_complete_text_drafting_contributions_unresolved",
            "common_frame": "共同文件：冲绳作为前线的战争准备；外交；自治与生活安全",
            "common_object": "共同文件并置全岛军事节点，并分列与那国、石垣、宫古三个地方请求段",
            "object_scale": "four_place_hyperedge_with_distributed_system",
            "formal_common_organization_status": "event_co_signing_not_stable_alliance",
            "interpretation_limit": "Four-place speaking/action is an attributed event hyperedge; only three island-specific request sections exist. Text ownership and independent adoption remain separate.",
        }
    ),
]


ISHIGAKI_LIFECYCLE_CANDIDATE_STAGES = [
    ("LC01", "2015-08-20", "old-name A010", "A010 predecessor core forms", "prevent_planned_installation", "single proposed facility", "central HR-012", "confirmed_old_name_A010", "historical lifecycle anchor"),
    ("LC02", "2016-09", "old-name A010", "A010 wider liaison coalition forms", "prevent_planned_installation", "local coalition and decision process", "central HR-012", "confirmed_old_name_A010", "not a simple rename"),
    ("LC03", "2023-03-16", "external policy event", "Ishigaki garrison opens", "installation_becomes_operational", "opened facility", "external official/news baseline", "not_an_organization_identity_observation", "policy event, not an NGO action"),
    ("LC04", "2023-04-15", "source-reported renamed organization", "news reports a general-meeting rename from old-name A010 to the new name", "reported_exact_rename_source_layer", "organization identity/name", "H3V2S015;H3V2S025", "reported_exact_rename_central_lifecycle_human_pending", "Source-level exact rename is retained, but it conflicts with HR-012 and cannot write central canonical/alias/lifecycle without human reconciliation."),
    ("LC05", "2023-04-28 / reported 2023-04-30", "source-reported renamed organization", "new-name organization issues PAC3 statement; partial representative turnover reported", "post_rename_public_action", "local operations and war-preparation critique", "H3V2S025;H3V2S016", "reported_exact_rename_central_lifecycle_human_pending", "Old-name A010 already used Taiwan/evacuation/diplomacy framing on 2023-02-09, before the garrison opened; no installation-caused scale-shift inference."),
    ("LC06", "2025-03-22", "source-reported renamed organization", "statement opposing Kyushu long-range missile deployment", "cross_regional_solidarity", "distributed missile deployment beyond Ishigaki", "H3V2S017", "reported_exact_rename_central_lifecycle_human_pending", "One reported statement does not establish an installation-caused before/after organizational change."),
    ("LC07", "2025-05-06", "source-reported renamed organization", "listed as participating/constituent group; Fujii named regional operator", "formal_action_carrier_participation_candidate", "Okinawa-West Japan action carrier", "H3V2S010;H3V2S011", "reported_exact_rename_central_lifecycle_human_pending", "As-of listing and proposed role do not prove retention or governance execution; central lifecycle remains human-pending."),
    ("LC08", "2026-03-24", "source-reported renamed organization", "protest against local garrison public event reported", "post_installation_local_monitoring", "local facility operations", "H3V2S018", "reported_exact_rename_central_lifecycle_human_pending", "Continued action does not establish size, representativeness or installation-caused scale shift."),
    ("LC09", "2026-05-07 submission / 2026-05-16 publication", "source-reported renamed organization", "new-name entity is an endorser; the petition contains an Ishigaki request section whose drafter is unknown", "event_level_multi_scalar_document", "local request plus common-document distributed object", "H3V2S023;H3V2S024", "reported_exact_rename_central_lifecycle_human_pending", "Endorsement does not prove section authorship, stable alliance or organizational scale shift; central lifecycle remains human-pending."),
]


EVENT_SEQUENCE = [
    ("EV01", "2017-02-28", "Sakishima", "four-group government negotiation", "event_contact", "S036", "independent_news", "older cross-island baseline"),
    ("EV02", "2023-11-23", "Okinawa", "prefectural peace rally", "claimed_trigger", "H3V2S011;H3V2S012", "organizer_self_attribution", "trigger is not causal proof"),
    ("EV03", "2024-04-21", "Ehime", "regional exchange/action", "contact_sequence", "H3V2S011", "organizer_self_narrative", "participant roster incomplete"),
    ("EV04", "2024-08-11", "Okinawa", "cross-regional exchange", "contact_sequence", "H3V2S011", "organizer_self_narrative", "participant roster incomplete"),
    ("EV05", "2024-09-21", "Hiroshima/Kure", "cross-regional exchange", "contact_sequence", "H3V2S011", "organizer_self_narrative", "participant roster incomplete"),
    ("EV06", "2024-11-30", "Oita", "cross-regional exchange", "contact_sequence", "H3V2S011", "organizer_self_narrative", "participant roster incomplete"),
    ("EV07", "2025-02-22", "Kagoshima/Satsuma", "formal action carrier formation", "formal_action_carrier", "H3V2S009;H3V2S010", "organization_primary", "governance is proposed; execution and network identity pending HR"),
    ("EV08", "2025-04-20", "Fukuoka/Tsuiki", "regional exchange/action", "contact_sequence", "H3V2S011", "organizer_self_narrative", "participant roster incomplete"),
    ("EV09", "2025-05-06", "Okinawa/West Japan", "35 participating/constituent groups as listed", "dated_participating_group_claim", "H3V2S011", "organization_primary", "as-of listing is not legal membership, retention, active role or dyadic alliance"),
    ("EV10", "2025-06-06", "Tokyo", "first government negotiation", "repeat_formal_action_1", "H3V2S013", "independent_report", "200 attendance report is event-specific"),
    ("EV11", "2026-01-26", "Tokyo", "second government negotiation", "repeat_formal_action_2", "H3V2S014", "independent_report", "38 groups not comparable growth without roster"),
    ("EV12", "2026-05-07 submission; 2026-05-16 publication", "Yonaguni/Ishigaki/Miyako/Okinawa main island", "three island-specific requests in a four-place action", "event_hyperedge", "H3V2S023;H3V2S024", "publisher_plus_party_press_attribution", "the 'first' description is attributed; four-place speaking/action differs from three island-specific request sections"),
]


NEGATIVE_CONTROLS = [
    guarded(
        {
            "control_id": "NC01",
            "date": "2010",
            "source_id": "S003",
            "control_type": "complete_text_genre_negative",
            "matched_dimension": "joint statement / Henoko / environmental organizations",
            "observed": "No hits for Taiwan, contingency, Okinawa war, battlefield, frontline or evacuation in the archived text scan.",
            "valid_inference": "This environmental statement uses a different issue grammar.",
            "invalid_inference": "The target vocabulary was absent from Okinawan civil society in 2010.",
        }
    ),
    guarded(
        {
            "control_id": "NC02",
            "date": "2015",
            "source_id": "S004",
            "control_type": "complete_text_genre_negative",
            "matched_dimension": "joint statement / Henoko / environmental organizations",
            "observed": "No hits for Taiwan, contingency, Okinawa war, battlefield, frontline or evacuation in the archived text scan.",
            "valid_inference": "This environmental statement uses a different issue grammar.",
            "invalid_inference": "The target vocabulary was absent from Okinawan civil society in 2015.",
        }
    ),
    guarded(
        {
            "control_id": "NC03",
            "date": "2020",
            "source_id": "S006",
            "control_type": "complete_text_genre_negative",
            "matched_dimension": "international request / Henoko / environmental organizations",
            "observed": "No English hits for Taiwan, battlefield, frontline, war, evacuation or militarization in the archived text scan.",
            "valid_inference": "The international dugong request uses an environmental/legal grammar.",
            "invalid_inference": "Target vocabulary had not grown by 2020.",
        }
    ),
    guarded(
        {
            "control_id": "NC04",
            "date": "2016",
            "source_id": "H3V2S001",
            "control_type": "older_memory_without_distributed_object",
            "matched_dimension": "national women organization / Okinawa / protest statement",
            "observed": "War memory is linked to bases and sexual violence, without the later port-airport-depot-evacuation system.",
            "valid_inference": "War memory predates the recent carrier; the contribution can only be operationalization and role separation, not discovery of the discourse.",
            "invalid_inference": "National war-memory discourse and Sakishima life-safety discourse are identical.",
        }
    ),
    guarded(
        {
            "control_id": "NC05",
            "date": "2023",
            "source_id": "H3V2S022",
            "control_type": "independent_local_convergence",
            "matched_dimension": "pre-network West Japan local statement",
            "observed": "Oita independently connects residential danger, IHL, Sakishima logistics and evacuation before formal network formation.",
            "valid_inference": "Aggregation of existing local frames is at least as plausible as diffusion from Okinawa.",
            "invalid_inference": "Similarity proves no interpersonal transmission occurred.",
        }
    ),
    guarded(
        {
            "control_id": "NC06",
            "date": "2024/2025/2026",
            "source_id": "H3V2S019;H3V2S011;H3V2S023",
            "control_type": "media_attributed_common_frame_without_dated_participating_group_listing",
            "matched_dimension": "same Miyako organization across media attribution, dated list and later event",
            "observed": "Media attributes battlefield/dialogue framing to Miyako organizers; the group is absent from the dated 2025 35-group list and appears as a 2026 endorser.",
            "valid_inference": "Attributed language, dated participating-group listing and one event role are distinct dimensions.",
            "invalid_inference": "The 2025 list absence proves rejection or non-participation at all later dates.",
        }
    ),
]


ACADEMIC_LINKS = [
    ("AL01", "比嘉盛人", "2023", "「沖縄を再び戦場にさせない県民の会」の設立と11・23県民平和大集会", "けーし風 119:17-22", "https://ndlsearch.ndl.go.jp/books/R000000004-I033183383", "metadata_only_no_online_full_text", "direct case literature; required to position the operationalization and role distinctions", "Request NDL/local copy; do not claim topic or mechanism novelty."),
    ("AL02", "門野里栄子", "2009", "Relaying and Handing Down of the Experience of an Untold Story", "Japan Oral History Association 5:63-71", "https://www.jstage.jst.go.jp/article/jjoha/5/0/5_KJ00005927936/_article/-char/en", "abstract_reviewed", "war memory is reconstructed in activist subject formation, not simply inherited", "Use for memory mechanism, not diffusion evidence."),
    ("AL03", "大野光明", "2016", "Dynamics of Problematizing Okinawa", "Japanese Sociological Review 67(4):415-431", "https://www.jstage.jst.go.jp/article/jsr/67/4/67_415/_article/-char/en", "abstract_reviewed", "historical analogue of cross-regional carriers translating local harm into an Okinawa problem", "Prevents claiming cross-regional linkage is wholly new."),
    ("AL04", "新崎盛暉", "1999", "Okinawa's Anti-Base Protests and the Creation of Peace in East Asia", "International Relations 120:109-119", "https://www.jstage.jst.go.jp/article/kokusaiseiji1957/1999/120/1999_120_109/_article", "abstract_reviewed", "historical baseline of transnational and mainland cooperation", "Recent carrier may be a new form, not the first external linkage."),
    ("AL05", "大野光明", "2019", "基地・軍隊をめぐる概念・認識枠組みと軍事化の力学", "環境社会学研究 25:35-50", "https://www.jstage.jst.go.jp/article/jpkankyo/25/0/25_35/_article/-char/ja", "abstract_reviewed", "military harm crosses wartime/peacetime, environment, rights and autonomy", "Supports object-bundling lens, not empirical adoption."),
    ("AL06", "比嘉理麻", "2024", "沖縄の基地反対運動と命のアナキズム", "文化人類学 89(1):22-41", "https://www.jstage.jst.go.jp/article/jjcanth/89/1/89_022/_article/-char/ja", "abstract_reviewed", "movement subject/object can expand after limits of conventional opposition", "Useful comparison for object transformation."),
    ("AL07", "熊本博之", "2024", "沖縄に「平和」をもたらす「自立」の実現に向けて", "平和研究 61:1-22", "https://www.jstage.jst.go.jp/article/psaj/61/0/61_610111/_article/-char/ja/", "abstract_reviewed", "mainland peace discourse can erase Okinawan positionality", "Use as a check against mainland-centered common-language claims."),
    ("AL08", "中林啓修", "2024", "沖縄・南西地域における国民保護の課題", "防衛学研究 71:7-28", "https://www.jstage.jst.go.jp/article/jds/2024/71/2024_7/_article/-char/ja", "abstract_and_first_page_reviewed", "official/academic civil-protection frame for comparison with civic evacuation critique", "Official problem setting is not civic adoption."),
    ("AL09", "野添文彬", "2024", "日本の安全保障と沖縄―特集にあたって―", "防衛学研究 71", "https://www.jstage.jst.go.jp/article/jds/2024/71/2024_1/_pdf", "intro_excerpt_reviewed", "security-policy discourse bundles Okinawa history, public opinion and national security", "Counter-discourse, not civic evidence."),
    ("AL10", "桐山節子", "2023", "沖縄の軍事基地に抗する人々と地域", "同志社大学人文科学研究所紀要", "https://cir.nii.ac.jp/crid/1390576966668638592", "abstract_reviewed", "organizationally based activity can shift toward individual activity", "Competing explanation for roster/personnel continuity."),
    ("AL11", "福間良明", "2016", "war memory and dehistoricization", "mass communication studies", "https://www.jstage.jst.go.jp/article/mscom/88/0/88_KJ00010233527/_article/-char/en", "metadata_or_abstract_only", "memory inheritance can flatten historical complexity", "Caution against treating war memory as one stable national code."),
    ("AL12", "author metadata pending", "2016", "Principle of Renunciation of War and Strengthening the Self-Defense Forces", "沖縄大学地域研究 18:1-24", "https://cir.nii.ac.jp/crid/1390290701858194304", "abstract_reviewed", "older Sakishima militarization scholarship", "Read full text before claiming the recent frame is new."),
]


SEARCH_LOG = [
    ("SL01", "2026-07-20", "formal cross-regional action carrier", "戦争止めよう 沖縄 西日本 ネットワーク 結成 参加団体", "official site, declaration, governance proposal and dated 35 participating-group list found", "closed_for_v2"),
    ("SL02", "2026-07-20", "repeat formal action", "沖縄 西日本 ネットワーク 政府交渉 2025 2026", "2025 first action and 2026 second action found in two external reports", "closed_for_v2"),
    ("SL03", "2026-07-20", "source-reported A010 rename / central lifecycle conflict", "石垣島 市民連絡会 名称変更 平和と自然", "Okinawa Times and Ryukyu Shimpo report an exact 2023-04-15 general-meeting rename; central HR-012 lifecycle remains human-pending", "human_reconciliation_required"),
    ("SL04", "2026-07-20", "new-name Ishigaki public-action sequence", "石垣 長射程 九州 沖縄西日本 連帯 声明", "2025 cross-regional statement and 2026 local action found; no identity or before/after change inference", "closed_descriptive_only"),
    ("SL05", "2026-07-20", "Miyako boundary", "宮古島 戦場 話し合い ミサイル基地 2024", "2024 report split by speaker; official minutes show a similar-name request submitter, not attendance or an exact A013 crosswalk", "organization_authored_text_still_missing"),
    ("SL06", "2026-07-20", "three-island request / four-place event hyperedge", "沖縄 最前線 戦争準備 請願 与那国 石垣 宮古", "petition with three island-specific sections whose drafters/representative organizations are unknown, 35 endorsers, 5/7 action and 5/16 publication plus external four-place event report found", "human_role_crosswalk_required"),
    ("SL07", "2026-07-20", "national memory baseline", "site:ywca.or.jp 沖縄 戦場 基地 声明", "2016 Japan YWCA statement found", "closed_for_v2"),
    ("SL08", "2026-07-20", "national anti-nuclear bridge", "site:antiatom.org 台湾有事 南西諸島 戦場", "2021 conference speaker text found", "speaker_not_whole_organization"),
    ("SL09", "2026-07-20", "West Japan independent adoption", "大分 敷戸 ミサイル 弾薬庫 市民の会 声明", "organization site and 2023 complete statement found", "closed_for_v2"),
    ("SL10", "2026-07-20", "direct academic case", "site:ndlsearch.ndl.go.jp 沖縄を再び戦場にさせない県民の会", "Higa 2023 article metadata found; no online full text", "local_or_NDL_copy_required"),
    ("SL11", "2026-07-20", "academic carrier analogue", "site:jstage.jst.go.jp 沖縄 市民運動 ネットワーク 公害", "Ono 2016 and historical cross-regional literature found", "principal_reading_required"),
    ("SL12", "2026-07-20", "official counter-frame", "site:jstage.jst.go.jp 沖縄 南西 国民保護", "Nakabayashi 2024 civil-protection article found", "principal_reading_required"),
    ("SL13", "2026-07-20", "listed-group own-text panel", "沖西ネット 参加団体 names + 声明/要請/公式", "organization text found for A101 and Oita; old-name A010 text cannot be transferred to the new-name listed group without lifecycle review", "bounded_stop_missing_not_negative"),
    ("SL14", "2026-07-20", "older complete-text controls", "local archive exact-term scan S003/S004/S006", "target-term non-hits recorded for three complete environmental documents", "genre_bounded_only"),
]


HUMAN_REVIEW_QUEUE = [
    ("H3HR01", "network identity", "Decide whether 戦争止めよう！沖縄・西日本ネットワーク is a new actor and assign scope/class.", "H3V2S008;H3V2S009;H3V2S010", "No central actor before decision.", "high"),
    ("H3HR02", "dated participating-group list", "Review all 35 参加／構成団体 claims as-of 2025-05-06 and five Okinawa registry crosswalks.", "H3V2S011", "A dated listing is not legal membership, retention, governance execution or dyadic alliance.", "high"),
    ("H3HR03", "three-island request / four-place event", "Review 35 endorsers while keeping publisher, three section headings with unknown drafters/representative organizations, four-place speakers/action participants and endorsers distinct.", "H3V2S023;H3V2S024", "No A016/A010/A013 section-authorship inference; event hyperedge only; 'first' is attributed; no stable alliance.", "high"),
    ("H3HR04", "A010 source-reported rename / central lifecycle conflict", "Reconcile the two news reports of a 2023-04-15 exact rename with HR-012, then decide central canonical/alias/lifecycle fields.", "H3V2S015;H3V2S025;H3V2S016", "Retain the source-level reported rename; do not write it directly into central before human reconciliation.", "high"),
    ("H3HR05", "Ishigaki no-scale-shift boundary", "Confirm that old-name A010 already used Taiwan/evacuation/diplomacy framing before the 2023-03-16 garrison opening.", "H3V2S005;H3V2S025;H3V2S017;H3V2S018;H3V2S023", "Do not restore an installation-caused A010 scale-shift claim, regardless of the lifecycle decision.", "high"),
    ("H3HR06", "Miyako boundary", "Confirm A013 absence from the 2025 list and later endorser status; review speaker-specific attributions and the similar-name official request-submission record; obtain organization-authored text.", "H3V2S011;H3V2S019;H3V2S020;H3V2S023", "A013 gets battlefield/dialogue only; other speakers' evacuation/life-safety statements and the official-record entity cannot be transferred.", "medium"),
    ("H3HR07", "list overlap", "Review 2023/2025/2026 normalized names and role-specific overlap.", "S246;H3V2S011;H3V2S023", "Host/endorser/participating-group/petition-endorser roles must remain distinct; A016 and A010 links are conditional.", "medium"),
    ("H3HR08", "formation sequence", "Decide how to phrase the 2023 rally as a claimed trigger.", "H3V2S011;H3V2S012", "Use organizer self-attribution, not causal diffusion.", "medium"),
    ("H3HR09", "repeat action/counts", "Review 2025 and 2026 government actions and whether 35/38 group counts are comparable.", "H3V2S013;H3V2S014", "Do not call 35→38 retention or growth without comparable lists.", "medium"),
    ("H3HR10", "academic positioning", "Read Higa 2023, Ono 2016 and Kumamoto 2024 to position the operationalization and role distinctions.", "AL01;AL03;AL07", "Metadata/abstract scan is not a literature review; no topic/mechanism novelty claim.", "high"),
    ("H3HR11", "source governance carryover", "Resolve S022/S036 metadata and S119 archive/date gates inherited from H3 v1.", "S022;S036;S119", "Do not silently normalize in this package.", "medium"),
]


LOCAL_RETRIEVAL_QUEUE = [
    ("H3LR01", "比嘉盛人 2023 full article", "NDL/local library copy of けーし風 119 pp.17-22", "direct formation mechanism and participant account", "AL01"),
    ("H3LR02", "A010 rename records and central lifecycle reconciliation", "2023-04-15 general-meeting minutes/resolution, flyers and participant circulars", "reconcile the source-reported exact rename with HR-012 central lifecycle; not to revive an installation-caused scale-shift test", "H3HR04;H3HR05"),
    ("H3LR03", "Miyako own texts", "A013 requests/newsletters around 2024-2026 and participation correspondence", "separate media-attributed language from organization-authored language and dated participation", "H3HR06"),
    ("H3LR04", "network dated lists/minutes", "formation minutes and participating-group lists for 2025-02, 2025-05 and 2026-01", "retention, governance execution and division-of-labor test", "H3HR02;H3HR09"),
    ("H3LR05", "2024 exchange programs", "full programs/participant lists for Ehime, Okinawa, Kure and Oita exchanges", "turn self-narrated sequence into comparable event hyperedges", "H3HR08"),
]


ROSTER_2023 = {
    "A101": "沖縄・琉球弧の声を届ける会（host）",
    "A055": "泡瀬干潟を守る連絡会",
    "A056": "沖縄環境ネットワーク",
    "A071": "沖縄平和市民連絡会",
    "KADENA_PEACE_ACTION": "嘉手納ピースアクション",
    "A049": "基地・軍隊を許さない行動する女たちの会",
    "A002": "ジュゴン保護キャンペーンセンター",
    "JCJ": "日本ジャーナリスト会議",
    "JCJ_OKINAWA": "日本ジャーナリスト会議沖縄",
    "A018": "ノーモア沖縄戦 命どぅ宝の会",
    "A019": "ヘリ基地反対協議会",
    "A100": "ミサイル配備から命を守るうるま市民の会",
    "A099": "PFAS汚染から市民の命を守る連絡会",
    "OKUMA_FUND": "NPO法人奥間川流域保護基金",
}


def listed_entity_key(name: str, actor_id: str, crosswalk_status: str) -> str:
    if actor_id == "A016":
        return "CANDIDATE_ALIAS_A016"
    if actor_id == "A010":
        return "CANDIDATE_LIFECYCLE_A010"
    if actor_id:
        return actor_id
    return {
        "沖縄平和市民連絡会": "OKINAWA_PEACE_CITIZENS",
        "嘉手納ピースアクション": "KADENA_PEACE_ACTION",
    }.get(name, f"NAME::{name}")


def participating_groups_2025() -> dict[str, str]:
    return {
        listed_entity_key(name, actor_id, crosswalk_status): name
        for _, name, actor_id, crosswalk_status in NETWORK_PARTICIPATING_GROUPS
    }


def endorsing_groups_2026() -> dict[str, str]:
    return {
        listed_entity_key(name, actor_id, crosswalk_status): name
        for _, name, actor_id, crosswalk_status, _, _ in PETITION_ENDORSING_GROUPS
    }


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> int:
    materialized = list(rows)
    if not materialized:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in materialized:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(materialized)
    return len(materialized)


def svg_text(x: int, y: int, text: str, *, size: int = 14, weight: int = 400, fill: str = "#17202a", anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Noto Sans CJK SC, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f"{escape(text)}</text>"
    )


def render_timeline(path: Path) -> None:
    width, height = 2200, 930
    lane_y = {
        "local": 245,
        "contact": 410,
        "formal": 575,
        "joint": 740,
    }
    events = [
        (2017.16, "local", "2017\n先岛四团体\n政府交涉", "#537895"),
        (2022.25, "local", "2022\nA018/A017/A100\n独立公开框架", "#537895"),
        (2023.30, "local", "2023\nA010部署前请求\n台湾／避难／外交", "#537895"),
        (2023.90, "contact", "2023.11\n冲绳县民集会\n（组织方称“契机”）", "#d08c3f"),
        (2024.25, "local", "2024\n宫古媒体归因：\n战场化／对话", "#537895"),
        (2024.55, "contact", "2024\n爱媛→冲绳→吴→大分\n交流序列（自述）", "#d08c3f"),
        (2025.15, "formal", "2025.2\n行动载体成立\n治理方案＋宣言", "#8b5ea7"),
        (2025.36, "formal", "2025.5\n35参加／构成团体\n截至5月6日", "#8b5ea7"),
        (2025.48, "formal", "2025.6\n第一次政府交涉", "#8b5ea7"),
        (2026.08, "formal", "2026.1\n第二次政府交涉", "#8b5ea7"),
        (2026.35, "joint", "2026.5\n5/7提交·四地行动\n5/16发布·三岛请求", "#2d8f75"),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fbfaf7"/>',
        svg_text(50, 48, "从地方材料到正式跨区域行动载体：证据序列（不是扩散方向图）", size=25, weight=700),
        svg_text(50, 78, "每条只表示可核文本／事件；组织方所称“契机”保留为自我叙述，事件共现不等于联盟。", size=14, fill="#566573"),
        svg_text(50, 103, "横向按事件顺序等距排列，日期写在卡片内；间距不表示实际时间长度。", size=13, fill="#7b7d7d"),
    ]
    labels = {
        "local": "地方独立框架／行动",
        "contact": "跨地接触（名册不全）",
        "formal": "正式行动载体／重复行动",
        "joint": "共同事件超边",
    }
    for lane, y in lane_y.items():
        parts.append(f'<line x1="310" y1="{y}" x2="2140" y2="{y}" stroke="#d5d8dc" stroke-width="2"/>')
        parts.append(svg_text(285, y + 5, labels[lane], size=14, weight=600, anchor="end"))
    parts.append('<line x1="330" y1="128" x2="2115" y2="128" stroke="#aeb6bf" stroke-width="1.5"/>')
    parts.append('<path d="M2115 128 L2102 121 L2102 135 Z" fill="#aeb6bf"/>')
    parts.append(svg_text(330, 120, "2017", size=13, fill="#566573", anchor="middle"))
    parts.append(svg_text(2115, 120, "2026", size=13, fill="#566573", anchor="middle"))
    for idx, (year, lane, label, color) in enumerate(events):
        # Equal spacing keeps the dense 2023–2025 sequence legible. The date
        # stays in each card; horizontal distance is ordinal, not duration.
        x = 350 + idx * 170
        y = lane_y[lane]
        above = idx % 2 == 0
        box_y = y - 92 if above else y + 20
        lines = label.split("\n")
        box_h = 22 + len(lines) * 18
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        stem_to = box_y + box_h if above else box_y
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{stem_to}" stroke="{color}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x - 77}" y="{box_y}" width="154" height="{box_h}" rx="8" fill="#ffffff" stroke="{color}" stroke-width="1.5"/>')
        for line_idx, line in enumerate(lines):
            parts.append(svg_text(x, box_y + 22 + line_idx * 18, line, size=12, weight=600 if line_idx == 0 else 400, anchor="middle"))
    parts.extend(
        [
            svg_text(50, 875, "可支持：行动载体至少持续到2026初；2025宣言与2026请愿在共同文件层并置分布式对象。", size=15, weight=700, fill="#21618c"),
            svg_text(50, 903, "不可支持：治理全部执行、参加团体留存／独立采用、组织前后对象变化、单向扩散或稳定联盟。", size=15, weight=700, fill="#922b21"),
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def render_overlap(path: Path, overlap_rows: list[dict[str, str]]) -> None:
    width, height = 1260, 720
    sets = [
        ("2023 A101活动", 14, "#4e79a7"),
        ("2025 参加／构成团体（截至5/6）", 35, "#8b5ea7"),
        ("2026 请愿赞同团体", 35, "#2d8f75"),
    ]
    intersections = [
        ("2023∩2025", 3, "A018 · A100 · A101"),
        ("2023∩2026", 7, "A018 · A100 · A101 · A056 · A099 · 沖縄平和市民連絡会 · 嘉手納ピースアクション"),
        ("2025∩2026 名称归一化候选", 5, "精确registry 3：A018 · A100 · A101；条件性2：A016(alias) · 新名称↔A010(lifecycle)"),
        ("三期重复", 3, "A018 · A100 · A101"),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fbfaf7"/>',
        svg_text(48, 48, "三份不同角色名单的重复公开出现", size=25, weight=700),
        svg_text(48, 78, "主办／赞同／参加或构成团体／请愿赞同是不同角色；重叠只证明列名重复。", size=14, fill="#566573"),
    ]
    for idx, (label, count, color) in enumerate(sets):
        x = 65 + idx * 390
        parts.append(f'<rect x="{x}" y="120" width="340" height="110" rx="14" fill="{color}" opacity="0.14" stroke="{color}" stroke-width="2"/>')
        parts.append(svg_text(x + 22, 158, label, size=18, weight=700, fill=color))
        parts.append(svg_text(x + 22, 204, f"{count} 个列名主体", size=28, weight=700, fill="#17202a"))
    max_count = 7
    for idx, (label, count, names) in enumerate(intersections):
        y = 300 + idx * 88
        bar_w = int(count / max_count * 560)
        parts.append(svg_text(230, y + 23, label, size=16, weight=700, anchor="end"))
        parts.append(f'<rect x="250" y="{y}" width="560" height="34" rx="6" fill="#e8ecef"/>')
        parts.append(f'<rect x="250" y="{y}" width="{bar_w}" height="34" rx="6" fill="#d08c3f"/>')
        parts.append(svg_text(830, y + 24, str(count), size=18, weight=700))
        parts.append(svg_text(250, y + 62, names, size=12, fill="#566573"))
    parts.extend(
        [
            svg_text(48, 654, "宫古A013：2024框架仅为媒体归因；未列入截至2025-05-06的35团体表，2026列为赞同团体。", size=15, weight=700, fill="#21618c"),
            svg_text(48, 684, "5/7是提交／行动日，5/16是发布日；四地发言／行动超边不等于三岛地方请求段，也不等于联盟。", size=14, weight=700, fill="#922b21"),
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def render_frame_object(path: Path) -> None:
    width, height = 1320, 720
    nodes = [
        ("基地／驻屯地", 130, 420, "#537895"),
        ("长射程导弹", 330, 350, "#537895"),
        ("弹药库／储存", 520, 420, "#537895"),
        ("港·机场·道路", 710, 350, "#537895"),
        ("运输／演习", 900, 420, "#537895"),
        ("避难／疏开", 1090, 350, "#537895"),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fbfaf7"/>',
        svg_text(48, 48, "共同文件如何构造共同对象：2025宣言与2026请愿的操作化", size=25, weight=700),
        svg_text(48, 82, "两份共同文本并置分散节点；这不证明参加团体独立采用，也不证明任何组织发生前后尺度转换。", size=14, fill="#566573"),
        '<rect x="75" y="125" width="520" height="140" rx="16" fill="#f4ecf7" stroke="#8b5ea7" stroke-width="2"/>',
        svg_text(105, 164, "COMMON-TEXT FRAME 共同文件框架", size=18, weight=700, fill="#6c3483"),
        svg_text(105, 200, "冲绳战记忆 · 防止再次成为战场 · 生命／人权／环境", size=16),
        svg_text(105, 232, "外交／对话 · 加害者与受害者责任", size=16),
        '<rect x="725" y="125" width="520" height="140" rx="16" fill="#e8f6f3" stroke="#2d8f75" stroke-width="2"/>',
        svg_text(755, 164, "COMMON-TEXT OBJECT 共同文件对象", size=18, weight=700, fill="#1e8449"),
        svg_text(755, 200, "生产／储存／运输／部署／演习／避难", size=16),
        svg_text(755, 232, "跨岛、跨九州、跨日本的分布式政策体系", size=16),
        '<path d="M595 195 C650 195 670 195 725 195" stroke="#d08c3f" stroke-width="4" fill="none" marker-end="url(#arrow)"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#d08c3f"/></marker></defs>',
    ]
    for idx in range(len(nodes) - 1):
        x1, y1 = nodes[idx][1], nodes[idx][2]
        x2, y2 = nodes[idx + 1][1], nodes[idx + 1][2]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#aeb6bf" stroke-width="3"/>')
    for label, x, y, color in nodes:
        parts.append(f'<circle cx="{x}" cy="{y}" r="58" fill="#ffffff" stroke="{color}" stroke-width="3"/>')
        split = label.split("／")
        for line_idx, line in enumerate(split):
            parts.append(svg_text(x, y - 4 + line_idx * 19, line, size=13, weight=700, anchor="middle"))
    parts.extend(
        [
            '<rect x="75" y="520" width="1170" height="120" rx="12" fill="#ffffff" stroke="#d5d8dc"/>',
            svg_text(100, 555, "下一步才可检验的因果问题", size=17, weight=700),
            svg_text(100, 586, "这个对象是秘书处／起草者对既有地方诉求的聚合，还是参加团体分别采用？当前两种解释同样成立。", size=15),
            svg_text(100, 616, "须先核文本所有权、A010与新名称的连续性、宫古组织自写文本，以及同一组织的前后可比材料。", size=15),
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def build_overlap_rows() -> list[dict[str, str]]:
    rosters = {
        "2023_A101_event": ROSTER_2023,
        "2025_participating_groups_as_of": participating_groups_2025(),
        "2026_petition_endorsing_groups": endorsing_groups_2026(),
    }
    comparisons = [
        ("OV01", "2023_A101_event", "2025_participating_groups_as_of"),
        ("OV02", "2023_A101_event", "2026_petition_endorsing_groups"),
        ("OV03", "2025_participating_groups_as_of", "2026_petition_endorsing_groups"),
    ]
    rows: list[dict[str, str]] = []
    for overlap_id, left, right in comparisons:
        keys = sorted(set(rosters[left]) & set(rosters[right]))
        conditional_keys = [key for key in keys if key.startswith("CANDIDATE_")]
        exact_registry_keys = [
            key for key in keys if key.startswith("A") and not key.startswith("CANDIDATE_")
        ]
        raw_exact_surface_names = sorted(set(rosters[left].values()) & set(rosters[right].values()))
        rows.append(
            guarded(
                {
                    "overlap_id": overlap_id,
                    "left_roster": left,
                    "left_n": str(len(rosters[left])),
                    "right_roster": right,
                    "right_n": str(len(rosters[right])),
                    "overlap_n": str(len(keys)),
                    "overlap_basis": "normalized_name_candidate" if overlap_id == "OV03" else "registry_or_name_crosswalk_candidate",
                    "raw_exact_surface_overlap_n": str(len(raw_exact_surface_names)),
                    "exact_registry_overlap_n": str(len(exact_registry_keys)),
                    "conditional_crosswalk_overlap_n": str(len(conditional_keys)),
                    "entity_keys": ";".join(keys),
                    "conditional_entity_keys": ";".join(conditional_keys),
                    "display_names": ";".join(rosters[right].get(key, rosters[left][key]) for key in keys),
                    "role_warning": "host/endorser/participating-group/endorser roles differ; overlap is repeated listing only",
                }
            )
        )
    triple = sorted(
        set(ROSTER_2023)
        & set(participating_groups_2025())
        & set(endorsing_groups_2026())
    )
    rows.append(
        guarded(
            {
                "overlap_id": "OV04",
                "left_roster": "all_three",
                "left_n": "",
                "right_roster": "all_three",
                "right_n": "",
                "overlap_n": str(len(triple)),
                "overlap_basis": "exact_registry_crosswalk_across_three_lists",
                "raw_exact_surface_overlap_n": str(len(triple)),
                "exact_registry_overlap_n": str(len(triple)),
                "conditional_crosswalk_overlap_n": "0",
                "entity_keys": ";".join(triple),
                "conditional_entity_keys": "",
                "display_names": ";".join(endorsing_groups_2026().get(key, key) for key in triple),
                "role_warning": "three-period repetition is not centrality, influence or stable alliance",
            }
        )
    )
    return rows


def build_readme(counts: dict[str, int]) -> str:
    return f"""# research_wave_h3_frontline_memory_v2

独立研究包，检验“反战／防止前线化／台湾有事是否成为跨地区共同语言”，同时严格区分两个**共同文件层**对象：

1. **共同文件框架（common-text frame）**：战争记忆、再次成为战场、生活安全、人权、环境、外交／对话如何被并置；
2. **共同文件对象（common-text object）**：2025 结成宣言与 2026 请愿如何把基地、导弹、弹药库、民用港机场与道路、运输／演习、避难构造成跨地域“战争准备”体系。

## 当前结论

- 可确认一个**至少持续到 2026 年初的正式跨区域行动载体**：2025-02-22 材料提出治理方案、共同代表、区域运营、秘书处及信息基础设施；2025-05-06 来源列出 {counts['network_participating_groups']} 个“参加／构成团体”；2025-06 与 2026-01 有两次正式行动。它不证明列名团体留存、实际分工或治理方案全部执行。
- 2025 结成宣言与 2026 请愿在**共同文件层**清楚并置生产、储存、运输、部署、演习和避难等节点。现阶段不能把这一文本构造转写成“组织／地方运动已经对象上移”。
- 这仍**不是扩散证明**。大分、石垣、宫古等地在正式网络成立前已有相近但地方化的语言；“把已有地方运动聚合起来”与“冲绳语言向外扩散”至少同样可行。
- 两家地方报纸在来源层明确报道旧名称 A010 于 2023-04-15 总会改为新名称；这一报道与 HR-012 的中央生命周期记录冲突，因此中央 canonical／alias／生命周期仍待人工裁决。旧名称 A010 在驻屯地启用前已经使用台湾有事、避难与外交框架，本包明确不写“安装造成尺度上移”。
- 宫古的 A013 战场化／对话框架来自对其共同代表的媒体归因，不是组织自写文本；同篇报道中撤离／生活安全说法来自其他发言者，不能转嫁给 A013。官方会议记录只证明一个相似名称主体提交意见／请求并获得答复，不证明到场或与 A013 完全同一。
- 2026-05-07 是提交／行动日，页面发布于 2026-05-16。正文只有与那国、石垣、宫古三个地方请求段；“四地”指外部报道中的发言／行动超边。{counts['petition_endorsing_groups']} 个赞同团体中有 {counts['petition_registry_crosswalks']} 个 registry 候选 crosswalk；“首次”仅作发布方／党媒归因。
- 2010／2015／2020 三份完整环境文本没有目标词，只能作为**文体／议题负例**，不能证明社会总体词汇增长。

## 复现

```powershell
python scripts\\make_research_wave_h3_frontline_memory_v2.py
python -m unittest tests.test_make_research_wave_h3_frontline_memory_v2
```

## 文件

- `frontline_memory_brief_v2.md`：解释性研究简报。
- `hypothesis_tests_v2.csv`：七个可证伪命题及当前判定。
- `comparable_corpus_v2.csv`：{counts['corpus']} 条分层语料观察；组织自写、转载、媒体归因、官方与学术反框架分开。
- `source_log_v2.csv`、`search_log_v2.csv`：来源与检索边界。
- `network_participating_group_candidates_v2.csv`：截至 2025-05-06 的 {counts['network_participating_groups']} 个参加／构成团体主张。
- `three_island_request_four_place_event_entities_v2.csv`：5 月 7 日事件／提交、5 月 16 日发布的 {counts['petition_endorsing_groups']} 个赞同团体及分层角色。
- `three_island_request_sections_v2.csv`：三个地方请求段；起草者与代表组织均保持 unknown，不把段落归给列名赞同团体。
- `event_speaker_attributions_v2.csv`：{counts['speaker_attributions']} 条逐发言者媒体归因，防止个人发言转嫁给组织。
- `event_endorser_issue_family_candidates_v2.csv`：分析者提出的事件赞同团体功能分类候选，不是来源原分类。
- `event_roster_overlap_v2.csv`：2023／2025／2026 名单重叠；角色不等价。
- `independent_adoption_panel_v2.csv`：独立采用、媒体归因、名册限定和缺失分开。
- `frame_object_observations_v2.csv`：共同框架与共同对象分离。
- `ishigaki_name_lifecycle_candidate_v2.csv`：保存来源层明确报道的改名，同时将与 HR-012 冲突的中央生命周期写回保持 human-pending。
- `network_formation_events_v2.csv`：2017–2026 载体／接触／正式行动序列。
- `negative_controls_v2.csv`：负例和竞争解释。
- `academic_connection_v2.csv`：直接案例、历史对照、战争记忆、组织变化和官方反框架的学术连接。
- `human_review_queue_v2.csv`、`local_retrieval_queue_v2.csv`：人工判断与当地材料任务。
- `fig1_carrier_and_object_timeline_v2.svg`、`fig2_roster_overlap_v2.svg`、`fig3_common_frame_vs_common_object_v2.svg`：三张研究图。
- `principal_checkpoint_v2.md`：负责人阅读与选择闸门。
- `validation_report_v2.md`、`manifest.json`：校验与复现信息。

## 硬边界

本包所有行均为 `research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`。参加／构成团体主张不生成团体之间的 dyadic 联盟边；共同请愿只生成事件级超边；“契机／首次”均保留为来源归因；35→38 不写成增长或留存；A010 的来源层改名报道不直接写入中央生命周期；共同文件对象不外推为各组织独立采用或前后变化。
"""


def build_brief(counts: dict[str, int], overlaps: list[dict[str, str]]) -> str:
    overlap_map = {row["overlap_id"]: row for row in overlaps}
    return f"""# H3 v2：前线化、战争记忆与“分布式战争准备”对象

## 一句话判断

当前线上证据能证明的是：**2025 结成宣言与 2026 请愿在共同文件层，把基地、导弹、弹药库、港机场、公路、运输／演习和避难并置成跨地域“战争准备”对象。**它还不能证明任何参加团体独立采用，也不能证明某个组织发生前后尺度转换。

## 1. 新证据把“共同语言”拆成两个共同文件层

2025 年网络结成宣言把冲绳／奄美岛屿基地、西日本长射程导弹与弹药库、住宅附近军事设施、民用港机场／公路、居民避难和冲绳战记忆放进同一文本。它既提供共同框架，也首次在本包中清楚列出一个分布式共同对象。

战争记忆在这里不是唯一机制。它与国际人道法、居民生命、人权、自然、地方说明权和外交并列，由共同文件把异质地方损害压缩成“战争准备”总框架。当前最严格的 text-ownership 判断是：**对象由宣言／请愿构造；起草者、秘书处和各列名团体分别贡献了什么，尚未测量。**

## 2. 正式行动载体可见，但“制度化”证据不足

结成材料提出区域运营、四名共同代表、秘书处／会计、在线会议、网页与邮件列表。2025-05-06 来源以原词列出 {counts['network_participating_groups']} 个“参加／构成团体”，2025-06 和 2026-01 又有两次政府交涉。最强安全表述是：**正式跨区域行动载体至少持续到 2026 年初。**这些材料不证明列名团体留存、实际分工或治理方案全部执行。

这也不等于从冲绳向西日本的语言扩散。大分敷户团体在 2023 年自有材料中已独立连接住宅安全、国际人道法、南西诸岛后勤和居民避难；A100、A101 及旧名称 A010 也有网络成立前材料，宫古则只有媒体归因。秘书处／共同文件聚合既有地方问题，与参加团体分别采用共同对象，两种解释目前同样成立。

## 3. 石垣材料同时包含来源层改名事实与中央生命周期冲突

可核序列分成两段：

- 2015–2016：HR-012 确认的旧名称 A010 成立核心与市民连络会；
- 2019／2023-02：旧名称 A010 的请愿／转载请求；
- 2023-03：石垣驻屯地启用；
- 2023-04-15：两家地方报纸报道旧名称组织在总会上改为新名称；4 月 28 日新名称组织发布 PAC3 声明，并伴随部分代表更替；
- 2025-03／05、2026-03／05：新名称组织分别出现在九州导弹声明、参加团体表、本地行动和共同请愿中。

来源层可以编码 `reported_exact_rename`，但它与 HR-012 的既有生命周期叙述冲突，中央 canonical／alias／生命周期必须保持 `human_pending`。更重要的是，旧名称 A010 在石垣驻屯地 2023-03-16 启用前的 2 月 9 日，已经把台湾有事、居民避难、外交和自治写入请求。因此即使以后确认中央改名，也**不能把跨尺度话语解释为驻屯地启用造成的转变**。

## 4. 宫古说明媒体归因、列名参加与共同事件并不等价

2024 年外部运动媒体把“不要把宫古变成战场／和平需要对话”归因给 A013 的一名共同代表；同篇报道中的撤离与“无处可逃”说法来自另外两名发言者，不能转嫁给 A013。官方地域连络会议记录只证明一个相似名称主体提交意见／请求并获得答复，既不证明到场，也不完成与 A013 的同一性 crosswalk。A013 未列入截至 2025-05-06 的 35 团体表，2026 则作为赞同团体出现。

因此不能把三种东西合并：

1. 媒体归因的相近语言；
2. 截至某日列为参加／构成团体；
3. 一次共同事件中的赞同／地方请求角色。

2025 表中缺席只是一个日期截面，不代表拒绝参加或后来仍未参加；组织独立采用则仍需自写文本。

## 5. 2026 材料是“三岛请求＋四地行动”的事件超边

请愿于 2026-05-07 提交并举行行动，发布页日期为 2026-05-16。正文先列共同请求，再分列与那国、石垣、宫古三个地方请求段；外部党媒报道的事件则包括三岛与冲绳本岛四地发言／参与。{counts['petition_endorsing_groups']} 个赞同团体中有 {counts['petition_registry_crosswalks']} 个 registry 候选 crosswalk。

发布方文字和党媒报道把它描述为“首次”共同／连带行动；本包只保存该归因，不把它当作已穷尽历史后的客观首次。编码必须拆为：

- 发布页面／站点所有者；
- 与那国、石垣、宫古三个地方请求段（起草者／代表组织 unknown）；
- 赞同团体；
- 外部报道中的四地发言人。

三个地方请求段的标题和正文不识别各段起草者或代表组织，不能把作者身份分别赋给 A016、A010 或 A013。

`event_endorser_issue_family_candidates_v2.csv` 的类别是分析者候选分类，不是来源原分类；不能把 35 个赞同团体互连成稳定关系网。

## 6. 重复骨架存在，但名单角色不同

- 2023 A101 活动（host + endorsers）与截至 2025-05-06 的参加／构成团体重叠 {overlap_map['OV01']['overlap_n']} 个；
- 2023 活动与 2026 请愿重叠 {overlap_map['OV02']['overlap_n']} 个；
- 2025 列名团体与 2026 赞同团体经名称归一化得到 {overlap_map['OV03']['overlap_n']} 个候选重叠，其中当前精确 registry 对应只有 {overlap_map['OV03']['exact_registry_overlap_n']} 个（A018、A100、A101），另 {overlap_map['OV03']['conditional_crosswalk_overlap_n']} 个是条件性 crosswalk（A016 alias；新名称组织与 A010 生命周期连续性）；
- 三期都出现的只有 {overlap_map['OV04']['overlap_n']} 个：A018、A100、A101。

这只能说明少数名称／组织构成可见的重复列名骨架。host／endorser／participating group／petition endorser 不是同一种关系，不能据重叠推定影响力、留存或联盟稳定性。

## 7. 学术价值在操作化与角色区分，不在宣称题目全新

既有研究早已讨论战争记忆、冲绳—本土连带、军事环境与反基地运动变化。本包目前可贡献的是：

1. 把共同框架与共同对象操作化为文件级变量；
2. 把文本所有权、参加／构成团体、赞同、起草者未知的地方请求段和发言角色拆开；
3. 用身份连续性、日期截面和负例阻止“组织改变／扩散／增长”的过强推断；
4. 把官方避难／国民保护框架与民间共同文件放进可比较但不混同的层次。

直接讨论 A108 成立的比嘉盛人 2023 文章只有书目信息，没有在线全文。未读它之前，本包不主张题目、历史叙述或机制新颖。

## 8. 当前判定

- 正式跨区域行动载体持续到 2026 初：**研究层支持；不等于制度化或团体留存**。
- 共同框架：**共同文件自我叙述层支持**。
- 分布式共同对象：**2025 宣言／2026 请愿文件层支持；列名团体独立采用未证**。
- 方向明确的语言扩散：**未确认**。
- 总体词汇增长：**当前不可检验**。
- A010：**来源层明确报道改名；中央生命周期因与 HR-012 冲突而待人工裁决；安装后尺度转换不支持**。
- 四地稳定共同组织／稳定联盟：**不支持；仅有参加团体表、三岛请求与四地事件超边等分层事实**。
"""


def build_checkpoint() -> str:
    return """# H3 v2 负责人检查点

本包已经到“需要负责人解释性参与”的位置，暂不继续自动扩检，也不写回中央。

## 建议阅读（约 75 分钟）

1. 15 分钟：`H3V2S009` 结成宣言——圈出共同文件框架与共同文件对象；现有公开文件不识别起草者，不把文本归给载体或列名团体。
2. 20 分钟：`H3V2S023`——区分 5 月 7 日提交／行动与 5 月 16 日发布，标出共同段、与那国／石垣／宫古三个请求段；各段起草者／代表组织保持 unknown。
3. 15 分钟：`H3V2S015` 与 `H3V2S025`——确认来源层明确报道 4 月 15 日改名，再判断如何与 HR-012 的中央生命周期记录协调；不再检验“驻屯地启用导致尺度上移”。
4. 10 分钟：`H3V2S019–020` 宫古——逐发言者区分 A013 共同代表的战场化／对话说法与他人的撤离说法；把官方材料限定为相似名称主体的请求提交记录，不写到场。
5. 15 分钟：`AL03`（Ono 2016）与 `AL07`（Kumamoto 2024）摘要／全文相关段；同时派取 `AL01` 比嘉盛人全文。

## 需要负责人拍板的四件事

1. 是否以“共同文件如何构造分布式战争准备对象、谁拥有文本”为论文候选；不预设地方组织已经对象上移。
2. 如何把来源层 `reported_exact_rename` 与 HR-012 的中央生命周期冲突写成人工裁决；来源事实不抹除，中央字段暂不改。
3. 2025 网络是否进入 registry；若进入，35 条只编码 `participating_or_constituent_group as-of 2025-05-06`，不写法律成员身份、留存或团体间联盟。
4. 2026 材料是否进入中央事件层；若进入，分 5/7 提交／行动、5/16 发布、三个起草者／代表组织 unknown 的地方请求段、四地发言／行动、赞同团体及“首次”归因。

## 暂停线

负责人完成上述阅读和 `human_review_queue_v2.csv` 的高优先项以前：

- 不把本包接到前端；
- 不改 A010 canonical／alias／生命周期；
- 不新增正式关系边；
- 不写“词汇增长”“单向扩散”“全日本共同语言”“稳定联盟”；
- 不把共同文件对象写成参加团体独立采用或组织前后变化；
- 不把 35→38 写成团体增长、留存或治理执行。
"""


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(out: Path) -> list[str]:
    errors: list[str] = []
    csv_paths = sorted(out.glob("*.csv"))
    for path in csv_paths:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            errors.append(f"{path.name}: empty")
            continue
        for idx, row in enumerate(rows, start=2):
            if "data_layer" in row and row["data_layer"] != "research_only":
                errors.append(f"{path.name}:{idx}: data_layer")
            if "frontend_eligibility" in row and row["frontend_eligibility"] != "not_frontend_ready":
                errors.append(f"{path.name}:{idx}: frontend_eligibility")
            if "central_writeback" in row and row["central_writeback"] != "no":
                errors.append(f"{path.name}:{idx}: central_writeback")

    if len(NETWORK_PARTICIPATING_GROUPS) != 35:
        errors.append("network participating-group list must contain 35 rows")
    if len({name for _, name, _, _ in NETWORK_PARTICIPATING_GROUPS}) != 35:
        errors.append("network participating-group names must be unique")
    if len(PETITION_ENDORSING_GROUPS) != 35:
        errors.append("petition must contain 35 endorsing-group rows")
    if len({name for _, name, _, _, _, _ in PETITION_ENDORSING_GROUPS}) != 35:
        errors.append("petition endorsing-group names must be unique")
    if len(THREE_ISLAND_REQUEST_SECTIONS) != 3:
        errors.append("petition must have exactly three island-specific request sections")
    if any(
        drafter != "unknown" or representative_org != "unknown"
        for _, _, _, _, drafter, representative_org, _ in THREE_ISLAND_REQUEST_SECTIONS
    ):
        errors.append("request-section drafter and representative organization must remain unknown")
    if any(
        "local_request_subject_candidate" in role
        for _, _, _, _, _, role in PETITION_ENDORSING_GROUPS
    ):
        errors.append("listed endorsers cannot inherit local-request section authorship")
    if "A013" in participating_groups_2025():
        errors.append("Miyako A013 must remain absent from dated 2025 participating-group list")
    if "A013" not in endorsing_groups_2026():
        errors.append("Miyako A013 must appear among 2026 endorsing groups")
    a013_adoption_rows = [row for row in ADOPTION_PANEL if row[0] == "A013"]
    if len(a013_adoption_rows) != 1 or "life_safety" in a013_adoption_rows[0][5]:
        errors.append("A013 may retain only its speaker-attributed battlefield/dialogue frame")
    if len(EVENT_SPEAKER_ATTRIBUTIONS) != 3:
        errors.append("H3V2S019 must remain split into three speaker-specific rows")
    if any(row[8] != "speaker_specific_media_attribution" for row in EVENT_SPEAKER_ATTRIBUTIONS):
        errors.append("H3V2S019 speaker rows must remain media attributions")

    overlaps = {row["overlap_id"]: row for row in build_overlap_rows()}
    expected = {"OV01": "3", "OV02": "7", "OV03": "5", "OV04": "3"}
    for key, value in expected.items():
        if overlaps[key]["overlap_n"] != value:
            errors.append(f"{key} expected {value}, got {overlaps[key]['overlap_n']}")
    if overlaps["OV03"]["overlap_basis"] != "normalized_name_candidate":
        errors.append("OV03 must be labeled normalized_name_candidate")
    if overlaps["OV03"]["exact_registry_overlap_n"] != "3":
        errors.append("OV03 exact registry overlap must be 3")
    if overlaps["OV03"]["conditional_crosswalk_overlap_n"] != "2":
        errors.append("OV03 conditional overlap must be 2")

    source_by_id = {source["source_id"]: source for source in SOURCES}
    if source_by_id["H3V2S023"]["date"] != "2026-05-16":
        errors.append("H3V2S023 must use publication date 2026-05-16")
    if source_by_id["H3V2S025"]["attribution_status"] != "independent_news_reported_exact_rename":
        errors.append("H3V2S025 must preserve the source-reported exact rename")
    if source_by_id["H3V2S020"]["attribution_status"] != "official_request_submission_record_not_attendance":
        errors.append("H3V2S020 must not be encoded as attendance")
    hypothesis_by_id = {row["hypothesis_id"]: row for row in HYPOTHESES}
    if hypothesis_by_id["H3c"]["current_assessment"] != "supported_at_common_document_layer_only":
        errors.append("H3c must remain common-document-layer only")
    if hypothesis_by_id["H3f"]["current_assessment"] != "reported_exact_rename_central_lifecycle_human_pending_no_scale_shift_claim":
        errors.append("H3f must retain the reported rename, central lifecycle gate and no-scale-shift boundary")
    post_rename_stages = [
        row for row in ISHIGAKI_LIFECYCLE_CANDIDATE_STAGES if row[0] >= "LC04"
    ]
    if any(
        row[7] != "reported_exact_rename_central_lifecycle_human_pending"
        for row in post_rename_stages
    ):
        errors.append("post-LC04 Ishigaki stages must retain source-reported rename and central human gate")

    source_ids = {source["source_id"] for source in SOURCES}
    for corpus_id, _, source_id, *_ in COMPARABLE_CORPUS:
        for one_id in source_id.split(";"):
            if one_id not in source_ids:
                errors.append(f"{corpus_id}: unknown source {one_id}")
    for source in SOURCES:
        if not source["url"].startswith("https://"):
            errors.append(f"{source['source_id']}: URL is not HTTPS")

    required_svgs = {
        "fig1_carrier_and_object_timeline_v2.svg",
        "fig2_roster_overlap_v2.svg",
        "fig3_common_frame_vs_common_object_v2.svg",
    }
    for name in required_svgs:
        path = out / name
        if not path.exists() or "<svg" not in path.read_text(encoding="utf-8"):
            errors.append(f"{name}: missing or invalid")

    generated_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in out.iterdir()
        if path.is_file() and path.suffix.lower() in {".md", ".csv", ".svg"}
    )
    forbidden_phrases = (
        "一个正式跨区域载体已经制度化",
        "A010 安装后尺度转换",
        "共同对象发生上移",
        "35 个正式成员",
        "四地地方请求",
    )
    for phrase in forbidden_phrases:
        if phrase in generated_text:
            errors.append(f"forbidden overclaim remains: {phrase}")
    return errors


def build_package(out: Path = DEFAULT_OUT) -> dict[str, int]:
    out.mkdir(parents=True, exist_ok=True)
    for stale_name in STALE_OUTPUT_FILENAMES:
        (out / stale_name).unlink(missing_ok=True)
    protected_before = {str(path): file_sha256(path) for path in PROTECTED_INPUTS}

    source_rows = [guarded(dict(source)) for source in SOURCES]
    write_csv(out / "source_log_v2.csv", source_rows)
    write_csv(out / "hypothesis_tests_v2.csv", HYPOTHESES)

    corpus_rows = [
        guarded(
            {
                "corpus_id": corpus_id,
                "date": date,
                "source_id": source_id,
                "text_owner_or_subject": owner,
                "genre": genre,
                "place_scope": place,
                "frame_codes": frames,
                "object_scope": object_scope,
                "text_status": text_status,
                "analytical_role": analytical_role,
                "interpretation_limit": "Document-level observation only; no automatic diffusion, alliance or trend inference.",
            }
        )
        for corpus_id, date, source_id, owner, genre, place, frames, object_scope, text_status, analytical_role in COMPARABLE_CORPUS
    ]
    write_csv(out / "comparable_corpus_v2.csv", corpus_rows)

    participating_group_rows = [
        guarded(
            {
                "participating_group_claim_id": f"H3PG{idx:03d}",
                "as_of_date": "2025-05-06",
                "region": region,
                "organization_name_as_listed": name,
                "actor_id": actor_id,
                "registry_crosswalk_status": status,
                "evidence_role": "participating_or_constituent_group_as_listed",
                "source_id": "H3V2S011",
                "locator": "PDF p.2 参加団体35団体 / 構成団体 list",
                "retention_claim": "unmeasured",
                "active_division_of_labor_claim": "unmeasured",
                "governance_execution_claim": "unmeasured",
                "stable_alliance_claim": "no",
                "interpretation_limit": "Source-original participating/constituent-group listing as-of one date; not legal membership, retention, active role, governance execution or dyadic alliance.",
            }
        )
        for idx, (region, name, actor_id, status) in enumerate(
            NETWORK_PARTICIPATING_GROUPS, start=1
        )
    ]
    write_csv(
        out / "network_participating_group_candidates_v2.csv",
        participating_group_rows,
    )

    petition_endorser_rows = [
        guarded(
            {
                "event_endorser_claim_id": f"H3Q{idx:03d}",
                "event_id": "H3EV2026_THREE_ISLAND_REQUEST_FOUR_PLACE_ACTION",
                "event_date": "2026-05-07",
                "publication_date": "2026-05-16",
                "place_or_scope": place,
                "organization_name_as_listed": name,
                "actor_id": actor_id,
                "registry_crosswalk_status": crosswalk,
                "analyst_issue_family_candidate": issue_family,
                "issue_family_classification_status": "analyst_candidate_not_source_label",
                "event_role": role,
                "source_id": "H3V2S023",
                "external_confirmation_source_id": "H3V2S024",
                "first_joint_action_claim_status": "publisher_and_party_press_attribution_not_independently_established",
                "stable_alliance_claim": "no",
                "independent_adoption_claim": "unconfirmed_unless_separately_documented",
                "interpretation_limit": "Listed endorser only. The document has three island-specific request sections; four-place speaking/action, first-action attribution, text ownership and independent adoption remain separately gated.",
            }
        )
        for idx, (place, name, actor_id, crosswalk, issue_family, role) in enumerate(PETITION_ENDORSING_GROUPS, start=1)
    ]
    write_csv(
        out / "three_island_request_four_place_event_entities_v2.csv",
        petition_endorser_rows,
    )

    request_section_rows = [
        guarded(
            {
                "request_section_id": section_id,
                "event_id": "H3EV2026_THREE_ISLAND_REQUEST_FOUR_PLACE_ACTION",
                "event_or_submission_date": "2026-05-07",
                "publication_date": "2026-05-16",
                "island": island,
                "section_heading_as_published": heading,
                "request_item_count": request_count,
                "publisher_or_host": "ノーモア沖縄戦 命どぅ宝の会 website",
                "document_author_or_drafter": drafter,
                "representative_organization": representative_org,
                "attribution_status": attribution_status,
                "source_id": "H3V2S023",
                "organization_authorship_claim": "unconfirmed",
                "interpretation_limit": "A section heading and its requests do not identify the drafter or a representative organization; do not transfer authorship to A016, A010 or A013.",
            }
        )
        for (
            section_id,
            island,
            heading,
            request_count,
            drafter,
            representative_org,
            attribution_status,
        ) in THREE_ISLAND_REQUEST_SECTIONS
    ]
    write_csv(out / "three_island_request_sections_v2.csv", request_section_rows)

    speaker_rows = [
        guarded(
            {
                "speaker_attribution_id": attribution_id,
                "event_date": date,
                "source_id": source_id,
                "publisher_or_host": publisher,
                "document_author_or_drafter": document_author,
                "speaker_or_subject": speaker,
                "actor_id_crosswalk": actor_id,
                "frame_codes_attributed_to_this_speaker": frame_codes,
                "attribution_status": attribution_status,
                "organization_frame_transfer": "no",
                "interpretation_limit": limit,
            }
        )
        for (
            attribution_id,
            date,
            source_id,
            publisher,
            document_author,
            speaker,
            actor_id,
            frame_codes,
            attribution_status,
            limit,
        ) in EVENT_SPEAKER_ATTRIBUTIONS
    ]
    write_csv(out / "event_speaker_attributions_v2.csv", speaker_rows)

    issue_counts = Counter(row[4] for row in PETITION_ENDORSING_GROUPS)
    issue_rows = [
        guarded(
            {
                "analyst_issue_family_candidate": family,
                "endorser_count": str(count),
                "event_id": "H3EV2026_THREE_ISLAND_REQUEST_FOUR_PLACE_ACTION",
                "source_id": "H3V2S023",
                "classification_status": "analyst_candidate_not_source_label",
                "classification_method": "manual analyst coding from listed name/function cues; pending human review",
                "interpretation_limit": "Candidate classification of this event's listed endorsers; not a source category or movement-population composition.",
            }
        )
        for family, count in sorted(issue_counts.items())
    ]
    write_csv(out / "event_endorser_issue_family_candidates_v2.csv", issue_rows)

    adoption_rows = [
        guarded(
            {
                "actor_id": actor_id,
                "organization_name": name,
                "place": place,
                "pre_2025_independent_evidence_status": evidence_status,
                "source_ids": source_ids,
                "frame_codes": frame_codes,
                "text_ownership": ownership,
                "network_or_event_status": event_status,
                "interpretation_limit": "Dated listing never substitutes for independently authored text; media attribution remains attribution and missing is not negative evidence.",
            }
        )
        for actor_id, name, place, evidence_status, source_ids, frame_codes, ownership, event_status in ADOPTION_PANEL
    ]
    write_csv(out / "independent_adoption_panel_v2.csv", adoption_rows)

    write_csv(out / "frame_object_observations_v2.csv", FRAME_OBJECT_OBSERVATIONS)
    lifecycle_rows = [
        guarded(
            {
                "stage_id": stage_id,
                "date": date,
                "entity_scope": entity_scope,
                "stage": stage,
                "action_orientation": orientation,
                "object_scope": object_scope,
                "source_ids": source_ids,
                "identity_continuity_status": continuity_status,
                "interpretation_limit": limit,
            }
        )
        for (
            stage_id,
            date,
            entity_scope,
            stage,
            orientation,
            object_scope,
            source_ids,
            continuity_status,
            limit,
        ) in ISHIGAKI_LIFECYCLE_CANDIDATE_STAGES
    ]
    write_csv(out / "ishigaki_name_lifecycle_candidate_v2.csv", lifecycle_rows)

    event_rows = [
        guarded(
            {
                "event_id": event_id,
                "date": date,
                "place": place,
                "event_label": label,
                "event_stage": stage,
                "source_ids": source_ids,
                "attribution_status": attribution,
                "interpretation_limit": limit,
            }
        )
        for event_id, date, place, label, stage, source_ids, attribution, limit in EVENT_SEQUENCE
    ]
    write_csv(out / "network_formation_events_v2.csv", event_rows)

    overlap_rows = build_overlap_rows()
    write_csv(out / "event_roster_overlap_v2.csv", overlap_rows)
    write_csv(out / "negative_controls_v2.csv", NEGATIVE_CONTROLS)

    academic_rows = [
        guarded(
            {
                "academic_id": academic_id,
                "author": author,
                "year": year,
                "title": title,
                "venue": venue,
                "url": url,
                "reading_depth": depth,
                "connection_to_h3": connection,
                "use_boundary_or_next_step": boundary,
            },
            claim_status="literature_link_candidate",
        )
        for academic_id, author, year, title, venue, url, depth, connection, boundary in ACADEMIC_LINKS
    ]
    write_csv(out / "academic_connection_v2.csv", academic_rows)

    search_rows = [
        guarded(
            {
                "search_id": search_id,
                "search_date": date,
                "target": target,
                "query": query,
                "result_summary": result,
                "stop_or_gap_status": status,
            },
            claim_status="search_log",
        )
        for search_id, date, target, query, result, status in SEARCH_LOG
    ]
    write_csv(out / "search_log_v2.csv", search_rows)

    hr_rows = [
        guarded(
            {
                "review_item_id": item_id,
                "decision_domain": domain,
                "question": question,
                "source_ids": sources,
                "hard_boundary": boundary,
                "priority": priority,
                "human_decision": "",
                "human_note": "",
            },
            claim_status="needs_human_decision",
            review_status="needs_human_review",
        )
        for item_id, domain, question, sources, boundary, priority in HUMAN_REVIEW_QUEUE
    ]
    write_csv(out / "human_review_queue_v2.csv", hr_rows)

    lr_rows = [
        guarded(
            {
                "retrieval_id": retrieval_id,
                "target_material": target,
                "retrieval_route": route,
                "research_value": value,
                "related_review_items": review_items,
                "status": "open",
            },
            claim_status="needs_local_or_library_retrieval",
            review_status="needs_local_retrieval",
        )
        for retrieval_id, target, route, value, review_items in LOCAL_RETRIEVAL_QUEUE
    ]
    write_csv(out / "local_retrieval_queue_v2.csv", lr_rows)

    render_timeline(out / "fig1_carrier_and_object_timeline_v2.svg")
    render_overlap(out / "fig2_roster_overlap_v2.svg", overlap_rows)
    render_frame_object(out / "fig3_common_frame_vs_common_object_v2.svg")

    counts = {
        "sources": len(SOURCES),
        "corpus": len(COMPARABLE_CORPUS),
        "network_participating_groups": len(NETWORK_PARTICIPATING_GROUPS),
        "petition_endorsing_groups": len(PETITION_ENDORSING_GROUPS),
        "petition_registry_crosswalks": sum(1 for row in PETITION_ENDORSING_GROUPS if row[2]),
        "request_sections": len(THREE_ISLAND_REQUEST_SECTIONS),
        "speaker_attributions": len(EVENT_SPEAKER_ATTRIBUTIONS),
        "hypotheses": len(HYPOTHESES),
        "academic_links": len(ACADEMIC_LINKS),
        "human_review_items": len(HUMAN_REVIEW_QUEUE),
        "local_retrieval_items": len(LOCAL_RETRIEVAL_QUEUE),
    }
    (out / "README.md").write_text(build_readme(counts), encoding="utf-8")
    (out / "frontline_memory_brief_v2.md").write_text(build_brief(counts, overlap_rows), encoding="utf-8")
    (out / "principal_checkpoint_v2.md").write_text(build_checkpoint(), encoding="utf-8")

    errors = validate(out)
    validation_lines = [
        "# H3 v2 validation",
        "",
        f"- Result: **{'PASS' if not errors else 'FAIL'}**",
        f"- CSV files parsed: {len(list(out.glob('*.csv')))}",
        f"- Network participating/constituent-group rows as-of 2025-05-06: {len(NETWORK_PARTICIPATING_GROUPS)} (unique names: {len({row[1] for row in NETWORK_PARTICIPATING_GROUPS})})",
        f"- 2026 petition endorsing-group rows: {len(PETITION_ENDORSING_GROUPS)} (unique names: {len({row[1] for row in PETITION_ENDORSING_GROUPS})})",
        f"- Registry crosswalk candidates in petition: {counts['petition_registry_crosswalks']}",
        "- Expected overlaps: 2023∩2025=3; 2023∩2026=7; 2025∩2026 normalized-name candidate=5 (exact registry=3, conditional=2); all-three=3.",
        "- Miyako gate: media-attributed frame; absent from dated 2025 participating-group list; present as a 2026 endorser.",
        "- 2026 date/role gate: 2026-05-07 submission/action; 2026-05-16 publication; three island-specific request sections; four-place speaking/action hyperedge.",
        f"- Ownership gate: {counts['request_sections']} request sections have unknown drafters/representative organizations; {counts['speaker_attributions']} Miyako statements remain speaker-specific attributions.",
        "- Common-object gate: supported only at the 2025 declaration / 2026 petition document layer.",
        "- A010 gate: source-level exact rename reported; central canonical/alias/lifecycle human-pending because of HR-012 conflict; no installation-caused scale-shift claim.",
        "- Issue-family gate: analyst candidate classification, not source taxonomy.",
        "- Guard: all guarded outputs are research_only / not_frontend_ready / central_writeback=no.",
        "- Protected-input hash check: pending post-write comparison below.",
        "",
    ]
    protected_after = {str(path): file_sha256(path) for path in PROTECTED_INPUTS}
    protected_unchanged = protected_before == protected_after
    validation_lines.append(f"- Protected central/v1 inputs unchanged: **{'yes' if protected_unchanged else 'NO'}**")
    if not protected_unchanged:
        errors.append("protected inputs changed during build")
    if errors:
        validation_lines.extend(["", "## Errors", *[f"- {error}" for error in errors]])
    (out / "validation_report_v2.md").write_text("\n".join(validation_lines) + "\n", encoding="utf-8")
    if errors:
        raise RuntimeError("validation failed: " + "; ".join(errors))

    files = sorted(
        path
        for path in out.iterdir()
        if path.is_file() and path.name != "manifest.json"
    )
    manifest = {
        "package": "research_wave_h3_frontline_memory_v2",
        "built_on": "2026-07-20",
        "status": "research_only_not_frontend_ready",
        "central_writeback": "no",
        "counts": counts,
        "protected_inputs": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": protected_after[str(path)],
            }
            for path in PROTECTED_INPUTS
        ],
        "files": [
            {
                "path": path.name,
                "sha256": file_sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in files
        ],
        "hard_boundaries": [
            "No vocabulary-growth claim from schema tags or three unmatched controls.",
            "No diffusion direction without same-organization before/after texts and transmission evidence.",
            "The 2025 source lists participating/constituent groups as-of one date; it proves neither legal membership, retention, governance execution nor dyadic alliances.",
            "The 2026 material separates 2026-05-07 submission/action from 2026-05-16 publication, three island-specific request sections from a four-place speaking/action hyperedge, and attributed 'first' language from fact.",
            "The three request-section headings identify neither drafters nor representative organizations; A016, A010 and A013 do not inherit section authorship.",
            "H3V2S019 remains speaker-specific: A013 receives battlefield/dialogue attribution only, while evacuation/life-safety remarks stay with two other speakers.",
            "The 2025 declaration and 2026 petition construct a common object at document level; participating-group adoption and before/after organizational change are unproven.",
            "News sources report an exact A010 rename, but central canonical/alias/lifecycle remains human-pending because of the HR-012 conflict; no installation-caused scale-shift inference is available.",
            "35-to-38 is not a growth or retention estimate without comparable dated lists.",
        ],
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return counts


def main() -> int:
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUT
    counts = build_package(out)
    print(json.dumps({"output": str(out), "counts": counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
