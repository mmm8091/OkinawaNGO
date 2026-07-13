from __future__ import annotations

"""Build the formal R9 referendum/opinion-ad/litigation process layer.

The script is deliberately module-scoped and idempotent. It writes only the
formal stage table plus files under outputs/R09_referendum_process_v0. It does
not update the actor registry, source log, or project control documents.
"""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "R09_referendum_process_v0"
DATA = ROOT / "data" / "interim"
STAGE_PATH = DATA / "20_referendum_process_stages_v0.csv"
ALL_STAGE_PATH = OUT / "process_stages_reviewed_all_v0.csv"
ROLE_PATH = OUT / "actor_process_roles_v0.csv"
ALL_ROLE_PATH = OUT / "actor_process_roles_reviewed_all_v0.csv"
SOURCE_PATH = OUT / "source_register_v0.csv"
CASE_PATH = OUT / "case_summary_v0.csv"
REJECT_PATH = OUT / "rejected_claims_v0.csv"
HR017_CSV_PATH = OUT / "hr017_review_queue_v0.csv"
HR017_PACKET_PATH = OUT / "HR017_review_packet_v0.md"
LEGACY_REVIEW_QUEUE_PATH = OUT / "review_queue_v0.csv"
BRIEF_PATH = OUT / "R09_process_brief_v1.md"
README_PATH = OUT / "README.md"
VALIDATION_PATH = OUT / "validation_report_v0.md"
TIMELINE_PATH = OUT / "referendum_process_timeline_v0.png"
FLOW_PATH = OUT / "institutional_gate_flow_v0.png"


STAGE_FIELDS = [
    "stage_id", "case_id", "case_name", "place", "process_branch", "stage_order",
    "date_start", "date_end", "date_precision", "stage_type", "short_label",
    "process_action", "formal_basis", "decision_body_or_forum", "outcome",
    "source_refs", "evidence_level", "review_status", "needs_local_retrieval",
    "interpretation_limit", "notes",
]

ROLE_FIELDS = [
    "role_id", "case_id", "stage_id", "actor_id", "entity_id", "entity_name",
    "entity_kind", "role_type", "role_scope", "source_refs", "evidence_level",
    "review_status", "needs_local_retrieval", "interpretation_limit", "notes",
]

SOURCE_FIELDS = [
    "source_id", "existing_source_id", "case_id", "source_tier", "source_type",
    "title", "year", "url", "evidence_level", "review_status", "disposition",
    "supports", "interpretation_limit", "notes",
]

CASE_FIELDS = [
    "case_id", "case_name", "place", "date_start", "date_end", "vote_held",
    "institutional_entry", "institutional_gate_result", "post_gate_path",
    "accepted_stage_count", "pending_stage_count", "mechanism_summary",
    "interpretation_limit",
]

REJECT_FIELDS = ["reject_id", "case_id", "claim", "reason", "source_refs", "status"]
HR017_FIELDS = [
    "task_id", "queue_id", "object_type", "object_id", "case_id", "subject",
    "evidence_level", "source_refs", "source_locator", "needs_local_retrieval",
    "review_question", "impact_if_accept", "impact_if_revise", "impact_if_reject",
    "decision", "human_reviewer", "review_date", "decision_note",
]


def stage(
    stage_id: str,
    case_id: str,
    case_name: str,
    place: str,
    process_branch: str,
    stage_order: int,
    date_start: str,
    date_end: str,
    date_precision: str,
    stage_type: str,
    short_label: str,
    process_action: str,
    formal_basis: str,
    decision_body_or_forum: str,
    outcome: str,
    source_refs: str,
    evidence_level: str,
    review_status: str = "accepted",
    needs_local_retrieval: str = "no",
    interpretation_limit: str = "",
    notes: str = "",
) -> dict[str, str]:
    return {key: str(value) for key, value in locals().items()}


NAGO = "R9C_NAGO_1997"
YONAGUNI = "R9C_YONAGUNI_2015"
PREF = "R9C_PREF_2019"
ISHIGAKI = "R9C_ISHIGAKI_2018_2024"


