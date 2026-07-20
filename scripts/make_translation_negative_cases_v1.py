#!/usr/bin/env python3
"""Build and validate the research-only translation negative-case package.

This builder is intentionally additive.  It reads the existing 13-episode
comparison only to describe its selection boundary and writes solely under
outputs/translation_negative_cases_v1.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "translation_negative_cases_v1"
BASELINE = (
    ROOT
    / "outputs"
    / "translation_episode_comparison_v1"
    / "translation_episode_candidates_v1.csv"
)
RUN_DATE = "2026-07-20"

CASE_FIELDS = [
    "case_id",
    "short_label",
    "gate_family",
    "claim",
    "claim_date",
    "actor",
    "actor_registry_status",
    "target_venue",
    "entry_attempt",
    "entry_gate",
    "formal_acceptance",
    "intermediate_output",
    "limited_relief",
    "substantive_change",
    "source_refs",
    "locator",
    "evidence_type",
    "candidate_status",
    "review_status",
    "package_status",
    "frontend_status",
    "central_writeback",
    "competing_explanation",
    "selection_reason",
    "interpretation_limit",
]

CASES = [
    {
        "case_id": "TN01",
        "short_label": "宫古2016住民投票陳情不採択",
        "gate_family": "legislative_petition_gate",
        "claim": (
            "要求就宫古岛市陆上自卫队驻屯地建设与配备计划实施住民投票，"
            "并设置包含市民与有识者的住民投票条例策定委员会。"
        ),
        "claim_date": "2016-09-06/2016-09-29",
        "actor": "てぃだぬふぁ島の子の平和な未来をつくる会（楚南有香子；石嶺香織）",
        "actor_registry_status": "named_civic_group_not_in_current_registry",
        "target_venue": "宫古岛市议会第7回定例会・总务财政委员会",
        "entry_attempt": "陳情書第26号",
        "entry_gate": "议会受理、委员会审查与全会採択判断",
        "formal_acceptance": "docketed_and_deliberated_not_adopted",
        "intermediate_output": (
            "官方案件登记、委员会公开审查与2016-09-29不採択结果记录"
        ),
        "limited_relief": "no_relief_from_this_petition",
        "substantive_change": "not_demonstrated_by_this_proceeding",
        "source_refs": "TNS001;TNS002;TNS003;TNS004",
        "locator": (
            "TNS001 PDF p.4 陳情書第26号；TNS002会議録案件处理与审议；"
            "TNS003正文第65–69行；TNS004正文第131–150行"
        ),
        "evidence_type": "E4_official_disposition_plus_two_local_reports",
        "candidate_status": "candidate",
        "review_status": "ai_seeded",
        "package_status": "research_only",
        "frontend_status": "not_frontend_ready",
        "central_writeback": "no",
        "competing_explanation": (
            "不採択可能来自议会既有配备立场、对直接请求方式的偏好、"
            "对策定委员会设计的异议或时机判断；不能简化为制度完全拒绝听取。"
        ),
        "selection_reason": (
            "同一官方档案同时锁定提出者、诉求、受理、审查和不採択，"
            "能观察到‘进入议会后被阻断’而非‘未能入场’。"
        ),
        "interpretation_limit": (
            "本案只证明该份陳情被正式处理后不採択；不代表所有宫古住民投票请求"
            "均被阻断，也不证明市议会从未讨论部署问题。"
        ),
    },
    {
        "case_id": "TN02",
        "short_label": "PFAS公害调停因防卫设施除外而却下",
        "gate_family": "administrative_eligibility_gate",
        "claim": (
            "围绕美军基地周边PFAS问题，请求基地内立入调查、由国家持续负担对策费用"
            "等三项措施，并希望通过县公害审查会调停推进事实查明与协商。"
        ),
        "claim_date": "2025-10-27/2026-02-21",
        "actor": (
            "A113 宜野湾ちゅら水会；A099 PFAS汚染から市民の生命を守る連絡会；"
            "#コドソラ（registry未确认）"
        ),
        "actor_registry_status": "two_registry_actors_plus_one_unresolved_coapplicant",
        "target_venue": "冲绳县公害审查会・公害调停程序",
        "entry_attempt": "公害调停申请书",
        "entry_gate": "公害纷争处理法的对象适格；防卫设施相关公害适用除外",
        "formal_acceptance": "application_received_then_dismissed_as_ineligible_before_mediation",
        "intermediate_output": (
            "却下决定书的内容由申请团体公开并被多家媒体报道；审查会同时留下"
            "对居民不安的理解及促请国家调查、法制化的非拘束性意见"
        ),
        "limited_relief": "discursive_recognition_only_nonbinding",
        "substantive_change": "unknown_not_tested_in_mediation",
        "source_refs": "TNS005;TNS006;TNS007;TNS008",
        "locator": (
            "TNS005正文第171–194行；TNS006正文第68–69行；"
            "TNS007正文第166–184行；TNS008正文第193–223行"
        ),
        "evidence_type": "E3_outcome_reports_plus_E4_official_procedure",
        "candidate_status": "candidate",
        "review_status": "ai_seeded",
        "package_status": "research_only",
        "frontend_status": "not_frontend_ready",
        "central_writeback": "no",
        "competing_explanation": (
            "这是法定对象适格／管辖边界，不是对PFAS污染事实、污染源或健康影响的"
            "实体判断；程序排除与诉求证据不足是不同解释。冲绳县官方终结事件库还"
            "显示，同一第50条门槛至少在2004年的基地替代设施公害调停中已经出现，"
            "提示这是持续的venue design，而非PFAS个案特有反应；两案仍不得合并。"
        ),
        "selection_reason": (
            "申请被书面接收但在调停启动前因资格边界被阻断，"
            "可直接观察行政程序的入口过滤。"
        ),
        "interpretation_limit": (
            "申请书原件与却下决定书原件尚未在公开网页找到，决定细节需人审补原件；"
            "不得从本案认证美军基地为污染源、个体健康损害或行政完全不回应。"
        ),
    },
    {
        "case_id": "TN03",
        "short_label": "安保法制违宪冲绳诉讼未进入违宪判断",
        "gate_family": "judicial_legal_interest_gate",
        "claim": (
            "冲绳县内战争体验者及美军／自卫队基地周边居民等主张安保法制侵害"
            "平和的生存权、人格权与宪法改正决定权，并向国家请求每人1万日元赔偿。"
        ),
        "claim_date": "2017/2021-02-18",
        "actor": (
            "安保法制違憲沖縄訴訟の原告集団（地裁82人；控诉人80人）"
        ),
        "actor_registry_status": "provisional_procedural_collective_not_registry",
        "target_venue": "那霸地方法院→福冈高等法院那霸支部",
        "entry_attempt": "国家赔偿请求诉讼（地裁平成29年(ワ)412号等；高裁令和2年(ネ)61号）",
        "entry_gate": "具体危险、法律上受保护利益与损害的成立；违宪判断仅在救济判断所需范围内进入",
        "formal_acceptance": "docketed_and_heard_damages_rejected_constitutional_merits_not_reached",
        "intermediate_output": (
            "正式判决承认冲绳居民的战争与成为攻击目标之恐惧具有切实性，"
            "但认定未达具体危险／受保护利益侵害，并未判断安保法是否违宪"
        ),
        "limited_relief": "recognition_without_legal_relief",
        "substantive_change": "no_change_to_security_laws",
        "source_refs": "TNS009;TNS010;TNS011;TNS012",
        "locator": (
            "TNS009 PDF pp.1,4–7；TNS010正文第67–74行；"
            "TNS011搜索可见正文；TNS012 PDF案件表第13项"
        ),
        "evidence_type": "E4_official_appellate_judgment_plus_local_reports",
        "candidate_status": "candidate",
        "review_status": "ai_seeded",
        "package_status": "research_only",
        "frontend_status": "not_frontend_ready",
        "central_writeback": "no",
        "competing_explanation": (
            "法院未作违宪判断，可解释为在具体危险与受保护利益层面已足以驳回，"
            "无需进入宪法争点；这不同于法院一般性拒绝审查安保法。"
        ),
        "selection_reason": (
            "诉求已充分进入司法并留下正式判决，却在可司法化的权利／损害门槛处停住，"
            "可作为噪音赔偿案等部分救济案例的反向对照。"
        ),
        "interpretation_limit": (
            "冲绳本案是国家赔偿请求被棄却，不得借用大阪等地案件的差止却下结论；"
            "也不能把原告个人集体自动登记为持续组织。"
        ),
    },
    {
        "case_id": "TN04",
        "short_label": "与那国导弹配备问题的书面答复被拒",
        "gate_family": "administrative_response_modality_gate",
        "claim": (
            "15名与那国町民就地对空导弹追加配备、基地扩张、岛民安全与住民同意等"
            "提交10项问题，要求冲绳防卫局在2023-05-15说明会上作书面回答。"
        ),
        "claim_date": "2023-05-10/2023-07-25",
        "actor": "与那国町民15人联名（山田和幸等；不是当然等同A016）",
        "actor_registry_status": "individual_collective_not_registry_actor",
        "target_venue": "冲绳防卫局・与那国町住民说明会及后续问答渠道",
        "entry_attempt": "联名質問状并请求书面回答",
        "entry_gate": "行政机关对答复形式与公开方式的选择",
        "formal_acceptance": (
            "question_letter_received_written_reply_refused_"
            "later_public_QA_artifacts_exist_linkage_unconfirmed"
        ),
        "intermediate_output": (
            "据住民所述防卫局电话拒绝书面回答；其后确有住民说明会、"
            "町官网公布的说明会问答及追加问题答复，但与原10项问题的逐项对应尚未证实"
        ),
        "limited_relief": (
            "public_information_available_"
            "relief_to_original_submission_not_established"
        ),
        "substantive_change": "unknown_not_established",
        "source_refs": "TNS013;TNS014;TNS015;TNS016;TNS017",
        "locator": (
            "TNS013正文第30–39行；TNS014正文第25–38行；"
            "TNS015正文第65–70行；TNS016 PDF全文；TNS017页面及附件"
        ),
        "evidence_type": "E3_reported_refusal_plus_E4_official_QA_artifacts",
        "candidate_status": "candidate",
        "review_status": "ai_seeded",
        "package_status": "research_only",
        "frontend_status": "not_frontend_ready",
        "central_writeback": "no",
        "competing_explanation": (
            "书面方式被拒可能是答复渠道选择、信息安全或行政惯例；"
            "后续公开问答材料存在，但尚不能证明它们是原質問状的替代答复。"
        ),
        "selection_reason": (
            "它把‘行政无正式回应’细分为更可检验的‘指定答复形式被拒，"
            "后续另有公开问答材料但对应关系未闭合’，避免制造过强的零回应案例。"
        ),
        "interpretation_limit": (
            "拒绝事实目前来自住民转述，防卫局当时未向媒体确认；"
            "未找到原質問状和正式书面拒绝，且不能把15人联名身份转嫁给A016。"
        ),
    },
    {
        "case_id": "TN05",
        "short_label": "边野古白宫请愿达标后仅追到确认函",
        "gate_family": "transnational_petition_response_gate",
        "claim": (
            "请求美国总统在2019年冲绳县民投票举行前停止边野古／大浦湾填埋工程。"
        ),
        "claim_date": "2018-12-08/2019-01-21",
        "actor": "Robert/Rob Kajiwara（个人发起者；支持者不自动视为共同组织）",
        "actor_registry_status": "individual_initiator_not_registry_actor",
        "target_venue": "美国白宫 We the People 请愿平台",
        "entry_attempt": "公开电子请愿",
        "entry_gate": "30日内10万签名触发平台审查与官方更新承诺",
        "formal_acceptance": "published_threshold_met_acknowledgment_received_issue_specific_update_not_located_in_bounded_trace",
        "intermediate_output": (
            "国家档案馆保存的正式请愿页记录212945份签名；发起者公开一封"
            "白宫通信部门确认正在审阅并致谢的信件"
        ),
        "limited_relief": "acknowledgment_and_public_visibility_only",
        "substantive_change": "not_demonstrated_by_this_package",
        "source_refs": "TNS018;TNS019;TNS020;TNS021",
        "locator": (
            "TNS018页面标题、创建日、签名数与诉求；TNS019 About第28–52行；"
            "TNS020全文；TNS021正文"
        ),
        "evidence_type": "E4_entry_record_plus_E3_response_trace",
        "candidate_status": "candidate",
        "review_status": "ai_seeded",
        "package_status": "research_only",
        "frontend_status": "not_frontend_ready",
        "central_writeback": "no",
        "competing_explanation": (
            "后续难以追到可能来自特朗普时期平台积压、外交／地方事项边界、"
            "统一回应机制或历史站点保存不完整；不能据此推定对冲绳的特定拒绝。"
        ),
        "selection_reason": (
            "它达到明文入口阈值并收到确认，却无法在受限搜索中闭合为议题专属政策回应，"
            "能检验‘国际化入口可见性’与‘可追踪政策产出’之间的落差。"
        ),
        "interpretation_limit": (
            "必须写成‘在本轮限定检索中未找到议题专属官方更新’，"
            "不得写成现实中绝无正式回应；也不从请愿参与推定组织联盟或工程因果。"
        ),
    },
]

SOURCE_FIELDS = [
    "log_id",
    "row_kind",
    "case_id",
    "local_source_id",
    "source_type",
    "publisher",
    "title",
    "source_date",
    "url",
    "locator",
    "supports",
    "search_or_exclusion_note",
    "evidence_type",
    "included_in_case",
    "candidate_status",
    "review_status",
    "package_status",
    "frontend_status",
    "central_writeback",
    "central_source_id",
]

SOURCES = [
    {
        "log_id": "TNL001",
        "row_kind": "included_source",
        "case_id": "TN01",
        "local_source_id": "TNS001",
        "source_type": "official_municipal_council_result_pdf",
        "publisher": "宮古島市議会",
        "title": "平成28年第7回定例会上程案件处理结果",
        "source_date": "2016-09-29",
        "url": "https://www.city.miyakojima.lg.jp/gyosei/gikai/files/28.dai7kaijyouteiannkennsyorikekka.pdf",
        "locator": "PDF p.4 陳情書第26号",
        "supports": "提出者、诉求、提出日、处理日与不採択",
    },
    {
        "log_id": "TNL002",
        "row_kind": "included_source",
        "case_id": "TN01",
        "local_source_id": "TNS002",
        "source_type": "official_municipal_council_minutes_pdf",
        "publisher": "宮古島市議会",
        "title": "平成28年第7回宮古島市議会定例会会議録",
        "source_date": "2016-09",
        "url": "https://www.city.miyakojima.lg.jp/gyosei/gikai/files/h28.9.dai7kai.kaigiroku.pdf",
        "locator": "PDF案件处理表及陳情書第26号审议记录",
        "supports": "正式议程、委员会／全会处理轨迹",
    },
    {
        "log_id": "TNL003",
        "row_kind": "included_source",
        "case_id": "TN01",
        "local_source_id": "TNS003",
        "source_type": "local_news",
        "publisher": "琉球新報",
        "title": "「陸自配備 住民投票を」宮古島市 市民、条例制定求め陳情",
        "source_date": "2016-09-07",
        "url": "https://ryukyushimpo.jp/news/entry-352086.html",
        "locator": "正文第65–69行",
        "supports": "组织正式名称、共同代表与原始诉求",
    },
    {
        "log_id": "TNL004",
        "row_kind": "included_source",
        "case_id": "TN01",
        "local_source_id": "TNS004",
        "source_type": "local_news",
        "publisher": "宮古毎日新聞",
        "title": "住民投票実施など審査／総務財政委",
        "source_date": "2016-09-14",
        "url": "https://www.miyakomainichi.com/news/post-92682/",
        "locator": "正文第131–150行",
        "supports": "委员会实质审查及多种不支持理由",
    },
    {
        "log_id": "TNL005",
        "row_kind": "included_source",
        "case_id": "TN02",
        "local_source_id": "TNS005",
        "source_type": "local_broadcast_news",
        "publisher": "RBC琉球放送",
        "title": "PFAS汚染源の特定へ「公害認定を第一歩に」市民団体が県に調停申請",
        "source_date": "2025-10-27",
        "url": "https://newsdig.tbs.co.jp/articles/rbc/2252071?display=1",
        "locator": "正文第171–194行",
        "supports": "申请日期、主要诉求、程序对象适格争点",
    },
    {
        "log_id": "TNL006",
        "row_kind": "included_source",
        "case_id": "TN02",
        "local_source_id": "TNS006",
        "source_type": "local_news",
        "publisher": "琉球新報",
        "title": "PFAS公害調停の申請を却下 県審査会が市民団体に通知",
        "source_date": "2026-02-21",
        "url": "https://ryukyushimpo.jp/news/entry-5057453.html",
        "locator": "正文第68–69行",
        "supports": "三申请团体、却下与防卫设施适用除外",
    },
    {
        "log_id": "TNL007",
        "row_kind": "included_source",
        "case_id": "TN02",
        "local_source_id": "TNS007",
        "source_type": "wire_report_republished_local",
        "publisher": "共同通信／沖縄タイムス",
        "title": "PFAS公害調停の申請を却下 沖縄、米軍基地は対象外",
        "source_date": "2026-02-21",
        "url": "https://www.okinawatimes.co.jp/articles/-/1779988",
        "locator": "正文第166–184行",
        "supports": "决定书理由、程序性却下及非拘束性意见",
    },
    {
        "log_id": "TNL008",
        "row_kind": "included_source",
        "case_id": "TN02",
        "local_source_id": "TNS008",
        "source_type": "official_prefectural_procedure_page",
        "publisher": "沖縄県",
        "title": "調停とは（手続きの流れ）",
        "source_date": "2024-01-11",
        "url": "https://www.pref.okinawa.lg.jp/kensei/shingikai/1014397/1014517/1004600/1004614.html",
        "locator": "正文第193–223行",
        "supports": "申请接收、受理／却下门槛、调停的非强制与非命令性质",
    },
    {
        "log_id": "TNL009",
        "row_kind": "included_source",
        "case_id": "TN03",
        "local_source_id": "TNS009",
        "source_type": "official_appellate_judgment_pdf",
        "publisher": "福岡高等裁判所那覇支部",
        "title": "令和2年(ネ)第61号 安保法制違憲国家賠償請求控訴事件判決",
        "source_date": "2021-02-18",
        "url": "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-90088.pdf",
        "locator": "PDF pp.1,4–7",
        "supports": "诉求、80名控诉人、恐惧认定、权利侵害否定与控诉棄却",
        "search_or_exclusion_note": (
            "法院现行assets迁移地址于2026-07-20直连返回200。旧地址"
            "https://www.courts.go.jp/app/files/hanrei_jp/088/090088_hanrei.pdf "
            "同日直连返回404，仅保留为legacy locator，不再用于复现。"
        ),
    },
    {
        "log_id": "TNL010",
        "row_kind": "included_source",
        "case_id": "TN03",
        "local_source_id": "TNS010",
        "source_type": "local_news",
        "publisher": "琉球新報",
        "title": "安保法訴訟、控訴を棄却 住民側は上告方針 高裁那覇支部",
        "source_date": "2021-02-19",
        "url": "https://ryukyushimpo.jp/news/entry-1274492.html",
        "locator": "正文第67–74行",
        "supports": "原告构成、法院承认切实恐惧但未作违宪判断",
    },
    {
        "log_id": "TNL011",
        "row_kind": "included_source",
        "case_id": "TN03",
        "local_source_id": "TNS011",
        "source_type": "local_news",
        "publisher": "沖縄タイムス",
        "title": "安保違憲訴訟 原告側が控訴／那覇地裁判決に不服",
        "source_date": "2020-07-11",
        "url": "https://www.okinawatimes.co.jp/articles/-/599308",
        "locator": "搜索可见正文摘要",
        "supports": "地裁82人原告、每人1万日元国家赔偿与地裁未作违宪判断",
    },
    {
        "log_id": "TNL012",
        "row_kind": "included_source",
        "case_id": "TN03",
        "local_source_id": "TNS012",
        "source_type": "official_court_preservation_list_pdf",
        "publisher": "福岡高等裁判所",
        "title": "特別保存に付した事件（令和3年終局分）",
        "source_date": "2025-06-24",
        "url": "https://www.courts.go.jp/fukuoka-h/vc-files/fukuoka-h/tokubetuhozon/20250624/syuukyoku/r3syuukyokubun.pdf",
        "locator": "PDF案件表第13项",
        "supports": "那覇支部令和2年(ネ)61号、案件名与终局日2021-02-18",
    },
    {
        "log_id": "TNL013",
        "row_kind": "included_source",
        "case_id": "TN04",
        "local_source_id": "TNS013",
        "source_type": "party_press",
        "publisher": "しんぶん赤旗",
        "title": "ミサイル配備 説明を／沖縄 与那国町民、防衛省に質問書",
        "source_date": "2023-05-12",
        "url": "https://www.jcp.or.jp/akahata/aik23/2023-05-12/2023051201_03_0.html",
        "locator": "正文第30–39行",
        "supports": "10项问题、说明会答复请求与问题内容",
    },
    {
        "log_id": "TNL014",
        "row_kind": "included_source",
        "case_id": "TN04",
        "local_source_id": "TNS014",
        "source_type": "local_broadcast_news",
        "publisher": "QAB",
        "title": "自衛隊ミサイル配備計画で 与那国住民が国に質問書",
        "source_date": "2023-05-10",
        "url": "https://www.qab.co.jp/news/20230510174085.html",
        "locator": "正文第25–38行",
        "supports": "提出人、问题主旨与要求在说明会回答",
    },
    {
        "log_id": "TNL015",
        "row_kind": "included_source",
        "case_id": "TN04",
        "local_source_id": "TNS015",
        "source_type": "local_news",
        "publisher": "琉球新報",
        "title": "与那国ミサイル配備計画 住民の質問状に沖縄防衛局「文書による回答できない」",
        "source_date": "2023-05-13",
        "url": "https://ryukyushimpo.jp/news/entry-1709292.html",
        "locator": "正文第65–70行",
        "supports": "15人联名、书面答复请求与住民转述的电话拒绝",
    },
    {
        "log_id": "TNL016",
        "row_kind": "included_source",
        "case_id": "TN04",
        "local_source_id": "TNS016",
        "source_type": "official_municipal_QA_pdf",
        "publisher": "与那国町",
        "title": "与那国住民説明会における質問回答",
        "source_date": "2023-06-05",
        "url": "https://www.town.yonaguni.okinawa.jp/docs/2023060500011/file_contents/shitumon.pdf",
        "locator": "PDF全文",
        "supports": "说明会中住民问题的官方公开答复",
    },
    {
        "log_id": "TNL017",
        "row_kind": "included_source",
        "case_id": "TN04",
        "local_source_id": "TNS017",
        "source_type": "official_municipal_followup_page",
        "publisher": "与那国町",
        "title": "駐屯地への地対空誘導弾部隊の配備に関する追加質問への回答",
        "source_date": "2023-07-25",
        "url": "https://www.town.yonaguni.okinawa.jp/docs/2023072500016/",
        "locator": "页面及附件",
        "supports": "防卫省对町所收追加问题提供答复",
    },
    {
        "log_id": "TNL018",
        "row_kind": "included_source",
        "case_id": "TN05",
        "local_source_id": "TNS018",
        "source_type": "official_archived_petition_page",
        "publisher": "U.S. National Archives / Trump White House archive",
        "title": "Stop the landfill of Henoko / Oura Bay until a referendum can be held in Okinawa",
        "source_date": "2018-12-08",
        "url": "https://petitions.trumpwhitehouse.archives.gov/petition/stop-landfill-henoko-oura-bay-until-referendum-can-be-held-okinawa",
        "locator": "页面标题、创建日、212945签名、诉求与类别",
        "supports": "正式入场、诉求文本与超过阈值的签名数",
    },
    {
        "log_id": "TNL019",
        "row_kind": "included_source",
        "case_id": "TN05",
        "local_source_id": "TNS019",
        "source_type": "official_platform_rules",
        "publisher": "Trump White House archive",
        "title": "About We the People",
        "source_date": "archived",
        "url": "https://petitions.trumpwhitehouse.archives.gov/about",
        "locator": "正文第28–52行及FAQ",
        "supports": "10万／30日门槛、审查队列与官方回应规则及例外",
    },
    {
        "log_id": "TNL020",
        "row_kind": "included_source",
        "case_id": "TN05",
        "local_source_id": "TNS020",
        "source_type": "party_press",
        "publisher": "しんぶん赤旗",
        "title": "辺野古請願署名 ホワイトハウス「慎重に検討」",
        "source_date": "2019-01-23",
        "url": "https://www.jcp.or.jp/akahata/aik18/2019-01-23/2019012301_04_1.html",
        "locator": "全文",
        "supports": "发起者身份、达标日、通信部门确认函与致谢内容",
    },
    {
        "log_id": "TNL021",
        "row_kind": "included_source",
        "case_id": "TN05",
        "local_source_id": "TNS021",
        "source_type": "local_news",
        "publisher": "琉球新報",
        "title": "目標の10万筆突破 ホワイトハウス請願サイト署名",
        "source_date": "2018-12-19",
        "url": "https://ryukyushimpo.jp/news/entry-850681.html",
        "locator": "正文",
        "supports": "Robert Kajiwara发起者身份与2018-12-18超过10万",
    },
    {
        "log_id": "TNL022",
        "row_kind": "excluded_lead",
        "case_id": "",
        "local_source_id": "",
        "source_type": "official_municipal_page",
        "publisher": "石垣市",
        "title": "石垣市平得大俣地域住民投票条例に係る議会審議の結果",
        "source_date": "2019-02-04",
        "url": "https://www.city.ishigaki.okinawa.jp/jieiteikannrenn/news/3615.html",
        "locator": "页面全文",
        "supports": "既有R9／TE05中的议会否决阶段",
        "search_or_exclusion_note": (
            "不作为独立TN案例；只能在既有石垣住民投票episode内标注gate-negative stage，"
            "避免重复计算。"
        ),
        "included_in_case": "no",
    },
    {
        "log_id": "TNL023",
        "row_kind": "excluded_lead",
        "case_id": "",
        "local_source_id": "",
        "source_type": "official_prefectural_page",
        "publisher": "沖縄県",
        "title": "有機フッ素化合物について",
        "source_date": "current_page",
        "url": "https://www.pref.okinawa.jp/kurashikankyo/kankyo/1004418/1028431.html",
        "locator": "基地内立入申请栏目",
        "supports": "县政府多次基地内立入申请及不许可",
        "search_or_exclusion_note": (
            "申请主体是县政府而非民间组织；未在本轮闭合到具名NGO提出者，"
            "故不纳入NGO负案例。"
        ),
        "included_in_case": "no",
    },
    {
        "log_id": "TNL024",
        "row_kind": "method_source",
        "case_id": "",
        "local_source_id": "",
        "source_type": "official_prefectural_petition_database",
        "publisher": "沖縄県議会",
        "title": "すべての陳情",
        "source_date": "current_database",
        "url": "https://www2.pref.okinawa.jp/oki/seichinweb.nsf/Web_AllChinjo?Count=9999&OpenView=",
        "locator": "受理日、编号、件名、付託委员会、审议结果、县等报告字段",
        "supports": "採択／不採択／継続審議／取り下げ等结构化结果词汇",
        "search_or_exclusion_note": (
            "保留作下一轮结构化搜索底盘；本包没有仅凭结果字段、未锁定提出者"
            "就制造新案例。"
        ),
        "included_in_case": "no",
    },
    {
        "log_id": "TNL025",
        "row_kind": "excluded_lead",
        "case_id": "",
        "local_source_id": "",
        "source_type": "official_judgment_pdf",
        "publisher": "大阪地方裁判所",
        "title": "大阪・自衛隊出動差止等請求事件（裁判所PDF 089424）",
        "source_date": "2020",
        "url": "https://www.courts.go.jp/app/files/hanrei_jp/424/089424_hanrei.pdf",
        "locator": "主文与案件标识",
        "supports": "大阪安保法制案件的差止却下",
        "search_or_exclusion_note": (
            "检索中发现但排除：不是冲绳诉讼。不得把大阪差止却下结论转写到TN03。"
        ),
        "included_in_case": "no",
    },
    {
        "log_id": "TNL026",
        "row_kind": "contextual_precedent",
        "case_id": "",
        "local_source_id": "",
        "source_type": "official_prefectural_closed_case_summary",
        "publisher": "沖縄県",
        "title": "これまでに終結した事件の概要",
        "source_date": "current_page",
        "url": (
            "https://www.pref.okinawa.lg.jp/kensei/shingikai/"
            "1014397/1014517/1004600/1004603.html"
        ),
        "locator": "事件6「米軍代替飛行場施設建設差止等請求事件」（調停）",
        "supports": (
            "2004-02-03受理、3次调停委员会、913名申请人，以及2004-03-30"
            "因防卫设施属公害纷争处理法第50条对象外而却下"
        ),
        "search_or_exclusion_note": (
            "只作TN02的纵向制度背景：同一适格门槛至少在2004年已有官方公开先例。"
            "913名申请人是个人集合，不能据此建立组织actor；本记录也不另算第6个TN案例。"
        ),
        "included_in_case": "no",
    },
]

for row in SOURCES:
    row.setdefault("search_or_exclusion_note", "")
    row.setdefault("evidence_type", "source_or_search_log_only")
    row.setdefault("included_in_case", "yes" if row["row_kind"] == "included_source" else "no")
    row.setdefault("candidate_status", "candidate")
    row.setdefault("review_status", "ai_seeded")
    row.setdefault("package_status", "research_only")
    row.setdefault("frontend_status", "not_frontend_ready")
    row.setdefault("central_writeback", "no")
    row.setdefault("central_source_id", "")

COMPARISON_FIELDS = [
    "comparison_id",
    "case_id",
    "case_or_baseline",
    "gate_family",
    "public_claim",
    "entry_attempt",
    "formal_processing",
    "intermediate_output",
    "limited_relief",
    "substantive_change",
    "selection_boundary",
    "comparison_use",
    "review_status",
    "package_status",
    "frontend_status",
    "central_writeback",
]

COMPARISON = [
    {
        "comparison_id": "TNC00",
        "case_id": "BASE13",
        "case_or_baseline": "existing_13_episode_baseline",
        "gate_family": "selected_on_observable_venue_entry",
        "public_claim": "13/13_yes",
        "entry_attempt": "13/13_yes",
        "formal_processing": "13/13_yes",
        "intermediate_output": "13/13_yes",
        "limited_relief": "mixed",
        "substantive_change": "mostly_no_or_unknown",
        "selection_boundary": (
            "原13案因已观察到正式／战略场域入场与中间产出而入选，"
            "不是诉求总体，也不能计算成功率。"
        ),
        "comparison_use": "entry_conditioned_reference_not_denominator",
    },
    {
        "comparison_id": "TNC01",
        "case_id": "TN01",
        "case_or_baseline": "candidate_negative_case",
        "gate_family": "legislative_petition_gate",
        "public_claim": "yes",
        "entry_attempt": "yes",
        "formal_processing": "docketed_deliberated_not_adopted",
        "intermediate_output": "yes_official_disposition",
        "limited_relief": "none",
        "substantive_change": "not_demonstrated",
        "selection_boundary": "online-visible official council record",
        "comparison_use": "post_entry_legislative_rejection",
    },
    {
        "comparison_id": "TNC02",
        "case_id": "TN02",
        "case_or_baseline": "candidate_negative_case",
        "gate_family": "administrative_eligibility_gate",
        "public_claim": "yes",
        "entry_attempt": "yes",
        "formal_processing": "received_then_dismissed_before_mediation",
        "intermediate_output": "yes_decision_and_nonbinding_comment",
        "limited_relief": "discursive_only",
        "substantive_change": "unknown",
        "selection_boundary": "outcome primary documents still missing",
        "comparison_use": "eligibility_or_jurisdiction_block",
    },
    {
        "comparison_id": "TNC03",
        "case_id": "TN03",
        "case_or_baseline": "candidate_negative_case",
        "gate_family": "judicial_legal_interest_gate",
        "public_claim": "yes",
        "entry_attempt": "yes",
        "formal_processing": "heard_claims_rejected_no_constitutional_holding",
        "intermediate_output": "yes_official_judgment",
        "limited_relief": "recognition_only",
        "substantive_change": "no",
        "selection_boundary": "procedural collective identity remains provisional",
        "comparison_use": "legal_interest_failure_and_constitutional_avoidance",
    },
    {
        "comparison_id": "TNC04",
        "case_id": "TN04",
        "case_or_baseline": "candidate_negative_case",
        "gate_family": "administrative_response_modality_gate",
        "public_claim": "yes",
        "entry_attempt": "yes",
        "formal_processing": (
            "written_mode_refused_later_public_QA_exists_linkage_unconfirmed"
        ),
        "intermediate_output": "later_public_QA_artifacts_linkage_unconfirmed",
        "limited_relief": "relief_to_original_submission_not_established",
        "substantive_change": "unknown",
        "selection_boundary": "refusal is resident-attributed; item-level answer mapping unclosed",
        "comparison_use": "requested_response_mode_block_not_total_nonresponse",
    },
    {
        "comparison_id": "TNC05",
        "case_id": "TN05",
        "case_or_baseline": "candidate_negative_case",
        "gate_family": "transnational_petition_response_gate",
        "public_claim": "yes",
        "entry_attempt": "yes_threshold_met",
        "formal_processing": "acknowledgment_found_issue_update_not_located",
        "intermediate_output": "yes_acknowledgment_and_visibility",
        "limited_relief": "acknowledgment_only",
        "substantive_change": "not_demonstrated",
        "selection_boundary": "bounded response trace is not proof of real-world absence",
        "comparison_use": "threshold_entry_without_closed_policy_response_trace",
    },
]

for row in COMPARISON:
    row.update(
        {
            "review_status": "ai_seeded",
            "package_status": "research_only",
            "frontend_status": "not_frontend_ready",
            "central_writeback": "no",
        }
    )

REVIEW_FIELDS = [
    "review_item_id",
    "case_id",
    "priority",
    "review_question",
    "required_material",
    "current_gap",
    "allowed_decisions",
    "provisional_status",
    "central_writeback",
    "human_decision",
    "human_reviewer",
    "review_date",
    "review_note",
]

REVIEW_QUEUE = [
    {
        "review_item_id": "TNHR001",
        "case_id": "TN01",
        "priority": "P1",
        "review_question": (
            "是否接受TN01为‘正式受理并审议后不採択’的立法入口负例，"
            "并确认组织仍只作本案具名团体而不自动入registry？"
        ),
        "required_material": "TNS001–TNS004",
        "current_gap": "无需新源；需负责人判断比较价值与组织身份边界",
    },
    {
        "review_item_id": "TNHR002",
        "case_id": "TN02",
        "priority": "P0",
        "review_question": (
            "却下决定能否冻结为防卫设施对象适格阻断，而非PFAS实体败诉？"
        ),
        "required_material": "申请书原件；冲绳县公害审查会却下决定书／通知书原件",
        "current_gap": (
            "现有媒体准确转述决定书，但公开网页尚未找到申请书与决定书原件；"
            "#コドソラ身份也未闭合"
        ),
    },
    {
        "review_item_id": "TNHR003",
        "case_id": "TN03",
        "priority": "P0",
        "review_question": (
            "是否接受TN03为‘权利／具体危险门槛导致未进入违宪判断’的司法负例，"
            "并将原告集体保持为程序节点而非registry组织？"
        ),
        "required_material": "TNS009、TNS010、TNS012；必要时补那霸地裁一审判决全文",
        "current_gap": "一审全文尚未纳入包；原告团组织持续性未确认",
    },
    {
        "review_item_id": "TNHR004",
        "case_id": "TN04",
        "priority": "P1",
        "review_question": (
            "是否接受‘书面方式被拒、替代问答存在’的窄负例，"
            "并确认不得写成行政完全无回应？"
        ),
        "required_material": "原10项質問状；防卫局正式书面回复／拒绝记录；TNS016逐项比对",
        "current_gap": (
            "拒绝为住民转述，防卫局当时未确认；原问题与官网问答的逐项对应未闭合"
        ),
    },
    {
        "review_item_id": "TNHR005",
        "case_id": "TN05",
        "priority": "P1",
        "review_question": (
            "是否接受‘达标并获确认，但本轮未追到议题专属更新’作为国际请愿的"
            "回应追踪负例？"
        ),
        "required_material": (
            "白宫回应索引／API历史数据；发起者保存的完整通信；"
            "国家档案馆对应petition状态字段"
        ),
        "current_gap": (
            "保存页未展示response区；限定搜索未找到议题专属更新，"
            "但这不能证明现实中绝无回应"
        ),
    },
]

for row in REVIEW_QUEUE:
    row.update(
        {
            "allowed_decisions": (
                "accept_candidate;revise;defer_second_source;defer_primary;reject"
            ),
            "provisional_status": "ai_seeded_research_only_not_frontend_ready",
            "central_writeback": "no",
            "human_decision": "",
            "human_reviewer": "",
            "review_date": "",
            "review_note": "",
        }
    )


def write_csv(path: Path, fields: Sequence[str], rows: Iterable[Mapping[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="raise", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def baseline_count() -> int:
    if not BASELINE.exists():
        raise FileNotFoundError(f"missing baseline input: {BASELINE}")
    return len(read_csv(BASELINE))


def render_readme() -> str:
    return f"""# Translation negative cases v1

