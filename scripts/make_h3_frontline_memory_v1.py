from __future__ import annotations

"""Build a research-only package for the H3 frontline/memory hypothesis.

The package separates three claims that must not be collapsed:

H3a — whether vocabulary use increased in a comparable corpus;
H3b — whether vocabulary diffused across organizations/issues;
H3c — whether it supported repeated common mobilization.

Every output is a candidate research layer.  The script reads six archived
documents and three current central tables, writes only to its output
directory, and never mutates central actor, issue, event, or relation data.
"""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "research_wave_h3_frontline_memory_v1"

SOURCE_PATHS = {
    source_id: ROOT / "source_docs" / "source_archive" / source_id / "raw.html"
    for source_id in ("S022", "S023", "S036", "S119", "S148", "S246")
}

SOURCE_LOG_PATH = (
    ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
)
ARCHIVE_MANIFEST_PATH = (
    ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
)

CENTRAL_INPUT_PATHS = (
    ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv",
    ROOT / "data" / "interim" / "09_actor_event_venue_edges_v0.csv",
    ROOT / "data" / "interim" / "24_r01_r02_actor_issue_layered_v0.csv",
)

OUTPUT_FILENAMES = {
    "hypothesis_layers_v1.csv",
    "source_observations_v1.csv",
    "diffusion_carrier_candidates_v1.csv",
    "event_participant_candidates_v1.csv",
    "control_corpus_plan_v1.csv",
    "negative_case_plan_v1.csv",
    "human_review_queue_v1.csv",
    "local_retrieval_queue_v1.csv",
    "source_governance_v1.csv",
    "evidence_graph_v1.json",
    "manifest.json",
    "brief_v1.md",
    "README.md",
}

TARGET_ISSUES = ("frontline_prevention", "Taiwan_contingency", "anti_war")


OBSERVATION_SPECS = [
    {
        "observation_id": "H3O001",
        "source_id": "S036",
        "document_date": "2017-02-28",
        "event_date": "2017-02-28",
        "actor_id": "A065",
        "actor_name": "南西諸島ピースネット",
        "event_id": "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION",
        "event_label": "南西诸岛四团体政府交涉",
        "frame_codes": "evacuation;life_safety;frontline_prevention",
        "observation_type": "attributed_public_frame",
        "original_excerpt": "避難計画策定の必要性を訴えた。",
        "interpretation_limit": "记录的是团体向政府提出避难计划必要性；不证明风险已经发生或政府接受主张。",
    },
    {
        "observation_id": "H3O002",
        "source_id": "S036",
        "document_date": "2017-02-28",
        "event_date": "2017-02-28",
        "actor_id": "A065",
        "actor_name": "南西諸島ピースネット",
        "event_id": "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION",
        "event_label": "南西诸岛四团体政府交涉",
        "frame_codes": "cross_island_coordination;anti_military",
        "observation_type": "event_participant_roster",
        "original_excerpt": "政府交渉を開いたのは、宮古島市民会議、南西諸島ピースネット、八重山大地会、てぃだぬふぁ島の子の平和な未来をつくる会。",
        "interpretation_limit": "共同交涉只证明该事件的共同参与；不建立稳定联盟、成员关系或持续组织。",
    },
    {
        "observation_id": "H3O003",
        "source_id": "S023",
        "document_date": "2022-03-21",
        "event_date": "2021-01–2022-03",
        "actor_id": "A018",
        "actor_name": "ノーモア沖縄戦 命どぅ宝の会",
        "event_id": "H3EV2022_A018_FORMATION_RALLY",
        "event_label": "ノーモア沖縄戦发足集会",
        "frame_codes": "okinawa_war_memory;frontline_prevention;peace",
        "observation_type": "organizational_positioning",
        "original_excerpt": "沖縄を二度と戦場にさせてはいけないという思い",
        "interpretation_limit": "组织定位可见；不据此推定参加者一致、行动效果或全县代表性。",
    },
    {
        "observation_id": "H3O004",
        "source_id": "S023",
        "document_date": "2022-03-21",
        "event_date": "2021-01–2022-03",
        "actor_id": "A018",
        "actor_name": "ノーモア沖縄戦 命どぅ宝の会",
        "event_id": "H3EV2022_A018_FORMATION_RALLY",
        "event_label": "ノーモア沖縄戦发足集会",
        "frame_codes": "Taiwan_contingency;frontline_prevention",
        "observation_type": "organizational_positioning",
        "original_excerpt": "「台湾有事」を想定した日米共同軍事作戦で、南西諸島が攻撃拠点となっていることに反対",
        "interpretation_limit": "这是组织公开风险框架，不是对冲突概率、攻击结果或军事事实的独立判定。",
    },
    {
        "observation_id": "H3O005",
        "source_id": "S022",
        "document_date": "2022-12-07",
        "event_date": "2022-10–2023-09",
        "actor_id": "A017",
        "actor_name": "沖縄対話プロジェクト",
        "event_id": "H3EV2022_2023_OKINAWA_DIALOGUE",
        "event_label": "沖縄对话项目",
        "frame_codes": "okinawa_war_memory;sacrificial_island;Taiwan_contingency",
        "observation_type": "programmatic_memory_link",
        "original_excerpt": "沖縄は第二次世界大戦の末期、本土（日本）の「捨て石」とされ",
        "interpretation_limit": "证明组织以冲绳战记忆解释当前风险；不证明所有对话参与者采用该解释。",
    },
    {
        "observation_id": "H3O006",
        "source_id": "S022",
        "document_date": "2022-12-07",
        "event_date": "2022-10–2023-09",
        "actor_id": "A017",
        "actor_name": "沖縄対話プロジェクト",
        "event_id": "H3EV2022_2023_OKINAWA_DIALOGUE",
        "event_label": "沖縄对话项目",
        "frame_codes": "cross_position_dialogue;war_prevention",
        "observation_type": "programmatic_invitation",
        "original_excerpt": "政治的な立場や意見・思想の違いを超えて対話していこう",
        "preferred_locator": "raw.html:L347",
        "interpretation_limit": "跨立场对话是项目目标；不能据目标反推参与构成、共识形成或扩散效果。",
    },
    {
        "observation_id": "H3O007",
        "source_id": "S119",
        "document_date": "2022-11-29",
        "event_date": "2022-11-28",
        "actor_id": "A100",
        "actor_name": "ミサイル配備から命を守るうるま市民の会",
        "event_id": "H3EV2022_A100_FORMATION",
        "event_label": "宇流麻反导弹部署市民会成立集会",
        "frame_codes": "carrier_event;anti_war;frontline_prevention",
        "observation_type": "speaker_carrier",
        "original_excerpt": "ノーモア沖縄戦命どぅ宝の会の新垣邦雄さんが講演",
        "interpretation_limit": "讲演和到场支持是事件级载体证据；不证明两个组织合并、隶属或稳定联盟。",
    },
    {
        "observation_id": "H3O008",
        "source_id": "S119",
        "document_date": "2022-11-29",
        "event_date": "2022-11-28",
        "actor_id": "A100",
        "actor_name": "ミサイル配備から命を守るうるま市民の会",
        "event_id": "H3EV2022_A100_FORMATION",
        "event_label": "宇流麻反导弹部署市民会成立集会",
        "frame_codes": "Taiwan_contingency;frontline_prevention;life_safety",
        "observation_type": "formation_purpose",
        "original_excerpt": "日米両政府の台湾有事を想定した南西諸島の軍事要塞化に反対し、沖縄を再び戦場にさせないことを目的とする。",
        "interpretation_limit": "组织目的可见；风险因果与政策效果仍须归属于组织主张。",
    },
    {
        "observation_id": "H3O009",
        "source_id": "S148",
        "document_date": "2023-07-26",
        "event_date": "2023-07-25",
        "actor_id": "A108",
        "actor_name": "沖縄を再び戦場にさせない県民の会",
        "event_id": "H3EV2023_A108_FORMATION",
        "event_label": "不让冲绳再次成为战场县民会成立",
        "frame_codes": "organizational_carrier;frontline_prevention;anti_war",
        "observation_type": "organizing_center",
        "original_excerpt": "「ノーモア沖縄戦命どぅ宝の会」を中心とした呼び掛け",
        "interpretation_limit": "证明 A018 在该成立过程中的中心呼吁角色；不把赞同者自动编码为成员或联盟边。",
    },
    {
        "observation_id": "H3O010",
        "source_id": "S148",
        "document_date": "2023-07-26",
        "event_date": "2023-07-25",
        "actor_id": "A108",
        "actor_name": "沖縄を再び戦場にさせない県民の会",
        "event_id": "H3EV2023_A108_FORMATION",
        "event_label": "不让冲绳再次成为战场县民会成立",
        "frame_codes": "war_remains;okinawa_war_memory;future_victimhood",
        "observation_type": "memory_carrier_statement",
        "original_excerpt": "沖縄に戦没者の遺骨があるのは、沖縄が戦場になったからだ。",
        "interpretation_limit": "具志堅隆松的具名论述可见；不能转写成所有赞同组织的统一立场。",
    },
    {
        "observation_id": "H3O011",
        "source_id": "S246",
        "document_date": "2024-01-05",
        "event_date": "2023-11-12",
        "actor_id": "A101",
        "actor_name": "沖縄・琉球弧の声を届ける会",
        "event_id": "H3EV2023_A101_LECTURE_1",
        "event_label": "沖縄・琉球弧之声第一回连续讲座",
        "frame_codes": "new_prewar;frontline_prevention;human_rights",
        "observation_type": "event_master_frame",
        "original_excerpt": "「新たな戦前」に直面する沖縄・琉球弧の島々の真実を！",
        "interpretation_limit": "活动标题证明主办方框架；不证明每个赞同团体接受全部论证。",
    },
    {
        "observation_id": "H3O012",
        "source_id": "S246",
        "document_date": "2024-01-05",
        "event_date": "2023-11-12",
        "actor_id": "A101",
        "actor_name": "沖縄・琉球弧の声を届ける会",
        "event_id": "H3EV2023_A101_LECTURE_1",
        "event_label": "沖縄・琉球弧之声第一回连续讲座",
        "frame_codes": "cross_issue_endorsement;environment;peace;life_safety",
        "observation_type": "endorser_roster",
        "original_excerpt": "泡瀬干潟を守る連絡会、沖縄環境ネットワーク、沖縄平和市民連絡会",
        "interpretation_limit": "赞同名单是该活动的事件级参与证据；不证明稳定联盟、成员身份或后续共同动员。",
    },
]

