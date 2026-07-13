from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "edge_activation_v1"
DATA = ROOT / "data" / "interim" / "28_edge_activation_candidates_v1.csv"
ACCESSED = "2026-07-13"

ACTORS = {
    "A073": "琉球沖縄国際支援プログラム",
    "A076": "ジュゴン保護基金委員会（Save the Dugong Foundation）",
    "A086": "Turtle Island Restoration Network",
    "A087": "NPO法人世界版「平和の礎」を提案する会",
    "A088": "特定非営利活動法人沖縄平和協力センター",
    "A089": "沖縄県教職員組合",
    "A090": "沖縄県高等学校障害児学校教職員組合",
    "A091": "日本労働組合総連合会沖縄県連合会（連合沖縄）",
    "A092": "沖縄県労働組合総連合",
    "A093": "全日本自治団体労働組合沖縄県本部",
    "A094": "一般社団法人沖縄県女性連合会",
    "A095": "止めよう「自衛隊配備」宮古郡民の会",
    "A096": "宮古平和運動連絡協議会",
    "A097": "宮古島環境クラブ",
    "A098": "特定非営利活動法人宮古島海の環境ネットワーク",
    "A099": "有機フッ素化合物（PFAS）汚染から市民の生命を守る連絡会",
    "A100": "ミサイル配備から命を守るうるま市民の会",
    "A101": "沖縄・琉球弧の声を届ける会",
}

# HR-013 subsequently rejected A094 as a general women's association outside the
# Phase-1 scope.  Keep the original 18-actor acquisition snapshot reproducible,
# but generate a separate current queue that excludes the human-rejected actor.
# This is intentionally encoded as a disposition, not as a new AI review.
POST_HR013_EXCLUSIONS = {
    "A094": {
        "human_decision_ref": "HR-013",
        "human_decision": "out_of_scope_rejected",
        "reason": "一般妇人会；HR-013明确剔除，不再进入registry或edge复核队列。",
    }
}

ISSUES = {
    "I001": "anti_base",
    "I002": "anti_military",
    "I003": "Henoko",
    "I004": "dugong",
    "I005": "biodiversity",
    "I006": "groundwater",
    "I007": "life_safety",
    "I008": "health_risk",
    "I009": "local_autonomy",
    "I011": "legal",
    "I012": "international_advocacy",
    "I015": "international_cooperation",
    "I017": "frontline_prevention",
    "I018": "Taiwan_contingency",
    "I019": "peace",
    "I020": "environment",
    "I022": "women",
    "I023": "human_rights",
    "I025": "anti_war",
    "I026": "mobilization",
}


def source(
    key: str,
    actor_id: str,
    url: str,
    title: str,
    date: str,
    source_type: str,
    level: str,
    identity_support: str,
    direct_issue_support: str,
    locator: str,
    limit: str,
) -> dict[str, str]:
    return {
        "source_key": key,
        "actor_id": actor_id,
        "actor_name": ACTORS[actor_id],
        "source_url": url,
        "source_title": title,
        "source_date": date,
        "source_type": source_type,
        "evidence_level": level,
        "identity_support": identity_support,
        "direct_issue_support": direct_issue_support,
        "locator": locator,
        "explanation_limit": limit,
        "accessed_on": ACCESSED,
    }