本包是对 `outputs/translation_episode_comparison_v1/` 的**加法型、研究专用对照包**。原包
13 个 episode 全部因已有可观察的场域进入和中间产出而入选；本包定向寻找入口受阻、
资格排除、可司法化失败、指定回应方式被拒或回应追踪停滞的案例，用来检查“制度让步上限”
是否受到入场选择偏差影响。

## 内容

- `negative_case_candidates_v1.csv`：5 个统一字段候选案例。
- `source_search_log_v1.csv`：21 条纳入来源与5条方法／背景／排除记录；`TNS*` 仅为本包本地编号，
  不是中央 `S*` source ID。
- `comparison_table_v1.csv`：原13案选择边界与5个候选负例的同口径比较。
- `human_review_queue_v1.csv`：5项负责人判断候选；决定栏保持空白，尚未进入正式HR总账。
- `brief_v1.md`：研究结论、竞争解释与不能说什么。
- `validation_report_v1.md`：结构、状态与边界检查。
- `handoff_v1.md`：主线程换手说明。

## 强制边界

所有行都是 `research_only / candidate / ai_seeded / not_frontend_ready /
central_writeback=no`。它们不是中央事实、前端数据或正式报告结论。未找到公开回应只能写成
“本轮限定检索未找到”，不得写成现实中没有回应；不採択不等于未受理；同案、联名、共同
申请不生成稳定联盟。