OBSERVATION_ATTRIBUTION = {
    "H3O001": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": (
            "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION::CIVIC_GROUPS"
        ),
        "claim_subject_label": "南西诸岛部署反对市民团体（报道集合主语）",
        "claim_subject_kind": "reported_collective",
        "target_actor_or_event_id": "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION",
    },
    "H3O002": {
        "hypothesis_id": "H3c",
        "claim_subject_entity_id": (
            "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION::ROSTER"
        ),
        "claim_subject_label": "四团体政府交涉名册",
        "claim_subject_kind": "event_roster",
        "target_actor_or_event_id": "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION",
    },
    "H3O003": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A018",
        "claim_subject_label": "ノーモア沖縄戦 命どぅ宝の会",
        "claim_subject_kind": "registry_actor",
        "target_actor_or_event_id": "A018",
    },
    "H3O004": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A018",
        "claim_subject_label": "ノーモア沖縄戦 命どぅ宝の会",
        "claim_subject_kind": "registry_actor",
        "target_actor_or_event_id": "A018",
    },
    "H3O005": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A017",
        "claim_subject_label": "沖縄対話プロジェクト",
        "claim_subject_kind": "registry_actor",
        "target_actor_or_event_id": "A017",
    },
    "H3O006": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A017",
        "claim_subject_label": "沖縄対話プロジェクト",
        "claim_subject_kind": "registry_actor",
        "target_actor_or_event_id": "A017",
    },
    "H3O007": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "PROV_ARAKAKI_KUNIO",
        "claim_subject_label": "新垣邦雄（A018 关联讲演者）",
        "claim_subject_kind": "provisional_person",
        "target_actor_or_event_id": "A100",
    },
    "H3O008": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A100",
        "claim_subject_label": "ミサイル配備から命を守るうるま市民の会",
        "claim_subject_kind": "registry_actor",
        "target_actor_or_event_id": "A100",
    },
    "H3O009": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A018",
        "claim_subject_label": "ノーモア沖縄戦 命どぅ宝の会",
        "claim_subject_kind": "registry_actor",
        "target_actor_or_event_id": "A108",
    },
    "H3O010": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "PROV_GUSHIKEN_TAKAMATSU",
        "claim_subject_label": "具志堅隆松／ガマフヤー",
        "claim_subject_kind": "provisional_person",
        "target_actor_or_event_id": "A108",
    },
    "H3O011": {
        "hypothesis_id": "H3b",
        "claim_subject_entity_id": "A101",
        "claim_subject_label": "沖縄・琉球弧の声を届ける会",
        "claim_subject_kind": "registry_actor_host",
        "target_actor_or_event_id": "H3EV2023_A101_LECTURE_1",
    },
    "H3O012": {
        "hypothesis_id": "H3c",
        "claim_subject_entity_id": "H3EV2023_A101_LECTURE_1::ENDORSERS",
        "claim_subject_label": "第一回连续讲座赞同团体名册",
        "claim_subject_kind": "event_endorser_roster",
        "target_actor_or_event_id": "H3EV2023_A101_LECTURE_1",
    },
}


HYPOTHESIS_LAYERS = [
    {
        "hypothesis_id": "H3a",
        "hypothesis_label": "词汇增长",
        "question": "可比组织文本中，冲绳战／再度战场化／前线／台湾有事等表达的使用比例是否随时间增加？",
        "unit_of_analysis": "dated organization-authored document",
        "current_assessment": "not_testable_with_current_unbalanced_corpus",
        "current_evidence": "近期组织文本形成可见聚集，但来源年代、文体和组织构成不平衡。",
        "minimum_test": "按时期和文体配平文本，以文档为分母比较标题、宗旨、正文中的首现与使用率。",
        "falsification_rule": "若配平后使用率不增，或增长仅来自 schema 新标签／新组织进入，而既有组织不采用，则否定社会趋势判断。",
        "decision_gate": "human_review_of_corpus_and_dictionary",
    },
    {
        "hypothesis_id": "H3b",
        "hypothesis_label": "跨组织扩散",
        "question": "该语言是否越过原有反战组织，进入环保、生活安全、女性、人权、地方自治等组织或活动？",
        "unit_of_analysis": "organization-document and event-bounded carrier",
        "current_assessment": "candidate_carrier_mechanisms_direction_unconfirmed",
        "current_evidence": "A018 人员参与 A100 成立活动、A018 推动 A108 形成、A101 活动获得跨议题赞同，构成接触／载体路径候选；S246 只证明事件覆盖，不证明组织独立采用。",
        "minimum_test": "先区分载体接触、事件赞同与组织独立采用；只有目标组织在可定位自有文本中采用该语言，或有明确的传播过程证据，才确认扩散。",
        "falsification_rule": "若词汇只出现在主办方文本、其他组织仅被列名且没有独立采用，则不构成跨组织扩散。",
        "decision_gate": "event_and_document_level_human_review",
    },
    {
        "hypothesis_id": "H3c",
        "hypothesis_label": "共同动员",
        "question": "该语言是否使不同议题家族形成可重复的共同动员，而非一次性同场或赞同？",
        "unit_of_analysis": "event-participant-role hyperedge",
        "current_assessment": "episodic_convergence_not_durable_mobilization",
        "current_evidence": "2017、2022、2023 有少数事件性汇合，但中央 AEV 尚无完整、可重复的参与矩阵。",
        "minimum_test": "至少两个可比事件出现 repeat registry actors，且每次均有三个以上议题家族的具名组织和明确事件角色。",
        "falsification_rule": "若跨议题组织只在单一事件同场／赞同，或重复仅来自少数组织者，则否定持续共同动员。",
        "decision_gate": "human_reviewed_event_rosters_and_repeat_test",
    },
]


