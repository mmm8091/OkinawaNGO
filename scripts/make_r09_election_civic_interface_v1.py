"""Build the R9 election-civic interface candidate package (NW2-B).

The package is deliberately separate from the central actor/event/source tables.
Every actor-event role is election-sensitive and therefore remains a machine-
structured candidate routed to HR-026. Existing human decision fields are
preserved by stable review_item_id on every regeneration.
Candidate people and political parties are event/institutional nodes only.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R09_election_civic_interface_v1"

EVENT_PATH = DATA / "33_r09_election_civic_events_v1.csv"
WINDOW_PATH = OUT / "three_election_windows_v1.csv"
MODE_PATH = OUT / "intervention_mode_counts_v1.csv"
SOURCE_PATH = OUT / "source_proposals_v1.csv"
HR_PATH = OUT / "HR026_election_civic_role_review_v0.csv"
GAP_PATH = OUT / "online_gap_register_v1.csv"
BRIEF_PATH = OUT / "R09_election_civic_interface_brief_v1.md"
README_PATH = OUT / "README.md"
VALIDATION_PATH = OUT / "validation_report_v1.md"
FIG_MODE_PNG = OUT / "fig_r09_intervention_modes_v1.png"
FIG_MODE_SVG = OUT / "fig_r09_intervention_modes_v1.svg"
FIG_MECH_PNG = OUT / "fig_r09_noncausal_mechanism_v1.png"
FIG_MECH_SVG = OUT / "fig_r09_noncausal_mechanism_v1.svg"


EVENT_FIELDS = [
    "record_id", "election_id", "election_year", "election_name",
    "window_phase", "event_date_start", "event_date_end", "date_precision",
    "actor_name", "registry_crosswalk", "entity_boundary", "actor_scope",
    "action_type", "channel", "role_label", "event_name", "place_or_medium",
    "target_node_type", "target_node_name", "issue_focus", "observable_action",
    "evidence_level", "source_proposal_ids", "machine_status", "hr_task_id",
    "interpretation_limit", "notes",
]

SOURCE_FIELDS = [
    "proposal_id", "title", "url", "publisher", "source_type",
    "publication_or_record_date", "locator", "support_scope",
    "suggested_evidence_level", "source_log_state",
    "relation_or_claim_approved", "caveat",
]

HR_FIELDS = [
    "review_item_id", "task_id", "record_id", "election_year", "actor_name",
    "action_type_candidate", "event_name", "source_proposal_ids",
    "review_question", "publishable_if_accept", "required_boundary",
    "decision", "human_reviewer", "review_date", "review_note",
]

HUMAN_FIELDS = ("decision", "human_reviewer", "review_date", "review_note")

WINDOW_FIELDS = [
    "election_id", "election_year", "election_name", "official_vote_date",
    "official_context_source", "candidate_event_rows", "action_types_observed",
    "pre_campaign_rows", "campaign_rows", "post_result_rows", "online_status",
    "online_limit",
]

MODE_FIELDS = ["election_year", "action_type", "candidate_row_count", "status_boundary"]

GAP_FIELDS = [
    "gap_id", "election_year", "object", "missing_detail", "search_status",
    "safe_current_use", "next_route",
]


SOURCES = [
    {
        "proposal_id": "R9EC_S001",
        "title": "平成26年版 選挙管理委員会年報",
        "url": "https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/004/927/h26nenpou.pdf",
        "publisher": "沖縄県選挙管理委員会", "source_type": "official_election_record",
        "publication_or_record_date": "2015-06", "locator": "『沖縄県知事選挙の実績』第12回（告示2014-10-30、投票2014-11-16）",
        "support_scope": "2014 election-window date and official institutional context only",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Does not support any civic-actor role or causal effect.",
    },
    {
        "proposal_id": "R9EC_S002",
        "title": "きちきちニュースレター Vol.6（島ぐるみ会議結成）",
        "url": "https://www.ywca.or.jp/pdf/2014/0716.pdf",
        "publisher": "日本YWCA 基地チーム", "source_type": "organization_newsletter",
        "publication_or_record_date": "2014-07", "locator": "p.1, lines describing 7/27 founding and explicitly stating the body was not directly election-purpose",
        "support_scope": "2014 Shimagurumi founding as issue-campaign window and non-endorsement boundary",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Participant/advocacy publication; exact crosswalk to A059 requires human review.",
    },
    {
        "proposal_id": "R9EC_S003",
        "title": "翁長那覇市長に保革双方が出馬を要請",
        "url": "https://www.qab.co.jp/news/2014082157456.html",
        "publisher": "琉球朝日放送", "source_type": "local_broadcast_news",
        "publication_or_record_date": "2014-08-21", "locator": "Names two women-led request groups and reports their candidate-entry requests",
        "support_scope": "2014 women-group request to Takeshi Onaga to stand",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Does not provide the full member roster of either ad hoc request body.",
    },
    {
        "proposal_id": "R9EC_S004",
        "title": "翁長さんで新基地阻止／女性団体が出馬要請",
        "url": "https://www.jcp.or.jp/akahata/aik14/2014-08-22/2014082204_01_1.html",
        "publisher": "しんぶん赤旗", "source_type": "party_media",
        "publication_or_record_date": "2014-08-22", "locator": "Reports the request body as 52 groups/individuals and names two example networks",
        "support_scope": "2014 women request-body scale/context; second source to QAB",
        "suggested_evidence_level": "E2", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Party-media framing; 52 is not a verified organization roster.",
    },
    {
        "proposal_id": "R9EC_S005",
        "title": "『新基地ノー』心一つ／沖縄知事選 女性29団体が集会",
        "url": "https://www.jcp.or.jp/akahata/aik14/2014-10-11/2014101104_01_1.html",
        "publisher": "しんぶん赤旗", "source_type": "party_media",
        "publication_or_record_date": "2014-10-11", "locator": "Reports 10/9 women assembly organized by the Hiyamikachi Umānchu campaign women's bureau",
        "support_scope": "2014 public endorsement/mobilization meeting",
        "suggested_evidence_level": "E2", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Single party-media report; full 29-group roster is not available online.",
    },
    {
        "proposal_id": "R9EC_S006",
        "title": "『ゆんたく』から始まった、沖縄・若者の抵抗",
        "url": "https://www.magazine9.jp/article/yuntacrew/18975/",
        "publisher": "マガジン9 / ゆんたくるー", "source_type": "participant_account",
        "publication_or_record_date": "2015-04-22", "locator": "Participant describes formation after 2014-08-12 and a pre-gubernatorial-election field-learning bus tour",
        "support_scope": "2014 youth observation/dialogue intervention",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Retrospective first-person account; does not establish turnout or vote effects.",
    },
    {
        "proposal_id": "R9EC_S007",
        "title": "談話：沖縄県知事選で圧勝の民意に応え、ただちに新基地建設中止を",
        "url": "https://www.shinfujin.gr.jp/2943/",
        "publisher": "新日本婦人の会", "source_type": "organization_statement",
        "publication_or_record_date": "2014-11-19", "locator": "Official post-result statement; self-reports Okinawa members' campaign activity",
        "support_scope": "2014 organization public interpretation and bounded self-report",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Organizational self-report is not independent evidence of electoral effect.",
    },
    {
        "proposal_id": "R9EC_S008",
        "title": "平成30年沖縄県知事選挙 特設ページ",
        "url": "https://www.pref.okinawa.jp/kensei/senkyo/1005009/1023802/1021246.html",
        "publisher": "沖縄県選挙管理委員会", "source_type": "official_election_record",
        "publication_or_record_date": "2018-09", "locator": "Official 2018 election administration and 9/30 vote date",
        "support_scope": "2018 election-window date and institutional context only",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Does not support any civic-actor role or causal effect.",
    },
    {
        "proposal_id": "R9EC_S009",
        "title": "『知事、頑張れ』緊急集会で撤回表明に喜びと決意",
        "url": "https://ryukyushimpo.jp/news/entry-770040.html",
        "publisher": "琉球新報", "source_type": "local_news",
        "publication_or_record_date": "2018-07-27", "locator": "Reports All Okinawa Council rally, appeal supporting revocation, and 300+ participants",
        "support_scope": "2018 pre-election issue campaign supporting a gubernatorial administrative act",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Support for a policy act is not a candidate endorsement or vote-effect claim.",
    },
    {
        "proposal_id": "R9EC_S010",
        "title": "8.11県民大会（辺野古新基地建設断念要求）",
        "url": "https://all-okinawa.jp/492/",
        "publisher": "辺野古新基地を造らせないオール沖縄会議", "source_type": "organization_event_record",
        "publication_or_record_date": "2018-08-11", "locator": "Official event page and linked reports after Onaga's death",
        "support_scope": "2018 issue campaign and memorial rally; no candidate endorsement coded",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Election proximity does not convert the rally into an endorsement without explicit evidence.",
    },
    {
        "proposal_id": "R9EC_S011",
        "title": "沖縄県知事選 出遅れ危機感『結束優先』 玉城氏、出馬要請受諾",
        "url": "https://ryukyushimpo.jp/news/entry-789039.html",
        "publisher": "琉球新報", "source_type": "local_news",
        "publication_or_record_date": "2018-08-24", "locator": "Reports 8/23 request by the adjustment council composed of assembly caucuses, parties, unions and firms",
        "support_scope": "2018 candidate-selection request by a temporary mixed coalition",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "The temporary council is an event node, not an NGO or stable alliance.",
    },
    {
        "proposal_id": "R9EC_S012",
        "title": "主体的な主権者教育を育むための一考察―#みんなごと実践記録",
        "url": "https://www.jstage.jst.go.jp/article/isvsjapan/19/0/19_45/_pdf/-char/en",
        "publisher": "国際ボランティア学会 / 玉城直美", "source_type": "academic_participant_record",
        "publication_or_record_date": "2019", "locator": "pp.4-5 activity table: 9/5 debate, 9/13 workshop, 9/19 publication; p.7 identifies an informal eight-student group",
        "support_scope": "2018 nonpartisan civic-learning, public-meeting, policy-proposal and observation windows",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "First-party academic record; candidates are kept as generic event nodes as the paper masks names.",
    },
    {
        "proposal_id": "R9EC_S013",
        "title": "声明：沖縄県知事選挙で歴史的勝利！新基地建設はただちに中止を",
        "url": "https://www.shinfujin.gr.jp/wp-content/uploads/2018/11/20181003_seimei_okinawatidisen.pdf",
        "publisher": "新日本婦人の会", "source_type": "organization_statement",
        "publication_or_record_date": "2018-10-03", "locator": "Official statement, lines 13-16 self-report organization-wide activity for Tamaki",
        "support_scope": "2018 post-result public interpretation and bounded self-report",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Does not independently prove participation scale or effect on votes.",
    },
    {
        "proposal_id": "R9EC_S014",
        "title": "令和4年沖縄県知事選挙 特設ページ",
        "url": "https://www.pref.okinawa.jp/kensei/senkyo/1005009/1023802/1025046/index.html",
        "publisher": "沖縄県選挙管理委員会", "source_type": "official_election_record",
        "publication_or_record_date": "2022-09", "locator": "Official election administration, final records and 9/11 vote date",
        "support_scope": "2022 election-window date and institutional context only",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Does not support any civic-actor role or causal effect.",
    },
    {
        "proposal_id": "R9EC_S015",
        "title": "沖縄県知事選、女性団体有志が玉城氏に出馬要請",
        "url": "https://ryukyushimpo.jp/news/entry-1499534.html",
        "publisher": "琉球新報", "source_type": "local_news",
        "publication_or_record_date": "2022-04-10", "locator": "Reports 4/9 gathering and first public request to incumbent Tamaki to stand",
        "support_scope": "2022 women-led candidate-entry request",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Ad hoc body; membership and continuity are not inferred.",
    },
    {
        "proposal_id": "R9EC_S016",
        "title": "全国の連帯で平和な沖縄―沖縄県知事選集会ひらく",
        "url": "https://www.min-iren.gr.jp/news-press/shinbun/20220816_46093.html",
        "publisher": "全日本民主医療機関連合会", "source_type": "organization_event_report",
        "publication_or_record_date": "2022-08-16", "locator": "Reports 7/29 online support gathering, 436 access points, and explicit re-election call",
        "support_scope": "2022 mainland/medical-network endorsement meeting",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Self-reported attendance/access; does not prove voter reach or effect.",
    },
    {
        "proposal_id": "R9EC_S017",
        "title": "7月30日オンライン配信『復帰50年！新たな基地負担を許さない県民大会』",
        "url": "https://all-okinawa.jp/2005/",
        "publisher": "辺野古新基地を造らせないオール沖縄会議", "source_type": "organization_event_record",
        "publication_or_record_date": "2022-07-30", "locator": "Official event page, speakers and issue statements",
        "support_scope": "2022 election-adjacent issue campaign",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Organizer framing is issue campaign; classification remains HR-026 because election framing was disputed.",
    },
    {
        "proposal_id": "R9EC_S018",
        "title": "『知事選を前にいい発信』与野党の受け止め",
        "url": "https://www.okinawatimes.co.jp/articles/-/1000372",
        "publisher": "沖縄タイムス", "source_type": "local_news",
        "publication_or_record_date": "2022-07-31", "locator": "Contrasting political interpretations of the 7/30 online event",
        "support_scope": "Classification dispute for 2022 All Okinawa issue event",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Quoted partisan interpretations are observations, not adjudicated event purpose.",
    },
    {
        "proposal_id": "R9EC_S019",
        "title": "沖縄県知事選挙―二度と戦場にしない平和で誇りある豊かな沖縄を",
        "url": "https://www.shinfujin.gr.jp/up/newspaper/12908/",
        "publisher": "新日本婦人の会", "source_type": "organization_campaign_statement",
        "publication_or_record_date": "2022-08-01", "locator": "Official page explicitly calls for Tamaki re-election and nationwide support",
        "support_scope": "2022 organization endorsement/campaign call",
        "suggested_evidence_level": "E4", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Endorsement is observable; audience reach and electoral effect are not.",
    },
    {
        "proposal_id": "R9EC_S020",
        "title": "候補者アンケートを基に沖縄知事選の争点考える",
        "url": "https://ryukyushimpo.jp/news/entry-1579341.html",
        "publisher": "琉球新報", "source_type": "local_news",
        "publication_or_record_date": "2022-09-07", "locator": "Reports August 26-theme/74-question survey and 9/8, 9/10 public online talks",
        "support_scope": "2022 multi-issue candidate observation and public deliberation",
        "suggested_evidence_level": "E3", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Named individuals do not transfer roles to their organizations; original response sheet was not located.",
    },
    {
        "proposal_id": "R9EC_S021",
        "title": "優しい県政 デニーさんと／沖縄知事選必勝へ女性集会",
        "url": "https://www.jcp.or.jp/akahata/aik22/2022-08-14/2022081403_01_0.html",
        "publisher": "しんぶん赤旗", "source_type": "party_media",
        "publication_or_record_date": "2022-08-14", "locator": "Reports 8/13 women gathering and explicit support call",
        "support_scope": "2022 women public endorsement meeting",
        "suggested_evidence_level": "E2", "source_log_state": "proposal_only",
        "relation_or_claim_approved": "no", "caveat": "Organizer identity is not named on the available page; no stable coalition inferred.",
    },
]


def event(
    record_id: str, election_year: str, window_phase: str, start: str, end: str,
    precision: str, actor: str, boundary: str, scope: str, action: str,
    channel: str, role: str, name: str, medium: str, target_type: str,
    target_name: str, issues: str, observable: str, evidence: str, sources: str,
    limit: str, notes: str = "", crosswalk: str = "none",
) -> dict[str, str]:
    election_id = f"R9GE{election_year}"
    return {
        "record_id": record_id, "election_id": election_id,
        "election_year": election_year,
        "election_name": f"{election_year} Okinawa gubernatorial election",
        "window_phase": window_phase, "event_date_start": start,
        "event_date_end": end, "date_precision": precision,
        "actor_name": actor, "registry_crosswalk": crosswalk,
        "entity_boundary": boundary, "actor_scope": scope,
        "action_type": action, "channel": channel, "role_label": role,
        "event_name": name, "place_or_medium": medium,
        "target_node_type": target_type, "target_node_name": target_name,
        "issue_focus": issues, "observable_action": observable,
        "evidence_level": evidence, "source_proposal_ids": sources,
        "machine_status": "needs_human_review", "hr_task_id": "HR-026",
        "interpretation_limit": limit, "notes": notes,
    }


EVENTS = [
    event("R9EC001", "2014", "pre_campaign", "2014-07-27", "2014-07-27", "day",
          "沖縄『建白書』を実現し未来を拓く島ぐるみ会議", "provisional_civic_network", "okinawa_local",
          "issue_campaign", "founding_public_assembly", "organizer", "島ぐるみ会議結成大会",
          "宜野湾市民会館", "policy_issue", "建白書／辺野古新基地", "Henoko;anti_base;local_autonomy", "Held a founding assembly to rebuild a long-term anti-base issue platform.",
          "E3", "R9EC_S002", "The source explicitly says the body was not directly election-purpose; do not code endorsement or vote mobilization.",
          "Exact identity relationship with registry A059 remains unresolved.", "possible_A059_requires_review"),
    event("R9EC002", "2014", "pre_campaign", "2014-08-21", "2014-08-21", "day",
          "翁長雄志さんを沖縄県知事に送る女性要請団", "ad_hoc_event_collective", "okinawa_local",
          "request", "candidate_entry_request", "requesting_collective", "女性団体による翁長雄志氏出馬要請",
          "那覇市内", "candidate_person", "翁長雄志", "Henoko;women;local_autonomy", "Publicly requested that Onaga enter the gubernatorial race.",
          "E3", "R9EC_S003;R9EC_S004", "A request to stand is not itself a stable alliance; the reported 52 groups/individuals are not a verified roster."),
    event("R9EC003", "2014", "campaign", "2014-10-09", "2014-10-09", "day",
          "ひやみかち うまんちゅの会 女性局", "candidate_campaign_body", "okinawa_local",
          "endorsement", "women_public_assembly", "endorsement_mobilizer", "女性大集会",
          "那覇市内", "candidate_person", "翁長雄志", "Henoko;women;peace", "Held a women-focused public assembly explicitly calling for the candidate's victory.",
          "E2", "R9EC_S005", "Single party-media source; do not convert 29 participating groups into registry actors or a stable coalition."),
    event("R9EC004", "2014", "pre_campaign", "2014-08-12", "2014-11-15", "bounded_window",
          "ゆんたくるー", "informal_youth_group", "okinawa_local",
          "observation", "field_learning_bus_tour", "youth_civic_learning_organizer", "県知事選前の辺野古・高江フィールド学習バス",
          "辺野古／高江／若者対話", "public_issue_and_election_context", "基地問題と県知事選", "Henoko;Takae;youth_civic_education", "Organized a youth field-learning and peer-dialogue bus activity before the election.",
          "E3", "R9EC_S006", "The dates bound formation and pre-election activity, not an exact tour day; no turnout or vote effect is claimed."),
    event("R9EC005", "2014", "post_result", "2014-11-19", "2014-11-19", "day",
          "新日本婦人の会", "organization_outside_registry", "japan_domestic",
          "observation", "organization_statement", "post_result_interpreter", "県知事選結果に関する談話",
          "organization_website", "election_result_and_government", "2014 election result / Japanese government", "anti_base;post_result_interpretation", "Published an organizational interpretation and self-reported nationwide/Okinawa member activity.",
          "E4", "R9EC_S007", "Self-report supports the statement and claimed participation only; it cannot establish participation scale or causal effect."),

    event("R9EC006", "2018", "pre_campaign", "2018-07-27", "2018-07-27", "day",
          "辺野古新基地を造らせないオール沖縄会議", "mixed_civic_political_network", "okinawa_local",
          "issue_campaign", "emergency_public_rally", "organizer", "埋立承認撤回支持の緊急集会",
          "沖縄県民広場", "incumbent_governor_policy_act", "翁長知事の埋立承認撤回表明", "Henoko;local_autonomy;legal", "Held a rally and adopted an appeal supporting the announced revocation.",
          "E3", "R9EC_S009", "Policy-act support is not coded as candidate endorsement and is not evidence of electoral effect."),
    event("R9EC007", "2018", "pre_campaign", "2018-08-11", "2018-08-11", "day",
          "辺野古新基地を造らせないオール沖縄会議", "mixed_civic_political_network", "okinawa_local",
          "issue_campaign", "prefectural_public_assembly", "organizer", "土砂投入を許さない8.11県民大会",
          "奥武山公園陸上競技場", "national_government_policy", "辺野古土砂投入／新基地建設", "Henoko;anti_base;peace", "Convened an issue rally and memorial after Governor Onaga's death.",
          "E4", "R9EC_S010", "Election proximity does not make this a candidate endorsement; participant counts and political effects are excluded."),
    event("R9EC008", "2018", "pre_campaign", "2018-08-23", "2018-08-23", "day",
          "県政与党等の調整会議", "temporary_mixed_selection_coalition", "mixed",
          "request", "candidate_selection_meeting", "candidate_request_body", "玉城デニー氏への出馬要請",
          "沖縄市／調整会議", "candidate_person", "玉城デニー", "Henoko;governance;candidate_selection", "Selected Tamaki and formally requested that he stand.",
          "E3", "R9EC_S011", "This temporary party-labor-business council is an event node, not an NGO or stable alliance."),
    event("R9EC009", "2018", "pre_campaign", "2018-09-05", "2018-09-05", "day",
          "#みんなごと 若者が考える（沖縄県）知事選", "informal_student_civic_project", "okinawa_local",
          "public_meeting", "candidate_public_debate", "civic_learning_organizer", "県知事候補者2名による公開討論会と振り返り",
          "public_debate / student learning", "candidate_event_nodes", "候補者1／候補者2", "candidate_policy;youth_civic_education", "Observed a two-candidate debate and held a structured post-debate clarification session.",
          "E4", "R9EC_S012", "The source masks candidate names; generic candidate nodes are retained and neutrality is not independently audited."),
    event("R9EC010", "2018", "campaign", "2018-09-13", "2018-09-13", "day",
          "#みんなごと 若者が考える（沖縄県）知事選", "informal_student_civic_project", "okinawa_local",
          "request", "public_policy_workshop", "policy_proposal_drafter", "公開ワークショップ：知事候補者への政策提言案作成",
          "public workshop / newspaper and SNS recruitment", "candidate_event_nodes", "県知事候補者", "youth_policy_agenda;civic_education", "Held a 34-person public workshop to draft policy proposals for candidates.",
          "E4", "R9EC_S012", "Drafting a proposal is coded as a request candidate only; delivery/acceptance by each candidate is not established."),
    event("R9EC011", "2018", "campaign", "2018-09-19", "2018-09-19", "day",
          "#みんなごと 若者が考える（沖縄県）知事選", "informal_student_civic_project", "okinawa_local",
          "observation", "newspaper_policy_comparison", "public_information_producer", "新聞企画：候補者政策比較と政策提言の公開",
          "琉球新報紙面／SNS", "candidate_event_nodes", "県知事候補者", "candidate_policy;youth_civic_education", "Published a comparison of candidate positions and the project's policy proposals.",
          "E4", "R9EC_S012", "Information production is observable; readership, persuasion, turnout and vote effects are not."),
    event("R9EC012", "2018", "post_result", "2018-10-03", "2018-10-03", "day",
          "新日本婦人の会", "organization_outside_registry", "japan_domestic",
          "observation", "organization_statement", "post_result_interpreter", "県知事選結果に関する声明",
          "organization_website / PDF", "election_result_and_government", "2018 election result / Japanese government", "anti_base;post_result_interpretation", "Published a post-result interpretation and self-reported organization-wide support activity.",
          "E4", "R9EC_S013", "Self-report supports only the organization's stated activity; it cannot identify scale or effect."),

    event("R9EC013", "2022", "pre_campaign", "2022-04-09", "2022-04-09", "day",
          "沖縄の輝く未来をつくる女性たちの会", "ad_hoc_event_collective", "okinawa_local",
          "request", "candidate_entry_request_gathering", "requesting_collective", "女性団体有志による玉城知事出馬要請",
          "那覇市教育福祉会館", "candidate_person", "玉城デニー", "Henoko;women;children;governance", "Held a gathering and requested that the incumbent stand for re-election.",
          "E3", "R9EC_S015", "The ad hoc body remains event-only; membership and continuity are not inferred."),
    event("R9EC014", "2022", "pre_campaign", "2022-07-29", "2022-07-29", "day",
          "全日本民主医療機関連合会", "organization_outside_registry", "japan_domestic",
          "endorsement", "national_online_support_meeting", "endorsement_mobilizer", "沖縄県知事選勝利で基地のない平和で誇りある沖縄を",
          "online / 436 reported access points", "candidate_person", "玉城デニー", "Henoko;peace;healthcare_network", "Convened a nationwide online meeting explicitly calling for Tamaki's re-election.",
          "E4", "R9EC_S016", "Reported access points do not equal persons, voters or persuasion; no electoral effect is inferred."),
    event("R9EC015", "2022", "pre_campaign", "2022-07-30", "2022-07-30", "day",
          "辺野古新基地を造らせないオール沖縄会議", "mixed_civic_political_network", "okinawa_local",
          "issue_campaign", "online_prefectural_assembly", "organizer", "復帰50年！新たな基地負担を許さない県民大会",
          "online broadcast", "national_government_policy", "新基地負担／辺野古設計変更", "Henoko;anti_base;local_autonomy", "Convened an online issue meeting on base burden and the design-change dispute.",
          "E4", "R9EC_S017;R9EC_S018", "Organizer framing is issue campaign, while political actors disputed whether it functioned as an election rally; HR-026 must decide wording."),
    event("R9EC016", "2022", "pre_campaign", "2022-08-01", "2022-08-01", "day",
          "新日本婦人の会", "organization_outside_registry", "japan_domestic",
          "endorsement", "organization_campaign_statement", "endorsement_mobilizer", "二度と戦場にしない平和で誇りある豊かな沖縄を",
          "organization website / newspaper", "candidate_person", "玉城デニー", "Henoko;anti_war;welfare;women", "Published an explicit re-election call and requests for nationwide support and diffusion.",
          "E4", "R9EC_S019", "Observable endorsement only; audience reach, compliance and vote effects are not established."),
    event("R9EC017", "2022", "pre_campaign", "2022-08-01", "2022-08-31", "month",
          "『沖縄県知事選2022県民有志からのアンケート』実行委員会", "ad_hoc_event_collective", "okinawa_local",
          "observation", "candidate_questionnaire", "multi_issue_observer", "県知事候補3名への26テーマ74問アンケート",
          "questionnaire / online publication", "candidate_event_nodes", "佐喜真淳／下地幹郎／玉城デニー", "climate;energy;PFAS;sexual_minorities;governance", "Sent a multi-issue questionnaire to all three candidates and used the responses as public information.",
          "E3", "R9EC_S020", "Named individual organizers do not transfer roles to A051 or other organizations; original answer sheet was not located."),
    event("R9EC018", "2022", "campaign", "2022-09-08", "2022-09-10", "day_range",
          "『沖縄県知事選2022県民有志からのアンケート』実行委員会", "ad_hoc_event_collective", "okinawa_local",
          "public_meeting", "online_talk_series", "public_deliberation_organizer", "候補者アンケートを基にしたオンライントーク",
          "online / Punga Ponga (limited in-person seats on 9/10)", "public_and_candidate_positions", "県知事選の争点", "climate;energy;PFAS;sexual_minorities;leadership", "Held two public talks using candidate questionnaire responses to discuss election issues.",
          "E3", "R9EC_S020", "Public discussion is not endorsement; attendance, influence and candidate uptake are not established."),
    event("R9EC019", "2022", "pre_campaign", "2022-08-13", "2022-08-13", "day",
          "女性集会（主催組織名未確認）", "unnamed_event_collective", "okinawa_local",
          "endorsement", "women_hybrid_support_meeting", "endorsement_mobilizer", "沖縄知事選必勝へ女性集会",
          "那覇市内／online", "candidate_person", "玉城デニー", "Henoko;women;welfare;poverty", "Held a women-focused hybrid gathering explicitly calling for Tamaki's re-election.",
          "E2", "R9EC_S021", "Organizer identity is not established; retain as an event collective and do not infer a stable women's alliance."),
]


GAPS = [
    {
        "gap_id": "R9EC_G01", "election_year": "2014",
        "object": "翁長雄志さんを沖縄県知事に送る女性要請団",
        "missing_detail": "Complete list and organization-level continuity for the reported 52 groups/individuals",
        "search_status": "online_exhausted", "safe_current_use": "Use only the named ad hoc request body and two example networks; no member edges.",
        "next_route": "Local newspaper archive, request letter, flyer or campaign archive if member-level analysis becomes figure-critical.",
    },
    {
        "gap_id": "R9EC_G02", "election_year": "2014",
        "object": "ひやみかち うまんちゅの会女性局 29団体集会",
        "missing_detail": "Full 29-group roster and independent organizer record",
        "search_status": "online_exhausted", "safe_current_use": "Use as one E2 endorsement event only; do not create 29 actor rows.",
        "next_route": "Campaign pamphlets, local press databases or political-funds/campaign archive if exact participants are required.",
    },
    {
        "gap_id": "R9EC_G03", "election_year": "2018",
        "object": "#みんなごと candidate-event nodes",
        "missing_detail": "The academic activity table masks the two 9/5 debate participants",
        "search_status": "online_exhausted", "safe_current_use": "Retain generic candidate 1/2 event nodes; do not guess names from election chronology.",
        "next_route": "Original Ryukyu Shimpo 2018 paper edition or project archive only if name-level comparison is needed.",
    },
    {
        "gap_id": "R9EC_G04", "election_year": "2022",
        "object": "県民有志アンケート実行委員会",
        "missing_detail": "Original questionnaire/three complete candidate response sheets and stable archive URL",
        "search_status": "online_exhausted", "safe_current_use": "Use only the reported 26 themes/74 questions and public-talk occurrence; do not quote answers.",
        "next_route": "Organizer archive or local newspaper capture if question-by-question content is needed.",
    },
    {
        "gap_id": "R9EC_G05", "election_year": "2022",
        "object": "8/13 women support gathering",
        "missing_detail": "Formal organizer name and participating organization roster",
        "search_status": "online_exhausted", "safe_current_use": "Retain an unnamed event collective at E2; no registry or alliance inference.",
        "next_route": "Local press archive/event flyer only if organization-level mapping is required.",
    },
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_with_fields(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        return fields, list(reader)


def preserve_human_fields(
    generated_rows: list[dict[str, str]], existing_path: Path,
    generated_fields: list[str], *, identity_field: str,
) -> tuple[list[dict[str, str]], list[str], dict[str, int]]:
    """Overlay human-owned cells from an existing HR file by review_item_id.

    Generated/machine columns are always refreshed. The four standard human
    columns and every pre-existing extra column (for example final_status) are
    retained. A populated orphan row or a stable-ID/identity collision aborts
    rather than silently discarding an adjudication.
    """
    existing_fields, existing_rows = read_csv_with_fields(existing_path)
    extra_fields = [field for field in existing_fields if field not in generated_fields]
    output_fields = list(generated_fields) + extra_fields
    human_fields = list(dict.fromkeys([*HUMAN_FIELDS, *extra_fields]))
    existing_by_id = {row.get("review_item_id", ""): row for row in existing_rows if row.get("review_item_id")}
    generated_ids = {row["review_item_id"] for row in generated_rows}
    if len(existing_by_id) != len([row for row in existing_rows if row.get("review_item_id")]):
        raise ValueError(f"Duplicate review_item_id in {existing_path}")

    preserved_rows = 0
    result: list[dict[str, str]] = []
    for generated in generated_rows:
        row = dict(generated)
        old = existing_by_id.get(row["review_item_id"])
        if old:
            if old.get(identity_field) and old[identity_field] != row[identity_field]:
                raise ValueError(
                    f"Stable review ID collision {row['review_item_id']}: "
                    f"{identity_field} changed from {old[identity_field]} to {row[identity_field]}"
                )
            for field in human_fields:
                row[field] = old.get(field, "")
            if any(row.get(field, "") for field in human_fields):
                preserved_rows += 1
        else:
            for field in extra_fields:
                row[field] = ""
        result.append(row)

    populated_orphans = [
        review_id for review_id, row in existing_by_id.items()
        if review_id not in generated_ids and any(row.get(field, "") for field in human_fields)
    ]
    if populated_orphans:
        raise ValueError(f"Refusing to drop populated retired HR rows: {populated_orphans}")
    return result, output_fields, {
        "existing_rows": len(existing_rows),
        "preserved_nonblank_rows": preserved_rows,
        "extra_human_fields": len(extra_fields),
    }


def human_preservation_self_test(generated_rows: list[dict[str, str]]) -> None:
    """Inject sentinel human values in a temp copy and prove regeneration keeps them."""
    with TemporaryDirectory(prefix="r09_hr026_preservation_") as temp_dir:
        path = Path(temp_dir) / "HR026_test.csv"
        fields = [*HR_FIELDS, "final_status", "final_note"]
        existing = [dict(row) for row in generated_rows]
        for row in existing:
            row["final_status"] = ""
            row["final_note"] = ""
        existing[0].update({
            "decision": "TEST_HUMAN_DECISION",
            "human_reviewer": "TEST_REVIEWER",
            "review_date": "2099-12-31",
            "review_note": "TEST_REVIEW_NOTE",
            "final_status": "TEST_FINAL_STATUS",
            "final_note": "TEST_FINAL_NOTE",
            "review_question": "STALE_MACHINE_TEXT",
        })
        write_csv(path, existing, fields)
        merged, merged_fields, stats = preserve_human_fields(
            [dict(row) for row in generated_rows], path, HR_FIELDS,
            identity_field="record_id",
        )
        assert merged[0]["decision"] == "TEST_HUMAN_DECISION"
        assert merged[0]["human_reviewer"] == "TEST_REVIEWER"
        assert merged[0]["review_date"] == "2099-12-31"
        assert merged[0]["review_note"] == "TEST_REVIEW_NOTE"
        assert merged[0]["final_status"] == "TEST_FINAL_STATUS"
        assert merged[0]["final_note"] == "TEST_FINAL_NOTE"
        assert merged[0]["review_question"] == generated_rows[0]["review_question"]
        assert "final_status" in merged_fields and stats["preserved_nonblank_rows"] == 1


def normalize_svg_trailing_whitespace(path: Path) -> None:
    """Normalize SVG line endings and strip Matplotlib's path-line tail spaces."""
    text = path.read_text(encoding="utf-8")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def build_windows() -> list[dict[str, str]]:
    official = {
        "2014": ("2014-11-16", "R9EC_S001"),
        "2018": ("2018-09-30", "R9EC_S008"),
        "2022": ("2022-09-11", "R9EC_S014"),
    }
    rows = []
    for year in ("2014", "2018", "2022"):
        subset = [row for row in EVENTS if row["election_year"] == year]
        phases = Counter(row["window_phase"] for row in subset)
        modes = ";".join(sorted({row["action_type"] for row in subset}))
        related_gaps = [row for row in GAPS if row["election_year"] == year]
        limit = "; ".join(row["missing_detail"] for row in related_gaps)
        rows.append({
            "election_id": f"R9GE{year}", "election_year": year,
            "election_name": f"{year} Okinawa gubernatorial election",
            "official_vote_date": official[year][0], "official_context_source": official[year][1],
            "candidate_event_rows": str(len(subset)), "action_types_observed": modes,
            "pre_campaign_rows": str(phases["pre_campaign"]),
            "campaign_rows": str(phases["campaign"]),
            "post_result_rows": str(phases["post_result"]),
            "online_status": "minimum_public_window_found",
            "online_limit": limit or "No year-level blocking gap; role claims still require HR-026.",
        })
    return rows