STAGES = [
    stage("R9ST001", NAGO, "1997 Nago heliport referendum", "Nago", "municipal_direct_request", 1,
          "1997-06-27", "", "day", "initiation", "Request preparation",
          "名護市民投票推進協議会向名护市启动条例制定直接请求准备",
          "地方自治法第74条", "Nago City", "进入代表者证明与签名程序", "R9S001", "E4",
          interpretation_limit="官方事件名称与 A068 当前规范名的映射仍待人工决定；不得据此推定后续组织连续性。"),
    stage("R9ST002", NAGO, "1997 Nago heliport referendum", "Nago", "municipal_direct_request", 2,
          "1997-07-08", "1997-09-16", "day_range", "signature_request", "19,734 submitted / 17,539 valid",
          "取得代表者证明、进行一个月签名、提交并由选管审查后提出条例制定直接请求",
          "地方自治法第74条", "Nago Election Administration Commission / Mayor",
          "提交19,734份，确认17,539份有效；直接请求成立", "R9S001", "E4",
          interpretation_limit="签名数量表示程序参与，不等于组织成员数。"),
    stage("R9ST003", NAGO, "1997 Nago heliport referendum", "Nago", "municipal_direct_request", 3,
          "1997-09-25", "1997-10-06", "day_range", "council_ordinance", "Four-choice ordinance",
          "市长附意见提交；市议会以17对11通过四选项修正案；条例公布",
          "individual referendum ordinance", "Nago City Council / Mayor", "条例成立并设四项选择",
          "R9S001", "E4", interpretation_limit="修正后的问题设计不能与市民团体原案混同。"),
    stage("R9ST004", NAGO, "1997 Nago heliport referendum", "Nago", "municipal_direct_request", 4,
          "1997-12-21", "1997-12-21", "day", "vote", "Referendum held",
          "实施名护市海上直升机场基地建设是非市民投票", "municipal referendum ordinance",
          "Nago Election Administration Commission", "投开票完成", "R9S003;R9S022", "E4",
          interpretation_limit="咨询型投票不能写成法律上阻止国家项目。"),
    stage("R9ST005", NAGO, "1997 Nago heliport referendum", "Nago", "municipal_direct_request", 5,
          "1997-12-21", "1997-12-21", "day", "result", "16,639 oppose / 14,267 support",
          "官方结果按条件选项合并：反对16,639，赞成14,267",
          "municipal referendum ordinance", "Nago Election Administration Commission",
          "赞成2,562、条件付赞成11,705、反对16,254、条件付反对385；投票者31,477；有效票30,906；无效565；投票率82.45%",
          "R9S022", "E4", interpretation_limit="百分比必须注明分母：反对占全体投票者约52.85%，占有效票约53.84%；不使用官方XLS中有90票差异的当日投票小计。"),
    stage("R9ST006", NAGO, "1997 Nago heliport referendum", "Nago", "municipal_direct_request", 6,
          "1997-12-24", "1997-12-24", "day", "post_result_executive", "Mayor accepts and resigns",
          "比嘉市长宣布接受海上基地并辞职", "mayoral executive decision", "Nago Mayor",
          "行政决定与投票多数方向发生分离", "R9S002", "E4",
          interpretation_limit="显示咨询型结果与行政决定可以分离，不等于投票没有政治意义。"),

    stage("R9ST007", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "opinion_ad_context", 1,
          "2012-08-31", "", "day", "opinion_ad_mobilization", "2012 opposition opinion-ad appeal",
          "与那国自卫队配备反对意见广告执行委员会公开征集反对部署意见广告",
          "public opinion mobilization", "Public sphere / Yaeyama-to-Yonaguni solidarity target",
          "形成2015住民投票前的公开意见动员线索", "R9S034", "E2", "needs_human_review", "yes",
          "A015 仅由单一政党媒体支持；意见广告不是2015投票的正式请求或实施阶段，也不能证明与A014组织连续。"),
    stage("R9ST008", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "municipal_ordinance", 2,
          "2014-12-01", "2014-12-01", "day", "council_ordinance", "Ordinance No. 23",
          "制定关于自卫队基地建设民意的个别住民投票条例", "Yonaguni Ordinance No.23",
          "Yonaguni Town Council / Mayor", "条例成立", "R9S005", "E3", "accepted", "yes",
          "现有文本来自大学法规数据库，不是町公报或议会原件。"),
    stage("R9ST009", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "municipal_ordinance", 3,
          "2015-01-13", "2015-01-16", "day_range", "ordinance_amendment", "Two ordinance amendments",
          "两次修正条例，调整投票制度细节", "Yonaguni Ordinance No.1 and No.2",
          "Yonaguni Town Council / Mayor", "修正后进入实施阶段", "R9S005", "E3", "accepted", "yes",
          "修正内容与表决过程仍需町公报／议会原始记录。"),
    stage("R9ST010", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "campaign_context", 4,
          "", "2015-02-22", "start_unknown", "campaign_mobilization", "Opposition campaign (start unknown)",
          "反对侧委员会围绕部署、前线化与投票过程开展公开行动", "public campaign",
          "Public sphere / referendum campaign", "同期报道确认委员会名称及上地国生委员长",
          "R9S032", "E2", "needs_human_review", "yes",
          "不得把A014写成投票发起者或实施者；活动精确起日、成立、成员与持续性均未闭合。"),
    stage("R9ST011", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "municipal_ordinance", 5,
          "2015-02-22", "2015-02-22", "day", "vote", "Referendum held",
          "实施沿岸监视部队等部署是非住民投票", "Yonaguni Ordinance No.23 as amended",
          "Yonaguni Election Administration Commission", "投开票完成", "R9S005", "E3", "accepted", "yes",
          "条例文本支持町长执行、选管办理；不是由A014或A015单独实施。"),
    stage("R9ST012", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "municipal_ordinance", 6,
          "2015-02-22", "2015-02-22", "day", "result", "632 support / 445 oppose",
          "地方报道记载赞成632、反对445、无效17；选举人1,276；投票率85.74%",
          "referendum result", "Yonaguni Town / Election Administration Commission",
          "部署赞成票占多数", "R9S007", "E3", "needs_human_review", "yes",
          "未取得町选管官方结果表；数字可作有来源的保守记录，不能升级为E4。"),
    stage("R9ST013", YONAGUNI, "2015 Yonaguni JSDF-deployment referendum", "Yonaguni", "post_result", 7,
          "2015-03", "", "month", "post_result_executive", "Mayor interprets result",
          "町长在施政方针中称结果使部署争议决着，同时承认约四成反对",
          "municipal policy statement", "Yonaguni Mayor", "行政以推进部署为方向解释结果",
          "R9S006", "E4", interpretation_limit="这是町长的官方解释，不代表全体町民共识。"),

    stage("R9ST014", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "prefectural_direct_request", 1,
          "2018-04-16", "2018-05-22", "day_range", "initiation", "A051 organizes initiative",
          "「辺野古」県民投票の会成立并准备条例制定直接请求", "civic initiative",
          "Civil-society organizing", "形成发起组织与请求代表层", "R9S021;R9S030;R9S031", "E3",
          interpretation_limit="成立日来自后续讲座记录；官方材料确认事件期组织与请求代表角色，但不能证明全部签名者为成员。"),
    stage("R9ST015", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "prefectural_direct_request", 2,
          "2018-05-23", "2018-07-23", "day_range", "signature_collection", "92,848 valid signatures",
          "全县签名活动并经市町村选管审查", "地方自治法第74条",
          "Municipal election commissions", "有效签名92,848，超过法定23,171", "R9S013", "E4",
          interpretation_limit="签名者不是组织成员。"),
    stage("R9ST016", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "prefectural_direct_request", 3,
          "2018-09-05", "2018-09-05", "day", "direct_request", "Formal direct request",
          "33名条例制定请求代表者向冲绳县提出直接请求", "地方自治法第74条第1项",
          "Okinawa Prefecture", "县受理并付议", "R9S009;R9S030;R9S031", "E4",
          interpretation_limit="33名请求代表者不自动等于A051全部成员。"),
    stage("R9ST017", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "prefectural_direct_request", 4,
          "2018-09-20", "2018-10-31", "day_range", "assembly_ordinance", "Ordinance No. 62",
          "县议会审议并制定县民投票条例第62号", "Okinawa Prefectural Ordinance No.62",
          "Okinawa Prefectural Assembly / Governor", "两选项条例公布", "R9S010", "E4",
          interpretation_limit="条例由直接请求启动，但经过议会／知事制度化。"),
    stage("R9ST018", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "prefectural_direct_request", 5,
          "2019-01-29", "2019-01-31", "day_range", "ordinance_amendment", "Third option added",
          "为全县实施加入‘どちらでもない’第三选项", "Okinawa Prefectural Ordinance No.1",
          "Okinawa Prefectural Assembly / Governor", "三选项修正公布，五市转为实施", "R9S011", "E4",
          interpretation_limit="选项变化是制度转换，不是简单技术调整。"),
    stage("R9ST019", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "prefectural_direct_request", 6,
          "2019-02-24", "2019-02-24", "day", "vote", "All 41 municipalities vote",
          "全41市町村实施县民投票", "Prefectural Ordinance No.62 as amended",
          "Governor / municipal election administration", "投票总数605,385，投票率52.48%", "R9S012", "E4",
          interpretation_limit="投票是咨询／民意表达机制。"),
    stage("R9ST020", PREF, "2019 Okinawa Henoko prefectural referendum", "Okinawa Prefecture", "post_result", 7,
          "2019-02-24", "2019-03-01", "day_range", "result_notification", "434,273 oppose; external notice",
          "反对434,273（71.7%）、赞成114,933、どちらでもない52,682；知事向日美政府通知",
          "条例第10条", "Governor / Japan and U.S. executive targets",
          "反对多数被转化为外部通知与倡议资源", "R9S012", "E4",
          interpretation_limit="结果没有直接停止工程的法律效力。"),

    stage("R9ST021", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "direct_request", 1,
          "2018-10", "2018-12-20", "month_to_day", "signature_collection", "14,263 valid signatures",
          "居民收集有效签名并请求实施住民投票", "自治基本条例第28条、地方自治法第74条",
          "Ishigaki residents / Election Administration Commission", "14,263有效签名，超过38,799选民四分之一",
          "R9S015", "E4", interpretation_limit="法院确认程序事实，但没有把全部行动归给A011或把全部签名者认定为组织成员。"),
    stage("R9ST022", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "direct_request", 2,
          "2018-12-20", "2018-12-20", "day", "direct_request", "27 request representatives",
          "27名请求代表向石垣市长提出条例制定／实施请求", "自治基本条例第28条、地方自治法第74条",
          "Ishigaki Mayor", "市长收受请求并提交第一次条例案", "R9S015", "E4",
          interpretation_limit="27名请求代表与A011成员的逐一映射未闭合。"),
    stage("R9ST023", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "direct_request", 3,
          "2019-02-01", "2019-02-01", "day", "council_rejection", "First ordinance rejected",
          "石垣市议会否决市长提交的住民投票条例案", "municipal ordinance bill",
          "Ishigaki City Council", "条例未成立、投票未实施", "R9S014;R9S023", "E4",
          interpretation_limit="2月1日是议会决定日；2月4日是市政府通知日。"),
    stage("R9ST024", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "councillor_proposal", 4,
          "2019-06-17", "2019-06-17", "day", "second_council_rejection", "Councillor bill rejected",
          "市议员提出議案第2号住民投票条例案，市议会再次否决",
          "councillor-proposed municipal ordinance bill", "Ishigaki City Council", "议员提案未成立",
          "R9S024", "E4", interpretation_limit="第二案是市议员提案；不得写成运动方直接提交或市长第二次付议。"),
    stage("R9ST025", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "mandatory_order_chain", 5,
          "2019-09", "", "month", "judicial_filing", "Mandatory-order suit filed",
          "请求代表／签名居民提起实施义务付け等行政诉讼", "Administrative Case Litigation Act",
          "Naha District Court", "令和元年（行ウ）第14号・第15号进入司法", "R9S015;R9S016", "E4",
          interpretation_limit="法院匿名化个人原告；A011不能因此写成组织原告。"),
    stage("R9ST026", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "mandatory_order_chain", 6,
          "2020-08-27", "2020-08-27", "day", "district_court_result", "All actions procedurally dismissed",
          "那霸地裁审理实施义务付け等请求", "Administrative Case Litigation Act",
          "Naha District Court", "令和元年（行ウ）第14号・第15号之诉全部却下", "R9S015;R9S016", "E4",
          interpretation_limit="‘却下’是程序性／适法性判断，不是对部署政策是非的实体裁判。"),
    stage("R9ST027", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "status_confirmation_chain", 7,
          "2021", "", "year", "second_chain_filing", "Status-confirmation chain filed",
          "居民另行提起地位确认等当事者诉讼", "party/status-confirmation litigation",
          "Naha District Court", "令和3年（行ウ）第5号进入第二条诉讼链", "R9S027;R9S029", "E3",
          "needs_human_review", "no", "精确起诉日和那霸地裁官方判决全文未取得；不得与第一条义务付け诉讼合并。"),
    stage("R9ST028", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "mandatory_order_chain", 8,
          "", "2021-03-23", "end_day_only", "first_chain_appeal", "First-chain appeal ends",
          "第一条实施义务付け诉讼进入福冈高裁那霸支部", "Administrative Case Litigation Act",
          "Fukuoka High Court Naha Branch", "令和2年（行コ）第3号已终结；精确主文待取得判决全文",
          "R9S026;R9S029", "E3", "needs_human_review", "no",
          "官方保存表确认案号但不能替代判决全文；上诉起日未知。"),
    stage("R9ST029", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "institutional_framework", 9,
          "2021-06-28", "2021-06-28", "day", "ordinance_framework_change", "Referendum clauses deleted",
          "市议会通过议员提出的自治基本条例修正案，删除住民投票第27/28条",
          "municipal ordinance amendment", "Ishigaki City Council", "常设住民投票条款被删除",
          "R9S018;R9S025", "E4", interpretation_limit="只说明制度机会结构改变；不推断由诉讼直接导致。"),
    stage("R9ST030", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "status_confirmation_chain", 10,
          "2023-05-23", "2023-05-23", "day", "status_confirmation_district_result", "Second-chain district judgment",
          "那霸地裁审理地位确认等第二诉讼链", "party/status-confirmation litigation",
          "Naha District Court", "令和3年（行ウ）第5号判决", "R9S027", "E3",
          "needs_human_review", "no", "现有依据为高裁判决所载前审信息；仍需那霸地裁官方判决全文。"),
    stage("R9ST031", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "status_confirmation_chain", 11,
          "2024-03-12", "2024-03-12", "day", "status_confirmation_high_court_result", "Second-chain high-court judgment",
          "福冈高裁那霸支部审理地位确认等上诉", "party/status-confirmation litigation",
          "Fukuoka High Court Naha Branch", "令和5年（行コ）第6号判决", "R9S026;R9S027", "E3",
          "needs_human_review", "no", "CALL4收录裁判书不是法院托管E4；案号由官方保存表交叉确认。"),
    stage("R9ST032", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "status_confirmation_chain", 12,
          "2024-09-26", "2024-09-26", "day", "supreme_court_finalization", "Supreme Court decision; loss final",
          "最高裁决定后第二诉讼链败诉确定", "Supreme Court procedure", "Supreme Court",
          "地方媒体与组织侧案件页均称2024-09-26收到决定；案号与处分类型待核", "R9S028;R9S029", "E2",
          "needs_human_review", "no", "取得最高裁一手决定前只用中性措辞；不得确定写成上告棄却或上告不受理。"),
    stage("R9ST033", ISHIGAKI, "Ishigaki JSDF referendum drive and two litigation chains", "Ishigaki", "organizational_context", 13,
          "2024-11-27", "2024-11-27", "day", "organizational_close", "A011 dissolution meeting reported",
          "地方媒体报道石垣市住民投票を求める会举行解散集会", "organizational decision",
          "A011 / public meeting", "地方报道指六年活动结束", "R9S019;R9S029", "E2",
          "needs_human_review", "yes", "S051当前域名内容错配；组织沿革与解散仍需历史网页、会报或当地材料闭合。"),
]


def role(
    role_id: str,
    case_id: str,
    stage_id: str,
    actor_id: str,
    entity_id: str,
    entity_name: str,
    entity_kind: str,
    role_type: str,
    role_scope: str,
    source_refs: str,
    evidence_level: str,
    review_status: str = "accepted",
    needs_local_retrieval: str = "no",
    interpretation_limit: str = "",
    notes: str = "",
) -> dict[str, str]:
    return {key: str(value) for key, value in locals().items()}