DIFFUSION_CARRIER_SPECS = [
    {
        "candidate_id": "H3D001",
        "source_id": "S036",
        "event_id": "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION",
        "event_date": "2017-02-28",
        "source_actor_id": "A065",
        "source_actor_name": "南西諸島ピースネット",
        "target_actor_or_event_id": "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION",
        "target_name": "四团体政府交涉",
        "carrier_type": "cross_island_coaction",
        "diffusion_stage": "event_contact_only",
        "direction_status": "not_a_directional_diffusion_observation",
        "observed_role": "named co-participant and evacuation-frame speaker",
        "frame_transfer_candidate": "anti_military→evacuation/life_safety/frontline",
        "evidence_excerpt": "政府交渉を開いたのは、宮古島市民会議、南西諸島ピースネット",
        "interpretation_limit": "单次共同交涉不建立持续网络或同一框架的独立采用。",
    },
    {
        "candidate_id": "H3D002",
        "source_id": "S119",
        "event_id": "H3EV2022_A100_FORMATION",
        "event_date": "2022-11-28",
        "source_actor_id": "A018",
        "source_actor_name": "ノーモア沖縄戦 命どぅ宝の会",
        "target_actor_or_event_id": "A100",
        "target_name": "ミサイル配備から命を守るうるま市民の会",
        "carrier_type": "formation_event_speaker_and_participant",
        "diffusion_stage": "speaker_contact_direction_unconfirmed",
        "direction_status": "unconfirmed",
        "observed_role": "A018 personnel spoke and participated at A100 formation",
        "frame_transfer_candidate": "Okinawa-war/frontline→local missile/life-safety",
        "evidence_excerpt": "ノーモア沖縄戦命どぅ宝の会の新垣邦雄さんが講演",
        "interpretation_limit": "人员讲演和声援不证明组织隶属、共同领导或长期协调。",
    },
    {
        "candidate_id": "H3D003",
        "source_id": "S148",
        "event_id": "H3EV2023_A108_FORMATION",
        "event_date": "2023-07-25",
        "source_actor_id": "A018",
        "source_actor_name": "ノーモア沖縄戦 命どぅ宝の会",
        "target_actor_or_event_id": "A108",
        "target_name": "沖縄を再び戦場にさせない県民の会",
        "carrier_type": "organizing_center",
        "diffusion_stage": "formation_carrier_candidate",
        "direction_status": "candidate_A018_to_A108_not_yet_human_reviewed",
        "observed_role": "reported center of the launch initiative",
        "frame_transfer_candidate": "No-more-Okinawa-war→prefecture-wide anti-war umbrella",
        "evidence_excerpt": "「ノーモア沖縄戦命どぅ宝の会」を中心とした呼び掛け",
        "interpretation_limit": "成立过程的中心角色不自动建立 predecessor、membership 或稳定联盟关系。",
    },
    {
        "candidate_id": "H3D004",
        "source_id": "S148",
        "event_id": "H3EV2023_A108_FORMATION",
        "event_date": "2023-07-25",
        "source_actor_id": "PROV_GUSHIKEN_TAKAMATSU",
        "source_actor_name": "具志堅隆松／ガマフヤー",
        "target_actor_or_event_id": "A108",
        "target_name": "沖縄を再び戦場にさせない県民の会",
        "carrier_type": "war_memory_carrier_cochair",
        "diffusion_stage": "within_target_event_frame_articulation",
        "direction_status": "person_to_event_context_not_org_diffusion",
        "observed_role": "named co-chair linking war remains to future battlefield risk",
        "frame_transfer_candidate": "war remains→future victimhood/frontline prevention",
        "evidence_excerpt": "沖縄に戦没者の遺骨があるのは、沖縄が戦場になったからだ。",
        "interpretation_limit": "个人具名论述不转嫁给全部赞同组织，也不把个人自动 actor 化。",
    },
    {
        "candidate_id": "H3D005",
        "source_id": "S246",
        "event_id": "H3EV2023_A101_LECTURE_1",
        "event_date": "2023-11-12",
        "source_actor_id": "A101",
        "source_actor_name": "沖縄・琉球弧の声を届ける会",
        "target_actor_or_event_id": "H3EV2023_A101_LECTURE_1",
        "target_name": "第一回连续讲座及其赞同团体",
        "carrier_type": "cross_issue_endorsement_event",
        "diffusion_stage": "event_endorsement_only",
        "direction_status": "no_independent_adoption_observed",
        "observed_role": "host framing a listed multi-issue endorser set",
        "frame_transfer_candidate": "new-prewar/frontline→cross-issue event endorsement",
        "evidence_excerpt": "賛同団体：",
        "interpretation_limit": "赞同只限该活动；不能证明每个团体采用全部框架或之后重复共同动员。",
    },
    {
        "candidate_id": "H3D006",
        "source_id": "S022",
        "event_id": "H3EV2022_2023_OKINAWA_DIALOGUE",
        "event_date": "2022-10–2023-09",
        "source_actor_id": "A017",
        "source_actor_name": "沖縄対話プロジェクト",
        "target_actor_or_event_id": "H3EV2022_2023_OKINAWA_DIALOGUE",
        "target_name": "跨政治立场对话项目",
        "carrier_type": "programmatic_cross_position_invitation",
        "diffusion_stage": "host_program_goal_only",
        "direction_status": "no_participant_adoption_observed",
        "observed_role": "project host declaring a cross-position dialogue goal",
        "frame_transfer_candidate": "Okinawa-war/Taiwan-risk→dialogue across political positions",
        "evidence_excerpt": "政治的な立場や意見・思想の違いを超えて対話していこう",
        "preferred_locator": "raw.html:L347",
        "interpretation_limit": "这是项目目标而非参与者构成、实际意见改变或共同组织的证据。",
    },
]