def build_mode_counts() -> list[dict[str, str]]:
    counts = Counter((row["election_year"], row["action_type"]) for row in EVENTS)
    rows = []
    for year in ("2014", "2018", "2022"):
        for action in ("endorsement", "issue_campaign", "public_meeting", "request", "observation"):
            rows.append({
                "election_year": year, "action_type": action,
                "candidate_row_count": str(counts[(year, action)]),
                "status_boundary": "machine-structured candidate; not a human-reviewed finding",
            })
    return rows


def build_hr026(existing_path: Path = HR_PATH) -> list[dict[str, str]]:
    questions = {
        "endorsement": "Does the cited record support explicit candidate endorsement, and is the actor name/entity boundary publishable as written?",
        "issue_campaign": "Should this remain an issue campaign rather than an endorsement, and is the election-adjacent wording sufficiently bounded?",
        "public_meeting": "Does the source support this public-meeting role without implying neutrality, persuasion or candidate uptake beyond the record?",
        "request": "Does the record support a request to the stated target, and is proposal drafting distinguished from delivery/acceptance?",
        "observation": "Does the record support the bounded observation/information role without turning it into endorsement or effect?",
    }
    _, existing_rows = read_csv_with_fields(existing_path)
    existing_by_record: dict[str, str] = {}
    existing_ids = {row["review_item_id"] for row in existing_rows if row.get("review_item_id")}
    for old in existing_rows:
        if not old.get("record_id"):
            continue
        if old["record_id"] in existing_by_record and existing_by_record[old["record_id"]] != old["review_item_id"]:
            raise ValueError(f"Duplicate stable HR-026 record mapping: {old['record_id']}")
        existing_by_record[old["record_id"]] = old["review_item_id"]
    next_number = max(
        [int(match.group(1)) for review_id in existing_ids if (match := re.fullmatch(r"HR026-(\d+)", review_id))],
        default=0,
    ) + 1

    rows = []
    for row in EVENTS:
        review_id = existing_by_record.get(row["record_id"], "")
        if not review_id:
            while f"HR026-{next_number:02d}" in existing_ids:
                next_number += 1
            review_id = f"HR026-{next_number:02d}"
            existing_ids.add(review_id)
            next_number += 1
        rows.append({
            "review_item_id": review_id, "task_id": "HR-026",
            "record_id": row["record_id"], "election_year": row["election_year"],
            "actor_name": row["actor_name"], "action_type_candidate": row["action_type"],
            "event_name": row["event_name"], "source_proposal_ids": row["source_proposal_ids"],
            "review_question": questions[row["action_type"]],
            "publishable_if_accept": row["observable_action"],
            "required_boundary": row["interpretation_limit"],
            "decision": "", "human_reviewer": "", "review_date": "", "review_note": "",
        })
    return rows