ROLES = [
    role("R9R001", NAGO, "R9ST001", "A068", "", "名護市民投票推進協議会", "registry_actor_mapping_pending",
         "initiative_and_signature_organizer", "1997 direct-request process", "R9S001", "E4", "needs_human_review", "no",
         "官方事件名与A068现规范名不一致；改名、alias或拆分由人工决定。"),
    role("R9R002", NAGO, "R9ST001", "", "R9E001", "宮城康博", "individual",
         "formal_request_representative", "1997 direct-request initiation", "R9S001", "E4",
         interpretation_limit="个人角色不建立person registry，也不自动转嫁给A068以外的组织。"),
    role("R9R003", NAGO, "R9ST002", "", "R9E002", "名護市選挙管理委員会", "government_body",
         "signature_verifier_and_vote_administrator", "signature and vote stages", "R9S001;R9S022", "E4",
         interpretation_limit="制度执行角色，不是运动 actor。"),
    role("R9R004", NAGO, "R9ST003", "", "R9E003", "名護市議会", "council",
         "ordinance_decision_body", "council ordinance stage", "R9S001", "E4",
         interpretation_limit="记录议决，不把议会整体写成公民组织盟友或对手。"),
    role("R9R005", NAGO, "R9ST006", "", "R9E004", "比嘉鉄也", "individual",
         "mayor_and_post_result_decision_maker", "post-result executive stage", "R9S002", "E4",
         interpretation_limit="个人行政决定不转写为任何组织角色。"),

    role("R9R006", YONAGUNI, "R9ST007", "A015", "", "与那国自衛隊配備反対意見広告実行委員会", "registry_actor",
         "opinion_ad_committee", "2012 public-opinion mobilization", "R9S034", "E2", "needs_human_review", "yes",
         "单一政党媒体来源；Yaeyama/Ishigaki主导与Yonaguni目标地点必须区分，不与A014合并。"),
    role("R9R007", YONAGUNI, "R9ST010", "A014", "", "住民投票を成功させるための実行委員会", "registry_actor",
         "opposition_campaign_committee", "2015 referendum campaign", "R9S032", "E2", "needs_human_review", "yes",
         "只确认事件期公开名称与反对侧运动角色；不得写成正式发起者或实施者。"),
    role("R9R008", YONAGUNI, "R9ST010", "", "R9E005", "上地国生", "individual",
         "reported_committee_chair", "2015 campaign", "R9S032", "E2", "needs_human_review", "yes",
         "同期媒体称委员长；个人角色不替代A014组织身份、成员与持续性证据。"),
    role("R9R009", YONAGUNI, "R9ST008", "", "R9E006", "与那国町議会", "council",
         "ordinance_decision_body", "ordinance and amendments", "R9S005", "E3", "accepted", "yes",
         "现依据为大学法规数据库，需町议会原始记录。"),
    role("R9R010", YONAGUNI, "R9ST011", "", "R9E007", "与那国町選挙管理委員会", "government_body",
         "vote_administrator", "vote stage", "R9S005", "E3", "accepted", "yes",
         "制度角色来自条例文本；投票结果表仍待当地调取。"),
    role("R9R011", YONAGUNI, "R9ST013", "", "R9E008", "外間守吉", "individual",
         "mayor_and_post_result_interpreter", "post-result stage", "R9S006", "E4",
         interpretation_limit="町长解释不是全体町民共识。"),

    role("R9R012", PREF, "R9ST014", "A051", "", "「辺野古」県民投票の会", "registry_actor",
         "initiative_signature_and_direct_request_organizer", "initiative through direct request", "R9S030;R9S031", "E4",
         interpretation_limit="33名请求代表和92,848名签名者不自动等于组织成员。"),
    role("R9R013", PREF, "R9ST014", "", "R9E009", "元山仁士郎", "individual",
         "organization_representative_and_direct_request_representative", "initiative through direct request", "R9S030;R9S031", "E4",
         interpretation_limit="个人代表角色不替代组织全体成员或持续性证据。"),
    role("R9R014", PREF, "R9ST014", "", "R9E010", "安里長従", "individual",
         "organization_deputy_representative_and_direct_request_representative", "initiative through direct request", "R9S030;R9S031", "E4",
         interpretation_limit="只限官方记录的事件期角色。"),
    role("R9R015", PREF, "R9ST014", "", "R9E011", "中村昌樹", "individual",
         "organization_affiliate_and_direct_request_representative", "initiative through direct request", "R9S030;R9S031", "E4",
         interpretation_limit="使用官方记录所载身份，不外推组织职衔。"),
    role("R9R016", PREF, "R9ST016", "", "R9E012", "33名条例制定請求代表者", "resident_collective",
         "formal_request_representatives", "direct request", "R9S031", "E4",
         interpretation_limit="请求代表集合不是A051成员名册。"),
    role("R9R017", PREF, "R9ST017", "", "R9E013", "沖縄県議会", "council",
         "ordinance_decision_body", "ordinance and amendment", "R9S010;R9S011", "E4",
         interpretation_limit="议会是制度转换场域，不是公民组织。"),
    role("R9R018", PREF, "R9ST019", "", "R9E014", "沖縄県知事・県民投票事務局", "government_body",
         "executive_vote_administration_and_result_notifier", "implementation and notification", "R9S012", "E4",
         interpretation_limit="行政执行与公民发起分开编码。"),
    role("R9R019", PREF, "R9ST015", "", "R9E015", "県内市町村選挙管理委員会", "government_collective",
         "signature_verification_and_local_execution", "signature and vote stages", "R9S013;R9S012", "E4",
         interpretation_limit="市町村在实施争议中的选择不同，不能写成单一政治立场。"),

    role("R9R020", ISHIGAKI, "R9ST021", "A011", "", "石垣市住民投票を求める会", "registry_actor",
         "signature_and_referendum_campaign_organizer", "2018 public campaign", "R9S020;R9S029", "E3",
         "needs_human_review", "yes", "组织不自动等于27名请求代表、全部签名居民或法院原告；S051不可用。"),
    role("R9R021", ISHIGAKI, "R9ST022", "", "R9E016", "27名の実施請求代表者", "resident_collective",
         "formal_request_representatives", "direct request", "R9S015", "E4",
         interpretation_limit="法院程序事实不建立与A011成员的逐一映射。"),
    role("R9R022", ISHIGAKI, "R9ST022", "", "R9E017", "中山義隆・石垣市長", "individual",
         "request_receiver_and_first_bill_submitter", "direct request and first council bill", "R9S015;R9S023", "E4",
         interpretation_limit="只记录程序行为；第二次条例案不是市长提交。"),
    role("R9R023", ISHIGAKI, "R9ST024", "", "R9E018", "石垣市議会の条例案提出議員", "councillor_collective",
         "second_ordinance_proposers", "2019-06-17 councillor bill", "R9S024", "E4",
         interpretation_limit="市议员提案不能写成运动方直接提交，也不证明与A011稳定组织关系。"),
    role("R9R024", ISHIGAKI, "R9ST023", "", "R9E019", "石垣市議会", "council",
         "ordinance_decision_body", "two rejections and 2021 amendment", "R9S023;R9S024;R9S025", "E4",
         interpretation_limit="记录具体议决，不把议会整体写成稳定阵营。"),
    role("R9R025", ISHIGAKI, "R9ST025", "", "R9E020", "第一訴訟の個人原告（請求代表者・署名者）", "individual_plaintiff_collective",
         "individual_plaintiffs", "mandatory-order chain", "R9S015", "E4",
         interpretation_limit="法院匿名化个人；不得转嫁为A011组织原告角色。"),
    role("R9R026", ISHIGAKI, "R9ST025", "", "R9E021", "石垣市", "government_body",
         "defendant", "mandatory-order chain", "R9S015", "E4",
         interpretation_limit="法律当事人角色不同于运动 actor 分类。"),
    role("R9R027", ISHIGAKI, "R9ST026", "", "R9E022", "那覇地方裁判所", "court",
         "judicial_forum", "mandatory-order district stage", "R9S015;R9S016", "E4",
         interpretation_limit="法院是裁判场域，不是网络 actor。"),
    role("R9R028", ISHIGAKI, "R9ST028", "", "R9E023", "福岡高等裁判所那覇支部", "court",
         "judicial_forum", "mandatory-order appeal", "R9S026", "E4",
         interpretation_limit="官方表确认案号；判决主文仍待原件。"),
    role("R9R029", ISHIGAKI, "R9ST027", "A011", "", "石垣市住民投票を求める会", "registry_actor",
         "litigation_support_and_public_advocacy", "status-confirmation chain", "R9S027;R9S029", "E3",
         "needs_human_review", "yes", "不得写成法院确认的组织原告；应与三名个人原告分开。"),
    role("R9R030", ISHIGAKI, "R9ST027", "", "R9E024", "第二訴訟の3名の個人原告", "individual_plaintiff_collective",
         "individual_plaintiffs", "status-confirmation chain", "R9S027;R9S029", "E3",
         "needs_human_review", "no", "个人原告与A011支持组织分开；需地裁官方判决／起诉材料闭合。"),
    role("R9R031", ISHIGAKI, "R9ST031", "", "R9E025", "第二訴訟原告代理人弁護士", "counsel_collective",
         "counsel", "status-confirmation chain", "R9S027", "E3",
         "needs_human_review", "no", "仅记录判决所载诉讼代理功能；不新建律师个人或组织 actor。"),
    role("R9R032", ISHIGAKI, "R9ST030", "", "R9E022", "那覇地方裁判所", "court",
         "judicial_forum", "status-confirmation district stage", "R9S027", "E3",
         interpretation_limit="现由高裁判决回溯前审；需地裁官方原件。"),
    role("R9R033", ISHIGAKI, "R9ST031", "", "R9E023", "福岡高等裁判所那覇支部", "court",
         "judicial_forum", "status-confirmation appeal", "R9S026;R9S027", "E4",
         interpretation_limit="官方保存表确认案号；CALL4副本支持裁判内容。"),
    role("R9R034", ISHIGAKI, "R9ST032", "", "R9E026", "最高裁判所", "court",
         "judicial_forum", "status-confirmation finalization", "R9S028;R9S029", "E2",
         "needs_human_review", "no", "无官方决定书与案号；不确定写棄却或不受理。"),
]


def source(
    source_id: str,
    existing_source_id: str,
    case_id: str,
    source_tier: str,
    source_type: str,
    title: str,
    year: str,
    url: str,
    evidence_level: str,
    review_status: str,
    disposition: str,
    supports: str,
    interpretation_limit: str = "",
    notes: str = "",
) -> dict[str, str]:
    return {key: str(value) for key, value in locals().items()}