SOURCES = [
    source("EA-S001", "A076", "https://earthjustice.org/press/2003/us-japanese-conservation-groups-join-in-legal-effort-to-save-okinawa-dugong-from-extinction", "US & Japanese Conservation Groups Join in Legal Effort to Save Okinawa Dugong from Extinction", "2003-09-25", "legal_advocacy_primary", "E4", "yes_named_party", "yes_case_specific", "paras/lines 81–100: lawsuit object, Henoko relocation, plaintiff list and Save the Dugong Foundation quote", "Plaintiff role is case-specific; it does not prove continuing organizational activity after the litigation."),
    source("EA-S002", "A076", "https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_03-cv-04350/pdf/USCOURTS-cand-3_03-cv-04350-16.pdf", "Okinawa Dugong v. Rumsfeld federal court record", "2003–2018", "court_record", "E4", "yes_caption", "yes_case_specific", "caption and procedural history for C-03-4350", "Use only for named-party/legal-role facts; scanned pagination should be pinpointed before quotation."),
    source("EA-S003", "A076", "https://ryukyushimpo.jp/okinawa-dic/prentry-41677.html", "琉球新報 沖縄用語辞典：ジュゴン保護基金委員会", "n.d.", "local_newspaper_reference", "E3", "yes_secondary", "yes_background", "entry states 1999 formation after Henoko became a relocation candidate and a dugong-protection/ecological-survey purpose", "Secondary reference; legal status and continuity still need local or organizational records."),
    source("EA-S004", "A086", "https://seaturtles.org/wp-content/uploads/2025/01/TIRN-6.30.2024-Public-Disclosure-Copy-2.pdf", "Turtle Island Restoration Network Form 990 public disclosure", "FY2023", "organization_financial_filing", "E4", "yes", "mission_only", "Form 990 Part III: marine-wildlife/ocean mission and advocacy programs", "Establishes organizational identity and general marine mission, not the Okinawa case by itself."),
    source("EA-S005", "A086", "https://earthjustice.org/press/2003/us-japanese-conservation-groups-join-in-legal-effort-to-save-okinawa-dugong-from-extinction", "US & Japanese Conservation Groups Join in Legal Effort to Save Okinawa Dugong from Extinction", "2003-09-25", "legal_advocacy_primary", "E4", "yes_named_party", "yes_case_specific", "paras/lines 81–100: TIRN listed as a U.S. plaintiff; suit concerns dugong habitat and the Henoko relocation plan", "Case participation is not a stable alliance and does not establish a continuing Okinawa program."),
    source("EA-S006", "A086", "https://seaturtles.org/wp-content/uploads/2019/01/19-01-02-OPENING-BRIEF.pdf", "Opening Brief, Center for Biological Diversity et al. v. Esper", "2019-01-02", "party_legal_filing", "E4", "yes_named_party", "yes_case_specific", "caption and statement of the case", "Use as litigation evidence only; do not infer broader political stance."),
    source("EA-S007", "A087", "https://www.npo-homepage.go.jp/npoportal/gyosei-print/047006834", "NPO法人世界版「平和の礎」を提案する会 行政入力情報", "2025-01-29 update", "official_npo_portal", "E4", "yes", "yes_statutory_purpose", "registered purpose: world peace, international cooperation/understanding, abolition of war and nuclear weapons", "Statutory purpose supports positioning, not proof of every planned activity being implemented."),
    source("EA-S008", "A087", "https://www.ishiji.org/about", "概要｜世界版「平和の礎」を提案する会", "2025-02-15 update", "organization_site", "E4", "yes", "yes_positioning", "sections 1–3: worldwide memorial proposal, war/nuclear abolition, lasting peace and international joint work", "Organization-authored framing; distinguish aspiration from completed international participation."),
    source("EA-S009", "A088", "https://www.npo-homepage.go.jp/npoportal/list?fiscal_year_end_first=&fiscal_year_end_second=&fiscal_year_start_first=&fiscal_year_start_second=&goc%5B0%5D=000&order=desc&page=260&sort=gov_code", "NPO法人ポータル：沖縄平和協力センター", "2025-07-28 update", "official_npo_portal", "E4", "yes", "no", "entity row and 2002-10-17 certification", "Identity only; use activity sources for actor–issue edges."),
    source("EA-S010", "A088", "https://www.jica.go.jp/domestic/okinawa/activities/kaihatsu/festival/2022/organization_02/08.html", "特定非営利活動法人 沖縄平和協力センター（OPAC）", "2022", "official_jica_partner_page", "E4", "yes", "yes_positioning", "organization profile: peace/security think tank, international peace cooperation, training, overseas technical support", "Administrative/international-cooperation node; do not recode as anti-base or movement funding."),
    source("EA-S011", "A088", "https://www.jica.go.jp/domestic/okinawa/information/topics/2023/1525168_14644.html", "沖縄県の平和希求の心をカンボジアの地雷対策に活かす草の根技術協力", "2023-11-15", "official_jica_project_record", "E4", "yes_designated_organization", "yes_project_specific", "OPAC named as designated organization for Cambodia peace-museum/human-security training", "Confirms a project role, not a payment amount or movement relation."),
    source("EA-S012", "A089", "https://www.oki-tu.org/about_us", "沖教組とは", "n.d.", "organization_site", "E4", "yes", "yes_positioning", "history and peace-education sections: peace/democratic education and ‘never again send our students to the battlefield’", "Mission/history supports peace and anti-war positioning; inter-organizational cooperation mentioned there is not an alliance edge."),
    source("EA-S013", "A089", "https://www.oki-tu.org/branch", "各支部｜沖縄県教職員組合", "n.d.", "organization_site_subunit_page", "E4", "yes_parent_site", "yes_with_attribution_caveat", "Kunigami branch states it engages in peace education and opposition to the Henoko new-base construction", "A branch statement cannot automatically be generalized to every prefectural-union unit; HR-010 must decide attribution."),
    source("EA-S014", "A090", "https://www.oki-htu.or.jp/about.php", "組合について｜沖縄県高等学校障害児学校教職員組合", "n.d.", "organization_site", "E4", "yes", "yes_positioning_and_repertoire", "peace/human-rights/environment learning; annual 5.15 peace march seeking a base-free peaceful Okinawa", "Annual march is a public repertoire; it does not itself establish alliances with other participants."),
    source("EA-S015", "A091", "https://www.rengo-okinawa.jp/about-us/", "連合沖縄とは", "n.d.", "organization_site", "E4", "yes", "no", "formal name, federation status and territorial structure", "Identity only."),
    source("EA-S016", "A091", "https://www.rengo-okinawa.jp/cat-news/post-2485/", "在日米軍関係者によって繰り返される性的暴行事件に関する抗議・要請", "2025-03-11", "organization_action_record", "E4", "yes", "yes_event_specific", "request of 2025-01-20; explicit safety, women/children and human-rights language", "Event-specific request; do not treat it as the federation’s entire mission."),
    source("EA-S017", "A091", "https://www.rengo-okinawa.jp/cat-news/post-2174/", "連合2024平和行動in沖縄を開催", "2024-07-05", "organization_action_record", "E4", "yes", "yes_repeated_program", "peace action, base-burden/life-safety statements and Henoko/base route", "Participation and hosting are not proof of stable alliance with every attendee."),
    source("EA-S018", "A091", "https://www.rengo-okinawa.jp/cat-news/post-2414/", "連合沖縄2025新春の集いを開催", "2025-01-14", "organization_action_record", "E4", "yes", "yes_declared_direction", "chair calls for base consolidation/reduction, status-of-forces revision and stopping Henoko construction", "A leadership statement is source-backed positioning for this period, not timeless consensus."),
    source("EA-S019", "A092", "https://okinawakenroren.org/kenrorenshokai.html", "沖縄県労連の紹介", "n.d.", "organization_site", "E4", "yes", "yes_charter", "organizational principles oppose militarism and seek base removal, nuclear abolition, peace and democracy", "Supports positioning, not a relation to other organizations."),
    source("EA-S020", "A093", "https://www.jichiro.okinawa/about.php", "自治労とは？｜自治労沖縄県本部", "n.d.", "organization_site", "E4", "yes", "no", "prefectural headquarters structure and membership", "Identity only."),
    source("EA-S021", "A093", "https://www.jichiro.okinawa/", "自治労沖縄県本部", "2021–2024 records", "organization_site_action_index", "E4", "yes", "yes_repeated_actions", "dated activity index: Henoko petitions/rallies, ‘local autonomy’ framing, 5.15 marches and Okinawa peace travel", "Index entries support visible actions; members-only detail may still require locator review."),
    source("EA-S022", "A094", "https://www.okifuren.com/", "一般社団法人 沖縄県女性連合会", "n.d.", "organization_site", "E4", "yes", "yes_statutory_purpose", "purpose and activities: gender equality, environmental conservation, world peace and international exchange", "Organizational purpose does not by itself show base-related action."),
    source("EA-S023", "A094", "https://www.okifuren.com/about.php", "女性連合会とは｜沖縄県女性連合会", "1948–2024 chronology", "organization_site_history", "E4", "yes_continuity", "yes_historical_actions", "history includes peace rallies, US-base return/removal requests and protests after base-related incidents", "Historical event records must retain dates; do not flatten them into a continuous alliance or identical stance across all periods."),
    source("EA-S024", "A095", "https://www.miyakomainichi.com/news/post-76312/", "止めよう「自衛隊配備」―70人の市民結集し結成会", "2015-05-31", "local_newspaper", "E2", "yes_secondary", "yes_foundation_event", "founding purpose, peaceful-life/target and planned-site water-source statements, intended signature activity", "Statements are reported at the founding meeting; claims about risk and water impacts remain attributed to the group/speakers."),
    source("EA-S025", "A095", "https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/017/050/inkaihou.compressed.pdf", "沖縄県議会委員会報：陸自ミサイル部隊の配備に関する陳情", "2017–2020", "official_legislative_record", "E4", "yes_named_petitioner", "yes_procedural_action", "petition index names A095/A096 and representatives for a missile-deployment petition", "Proves formal petitioning and issue connection, not acceptance of every substantive claim."),
    source("EA-S026", "A095", "https://www.miyakomainichi.com/news/post-81162/", "反対派市民が署名提出／陸自配備", "2015-10-06", "local_newspaper", "E2", "yes_secondary", "yes_event_specific", "16,439 signatures submitted and continued mobilization announced", "Signature count is an event record, not membership size or alliance strength."),
    source("EA-S027", "A096", "https://www.city.miyakojima.lg.jp/gyosei/gikai/files/h27.6.dai4kaikaigiroku.pdf", "宮古島市議会 平成27年6月定例会会議録", "2015", "official_legislative_record", "E4", "yes_named_petitioner", "yes_procedural_action", "petition No. 9: request opposing JSDF deployment, submitted by co-representative Sayoko Shimizu", "Proves a formal anti-deployment request; it does not prove all registry tags."),
    source("EA-S028", "A096", "https://www.miyakomainichi.com/2011/06/20401/", "下地島への自衛隊配備に反対／平和運動連絡協", "2011-06-25", "local_newspaper", "E2", "yes_secondary", "yes_event_specific", "A096-hosted meeting reached shared opposition to JSDF use of Shimojishima as a disaster-support base", "Reported event and speaker claims; do not infer a stable coalition from attendance."),
    source("EA-S029", "A097", "https://www.npo-mec.net/", "ホーム｜宮古島環境クラブ", "n.d.", "organization_site", "E4", "yes", "yes_positioning", "purpose and sustained work on Miyako nature, waterside protection/restoration and environmental education", "General environmental actor; no deployment stance is inferred."),
    source("EA-S030", "A097", "https://www.npo-mec.net/services", "宮古島環境クラブ（MEC）の活動とは？", "n.d.", "organization_site", "E4", "yes", "yes_program_specific", "explicit ‘地下水保全活動’ and waterside-nature programs", "Groundwater conservation is confirmed; no automatic military-facility linkage."),
    source("EA-S031", "A098", "https://econet.jpn.org/", "特定非営利活動法人 宮古島 海の環境ネットワーク", "n.d.", "organization_site", "E4", "yes", "yes_positioning", "marine-environment protection through beach cleaning, marine surveys and environmental education", "General marine/environment work; no anti-base stance inferred."),
    source("EA-S032", "A098", "https://econet.jpn.org/outline", "法人概要｜宮古島 海の環境ネットワーク", "n.d.", "organization_site", "E4", "yes", "yes_statutory_purpose", "purpose includes preserving Miyako marine nature and biological ecosystems", "Supports environment/biodiversity positioning only."),
    source("EA-S033", "A099", "https://darkwater.okinawa/about/", "連絡会について｜PFAS汚染から市民の生命を守る連絡会", "n.d.", "organization_site", "E4", "yes", "yes_positioning", "2019 formation; drinking-water contamination, health concern, safe-water demand and environmental persistence", "Base-source and health-effect statements are the organization’s attributed claims; actor–issue coding does not certify causation."),
    source("EA-S034", "A099", "https://darkwater.okinawa/pfas%E8%A1%80%E4%B8%AD%E6%BF%83%E5%BA%A6%E8%AA%BF%E6%9F%BB%E3%81%B8%E3%80%80%E5%B8%82%E6%B0%91%E9%80%A3%E7%B5%A1%E4%BC%9A%E3%81%8C%E6%8B%A1%E5%A4%A7%E5%B9%B9%E4%BA%8B%E4%BC%9A%EF%BC%885%E6%9C%8825/", "PFAS血中濃度調査へ 市民連絡会が拡大幹事会", "2022", "organization_action_record", "E4", "yes", "yes_event_specific", "group plan for blood testing and public epidemiological investigation", "Evidence of the group’s health-risk action; not independent validation of causal claims."),
    source("EA-S035", "A100", "https://www.city.uruma.lg.jp/documents/2778/163164165kaigiroku_2.pdf", "うるま市議会会議録：ミサイル配備から命を守るうるま市民の会", "2022", "official_legislative_record", "E4", "yes_named_group", "yes_issue_context", "council record notes the group formed in opposition to missile deployment and to protect residents’ life/property/safety", "Government minutes confirm public existence/context, not every movement claim."),
    source("EA-S036", "A100", "https://ryukyushimpo.jp/news/entry-1623776.html", "陸自勝連分屯地へのミサイル配備阻止へ「市民の会」発足", "2022-11-29", "main_local_newspaper", "E2", "yes_secondary", "yes_foundation_event", "group formation, prior photo exhibitions, target-risk and ‘do not make our islands a battlefield’ statements", "Reported statements remain attributed; fear of targeting is not coded as a proven future event."),
    source("EA-S037", "A100", "https://ryukyushimpo.jp/news/national/entry-2869997.html", "陸自ミサイル配備計画「反対を」―知事や県議会に要請", "2024-03-05", "main_local_newspaper", "E2", "yes_secondary", "yes_event_specific", "formal request, frontline/target reasoning and about 10,500 signatures", "Signature count and request are event-specific; no stable alliance inference."),
    source("EA-S038", "A101", "https://ryukyukohp.jimdofree.com/%E3%83%9B%E3%83%BC%E3%83%A0/%E6%B2%96%E7%B8%84-%E7%90%89%E7%90%83%E5%BC%A7%E3%81%AE%E5%A3%B0%E3%81%A8%E3%81%AF/", "沖縄・琉球弧の声とは", "2023-11-03", "organization_site", "E4", "yes", "yes_positioning", "purpose: publicize Okinawa/Ryukyu-arc voices in Japan and worldwide; explicit militarization, Taiwan-contingency, frontline, anti-war, human-rights and safe-life framing", "Organization-authored positioning; does not establish the truth of projected contingency scenarios."),
    source("EA-S039", "A101", "https://ryukyukohp.jimdofree.com/%E3%83%9B%E3%83%BC%E3%83%A0/%E7%AC%AC1%E5%9B%9E-2023-11-12/", "第1回連続講座（2023.11.12）", "2023-11-12", "organization_event_record", "E4", "yes", "yes_event_specific", "first lecture features Yonaguni/Yambaru/Mageshima militarization and natural-environment protection; online/international dissemination", "One event does not prove stable alliance among speakers or supporting groups."),
    source("EA-S040", "A101", "https://ryukyukohp.jimdofree.com/%E3%83%9B%E3%83%BC%E3%83%A0/%E5%A3%B0%E6%98%8E-%E6%8F%90%E8%A8%80/", "声明・提言｜沖縄・琉球弧の声を届ける会", "2025-10-27", "organization_statement", "E4", "yes_continuity", "yes_event_specific", "prefectural proposal after its environmental-assessment lecture seeks protection of Urasoe’s sea", "Event-specific environmental/procedural advocacy; not a general anti-development position."),
]