EVENT_PARTICIPANT_SPECS = [
    # S036: four named groups at one government-negotiation event.
    ("S036", "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION", "2017-02-28", "宮古島市民会議", "", "", "provisional_event_entity", "named co-participant", "local anti-deployment"),
    ("S036", "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION", "2017-02-28", "南西諸島ピースネット", "A065", "南西諸島ピースネット", "registry_actor", "named co-participant", "frontline/anti-military"),
    ("S036", "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION", "2017-02-28", "八重山大地会", "", "", "deferred_candidate_entity", "named co-participant", "local anti-deployment"),
    ("S036", "H3EV2017_CROSS_ISLAND_GOV_NEGOTIATION", "2017-02-28", "てぃだぬふぁ島の子の平和な未来をつくる会", "", "", "event_only_entity", "named co-participant", "peace/life-safety"),
    # S246: the event page labels these entities as endorsing groups.
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "泡瀬干潟を守る連絡会", "A055", "泡瀬干潟を守る連絡会", "registry_actor", "listed endorser", "environment/legal"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "沖縄環境ネットワーク", "A056", "沖縄環境ネットワーク", "registry_actor", "listed endorser", "environment"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "沖縄平和市民連絡会", "", "", "provisional_event_entity", "listed endorser", "peace"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "嘉手納ピースアクション", "", "", "provisional_event_entity", "listed endorser", "peace/noise"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "基地・軍隊を許さない行動する女たちの会", "A049", "基地・軍隊を許さない行動する女たちの会", "registry_actor", "listed endorser", "women/human-rights/anti-base"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "ジュゴン保護キャンペーンセンター", "A002", "ジュゴン保護キャンペーンセンター（Save the Dugong Campaign Center）", "registry_actor", "listed endorser", "environment/international"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "日本ジャーナリスト会議", "", "", "provisional_event_entity", "listed endorser", "media/human-rights"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "日本ジャーナリスト会議沖縄", "", "", "provisional_event_entity", "listed endorser", "media/human-rights"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "ノーモア沖縄戦命どぅ宝の会", "A018", "ノーモア沖縄戦 命どぅ宝の会", "registry_actor", "listed endorser", "anti-war/frontline"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "ヘリ基地反対協議会", "A019", "ヘリ基地反対協議会（海上ヘリ基地建設反対・平和と名護市政民主化を求める協議会）", "registry_actor", "listed endorser", "Henoko/anti-base"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "ミサイル配備から命を守るうるま市民の会", "A100", "ミサイル配備から命を守るうるま市民の会", "registry_actor", "listed endorser", "life-safety/frontline"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "有機フッ素化合物（PFAS）汚染から市民の生命を守る連絡会", "A099", "有機フッ素化合物（PFAS）汚染から市民の生命を守る連絡会", "registry_actor", "listed endorser", "PFAS/life-safety"),
    ("S246", "H3EV2023_A101_LECTURE_1", "2023-11-12", "NPO 法人奥間川流域保護基金", "", "", "provisional_event_entity", "listed endorser", "environment"),
]


CONTROL_CORPUS_PLAN = [
    {
        "control_id": "H3C001",
        "period": "2010",
        "candidate_source_or_event": "EV2010_WWF_67 / S003",
        "document_genre": "joint statement",
        "comparison_role": "早期生态／边野古共同声明",
        "test": "用相同词典检查战争记忆、前线化、台湾有事是否出现及处于何种文本位置。",
        "status": "planned_not_collected",
    },
    {
        "control_id": "H3C002",
        "period": "2015",
        "candidate_source_or_event": "EV2015_NACSJ_31 / S004",
        "document_genre": "joint statement",
        "comparison_role": "生态—国际倡议名单对照",
        "test": "区分环保共同声明与后来的前线化共同语言；缺词不预设为负结果。",
        "status": "planned_not_collected",
    },
    {
        "control_id": "H3C003",
        "period": "2020",
        "candidate_source_or_event": "EV2020_MMC_71 / S006",
        "document_genre": "request letter",
        "comparison_role": "近期但仍以边野古／生态为主的事件对照",
        "test": "控制年代后检验议题对象而非年份是否解释词汇差异。",
        "status": "planned_not_collected",
    },
    {
        "control_id": "H3C004",
        "period": "2011–2015",
        "candidate_source_or_event": "A095/A096 宫古反部署陈情与集会",
        "document_genre": "petition and event call",
        "comparison_role": "先岛部署早期地方语言",
        "test": "检验生活、水源和反部署是否早于台湾有事／再战场化主框架。",
        "status": "planned_local_or_archival",
    },
    {
        "control_id": "H3C005",
        "period": "1995–2010",
        "candidate_source_or_event": "女性／和平／劳工组织的基地声明样本",
        "document_genre": "statement or rally resolution",
        "comparison_role": "长期和平语言基线",
        "test": "区分长期 peace/anti-war 词汇与近期 Taiwan/frontline 组合。",
        "status": "planned_local_or_archival",
    },
    {
        "control_id": "H3C006",
        "period": "2021–2024",
        "candidate_source_or_event": "同组织不同事件配对",
        "document_genre": "formation statement vs later action",
        "comparison_role": "组织内采用／保持／退出",
        "test": "检验既有组织是否独立延续该语言，而不只在赞同名单中出现一次。",
        "status": "planned_online",
    },
]


NEGATIVE_CASE_PLAN = [
    {
        "negative_id": "H3N001",
        "case_type": "same_period_no_frontline_language",
        "selection_rule": "2021–2024 同期基地／环境行动，但主办文本未采用目标词典。",
        "purpose": "排除所有近期材料都会出现该语言的年代效应。",
        "required_evidence": "完整活动呼吁／决议原文；不能用搜索无结果判定缺席。",
        "status": "planned",
    },
    {
        "negative_id": "H3N002",
        "case_type": "listed_endorser_no_independent_adoption",
        "selection_rule": "S246 等名单中的赞同团体，后续自有文本没有可核独立采用。",
        "purpose": "区分事件性赞同与真正的跨组织扩散。",
        "required_evidence": "赞同事件前后各一份组织自有文本。",
        "status": "planned",
    },
    {
        "negative_id": "H3N003",
        "case_type": "official_frame_without_civic_carrier",
        "selection_rule": "R4 中只见政府／议会的国民保护、避难或台湾有事文本。",
        "purpose": "检验词汇增长是否由官方规划资料可见性而非民间共同语言造成。",
        "required_evidence": "同地同期官方文本与民间组织文本配对。",
        "status": "planned",
    },
    {
        "negative_id": "H3N004",
        "case_type": "new_actor_composition_only",
        "selection_rule": "仅新成立组织使用目标语言，既有环保／和平组织没有改用。",
        "purpose": "区分新组织进入造成的构成变化与既有组织语言扩散。",
        "required_evidence": "同一既有组织跨期文本面板和首次采用日期。",
        "status": "planned",
    },
    {
        "negative_id": "H3N005",
        "case_type": "single_organizer_repeat",
        "selection_rule": "多个事件重复的只有 A018/A108 等少数组织者，外围组织不重复。",
        "purpose": "检验共同动员是否只是组织者核心的事件重组。",
        "required_evidence": "至少两个事件的完整组织角色表和规范化 identity crosswalk。",
        "status": "planned",
    },
]


