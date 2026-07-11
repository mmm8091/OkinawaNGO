from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
EXPLAIN = ROOT / "outputs" / "explanatory_v0"
ARCHIVE_MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
OUT = ROOT / "outputs" / "module_completion_v0"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def split_refs(value: str) -> set[str]:
    return {part.strip() for part in value.replace(",", ";").split(";") if part.strip()}


def actor_map(actors: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["actor_id"]: row for row in actors}


def source_map(sources: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["source_id"]: row for row in sources}


def issue_actor_sets(issue_edges: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for row in issue_edges:
        if row["evidence_level"] in {"E2", "E3", "E4"}:
            result[row["issue_label"]].add(row["actor_id"])
    return result


def place_actor_sets(place_edges: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for row in place_edges:
        if row["evidence_level"] in {"E2", "E3", "E4"}:
            result[row["place_name"]].add(row["actor_id"])
    return result


def make_module_status() -> None:
    rows = [
        {
            "module": "R2 actor-issue network",
            "completion_level": "module_v0",
            "current_outputs": "fig_actor_issue_bridge_network.png; actor_issue_bridge_nodes.csv; R02_actor_issue_network_brief.md",
            "what_is_publishable_now": "Issue bridge pattern and bridge actor shortlist, with E2 caveat.",
            "main_gap": "Need relation strength and event-specific issue roles.",
            "next_action": "Add event_id/action_type to actor_issue_edges or derive event table.",
        },
        {
            "module": "R3/R4 place-frame matrix",
            "completion_level": "module_v0",
            "current_outputs": "fig_place_issue_matrix_explanatory.png; place_issue_matrix.csv; R03_R04_place_frame_brief.md",
            "what_is_publishable_now": "Place division of labor: Henoko/Oura Bay ecology-international route; Sakishima life-safety/frontline/autonomy.",
            "main_gap": "Yonaguni, Ishigaki, Miyako still need local newspaper/database reinforcement.",
            "next_action": "Local retrieval package for Yonaguni/Ishigaki/Miyako evidence lines.",
        },
        {
            "module": "R5 co-action network",
            "completion_level": "full_event_list_v0",
            "current_outputs": "coaction_events_v0.csv; coaction_participants_v0.csv; coaction_participants_2020_mmc_71_full_v0.csv; fig_coaction_sample_composition.png; R05_coaction_event_brief.md",
            "what_is_publishable_now": "Co-signing/request samples as event participation, including full 2020 MMC 71-group participant list.",
            "main_gap": "Unmatched 2020 participants need alias/legal identity review before entering actor registry.",
            "next_action": "Review actor_registry_extension_candidates_2020_mmc_v0.csv and add selected actors.",
        },
        {
            "module": "R6 transnational advocacy (legacy R11 filenames)",
            "completion_level": "pathway_v0",
            "current_outputs": "fig_henoko_internationalization_pathway.png; transnational_pathway_nodes_v0.csv; R11_transnational_pathway_brief.md",
            "what_is_publishable_now": "Henoko/Oura Bay issue internationalization pathway.",
            "main_gap": "Actor-to-institution edges and lawsuit plaintiff mapping need more precision.",
            "next_action": "Separate lawsuit, MMC request, and international signatory event tables.",
        },
        {
            "module": "Foundation coverage bias audit (legacy R14 filenames)",
            "completion_level": "audit_v0",
            "current_outputs": "fig_evidence_gap_map.png; coverage_gap_summary_v0.csv; R14_coverage_bias_audit_brief.md",
            "what_is_publishable_now": "Transparent limits of source coverage, review status, and archive status.",
            "main_gap": "Source access classification and missing-cases log need ongoing maintenance.",
            "next_action": "Review failed archives, maintain evidence notes, and execute HR-010–HR-015.",
        },
    ]
    write_csv(
        OUT / "module_status_table_v0.csv",
        rows,
        ["module", "completion_level", "current_outputs", "what_is_publishable_now", "main_gap", "next_action"],
    )


def make_r2(actors: list[dict[str, str]], bridge_nodes: list[dict[str, str]]) -> None:
    top = sorted(bridge_nodes, key=lambda r: (-int(r["issue_count"]), r["actor_id"]))[:12]
    rows = []
    for row in top:
        rows.append(
            {
                "rank": len(rows) + 1,
                "actor_id": row["actor_id"],
                "canonical_name": row["canonical_name"],
                "issue_count": row["issue_count"],
                "issues": row["issues"],
                "actor_class": row["actor_class"],
                "origin_type": row["origin_type"],
                "review_status": row["review_status"],
                "interpretation": "bridge_actor_candidate",
            }
        )
    write_csv(
        OUT / "R02_bridge_actor_shortlist_v0.csv",
        rows,
        ["rank", "actor_id", "canonical_name", "issue_count", "issues", "actor_class", "origin_type", "review_status", "interpretation"],
    )
    bullets = "\n".join(
        f"- {r['actor_id']} {r['canonical_name']}：连接 {r['issues']}；状态 `{r['review_status']}`。"
        for r in rows[:8]
    )
    content = f"""# R2 组织-议题网络 brief v0

## 当前完成度

R2 已达到 `module_v0`：已有 actor-issue edge 表、Top bridge actors 图、桥接组织清单。

## 可交付图件

- `outputs/explanatory_v0/fig_actor_issue_bridge_network.png`
- `outputs/module_completion_v0/R02_bridge_actor_shortlist_v0.csv`

## 当前可讲结论

1. 当前网络中，反基地不是孤立标签，而是经由环保、法律、地方自治、国际倡议和生活安全等框架扩展。
2. 桥接 actor 分成三类：本地运动 / 法律节点、日本国内 NGO / 倡议节点、海外签名 / 国际倡议节点。
3. 该图只能说明“公开资料中的议题连接”，不能说明组织长期主打议题，也不能把共同署名写成稳定联盟。

## Top bridge actors

{bullets}

## 还需要继续做

- 给 actor-issue edge 增加 `event_id` / `action_type` / `relation_strength`。
- 区分长期组织定位、事件性署名、法律程序角色。
- 对 `needs_second_source` 的桥接 actor 优先补证。
"""
    write_text(OUT / "R02_actor_issue_network_brief.md", content)


def make_r3_r4(place_matrix: list[dict[str, str]]) -> None:
    by_place: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in place_matrix:
        if int(row["actor_count"]):
            by_place[row["place"]].append(row)
    rows = []
    for place, items in by_place.items():
        frames = sorted(items, key=lambda r: -int(r["actor_count"]))
        rows.append(
            {
                "place": place,
                "top_frame_1": f"{frames[0]['frame']} ({frames[0]['actor_count']})" if frames else "",
                "top_frame_2": f"{frames[1]['frame']} ({frames[1]['actor_count']})" if len(frames) > 1 else "",
                "top_frame_3": f"{frames[2]['frame']} ({frames[2]['actor_count']})" if len(frames) > 2 else "",
                "interpretation": place_interpretation(place),
                "next_evidence_need": place_next_need(place),
            }
        )
    write_csv(
        OUT / "R03_R04_place_frame_profiles_v0.csv",
        rows,
        ["place", "top_frame_1", "top_frame_2", "top_frame_3", "interpretation", "next_evidence_need"],
    )
    profile_lines = "\n".join(f"- {r['place']}：{r['interpretation']} 主要框架：{'; '.join(v for v in [r['top_frame_1'], r['top_frame_2'], r['top_frame_3']] if v)}。" for r in rows)
    content = f"""# R3/R4 地点-议题框架 brief v0

## 当前完成度

R3/R4 已达到 `module_v0`：已有地点登记表、actor-place edge、地点 × 议题框架矩阵和地点画像表。

## 可交付图件

- `outputs/explanatory_v0/fig_place_issue_matrix_explanatory.png`
- `outputs/module_completion_v0/R03_R04_place_frame_profiles_v0.csv`

## 当前可讲结论

1. 边野古 / 大浦湾是环保、生物多样性、法律程序与国际倡议最集中的场域。
2. 石垣 / 宫古更适合承接生活安全、地下水、住民投票和自卫队配备相关框架。
3. 与那国应按前线化、地方自治、住民投票、健康 / 生活安全读取，不宜强行写成环保拒止主案例。
4. 嘉手纳 / 普天间主要支撑噪音、生活安全、法律诉讼和基地负担框架。

## 地点画像

{profile_lines}

## 还需要继续做

- 与那国 A014/A015 需要地方报纸、意见广告实物、议会记录。
- 石垣 / 宫古需要地下水、住民投票、弹药库 / 导弹配备的来源补强。
- 嘉手纳 / 普天间需要诉讼材料与原告团组织结构补强。
"""
    write_text(OUT / "R03_R04_place_frame_brief.md", content)


def place_interpretation(place: str) -> str:
    mapping = {
        "Henoko": "环保-反基地-国际倡议主场",
        "Oura Bay": "生态 / 儒艮 / 大浦湾环境框架",
        "Ishigaki": "自卫队配备、住民投票、生活安全与地下水线索",
        "Miyako": "导弹 / 弹药库、地下水与生活安全线索",
        "Yonaguni": "前线化、地方自治、住民投票与健康风险线索",
        "Kadena": "爆音诉讼、生活安全、基地负担",
        "Futenma": "城市安全、基地风险与法律程序",
        "Camp Foster": "基地社区服务 / 军属服务场域",
        "U.S. Consulate General Naha": "公共外交 / grant opportunity 场域",
        "JICA Okinawa": "国际合作 / 行政协作背景场域",
    }
    return mapping.get(place, "待解释场域")


def place_next_need(place: str) -> str:
    mapping = {
        "Henoko": "2010/2015/2020 event table and lawsuit/procedure role separation",
        "Oura Bay": "biodiversity reports and actor-role evidence",
        "Ishigaki": "local newspaper and referendum/legal records",
        "Miyako": "local newspaper and groundwater/source protection records",
        "Yonaguni": "local newspaper, town assembly, opinion ad materials",
        "Kadena": "court records and plaintiff organization details",
        "Futenma": "court records and plaintiff organization details",
        "Camp Foster": "service organization program/recipient records",
        "U.S. Consulate General Naha": "award/recipient monitoring",
        "JICA Okinawa": "ONC/JICA/MOFA contract or project records",
    }
    return mapping.get(place, "source reinforcement")


def make_r5(actors: list[dict[str, str]], sources: list[dict[str, str]]) -> None:
    sources_by_id = source_map(sources)
    event_specs = [
        {
            "event_id": "EV2010_WWF_67",
            "event_name": "WWF Japan 67-group Henoko / dugong statement",
            "event_year": "2010",
            "source_id": "S003",
            "relation_type": "joint_statement",
            "relation_strength": "co_signatory_event",
            "interpretation_limit": "co-signing does not prove stable alliance",
        },
        {
            "event_id": "EV2015_NACSJ_31",
            "event_name": "NACSJ / Peace Boat 31-NGO emergency Henoko statement",
            "event_year": "2015",
            "source_id": "S004",
            "relation_type": "joint_statement",
            "relation_strength": "co_signatory_event",
            "interpretation_limit": "co-signing does not prove stable alliance",
        },
        {
            "event_id": "EV2020_OEJP_MMC_71",
            "event_name": "OEJP / MMC civil-society request and report",
            "event_year": "2020",
            "source_id": "S006",
            "relation_type": "request_letter_report",
            "relation_strength": "request_participant_event",
            "interpretation_limit": "current registry under-enters the 71 participants",
        },
    ]
    event_rows = []
    participant_rows = []
    for event in event_specs:
        source = sources_by_id.get(event["source_id"], {})
        participants = [a for a in actors if event["source_id"] in split_refs(a["source_refs"])]
        origin_counts = Counter(a["origin_type"] for a in participants)
        event_rows.append(
            {
                **event,
                "source_title": source.get("title", ""),
                "source_url": source.get("url", ""),
                "registry_participant_count": len(participants),
                "origin_breakdown": ";".join(f"{k}:{v}" for k, v in origin_counts.most_common()),
                "next_action": "review 71-participant candidate table" if event["source_id"] == "S006" else "verify participant roles and aliases",
            }
        )
        for actor in participants:
            participant_rows.append(
                {
                    "event_id": event["event_id"],
                    "source_id": event["source_id"],
                    "actor_id": actor["actor_id"],
                    "canonical_name": actor["canonical_name"],
                    "origin_type": actor["origin_type"],
                    "actor_class": actor["actor_class"],
                    "role": "co_signer_or_participant",
                    "relation_strength": event["relation_strength"],
                    "evidence_level": actor["evidence_level"],
                    "review_status": actor["review_status"],
                    "interpretation_limit": event["interpretation_limit"],
                }
            )
    write_csv(
        OUT / "coaction_events_v0.csv",
        event_rows,
        ["event_id", "event_name", "event_year", "source_id", "source_title", "source_url", "relation_type", "relation_strength", "registry_participant_count", "origin_breakdown", "interpretation_limit", "next_action"],
    )
    write_csv(
        OUT / "coaction_participants_v0.csv",
        participant_rows,
        ["event_id", "source_id", "actor_id", "canonical_name", "origin_type", "actor_class", "role", "relation_strength", "evidence_level", "review_status", "interpretation_limit"],
    )
    event_lines = "\n".join(
        f"- {r['event_id']}：当前 registry 已录入 {r['registry_participant_count']} 个 participant；下一步：{r['next_action']}。"
        for r in event_rows
    )
    content = f"""# R5 共同行动事件 brief v0

## 当前完成度

R5 已达到 `full_event_list_v0`：已有 3 个共同行动事件样本、participant 表、2020 OEJP/MMC 71 团体完整抽取表和构成图。尚未进入“稳定联盟网络”阶段。

## 可交付图表

- `outputs/explanatory_v0/fig_coaction_sample_composition.png`
- `outputs/module_completion_v0/coaction_events_v0.csv`
- `outputs/module_completion_v0/coaction_participants_v0.csv`
- `outputs/module_completion_v0/coaction_participants_2020_mmc_71_full_v0.csv`
- `outputs/module_completion_v0/actor_registry_extension_candidates_2020_mmc_v0.csv`

## 当前可讲结论

1. 当前可以展示共同行动样本如何把本地团体、日本国内 NGO、海外 NGO 放到同一个公开行动中。
2. 这些关系只能写为共同署名、共同请求、共同在场或声援，不能写成稳定联盟。
3. 2020 OEJP/MMC 71 团体样本已抽取完整 participant list；当前 registry 仍需根据候选表继续补 actor。

## 事件状态

{event_lines}

## 还需要继续做

- 从 2020 OEJP/MMC 候选表中筛选应进入 actor registry 的 actor。
- 给每个 participant 标注 role：organizer / signer / plaintiff / attorney / supporter / target。
- 在进入联盟网络图前，先区分一次性署名、重复共同发声、共同诉讼或长期协作。
"""
    write_text(OUT / "R05_coaction_event_brief.md", content)


def mmc_2020_participants() -> list[dict[str, str]]:
    raw = [
        (1, "Diving Team Rainbow", "Environmental organizations and groups in Okinawa", "", ""),
        (2, "Dugong Network Okinawa", "Environmental organizations and groups in Okinawa", "A003", "exact_alias"),
        (3, "Dugong no Sato", "Environmental organizations and groups in Okinawa", "", ""),
        (4, "Dugong Protection Foundation", "Environmental organizations and groups in Okinawa", "A076", "exact_alias"),
        (5, "Okinawa Environmental Justice Project", "Environmental organizations and groups in Okinawa", "A001", "exact"),
        (6, "Okinawa Environmental Network", "Environmental organizations and groups in Okinawa", "A056", "exact_alias"),
        (7, "Okinawa Reefcheck and Research Group", "Environmental organizations and groups in Okinawa", "", ""),
        (8, "Okumagawa Basin Protection Foundation", "Environmental organizations and groups in Okinawa", "", ""),
        (9, "Protect Northernmost Dugong Team Zan", "Environmental organizations and groups in Okinawa", "", ""),
        (10, "Save Awasehigata Association (SAA)", "Environmental organizations and groups in Okinawa", "A055", "exact_alias"),
        (11, "Save the Dugong Campaign Center", "Environmental organizations and groups in Okinawa", "A002", "exact_alias"),
        (12, "All Okinawa Council for Human Rights (AOCHR)", "Peace, human rights and other organizations and groups in Okinawa", "A054", "tentative_alias"),
        (13, "Association of Nightingales, Medical Professionals, and Students for the Protection of Life", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (14, "East Asian Community Institute Ryukyu Okinawa Center", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (15, "Henoko Blue", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (16, "Minshuku Yaponesia", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (17, "Nago Democracy", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (18, "No Helipad Takae Resident Society", "Peace, human rights and other organizations and groups in Okinawa", "A060", "exact_alias"),
        (19, "No Heliport Base Association of 10 Districts North of Futamai", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (20, "Nuchi du Takara o keisyosurukai", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (21, "Okinawa Citizens Network for Peace", "Peace, human rights and other organizations and groups in Okinawa", "A071", "exact_alias"),
        (22, "Okinawa Nobel Peace Prize Action Committee", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (23, "Okinawa Women Act Against Military Violence", "Peace, human rights and other organizations and groups in Okinawa", "A049", "exact_alias"),
        (24, "Project Disagree", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (25, "The Conference Opposing Heliport Construction", "Peace, human rights and other organizations and groups in Okinawa", "A019", "exact_alias"),
        (26, "Wabiai no Sato Foundation", "Peace, human rights and other organizations and groups in Okinawa", "", ""),
        (27, "Veterans for Peace Ryukyu-Okinawa", "Peace, human rights and other organizations and groups in Okinawa", "A070", "exact_alias"),
        (28, "Association for Conservation of Amami Forests, Rivers, and Coastal Ecosystems", "Environmental organizations and groups in Japan", "", ""),
        (29, "Association for Conservation of Marine Communities", "Environmental organizations and groups in Japan", "", ""),
        (30, "Environmental Network AMAMI (ENA)", "Environmental organizations and groups in Japan", "", ""),
        (31, "Iruka & Kujira (Dolphin & Whale) Action Network", "Environmental organizations and groups in Japan", "", ""),
        (32, "Japan Environmental Lawyers for Future (JELF)", "Environmental organizations and groups in Japan", "A020", "exact_alias"),
        (33, "Japan Wetlands Action Network", "Environmental organizations and groups in Japan", "A062", "exact_alias"),
        (34, "Nature Conservation Society of Japan", "Environmental organizations and groups in Japan", "A004", "exact_alias"),
        (35, "Pan-Seto Inland Sea Congress", "Environmental organizations and groups in Japan", "", ""),
        (36, "Protect Henoko and Takae! NGO Network", "Environmental organizations and groups in Japan", "", ""),
        (37, "Ramsar Network Japan", "Environmental organizations and groups in Japan", "A022", "exact_alias"),
        (38, "The Nature and Culture Conservation Group of Amami (NCA)", "Environmental organizations and groups in Japan", "", ""),
        (39, "Ainokai Aitou", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (40, "Airin Community Center", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (41, "AKAY JAPAN", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (42, "AKCDF-MAPALAD KA (The Philippines)", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (43, "All Japan Dockworkers' Union (JDU) Kansai Regional Osaka Branch", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (44, "Anti-war Network", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "A008", "tentative_alias"),
        (45, "Budounokihoikuen", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (46, "East Asian Community Institute", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (47, "Family Home Suzuran", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (48, "Family Home Sansouen", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (49, "Family Home Yamayuri", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (50, "Henoko dosha hanshutsu hantai zenkoku renraku kyougikai", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "A067", "exact_alias"),
        (51, "Henoko ni kichi wo Zettai Tsukurasenai Osaka Kodo", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (52, "Henoko no Umi ni Kichi wo Tsukurasenai Kobe Kodo", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (53, "Kyoto Shimin Center", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (54, "Myougasan Tennpoji", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (55, "Nonoyurihoikuen", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (56, "NPO Active Center Uda", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (57, "NPO Myogamura", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (58, "NPO Sansouen Kazoku", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (59, "NPO Warabemura", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (60, "Ohagi Myogamura", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (61, "Ohisama Firm Ryudo Shizen Noen", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (62, "Peaceforum-Yamaguchi", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (63, "Social Democratic Party Miyazaki", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (64, "Social Welfare Organization SHUKO-GAKUEN", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (65, "Stop! Henoko Reclamation Campaign", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (66, "STOP! Henoko Shinkichikensetsu Osaka Action", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (67, "Straight Inc.", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (68, "The Association for Military Base Free Peaceful Okinawa", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "A072", "tentative_alias"),
        (69, "Yokaichi Megumi Nursery School", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (70, "Yuntaku Takae", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
        (71, "ZENKO, National Assembly for Peace and Democracy", "Peace, human rights, labor, and other organizations and groups in Japan and the Philippines", "", ""),
    ]
    rows = []
    for number, name, category, actor_id, match_status in raw:
        if "Okinawa" in category:
            origin = "okinawa_local"
        elif "Philippines" in name:
            origin = "international"
        else:
            origin = "japan_domestic"
        if "Environmental" in category:
            actor_class = "environmental_ngo_or_group"
        elif "labor" in category:
            actor_class = "peace_human_rights_labor_or_other"
        else:
            actor_class = "peace_human_rights_or_other"
        rows.append(
            {
                "event_id": "EV2020_OEJP_MMC_71",
                "participant_no": number,
                "participant_name_en": name,
                "participant_category": category,
                "origin_guess": origin,
                "actor_class_guess": actor_class,
                "matched_actor_id": actor_id,
                "match_status": match_status or "unmatched_registry_candidate",
                "role": "undersigned_organization_or_group",
                "relation_strength": "co_signatory_request",
                "source_id": "S006",
                "source_detail": "Letter of Request to the U.S. Marine Mammal Commission, July 10 2020, pages 5-7",
                "evidence_level": "E4 for event participation; actor identity may require separate verification",
                "publishable_claim": "cautious",
                "notes": "Co-signing/request participation only; does not prove stable alliance.",
            }
        )
    return rows


def make_mmc_2020_full_tables() -> None:
    rows = mmc_2020_participants()
    write_csv(
        OUT / "coaction_participants_2020_mmc_71_full_v0.csv",
        rows,
        [
            "event_id",
            "participant_no",
            "participant_name_en",
            "participant_category",
            "origin_guess",
            "actor_class_guess",
            "matched_actor_id",
            "match_status",
            "role",
            "relation_strength",
            "source_id",
            "source_detail",
            "evidence_level",
            "publishable_claim",
            "notes",
        ],
    )
    candidates = [
        {
            "participant_no": row["participant_no"],
            "candidate_name": row["participant_name_en"],
            "origin_guess": row["origin_guess"],
            "actor_class_guess": row["actor_class_guess"],
            "source_id": row["source_id"],
            "reason_to_add": "2020 OEJP/MMC 71-group request participant",
            "recommended_review_priority": "P2" if row["origin_guess"] == "okinawa_local" else "P3",
            "notes": "Add only after alias/legal identity check; signatory-only unless further evidence exists.",
        }
        for row in rows
        if not row["matched_actor_id"]
    ]
    write_csv(
        OUT / "actor_registry_extension_candidates_2020_mmc_v0.csv",
        candidates,
        ["participant_no", "candidate_name", "origin_guess", "actor_class_guess", "source_id", "reason_to_add", "recommended_review_priority", "notes"],
    )
    summary = Counter(row["match_status"] for row in rows)
    origin_summary = Counter(row["origin_guess"] for row in rows)
    content = "\n".join(
        [
            "# 2020 OEJP/MMC 71 团体抽取说明 v0",
            "",
            "来源：S006 `Letter of Request to the U.S. Marine Mammal Commission`, 2020-07-10, pages 5-7。",
            "",
            "## 抽取结果",
            "",
            f"- participant 总数：{len(rows)}。",
            f"- 已匹配到现有 actor：{sum(1 for row in rows if row['matched_actor_id'])}。",
            f"- 未匹配、可作为 actor registry 候选：{len(candidates)}。",
            "",
            "## match_status",
            "",
            *[f"- {k}: {v}" for k, v in summary.most_common()],
            "",
            "## origin_guess",
            "",
            *[f"- {k}: {v}" for k, v in origin_summary.most_common()],
            "",
            "## 解释边界",
            "",
            "- 本表只证明这些组织 / 团体在 2020 年 request letter 中作为 undersigned 出现。",
            "- 不能据此写成稳定联盟。",
            "- 未匹配 candidate 不能直接进入核心解释，需要 alias、法律身份或二次来源核实。",
        ]
    )
    write_text(OUT / "coaction_2020_mmc_71_extraction_note.md", content)



def make_r11() -> None:
    nodes = [
        {"node_id": "P002/P003", "layer": "Local site", "label": "Henoko / Oura Bay", "evidence": "E4", "role": "conflict site"},
        {"node_id": "A019", "layer": "Local actors", "label": "ヘリ基地反対協", "evidence": "E4", "role": "Henoko on-site core actor"},
        {"node_id": "A003", "layer": "Local actors", "label": "ジュゴンネットワーク沖縄", "evidence": "E3", "role": "local dugong advocacy"},
        {"node_id": "A076", "layer": "Local actors", "label": "Save the Dugong Foundation", "evidence": "E3", "role": "lawsuit plaintiff direction; mapping still needs precision"},
        {"node_id": "A004", "layer": "Domestic NGO / legal", "label": "NACSJ", "evidence": "E4", "role": "domestic environmental NGO"},
        {"node_id": "A005", "layer": "Domestic NGO / legal", "label": "WWF Japan", "evidence": "E4", "role": "domestic/international environmental NGO"},
        {"node_id": "A020", "layer": "Domestic NGO / legal", "label": "JELF", "evidence": "E4", "role": "legal/environmental procedure"},
        {"node_id": "F_DUGONG", "layer": "Translation frames", "label": "dugong / biodiversity", "evidence": "E4", "role": "environmental translation frame"},
        {"node_id": "F_EIA", "layer": "Translation frames", "label": "EIA / legal procedure", "evidence": "E3/E4", "role": "procedure/legal translation frame"},
        {"node_id": "F_AUTONOMY", "layer": "Translation frames", "label": "local autonomy", "evidence": "E3", "role": "democratic/autonomy frame"},
        {"node_id": "A001", "layer": "International route", "label": "OEJP -> MMC", "evidence": "E4", "role": "U.S. federal institution route"},
        {"node_id": "A009", "layer": "International route", "label": "Earthjustice", "evidence": "E4", "role": "U.S. legal advocacy route"},
        {"node_id": "EV2015_2020", "layer": "International route", "label": "2015 / 2020 signatory networks", "evidence": "signatory-only", "role": "international co-signing / request context"},
    ]
    write_csv(OUT / "transnational_pathway_nodes_v0.csv", nodes, ["node_id", "layer", "label", "evidence", "role"])
    content = """# R11 跨国 / 国际倡议路径 brief v0

## 当前完成度

R11 已达到 `pathway_v0`：已有边野古 / 大浦湾国际化路径图和路径节点表。它已经可以支撑“地方议题如何被翻译成国际机构可处理的问题”的说明。

## 可交付图表

- `outputs/explanatory_v0/fig_henoko_internationalization_pathway.png`
- `outputs/module_completion_v0/transnational_pathway_nodes_v0.csv`

## 当前可讲结论

1. 边野古 / 大浦湾不是单纯地方抗议场域，也被组织转译为儒艮、生物多样性、环境影响评价、法律程序和国际倡议问题。
2. 路径中至少有三类节点：地方现场 actor、日本国内 NGO / 法律网络、美国法院 / 美国联邦机构 / 国际倡议节点。
3. 这张图是路径图，不是资金链，也不是稳定联盟图。

## 禁写边界

- A002 SDCC 不写成美国诉讼法律原告。
- 2015 / 2020 署名网络不写成稳定联盟。
- Earthjustice / MMC 路径不写成“外部操控”或资助关系。

## 还需要继续做

- 把 lawsuit、MMC request、joint statement 分成独立 event table。
- 核实 A019 / A076 / 个人 plaintiff 的具体映射。
- 从 2020 OEJP/MMC 候选表中筛选应进入 actor registry 的 actor。
"""
    write_text(OUT / "R11_transnational_pathway_brief.md", content)


def make_r14(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    manifest: list[dict[str, str]],
    next_candidates: list[dict[str, str]],
) -> None:
    rows = []
    for label, counter in [
        ("actor_review_status", Counter(a["review_status"] for a in actors)),
        ("actor_evidence_level", Counter(a["evidence_level"] for a in actors)),
        ("source_type", Counter(s["source_type"] for s in sources)),
        ("source_archive_status", Counter(m["archive_status"] for m in manifest)),
    ]:
        for key, count in counter.most_common():
            rows.append({"metric_group": label, "metric": key, "count": count})
    write_csv(OUT / "coverage_gap_summary_v0.csv", rows, ["metric_group", "metric", "count"])

    next_summary = Counter((r["item_type"], r["status"]) for r in next_candidates)
    next_lines = "\n".join(f"- {item_type} / {status}: {count}" for (item_type, status), count in sorted(next_summary.items()))
    content = f"""# R14 覆盖与偏差审计 brief v0

## 当前完成度

R14 已达到 `audit_v0`：已有 source archive manifest、HR review log、next investigation candidates 和证据缺口图。

## 可交付图表

- `outputs/explanatory_v0/fig_evidence_gap_map.png`
- `outputs/explanatory_v0/next_investigation_candidates.csv`
- `outputs/module_completion_v0/coverage_gap_summary_v0.csv`

## 当前可讲结论

1. 当前数据不是全量冲绳 NGO 网络，而是公开资料驱动的议题相关 actor registry。
2. 来源覆盖明显偏向边野古 / 大浦湾、公开声明、组织官网、近期网页和国际倡议材料。
3. 离岛小团体、旧组织、报刊数据库材料、军属慈善 recipient 和行政 / 委托合同材料仍需要补。

## 下一轮缺口计数

{next_lines}

## 必须保留的解释边界

- 不能从当前样本推论冲绳所有 NGO 的数量。
- 不能把 NPO 法人生态等同于抗争型市民社会生态。
- 不能把共同署名等同于稳定联盟。
- 不能把 grant opportunity 等同于拨款事实。

## 还需要继续做

- 维护 source archive manifest；新增真实 URL 后继续归档。
- `inferred_url` 已全部解决；手工处理高价值归档失败来源，并记录访问限制。
- 按 HR-010 至 HR-015 复核新增主体字段、法律角色、evidence note 和 event-venue seed。
- 给 source log 增加 source_access / archive_status / coverage_note 字段，或继续使用 manifest 旁表。
- 建立 missing_cases_log，专门记录离岛、旧组织、失效网站和馆内数据库缺口。
"""
    write_text(OUT / "R14_coverage_bias_audit_brief.md", content)


def make_next_tasks() -> None:
    rows = [
        {
            "task_id": "MT-001",
            "module": "R5/R6",
            "priority": "P1",
            "status": "tier_A_added_to_registry_and_R5; B_layer_conditional_C_signatory_only",
            "task": "Review and incorporate 2020 OEJP/MMC 71-group participant list",
            "input": "S006; mt001_candidate_triage_v0.csv; coaction_participants_v0.csv",
            "output": "Tier A 9 actors (A077-A085) added at E2 signatory-only and wired into 2020 MMC co-action event",
            "why_it_matters": "Registry grew 93->102 and the 2020 co-action sample now enters 11 participants; Tier B enters only as a separately coded mainland-solidarity layer when it improves R5/R11; Tier C remains event-only.",
            "done_when": "Tier A aliases and second sources confirmed; issue/place candidate edges added where supported; any Tier B addition is visibly separated from the Okinawa core.",
        },
        {
            "task_id": "MT-002",
            "module": "Foundation",
            "priority": "P1",
            "status": "basically_done",
            "task": "Maintain source archive after first full URL pass",
            "input": "source_docs/source_archive/source_archive_manifest.csv",
            "output": "Updated archive manifest and raw files; 0 pending_archive",
            "why_it_matters": "Prevents link rot and makes the evidence package auditable.",
            "done_when": "New real URLs are archived as they are added; manual archive note exists for non-scriptable sources.",
        },
        {
            "task_id": "MT-003",
            "module": "Foundation/R3",
            "priority": "P1",
            "status": "done; all 25 inferred_url placeholders resolved",
            "task": "Resolve remaining inferred_url placeholders",
            "input": "data/interim/05_source_log_initial_v0.csv; data/interim/16_inferred_url_resolution_queue_v0.csv",
            "output": "All 25 placeholders resolved; S020 recovered as a 2016 Ryukyu Shimpo article; year corrections also made on S027/S030/S037/S040",
            "why_it_matters": "Source log now has 100 real URLs and 2 non-URL references; the evidence base no longer contains inferred URL placeholders.",
            "done_when": "Completed; maintain archive for new URLs and rerun transient failures where appropriate.",
        },
        {
            "task_id": "MT-004",
            "module": "R3/R4",
            "priority": "P1",
            "status": "online_pass_done; org-level still needs local retrieval (Tier 2)",
            "task": "Yonaguni A014/A015 local evidence pack",
            "input": "A014; A015; HR-003; S010; S011; S015; S069; LR-002",
            "output": "MT004 online-pass note; A014 event context corroborated by mainstream media, A015 kept E2 (no non-party source online)",
            "why_it_matters": "Yonaguni is strategically important but current actor evidence remains E2.",
            "done_when": "Org-level identity (founding/representatives/continuity, party vs non-party naming) needs Yaeyama newspaper archives, town-assembly records, and opinion-ad copy (LR Tier 2).",
        },
        {
            "task_id": "MT-005",
            "module": "R11/Foundation",
            "priority": "P2",
            "status": "online_pass_done; named recipients F028-F030 and joint NOSCO event F036 added; full table needs Form 990/internal reports",
            "task": "AWWA / spouse clubs charity recipient evidence",
            "input": "X004-X007; F025-F030; F036; S072; S078; S094; S102; LR-003",
            "output": "Named E3 recipient edges plus NOSCO joint in-kind donation event and field-level online_exhausted logs",
            "why_it_matters": "Turns the unnamed AWWA aggregate (F027) into named, source-backed recipient edges without over-claiming.",
            "done_when": "Full annual recipient table still needs AWWA/club Form 990 Schedule I, annual reports, or internal activity booklets; do not attribute joint gifts to one club.",
        },
        {
            "task_id": "MT-006",
            "module": "R10",
            "priority": "P2",
            "status": "basically_done",
            "task": "ONC / JICA / MOFA relationship chain",
            "input": "X010; X011; A074; S095-S101; F011; F019; F031-F033",
            "output": "MT006 memo + E4 edges F031-F033 with FY2024 project costs; JICA report confirms ONC contractor role without amount; F019 downgraded",
            "why_it_matters": "Places ONC in the international-cooperation/multicultural administrative layer, separate from the anti-base movement and from the base-affairs division.",
            "done_when": "Completed for public online records; retain project-cost wording and do not treat FY2024 costs as contract payment amounts or movement funding.",
        },
        {
            "task_id": "MT-007",
            "module": "R8/R6",
            "priority": "P2",
            "status": "basically_done",
            "task": "Dugong lawsuit plaintiff mapping",
            "input": "A002; A019; A020; A045; A076; A086; S060; S061; S062; S093",
            "output": "lawsuit_actor_role_table_v0.csv + MT007_dugong_lawsuit_note.md",
            "why_it_matters": "Confirms A076 as named plaintiff, keeps A002 SDCC and A019 as non-parties, and clarifies JELF as plaintiff (not counsel) and Earthjustice as counsel.",
            "done_when": "Organization-level parties are mapped and Turtle Island Restoration Network is A086; individuals stay in the role table only.",
        },
        {
            "task_id": "MT-008",
            "module": "R2/R5",
            "priority": "P2",
            "status": "basically_done; event-aware side table v1 built, schema proposal pending merge",
            "task": "Add event_id/action_type/relation_strength to relation edges",
            "input": "coaction_participants_v0.csv; lawsuit_actor_role_table_v0.csv; referendum spec",
            "output": "actor_relation_events_v1.csv (54 rows, 9 events, 5 action types) + MT008 note with schema proposal",
            "why_it_matters": "Turns static issue tags into event-aware network data; separates co-signing, litigation, and referendum roles.",
            "done_when": "07/08 edge tables get optional event_id/action_type/relation_strength columns once the side table is validated; protest and noise-lawsuit events still to add.",
        },
    ]
    write_csv(
        OUT / "next_module_investigation_tasks_v0.csv",
        rows,
        ["task_id", "module", "priority", "status", "task", "input", "output", "why_it_matters", "done_when"],
    )


def write_index() -> None:
    content = """# 模块完成包 v0

日期：2026-07-12（状态更新；模块产出仍为 v0）

编号说明：本包沿用早期内部编号。对最终 DOCX 方案验收时，Henoko/跨国路径归入 R6，coverage audit 归入基础建设；最终方案 R11 是外来 actor 进入生态，R14 是扩展模块“组织谱系”。本包不能替代 `docs/phase1_scheme_acceptance_audit_v1.md` 的 R1–R11 验收状态。

本目录把解释性图表包进一步整理成模块交付物。目标是让下一次沟通不只展示统计，而是展示可解释机制和下一轮调查路线。

## 覆盖模块

- R2 组织-议题网络：`R02_actor_issue_network_brief.md`
- R3/R4 地点-议题框架：`R03_R04_place_frame_brief.md`
- R5 共同行动事件样本：`R05_coaction_event_brief.md`
- R6 跨国 / 国际倡议路径：`R11_transnational_pathway_brief.md`（旧文件名）
- 基础建设覆盖与偏差审计：`R14_coverage_bias_audit_brief.md`（旧文件名）

## 总表

- `module_status_table_v0.csv`
- `next_module_investigation_tasks_v0.csv`

## 沟通建议

下一次沟通建议主用三张图：

1. `outputs/explanatory_v0/fig_place_issue_matrix_explanatory.png`
2. `outputs/explanatory_v0/fig_henoko_internationalization_pathway.png`
3. `outputs/explanatory_v0/fig_actor_issue_bridge_network.png`

补充图：

- `fig_coaction_sample_composition.png` 用来说明 R5 已有样本但不能写成稳定联盟。
- `fig_evidence_gap_map.png` 用来说明下一轮调查为什么会更明确。

## 下一步调查优先级

1. 按 HR-010–HR-015 复核新增主体字段、E3/沿革/范围候选、R8 角色及 evidence/venue seed。
2. 验证事件感知侧表，并补充有足够线上证据的 protest / noise-litigation 事件。
3. 使用 `outputs/phase1_visuals_v1/` 和 `docs/phase1_research_report_v0.md` 完成跨图、图文和证据一致性审查。
4. 把已经字段级 `online_exhausted` 的缺口整理为当地协作者正式任务包。

## 当前状态

- MT-001：Tier A 9 个组织已入 registry 和 R5；Tier B/C 按分层决策暂不入表。
- MT-002：归档机制持续运行；合并后 143 条来源为 128 archived、2 manual、11 failed、2 non-URL；失败状态保留供手工处理。
- MT-003：25 条 `inferred_url` 已全部解决；S020 已恢复为 2016 年真实 URL。
- MT-004：线上 pass 完成，组织级身份仍需当地材料。
- MT-005：线上 pass 完成，已有命名 recipient 与 NOSCO 共同捐赠事件；完整年度表仍需 Form 990 / 内部年报。
- MT-006：ONC 公开年报金额和 JICA 受托角色已补齐，按行政协作层解释。
- MT-007：诉讼角色表完成，Turtle Island Restoration Network 已作为 A086 入 registry。
- MT-008：54 行事件感知侧表完成，主表 schema 是否合并仍待验证。
- REG-01：20 个 E4 主体完成身份级安全合并，registry 达 123；分类、别名与关系边待 HR-010。
- R8：六案元数据以 `needs_human_review` 合并；角色 crosswalk 待 HR-014。
"""
    write_text(OUT / "README.md", content)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    sources = read_csv(DATA / "05_source_log_initial_v0.csv")
    issue_edges = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    place_edges = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    manifest = read_csv(ARCHIVE_MANIFEST)
    bridge_nodes = read_csv(EXPLAIN / "actor_issue_bridge_nodes.csv")
    place_matrix = read_csv(EXPLAIN / "place_issue_matrix.csv")
    next_candidates = read_csv(EXPLAIN / "next_investigation_candidates.csv")

    make_module_status()
    make_r2(actors, bridge_nodes)
    make_r3_r4(place_matrix)
    make_r5(actors, sources)
    make_mmc_2020_full_tables()
    make_r11()
    make_r14(actors, sources, manifest, next_candidates)
    make_next_tasks()
    write_index()
    print(f"Wrote module completion package to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