def setup_plotting() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "Noto Sans CJK SC", "Noto Sans CJK JP", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": "#F5F1E8",
        "axes.facecolor": "#F5F1E8",
        "savefig.facecolor": "#F5F1E8",
        "svg.hashsalt": "r9-election-civic-v1",
    })


def render_mode_figure(mode_rows: list[dict[str, str]]) -> None:
    setup_plotting()
    actions = ["endorsement", "issue_campaign", "public_meeting", "request", "observation"]
    labels = ["公开支持", "议题行动", "公共讨论", "请求/提案", "观察/信息"]
    colors = ["#C45850", "#2A6F6B", "#D69E2E", "#6B5B95", "#457B9D"]
    years = ["2014", "2018", "2022"]
    lookup = {(r["election_year"], r["action_type"]): int(r["candidate_row_count"]) for r in mode_rows}
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    x = list(range(len(years)))
    bottoms = [0, 0, 0]
    for action, label, color in zip(actions, labels, colors):
        vals = [lookup[(year, action)] for year in years]
        bars = ax.bar(x, vals, bottom=bottoms, width=0.58, label=label, color=color, edgecolor="#F5F1E8")
        for bar, val, bottom in zip(bars, vals, bottoms):
            if val:
                ax.text(bar.get_x() + bar.get_width()/2, bottom + val/2, str(val), ha="center", va="center", color="white", fontsize=11, fontweight="bold")
        bottoms = [a + b for a, b in zip(bottoms, vals)]
    ax.set_xticks(x, ["2014\n翁长竞选窗口", "2018\n继任与议题窗口", "2022\n再选与多议题窗口"])
    ax.set_ylabel("公开可核的 actor-event 候选条数")
    ax.set_title("三届冲绳县知事选：市民组织介入方式（候选层）", fontsize=17, fontweight="bold", loc="left", pad=16)
    ax.text(0, 1.01, "同一组织可以在不同时间承担不同角色；条数不代表影响力、票数或联盟强度。", transform=ax.transAxes, fontsize=10, color="#5F625F")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color="#D4CEC0", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(ncol=3, loc="upper left", bbox_to_anchor=(0, -0.15), frameon=False)
    fig.text(0.02, 0.015, "全部19条均进入 HR-026；重生保留人审字段，但本候选图不自动并表。共同出现不形成稳定联盟。", fontsize=9, color="#7A4D3A")
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(FIG_MODE_PNG, dpi=180, bbox_inches="tight", metadata={"Software": "NW2-B R9 election-civic builder"})
    fig.savefig(FIG_MODE_SVG, bbox_inches="tight", metadata={"Date": "2026-07-13"})
    normalize_svg_trailing_whitespace(FIG_MODE_SVG)
    plt.close(fig)