HUMAN_REVIEW_QUEUE = [
    {
        "review_id": "HR-H3-001",
        "review_scope": "S036 event roster and date",
        "candidate_ids": "H3O001;H3O002;H3D001",
        "question": "是否接受 2017 政府交涉为四团体的事件级共同参与，并保留 A065 2016–2018 时间边界？",
        "decision": "",
    },
    {
        "review_id": "HR-H3-002",
        "review_scope": "A018 formation chronology and frame",
        "candidate_ids": "H3O003;H3O004",
        "question": "报道中的 2021 成组与 2022 发足集会应如何分期；两条 frame 是否均为组织定位？",
        "decision": "",
    },
    {
        "review_id": "HR-H3-003",
        "review_scope": "A018 to A100 carrier",
        "candidate_ids": "H3O007;H3O008;H3D002",
        "question": "是否接受成立集会讲演／到场为事件级话语载体；不得建稳定联盟边？",
        "decision": "",
    },
    {
        "review_id": "HR-H3-004",
        "review_scope": "A018/Gushiken to A108 carrier",
        "candidate_ids": "H3O009;H3O010;H3D003;H3D004",
        "question": "是否接受组织推动和具名战争记忆载体两种不同关系；是否需要 person crosswalk？",
        "decision": "",
    },
    {
        "review_id": "HR-H3-005",
        "review_scope": "S246 endorser crosswalk",
        "candidate_ids": "H3O011;H3O012;H3D005;H3P005-H3P017",
        "question": "逐项确认 13 个赞同名称的 identity 与事件角色；赞同是否仅限该场活动？",
        "decision": "",
    },
    {
        "review_id": "HR-H3-006",
        "review_scope": "H3a corpus denominator",
        "candidate_ids": "H3a;H3C001-H3C006",
        "question": "确定时期、文体与组织面板；不得以 schema 标签数量代替文本频率。",
        "decision": "",
    },
    {
        "review_id": "HR-H3-007",
        "review_scope": "H3c repeat threshold",
        "candidate_ids": "H3c;H3N005",
        "question": "确认共同动员的最低门槛：至少两事件、三议题家族、重复 registry actor 和明确角色。",
        "decision": "",
    },
    {
        "review_id": "HR-H3-008",
        "review_scope": "source governance and attribution",
        "candidate_ids": "S022;S036;S119;H3O001-H3O012",
        "question": (
            "复核 S119 failed-manifest／残留 raw 的归档状态，修正 "
            "S022/S036/S119 source-log 日期或标题，并逐条确认 context "
            "actor、陈述主语和 target 不被混用。"
        ),
        "decision": "",
    },
    {
        "review_id": "HR-H3-009",
        "review_scope": "direct prior art and novelty boundary",
        "candidate_ids": "LIT19;LIT20;LIT21;LIT22;H3a;H3b;H3c",
        "question": (
            "通读冲绳对话项目、A108 成立／大会、石垣“不让岛成为"
            "战场”运动回顾与前泊博盛 2024；判断新意是否只能落在"
            "结构化组织—事件比较、载体／独立采用区分和负案例设计，"
            "不得把战争记忆与前线化的连接本身写成首次发现。"
        ),
        "decision": "",
    },
]