## 复现

```powershell
python scripts\\make_translation_negative_cases_v1.py
python scripts\\make_translation_negative_cases_v1.py --check
```

生成日期：{RUN_DATE}。
"""


def render_brief() -> str:
    return """# 转译机制负案例：第一轮研究简报

## 这轮回答了什么

原有13个“转译 episode”都有公开诉求、场域进入和中间产出。这不是偶然遗漏，而是入选规则
本身造成的：我们先看见了成功进入正式场域的案例，才有足够材料把它们写成 episode。因此，
“制度通常留下记录或有限结果”的描述，可能低估了进门前和进门处的损耗。

本轮找到5个结构不同的候选对照：

1. **宫古2016陳情**：议会收件、审查、讨论后不採択。它不是“没人理”，而是被正式处理后
   阻断。
2. **PFAS公害调停**：申请被接收，但防卫设施的法定适用除外使调停没有启动。审查会留下
   关切和建议，却没有调停、命令或实体污染判断。县官方终结事件库显示，同一法定门槛
   至少在2004年的基地替代设施公害调停中已经出现，但两案不能合并。
3. **安保法制违宪冲绳诉讼**：诉讼进入法院并形成判决，法院承认冲绳居民恐惧的切实性，
   但在具体危险和受保护利益层面驳回赔偿，因而没有进入安保法违宪判断。