def render_mechanism_figure() -> None:
    setup_plotting()
    fig, ax = plt.subplots(figsize=(14, 7.2))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    top = [
        (0.5, "长期议题与组织资源", "建白书／边野古\n女性、青年、医疗\nPFAS与生活议题", "#DDE8E4"),
        (3.35, "公开介入方式", "endorsement\nissue campaign\npublic meeting\nrequest / observation", "#E6D9C8"),
        (6.25, "选举公共接口", "候选承诺窗口\n议题可见性\n公共学习与讨论\n组织自我定位", "#D8E3ED"),
        (9.15, "可观察产出", "声明／请求书\n集会／问卷\n政策比较\n公开记录", "#D9E7D2"),
    ]
    for x, title, body, color in top:
        box = FancyBboxPatch((x, 4.7), 2.25, 2.05, boxstyle="round,pad=0.08", facecolor=color, edgecolor="#465752", linewidth=1.3)
        ax.add_patch(box)
        ax.text(x + 1.125, 6.35, title, ha="center", va="center", fontsize=12, fontweight="bold")
        ax.text(x + 1.125, 5.55, body, ha="center", va="center", fontsize=10, linespacing=1.35)
    for x1, x2 in ((2.75, 3.35), (5.6, 6.25), (8.5, 9.15)):
        ax.add_patch(FancyArrowPatch((x1, 5.72), (x2, 5.72), arrowstyle="-|>", mutation_scale=15, linewidth=1.5, color="#465752"))

    barrier = FancyBboxPatch((12.05, 4.55), 1.45, 2.35, boxstyle="round,pad=0.08", facecolor="#F2D6D3", edgecolor="#9B4B45", linewidth=2, linestyle="--")
    ax.add_patch(barrier)
    ax.text(12.78, 6.32, "本资料不能识别", ha="center", va="center", fontsize=11, fontweight="bold", color="#842F2A")
    ax.text(12.78, 5.53, "票数变化\n投票率变化\n胜负原因\n政策因果效果", ha="center", va="center", fontsize=10, color="#842F2A", linespacing=1.35)
    ax.add_patch(FancyArrowPatch((11.4, 5.72), (12.02, 5.72), arrowstyle="-[", mutation_scale=20, linewidth=2, linestyle="--", color="#9B4B45"))

    lower = [
        (0.75, "2014", "议题平台与女性请求\n青年现场观察式参与"),
        (4.25, "2018", "政策行动与候选形成并行\n出现非党派主权者教育"),
        (7.75, "2022", "支持网络持续\n问卷扩展到PFAS/气候/性少数"),
    ]
    for x, year, body in lower:
        box = FancyBboxPatch((x, 1.35), 2.85, 1.55, boxstyle="round,pad=0.08", facecolor="#FFFDF8", edgecolor="#8A8174", linewidth=1.1)
        ax.add_patch(box)
        ax.text(x + 0.2, 2.55, year, ha="left", va="center", fontsize=13, fontweight="bold", color="#2A6F6B")
        ax.text(x + 1.425, 1.95, body, ha="center", va="center", fontsize=10, linespacing=1.35)
    ax.text(0.5, 7.55, "R9 选举—市民组织接口：可解释机制，但不识别选举因果", fontsize=19, fontweight="bold")
    ax.text(0.5, 7.18, "箭头表示资料组织与公共接口顺序，不表示组织行动导致候选得票、胜负或政策结果。", fontsize=11, color="#5F625F")
    ax.text(12.25, 2.05, "候选人与政党\n只作事件/制度节点\n不进入 NGO registry", ha="center", va="center", fontsize=10, color="#6C4B3B",
            bbox={"boxstyle": "round,pad=0.4", "facecolor": "#EFE3D3", "edgecolor": "#A4856C"})
    fig.tight_layout()
    fig.savefig(FIG_MECH_PNG, dpi=180, bbox_inches="tight", metadata={"Software": "NW2-B R9 election-civic builder"})
    fig.savefig(FIG_MECH_SVG, bbox_inches="tight", metadata={"Date": "2026-07-13"})
    normalize_svg_trailing_whitespace(FIG_MECH_SVG)
    plt.close(fig)