LOCAL_RETRIEVAL_QUEUE = [
    {
        "local_id": "LR-H3-001",
        "priority": "P0",
        "places": "Miyako;Ishigaki;Yonaguni",
        "material": "组织会报、传单、请求书、陈情原文、意见广告",
        "purpose": "建立 2011–2024 地方组织自有文本面板，判断水／自治／前线化语言的首现与变化。",
        "closure_condition": "每地至少三个有日期、可归属具名组织的原始文本，并记录检索阴性范围。",
        "status": "open_local",
    },
    {
        "local_id": "LR-H3-002",
        "priority": "P0",
        "places": "Yonaguni;Yaeyama",
        "material": "A014/A015 的2012意见广告、2015公投传单／会议材料",
        "purpose": "确认早期部署反对是否已经使用前线／台湾／战争记忆语言，避免以近期材料倒推。",
        "closure_condition": "取得实物影像、日期、发行主体和完整正文；无材料时记录馆藏与报刊检索范围。",
        "status": "open_local",
    },
    {
        "local_id": "LR-H3-003",
        "priority": "P1",
        "places": "Okinawa Prefecture",
        "material": "A018/A108 成立材料、赞同团体／呼吁人名单、集会决议",
        "purpose": "区分共同语言、组织构成和事件参与，验证 A018→A108 的载体机制。",
        "closure_condition": "获得原始成立趣意、名单版本日期、角色说明；不把人数／团体数直接写成稳定成员关系。",
        "status": "open_local",
    },
    {
        "local_id": "LR-H3-004",
        "priority": "P1",
        "places": "Okinawa;Sakishima",
        "material": "1995–2020 女性、和平、劳工、环境组织声明与会报",
        "purpose": "形成近期词汇增长的历史对照，并识别既有组织是否后来采用新框架。",
        "closure_condition": "至少覆盖两个历史时期和四个议题家族；保持文体可比。",
        "status": "open_local",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: Iterable[dict[str, object]],
    fields: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_texts() -> dict[str, str]:
    missing = [path for path in SOURCE_PATHS.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing local H3 source file(s): {missing}")
    return {
        source_id: path.read_text(encoding="utf-8", errors="replace")
        for source_id, path in SOURCE_PATHS.items()
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_source_governance() -> list[dict[str, str]]:
    source_log = {
        row["source_id"]: row for row in read_csv(SOURCE_LOG_PATH)
    }
    archive_manifest = {
        row["source_id"]: row for row in read_csv(ARCHIVE_MANIFEST_PATH)
    }
    correction_notes = {
        "S022": (
            "Source log year is 2023, while the archived page metadata and "
            "the H3 observation date are 2022-12-07; the source-log year "
            "requires a separate bounded correction decision."
        ),
        "S036": (
            "Source log says 2015 formation, while the archived page used here "
            "is a 2017-02-28 government-negotiation report; identity/formation "
            "support and event dating must remain separate."
        ),
        "S119": (
            "Source log year is 2026, while the local article states "
            "2022-11-29; archive manifest is failed even though raw.html is "
            "present and therefore requires reconciliation."
        ),
    }
    rows: list[dict[str, str]] = []
    for source_id, raw_path in sorted(SOURCE_PATHS.items()):
        source = source_log.get(source_id, {})
        archive = archive_manifest.get(source_id, {})
        raw_present = raw_path.is_file()
        archive_status = archive.get("archive_status", "missing_manifest_row")
        if archive_status == "archived":
            use_status = (
                "candidate_source_metadata_correction_needed"
                if source_id in correction_notes
                else "candidate_archived_input"
            )
        elif raw_present:
            use_status = (
                "candidate_local_residual_archive_reconciliation_required"
            )
        else:
            use_status = "blocked_missing_local_source"
        rows.append(
            {
                "source_id": source_id,
                "source_log_title": source.get("title", ""),
                "source_log_year": source.get("year", ""),
                "source_log_url": source.get("url", ""),
                "archive_status": archive_status,
                "manifest_local_path": archive.get("local_path", ""),
                "manifest_sha256": archive.get("sha256", ""),
                "raw_file_present": "yes" if raw_present else "no",
                "actual_raw_sha256": (
                    file_sha256(raw_path) if raw_present else ""
                ),
                "h3_use_status": use_status,
                "metadata_or_archive_correction_needed": (
                    "yes" if source_id in correction_notes or archive_status != "archived"
                    else "no"
                ),
                "correction_note": correction_notes.get(source_id, ""),
                "data_layer": "research_only",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "frontend_eligibility": "not_frontend_ready",
                "central_writeback": "no",
                "interpretation_limit": (
                    "Local file presence does not override archive-manifest "
                    "status or approve the source-log metadata."
                ),
            }
        )
    return rows


def locate(
    text: str,
    excerpt: str,
    preferred_locator: str = "",
) -> str:
    """Return a deterministic raw-file line locator for an exact excerpt."""
    if preferred_locator:
        prefix = "raw.html:L"
        if not preferred_locator.startswith(prefix):
            raise ValueError(f"Invalid preferred locator: {preferred_locator!r}")
        line_number = int(preferred_locator[len(prefix) :])
        lines = text.splitlines()
        if line_number < 1 or line_number > len(lines):
            raise ValueError(f"Preferred locator is outside archive: {preferred_locator}")
        if excerpt not in lines[line_number - 1]:
            raise ValueError(
                f"Excerpt not found at preferred locator {preferred_locator}: "
                f"{excerpt!r}"
            )
        return preferred_locator
    position = text.find(excerpt)
    if position < 0:
        raise ValueError(f"Excerpt not found in approved archive: {excerpt!r}")
    line_number = text.count("\n", 0, position) + 1
    return f"raw.html:L{line_number}"


def validate_actor_crosswalk(
    registry: dict[str, dict[str, str]],
    actor_id: str,
    expected_canonical: str,
) -> None:
    if not actor_id:
        return
    if actor_id not in registry:
        raise ValueError(f"Unknown registry actor in H3 candidate: {actor_id}")
    actual = registry[actor_id]["canonical_name"]
    if actual != expected_canonical:
        raise ValueError(
            f"H3 actor crosswalk drift for {actor_id}: "
            f"{expected_canonical!r} != {actual!r}"
        )


def current_actor_issue_metrics(
    rows: list[dict[str, str]],
) -> tuple[dict[str, int], dict[str, list[str]], dict[str, int]]:
    active = [
        row
        for row in rows
        if row["analysis_inclusion"] == "active"
        and row["issue_label"] in TARGET_ISSUES
    ]
    counts = Counter(row["issue_label"] for row in active)
    actors: dict[str, set[str]] = defaultdict(set)
    reviewed_counts = Counter()
    for row in active:
        actors[row["issue_label"]].add(row["actor_id"])
        if row["review_layer"] == "human_reviewed":
            reviewed_counts[row["issue_label"]] += 1
    return (
        {issue: counts[issue] for issue in TARGET_ISSUES},
        {issue: sorted(actors[issue]) for issue in TARGET_ISSUES},
        {issue: reviewed_counts[issue] for issue in TARGET_ISSUES},
    )


def build_observations(
    texts: dict[str, str],
    source_governance: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for spec in OBSERVATION_SPECS:
        excerpt = spec["original_excerpt"]
        if len(excerpt) > 120:
            raise ValueError(
                f"Observation excerpt exceeds 120 characters: "
                f"{spec['observation_id']}"
            )
        attribution = OBSERVATION_ATTRIBUTION[spec["observation_id"]]
        gate_status = source_governance[spec["source_id"]]["h3_use_status"]
        row = {
            **{
                key: value
                for key, value in spec.items()
                if key
                not in {
                    "preferred_locator",
                    "actor_id",
                    "actor_name",
                    "observation_type",
                }
            },
            **attribution,
            "observation_kind": spec["observation_type"],
            "context_actor_id": spec["actor_id"],
            "context_actor_name": spec["actor_name"],
            "source_path": SOURCE_PATHS[spec["source_id"]]
            .relative_to(ROOT)
            .as_posix(),
            "locator": locate(
                texts[spec["source_id"]],
                excerpt,
                spec.get("preferred_locator", ""),
            ),
            "source_ids": spec["source_id"],
            "archive_gate_status": gate_status,
            "evidence_level": (
                "local_file_candidate_archive_reconciliation_required"
                if "reconciliation_required" in gate_status
                else "source_backed_candidate"
            ),
            "data_layer": "research_only",
            "claim_status": "candidate",
            "review_status": "ai_seeded",
            "frontend_eligibility": "not_frontend_ready",
            "central_writeback": "no",
        }
        rows.append(row)
    return rows


def build_carriers(
    texts: dict[str, str],
    source_governance: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for spec in DIFFUSION_CARRIER_SPECS:
        excerpt = spec["evidence_excerpt"]
        rows.append(
            {
                **{
                    key: value
                    for key, value in spec.items()
                    if key != "preferred_locator"
                },
                "locator": locate(
                    texts[spec["source_id"]],
                    excerpt,
                    spec.get("preferred_locator", ""),
                ),
                "observation_id": spec["candidate_id"],
                "hypothesis_id": "H3b",
                "observation_kind": "event_bounded_carrier_candidate",
                "source_ids": spec["source_id"],
                "archive_gate_status": source_governance[spec["source_id"]][
                    "h3_use_status"
                ],
                "data_layer": "research_only",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "frontend_eligibility": "not_frontend_ready",
                "relation_scope": "event_bounded",
                "diffusion_claim_status": "direction_or_adoption_unconfirmed",
                "stable_alliance_claim": "no",
                "central_writeback": "no",
            }
        )
    return rows


def build_participants(
    texts: dict[str, str],
    registry: dict[str, dict[str, str]],
    source_governance: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, spec in enumerate(EVENT_PARTICIPANT_SPECS, start=1):
        (
            source_id,
            event_id,
            event_date,
            listed_name,
            actor_id,
            canonical_name,
            entity_status,
            participation_role,
            prior_issue_family,
        ) = spec
        validate_actor_crosswalk(registry, actor_id, canonical_name)
        rows.append(
            {
                "participant_id": f"H3P{index:03d}",
                "observation_id": f"H3P{index:03d}",
                "source_id": source_id,
                "event_id": event_id,
                "event_date": event_date,
                "entity_name_as_listed": listed_name,
                "actor_id": actor_id,
                "canonical_name": canonical_name,
                "entity_status": entity_status,
                "participation_role": participation_role,
                "prior_issue_family": prior_issue_family,
                "locator": locate(texts[source_id], listed_name),
                "hypothesis_id": "H3c",
                "observation_kind": "event_participation_or_endorsement",
                "source_ids": source_id,
                "archive_gate_status": source_governance[source_id][
                    "h3_use_status"
                ],
                "data_layer": "research_only",
                "claim_status": "candidate",
                "review_status": "ai_seeded",
                "frontend_eligibility": "not_frontend_ready",
                "stable_alliance_claim": "no",
                "central_writeback": "no",
                "interpretation_limit": (
                    "Event-specific named participation/endorsement only; "
                    "not membership, stable alliance, funding, agreement with "
                    "every event claim, or repeated mobilization."
                ),
            }
        )
    return rows


def build_evidence_graph(
    carriers: list[dict[str, str]],
    participants: list[dict[str, str]],
) -> dict[str, object]:
    nodes: dict[str, dict[str, str]] = {}
    for row in carriers:
        source_id = row["source_actor_id"]
        target_id = row["target_actor_or_event_id"]
        nodes[source_id] = {
            "id": source_id,
            "label": row["source_actor_name"],
            "node_type": (
                "registry_actor" if source_id.startswith("A") else "carrier"
            ),
        }
        nodes[target_id] = {
            "id": target_id,
            "label": row["target_name"],
            "node_type": (
                "registry_actor" if target_id.startswith("A") else "event"
            ),
        }
    for row in participants:
        node_id = row["actor_id"] or f"EVENT_ONLY::{row['entity_name_as_listed']}"
        nodes[node_id] = {
            "id": node_id,
            "label": row["canonical_name"] or row["entity_name_as_listed"],
            "node_type": row["entity_status"],
        }
        if row["event_id"] not in nodes:
            nodes[row["event_id"]] = {
                "id": row["event_id"],
                "label": row["event_id"],
                "node_type": "event",
            }
    return {
        "package_id": "research_wave_h3_frontline_memory_v1",
        "data_layer": "research_only",
        "claim_status": "candidate",
        "graph_semantics": (
            "Event-bounded contact, context, carrier and participation "
            "candidates. Link source/target fields are layout endpoints, not "
            "confirmed diffusion directions or stable alliance edges."
        ),
        "nodes": sorted(nodes.values(), key=lambda row: row["id"]),
        "carrier_links": [
            {
                "id": row["candidate_id"],
                "source": row["source_actor_id"],
                "target": row["target_actor_or_event_id"],
                "carrier_type": row["carrier_type"],
                "diffusion_stage": row["diffusion_stage"],
                "direction_status": row["direction_status"],
                "source_id": row["source_id"],
                "claim_status": "candidate",
                "directional_diffusion_claim": False,
                "stable_alliance_claim": False,
            }
            for row in carriers
        ],
        "event_participation_links": [
            {
                "id": row["participant_id"],
                "source": (
                    row["actor_id"]
                    or f"EVENT_ONLY::{row['entity_name_as_listed']}"
                ),
                "target": row["event_id"],
                "role": row["participation_role"],
                "source_id": row["source_id"],
                "claim_status": "candidate",
                "stable_alliance_claim": False,
            }
            for row in participants
        ],
    }


def build_package(output_dir: Path = OUT) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    texts = source_texts()
    registry_rows = read_csv(CENTRAL_INPUT_PATHS[0])
    aev_rows = read_csv(CENTRAL_INPUT_PATHS[1])
    issue_rows = read_csv(CENTRAL_INPUT_PATHS[2])
    registry = {row["actor_id"]: row for row in registry_rows}

    source_governance_rows = build_source_governance()
    source_governance = {
        row["source_id"]: row for row in source_governance_rows
    }
    observations = build_observations(texts, source_governance)
    carriers = build_carriers(texts, source_governance)
    participants = build_participants(
        texts,
        registry,
        source_governance,
    )
    issue_counts, issue_actor_ids, reviewed_issue_counts = (
        current_actor_issue_metrics(issue_rows)
    )

    common_fields = [
        "data_layer",
        "claim_status",
        "central_writeback",
    ]
    write_csv(
        output_dir / "hypothesis_layers_v1.csv",
        [
            {
                **row,
                "data_layer": "research_only",
                "claim_status": "candidate",
                "central_writeback": "no",
            }
            for row in HYPOTHESIS_LAYERS
        ],
        [
            "hypothesis_id",
            "hypothesis_label",
            "question",
            "unit_of_analysis",
            "current_assessment",
            "current_evidence",
            "minimum_test",
            "falsification_rule",
            "decision_gate",
            *common_fields,
        ],
    )
    write_csv(
        output_dir / "source_observations_v1.csv",
        observations,
        [
            "observation_id",
            "hypothesis_id",
            "observation_kind",
            "source_id",
            "source_ids",
            "source_path",
            "document_date",
            "event_date",
            "context_actor_id",
            "context_actor_name",
            "claim_subject_entity_id",
            "claim_subject_label",
            "claim_subject_kind",
            "target_actor_or_event_id",
            "event_id",
            "event_label",
            "frame_codes",
            "original_excerpt",
            "locator",
            "archive_gate_status",
            "evidence_level",
            "data_layer",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "central_writeback",
            "interpretation_limit",
        ],
    )
    write_csv(
        output_dir / "diffusion_carrier_candidates_v1.csv",
        carriers,
        [
            "observation_id",
            "candidate_id",
            "hypothesis_id",
            "observation_kind",
            "source_id",
            "source_ids",
            "event_id",
            "event_date",
            "source_actor_id",
            "source_actor_name",
            "target_actor_or_event_id",
            "target_name",
            "carrier_type",
            "diffusion_stage",
            "direction_status",
            "observed_role",
            "frame_transfer_candidate",
            "evidence_excerpt",
            "locator",
            "archive_gate_status",
            "data_layer",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "relation_scope",
            "diffusion_claim_status",
            "stable_alliance_claim",
            "central_writeback",
            "interpretation_limit",
        ],
    )
    write_csv(
        output_dir / "event_participant_candidates_v1.csv",
        participants,
        [
            "observation_id",
            "participant_id",
            "hypothesis_id",
            "observation_kind",
            "source_id",
            "source_ids",
            "event_id",
            "event_date",
            "entity_name_as_listed",
            "actor_id",
            "canonical_name",
            "entity_status",
            "participation_role",
            "prior_issue_family",
            "locator",
            "archive_gate_status",
            "data_layer",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "central_writeback",
            "stable_alliance_claim",
            "interpretation_limit",
        ],
    )
    write_csv(
        output_dir / "control_corpus_plan_v1.csv",
        [
            {
                **row,
                "data_layer": "research_only",
                "claim_status": "planned_candidate",
                "central_writeback": "no",
            }
            for row in CONTROL_CORPUS_PLAN
        ],
        [
            "control_id",
            "period",
            "candidate_source_or_event",
            "document_genre",
            "comparison_role",
            "test",
            "status",
            *common_fields,
        ],
    )
    write_csv(
        output_dir / "negative_case_plan_v1.csv",
        [
            {
                **row,
                "data_layer": "research_only",
                "claim_status": "planned_candidate",
                "central_writeback": "no",
            }
            for row in NEGATIVE_CASE_PLAN
        ],
        [
            "negative_id",
            "case_type",
            "selection_rule",
            "purpose",
            "required_evidence",
            "status",
            *common_fields,
        ],
    )
    write_csv(
        output_dir / "human_review_queue_v1.csv",
        [
            {
                **row,
                "status": "open_human",
                "data_layer": "research_only",
                "central_writeback": "no",
            }
            for row in HUMAN_REVIEW_QUEUE
        ],
        [
            "review_id",
            "review_scope",
            "candidate_ids",
            "question",
            "decision",
            "status",
            "data_layer",
            "central_writeback",
        ],
    )
    write_csv(
        output_dir / "local_retrieval_queue_v1.csv",
        [
            {
                **row,
                "data_layer": "research_only",
                "central_writeback": "no",
            }
            for row in LOCAL_RETRIEVAL_QUEUE
        ],
        [
            "local_id",
            "priority",
            "places",
            "material",
            "purpose",
            "closure_condition",
            "status",
            "data_layer",
            "central_writeback",
        ],
    )
    write_csv(
        output_dir / "source_governance_v1.csv",
        source_governance_rows,
        [
            "source_id",
            "source_log_title",
            "source_log_year",
            "source_log_url",
            "archive_status",
            "manifest_local_path",
            "manifest_sha256",
            "raw_file_present",
            "actual_raw_sha256",
            "h3_use_status",
            "metadata_or_archive_correction_needed",
            "correction_note",
            "data_layer",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "central_writeback",
            "interpretation_limit",
        ],
    )

    graph = build_evidence_graph(carriers, participants)
    (output_dir / "evidence_graph_v1.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    target_event_rows = [
        row
        for row in aev_rows
        if (
            row["actor_or_counterpart_id"]
            in {"A017", "A018", "A065", "A100", "A101", "A108"}
            or row["event_id"] == "EV2023_PREFECTURAL_PEACE_RALLY"
        )
    ]
    manifest: dict[str, object] = {
        "package_id": "research_wave_h3_frontline_memory_v1",
        "as_of_date": "2026-07-20",
        "data_layer": "research_only",
        "claim_status": "candidate",
        "review_status": "ai_seeded",
        "frontend_eligibility": "not_frontend_ready",
        "central_writeback": False,
        "local_source_inputs": [
            {
                "source_id": row["source_id"],
                "archive_status": row["archive_status"],
                "h3_use_status": row["h3_use_status"],
            }
            for row in source_governance_rows
        ],
        "source_governance_blocker_count": sum(
            row["metadata_or_archive_correction_needed"] == "yes"
            for row in source_governance_rows
        ),
        "row_contract_status": (
            "h3_rows_normalized_but_human_and_source_governance_gated"
        ),
        "central_current_inputs": [
            path.relative_to(ROOT).as_posix()
            for path in CENTRAL_INPUT_PATHS
        ],
        "source_governance_inputs": [
            SOURCE_LOG_PATH.relative_to(ROOT).as_posix(),
            ARCHIVE_MANIFEST_PATH.relative_to(ROOT).as_posix(),
        ],
        "current_actor_issue_counts": issue_counts,
        "current_actor_issue_actor_ids": issue_actor_ids,
        "current_human_reviewed_edge_counts": reviewed_issue_counts,
        "central_target_aev_rows": len(target_event_rows),
        "package_counts": {
            "source_observations": len(observations),
            "diffusion_carriers": len(carriers),
            "event_participants": len(participants),
            "controls_planned": len(CONTROL_CORPUS_PLAN),
            "negative_cases_planned": len(NEGATIVE_CASE_PLAN),
            "human_review_items": len(HUMAN_REVIEW_QUEUE),
            "local_retrieval_items": len(LOCAL_RETRIEVAL_QUEUE),
        },
        "method_boundaries": [
            "Schema tag growth is not evidence of social vocabulary growth.",
            "Event co-participation or endorsement is not a stable alliance.",
            "Event contact or endorsement is not independent frame adoption.",
            "Carrier endpoints do not establish a diffusion direction.",
            "A common language is not the same as a common organization.",
            "Official evacuation discourse is separated from civic adoption.",
            "Japan-wide war-memory sensitivity is outside the present evidence.",
        ],
        "outputs": sorted(OUTPUT_FILENAMES),
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    brief = f"""# H3 前线化／战争记忆共同语言：研究包 v1

## 当前判断

本包把一个有潜力的解释拆成三个可证伪命题。现有材料只能把 H3b 保留为“载体／接触路径候选、方向未确认”，并把 H3c 保留为事件性覆盖；不足以确认总体词汇增长、跨组织扩散或稳定共同运动。

- H3a 词汇增长：**当前不可检验**。中央有效 actor–issue 层只有 `frontline_prevention={issue_counts['frontline_prevention']}`、`Taiwan_contingency={issue_counts['Taiwan_contingency']}`、`anti_war={issue_counts['anti_war']}` 条边，且时期、文体、组织进入和来源保存不平衡。**标签增长不等于社会趋势**。
- H3b 跨组织扩散：**方向未确认的载体候选**。S119 只支持 A018 人员进入 A100 成立事件，不能证明具体话语由 A018 传给 A100；S148 支持 A018 是 A108 成立呼吁中心之一，较接近形成机制，但仍待人审；具志堅隆松是个人陈述主语。S246 只证明一次活动覆盖多个议题组织，不能证明这些组织独立采用该语言。
- H3c 共同动员：**只见事件性参与／赞同覆盖**。S036、S119、S148、S246 提供少数事件的参加、讲演、组织推动或赞同证据；目前没有两场以上已人审完整名册形成的重复多议题参与矩阵。**同场／赞同不等于稳定联盟**，**共同语言不等于共同组织**。

## 当前最有解释力的候选链

1. 2017 年 A065 等四团体把南西诸岛部署争议带入政府交涉，并提出避难计划问题。
2. 2021–2022 年 A018、A017 把台湾有事／南西诸岛风险与冲绳战、捨て石和“再次成为战场”直接连接。
3. 2022 年 A018 人员参与 A100 成立事件，而 A100 自己公开使用相近的战场化框架；二者的传播方向尚未证实。
4. 2023 年 A018 被报道为推动 A108 形成的中心之一；具志堅隆松以战争遗骨连接过去战场与未来受害风险，但个人陈述不得转嫁给全部组织。
5. 2023 年 A101 以“新たな戦前／琉球弧”举办活动，并获得 13 个跨议题名称赞同；这是事件覆盖候选，不是独立采用、扩散方向或联盟边。

## 竞争解释

- 2020 年后网页、组织站和官方规划资料过密，可能制造近期增长。
- `anti_war` 等 schema 标签是项目后加词表，标签数不能替代历史文本频率。
- 观察到的变化可能是新组织进入，而非既有组织改用共同语言。
- R4 中大量前线／撤离材料来自政府、议会和防卫制度；民间组织可能是在回应官方问题设置。
- 事件间重复可能主要来自 A018/A108 等少数组织者，而非广泛外围持续汇合。

## 最小验证

1. 先处理 `source_governance_v1.csv`：S119 的 failed manifest／残留 raw 必须 reconcile 或人工归档，S022／S036／S119 的 source-log 日期或标题须另行校正。
2. 用 `control_corpus_plan_v1.csv` 建立时期×文体配平语料，以文档为分母，记录标题／宗旨／正文中的首现和语境。
3. 对 S246 赞同团体做事件前后自有文本配对；只有独立采用或可核传播过程才进入 H3b。
4. 对至少两场活动建立 actor×event×role 超边；三个以上原有议题家族且出现重复 registry actor，才进入 H3c。
5. 以 `negative_case_plan_v1.csv` 主动寻找同期未采用、只被列名、仅官方使用和只由新组织使用的反例。
6. 负责人须先通读四项直接先行研究，再判断新意是否仅在结构化比较方法与“载体／独立采用”区分。
7. 负责人逐项完成 `human_review_queue_v1.csv` 后，才决定哪些候选可进入报告；本包不写回中央 AEV、actor–issue 或组织关系层。

## 地理与外推边界

仓库目前能检验的是冲绳战记忆如何在冲绳／琉球弧组织与活动中被重新使用。它不能证明“整个日本的战争记忆敏感性”；该命题需要日本本土学术文献和对照案例。
"""
    (output_dir / "brief_v1.md").write_text(
        brief,
        encoding="utf-8",
        newline="\n",
    )

    readme = """# research_wave_h3_frontline_memory_v1

Independent research package for the hypothesis that frontline/Taiwan-contingency language and Okinawa-war memory may provide a recent common vocabulary across otherwise heterogeneous civic actors.

## Reproduce

```powershell
python scripts\\make_h3_frontline_memory_v1.py
python -m unittest tests.test_make_h3_frontline_memory_v1
```

## Data boundary

- Reads local files for S022, S023, S036, S119, S148 and S246 plus the source log, archive manifest and current actor/AEV/actor–issue tables. S022/S036 remain metadata-correction-gated and S119 remains archive-reconciliation-gated.
- Writes only this output directory.
- Every factual-looking row is `research_only` and `candidate`; `central_writeback=no`.
- Event participation, endorsement, speaking, organizing and personnel carriage are distinct roles. None is a stable alliance edge.
- H3a/H3b/H3c are separate tests. Schema tag growth is never used as evidence of historical vocabulary growth.

## Files

- `hypothesis_layers_v1.csv` — falsifiable H3a/H3b/H3c definitions.
- `source_observations_v1.csv` — short exact excerpts with explicit context actor, claim subject, target and locator.
- `diffusion_carrier_candidates_v1.csv` — event-bounded contact/carrier candidates; direction and adoption remain unconfirmed.
- `event_participant_candidates_v1.csv` — named event participants/endorsers, including provisional identities.
- `control_corpus_plan_v1.csv` and `negative_case_plan_v1.csv` — matched controls and disconfirming-case design.
- `human_review_queue_v1.csv` and `local_retrieval_queue_v1.csv` — explicit gates.
- `source_governance_v1.csv` — archive/source-log mismatch and reconciliation gate.
- `evidence_graph_v1.json` — visualization-ready candidate hypergraph, not a relation network.
- `brief_v1.md` — current interpretation and limits.
- `manifest.json` — inputs, current counts, package counts and boundary metadata.
"""
    (output_dir / "README.md").write_text(
        readme,
        encoding="utf-8",
        newline="\n",
    )

    actual = {path.name for path in output_dir.iterdir() if path.is_file()}
    missing_outputs = OUTPUT_FILENAMES - actual
    if missing_outputs:
        raise AssertionError(f"Missing H3 output(s): {sorted(missing_outputs)}")
    return manifest


def main() -> None:
    manifest = build_package()
    counts = manifest["package_counts"]
    print(
        "H3 research package: "
        f"{counts['source_observations']} observations / "
        f"{counts['diffusion_carriers']} carriers / "
        f"{counts['event_participants']} event participants; "
        "central_writeback=no"
    )


if __name__ == "__main__":
    main()