SOURCE_BY_KEY = {row["source_key"]: row for row in SOURCES}


def edge(
    actor_id: str,
    issue_id: str,
    claim: str,
    primary_source: str,
    scope: str,
    level: str,
    boundary: str,
    corroborating: str = "",
    conclusion: str = "candidate_ready_for_human_review",
    prior_human_anchor: str = "",
) -> dict[str, str]:
    src = SOURCE_BY_KEY[primary_source]
    return {
        "actor_id": actor_id,
        "actor_name": ACTORS[actor_id],
        "issue_id": issue_id,
        "issue_label": ISSUES[issue_id],
        "claim": claim,
        "primary_source_key": primary_source,
        "corroborating_source_keys": corroborating,
        "source_url": src["source_url"],
        "source_title": src["source_title"],
        "source_date": src["source_date"],
        "locator": src["locator"],
        "evidence_level": level,
        "scope": scope,
        "online_conclusion": conclusion,
        "identity_source_distinct": "same_source_but_separate_claim" if src["identity_support"].startswith("yes") else "yes",
        "explanation_boundary": boundary,
        "review_status": "ai_seeded",
        "needs_local_retrieval": "no",
        "prior_human_anchor": prior_human_anchor,
    }


EDGES = [
    edge("A076", "I004", "A076以具名原告身份参加保护冲绳儒艮及其栖息地的NHPA诉讼。", "EA-S002", "case", "E4", "仅为案件特定原告角色；不证明持续组织活动。", "EA-S001;EA-S003", prior_human_anchor="HR-014 R8C01/R8R004"),
    edge("A076", "I011", "A076通过美国NHPA司法程序对国防部的域外文化资源审查提出挑战。", "EA-S002", "case", "E4", "法律角色不得外推为其他案件角色。", "EA-S001", prior_human_anchor="HR-014 R8C01/R8R004"),
    edge("A076", "I003", "该诉讼直接针对普天间机场迁往边野古沿岸、可能影响儒艮栖息地的计划。", "EA-S001", "case", "E4", "这是案件议题连接，不等于A076在所有时期都有独立边野古行动。", "EA-S002", prior_human_anchor="HR-014 R8C01/R8R004"),
    edge("A086", "I004", "A086以美方具名原告身份参加冲绳儒艮保护诉讼。", "EA-S006", "case", "E4", "仅为案件特定角色。", "EA-S005", prior_human_anchor="HR-014 R8C01/R8R002"),
    edge("A086", "I011", "A086通过NHPA诉讼进入法律程序。", "EA-S006", "case", "E4", "不得外推为其他冲绳诉讼角色。", "EA-S005", prior_human_anchor="HR-014 R8C01/R8R002"),
    edge("A086", "I012", "A086作为美国海洋保护NGO原告，构成跨太平洋法律倡议路径的一环。", "EA-S005", "case", "E4", "跨国共同诉讼不是稳定组织联盟。", "EA-S006", prior_human_anchor="HR-014 R8C01/R8R002"),
    edge("A086", "I005", "A086参与的案件以珊瑚礁、海草床和濒危海洋物种栖息地受影响为核心事实背景。", "EA-S005", "case", "E4", "仅编码案件中的生物多样性连接，不把其全部全球项目纳入冲绳网络。", "EA-S004", prior_human_anchor="HR-014 R8C01/R8R002"),
    edge("A087", "I019", "法人定款和自有说明以世界恒久和平的创造为明确目的。", "EA-S007", "positioning", "E4", "法定目的不等于所有计划均已实施。", "EA-S008"),
    edge("A087", "I025", "法人目的明确包含废除战争与核武器。", "EA-S007", "positioning", "E4", "属于组织定位，不推断具体反基地行动。", "EA-S008"),
    edge("A087", "I015", "法人定款把国际合作与国际相互理解列为活动目的，并计划向世界提出网络纪念项目。", "EA-S007", "positioning", "E4", "国际意向不等于已形成国际合作关系。", "EA-S008"),
    edge("A088", "I019", "JICA官方组织介绍将OPAC界定为以和平为轴、开展和平学习与人才培养的机构。", "EA-S010", "positioning", "E4", "机构兼具安全保障研究功能，不应自动编码为反基地。", "EA-S011"),
    edge("A088", "I015", "OPAC持续开展国际和平合作，并作为指定团体参与柬埔寨和平博物馆人才培养项目。", "EA-S011", "case", "E4", "项目角色不等于资金金额或运动关系。", "EA-S010"),
    edge("A089", "I019", "沖教組把和平与民主教育作为持续组织目标。", "EA-S012", "positioning", "E4", "教育工会的和平定位不等于每个分会采取相同具体行动。"),
    edge("A089", "I025", "沖教組以“不再把学生送上战场”为基本理念。", "EA-S012", "positioning", "E4", "属于反战教育定位，不自动等于反对每一项军事政策。"),
    edge("A090", "I019", "高教組官网把和平、人权与环境学习列为活动，并持续参加5·15和平行进。", "EA-S014", "positioning", "E4", "共同参加行进不构成稳定联盟。"),
    edge("A090", "I001", "高教組官网将5·15和平行进表述为追求‘没有基地的和平冲绳’的年度活动。", "EA-S014", "event", "E4", "活动层连接，不外推为全部工会工作的单一定位。"),
    edge("A091", "I023", "连合沖縄在针对驻日美军人员性暴力的正式抗议中明确要求保障县民人权。", "EA-S016", "event", "E4", "事件特定；不把受害者信息或全部基地议题泛化。"),
    edge("A091", "I007", "同一抗议要求让县民安心生活，并把反复发生的事件事故表述为生活安全问题。", "EA-S016", "event", "E4", "组织的公开诉求不等于对事件因果作司法认定。", "EA-S017"),
    edge("A091", "I001", "连合沖縄会长公开提出推动米军基地整理缩小和地位协定修改。", "EA-S018", "positioning", "E4", "按2025年领导层公开方向编码，不写成跨期恒定立场。", "EA-S017"),
    edge("A091", "I003", "连合沖縄会长在2025年公开提出阻止边野古新基地建设。", "EA-S018", "positioning", "E4", "领导层声明需保持年份，不推断成员组织逐一同意。", "EA-S017"),
    edge("A091", "I019", "连合沖縄持续主办/参与‘平和行动in沖縄’并开展和平教育路线。", "EA-S017", "positioning", "E4", "项目参与不建立与每个参加团体的联盟边。"),
    edge("A092", "I001", "沖縄県労連的组织原则明确提出撤除基地。", "EA-S019", "positioning", "E4", "章程定位不等于具体地点行动。"),
    edge("A092", "I019", "沖縄県労連的组织原则明确提出维护和平与民主。", "EA-S019", "positioning", "E4", "仅为组织定位。"),
    edge("A092", "I025", "沖縄県労連明确反对军国主义复活并主张核武器废除。", "EA-S019", "positioning", "E4", "不自动等同于所有反部署组织的立场。"),
    edge("A093", "I003", "自治労沖縄県本部官网连续记录边野古新基地断念请愿与阻止建设集会。", "EA-S021", "positioning", "E4", "部分详细内容在会员区；正式采用前应复核具体条目定位。"),
    edge("A093", "I009", "自治労沖縄県本部官网以‘边野古问题关乎地方自治权’进行公开框架化。", "EA-S021", "positioning", "E4", "标题级材料需人工确认上下文后进入正式结论。"),
    edge("A093", "I019", "自治労沖縄県本部持续记录5·15和平行进与青年女性冲绳和平之旅。", "EA-S021", "positioning", "E4", "参与记录不等于稳定跨组织联盟。"),
    edge("A094", "I022", "沖縄県女性連合会以妇女会网络和男女共同参与为法定/公开核心目的。", "EA-S022", "positioning", "E4", "组织类型与女性议题连接成立，但不自动推断特定政治立场。"),
    edge("A094", "I019", "沖縄県女性連合会以建立世界和平为公开目的，并长期记录和平集会。", "EA-S022", "positioning", "E4", "历史记录应保留时期差异。", "EA-S023"),
    edge("A094", "I020", "沖縄県女性連合会把环境保全列入目的与活动。", "EA-S022", "positioning", "E4", "一般环境工作不自动指向基地环境争议。"),
    edge("A094", "I001", "组织沿革记录基地早期返还/撤去请求及基地事故后的抗议。", "EA-S023", "event", "E4", "按具体年份编码；不得压平为跨期稳定联盟。"),
    edge("A095", "I002", "A095以反对宫古岛自卫队/导弹部队部署为成立目的并正式提交陈情。", "EA-S025", "positioning", "E4", "陈情存在不证明其所有事实主张。", "EA-S024"),
    edge("A095", "I007", "成立会上共同代表把部署与岛民和平生活、成为攻击目标的风险相连。", "EA-S024", "event", "E2", "风险判断必须归属于组织/发言人，不作为已发生事实。"),
    edge("A095", "I006", "成立会上共同代表指出拟建基地地点涉及重要水源。", "EA-S024", "event", "E2", "这是组织公开提出的水源担忧；未由该报道独立验证环境影响。"),
    edge("A095", "I026", "A095与另一团体提交16,439人反部署署名并宣布继续动员。", "EA-S026", "event", "E2", "署名数量不是成员规模；共同提交不等于稳定联盟。"),
    edge("A096", "I002", "A096以具名请愿者身份正式反对宫古/下地岛自卫队部署。", "EA-S027", "case", "E4", "正式请愿角色不证明全部长期议题标签。", "EA-S025;EA-S028"),
    edge("A096", "I019", "A096主办集会并以和平运动框架形成反部署共识。", "EA-S028", "event", "E2", "地方新闻事件记录；参加者共识不是稳定联盟。"),
    edge("A097", "I020", "宮古島環境クラブ持续从事自然与环境保全、恢复和环境教育。", "EA-S029", "positioning", "E4", "一般环境定位，不推断军事部署立场。"),
    edge("A097", "I006", "宮古島環境クラブ官网明确列出地下水保全活动。", "EA-S030", "positioning", "E4", "只证明地下水保全，不自动连接自卫队设施。"),
    edge("A097", "I005", "宮古島環境クラブ持续保护水边自然并开展物种/生态教育。", "EA-S029", "positioning", "E4", "按一般生物多样性定位编码。"),
    edge("A098", "I020", "宮古島海の環境ネットワーク以海岸清扫、海洋调查和环境教育保护海洋环境。", "EA-S031", "positioning", "E4", "不推断反基地立场。"),
    edge("A098", "I005", "该NPO的法定目的明确包括维护宫古海域自然环境与生物生态系统。", "EA-S032", "positioning", "E4", "一般生物多样性定位。"),
    edge("A099", "I006", "A099因北谷净水场水源与自来水PFAS污染担忧而成立，并要求安全饮水。", "EA-S033", "positioning", "E4", "污染来源与健康影响均保持为组织主张；edge不认证因果。"),
    edge("A099", "I008", "A099围绕PFAS潜在健康影响开展血液检测与公共健康调查倡议。", "EA-S034", "positioning", "E4", "证明组织行动，不作为医学因果结论。", "EA-S033"),
    edge("A099", "I007", "A099以保障市民生命与可安心饮用的水为持续公开目标。", "EA-S033", "positioning", "E4", "生活安全框架不等于已证明个体健康损害。"),
    edge("A099", "I020", "A099把PFAS界定为持续存在的环境污染问题并开展调查/倡议。", "EA-S033", "positioning", "E4", "组织表述需与政府科学评估分开。", "EA-S034"),
    edge("A100", "I002", "A100为反对胜连分屯地导弹部队部署而成立并持续请求撤回。", "EA-S035", "positioning", "E4", "官方会议录确认组织与议题；具体风险判断另行归属。", "EA-S036;EA-S037"),
    edge("A100", "I007", "A100公开将导弹部署与居民生命、安全及学校周边风险相连。", "EA-S036", "event", "E2", "风险陈述属于组织/报道中的发言，不作预测事实。", "EA-S037"),
    edge("A100", "I017", "A100在成立与后续行动中提出不让岛屿成为战场、避免基地成为攻击目标。", "EA-S036", "positioning", "E2", "前线化判断是组织框架，不是已发生事实。", "EA-S037"),
    edge("A100", "I018", "A100把‘台湾有事’情境下的目标化风险作为反部署说明的一部分。", "EA-S036", "event", "E2", "仅记录公开议题框架，不对情境概率作判断。"),
    edge("A100", "I026", "A100开展照片展、约10,500人署名、要请与搬入抗议等持续动员。", "EA-S037", "positioning", "E2", "署名与行动不建立与其他团体的稳定联盟。", "EA-S036"),
    edge("A101", "I002", "A101的趣意书以反对琉球弧自卫队基地、导弹与弹药部署为核心议题。", "EA-S038", "positioning", "E4", "组织自身框架，不等于军事政策事实的独立判定。"),
    edge("A101", "I017", "A101把冲绳/琉球弧被置于最前线和再度战场化的风险作为持续框架。", "EA-S038", "positioning", "E4", "前线化为分析/倡议框架，不写成已发生结果。"),
    edge("A101", "I018", "A101明确围绕台湾有事叙事、岛屿部署与居民风险开展系列讲座。", "EA-S038", "positioning", "E4", "不判断台湾有事发生概率。"),
    edge("A101", "I025", "A101以反对军事化和战争、避免重演冲绳战为组织目标。", "EA-S038", "positioning", "E4", "反战定位不等于与所有反战团体结盟。"),
    edge("A101", "I023", "A101把表达/报道自由与保障人权列为连续讲座的核心论点。", "EA-S038", "positioning", "E4", "属于组织公开定位。"),
    edge("A101", "I012", "A101明确以向日本本土与海外媒体、组织和市民传播琉球弧市民声音为目的。", "EA-S038", "positioning", "E4", "传播意图与线上输出不等于已建立稳定国际组织关系。", "EA-S039"),
    edge("A101", "I020", "A101主办环境影响评价讲座并向县知事提交保护浦添海域的具体提言。", "EA-S040", "event", "E4", "事件特定环境/程序倡议，不推断一般反开发立场。", "EA-S039"),
]