def make_brief(
    windows: list[dict[str, str]], modes: list[dict[str, str]],
    hr_rows: list[dict[str, str]],
) -> str:
    counts = Counter(row["action_type"] for row in EVENTS)
    year_counts = Counter(row["election_year"] for row in EVENTS)
    human_fields = set(HUMAN_FIELDS) | {
        field for row in hr_rows for field in row if field not in HR_FIELDS
    }
    decided = sum(any(row.get(field, "") for field in human_fields) for row in hr_rows)
    pending = len(hr_rows) - decided
    return dedent(f"""
    # R9 选举—市民组织接口 brief v1

    日期：2026-07-13

    状态：**候选事实层；HR-026 人工字段按稳定 review item ID 保留。当前已填写 {decided} 条、待处理 {pending} 条。**

    ## 1. 交付与证据边界

    本包为2014、2018、2022三次冲绳县知事选建立 **{len(EVENTS)} 条 actor–event 候选观察**：2014年 {year_counts['2014']} 条、2018年 {year_counts['2018']} 条、2022年 {year_counts['2022']} 条。动作类型严格拆为：`endorsement` {counts['endorsement']}、`issue_campaign` {counts['issue_campaign']}、`public_meeting` {counts['public_meeting']}、`request` {counts['request']}、`observation` {counts['observation']}。

    `source_proposals_v1.csv` 保留本模块生成时的历史 proposal 状态；当前 provisional source ID 以 `outputs/next_wave_source_integration_v1/proposal_to_source_crosswalk_v1.csv` 为权威。来源已进入中央 source log 只建立索引，所有行仍为 `relation_or_claim_approved=no`，没有批准 actor registry 或正式关系。个人候选人、政党、临时选举协调体只作事件／制度节点。

    三届都达到 `minimum_public_window_found`，不存在“整届完全无资料”的阻断。不过，2014两个女性活动的完整组织名单、2018 `#みんなごと` 公开讨论会的具名候选节点、2022问卷原表与8/13女性集会主办名已在线耗尽，详见 `online_gap_register_v1.csv`。

    ![三届组织介入方式](fig_r09_intervention_modes_v1.png)

    ## 2. 三届的解释性比较

    ### 2014：议题平台、出马请求与青年观察式参与并存

    7月的「沖縄『建白書』を実現し未来を拓く島ぐるみ会議」把建白书与长期反基地议题重新组织成公开平台。日本YWCA当时的记录明确说该组织**并非直接为知事选而设**，因此本包只编为 `issue_campaign`，不编为 endorsement。

    8月的女性请求团体向翁长雄志提出出马请求，10月的女性集会则是明确候选支持，两者分别编码为 `request` 与 `endorsement`。`ゆんたくるー` 的现场学习巴士把选举窗口转化为青年观察、同辈对话与基地现场学习，编为 `observation`。这说明“参与选举公共空间”不只有支持候选一种形式。

    ### 2018：政策行动、继任人选形成与非党派学习通道交叠

    翁长知事生前的撤回表明及逝世后的8.11大会，是边野古政策行动／追悼动员，不自动等同于候选支持。随后，由县政与党会派、政党、劳组和企业构成的临时「調整会議」向玉城Denny提出出马请求；该协调体只作为选举事件节点，不能写成稳定NGO联盟。

    同期 `#みんなごと` 组织候选公开讨论、公众政策提案工作坊和报纸政策比较，展示了另一种接口：组织不必支持某一候选，也可以把选举变成主权者教育、问题比较和公共讨论的窗口。其2018活动由参与者撰写的学术记录完整列日，但候选人姓名在表中被隐去，本包不依据时间线猜名。

    ### 2022：支持网络持续，同时议题入口明显扩展

    女性有志团体、全日本民医连和新日本妇人会分别形成出马请求或公开支持窗口。7月30日 All Okinawa线上大会按组织原始页面编为基地负担 `issue_campaign`；由于地方媒体记录了“県民大会还是决起集会”的政治争议，其措辞单独送 HR-026。

    同年，县民有志问卷把候选观察扩展到气候、能源、PFAS、性少数等26主题74问，并以两场公开谈话展开讨论。这个变化支持“选举公共接口的议题范围扩张”这一描述，但不能推断议题改变了投票选择。

    ## 3. 非因果机制

    ![非因果机制](fig_r09_noncausal_mechanism_v1.png)

    可安全讨论的机制是：长期议题与组织资源，通过公开支持、议题行动、公共讨论、请求或观察，进入选举公共接口，并留下声明、请求、集会、问卷与政策比较等**可观察记录**。这叫“议题—制度接口”，不是“组织行动导致选举胜负”。

    本包不能回答：

    - 某组织带来多少票、提高多少投票率；
    - 哪次集会造成候选胜负；
    - 同场出现是否构成稳定联盟；
    - 候选接受问卷、提案或集会诉求后是否改变政策；
    - 政党、候选人或临时选举体是否应进入NGO registry。

    ## 4. HR-026 复核重点

    `HR026_election_civic_role_review_v0.csv` 有 {len(EVENTS)} 项；重生时保留既有 decision／reviewer／date／note 及附加 final/status 字段，不把已填写值清空。优先复核：

    1. 2014岛ぐるみ会议与A059的实体映射，以及“非直接选举目的”边界；
    2. 女性请求团／女性集会的组织名、名单数量与 request/endorsement 区分；
    3. 2018 All Okinawa 两次议题集会不得改写为候选支持；
    4. `#みんなごと` 的公开讨论、提案草拟、发布三种角色不可合并；
    5. 2022 All Okinawa大会的争议性措辞；
    6. 问卷中具志坚隆松、元山仁士郎等个人参与不得转嫁为其关联组织角色；
    7. 所有组织自述的“支援／奋战”不得升级为票数或胜负因果。

    ## 5. 复现

    运行：

    ```powershell
    python scripts\\make_r09_election_civic_interface_v1.py
    ```

    脚本从内置、可审计的候选记录生成两张图、事件表、三届窗口表、source proposal、HR-026、在线缺口与验证报告；重复运行字节稳定（图的metadata日期固定）。
    """).strip() + "\n"