4. **与那国2023質問状**：据居民转述，要求书面回答被拒；此后另有说明会问答和追加问题
   答复，但尚不能证明这些材料对应原10项質問。这里的负向结果只是“指定回应形式被拒”，
   不是“行政完全无回应”，也不是“原質問状获得部分救济”。
5. **边野古白宫请愿**：请愿超过10万门槛并收到审阅确认函；国家档案保存页记录212,945份
   签名，但本轮限定检索没有闭合到议题专属政策更新。它只能编码为回应追踪未闭合。

## 对“制度让步上限”的修正

这5案并没有推翻“制度能记录、承认或有限补偿，却很少改变工程／部署”的暂定观察；它们
把上限拆得更细：

- 有的诉求**进入后被表决否决**；
- 有的在**对象适格／管辖**处被排除；
- 有的留下完整判决，却在**具体权利与可救济性**处停住；
- 有的只在**回应方式**上受阻；
- 有的达到平台门槛，但**后续官方产出无法闭合追踪**。

因此，下一阶段不能只比较“进入制度后得到多少”，还要比较“什么样的 actor、claim 和
translation 才能越过哪一道入口”。制度上限至少包含 **entry gate → processing gate →
relief gate → implementation gate** 四层。

## 仍然存在的选择偏差

即使是这5个“负例”，也都留下了可检索记录。真正没有被受理、没有被报道、没有保存官网、
或者只在口头／纸本中消失的诉求，线上研究仍看不见。因此本包不能估计负例比例，也不能
计算成功率。它只是证明原13案不能充当所有诉求的分母。