UNRESOLVED = {
    "A073": "exact entity identity; legal status; activity continuity; any direct Phase-1 issue link",
    "A076": "post-case continuity, founding/legal status and current organization-level activity remain HR-001/local-retrieval questions",
    "A086": "whether to retain biodiversity and international-advocacy mappings as separate issue edges rather than one legal-case bundle",
    "A087": "whether international_cooperation describes implemented work or statutory aspiration",
    "A088": "security/human-security vocabulary is outside the present 26-issue taxonomy; no anti-base inference",
    "A089": "Henoko evidence is branch-attributed and is not proposed as a formal edge in this batch",
    "A090": "mobilization and anti-war remain uncoded pending scope preference",
    "A091": "time-bounded leadership statements require HR-010 scope review",
    "A092": "specific event/place actions not yet separately coded",
    "A093": "some detail pages are members-only; title-level locators require HR-010",
    "A094": "historical base actions require date-specific review",
    "A095": "groundwater claim is a reported group concern, not an independently verified impact finding",
    "A096": "long-term continuity after the documented petitions/events is not fully visible online",
    "A097": "no direct military-deployment link found or inferred",
    "A098": "no direct military-deployment link found or inferred",
    "A099": "causal source and medical effects remain attributed claims/scientific questions",
    "A100": "no organization-controlled site found; event claims rely on official minutes and major local press",
    "A101": "scenario claims remain attributed; supporting groups are not alliance edges",
}