def make_readme() -> str:
    return dedent("""
    # R09 election-civic interface v1

    Generated by `python scripts/make_r09_election_civic_interface_v1.py`.

    ## Outputs

    - `../../data/interim/33_r09_election_civic_events_v1.csv` — 19 election-sensitive actor-event candidates across 2014/2018/2022.
    - `three_election_windows_v1.csv` — year-level coverage and explicit online limits.
    - `intervention_mode_counts_v1.csv` — complete 3×5 action-mode grid.
    - `source_proposals_v1.csv` — historical 21-row proposal snapshot; every relation/claim approval flag is `no`. Current provisional S IDs are in `../next_wave_source_integration_v1/proposal_to_source_crosswalk_v1.csv`; source indexing does not approve claims.
    - `HR026_election_civic_role_review_v0.csv` — 19 stable review items; regeneration preserves all human and added final/status fields by `review_item_id`.
    - `online_gap_register_v1.csv` — five bounded online-exhausted details.
    - `fig_r09_intervention_modes_v1.*` — candidate action-mode comparison.
    - `fig_r09_noncausal_mechanism_v1.*` — explanatory non-causal mechanism.
    - `R09_election_civic_interface_brief_v1.md` — findings and interpretation boundaries.
    - `validation_report_v1.md` — generated checks.

    ## Status boundary

    This is a candidate/review package, not a human-reviewed formal relation layer. Candidate and party names are event nodes only. No row licenses a vote, turnout, victory, persuasion, policy-effect or stable-alliance claim.
    """).strip() + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_rows(windows: list[dict[str, str]], modes: list[dict[str, str]], hr_rows: list[dict[str, str]]) -> None:
    assert len(EVENTS) == 19
    assert len(SOURCES) == 21
    assert len(windows) == 3
    assert len(modes) == 15
    assert len(hr_rows) == len(EVENTS)
    assert {row["election_year"] for row in EVENTS} == {"2014", "2018", "2022"}
    assert {row["action_type"] for row in EVENTS} == {"endorsement", "issue_campaign", "public_meeting", "request", "observation"}
    assert all(row["machine_status"] == "needs_human_review" and row["hr_task_id"] == "HR-026" for row in EVENTS)
    assert all(row["relation_or_claim_approved"] == "no" for row in SOURCES)
    assert len({row["record_id"] for row in EVENTS}) == len(EVENTS)
    assert len({row["proposal_id"] for row in SOURCES}) == len(SOURCES)
    source_ids = {row["proposal_id"] for row in SOURCES}
    for row in EVENTS:
        refs = set(row["source_proposal_ids"].split(";"))
        assert refs <= source_ids, (row["record_id"], refs - source_ids)
        assert "caus" in row["interpretation_limit"].lower() or any(
            term in row["interpretation_limit"].lower() for term in (
                "effect", "vote", "turnout", "endorsement", "alliance", "influence",
                "uptake", "persuasion", "registry", "roster", "candidate", "scale",
                "participation", "continuity", "wording", "transfer", "organization",
            )
        ), row["record_id"]
    assert len({row["review_item_id"] for row in hr_rows}) == len(hr_rows)
    assert {row["record_id"] for row in hr_rows} == {row["record_id"] for row in EVENTS}
    assert all(field in row for row in hr_rows for field in HUMAN_FIELDS)
    assert all(row["online_status"] == "minimum_public_window_found" for row in windows)
    assert all(row["search_status"] == "online_exhausted" for row in GAPS)
    forbidden_actor_names = {"自由民主党", "公明党", "日本共産党", "社会民主党", "立憲民主党"}
    assert not any(row["actor_name"] in forbidden_actor_names for row in EVENTS)