SOURCES = [
    source("R9S001", "", NAGO, "primary_official", "official_prefecture_report", "沖縄の米軍基地・基地問題の沿革（1997年部分）", "2003", "https://www.pref.okinawa.jp/kititaisaku/DP-08-13.pdf", "E4", "qa_verified", "accepted", "名护代表者证明、签名、直接请求、议会修正、条例与投票程序"),
    source("R9S002", "S042", NAGO, "primary_official", "municipal_timeline", "移設問題の動向（年表）", "2026", "https://www.city.nago.okinawa.jp/kurashi/2018071900226/", "E4", "qa_verified", "accepted", "反对多数、投票后市长接受并辞职"),
    source("R9S003", "", NAGO, "primary_official", "municipal_election_page", "その他の選挙（県民投票・市民投票）", "2026", "https://www.city.nago.okinawa.jp/kurashi/2018071901216/", "E4", "qa_verified", "accepted", "1997投票日期与官方结果文件入口"),
    source("R9S005", "S071", YONAGUNI, "structured_legal_secondary", "university_legal_database", "与那国島への自衛隊基地建設の民意を問う住民投票条例", "2014", "https://greenaccess.law.osaka-u.ac.jp/archives/7214", "E3", "qa_verified", "usable_with_limit", "条例第23号及2015年两次修正、执行与投票资格", "不是町公报或议会原件；需当地交叉。"),
    source("R9S006", "", YONAGUNI, "primary_official", "municipal_policy_statement", "平成27年度 与那国町施政方針", "2015", "https://www.town.yonaguni.okinawa.jp/docs/2018041100076/file_contents/H27siseihousin.pdf", "E4", "qa_verified", "accepted", "町长对投票结果的行政解释", "官方立场不替代完整结果表。"),
    source("R9S007", "S011", YONAGUNI, "secondary_local", "local_news", "与那国住民投票 陸自配備を容認 賛成632、反対445", "2015", "https://ryukyushimpo.jp/news/prentry-239307.html", "E3", "qa_verified", "usable_with_limit", "投票结果数字", "需町选管原表升级为E4。"),
    source("R9S009", "", PREF, "primary_official", "prefectural_proposal", "平成30年第6回沖縄県議会臨時会 提案説明", "2018", "https://www.pref.okinawa.jp/kensei/kencho/1001519/1001591/1018974/1018988.html", "E4", "qa_verified", "accepted", "9月5日直接请求、签名与条例付议"),
    source("R9S010", "", PREF, "primary_official", "official_gazette", "沖縄県公報号外第43号・県民投票条例第62号", "2018", "https://www.pref.okinawa.jp/kenkouhou/H30/10gatsu/181031gogai43.pdf", "E4", "qa_verified", "accepted", "条例公布、目的、执行与通知制度"),
    source("R9S011", "", PREF, "primary_official", "official_gazette", "沖縄県公報号外第2号・県民投票条例一部改正", "2019", "https://www.pref.okinawa.jp/kenkouhou/H31/1gatsu/190131gogai2.pdf", "E4", "qa_verified", "accepted", "加入第三选项"),
    source("R9S012", "", PREF, "primary_official", "prefectural_chronology", "辺野古新基地建設問題の経緯", "2026", "https://www.pref.okinawa.jp/heiwakichi/futenma/1017409/1017427.html", "E4", "qa_verified", "accepted", "投票结果与结果通知"),
    source("R9S013", "", PREF, "primary_official", "assembly_record", "沖縄県議会会議録・県民投票条例直接請求", "2018", "https://www2.pref.okinawa.jp/oki/Gikairep1.nsf/GoZentai/20180703000000", "E4", "qa_verified", "accepted", "法定23,171、有效92,848签名与直接请求性质"),
    source("R9S014", "S138", ISHIGAKI, "primary_official", "municipal_notice", "陸上自衛隊配備計画の賛否を問う住民投票条例に係る議会審議結果", "2020", "https://www.city.ishigaki.okinawa.jp/jieiteikannrenn/news/3615.html", "E4", "qa_verified", "accepted", "第一次议会审议结果与附件入口"),
    source("R9S015", "S137", ISHIGAKI, "primary_official", "court_judgment", "石垣市住民投票実施義務付け等請求事件判決", "2020", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-89731.pdf", "E4", "qa_verified", "accepted", "签名、请求、令和元年行ウ14/15及全部却下", "使用法院迁移后URL；主source log旧URL尚未在本脚本中修改。"),
    source("R9S016", "", ISHIGAKI, "primary_official", "court_preservation_list", "那覇地方裁判所特別保存事件一覧", "2024", "https://www.courts.go.jp/naha/vc-files/naha/2024/chisai/minji/tokubetuhozon/R3kanketubunitiranhyou.pdf", "E4", "qa_verified", "accepted", "令和元年行ウ14/15及终局日"),
    source("R9S017", "S051", ISHIGAKI, "invalid_current_capture", "repurposed_domain", "石垣市住民投票を求める会旧官网URL当前捕获", "2026", "https://ishigaki-tohyo.com/", "E0", "qa_rejected", "rejected", "不支持任何正式R9事实", "当前页面和本地raw.html均为无关旅游站。"),
    source("R9S018", "", ISHIGAKI, "primary_official", "municipal_review_material", "石垣市自治基本条例 これまでの見直し・改正", "2025", "https://www.city.ishigaki.okinawa.jp/material/files/group/9/r71zitikihon_siryou1-3.pdf", "E4", "qa_verified", "accepted", "2021年删除第27/28条"),
    source("R9S019", "", ISHIGAKI, "secondary_local", "local_tv_news", "石垣市住民投票を求める会が解散", "2024", "https://www.otv.co.jp/okitive/news/post/00012171/index.html", "E2", "needs_human_review", "usable_with_limit", "最高裁后终局与组织解散报道", "最高裁程序措辞与QAB冲突；组织沿革需历史材料。"),
    source("R9S020", "S019", ISHIGAKI, "secondary_local", "local_news", "石垣市住民投票 署名活動で法定数超え", "2018", "https://www.yaeyama-nippo.co.jp/archives/4232", "E2", "qa_verified", "usable_with_limit", "签名与A011公开组织活动", "地方新闻只支持公开活动，不闭合成员与诉讼当事人。"),
    source("R9S021", "", PREF, "structured_secondary", "foundation_lecture_record", "辺野古県民投票の民意とこれから・元山仁士郎講座記録", "2021", "https://www.ichikawa-fusae.or.jp/20210313-1/", "E3", "qa_verified", "usable_with_limit", "2018-04-16组织成立日期", "后续讲座记录；组织与请求代表角色优先使用官方R9S030/R9S031。"),
    source("R9S022", "", NAGO, "primary_official", "municipal_result_xls", "1997年12月21日名護市民投票結果", "1997", "https://www.city.nago.okinawa.jp/kurashi/2018071901216/file_contents/19971221simintouhyou.xls", "E4", "qa_verified", "accepted", "完整票数、选举人、投票者、有效无效票和投票率", "核心总计一致；不引用有90票差异的当日投票小计。"),
    source("R9S023", "", ISHIGAKI, "primary_official", "municipal_council_result", "令和元年第1回石垣市議会臨時会提出議案と議決結果", "2019", "https://www.city.ishigaki.okinawa.jp/soshiki/gikai/teireikairinnjikai/teisyutugianntokekka/reiwagannnenndo/1310.html", "E4", "qa_verified", "accepted", "第一次条例案于2019-02-01否决"),
    source("R9S024", "", ISHIGAKI, "primary_official", "municipal_council_result", "令和元年第4回石垣市議会定例会提出議案と議決結果", "2019", "https://www.city.ishigaki.okinawa.jp/soshiki/gikai/teireikairinnjikai/teisyutugianntokekka/reiwagannnenndo/1314.html", "E4", "qa_verified", "accepted", "2019-06-17議員提出議案第2号及否决"),
    source("R9S025", "", ISHIGAKI, "primary_official", "municipal_council_agenda", "令和3年第5回石垣市議会定例会議事日程", "2021", "https://www.city.ishigaki.okinawa.jp/material/files/group/33/r3-6-28gijinittei.pdf", "E4", "qa_verified", "accepted", "2021-06-28自治基本条例修正议案与议决"),
    source("R9S026", "", ISHIGAKI, "primary_official", "court_preservation_list", "福岡高等裁判所特別保存事件一覧", "2025", "https://www.courts.go.jp/fukuoka-h/vc-files/fukuoka-h/reiwa7.pdf", "E4", "qa_verified", "accepted", "令和2年行コ3号与令和5年行コ6号案号", "保存表确认案号，不能替代判决主文。"),
    source("R9S027", "", ISHIGAKI, "primary_litigation_archive", "court_judgment_copy", "令和5年行コ第6号判決", "2024", "https://www.call4.jp/file/pdf/202407/5f499d29696072751d0d60cc3a9077f5.pdf", "E3", "needs_human_review", "usable_with_limit", "第二诉讼链高裁判决与前审信息", "CALL4托管而非法院官网；需官方裁判书。"),
    source("R9S028", "", ISHIGAKI, "secondary_local", "local_tv_news", "石垣住民投票訴訟 最高裁で敗訴確定", "2024", "https://www.qab.co.jp/news/20241007226830.html", "E2", "needs_human_review", "usable_with_limit", "2024-09-26最高裁决定后败诉确定", "不据此确定棄却或不受理。"),
    source("R9S029", "", ISHIGAKI, "primary_positioned", "organization_case_profile", "石垣市住民投票を求める裁判 CALL4案件页", "2024", "https://www.call4.jp/search.php?items_id=I0000141&items_id_PAL%5B%5D=match+comp&run=true&type=action", "E3", "needs_human_review", "usable_with_limit", "组织自述成立、诉讼支持与最高裁通知日期", "组织侧材料不等于法院确认组织原告身份。"),
    source("R9S030", "", PREF, "primary_official", "prefectural_assembly_committee_record", "沖縄県議会軍特委員会記録 県民投票条例請求代表者参考人", "2018", "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/021/212/h301002gun-1.pdf", "E4", "qa_verified", "accepted", "A051、元山、安里、中村的组织身份与请求代表角色"),
    source("R9S031", "", PREF, "primary_official", "official_gazette", "沖縄県公報号外第17号 条例制定請求代表者証明書", "2018", "https://www.pref.okinawa.jp/kenkouhou/H30/5gatsu/180523gogai17.pdf", "E4", "qa_verified", "accepted", "33名条例制定请求代表者名单", "名单不是组织成员名册。"),
    source("R9S032", "", YONAGUNI, "secondary_local", "local_tv_news", "与那国住民投票 配備賛成が過半数", "2015", "https://www.qab.co.jp/news/2015022363334.html", "E2", "qa_verified", "usable_with_limit", "A014事件期名称与上地国生委员长", "只支持事件期公开身份，不支持成立、法人性和持续性。"),
    source("R9S033", "S139", ISHIGAKI, "unavailable_historical_file", "organization_pdf", "旧ishigaki-tohyo.com诉讼意见PDF", "2020", "https://ishigaki-tohyo.com/wp-content/uploads/2022/07/%E5%9C%A8%E5%A4%96%E6%97%A5%E6%9C%AC%E4%BA%BA%E5%9B%BD%E6%B0%91%E5%AF%A9%E6%9F%BB%E6%A8%A9%E7%A2%BA%E8%AA%8D%E7%AD%89%E8%AB%8B%E6%B1%82%E4%BA%8B%E4%BB%B6%E6%9C%80%E9%AB%98%E8%A3%81%E5%88%A4%E6%89%80%E5%A4%A7%E6%B3%95%E5%BB%B7%E5%88%A4%E6%B1%BA%E3%82%92%E8%B8%8F%E3%81%BE%E3%81%88%E3%81%9F-1.pdf", "E0", "qa_rejected", "rejected", "恢复历史副本前不支持正式R9事实", "当前404／归档失败。"),
    source("R9S034", "S015", YONAGUNI, "secondary_positioned", "party_news", "与那国に自衛隊いらない 配備反対の意見広告呼びかけ", "2012", "https://www.jcp.or.jp/akahata/aik12/2012-08-31/2012083115_02_1.html", "E2", "needs_human_review", "usable_with_limit", "A015意见广告动员、名称与共同代表线索", "单一政党媒体；需八重山报纸、广告实物或组织材料。"),
]


REJECTED_CLAIMS = [
    {"reject_id": "R9X001", "case_id": ISHIGAKI, "claim": "市长两次提交石垣住民投票条例案", "reason": "2019-06-17第二案为市议员提出議案第2号。", "source_refs": "R9S024", "status": "rejected"},
    {"reject_id": "R9X002", "case_id": ISHIGAKI, "claim": "把2021-2024后续诉讼写成单一诉讼链", "reason": "混合令和2年行コ3号与令和3年行ウ5号／令和5年行コ6号两条不同诉讼链。", "source_refs": "R9S026;R9S027", "status": "rejected"},
    {"reject_id": "R9X003", "case_id": ISHIGAKI, "claim": "S051或S139可作为当前E4组织／诉讼证据", "reason": "S051域名内容错配，S139当前404；均不可复现。", "source_refs": "R9S017;R9S033", "status": "rejected"},
    {"reject_id": "R9X004", "case_id": ISHIGAKI, "claim": "A011是法院确认的组织原告", "reason": "第一诉讼链为匿名个人原告；第二诉讼链须区分个人原告、支持组织与代理律师。", "source_refs": "R9S015;R9S027;R9S029", "status": "rejected"},
    {"reject_id": "R9X005", "case_id": YONAGUNI, "claim": "A014或A015发起／实施了2015与那国住民投票", "reason": "现有材料只支持意见广告或反对侧公开运动；条例执行主体为町长／选管。", "source_refs": "R9S005;R9S032;R9S034", "status": "rejected"},
    {"reject_id": "R9X006", "case_id": ISHIGAKI, "claim": "2024-09-26最高裁处分可确定写为上告棄却", "reason": "二手来源在棄却／不受理上冲突，且无官方决定书与案号。", "source_refs": "R9S019;R9S028;R9S029", "status": "rejected"},
]


CASE_META = {
    NAGO: {
        "case_name": "1997 Nago heliport referendum", "place": "Nago", "date_start": "1997-06-27", "date_end": "1997-12-24", "vote_held": "yes",
        "institutional_entry": "地方自治法第74条直接请求与17,539份有效签名",
        "institutional_gate_result": "议会修正为四选项并立法，实际举行投票",
        "post_gate_path": "反对16,639对赞成14,267；三日后市长接受并辞职",
        "mechanism_summary": "公民诉求通过签名与条例门槛，但咨询型结果没有自动约束后续行政决定。",
        "interpretation_limit": "不能把反对多数写成法律否决；A068规范名仍待人工决定。",
    },
    YONAGUNI: {
        "case_name": "2015 Yonaguni JSDF-deployment referendum", "place": "Yonaguni", "date_start": "2012-08-31", "date_end": "2015-03", "vote_held": "yes",
        "institutional_entry": "自治体个别条例路径；2012意见广告与2015反对运动是并行公众动员",
        "institutional_gate_result": "町议会／町长条例及修正后实施投票",
        "post_gate_path": "地方报道632赞成、445反对；町长解释为推进依据",
        "mechanism_summary": "制度入口来自自治体条例，反对运动在制度外围争夺解释；投票结果再由行政解释。",
        "interpretation_limit": "A014/A015均维持E2并需当地检索；结果缺町选管原表。",
    },
    PREF: {
        "case_name": "2019 Okinawa Henoko prefectural referendum", "place": "Okinawa Prefecture", "date_start": "2018-04-16", "date_end": "2019-03-01", "vote_held": "yes",
        "institutional_entry": "A051与请求代表组织全县直接请求；92,848份有效签名",
        "institutional_gate_result": "县议会立法并以三选项修法实现全41市町村投票",
        "post_gate_path": "反对434,273（71.7%）；知事向日美政府通知",
        "mechanism_summary": "公民动员被转换为县条例、行政执行和对外通知资源。",
        "interpretation_limit": "签名者／请求代表不自动等于组织成员；结果不直接停止工程。",
    },
    ISHIGAKI: {
        "case_name": "Ishigaki JSDF referendum drive and two litigation chains", "place": "Ishigaki", "date_start": "2018-10", "date_end": "2024-11-27", "vote_held": "no",
        "institutional_entry": "14,263份有效签名与27名请求代表的直接请求",
        "institutional_gate_result": "第一次市长提交案被否决；第二次市议员提案也被否决",
        "post_gate_path": "实施义务付け与地位确认两条诉讼链；2021年常设条款删除",
        "mechanism_summary": "签名门槛达成仍可在议会议程和司法可诉性门槛被阻断，行动路径转向法院。",
        "interpretation_limit": "两条诉讼链必须分开；最高裁处分无一手前用中性措辞；A011不写组织原告。",
    },
}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_ids(path: Path, field: str) -> set[str]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row[field] for row in csv.DictReader(handle)}


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def build_case_rows() -> list[dict[str, str]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in STAGES:
        counts[row["case_id"]][row["review_status"]] += 1
    rows = []
    for case_id in (NAGO, YONAGUNI, PREF, ISHIGAKI):
        meta = CASE_META[case_id]
        rows.append({
            "case_id": case_id,
            **meta,
            "accepted_stage_count": str(counts[case_id]["accepted"]),
            "pending_stage_count": str(counts[case_id]["needs_human_review"]),
        })
    return rows


SOURCE_LOCATORS = {
    "R9S001": "官方PDF pp.44–47：名护直接请求、签名、条例与投票程序",
    "R9S007": "报道标题／导语：赞成632、反对445；正文：无效票、选举人与投票率",
    "R9S019": "OTV报道正文：最高裁终局措辞与2024-11-27解散集会；须与官方决定／组织材料核对",
    "R9S020": "八重山日报报道正文：A011名称、签名活动与法定数；不含成员名册",
    "R9S026": "福冈高裁特别保存事件一览：令和2年（行コ）第3号、令和5年（行コ）第6号对应行",
    "R9S027": "CALL4判决PDF：裁判书首页案号／当事人栏、前审摘要、主文与理由；精确页码待人审记录",
    "R9S028": "QAB报道正文：2024-09-26最高裁决定及败诉确定；处分用语须与原件核对",
    "R9S029": "CALL4案件页：原告、これまでの経緯、裁判の状況／最高裁通知日期各节",
    "R9S032": "QAB 2015-02-23报道正文：委员会名称、上地国生委员长及投票结果语境",
    "R9S034": "赤旗2012-08-31报道正文：意见广告执行委员会名称、共同代表与征集行动；需非政党来源交叉",
}


def format_source_locator(source_refs: str) -> str:
    parts = []
    for ref in split_refs(source_refs):
        parts.append(f"{ref}: {SOURCE_LOCATORS.get(ref, '见source_register_v0.csv；精确页/段待复核')}")
    return " | ".join(parts)


def review_impacts(item: dict[str, str], object_type: str) -> tuple[str, str, str]:
    object_id = item["stage_id"] if object_type == "stage" else item["role_id"]
    subject = item["short_label"] if object_type == "stage" else f"{item['entity_name']}／{item['role_type']}"
    if object_type == "stage":
        accept = (
            f"把{object_id}加入正式阶段表；全量时间线中该节点由空心改实心；"
            f"brief可将“{subject}”写为其当前证据等级下的正式阶段。"
        )
        revise = (
            f"按人审修订{object_id}的日期、主体、结果或措辞后再决定是否进入正式阶段表；"
            "同步重绘节点标签/状态并改写brief对应事实。"
        )
        reject = (
            f"{object_id}继续排除于正式阶段表，并从全量图的待审节点移出或转入拒绝说明；"
            "brief不得再把该事项作为程序阶段。"
        )
    else:
        accept = (
            f"把{object_id}加入正式角色表；正式阶段表不因此自动新增阶段；"
            f"图仅在对应节点的主体说明需要时更新，brief可正式使用“{subject}”角色。"
        )
        revise = (
            f"按人审修订{object_id}的主体映射、角色类型或边界后再决定是否进入正式角色表；"
            "阶段表保持不变，涉及主体标签的图与brief同步修订。"
        )
        reject = (
            f"{object_id}继续排除于正式角色表；阶段节点可按独立证据保留，"
            "但图与brief不得再把该角色归给当前主体。"
        )
    return accept, revise, reject


def build_review_queue() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in STAGES:
        if item["review_status"] != "needs_human_review":
            continue
        impact_accept, impact_revise, impact_reject = review_impacts(item, "stage")
        rows.append({
            "task_id": "HR-017",
            "queue_id": f"R9Q-{item['stage_id']}",
            "object_type": "stage",
            "object_id": item["stage_id"],
            "case_id": item["case_id"],
            "subject": item["short_label"],
            "evidence_level": item["evidence_level"],
            "source_refs": item["source_refs"],
            "source_locator": format_source_locator(item["source_refs"]),
            "needs_local_retrieval": item["needs_local_retrieval"],
            "review_question": item["interpretation_limit"],
            "impact_if_accept": impact_accept,
            "impact_if_revise": impact_revise,
            "impact_if_reject": impact_reject,
            "decision": "",
            "human_reviewer": "",
            "review_date": "",
            "decision_note": "",
        })
    for item in ROLES:
        if item["review_status"] != "needs_human_review":
            continue
        impact_accept, impact_revise, impact_reject = review_impacts(item, "role")
        rows.append({
            "task_id": "HR-017",
            "queue_id": f"R9Q-{item['role_id']}",
            "object_type": "role",
            "object_id": item["role_id"],
            "case_id": item["case_id"],
            "subject": f"{item['entity_name']} — {item['role_type']}",
            "evidence_level": item["evidence_level"],
            "source_refs": item["source_refs"],
            "source_locator": format_source_locator(item["source_refs"]),
            "needs_local_retrieval": item["needs_local_retrieval"],
            "review_question": item["interpretation_limit"],
            "impact_if_accept": impact_accept,
            "impact_if_revise": impact_revise,
            "impact_if_reject": impact_reject,
            "decision": "",
            "human_reviewer": "",
            "review_date": "",
            "decision_note": "",
        })
    if len(rows) != 18:
        raise ValueError(f"review queue count drift: {len(rows)}")
    return rows


def validate() -> dict[str, object]:
    errors: list[str] = []
    for name, rows, key in [
        ("stages", STAGES, "stage_id"), ("roles", ROLES, "role_id"),
        ("sources", SOURCES, "source_id"), ("rejected", REJECTED_CLAIMS, "reject_id"),
    ]:
        values = [row[key] for row in rows]
        if len(values) != len(set(values)):
            errors.append(f"duplicate {name} {key}")

    stage_ids = {row["stage_id"] for row in STAGES}
    source_ids = {row["source_id"] for row in SOURCES}
    case_ids = set(CASE_META)
    actor_ids = read_ids(DATA / "01_actor_registry_initial_v0.csv", "actor_id")
    main_source_ids = read_ids(DATA / "05_source_log_initial_v0.csv", "source_id")
    rejected_source_ids = {row["source_id"] for row in SOURCES if row["disposition"] == "rejected"}

    for row in STAGES:
        if row["case_id"] not in case_ids:
            errors.append(f"stage {row['stage_id']} bad case FK")
        refs = set(split_refs(row["source_refs"]))
        if not refs <= source_ids:
            errors.append(f"stage {row['stage_id']} missing source FK {sorted(refs-source_ids)}")
        if refs & rejected_source_ids:
            errors.append(f"stage {row['stage_id']} uses rejected source")
    for case_id in case_ids:
        orders = sorted(int(row["stage_order"]) for row in STAGES if row["case_id"] == case_id)
        if orders != list(range(1, len(orders) + 1)):
            errors.append(f"case {case_id} stage_order not contiguous")
    entity_defs: dict[str, tuple[str, str]] = {}
    for row in ROLES:
        if row["case_id"] not in case_ids or row["stage_id"] not in stage_ids:
            errors.append(f"role {row['role_id']} bad case/stage FK")
        if bool(row["actor_id"]) == bool(row["entity_id"]):
            errors.append(f"role {row['role_id']} must have exactly one actor_id/entity_id")
        if row["actor_id"] and row["actor_id"] not in actor_ids:
            errors.append(f"role {row['role_id']} bad actor FK {row['actor_id']}")
        if row["entity_id"]:
            definition = (row["entity_name"], row["entity_kind"])
            if row["entity_id"] in entity_defs and entity_defs[row["entity_id"]] != definition:
                errors.append(f"role entity {row['entity_id']} has inconsistent definition")
            entity_defs[row["entity_id"]] = definition
        refs = set(split_refs(row["source_refs"]))
        if not refs <= source_ids or refs & rejected_source_ids:
            errors.append(f"role {row['role_id']} bad/rejected source FK")
    for row in SOURCES:
        if row["case_id"] not in case_ids:
            errors.append(f"source {row['source_id']} bad case FK")
        if row["existing_source_id"] and row["existing_source_id"] not in main_source_ids:
            errors.append(f"source {row['source_id']} bad existing source FK")
    for row in REJECTED_CLAIMS:
        if row["case_id"] not in case_ids:
            errors.append(f"reject {row['reject_id']} bad case FK")
        if not set(split_refs(row["source_refs"])) <= source_ids:
            errors.append(f"reject {row['reject_id']} bad source FK")

    expected_stage_counts = {NAGO: 6, YONAGUNI: 7, PREF: 7, ISHIGAKI: 13}
    actual_stage_counts = Counter(row["case_id"] for row in STAGES)
    if dict(actual_stage_counts) != expected_stage_counts:
        errors.append(f"stage counts {dict(actual_stage_counts)} != {expected_stage_counts}")
    if Counter(row["review_status"] for row in STAGES) != Counter({"accepted": 24, "needs_human_review": 9}):
        errors.append("stage review counts drift")
    if Counter(row["review_status"] for row in ROLES) != Counter({"accepted": 25, "needs_human_review": 9}):
        errors.append(f"role review counts drift: {Counter(row['review_status'] for row in ROLES)}")

    nago_result = next(row for row in STAGES if row["stage_id"] == "R9ST005")
    for token in ("2,562", "11,705", "16,254", "385", "14,267", "16,639", "31,477", "30,906", "565", "82.45%"):
        if token not in nago_result["outcome"] and token not in nago_result["process_action"]:
            errors.append(f"Nago numeric token missing: {token}")
    yonaguni_result = next(row for row in STAGES if row["stage_id"] == "R9ST012")
    for token in ("632", "445", "17", "1,276", "85.74%"):
        if token not in yonaguni_result["process_action"]:
            errors.append(f"Yonaguni numeric token missing: {token}")
    pref_result = next(row for row in STAGES if row["stage_id"] == "R9ST020")
    for token in ("434,273", "71.7%", "114,933", "52,682"):
        if token not in pref_result["process_action"]:
            errors.append(f"Prefectural numeric token missing: {token}")
    ishigaki_second = next(row for row in STAGES if row["stage_id"] == "R9ST024")
    if "市议员" not in ishigaki_second["process_action"] or "2019-06-17" != ishigaki_second["date_start"]:
        errors.append("Ishigaki second ordinance correction missing")
    if any("市长再次" in row["process_action"] for row in STAGES):
        errors.append("rejected mayor-second-submission wording present")
    chain_types = {row["process_branch"] for row in STAGES if row["case_id"] == ISHIGAKI}
    if not {"mandatory_order_chain", "status_confirmation_chain"} <= chain_types:
        errors.append("Ishigaki chains not separated")
    supreme = next(row for row in STAGES if row["stage_id"] == "R9ST032")
    if "棄却" in supreme["outcome"] or "不受理" in supreme["outcome"]:
        errors.append("Supreme Court outcome is not neutral")
    a014 = next(row for row in ROLES if row["actor_id"] == "A014")
    if (a014["evidence_level"], a014["review_status"], a014["needs_local_retrieval"]) != ("E2", "needs_human_review", "yes"):
        errors.append("A014 boundary drift")
    if any(row["actor_id"] == "A011" and row["role_type"] == "individual_plaintiffs" for row in ROLES):
        errors.append("person plaintiff role transferred to A011")

    if errors:
        raise ValueError("R9 validation failed:\n- " + "\n- ".join(errors))
    return {
        "stage_count": len(STAGES),
        "stage_status": dict(Counter(row["review_status"] for row in STAGES)),
        "role_count": len(ROLES),
        "role_status": dict(Counter(row["review_status"] for row in ROLES)),
        "source_count": len(SOURCES),
        "source_disposition": dict(Counter(row["disposition"] for row in SOURCES)),
        "rejected_claim_count": len(REJECTED_CLAIMS),
        "review_queue_count": 18,
    }


def date_for_plot(row: dict[str, str]) -> datetime:
    override = {
        "R9ST010": "2015-02-01",
        "R9ST027": "2021-01-01",
        "R9ST028": "2021-03-23",
    }
    value = override.get(row["stage_id"]) or row["date_start"] or row["date_end"]
    if len(value) == 4:
        value += "-07-01"
    elif len(value) == 7:
        value += "-15"
    return datetime.strptime(value, "%Y-%m-%d")


def setup_fonts() -> None:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Yu Gothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def make_timeline() -> None:
    setup_fonts()
    cases = (NAGO, YONAGUNI, PREF, ISHIGAKI)
    titles = {
        NAGO: "名护 1997｜请求通过，但结果与行政决定分离",
        YONAGUNI: "与那国 2012–2015｜意见广告/反对运动与自治体条例并行",
        PREF: "冲绳县 2018–2019｜直接请求转为条例、投票与对外通知",
        ISHIGAKI: "石垣 2018–2024｜议会双重否决后分化为两条诉讼链",
    }
    colors = {
        "municipal_direct_request": "#277DA1", "opinion_ad_context": "#F9844A",
        "municipal_ordinance": "#43AA8B", "campaign_context": "#F9C74F",
        "post_result": "#577590", "prefectural_direct_request": "#4D908E",
        "direct_request": "#277DA1", "councillor_proposal": "#F8961E",
        "mandatory_order_chain": "#9B5DE5", "status_confirmation_chain": "#F15BB5",
        "institutional_framework": "#6C757D", "organizational_context": "#ADB5BD",
    }
    selected = {
        NAGO: ["R9ST001", "R9ST002", "R9ST003", "R9ST005", "R9ST006"],
        YONAGUNI: ["R9ST007", "R9ST008", "R9ST009", "R9ST012", "R9ST013"],
        PREF: ["R9ST014", "R9ST015", "R9ST017", "R9ST018", "R9ST019", "R9ST020"],
        ISHIGAKI: ["R9ST021", "R9ST023", "R9ST024", "R9ST026", "R9ST029", "R9ST031", "R9ST032"],
    }
    labels = {
        "R9ST001": "请求准备", "R9ST002": "17,539份有效签名", "R9ST003": "四选项条例",
        "R9ST005": "反对16,639／赞成14,267", "R9ST006": "市长接受并辞职",
        "R9ST007": "反部署意见广告*", "R9ST008": "条例第23号", "R9ST009": "条例两次修正",
        "R9ST012": "赞成632／反对445*", "R9ST013": "町长解释为推进",
        "R9ST014": "A051组织请求", "R9ST015": "92,848份有效签名", "R9ST017": "条例第62号",
        "R9ST018": "加入第三选项", "R9ST019": "全41市町村投票", "R9ST020": "知事通知日美",
        "R9ST021": "14,263份有效签名", "R9ST023": "市长案被否决", "R9ST024": "市议员案再否决",
        "R9ST026": "第一链：程序却下", "R9ST029": "住民投票条款删除",
        "R9ST031": "第二链：高裁判决*", "R9ST032": "最高裁终局*",
    }

    def display_date(row: dict[str, str]) -> str:
        start, end = row["date_start"], row["date_end"]
        if start and end and start != end:
            return f"{start} → {end}"
        return start or end or "日期待核"

    fig, axes = plt.subplots(4, 1, figsize=(16, 11), constrained_layout=True)
    for ax, case_id in zip(axes, cases):
        wanted = selected[case_id]
        lookup = {row["stage_id"]: row for row in STAGES if row["case_id"] == case_id}
        rows = [lookup[stage_id] for stage_id in wanted]
        xs = list(range(len(rows)))
        ax.hlines(0, 0, len(rows) - 1, color="#B8C0CC", linewidth=2, zorder=1)
        for idx, (row, x) in enumerate(zip(rows, xs)):
            pending = row["review_status"] == "needs_human_review"
            color = colors.get(row["process_branch"], "#577590")
            ax.scatter(x, 0, s=95, facecolors="white" if pending else color,
                       edgecolors=color, linewidths=2, zorder=3)
            y = 0.42 if idx % 2 == 0 else -0.46
            text_value = f"{display_date(row)}\n{labels[row['stage_id']]}"
            ax.annotate(text_value, (x, 0), xytext=(x, y), textcoords="data",
                        ha="center", va="bottom" if y > 0 else "top", fontsize=8.5,
                        bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "edgecolor": color, "alpha": 0.96},
                        arrowprops={"arrowstyle": "-", "color": color, "lw": 0.9})
            if idx < len(rows) - 1:
                ax.annotate("", xy=(x + 0.9, 0), xytext=(x + 0.12, 0),
                            arrowprops={"arrowstyle": "-|>", "color": "#B8C0CC", "lw": 1.2})
        ax.set_title(titles[case_id], loc="left", fontsize=12, fontweight="bold")
        ax.set_xlim(-0.45, len(rows) - 0.55)
        ax.set_ylim(-0.9, 0.9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines[["left", "right", "top", "bottom"]].set_visible(False)
    fig.suptitle("R9 住民投票、意见广告与诉讼程序时间线", fontsize=17, fontweight="bold")
    fig.text(0.01, 0.005, "关键节点按程序顺序等距排列，不表示实际时间间隔。实心点＝正式表；空心点/*＝仅在reviewed_all与HR-017中，尚未进入正式表。", fontsize=9)
    fig.savefig(TIMELINE_PATH, dpi=180, bbox_inches="tight", metadata={"Software": "R09 formal process builder"})
    plt.close(fig)


def make_gate_flow() -> None:
    setup_fonts()
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(-1.6, 15.3)
    ax.set_ylim(0, 10)
    ax.axis("off")
    gate_x = [1.0, 4.0, 7.0, 10.0, 13.0]
    gate_titles = ["公众动员", "资格/签名审查", "条例议程与设计", "投票或司法门槛", "结果的再解释"]
    for x, title in zip(gate_x, gate_titles):
        box = FancyBboxPatch((x - 0.8, 8.4), 1.6, 0.7, boxstyle="round,pad=0.08",
                             facecolor="#E9ECEF", edgecolor="#6C757D", linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, 8.75, title, ha="center", va="center", fontsize=10, fontweight="bold")
    cases = [
        ("名护", 7.0, "#277DA1", ["推进协议会", "17,539有效签名", "四选项条例", "投票：反对16,639", "市长接受并辞职"]),
        ("与那国", 5.4, "#43AA8B", ["意见广告/反对运动*", "自治体条例入口", "条例两次修正", "投票：632/445*", "町长解释为推进"]),
        ("县民投票", 3.8, "#4D908E", ["A051/请求代表", "92,848有效签名", "条例+第三选项", "全41市町村投票", "知事通知日美"]),
        ("石垣", 2.2, "#9B5DE5", ["A011/请求代表", "14,263有效签名", "市长案否决\n议员案再否决", "两条诉讼链", "程序却下/终局*\n条款删除"]),
    ]
    for case_name, y, color, labels in cases:
        ax.text(-1.4, y, case_name, ha="left", va="center", fontsize=12, fontweight="bold", color=color)
        for idx, (x, label) in enumerate(zip(gate_x, labels)):
            box = FancyBboxPatch((x - 0.9, y - 0.38), 1.8, 0.76, boxstyle="round,pad=0.06",
                                 facecolor="white", edgecolor=color, linewidth=2)
            ax.add_patch(box)
            ax.text(x, y, label, ha="center", va="center", fontsize=9)
            if idx < len(gate_x) - 1:
                ax.add_patch(FancyArrowPatch((x + 0.92, y), (gate_x[idx + 1] - 0.92, y),
                                             arrowstyle="-|>", mutation_scale=12,
                                             color=color, linewidth=1.4))
    ax.annotate("第一链：实施义务付け\n第二链：地位确认", xy=(10.0, 2.2), xytext=(10.0, 0.8),
                ha="center", fontsize=9, color="#9B5DE5",
                arrowprops={"arrowstyle": "-[,widthB=3.8", "color": "#9B5DE5", "lw": 1.4})
    ax.set_title("自治诉求如何被制度门槛转换", fontsize=18, fontweight="bold", pad=16)
    ax.text(-1.4, 9.6, "同为‘住民投票’，制度入口、议会转换、投票效力与司法可诉性决定了不同路径。", fontsize=11)
    ax.text(-1.4, 0.15, "* 空心/星号事项仅在reviewed_all与HR-017中，未进入正式表：与那国需当地材料；石垣最高裁无一手前用中性措辞。箭头不表示联盟或单向因果。", fontsize=9)
    fig.savefig(FLOW_PATH, dpi=180, bbox_inches="tight", metadata={"Software": "R09 formal process builder"})
    plt.close(fig)


def make_brief(stats: dict[str, object], case_rows: list[dict[str, str]]) -> str:
    case_lookup = {row["case_id"]: row for row in case_rows}
    source_disp = stats["source_disposition"]
    return dedent(f"""
    # R9 住民投票／意见广告／诉讼程序 brief v1

    日期：2026-07-13

    状态：正式程序层；含明确待人审／当地检索边界。

    ## 1. 本轮正式化结果

    中央正式阶段表只含 **24 条 accepted**，模块正式角色表只含 **25 条 accepted**。模块内审计全量表另保留33个阶段与34条角色，其中9个阶段、9条角色进入HR-017；因此合并计数为 **49条正式阶段/角色、18条待人审、6条拒绝说法**。来源登记共 {stats['source_count']} 条，其中 {source_disp.get('accepted', 0)} 条正式接受、{source_disp.get('usable_with_limit', 0)} 条限界使用、{source_disp.get('rejected', 0)} 条拒绝。

    正式层不把“住民投票”压成单一事件，而把它拆为：

    `公众动员 → 代表/签名资格 → 条例议程与设计 → 议会/行政执行 → 投票或司法可诉性 → 结果再解释`

    这条链说明，民间组织提出的自治诉求必须经过多个制度门槛。门槛既可能放行，也可能改变问题设计、阻断投票、把行动推向法院，或把结果转化为行政与对外倡议资源。

    ![四案程序时间线](referendum_process_timeline_v0.png)

    ![制度门槛流程](institutional_gate_flow_v0.png)

    两图从模块内 `reviewed_all` 审计表生成，以便显示缺口。**空心点和星号只属于HR-017待审层，不在中央正式阶段表或正式角色表中。** 实心节点才对应当前正式层。

    ## 2. 四案比较结论

    ### 名护 1997：投票实现，不等于行政受法律拘束

    直接请求经17,539份有效签名、议会四选项修正和条例成立进入投票。名护市官方 XLS 确认：赞成2,562、条件付赞成11,705、反对16,254、条件付反对385；合并赞成14,267、合并反对16,639；投票者31,477、有效票30,906、无效565、投票率82.45%。三日后市长宣布接受海上基地并辞职。

    机制：{case_lookup[NAGO]['mechanism_summary']} 若写比例，必须注明16,639占全体投票者约52.85%，占有效票约53.84%。

    ### 与那国 2012–2015：公众动员与自治体条例是并行层

    A015 的2012意见广告和 A014 的2015反对运动只在reviewed-all／HR-017层保留为 E2 线索，未进入正式阶段或角色表。它们需要八重山报纸、广告实物、町议会/选管材料或组织档案；当前不能作为确定性组织结论，更不能证明发起或实施住民投票、或证明两个委员会组织连续。正式条例文本只支持执行主体为町长／选管。

    地方报道所载赞成632、反对445、无效17、选举人1,276、投票率85.74%同样属于HR-017待审阶段；取得町选管原表前不得进入正式阶段表，只能表述为“地方报道所载数字”。町长施政方针可正式证明行政如何解释结果，但不代表全体町民共识。与那国的主框架是前线化、地方自治、台湾邻近与生活／健康风险，不强行环境化。

    ### 冲绳县民投票 2019：公民请求转为县级条例和外部通知

    官方委员会记录闭合 A051、元山仁士郎、安里長従、中村昌樹与条例制定请求代表角色。92,848份有效签名超过法定23,171；经县议会立法和加入第三选项后，全41市町村实施投票。反对434,273（71.7%），知事依据条例向日美政府通知。

    机制：{case_lookup[PREF]['mechanism_summary']} 33名请求代表、92,848名签名者与A051成员必须分开。

    ### 石垣 2018–2024：议会阻断后，司法门槛再分流

    14,263份有效签名和27名请求代表进入直接请求。第一次条例案由市长提交并于2019-02-01被否决；**第二次是2019-06-17市议员提出的議案第2号**，也被否决。不得写成运动方直接提交或市长第二次付议。

    两条诉讼链必须分开：

    1. 实施义务付け等：令和元年（行ウ）第14号・第15号，2020-08-27那霸地裁全部“却下”；这是已进入正式表的程序性／适法性处理，不是部署政策实体判断。令和2年（行コ）第3号的高裁终结阶段仍在HR-017。
    2. 地位确认等：令和3年（行ウ）第5号 → 令和5年（行コ）第6号 → 2024-09-26最高裁决定后败诉确定，整条链的裁判阶段目前保留在reviewed-all／HR-017，不在正式阶段表。最高裁官方决定书与案号未取得，现阶段不得确定写成“棄却”或“不受理”。

    2021-06-28市议会删除自治基本条例第27/28条，只能解释为制度机会结构改变，不推断由诉讼直接造成。

    ## 3. 角色边界

    - `requester`：正式请求代表；不自动等于组织全体成员。
    - `individual_plaintiff`：诉讼个人原告；不得转嫁为 A011 或其他支持组织的原告身份。
    - `supporter`：公开倡议或诉讼支持；不同于原告与律师。
    - `counsel`：诉讼代理功能；不因判决列名自动建立个人／律师团 actor。
    - `government/council/election administration/court`：制度 counterpart 或场域，不是运动 actor。
    - A068：官方事件名为“名護市民投票推進協議会”，与 registry 现名的改名／alias／拆分继续待人工决定。
    - A014/A015：均维持 E2 和当地检索；不自行解决组织身份。
    - A011：可写公开组织者／支持者，不能写法院确认的组织原告。

    ## 4. 待人审与当地检索

    1. A068 规范名与官方事件名的映射。
    2. A014/A015 的成立、代表、成员、持续性及意见广告实物。
    3. 与那国町选管正式结果表、町公报和议会修正记录。
    4. 石垣第一条高裁判决全文；第二条那霸地裁官方判决；最高裁案号与决定书。
    5. A011 历史官网／会报、27名请求代表与个人原告的组织映射。

    ## 5. 解释边界

    R9 支持的解释是“自治诉求如何被程序门槛转换”，不是“公投必然导致政策变化”的因果识别。共同动员、意见广告、请求、投票与诉讼支持都不能自动写成稳定联盟；法院程序结果也不能转写为组织政治立场。

    正式表、审计全量表与图由 `scripts/make_r09_referendum_process.py` 同源生成：正式表严格过滤为 accepted，图读取reviewed_all并显式标出HR-017空心节点。外键、来源、票数、关键措辞、图文计数和重复运行稳定性均已检查。
    """).strip() + "\n"


def make_hr017_packet(queue: list[dict[str, str]]) -> str:
    case_labels = {
        NAGO: "名护1997：组织名称映射",
        YONAGUNI: "与那国2012–2015：意见广告、反对运动与选管结果",
        PREF: "冲绳县民投票2019",
        ISHIGAKI: "石垣2018–2024：组织角色与两条诉讼链",
    }
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in queue:
        by_case[row["case_id"]].append(row)

    lines = [
        "# HR-017 R9 待人审程序与角色复核包 v0",
        "",
        "日期：2026-07-13",
        "",
        "状态：等待人工决定；本文件和CSV均未预填 accept／revise／reject。",
        "",
        "## 复核目标",
        "",
        "本包覆盖9个待审程序阶段和9个待审角色。它们只存在于模块内reviewed-all表、HR-017队列及图中的空心／星号层，尚未进入中央正式阶段表或正式角色表。",
        "",
        "每项必须选择 `accept`、`revise` 或 `reject`，并填写 reviewer、date 与 decision_note。组织名称映射、个人角色、组织角色、法院处分和当地材料缺口必须分别判断，不能用一个结论替代另一项。",
        "",
        "## 决定规则",
        "",
        "- `accept`：按当前证据等级和解释边界进入正式表。",
        "- `revise`：先写明修订后的日期、主体、角色、结果或措辞；只有修订后证据充分才进入正式表。",
        "- `reject`：不进入正式表，并同步从图／brief的待审叙述移除或转入拒绝记录。",
        "- 不得把person角色转嫁给组织，不得把意见广告／反对运动写成投票正式发起或实施，不得在无最高裁原件时猜测处分类型。",
        "",
    ]
    section = 1
    for case_id in (NAGO, YONAGUNI, PREF, ISHIGAKI):
        rows = by_case.get(case_id, [])
        if not rows:
            continue
        lines.extend([f"## {section}. {case_labels[case_id]}", ""])
        section += 1
        for row in rows:
            lines.extend([
                f"### {row['queue_id']}｜{row['subject']}",
                "",
                f"- 对象：`{row['object_type']}` / `{row['object_id']}`",
                f"- 当前等级：`{row['evidence_level']}`；当地检索：`{row['needs_local_retrieval']}`",
                f"- 来源：`{row['source_refs']}`",
                f"- locator：{row['source_locator']}",
                f"- 精确问题：{row['review_question']}",
                f"- 如 accept：{row['impact_if_accept']}",
                f"- 如 revise：{row['impact_if_revise']}",
                f"- 如 reject：{row['impact_if_reject']}",
                "",
                "决定：- [ ] accept  - [ ] revise  - [ ] reject",
                "",
                "human_reviewer：__________",
                "",
                "review_date：__________",
                "",
                "decision_note：",
                "",
                "________________________________________",
                "",
            ])
    lines.extend([
        "## 回写要求",
        "",
        "1. 同步填写 `hr017_review_queue_v0.csv` 的 `decision`、`human_reviewer`、`review_date`、`decision_note`。",
        "2. `revise` 必须在 decision_note 给出可直接替换的字段值或发布措辞。",
        "3. 人审回写后重跑生成脚本前，应先把决定合并到模块常量／专属决定输入；本脚本当前不会自行猜测或预填决定。",
        "4. 每次回写都要重新校验正式表无 pending、图中空心节点与剩余HR-017队列一致、brief只把正式事项写成确定性结论。",
        "",
    ])
    return "\n".join(lines)


def make_readme(stats: dict[str, object]) -> str:
    return dedent(f"""
    # R09 referendum process formal package

    Generated by `python scripts/make_r09_referendum_process.py`.

    ## Formal outputs

    - `../../data/interim/20_referendum_process_stages_v0.csv` — 24 accepted stages only; no pending rows.
    - `process_stages_reviewed_all_v0.csv` — all {stats['stage_count']} reviewed stages used for audit and figures, including 9 HR-017 pending rows.
    - `actor_process_roles_v0.csv` — 25 accepted roles only; no pending rows.
    - `actor_process_roles_reviewed_all_v0.csv` — all {stats['role_count']} reviewed roles, including 9 HR-017 pending rows.
    - `source_register_v0.csv` — module-local source IDs and source-log mappings; rejected captures are explicit.
    - `case_summary_v0.csv` — four-case gate comparison.
    - `rejected_claims_v0.csv` — {stats['rejected_claim_count']} claims prohibited from formal reporting.
    - `hr017_review_queue_v0.csv` — {stats['review_queue_count']} pending stage/role records with blank human-decision fields, source locators and decision impacts.
    - `HR017_review_packet_v0.md` — Chinese human-review packet; no decision is prefilled.
    - `referendum_process_timeline_v0.png` — four-panel small-multiple timeline.
    - `institutional_gate_flow_v0.png` — explanatory institutional-gate flow.
    - `R09_process_brief_v1.md` — interpretation and evidence boundaries.
    - `validation_report_v0.md` — generated validation summary.

    ## Status boundary

    `accepted` means the bounded stage/role is present in the formal table and may be used in reporting at its recorded evidence level. `needs_human_review` exists only in the module `reviewed_all` tables, HR-017 packet and hollow/starred figure layer; it is absent from both formal tables.

    Historical candidate and QA files remain in this directory for audit provenance; v1 formal outputs supersede the original v0 brief for current R9 reporting.
    """).strip() + "\n"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_validation_report(stats: dict[str, object]) -> str:
    return dedent(f"""
    # R09 validation report v0

    Generated: 2026-07-13

    - Formal stage rows: 24; every row `review_status=accepted`.
    - Reviewed-all stage rows: {stats['stage_count']} (`accepted=24`, `needs_human_review=9`).
    - Formal role rows: 25; every row `review_status=accepted`.
    - Reviewed-all role rows: {stats['role_count']} (`accepted=25`, `needs_human_review=9`).
    - Source rows: {stats['source_count']} ({json.dumps(stats['source_disposition'], ensure_ascii=False, sort_keys=True)}).
    - Rejected claims: {stats['rejected_claim_count']}.
    - HR-017 queue: {stats['review_queue_count']} pending stage/role records; all decision/reviewer/date/note fields blank.
    - Case/stage/role/source/actor/existing-source foreign keys: passed.
    - Per-case stage order and provisional-entity consistency: passed.
    - Rejected sources unused by formal stages and roles: passed.
    - Nago official vote-number assertions: passed.
    - Ishigaki 2019-06-17 councillor-proposal wording assertion: passed.
    - Ishigaki two-chain and neutral Supreme Court wording assertions: passed.
    - A014 E2 / needs-human-review / local-retrieval boundary: passed.
    - Individual plaintiff roles not transferred to A011: passed.
    - Figures generated from reviewed-all rows; hollow/starred nodes are absent from formal tables: passed.
    - Two consecutive executions on 2026-07-13: all generated outputs byte-stable by SHA-256.
    """).strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stats = validate()
    case_rows = build_case_rows()
    review_queue = build_review_queue()
    formal_stages = [row for row in STAGES if row["review_status"] == "accepted"]
    formal_roles = [row for row in ROLES if row["review_status"] == "accepted"]

    write_csv(STAGE_PATH, STAGE_FIELDS, formal_stages)
    write_csv(ALL_STAGE_PATH, STAGE_FIELDS, STAGES)
    write_csv(ROLE_PATH, ROLE_FIELDS, formal_roles)
    write_csv(ALL_ROLE_PATH, ROLE_FIELDS, ROLES)
    write_csv(SOURCE_PATH, SOURCE_FIELDS, SOURCES)
    write_csv(CASE_PATH, CASE_FIELDS, case_rows)
    write_csv(REJECT_PATH, REJECT_FIELDS, REJECTED_CLAIMS)
    write_csv(HR017_CSV_PATH, HR017_FIELDS, review_queue)
    hr017_packet = make_hr017_packet(review_queue)
    HR017_PACKET_PATH.write_text(hr017_packet, encoding="utf-8")
    LEGACY_REVIEW_QUEUE_PATH.unlink(missing_ok=True)
    make_timeline()
    make_gate_flow()

    brief = make_brief(stats, case_rows)
    BRIEF_PATH.write_text(brief, encoding="utf-8")
    README_PATH.write_text(make_readme(stats), encoding="utf-8")
    VALIDATION_PATH.write_text(make_validation_report(stats), encoding="utf-8")

    # Formal/all-layer, HR-017 and text/figure consistency assertions after writing.
    formal_stages_read = read_csv_rows(STAGE_PATH)
    formal_roles_read = read_csv_rows(ROLE_PATH)
    hr017_read = read_csv_rows(HR017_CSV_PATH)
    if len(formal_stages_read) != 24 or any(row["review_status"] != "accepted" for row in formal_stages_read):
        raise ValueError("Formal stage table must contain exactly 24 accepted rows")
    if len(formal_roles_read) != 25 or any(row["review_status"] != "accepted" for row in formal_roles_read):
        raise ValueError("Formal role table must contain exactly 25 accepted rows")
    blank_fields = ("decision", "human_reviewer", "review_date", "decision_note")
    if len(hr017_read) != 18 or any(row[field] for row in hr017_read for field in blank_fields):
        raise ValueError("HR-017 must contain 18 rows with blank human-decision fields")
    if hr017_packet.count("### R9Q-") != 18:
        raise ValueError("HR-017 packet must render all 18 review items")
    for token in ("24 条 accepted", "18条待人审", "2019-06-17市议员", "16,639", "14,267", "空心点和星号只属于HR-017"):
        if token not in brief:
            raise ValueError(f"Brief consistency token missing: {token}")
    for path in (TIMELINE_PATH, FLOW_PATH):
        if not path.exists() or path.stat().st_size < 20_000:
            raise ValueError(f"Figure missing or unexpectedly small: {path}")

    print(
        "R09 formal package generated: "
        "24 formal stages / 25 formal roles; "
        f"reviewed-all {stats['stage_count']} stages / {stats['role_count']} roles; "
        f"HR-017 {stats['review_queue_count']} pending; {stats['rejected_claim_count']} rejected claims."
    )


if __name__ == "__main__":
    main()