SEARCHES = {
    "A073": ('"琉球沖縄国際支援プログラム" | "琉球・沖縄国際支援プログラム" | "Ryukyu Okinawa International Support Program"', "general web; Japanese/English exact-name and variant searches", "0", "No exact organization or program record found; S033 is generic academic context and does not identify this entity."),
    "A076": ('"ジュゴン保護基金委員会" | "Save the Dugong Foundation"', "GovInfo; Earthjustice; JELF; Ryukyu Shimpo", "multiple", "Case-specific identity and direct issue link closed; continuity/legal status remain local."),
    "A086": ('site:seaturtles.org Okinawa dugong | Turtle Island Restoration Network mission', "TIRN filings; Earthjustice; GovInfo", "multiple", "Identity and case-specific issue links closed."),
    "A087": ('"世界版「平和の礎」を提案する会"', "Cabinet Office NPO portal; organization site", "multiple", "Identity and statutory positioning closed."),
    "A088": ('"沖縄平和協力センター" 国際平和協力 | site:opac.or.jp', "Cabinet Office NPO portal; JICA; OPAC", "multiple", "Peace and international-cooperation links closed; no movement stance inferred."),
    "A089": ('site:oki-tu.org 沖縄県教職員組合 平和 基地', "organization site and branch pages", "multiple", "Peace/anti-war links closed; branch Henoko attribution held back."),
    "A090": ('site:oki-htu.or.jp 沖縄県高等学校障害児学校教職員組合 平和 基地', "organization site", "multiple", "Peace and base-free march links closed."),
    "A091": ('site:rengo-okinawa.jp 米軍 基地 要請 辺野古 平和', "organization site/action archive", "multiple", "Human-rights/life-safety/base/Henoko/peace candidates found."),
    "A092": ('site:okinawakenroren.org 沖縄県労連 基地 撤去 平和', "organization site", "multiple", "Charter-level base/peace/anti-war links closed."),
    "A093": ('site:jichiro.okinawa 辺野古 平和行進 地方自治', "organization site/action index", "multiple", "Henoko/autonomy/peace links found; some locators members-only."),
    "A094": ('site:okifuren.com 沖縄県女性連合会 平和 環境 基地', "organization site/history", "multiple", "Women/peace/environment and dated base-action links found."),
    "A095": ('"止めよう「自衛隊配備」宮古郡民の会"', "Okinawa legislature; Miyako Mainichi; Ryukyu Shimpo", "multiple", "Anti-deployment, life-safety, groundwater concern and mobilization found."),
    "A096": ('"宮古平和運動連絡協議会" 自衛隊 配備', "Miyakojima council; Okinawa legislature; Miyako Mainichi", "multiple", "Formal anti-deployment and peace-framed event found."),
    "A097": ('site:npo-mec.net 宮古島環境クラブ 地下水', "organization site", "multiple", "Environment/groundwater/biodiversity positioning found; no military link inferred."),
    "A098": ('site:econet.jpn.org 宮古島海の環境ネットワーク 活動', "organization site", "multiple", "Marine environment/biodiversity positioning found; no military link inferred."),
    "A099": ('site:darkwater.okinawa PFAS 嘉手納 水道水 健康調査', "organization site; Okinawa Prefecture health committee context", "multiple", "Groundwater/health/life-safety/environment links found with causality caveat."),
    "A100": ('"ミサイル配備から命を守るうるま市民の会"', "Uruma council; Ryukyu Shimpo; Okinawa Times; Akahata", "multiple", "Anti-deployment/life-safety/frontline/Taiwan/mobilization links found; no own site."),
    "A101": ('site:ryukyukohp.jimdofree.com 沖縄 琉球弧 声を届ける会', "organization multilingual site, event archive and statements", "multiple", "Security/frontline/Taiwan/anti-war/human-rights/international/environment links found."),
}


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for index, row in enumerate(EDGES, 1):
        row["activation_id"] = f"EA{index:03d}"
    edge_fields = ["activation_id"] + [key for key in EDGES[0] if key != "activation_id"]
    write_csv(DATA, EDGES, edge_fields)
    write_csv(OUT / "source_evidence_crosswalk_v1.csv", SOURCES)

    by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in EDGES:
        by_actor[row["actor_id"]].append(row)

    conclusions = []
    for actor_id, actor_name in ACTORS.items():
        actor_edges = by_actor[actor_id]
        levels = {row["evidence_level"] for row in actor_edges}
        if actor_id == "A073":
            identity_status = "unverified_online"
            direct_status = "online_exhausted_no_edge"
            conclusion = "online_exhausted_needs_local_or_registry_reconsideration"
            local = "yes"
        elif actor_id == "A076":
            identity_status = "named_case_party_confirmed_continuity_unresolved"
            direct_status = "case_specific_candidates_found"
            conclusion = "activate_case_layer_after_HR024; retain continuity gap"
            local = "yes"
        else:
            identity_status = "online_verified"
            direct_status = "candidate_edges_found"
            conclusion = "candidate_activation_pending_human_review"
            local = "no"
        conclusions.append({
            "actor_id": actor_id,
            "actor_name": actor_name,
            "identity_online_status": identity_status,
            "direct_issue_status": direct_status,
            "candidate_edge_count": str(len(actor_edges)),
            "candidate_issue_ids": ";".join(row["issue_id"] for row in actor_edges),
            "strongest_evidence_level": "E4" if "E4" in levels else ("E2" if "E2" in levels else "none"),
            "unresolved_after_online_pass": UNRESOLVED[actor_id],
            "online_conclusion": conclusion,
            "needs_local_retrieval": local,
        })
    write_csv(OUT / "actor_online_conclusions_v1.csv", conclusions)

    search_rows = []
    source_counts = Counter(row["actor_id"] for row in SOURCES)
    for actor_id, (queries, domains, hits, outcome) in SEARCHES.items():
        search_rows.append({
            "actor_id": actor_id,
            "actor_name": ACTORS[actor_id],
            "queries": queries,
            "domains_or_source_families_checked": domains,
            "exact_name_hits": hits,
            "retained_source_records": str(source_counts[actor_id]),
            "candidate_edge_count": str(len(by_actor[actor_id])),
            "online_outcome": outcome,
            "searched_on": ACCESSED,
        })
    write_csv(OUT / "online_search_log_v1.csv", search_rows)

    hr024_rows = [{
        "task_id": "HR024-001",
        "review_object": "identity_and_registry_retention",
        "actor_id": "A073",
        "actor_name": ACTORS["A073"],
        "issue_id": "",
        "claim_or_question": "多轮日/英精确名称检索无可核实体；S033不支持该组织身份。应保留待当地核实、纠正名称，还是移出registry？",
        "source_keys": "",
        "evidence_level": "E0",
        "scope": "identity",
        "prior_human_anchor": "",
        "decision": "",
        "reviewer": "",
        "review_date": "",
        "review_note": "",
    }]
    next_id = 2
    for row in EDGES:
        if row["actor_id"] not in {"A076", "A086"}:
            continue
        hr024_rows.append({
            "task_id": f"HR024-{next_id:03d}",
            "review_object": "actor_issue_edge_mapping",
            "actor_id": row["actor_id"],
            "actor_name": row["actor_name"],
            "issue_id": row["issue_id"],
            "claim_or_question": row["claim"],
            "source_keys": ";".join(filter(None, [row["primary_source_key"], row["corroborating_source_keys"]])),
            "evidence_level": row["evidence_level"],
            "scope": row["scope"],
            "prior_human_anchor": row["prior_human_anchor"],
            "decision": "",
            "reviewer": "",
            "review_date": "",
            "review_note": "",
        })
        next_id += 1
    write_csv(OUT / "HR024_edge_activation_review_v0.csv", hr024_rows)

    hr010_rows = []
    for index, row in enumerate((r for r in EDGES if r["actor_id"] >= "A087"), 1):
        hr010_rows.append({
            "task_id": f"HR010-B6-{index:03d}",
            "review_object": "edge_evidence_addendum",
            "actor_id": row["actor_id"],
            "actor_name": row["actor_name"],
            "issue_id": row["issue_id"],
            "issue_label": row["issue_label"],
            "claim": row["claim"],
            "source_keys": ";".join(filter(None, [row["primary_source_key"], row["corroborating_source_keys"]])),
            "evidence_level": row["evidence_level"],
            "scope": row["scope"],
            "explanation_boundary": row["explanation_boundary"],
            "decision": "",
            "reviewer": "",
            "review_date": "",
            "review_note": "",
        })
    write_csv(OUT / "HR010_batch6_edge_evidence_addendum_v0.csv", hr010_rows)

    # Post-HR013 current-use layer.  IDs are deliberately not renumbered: gaps
    # preserve a stable crosswalk back to the pre-HR013 acquisition snapshot.
    post_actor_ids = [actor_id for actor_id in ACTORS if actor_id not in POST_HR013_EXCLUSIONS]
    post_edges = [row for row in EDGES if row["actor_id"] in post_actor_ids]
    post_sources = [row for row in SOURCES if row["actor_id"] in post_actor_ids]
    post_conclusions = [row for row in conclusions if row["actor_id"] in post_actor_ids]
    post_search_rows = [row for row in search_rows if row["actor_id"] in post_actor_ids]
    post_hr010_rows = [row for row in hr010_rows if row["actor_id"] in post_actor_ids]

    write_csv(OUT / "post_hr013_edge_activation_candidates_v1.csv", post_edges, edge_fields)
    write_csv(OUT / "post_hr013_source_evidence_crosswalk_v1.csv", post_sources)
    write_csv(OUT / "post_hr013_actor_online_conclusions_v1.csv", post_conclusions)
    write_csv(OUT / "post_hr013_online_search_log_v1.csv", post_search_rows)
    write_csv(OUT / "post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv", post_hr010_rows)

    disposition_rows = []
    for actor_id, disposition in POST_HR013_EXCLUSIONS.items():
        actor_edges = [row for row in EDGES if row["actor_id"] == actor_id]
        actor_sources = [row for row in SOURCES if row["actor_id"] == actor_id]
        actor_hr010 = [row for row in hr010_rows if row["actor_id"] == actor_id]
        disposition_rows.append({
            "actor_id": actor_id,
            "actor_name": ACTORS[actor_id],
            "human_decision_ref": disposition["human_decision_ref"],
            "human_decision": disposition["human_decision"],
            "current_queue_disposition": "excluded_after_human_rejection",
            "affected_activation_ids": ";".join(row["activation_id"] for row in actor_edges),
            "affected_source_keys": ";".join(row["source_key"] for row in actor_sources),
            "affected_HR010_task_ids": ";".join(row["task_id"] for row in actor_hr010),
            "reason": disposition["reason"],
        })
    write_csv(OUT / "post_hr013_disposition_v1.csv", disposition_rows)

    issue_counts = Counter(row["issue_label"] for row in EDGES)
    identity_covered = {
        actor_id
        for actor_id in ACTORS
        if any(row["actor_id"] == actor_id and row["identity_support"].startswith("yes") for row in SOURCES)
    }
    direct_covered = {
        actor_id
        for actor_id in ACTORS
        if any(row["actor_id"] == actor_id and row["direct_issue_support"].startswith("yes") for row in SOURCES)
    }
    validation_rows = [
        {"metric": "target_actor_count", "value": str(len(ACTORS)), "expected": "18", "status": "pass" if len(ACTORS) == 18 else "fail"},
        {"metric": "actor_conclusion_count", "value": str(len(conclusions)), "expected": "18", "status": "pass" if len(conclusions) == 18 else "fail"},
        {"metric": "actors_with_candidate_edge", "value": str(sum(bool(by_actor[a]) for a in ACTORS)), "expected": "17", "status": "pass" if sum(bool(by_actor[a]) for a in ACTORS) == 17 else "fail"},
        {"metric": "candidate_edge_count", "value": str(len(EDGES)), "expected": ">=17", "status": "pass" if len(EDGES) >= 17 else "fail"},
        {"metric": "source_record_count", "value": str(len(SOURCES)), "expected": ">=17", "status": "pass" if len(SOURCES) >= 17 else "fail"},
        {"metric": "actors_with_identity_source", "value": str(len(identity_covered)), "expected": "17", "status": "pass" if len(identity_covered) == 17 and "A073" not in identity_covered else "fail"},
        {"metric": "actors_with_direct_issue_source", "value": str(len(direct_covered)), "expected": "17", "status": "pass" if len(direct_covered) == 17 and "A073" not in direct_covered else "fail"},
        {"metric": "HR024_blank_decisions", "value": str(sum(not r["decision"] for r in hr024_rows)), "expected": str(len(hr024_rows)), "status": "pass" if all(not r["decision"] and not r["reviewer"] and not r["review_date"] and not r["review_note"] for r in hr024_rows) else "fail"},
        {"metric": "HR010_batch6_blank_decisions", "value": str(sum(not r["decision"] for r in hr010_rows)), "expected": str(len(hr010_rows)), "status": "pass" if all(not r["decision"] and not r["reviewer"] and not r["review_date"] and not r["review_note"] for r in hr010_rows) else "fail"},
        {"metric": "A073_online_exhausted", "value": conclusions[0]["direct_issue_status"], "expected": "online_exhausted_no_edge", "status": "pass" if conclusions[0]["direct_issue_status"] == "online_exhausted_no_edge" else "fail"},
    ]
    write_csv(OUT / "validation_summary_v1.csv", validation_rows)

    post_by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in post_edges:
        post_by_actor[row["actor_id"]].append(row)
    post_identity_covered = {
        actor_id
        for actor_id in post_actor_ids
        if any(row["actor_id"] == actor_id and row["identity_support"].startswith("yes") for row in post_sources)
    }
    post_direct_covered = {
        actor_id
        for actor_id in post_actor_ids
        if any(row["actor_id"] == actor_id and row["direct_issue_support"].startswith("yes") for row in post_sources)
    }
    post_validation_rows = [
        {"metric": "post_HR013_target_actor_count", "value": str(len(post_actor_ids)), "expected": "17", "status": "pass" if len(post_actor_ids) == 17 else "fail"},
        {"metric": "post_HR013_actor_conclusion_count", "value": str(len(post_conclusions)), "expected": "17", "status": "pass" if len(post_conclusions) == 17 else "fail"},
        {"metric": "post_HR013_actors_with_candidate_edge", "value": str(sum(bool(post_by_actor[a]) for a in post_actor_ids)), "expected": "16", "status": "pass" if sum(bool(post_by_actor[a]) for a in post_actor_ids) == 16 else "fail"},
        {"metric": "post_HR013_candidate_edge_count", "value": str(len(post_edges)), "expected": "54", "status": "pass" if len(post_edges) == 54 else "fail"},
        {"metric": "post_HR013_source_record_count", "value": str(len(post_sources)), "expected": "38", "status": "pass" if len(post_sources) == 38 else "fail"},
        {"metric": "post_HR013_actors_with_identity_source", "value": str(len(post_identity_covered)), "expected": "16", "status": "pass" if len(post_identity_covered) == 16 and "A073" not in post_identity_covered else "fail"},
        {"metric": "post_HR013_actors_with_direct_issue_source", "value": str(len(post_direct_covered)), "expected": "16", "status": "pass" if len(post_direct_covered) == 16 and "A073" not in post_direct_covered else "fail"},
        {"metric": "post_HR013_HR024_blank_decisions", "value": str(sum(not r["decision"] for r in hr024_rows)), "expected": "8", "status": "pass" if len(hr024_rows) == 8 and all(not r["decision"] and not r["reviewer"] and not r["review_date"] and not r["review_note"] for r in hr024_rows) else "fail"},
        {"metric": "post_HR013_HR010_batch6_blank_decisions", "value": str(sum(not r["decision"] for r in post_hr010_rows)), "expected": "47", "status": "pass" if len(post_hr010_rows) == 47 and all(not r["decision"] and not r["reviewer"] and not r["review_date"] and not r["review_note"] for r in post_hr010_rows) else "fail"},
        {"metric": "post_HR013_excluded_A094_rows", "value": str(sum(row["actor_id"] == "A094" for row in post_edges + post_sources + post_conclusions + post_search_rows + post_hr010_rows)), "expected": "0", "status": "pass" if all(row["actor_id"] != "A094" for row in post_edges + post_sources + post_conclusions + post_search_rows + post_hr010_rows) else "fail"},
        {"metric": "post_HR013_disposition_recorded", "value": str(len(disposition_rows)), "expected": "1", "status": "pass" if len(disposition_rows) == 1 and disposition_rows[0]["actor_id"] == "A094" else "fail"},
    ]
    write_csv(OUT / "post_hr013_validation_summary_v1.csv", post_validation_rows)

    if any(row["status"] != "pass" for row in validation_rows):
        raise SystemExit("edge activation validation failed")
    if any(row["status"] != "pass" for row in post_validation_rows):
        raise SystemExit("post-HR013 edge activation validation failed")
    if len({row["activation_id"] for row in EDGES}) != len(EDGES):
        raise SystemExit("duplicate activation_id")
    for row in EDGES:
        if row["primary_source_key"] not in SOURCE_BY_KEY:
            raise SystemExit(f"missing source: {row['primary_source_key']}")
        if SOURCE_BY_KEY[row["primary_source_key"]]["actor_id"] != row["actor_id"]:
            raise SystemExit(f"source/actor mismatch: {row['activation_id']}")
        if row["scope"] not in {"positioning", "case", "event"}:
            raise SystemExit(f"bad scope: {row['activation_id']}")
        for key in ("actor_id", "issue_id", "claim", "source_url", "source_title", "source_date", "locator", "evidence_level", "scope", "online_conclusion", "explanation_boundary"):
            if not row[key]:
                raise SystemExit(f"missing {key}: {row['activation_id']}")

    thin = ["groundwater", "health_risk", "environment", "women", "human_rights", "international_cooperation", "international_advocacy", "frontline_prevention", "Taiwan_contingency"]
    brief = f"""# edge-isolated actor 在线补证 brief v1

## 取证快照（HR-013 前）

- 18/18 已逐项检索并形成可回溯结论。
- 17 个 actor 找到至少一条直接 actor–issue 候选，共 {len(EDGES)} 条；全部仍待人审，未写回主表。
- A073 `琉球沖縄国際支援プログラム` 在多轮日/英精确名称与变体检索中没有可核实体；现有 S033 只是泛化学术背景，不能证明身份。该对象标为 `online_exhausted_needs_local_or_registry_reconsideration`。
- A076/A086 的诉讼事实继承 HR-014 案件锚点，但“案件角色 → issue edge”的映射仍进入 HR-024，不能由 AI 自动批准。
- A087–A101 原本就在未完成 HR-010 的分类/新增边范围内，因此不重复编号：本包提供 `HR010_batch6_edge_evidence_addendum_v0.csv`。补证不等于 HR-010 已完成。

## HR-013 后当前队列

- HR-013 已将 A094 `沖縄県女性連合会` 判为一般妇人会并剔除；其 4 条候选边、2 条来源提案和 4 个 HR-010 addendum 项只保留为取证历史，不得回流 registry 或当前复核队列。
- 当前可用过滤层为 17 个保留对象、16 个有候选边的 actor、{len(post_edges)} 条候选边和 {len(post_sources)} 条来源；HR-010 batch 6 当前队列为 {len(post_hr010_rows)} 项，原 task/activation ID 不重排。
- 当前复核应使用 `post_hr013_*` 文件；HR-024 仍为 A073/A076/A086 的 {len(hr024_rows)} 项，不受 A094 处置影响。

## 薄议题得到的候选补强

{chr(10).join(f'- `{name}`：{issue_counts[name]} 条候选' for name in thin)}

以上为 HR-013 前取证快照计数。groundwater 由 A095（部署地点水源担忧）、A097（持续地下水保全）和 A099（PFAS/饮用水）三种不同机制进入；health_risk 只由 A099 的调查/倡议进入，不能写成医学因果。HR-013 后 A094 的 women/environment 等候选不再进入当前队列；保留的 environment 候选来自 A097/A098/A099/A101，仍须区分一般环境定位、污染倡议与事件性环境程序。

## 强制解释边界

1. 所有候选仅是 actor–issue 连接，不是 actor–actor 联盟。
2. A076/A086 只确认 Dugong 案件角色，不外推其他案件或持续组织活动。
3. A088 是和平/国际合作机构，不因研究基地或安全保障而编码为反基地 actor。
4. A097/A098 的一般环境工作不自动连接军事部署。
5. A099 的污染来源与健康影响保持组织归属；edge 不认证因果。
6. A095/A100 的目标化、前线化与台湾有事情境是公开框架，不是预测事实。
7. A089 的边野古材料来自国头支部，本批未提出 A089–Henoko 正式 edge。

## 文件

- `data/interim/28_edge_activation_candidates_v1.csv`：{len(EDGES)} 条候选边及逐条来源/locator/边界。
- `source_evidence_crosswalk_v1.csv`：{len(SOURCES)} 条来源，明确拆分 identity support 与 direct issue support。
- `actor_online_conclusions_v1.csv`：18/18 逐项结论。
- `online_search_log_v1.csv`：每个 actor 的查询、来源家族与线上结论。
- `HR024_edge_activation_review_v0.csv`：A073/A076/A086 的 {len(hr024_rows)} 项新问题，决定栏全空。
- `HR010_batch6_edge_evidence_addendum_v0.csv`：HR-013 前 51 条取证快照，决定栏全空，不再作为当前队列。
- `post_hr013_edge_activation_candidates_v1.csv`：当前 {len(post_edges)} 条候选边。
- `post_hr013_source_evidence_crosswalk_v1.csv`：当前 {len(post_sources)} 条来源提案。
- `post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`：当前 {len(post_hr010_rows)} 项，决定栏全空。
- `post_hr013_disposition_v1.csv`：A094 的 HR-013 排除处置及受影响 ID。
- `post_hr013_validation_summary_v1.csv`：过滤层机械验收。
"""
    (OUT / "edge_activation_brief_v1.md").write_text(brief, encoding="utf-8")

    guide = f"""# HR-024 与 HR-010 batch 6 复核说明

## HR-024（{len(hr024_rows)}项）

- HR024-001：A073 身份与 registry 去留；线上未找到可核实体，不能从 issue_tags 反推 edge。
- 其余项目：A076/A086 已经 HR-014 确认的 Dugong 案件角色，是否映射为相应 issue edge，以及 scope 是否保持 `case`。
- A076 的持续性、法律身份仍沿用 HR-001/当地补查，不在本包伪闭合。

## HR-010 edge-evidence addendum / batch 6

- `HR010_batch6_edge_evidence_addendum_v0.csv` 是 HR-013 前 51 项取证快照；其中 A094 的 4 项已被 HR-013 排除，不再送审。
- 当前请使用 `post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`（{len(post_hr010_rows)}项）。A087–A093、A095–A101 属于原 HR-010 未完成范围；本表只是新补的 edge-level evidence，不另建 HR-024。
- 为保持取证谱系，post-HR013 表保留原 task ID，A094 对应 ID 空缺不重排。
- `decision/reviewer/review_date/review_note` 全部故意留空。
- 可用决定建议词：`accept` / `revise_scope` / `defer` / `reject`。这只是填写词表，不是预填结论。

## 复核顺序

1. 先核 actor 归属：总会、分支、人员或临时活动是否被混同。
2. 再核 issue 映射：来源是否直接支持该 issue，而非来自 registry 标签。
3. 再核 scope：`positioning`、`case`、`event` 三选一。
4. 最后核解释边界：事件参与不升为联盟；组织主张不升为事实因果；服务/行政机构不推断政治立场。
"""
    (OUT / "HR_review_guide_v0.md").write_text(guide, encoding="utf-8")

    readme = """# edge_activation_v1

R1/R2 edge-isolated actor 的在线补证包。运行：

```powershell
python scripts\\make_edge_activation_v1.py
```

`data/interim/28_edge_activation_candidates_v1.csv` 和未带 `post_hr013_` 的表保留 HR-013 前 18 actor / 58 edge / 40 source 的取证快照。HR-013 已人工剔除 A094；当前复核和后续合并必须使用本目录的 `post_hr013_*` 过滤表（17 actor / 54 edge / 38 source；HR-010 47 项）。

脚本只生成本目录和 `data/interim/28_edge_activation_candidates_v1.csv`；不读取或修改 registry、actor–issue 主表、source log 或中央文档。中央 registry 即使已移除 A094，脚本仍可重复运行；A094 只会出现在明确标为历史快照/排除处置的文件中。
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print(
        f"snapshot_actors={len(ACTORS)} snapshot_edges={len(EDGES)} snapshot_sources={len(SOURCES)} "
        f"post_HR013_actors={len(post_actor_ids)} post_HR013_edges={len(post_edges)} "
        f"post_HR013_sources={len(post_sources)} HR024={len(hr024_rows)} "
        f"HR010_snapshot={len(hr010_rows)} HR010_post_HR013={len(post_hr010_rows)}"
    )


if __name__ == "__main__":
    build()