def make_validation(
    windows: list[dict[str, str]], modes: list[dict[str, str]],
    hr_rows: list[dict[str, str]], preservation: dict[str, int],
) -> str:
    counts = Counter(row["action_type"] for row in EVENTS)
    years = Counter(row["election_year"] for row in EVENTS)
    human_fields = set(HUMAN_FIELDS) | {
        field for row in hr_rows for field in row if field not in HR_FIELDS
    }
    filled = sum(any(row.get(field, "") for field in human_fields) for row in hr_rows)
    return dedent(f"""
    # R09 election-civic interface validation v1

    Generated: 2026-07-13

    - Event candidate rows: {len(EVENTS)} ({dict(sorted(years.items()))}).
    - Action types: {dict(sorted(counts.items()))}; all five required types present.
    - Year windows: {len(windows)}; all `minimum_public_window_found`.
    - Source proposals: {len(SOURCES)}; every `relation_or_claim_approved=no`.
    - HR-026 rows: {len(hr_rows)} stable IDs; {filled} rows currently contain human/final/status values.
    - Stable ID mapping: pre-existing `record_id` retains its `review_item_id`; new rows allocate only unused suffixes.
    - HR preservation: {preservation['preserved_nonblank_rows']} populated rows restored from the pre-existing file; {preservation['extra_human_fields']} extra human columns retained.
    - Temporary-copy sentinel test (`TEST_HUMAN_DECISION` plus final/status fields): passed; real HR table was not modified by the test.
    - Online-exhausted bounded gaps: {len(GAPS)}.
    - Source foreign keys and record/proposal uniqueness: passed.
    - Candidate/party node boundary: passed; no party is encoded as civic actor.
    - Every event row has an explicit no-effect/no-alliance/no-endorsement-overreach boundary: passed.
    - Two explanatory figures generated in PNG and SVG; SVG line-tail whitespace normalized after save: passed.
    - Generated CSV/Markdown outputs are deterministic; figure metadata date is fixed.
    """).strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    windows = build_windows()
    modes = build_mode_counts()
    generated_hr_rows = build_hr026()
    human_preservation_self_test(generated_hr_rows)
    hr_rows, hr_fields, preservation = preserve_human_fields(
        generated_hr_rows, HR_PATH, HR_FIELDS, identity_field="record_id",
    )
    validate_rows(windows, modes, hr_rows)

    write_csv(EVENT_PATH, EVENTS, EVENT_FIELDS)
    write_csv(WINDOW_PATH, windows, WINDOW_FIELDS)
    write_csv(MODE_PATH, modes, MODE_FIELDS)
    write_csv(SOURCE_PATH, SOURCES, SOURCE_FIELDS)
    write_csv(HR_PATH, hr_rows, hr_fields)
    write_csv(GAP_PATH, GAPS, GAP_FIELDS)
    render_mode_figure(modes)
    render_mechanism_figure()
    BRIEF_PATH.write_text(make_brief(windows, modes, hr_rows), encoding="utf-8")
    README_PATH.write_text(make_readme(), encoding="utf-8")
    VALIDATION_PATH.write_text(
        make_validation(windows, modes, hr_rows, preservation), encoding="utf-8",
    )

    for path in (FIG_MODE_PNG, FIG_MODE_SVG, FIG_MECH_PNG, FIG_MECH_SVG):
        if not path.exists() or path.stat().st_size < 8_000:
            raise ValueError(f"Figure missing or unexpectedly small: {path}")

    # Re-read the critical CSVs to catch encoding/header mistakes.
    with EVENT_PATH.open(encoding="utf-8-sig", newline="") as handle:
        assert len(list(csv.DictReader(handle))) == 19
    with HR_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        assert list(reader.fieldnames or []) == hr_fields
        hr_read = list(reader)
        assert len(hr_read) == 19
        assert hr_read == hr_rows

    stable_paths = (EVENT_PATH, WINDOW_PATH, MODE_PATH, SOURCE_PATH, HR_PATH, GAP_PATH, BRIEF_PATH, README_PATH, VALIDATION_PATH)
    digest = hashlib.sha256("".join(sha256(path) for path in stable_paths).encode()).hexdigest()[:16]
    print(
        f"R09 election-civic package generated: 19 candidates / 21 sources / "
        f"HR-026 preserved {preservation['preserved_nonblank_rows']} populated rows / digest {digest}"
    )


if __name__ == "__main__":
    main()