## 竞争解释

- **claim fit**：不是制度一概封闭，而是诉求与法定权限、权利构成或回应格式不匹配。
- **actor capacity**：有律师、稳定文书、官网或媒体接入的主体更容易把失败也保存为资料。
- **venue design**：调停、法院、议会和请愿平台提供的救济不同，不能把“不採択、却下、
  棄却、未追到更新”合并成一个失败变量。
- **archive visibility**：白宫请愿和与那国书面答复的缺口也可能是保存／公开问题，不能把
  检索缺失当现实缺失。

## 负责人需要决定

负责人检查点候选共5项，尚未作为正式HR派工。优先先读：

1. TN02 的申请书和却下决定书原件；
2. TN03 的高裁判决及一审全文；
3. TN04 的原10项質問状和正式拒绝记录。

只有人审接受后，才可决定是否把负例接入论文比较；本轮不改中央表、不进前端，也不改原13案。
"""


def render_handoff() -> str:
    return f"""# Translation negative cases v1 — handoff

## 完成

- 5个统一结构的 `research_only` 候选对照，覆盖议会入口、行政对象适格、司法权利门槛、
  行政回应方式与跨国请愿回应追踪。
- 21条纳入来源；每案至少2源，并至少有1条官方／一手程序材料。
- 5条方法／背景／排除记录：石垣只作为既有TE05的负向阶段；县政府PFAS立入申请因主体不是NGO
  排除；县议会陳情库仅保留为未来搜索底盘；大阪安保判决明确排除，未误写为冲绳案；
  2004年基地公害调停仅作长期制度门槛背景，不把913名个人申请人组织化。
- 5项空白负责人判断候选，未做AI自审，也未写入正式HR总账。
- 生成与验证命令均通过。

## 没有改

- 中央 actor、issue、place、event、relation、source log 与 source archive；
- `outputs/translation_episode_comparison_v1/`；
- 前端、控制文档与工作台。

## 关键判断

- TN01 是“受理并审议后不採択”，不是未受理。
- TN02 是适用对象／资格阻断，不是PFAS实体败诉；原申请与决定书仍需补。
- TN03 只编码冲绳国家赔偿案；法院原文使用现行 `assets` 地址，
  福冈高裁现行保存目录第13项交叉锁定案号／案名／终局日；不借用大阪差止却下。
- TN04 只编码居民转述的书面形式被拒；后续公开问答存在，但与原質問状的程序对应未闭合，
  不能称完全无回应，也不能称原提出者获得部分救济。
- TN05 只称本轮未找到议题专属更新；不能称现实中没有正式回应。

## 建议下一步

负责人在检查点决定是否把 `human_review_queue_v1.csv` 转为正式HR任务。若其后接受至少3个跨门槛负例，再由新session
建立与原13案的案例匹配（相近议题、相近时间、不同gate outcome）；不要先合并为“成功／失败”
二元变量。

复现：

```powershell
python scripts\\make_translation_negative_cases_v1.py
python scripts\\make_translation_negative_cases_v1.py --check
```

生成日期：{RUN_DATE}。
"""


def validate() -> list[str]:
    messages: list[str] = []
    errors: list[str] = []

    paths = {
        "cases": OUT / "negative_case_candidates_v1.csv",
        "sources": OUT / "source_search_log_v1.csv",
        "comparison": OUT / "comparison_table_v1.csv",
        "review": OUT / "human_review_queue_v1.csv",
    }
    for label, path in paths.items():
        if not path.exists():
            errors.append(f"missing {label}: {path}")
    if errors:
        raise AssertionError("\n".join(errors))

    cases = read_csv(paths["cases"])
    sources = read_csv(paths["sources"])
    comparison = read_csv(paths["comparison"])
    review = read_csv(paths["review"])

    if baseline_count() != 13:
        errors.append(f"baseline episode count expected 13, got {baseline_count()}")
    else:
        messages.append("PASS baseline input remains 13 episodes")

    if len(cases) != 5:
        errors.append(f"case count expected 5, got {len(cases)}")
    else:
        messages.append("PASS five candidate negative cases")

    if len({row["case_id"] for row in cases}) != len(cases):
        errors.append("case_id values are not unique")
    else:
        messages.append("PASS unique case IDs")

    required_families = {
        "legislative_petition_gate",
        "administrative_eligibility_gate",
        "judicial_legal_interest_gate",
        "administrative_response_modality_gate",
        "transnational_petition_response_gate",
    }
    found_families = {row["gate_family"] for row in cases}
    if found_families != required_families:
        errors.append(
            f"gate family coverage mismatch: {sorted(found_families)}"
        )
    else:
        messages.append("PASS five distinct gate families")

    for row in cases:
        missing = [field for field in CASE_FIELDS if not row.get(field, "").strip()]
        if missing:
            errors.append(f"{row.get('case_id')}: blank required fields {missing}")
        fixed = {
            "candidate_status": "candidate",
            "review_status": "ai_seeded",
            "package_status": "research_only",
            "frontend_status": "not_frontend_ready",
            "central_writeback": "no",
        }
        for field, expected in fixed.items():
            if row.get(field) != expected:
                errors.append(
                    f"{row['case_id']}: {field}={row.get(field)!r}, expected {expected!r}"
                )
        if "TE05" in row["case_id"] or "石垣" in row["short_label"]:
            errors.append(f"{row['case_id']}: Ishigaki must not be an independent case")
    if not errors:
        messages.append("PASS case fields and research-only state contract")

    included = [row for row in sources if row["row_kind"] == "included_source"]
    sources_by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in included:
        sources_by_case[row["case_id"]].append(row)
        if row["central_source_id"]:
            errors.append(
                f"{row['log_id']}: local package must not assign central source ID"
            )
        if not row["local_source_id"].startswith("TNS"):
            errors.append(f"{row['log_id']}: included source lacks TNS local ID")
    for case in cases:
        rows = sources_by_case[case["case_id"]]
        if len(rows) < 2:
            errors.append(f"{case['case_id']}: fewer than two included sources")
        if not any(
            "official" in row["source_type"]
            or "court" in row["source_type"]
            for row in rows
        ):
            errors.append(f"{case['case_id']}: no official/procedural source")
        refs = set(case["source_refs"].split(";"))
        logged = {row["local_source_id"] for row in rows}
        if refs != logged:
            errors.append(
                f"{case['case_id']}: source_refs {sorted(refs)} != log {sorted(logged)}"
            )
    if not errors:
        messages.append("PASS per-case multi-source and official-source gates")

    excluded_titles = " ".join(
        row["title"] for row in sources if row["row_kind"] == "excluded_lead"
    )
    if "石垣" not in excluded_titles or "大阪" not in excluded_titles:
        errors.append("required Ishigaki and Osaka exclusion guards not logged")
    else:
        messages.append("PASS duplicate/misattribution exclusion guards")

    precedent = next(
        (
            row
            for row in sources
            if row["log_id"] == "TNL026"
            and row["row_kind"] == "contextual_precedent"
        ),
        None,
    )
    if (
        precedent is None
        or precedent["included_in_case"] != "no"
        or "913名申请人" not in precedent["supports"]
        or "不能据此建立组织actor" not in precedent["search_or_exclusion_note"]
    ):
        errors.append("2004 defense-facility mediation precedent boundary missing")
    else:
        messages.append(
            "PASS 2004 defense-facility mediation retained as non-actor contextual precedent"
        )

    source_by_id = {row["local_source_id"]: row for row in included}
    tn03_judgment = source_by_id.get("TNS009", {})
    current_judgment_url = (
        "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-90088.pdf"
    )
    legacy_judgment_url = (
        "https://www.courts.go.jp/app/files/hanrei_jp/088/090088_hanrei.pdf"
    )
    if tn03_judgment.get("url") != current_judgment_url:
        errors.append("TNS009 must use the current courts.go.jp assets judgment URL")
    elif legacy_judgment_url not in tn03_judgment.get(
        "search_or_exclusion_note", ""
    ):
        errors.append("TNS009 must retain the dead app/files URL only as a legacy note")
    else:
        messages.append("PASS TN03 current judgment locator and legacy-URL boundary")

    tn03_directory = source_by_id.get("TNS012", {})
    current_directory_url = (
        "https://www.courts.go.jp/fukuoka-h/vc-files/fukuoka-h/"
        "tokubetuhozon/20250624/syuukyoku/r3syuukyokubun.pdf"
    )
    if (
        tn03_directory.get("url") != current_directory_url
        or "第13项" not in tn03_directory.get("locator", "")
        or "令和2年(ネ)61号" not in tn03_directory.get("supports", "")
    ):
        errors.append(
            "TNS012 must use the current Fukuoka High Court directory and item 13"
        )
    else:
        messages.append("PASS TN03 current Fukuoka preservation-directory cross-check")

    case_by_id = {row["case_id"]: row for row in cases}
    comparison_by_case = {row["case_id"]: row for row in comparison}
    tn04 = case_by_id["TN04"]
    tn04_comparison = comparison_by_case["TN04"]
    if (
        "linkage_unconfirmed" not in tn04["formal_acceptance"]
        or "relief_to_original_submission_not_established"
        not in tn04["limited_relief"]
        or "linkage_unconfirmed" not in tn04_comparison["formal_processing"]
        or "relief_to_original_submission_not_established"
        not in tn04_comparison["limited_relief"]
    ):
        errors.append(
            "TN04 must separate later public Q&A artifacts from relief to the original submission"
        )
    else:
        messages.append(
            "PASS TN04 later-Q&A linkage and original-submission relief remain unconfirmed"
        )

    definitive_absence_terms = [
        "现实中没有正式回应",
        "no_formal_response",
        "institution_never_responded",
    ]
    searchable = "\n".join(
        "\t".join(row.get(field, "") for field in CASE_FIELDS) for row in cases
    )
    for term in definitive_absence_terms:
        if term in searchable:
            errors.append(f"definitive nonresponse wording found: {term}")
    if not any(
        "not_located" in row["formal_acceptance"] for row in cases
    ):
        errors.append("bounded not-located response status missing")
    else:
        messages.append("PASS bounded nonresponse wording")

    if len(comparison) != 6 or comparison[0]["case_id"] != "BASE13":
        errors.append("comparison table must contain BASE13 plus five cases")
    else:
        messages.append("PASS comparison table contains baseline plus five cases")

    if len(review) != 5:
        errors.append(f"review queue expected 5 items, got {len(review)}")
    for row in review:
        for field in ["human_decision", "human_reviewer", "review_date", "review_note"]:
            if row[field].strip():
                errors.append(f"{row['review_item_id']}: AI prefilled {field}")
        if row["central_writeback"] != "no":
            errors.append(f"{row['review_item_id']}: central_writeback must be no")
    if not errors:
        messages.append("PASS five blank human-review decisions")

    if errors:
        raise AssertionError("\n".join(errors))
    return messages


def render_validation(messages: Sequence[str]) -> str:
    source_counts = Counter(
        row["case_id"] for row in SOURCES if row["row_kind"] == "included_source"
    )
    lines = [
        "# Translation negative cases v1 — validation",
        "",
        f"验证日期：{RUN_DATE}",
        "",
        "## 结果",
        "",
        "**PASS**",
        "",
    ]
    lines.extend(f"- {message}" for message in messages)
    lines.extend(
        [
            "",
            "## 计数",
            "",
            f"- 原13案输入：{baseline_count()}。",
            f"- 候选负例：{len(CASES)}。",
            f"- 纳入来源：{sum(1 for row in SOURCES if row['row_kind'] == 'included_source')}。",
            f"- 方法／排除记录：{sum(1 for row in SOURCES if row['row_kind'] != 'included_source')}。",
            f"- 人审队列：{len(REVIEW_QUEUE)}，决定栏全部空白。",
            (
                "- 每案来源数："
                + "；".join(
                    f"{case_id}={source_counts[case_id]}"
                    for case_id in sorted(source_counts)
                )
                + "。"
            ),
            "",
            "## 状态边界",
            "",
            "- 全部候选为 `research_only / candidate / ai_seeded / not_frontend_ready`。",
            "- 全部 `central_writeback=no`；本地 `TNS*` 不是中央 `S*`。",
            "- 没有把石垣既有R9阶段重复算作新案例。",
            "- 没有把大阪安保差止判决误配给冲绳国家赔偿案。",
            "- 2004年基地公害调停只作TN02的制度背景，不把913名个人申请人组织化或另算案例。",
            "- TN03 法院原文已迁至现行 `assets` 地址；旧 `app/files` 地址仅作失效 locator 备注。",
            "- TN03 另由福冈高裁现行保存目录第13项交叉锁定案号、案名与终局日。",
            (
                "- 只有 TN01、TN03 具官方个案处分／判决原文；TN02 的却下结果、TN04 的"
                "拒绝形式、TN05 的确认函仍是官方程序材料与报道／公开通信组合而成的"
                "混合证据链，不因“每案有官方来源”而升级。"
            ),
            (
                "- TN04 后续官方问答材料与原10项質問状的逐项、程序或因果对应未闭合；"
                "不得编码为原提出者获得部分救济。"
            ),
            "- 没有把检索未找到回应写成现实无回应。",
            "",
            "复验命令：",
            "",
            "```powershell",
            "python scripts\\make_translation_negative_cases_v1.py --check",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "negative_case_candidates_v1.csv", CASE_FIELDS, CASES)
    write_csv(OUT / "source_search_log_v1.csv", SOURCE_FIELDS, SOURCES)
    write_csv(OUT / "comparison_table_v1.csv", COMPARISON_FIELDS, COMPARISON)
    write_csv(OUT / "human_review_queue_v1.csv", REVIEW_FIELDS, REVIEW_QUEUE)
    (OUT / "README.md").write_text(render_readme(), encoding="utf-8")
    (OUT / "brief_v1.md").write_text(render_brief(), encoding="utf-8")
    (OUT / "handoff_v1.md").write_text(render_handoff(), encoding="utf-8")
    messages = validate()
    (OUT / "validation_report_v1.md").write_text(
        render_validation(messages), encoding="utf-8"
    )
    print(
        f"PASS wrote {len(CASES)} cases, "
        f"{sum(1 for row in SOURCES if row['row_kind'] == 'included_source')} sources, "
        f"{len(REVIEW_QUEUE)} principal-decision candidates to {OUT}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate existing outputs without rewriting them",
    )
    args = parser.parse_args(argv)
    if args.check:
        messages = validate()
        for message in messages:
            print(message)
        print("PASS translation_negative_cases_v1")
    else:
        build()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, FileNotFoundError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
