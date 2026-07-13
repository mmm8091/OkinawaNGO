from __future__ import annotations

"""Build the R5 event-aware co-action package.

The script reads the current registry and archived primary sources, but writes
only data/interim/25_* and outputs/R05_coaction_v1/.  It deliberately models
event participation rather than durable actor-to-actor alliances.
"""

import csv
import hashlib
import html
import re
from collections import Counter, defaultdict
from pathlib import Path
from textwrap import dedent

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "R05_coaction_v1"
DATA = ROOT / "data" / "interim"
PARTICIPATION_PATH = DATA / "25_coaction_event_participation_v0.csv"
EVENT_PATH = OUT / "event_catalog_v0.csv"
BIPARTITE_PATH = OUT / "actor_event_bipartite_edges_v0.csv"
BRIDGE_PATH = OUT / "repeat_participation_bridges_v0.csv"
OVERLAP_PATH = OUT / "event_overlap_v0.csv"
SOURCE_PATH = OUT / "source_register_v0.csv"
HR020_PATH = OUT / "hr020_review_queue_v0.csv"
HR020_PACKET_PATH = OUT / "HR020_review_packet_v0.md"
BRIEF_PATH = OUT / "R05_explanatory_brief_v0.md"
README_PATH = OUT / "README.md"
VALIDATION_PATH = OUT / "validation_report_v0.md"
BIPARTITE_FIG_PATH = OUT / "fig_r05_event_bipartite_v0.png"
BRIDGE_FIG_PATH = OUT / "fig_r05_repeat_bridges_v0.png"

REGISTRY_PATH = DATA / "01_actor_registry_initial_v0.csv"
SOURCE_LOG_PATH = DATA / "05_source_log_initial_v0.csv"
MANIFEST_PATH = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
MMC_PATH = ROOT / "outputs" / "module_completion_v0" / "coaction_participants_2020_mmc_71_full_v0.csv"
S003_HTML = ROOT / "source_docs" / "source_archive" / "S003" / "raw.html"
S004_HTML = ROOT / "source_docs" / "source_archive" / "S004" / "raw.html"


EVENT_FIELDS = [
    "event_id", "event_name", "event_date", "event_year", "action_type",
    "role_vocabulary", "target_institution", "issue_tags", "place_tags",
    "source_refs", "source_locator", "declared_participant_count",
    "structured_participant_count", "registry_actor_rows", "event_only_name_rows",
    "alias_pending_rows", "interpretation_limit",
]

PARTICIPATION_FIELDS = [
    "event_id", "participant_key", "participant_no", "source_name",
    "canonical_name", "actor_id", "candidate_actor_id", "identity_status",
    "identity_review_status", "origin_type", "actor_class", "action_type",
    "role", "relation_strength", "target_institution", "source_refs",
    "source_locator", "evidence_level", "event_observation_status",
    "hr020_queue_ids", "interpretation_limit",
]

BIPARTITE_FIELDS = [
    "edge_id", "event_id", "participant_key", "entity_key", "actor_id",
    "source_name", "identity_status", "action_type", "role",
    "relation_strength", "source_refs", "review_status", "interpretation_limit",
]

BRIDGE_FIELDS = [
    "bridge_id", "entity_key", "actor_id", "canonical_name", "origin_type",
    "actor_class", "event_count", "event_ids", "action_types", "roles",
    "first_year", "last_year", "relation_strength", "evidence_basis",
    "interpretation_limit",
]

OVERLAP_FIELDS = [
    "event_a", "event_b", "confirmed_registry_actors_a",
    "confirmed_registry_actors_b", "shared_confirmed_registry_actors",
    "jaccard_confirmed_registry", "shared_actor_ids", "interpretation_limit",
]

SOURCE_FIELDS = [
    "source_ref", "existing_source_id", "source_type", "title", "year", "url",
    "archive_status", "local_path", "sha256", "source_locator", "supports",
    "interpretation_limit",
]

HR020_FIELDS = [
    "task_id", "queue_id", "object_type", "participant_keys", "event_ids",
    "source_names", "candidate_actor_id", "candidate_match", "source_refs",
    "source_locator", "review_question", "impact_if_accept", "impact_if_revise",
    "impact_if_reject", "decision", "human_reviewer", "review_date", "decision_note",
]


EVENT_META = {
    "EV2010_WWF_67": {
        "event_name": "2010 WWF Japan 67-group Henoko / dugong joint statement",
        "event_date": "2010-05-14",
        "event_year": "2010",
        "action_type": "joint_statement",
        "role_vocabulary": "listed_endorser",
        "target_institution": "Prime Minister; Minister of Defense; Minister for Foreign Affairs",
        "issue_tags": "Henoko;dugong;biodiversity;anti_base;democracy;life_safety",
        "place_tags": "Henoko;Oura Bay;Kayo;Okinawa",
        "source_refs": "S003",
        "source_locator": "archived raw.html lines 437-439; h3 賛同団体 and following paragraph",
        "declared_participant_count": "67",
    },
    "EV2015_NACSJ_31": {
        "event_name": "2015 NACSJ / Peace Boat 31-NGO Henoko emergency joint statement",
        "event_date": "2015-03-25",
        "event_year": "2015",
        "action_type": "joint_statement",
        "role_vocabulary": "listed_joint_statement_signatory",
        "target_institution": "Government of Japan; Government of the United States",
        "issue_tags": "Henoko;Oura Bay;biodiversity;human_rights;peace;anti_base",
        "place_tags": "Henoko;Oura Bay;Okinawa",
        "source_refs": "S004;S005",
        "source_locator": "S004 archived raw.html lines 346-412; 31 consecutive organization divs",
        "declared_participant_count": "31",
    },
    "EV2020_OEJP_MMC_71": {
        "event_name": "2020 OEJP-led 71-group request and civil-society report to MMC",
        "event_date": "2020-07-10",
        "event_year": "2020",
        "action_type": "request_letter_and_civil_society_report",
        "role_vocabulary": "initiator_and_undersigned_participant;undersigned_request_participant",
        "target_institution": "U.S. Marine Mammal Commission",
        "issue_tags": "Henoko;Oura Bay;dugong;environment;international_advocacy;administrative_oversight",
        "place_tags": "Henoko;Oura Bay;Okinawa;United States",
        "source_refs": "S006",
        "source_locator": "Letter of Request to the U.S. Marine Mammal Commission, 2020-07-10, pp. 5-7",
        "declared_participant_count": "71",
    },
}


MATCHES_2010 = {
    "JUCON ネットワーク": "A028",
    "グリーンピース・ジャパン": "A006",
    "ピースボート": "A007",
    "WWFジャパン": "A005",
    "（財）日本自然保護協会": "A004",
    "（財）日本野鳥の会": "A061",
    "沖縄環境ネットワーク": "A056",
    "沖縄・生物多様性市民ネットワーク": "A029",
    "高江「ヘリパッドいらない」住民の会": "A060",
    "ラムサール・ネットワーク日本": "A022",
    "ジュゴン保護キャンペーンセンター": "A002",
    "日本環境法律家連盟（JELF）": "A020",
    "ピース・フィロソフィー・センター": "A032",
    "日本湿地ネットワーク": "A062",
    "ピース・ニュース": "A026",
    "ジュゴンネットワーク沖縄": "A003",
}


MATCHES_2015 = {
    "国際環境NGO FoE Japan（エフ・オー・イー・ジャパン）": "A021",
    "NPO法人ラムサール・ネットワーク日本": "A022",
    "公益財団法人日本自然保護協会": "A004",
    "国際環境NGO グリーンピース・ジャパン": "A006",
    "ピースボート": "A007",
    "美ら海にもやんばるにも基地はいらない市民の会": "A023",
    "辺野古リレー": "A024",
    "辺野古への基地建設を許さない実行委員会": "A025",
    "ピース・ニュース": "A026",
    "公共事業改革市民会議": "A027",
    "公益財団法人世界自然保護基金（ＷＷＦ）ジャパン": "A005",
    "ジュゴン保護キャンペーンセンター": "A002",
    "沖縄のための日米市民ネットワーク（JUCON）": "A028",
    "沖縄・生物多様性市民ネットワーク": "A029",
    "市川三番瀬を守る会": "A030",
    "三番瀬のラムサール条約登録を実現する会": "A031",
    "Peace Philosophy Centre": "A032",
    "Friends of the Earth U.S.": "A033",
    "KOREA FEDERATION FOR ENVIRONMENTAL MOVEMENTS(KFEM)": "A034",
    "Russian Social Ecological Union": "A035",
    "Friends of the Siberian Forests": "A036",
    "Centre for Environmental Justice": "A037",
    "Sahabat Alam Malaysia": "A038",
    "The Legal Rights and Natural Resources Center-Kasama sa Kalikasan": "A039",
    "Pro Public": "A040",
    "Friends of the Earth Brisbane": "A041",
    "Pacific Environment": "A042",
    "PENGON-FoE Palestine": "A043",
    "Natuvernforbundet(Norwegian Society for the Conservation of Nature)": "A044",
    "Center for biological diversity": "A045",
    "Pro Natura / FoE Switzerland": "A046",
}


# Pending identity questions.  Both sides of a possible cross-event alias remain
# unmerged until a human decision is recorded.
PENDING_BY_EVENT_NAME = {
    ("EV2020_OEJP_MMC_71", "All Okinawa Council for Human Rights (AOCHR)"): ("HR020-01", "A054"),
    ("EV2020_OEJP_MMC_71", "Anti-war Network"): ("HR020-02", "A008"),
    ("EV2020_OEJP_MMC_71", "The Association for Military Base Free Peaceful Okinawa"): ("HR020-03", "A072"),
    ("EV2020_OEJP_MMC_71", "Henoko ni kichi wo Zettai Tsukurasenai Osaka Kodo"): ("HR020-04", "A110"),
    ("EV2020_OEJP_MMC_71", "Stop! Henoko Reclamation Campaign"): ("HR020-05", "A106"),
    ("EV2010_WWF_67", "憲法ひろば・杉並"): ("HR020-06", ""),
    ("EV2010_WWF_67", "福岡地区合同労働組合"): ("HR020-06", ""),
    ("EV2010_WWF_67", "ヘリ基地いらない二見以北十区の会"): ("HR020-07", ""),
    ("EV2020_OEJP_MMC_71", "No Heliport Base Association of 10 Districts North of Futamai"): ("HR020-07", ""),
    ("EV2010_WWF_67", "北限のジュゴンを見守る会"): ("HR020-08", ""),
    ("EV2020_OEJP_MMC_71", "Protect Northernmost Dugong Team Zan"): ("HR020-08", ""),
    ("EV2010_WWF_67", "環瀬戸内海会議"): ("HR020-09", ""),
    ("EV2020_OEJP_MMC_71", "Pan-Seto Inland Sea Congress"): ("HR020-09", ""),
    ("EV2010_WWF_67", "海の生き物を守る会"): ("HR020-10", ""),
    ("EV2020_OEJP_MMC_71", "Association for Conservation of Marine Communities"): ("HR020-10", ""),
    ("EV2010_WWF_67", "みん宿ヤポネシア"): ("HR020-11", ""),
    ("EV2020_OEJP_MMC_71", "Minshuku Yaponesia"): ("HR020-11", ""),
    ("EV2010_WWF_67", "じゅごんの里"): ("HR020-12", ""),
    ("EV2020_OEJP_MMC_71", "Dugong no Sato"): ("HR020-12", ""),
    ("EV2010_WWF_67", "沖縄について考え・連帯する「命どぅ宝」の会"): ("HR020-13", ""),
    ("EV2020_OEJP_MMC_71", "Nuchi du Takara o keisyosurukai"): ("HR020-13", ""),
    ("EV2010_WWF_67", "「自然の権利」基金"): ("HR020-14", "A020"),
}


HR020_SPECS = [
    ("HR020-01", "2020 AOCHR 对应 A054 沖縄人権協会", "A054", "S006", "MMC letter pp. 5-7, participant 12",
     "英文 AOCHR 是否确为 registry A054，而非另一个全冲绳人权团体？",
     "把该参与行连接到 A054；若 A054 另有跨事件行，重复参与计数随之更新。",
     "按人审给出的其他 actor 或规范名连接，并记录修订依据。",
     "保留为 event-only name，不进入 registry actor 桥梁。"),
    ("HR020-02", "2020 Anti-war Network 对应 A008 NGO非戦ネット", "A008", "S006;S064;S065;S066;S067", "MMC letter pp. 5-7, participant 44; A008 existing sources",
     "通用英文名 Anti-war Network 是否足以对应 A008 NGO非戦ネット？",
     "把参与行连接到 A008；不得恢复 S005 对 A008 的旧误配。",
     "按核实到的正式英文名或另一个主体修订。",
     "保留为 event-only name；A008 不获得 2020 参与关系。"),
    ("HR020-03", "2020 基地撤去和平组织英文名对应 A072", "A072", "S006;S031", "MMC letter pp. 5-7, participant 68; registry A072 source S031",
     "The Association for Military Base Free Peaceful Okinawa 是否确为 A072？",
     "把参与行连接到 A072，并仅解释为一次请求参与。",
     "连接到人审核定的其他主体或规范名。",
     "保留为 event-only name。"),
    ("HR020-04", "2020 大阪行动罗马字名对应 A110", "A110", "S006;S153;S154", "MMC letter pp. 5-7, participant 51; A110 organization sources",
     "Henoko ni kichi wo Zettai Tsukurasenai Osaka Kodo 是否为 A110 的罗马字署名？",
     "连接 A110；证明2020请求参与，不证明与其他签署者有稳定联盟。",
     "按人审结果修订为其他主体或规范罗马字别名。",
     "保留为 event-only name；A110 不获得该事件关系。"),
    ("HR020-05", "2020 Stop! Henoko Reclamation Campaign 对应 A106", "A106", "S006;S126;S127", "MMC letter pp. 5-7, participant 65; A106 organization sources",
     "Stop! Henoko Reclamation Campaign 是否为 A106 首都圏キャンペーン／連絡会的英文署名？",
     "连接 A106；不解决 A106 当前 canonical variant 的另一个待定问题。",
     "按人审给出的英文名、组织层级或其他 actor 修订。",
     "保留为 event-only name。"),
    ("HR020-06", "2010 名单缺分隔符的两组织切分", "", "S003;R5S004", "S003 raw.html line 438; WBSJ mirror 賛同団体 paragraph",
     "标称67团体但逗号切分仅66项；“憲法ひろば・杉並福岡地区合同労働組合”是否应切成两个组织？",
     "保留两行，2010结构化总数与来源声明67一致。",
     "按人审提供的正确边界或正式名修订两行。",
     "合并为一个 source-literal 名称；结构化可辨名称降为66，并保留来源自称67的差异。"),
    ("HR020-07", "二見以北十区组织的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 19",
     "2010“ヘリ基地いらない二見以北十区の会”与2020英文名是否为同一组织？",
     "合并为一个 event-only bridge，进入2010/2020重复参与表。",
     "按核实到的正式名、英文别名或组织沿革修订。",
     "两行保持独立 event-only names。"),
    ("HR020-08", "北限儒艮组织的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 9",
     "2010“北限のジュゴンを見守る会”与2020 Protect Northernmost Dugong Team Zan 是否同一组织？",
     "合并为一个 event-only bridge，进入2010/2020重复参与表。",
     "按人审给出的组织名或沿革关系修订。",
     "两行保持独立。"),
    ("HR020-09", "環瀬戸内海会議的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 35",
     "Pan-Seto Inland Sea Congress 是否为環瀬戸内海会議的英文名？",
     "合并为2010/2020 event-only bridge。",
     "按核实到的正式英文名或继承关系修订。",
     "两行保持独立。"),
    ("HR020-10", "海洋生物保护组织的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 29",
     "Association for Conservation of Marine Communities 是否对应2010“海の生き物を守る会”？",
     "合并为2010/2020 event-only bridge。",
     "按人审确认的其他日文名修订。",
     "两行保持独立。"),
    ("HR020-11", "みん宿ヤポネシア的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 16",
     "Minshuku Yaponesia 是否就是2010“みん宿ヤポネシア”？",
     "合并为2010/2020 event-only bridge；仍不自动认定为 NGO。",
     "修订其实体类型、正式名或组织／场所边界。",
     "两行保持独立。"),
    ("HR020-12", "じゅごんの里的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 3",
     "Dugong no Sato 是否就是2010“じゅごんの里”？",
     "合并为2010/2020 event-only bridge。",
     "按正式名或组织持续性证据修订。",
     "两行保持独立。"),
    ("HR020-13", "命どぅ宝名称的日英跨事件对应", "", "S003;S006", "S003 signatory paragraph; MMC letter participant 20",
     "Nuchi du Takara o keisyosurukai 是否对应2010“沖縄について考え・連帯する『命どぅ宝』の会”？",
     "合并为2010/2020 event-only bridge。",
     "按人审确认的日文原名或不同组织关系修订。",
     "两行保持独立。"),
    ("HR020-14", "“自然の権利”基金与 JELF 的实体边界", "A020", "S003", "S003 signatory paragraph and JUCON contact line 441-442",
     "2010名单将 JELF 与“自然の権利”基金分别列名；基金应作为独立 event-only 名、JELF 下属项目，还是 A020 别名？",
     "按人审指定边界连接；若并入 A020，必须注明同一事件双列名问题并避免重复计数。",
     "记录为项目／组织层级关系，但不作为同一 actor。",
     "维持独立 event-only name；不把联系地址关系写成组织同一。"),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = "\n".join(line.rstrip() for line in content.strip().splitlines()) + "\n"
    path.write_text(cleaned, encoding="utf-8")


def clean_html_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[\r\n\t]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    # The archived WWF page contains visual line-wrap spaces inside Japanese words.
    jp = r"\u3040-\u30ff\u3400-\u9fff"
    value = re.sub(fr"(?<=[{jp}]) (?=[{jp}])", "", value)
    value = value.replace("・ジャパ ン", "・ジャパン")
    value = value.replace("基 金", "基金")
    value = value.replace("キャン ペーン", "キャンペーン")
    value = value.replace("労 働組合", "労働組合")
    return value


def extract_2010() -> tuple[list[str], int]:
    raw = S003_HTML.read_text(encoding="utf-8")
    match = re.search(r"<h3>賛同団体</h3>\s*<p>(.*?)</p>", raw, flags=re.S)
    if not match:
        raise AssertionError("Could not locate S003 signatory paragraph")
    literal = clean_html_text(match.group(1))
    source_split = [item.strip() for item in literal.split("、") if item.strip()]
    if len(source_split) != 66:
        raise AssertionError(f"S003 comma split changed: expected 66, got {len(source_split)}")
    joined = "憲法ひろば・杉並福岡地区合同労働組合"
    if source_split.count(joined) != 1:
        raise AssertionError("S003 concatenated-name token changed")
    names: list[str] = []
    for item in source_split:
        if item == joined:
            names.extend(["憲法ひろば・杉並", "福岡地区合同労働組合"])
        else:
            names.append(item)
    if len(names) != 67 or len(set(names)) != 67:
        raise AssertionError("S003 structured list must contain 67 unique rows")
    return names, len(source_split)


def extract_2015() -> list[str]:
    raw = S004_HTML.read_text(encoding="utf-8")
    divs = [clean_html_text(item) for item in re.findall(r"<div[^>]*>(.*?)</div>", raw, flags=re.S)]
    first = "国際環境NGO FoE Japan（エフ・オー・イー・ジャパン）"
    marker = "（3月25日時点 31団体）"
    try:
        start = divs.index(first)
        end = divs.index(marker, start)
    except ValueError as exc:
        raise AssertionError("Could not locate S004 31-group list") from exc
    names = [item for item in divs[start:end] if item and item != "&nbsp;"]
    if len(names) != 31 or len(set(names)) != 31:
        raise AssertionError(f"S004 list must contain 31 unique rows; got {len(names)}")
    return names


def origin_for_unmatched_2010(name: str) -> str:
    okinawa_names = {
        "ヘリ基地いらない二見以北十区の会", "北限のジュゴンを見守る会",
        "みん宿ヤポネシア", "じゅごんの里",
    }
    return "okinawa_local" if name in okinawa_names else "japan_domestic"


def build_participation(registry: dict[str, dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    rows: list[dict[str, str]] = []
    names_2010, raw_count_2010 = extract_2010()
    names_2015 = extract_2015()
    mmc_rows = read_csv(MMC_PATH)
    if len(mmc_rows) != 71 or [int(row["participant_no"]) for row in mmc_rows] != list(range(1, 72)):
        raise AssertionError("MMC source extraction must contain participants 1-71")

    def append_row(event_id: str, no: int, name: str, actor_id: str, origin: str, actor_class: str,
                   source_refs: str, source_locator: str, role: str) -> None:
        pending = PENDING_BY_EVENT_NAME.get((event_id, name))
        if pending:
            queue_id, candidate_actor_id = pending
            identity_status = "alias_pending"
            identity_review_status = "needs_human_review"
            actor_id_final = ""
        elif actor_id:
            queue_id, candidate_actor_id = "", ""
            identity_status = "registry_actor"
            identity_review_status = "accepted_current_registry_match"
            actor_id_final = actor_id
        else:
            queue_id, candidate_actor_id = "", ""
            identity_status = "event_only_name"
            identity_review_status = "event_only_no_registry_merge"
            actor_id_final = ""
        canonical = registry[actor_id_final]["canonical_name"] if actor_id_final else ""
        rows.append({
            "event_id": event_id,
            "participant_key": f"{event_id}:P{no:03d}",
            "participant_no": str(no),
            "source_name": name,
            "canonical_name": canonical,
            "actor_id": actor_id_final,
            "candidate_actor_id": candidate_actor_id,
            "identity_status": identity_status,
            "identity_review_status": identity_review_status,
            "origin_type": registry[actor_id_final]["origin_type"] if actor_id_final else origin,
            "actor_class": registry[actor_id_final]["actor_class"] if actor_id_final else actor_class,
            "action_type": EVENT_META[event_id]["action_type"],
            "role": role,
            "relation_strength": "",
            "target_institution": EVENT_META[event_id]["target_institution"],
            "source_refs": source_refs,
            "source_locator": source_locator,
            "evidence_level": "E4",
            "event_observation_status": (
                "needs_human_review_source_segmentation"
                if queue_id == "HR020-06" else "accepted_source_list_observation"
            ),
            "hr020_queue_ids": queue_id,
            "interpretation_limit": "Publicly listed participation in this event only; not evidence of a stable alliance, membership, funding, or continuing coordination.",
        })

    for no, name in enumerate(names_2010, 1):
        actor_id = MATCHES_2010.get(name, "")
        append_row(
            "EV2010_WWF_67", no, name, actor_id, origin_for_unmatched_2010(name),
            "organization_or_group_unspecified", "S003",
            EVENT_META["EV2010_WWF_67"]["source_locator"], "listed_endorser",
        )

    if set(names_2015) != set(MATCHES_2015):
        missing = sorted(set(names_2015) - set(MATCHES_2015))
        extra = sorted(set(MATCHES_2015) - set(names_2015))
        raise AssertionError(f"S004 mapping mismatch; missing={missing}; extra={extra}")
    for no, name in enumerate(names_2015, 1):
        append_row(
            "EV2015_NACSJ_31", no, name, MATCHES_2015[name], "", "",
            "S004", EVENT_META["EV2015_NACSJ_31"]["source_locator"],
            "listed_joint_statement_signatory",
        )

    for raw in mmc_rows:
        name = raw["participant_name_en"]
        actor_id = raw["matched_actor_id"] if raw["match_status"] in {"exact", "exact_alias"} else ""
        role = "initiator_and_undersigned_participant" if int(raw["participant_no"]) == 5 else "undersigned_request_participant"
        append_row(
            "EV2020_OEJP_MMC_71", int(raw["participant_no"]), name, actor_id,
            raw["origin_guess"], raw["actor_class_guess"], "S006",
            EVENT_META["EV2020_OEJP_MMC_71"]["source_locator"], role,
        )

    event_sets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row["identity_status"] == "registry_actor":
            event_sets[row["actor_id"]].add(row["event_id"])
    for row in rows:
        if row["identity_status"] == "alias_pending":
            row["relation_strength"] = "pending_identity_not_scored"
        elif row["identity_status"] == "event_only_name":
            row["relation_strength"] = "single_event_observation"
        else:
            count = len(event_sets[row["actor_id"]])
            row["relation_strength"] = (
                f"repeated_public_participation_{count}_events"
                if count > 1 else "single_event_registry_participation"
            )
    return rows, raw_count_2010


def build_events(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["event_id"]].append(row)
    events = []
    for event_id, meta in EVENT_META.items():
        event_rows = grouped[event_id]
        counts = Counter(row["identity_status"] for row in event_rows)
        events.append({
            "event_id": event_id,
            **meta,
            "structured_participant_count": str(len(event_rows)),
            "registry_actor_rows": str(counts["registry_actor"]),
            "event_only_name_rows": str(counts["event_only_name"]),
            "alias_pending_rows": str(counts["alias_pending"]),
            "interpretation_limit": "Participant count is a source-list count. It is not a membership count and does not establish a durable coalition.",
        })
    return events


def build_bipartite(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    edges = []
    for idx, row in enumerate(rows, 1):
        entity_key = f"ACTOR:{row['actor_id']}" if row["actor_id"] else f"NAME:{row['participant_key']}"
        edges.append({
            "edge_id": f"R5BE{idx:03d}",
            "event_id": row["event_id"],
            "participant_key": row["participant_key"],
            "entity_key": entity_key,
            "actor_id": row["actor_id"],
            "source_name": row["source_name"],
            "identity_status": row["identity_status"],
            "action_type": row["action_type"],
            "role": row["role"],
            "relation_strength": row["relation_strength"],
            "source_refs": row["source_refs"],
            "review_status": row["identity_review_status"],
            "interpretation_limit": row["interpretation_limit"],
        })
    return edges


def build_bridges(rows: list[dict[str, str]], registry: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    actor_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["identity_status"] == "registry_actor":
            actor_rows[row["actor_id"]].append(row)
    bridges = []
    for actor_id, items in actor_rows.items():
        event_ids = sorted({item["event_id"] for item in items}, key=lambda item: int(EVENT_META[item]["event_year"]))
        if len(event_ids) < 2:
            continue
        action_types = sorted({item["action_type"] for item in items})
        roles = sorted({item["role"] for item in items})
        years = [int(EVENT_META[event_id]["event_year"]) for event_id in event_ids]
        bridges.append({
            "bridge_id": "",
            "entity_key": f"ACTOR:{actor_id}",
            "actor_id": actor_id,
            "canonical_name": registry[actor_id]["canonical_name"],
            "origin_type": registry[actor_id]["origin_type"],
            "actor_class": registry[actor_id]["actor_class"],
            "event_count": str(len(event_ids)),
            "event_ids": ";".join(event_ids),
            "action_types": ";".join(action_types),
            "roles": ";".join(roles),
            "first_year": str(min(years)),
            "last_year": str(max(years)),
            "relation_strength": f"repeated_public_participation_{len(event_ids)}_events",
            "evidence_basis": ";".join(sorted({item["source_refs"] for item in items})),
            "interpretation_limit": "Repeated appearance across sampled public actions is a bridge indicator, not proof of a stable alliance or continuous coordination.",
        })
    bridges.sort(key=lambda row: (-int(row["event_count"]), row["canonical_name"].casefold()))
    for idx, row in enumerate(bridges, 1):
        row["bridge_id"] = f"R5BR{idx:02d}"
    return bridges


def build_overlap(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    sets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row["identity_status"] == "registry_actor":
            sets[row["event_id"]].add(row["actor_id"])
    event_ids = list(EVENT_META)
    overlaps = []
    for i, event_a in enumerate(event_ids):
        for event_b in event_ids[i + 1:]:
            shared = sorted(sets[event_a] & sets[event_b])
            union = sets[event_a] | sets[event_b]
            overlaps.append({
                "event_a": event_a,
                "event_b": event_b,
                "confirmed_registry_actors_a": str(len(sets[event_a])),
                "confirmed_registry_actors_b": str(len(sets[event_b])),
                "shared_confirmed_registry_actors": str(len(shared)),
                "jaccard_confirmed_registry": f"{len(shared) / len(union):.4f}" if union else "0.0000",
                "shared_actor_ids": ";".join(shared),
                "interpretation_limit": "Overlap uses only confirmed current-registry matches; HR-020 aliases are excluded and overlap does not establish alliance durability.",
            })
    return overlaps


def build_sources() -> list[dict[str, str]]:
    source_log = {row["source_id"]: row for row in read_csv(SOURCE_LOG_PATH)}
    manifest = {row["source_id"]: row for row in read_csv(MANIFEST_PATH)}
    locators = {
        "S003": EVENT_META["EV2010_WWF_67"]["source_locator"],
        "S004": EVENT_META["EV2015_NACSJ_31"]["source_locator"],
        "S005": "archived Peace Boat article body; 2015-03-25 statement framing and participation context",
        "S006": EVENT_META["EV2020_OEJP_MMC_71"]["source_locator"],
    }
    supports = {
        "S003": "2010 event, declared 67 groups, source-list names and target ministries",
        "S004": "2015 event and complete 31-name list",
        "S005": "2015 peace/environment framing; does not add a second participant list",
        "S006": "2020 OEJP-led request/report and complete 71-name list from letter pp. 5-7",
    }
    rows = []
    for source_id in ["S003", "S004", "S005", "S006"]:
        source = source_log[source_id]
        archived = manifest[source_id]
        rows.append({
            "source_ref": source_id,
            "existing_source_id": source_id,
            "source_type": source["source_type"],
            "title": source["title"],
            "year": source["year"],
            "url": source["url"],
            "archive_status": archived["archive_status"],
            "local_path": archived["local_path"],
            "sha256": archived["sha256"],
            "source_locator": locators[source_id],
            "supports": supports[source_id],
            "interpretation_limit": source["bias_note"],
        })
    rows.append({
        "source_ref": "R5S004",
        "existing_source_id": "",
        "source_type": "supplementary_primary_organization_page",
        "title": "日本野鳥の会：辺野古への基地建設に反対する共同声明",
        "year": "2010",
        "url": "https://www.wbsj.org/activity/conservation/habitat-conservation/okinawaken/declaration_henoko20100514/",
        "archive_status": "online_checked_not_archived",
        "local_path": "",
        "sha256": "",
        "source_locator": "賛同団体 paragraph and 合計67団体 line; checked 2026-07-13",
        "supports": "corroborates the 2010 statement text, declared total and the same missing-delimiter string",
        "interpretation_limit": "Supplementary mirror does not itself resolve the concatenated-name segmentation.",
    })
    return rows


def build_hr020(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_queue: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["hr020_queue_ids"]:
            by_queue[row["hr020_queue_ids"]].append(row)
    specs = {item[0]: item for item in HR020_SPECS}
    if set(by_queue) != set(specs):
        raise AssertionError(f"HR-020 queue mismatch: rows={sorted(by_queue)} specs={sorted(specs)}")
    queue = []
    for idx, queue_id in enumerate(sorted(specs, key=lambda value: int(value.split("-")[-1])), 1):
        _, candidate_match, candidate_actor_id, source_refs, locator, question, accept, revise, reject = specs[queue_id]
        items = by_queue[queue_id]
        queue.append({
            "task_id": "HR-020",
            "queue_id": queue_id,
            "object_type": "source_name_identity_or_segmentation",
            "participant_keys": ";".join(item["participant_key"] for item in items),
            "event_ids": ";".join(dict.fromkeys(item["event_id"] for item in items)),
            "source_names": ";".join(item["source_name"] for item in items),
            "candidate_actor_id": candidate_actor_id,
            "candidate_match": candidate_match,
            "source_refs": source_refs,
            "source_locator": locator,
            "review_question": question,
            "impact_if_accept": accept,
            "impact_if_revise": revise,
            "impact_if_reject": reject,
            "decision": "",
            "human_reviewer": "",
            "review_date": "",
            "decision_note": "",
        })
    return queue


def build_hr020_packet(queue: list[dict[str, str]]) -> str:
    sections = []
    for row in queue:
        sections.append(dedent(f"""
        ### {row['queue_id']}｜{row['candidate_match']}

        - 对象：`{row['participant_keys']}`
        - 事件：`{row['event_ids']}`
        - 来源原名：{row['source_names']}
        - 候选 registry actor：`{row['candidate_actor_id'] or '无／跨事件 event-only 对应'}`
        - 来源：`{row['source_refs']}`
        - 精确定位：{row['source_locator']}
        - 人工问题：{row['review_question']}
        - 若接受：{row['impact_if_accept']}
        - 若修订：{row['impact_if_revise']}
        - 若拒绝：{row['impact_if_reject']}

        决定（留空）：[ ] accept　[ ] revise　[ ] reject

        复核人：__________　日期：__________

        决定说明：

        """))
    header = dedent(f"""
    # HR-020：R5 共同行动名称／身份人工复核包

    本包只处理线上来源仍无法自动决定的名称切分、日英别名和 registry 对应。事件参与本身已有一手名单支持；待决定的是“这些名称是否代表同一 actor”。

    共 {len(queue)} 个问题。`decision`、`human_reviewer`、`review_date`、`decision_note` 均未预填。接受别名只会改变身份连接与重复参与计数，不会把共同署名改写为稳定联盟。

    ## 决策规则

    - `accept`：明确接受题面对应，按影响说明回写 actor/entity key。
    - `revise`：给出新的规范名、actor、组织层级或名单切分。
    - `reject`：保留不同 event-only names，不建立跨事件或 registry 连接。
    - 任何决定都不得仅凭共同署名推定成员关系、资金关系或持续协调。

    ## 待审项目
    """)
    footer = dedent("""
    ## 回写要求

    人审完成后，应同时重跑参与表、二部边、重复桥梁、重叠表、两图和解释性 brief，并保留原始 `source_name`。
    """)
    return header + "\n" + "".join(sections) + "\n" + footer


def choose_font() -> str:
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Noto Sans CJK JP", "SimHei", "Arial Unicode MS"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return "DejaVu Sans"


def setup_plot() -> None:
    plt.rcParams.update({
        "font.family": choose_font(),
        "axes.unicode_minus": False,
        "figure.facecolor": "#F7F4EE",
        "axes.facecolor": "#F7F4EE",
        "savefig.facecolor": "#F7F4EE",
    })


def short_label(value: str, limit: int = 28) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def plot_bipartite(rows: list[dict[str, str]], bridges: list[dict[str, str]]) -> None:
    setup_plot()
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 1.22)
    ax.set_ylim(0, 1)
    ax.axis("off")
    event_y = {"EV2010_WWF_67": 0.80, "EV2015_NACSJ_31": 0.50, "EV2020_OEJP_MMC_71": 0.20}
    event_short = {"EV2010_WWF_67": "2010 WWF 67", "EV2015_NACSJ_31": "2015 NACSJ 31", "EV2020_OEJP_MMC_71": "2020 MMC 71"}
    colors = {"registry_actor": "#236B8E", "event_only_name": "#9AA0A6", "alias_pending": "#D8842F"}

    bridge_ids = {row["actor_id"] for row in bridges}
    bridge_y = {}
    for idx, bridge in enumerate(bridges):
        y = 0.93 - idx * (0.86 / max(1, len(bridges) - 1))
        bridge_y[bridge["actor_id"]] = y

    single_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["actor_id"] and row["actor_id"] in bridge_ids:
            continue
        single_rows[row["event_id"]].append(row)

    single_positions: dict[str, tuple[float, float]] = {}
    for event_id, items in single_rows.items():
        center = event_y[event_id]
        low, high = center - 0.115, center + 0.115
        for idx, row in enumerate(items):
            frac = (idx + 0.5) / len(items)
            y = low + frac * (high - low)
            x = 0.93 + 0.18 * ((idx % 5) / 4)
            single_positions[row["participant_key"]] = (x, y)

    for row in rows:
        start = (0.17, event_y[row["event_id"]])
        if row["actor_id"] and row["actor_id"] in bridge_y:
            end = (0.55, bridge_y[row["actor_id"]])
            alpha, width = 0.38, 1.0
        else:
            end = single_positions[row["participant_key"]]
            alpha, width = 0.10, 0.45
        ax.plot([start[0], end[0]], [start[1], end[1]], color=colors[row["identity_status"]], alpha=alpha, linewidth=width, zorder=1)

    for event_id, y in event_y.items():
        ax.scatter([0.17], [y], s=1350, color="#17324D", edgecolor="white", linewidth=2.5, zorder=4)
        ax.text(0.17, y, event_short[event_id], color="white", ha="center", va="center", fontsize=12, weight="bold", zorder=5)

    for bridge in bridges:
        y = bridge_y[bridge["actor_id"]]
        ax.scatter([0.55], [y], s=72 + 20 * int(bridge["event_count"]), color="#5B3C88", edgecolor="white", linewidth=1.2, zorder=4)
        ax.text(0.585, y, short_label(bridge["canonical_name"], 30), va="center", fontsize=8.6, color="#29243A")

    for row in rows:
        if row["actor_id"] and row["actor_id"] in bridge_ids:
            continue
        x, y = single_positions[row["participant_key"]]
        ax.scatter([x], [y], s=18 if row["identity_status"] != "alias_pending" else 30,
                   color=colors[row["identity_status"]], alpha=0.84, edgecolor="none", zorder=3)

    ax.text(0.03, 0.975, "R5 事件—参与者二部图（169条公开参与边）", fontsize=20, weight="bold", color="#17324D")
    ax.text(0.03, 0.944, "左：3个行动事件｜中：已确认的跨事件 registry bridge｜右：单次参与者与待审名称", fontsize=11.5, color="#4A5560")
    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=colors["registry_actor"], markersize=8, label="当前 registry actor"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=colors["event_only_name"], markersize=8, label="event-only name"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=colors["alias_pending"], markersize=8, label="HR-020 alias pending"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#5B3C88", markersize=8, label="已确认重复参与 bridge"),
    ]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.02, 0.005), ncol=4, frameon=False, fontsize=9.5)
    ax.text(0.03, -0.025, "边只表示在对应声明／请求名单中公开出现。共同署名、重复出现均不等于稳定联盟；HR-020 名称在决定前不合并。",
            fontsize=10, color="#5A4D3F", transform=ax.transAxes)
    fig.savefig(BIPARTITE_FIG_PATH, dpi=180, bbox_inches="tight", metadata={"Software": "make_r05_coaction_v1.py"})
    plt.close(fig)


def plot_bridges(events: list[dict[str, str]], bridges: list[dict[str, str]]) -> None:
    setup_plot()
    fig = plt.figure(figsize=(16, 13))
    grid = fig.add_gridspec(2, 1, height_ratios=[0.78, 2.22], hspace=0.28)
    ax1 = fig.add_subplot(grid[0])
    ax2 = fig.add_subplot(grid[1])
    event_ids = list(EVENT_META)
    labels = ["2010 WWF 67", "2015 NACSJ 31", "2020 MMC 71"]
    statuses = ["registry_actor_rows", "event_only_name_rows", "alias_pending_rows"]
    status_labels = ["registry actor", "event-only name", "HR-020 pending"]
    colors = ["#236B8E", "#9AA0A6", "#D8842F"]
    left = [0, 0, 0]
    for field, label, color in zip(statuses, status_labels, colors):
        values = [int(event[field]) for event in events]
        ax1.barh(labels, values, left=left, color=color, height=0.58, label=label)
        for idx, (value, start) in enumerate(zip(values, left)):
            if value:
                ax1.text(start + value / 2, idx, str(value), ha="center", va="center", color="white" if color != "#9AA0A6" else "#252525", fontsize=10, weight="bold")
        left = [a + b for a, b in zip(left, values)]
    for idx, event in enumerate(events):
        ax1.text(int(event["structured_participant_count"]) + 1.2, idx, f"n={event['structured_participant_count']}", va="center", fontsize=10, color="#333333")
    ax1.set_xlim(0, 77)
    ax1.set_xlabel("source-list participant rows")
    ax1.set_title("三次事件的身份层构成", loc="left", fontsize=15, weight="bold", color="#17324D")
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.grid(axis="x", color="#D8D3C8", linewidth=0.7, alpha=0.7)
    ax1.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=3, frameon=False)

    xmap = {event_id: idx for idx, event_id in enumerate(event_ids)}
    ax2.set_xlim(-0.08, 2.55)
    ax2.set_ylim(-0.8, len(bridges) - 0.2)
    ax2.invert_yaxis()
    ax2.set_xticks([0, 1, 2], labels)
    ax2.xaxis.tick_top()
    ax2.tick_params(axis="x", labelsize=11, pad=10)
    ax2.set_yticks(range(len(bridges)), [short_label(row["canonical_name"], 35) for row in bridges], fontsize=9.5)
    ax2.spines[:].set_visible(False)
    ax2.grid(axis="x", color="#D8D3C8", linewidth=1.0)
    pattern_colors = {3: "#5B3C88", 2: "#287A72"}
    for idx, bridge in enumerate(bridges):
        xs = [xmap[event_id] for event_id in bridge["event_ids"].split(";")]
        ax2.plot([min(xs), max(xs)], [idx, idx], color=pattern_colors[int(bridge["event_count"])], linewidth=2.1, alpha=0.75)
        ax2.scatter(xs, [idx] * len(xs), s=78, color=pattern_colors[int(bridge["event_count"])], edgecolor="white", linewidth=1.1, zorder=3)
        ax2.text(2.12, idx, f"{bridge['event_count']} events", va="center", fontsize=8.8, color="#4A4A4A")
    ax2.set_title(f"严格身份口径下的重复参与桥梁（{len(bridges)} actors）", loc="left", fontsize=15, weight="bold", color="#17324D", pad=18)

    fig.subplots_adjust(top=0.885, bottom=0.075, left=0.26, right=0.96)
    fig.suptitle("R5 共同行动样本：规模扩大，不等于联盟稳定化", x=0.06, y=0.985, ha="left", fontsize=22, weight="bold", color="#17324D")
    fig.text(0.06, 0.942, "三张一手名单完整结构化；下图只合并当前 registry 已确认身份，HR-020 待审别名不计入桥梁。", fontsize=11.5, color="#4A5560")
    fig.text(0.06, 0.018, "读法：重复出现说明组织把同一议题带入多个公开行动场合；它不能单独证明组织间存在长期联盟、成员关系、资金流或持续协调。", fontsize=10.5, color="#5A4D3F")
    fig.savefig(BRIDGE_FIG_PATH, dpi=180, bbox_inches="tight", metadata={"Software": "make_r05_coaction_v1.py"})
    plt.close(fig)


def build_brief(events: list[dict[str, str]], bridges: list[dict[str, str]], overlaps: list[dict[str, str]], hr_count: int) -> str:
    event_by_id = {row["event_id"]: row for row in events}
    all_three = [row for row in bridges if row["event_count"] == "3"]
    pairs = {(row["event_a"], row["event_b"]): row for row in overlaps}
    all_three_names = "、".join(row["canonical_name"] for row in all_three)
    return dedent(f"""
    # R5 共同行动网络解释性简报 v0

    ## 结论先行

    一期 R5 现已把三张一手名单完整结构化为 **169 条事件参与观察**：2010 WWF Japan 67团体、2015 NACSJ／Peace Boat 31团体、2020 OEJP／MMC 71团体。它们构成的是“组织—事件”二部网络，不是已经被证明的稳定联盟网络。

    当前身份层包括 **{sum(int(row['registry_actor_rows']) for row in events)} 条 registry actor 参与行**、**{sum(int(row['event_only_name_rows']) for row in events)} 条 event-only name** 与 **{sum(int(row['alias_pending_rows']) for row in events)} 条 alias pending**。{hr_count} 个人工问题进入 HR-020，决定栏全部留空；待审名称不参与正式重复桥梁计算。

    ## 三次事件分别说明什么

    - **2010 WWF 67**：环境保全团体把边野古基地争议表达为儒艮、海草藻场、珊瑚、生物多样性、民主程序与生活安全问题，并向首相、防卫大臣、外务大臣提交共同声明。完整名单中 registry／event-only／pending 分别为 {event_by_id['EV2010_WWF_67']['registry_actor_rows']}／{event_by_id['EV2010_WWF_67']['event_only_name_rows']}／{event_by_id['EV2010_WWF_67']['alias_pending_rows']}。
    - **2015 NACSJ 31**：31个团体全部可连接当前 registry，显示和平组织、冲绳现场团体、日本国内环保 NGO 与海外环保组织在同一公开声明中并列出现。该名单证明跨层共同发声，不证明31个团体形成常设组织。
    - **2020 OEJP／MMC 71**：行动对象从日本政府转向美国海洋哺乳动物委员会，行动形式从共同声明转为 request letter 与 civil-society report。71行中 registry／event-only／pending 分别为 {event_by_id['EV2020_OEJP_MMC_71']['registry_actor_rows']}／{event_by_id['EV2020_OEJP_MMC_71']['event_only_name_rows']}／{event_by_id['EV2020_OEJP_MMC_71']['alias_pending_rows']}；这些 event-only names 不自动进入 actor registry。

    ## 可解释的重复参与桥梁

    严格按当前 registry 身份合并后，有 **{len(bridges)} 个 actor** 至少出现在两次样本行动中。其中同时跨越三次事件的有 **{len(all_three)} 个**：{all_three_names}。它们连接了2010国内政府声明、2015跨国 NGO 声明与2020美国行政／科学机构请求，是“议题与行动场域桥梁”的强线索。

    事件两两的已确认 registry actor 重叠为：

    - 2010–2015：{pairs[('EV2010_WWF_67', 'EV2015_NACSJ_31')]['shared_confirmed_registry_actors']} 个；
    - 2010–2020：{pairs[('EV2010_WWF_67', 'EV2020_OEJP_MMC_71')]['shared_confirmed_registry_actors']} 个；
    - 2015–2020：{pairs[('EV2015_NACSJ_31', 'EV2020_OEJP_MMC_71')]['shared_confirmed_registry_actors']} 个。

    这说明样本中的连续性不是“所有签署者都持续协作”，而是少数环保、儒艮、法律与冲绳议题节点反复接入不同规模和对象的公开行动。重复参与仍然只是公开可见的 event-level relation。

    ## 基础问题：现在能回答什么

    1. **谁在同一公开行动中出现？** 可以，三次名单均为全量事件级结构化，不再只展示 registry 中的少数样本。
    2. **行动方式如何变化？** 可以：2010/2015 是共同声明，2020 是面向美国联邦专门机构的请求信与公民社会报告。
    3. **哪些 actor 跨事件重复出现？** 可以，但只对当前 registry 已确认身份给出正式桥梁；待审别名在 HR-020 决定前不合并。
    4. **地方—日本国内—国际层如何同场？** 2015名单最清楚地显示三层并列；2020则显示冲绳／日本团体把诉求送入美国行政／科学监督场域。

    ## 不能回答什么

    - 不能仅凭共同署名证明稳定联盟、正式成员关系、领导—隶属结构、资金关系或持续协调。
    - 不能把所有名单名称都当作具备持续性的 NGO；event-only name 可能是临时委员会、设施、媒体、企业、工会分部或松散行动名。
    - 不能把共同出现次数解释为组织影响力、动员能力或对政策结果的因果贡献。
    - 三次事件是围绕边野古／大浦湾与儒艮的目的性样本，不代表复归后冲绳全部共同行动，也不能据此比较所有议题的联盟密度。

    ## 证据与人工边界

    S003、S004、S005、S006 均已有本地归档。2010 WWF 页面标称67团体，但名单字符串有一处缺分隔符；日本野鸟の会镜像保留相同字符串，故当前按两组织切分并标入 HR020-06，而非由 AI 终审。其余潜在日英别名、三项旧 tentative alias、A106/A110 英文对应和“自然の権利”基金实体边界均在 HR-020 中逐项提出精确问题。

    图和桥梁表只把 `registry_actor` 合并为跨事件 entity；`event_only_name` 不跨语种自动合并，`alias_pending` 更不会提前进入正式桥梁。所有图注均明确：共同署名与重复出现不是稳定联盟。
    """)


def build_readme(events: list[dict[str, str]], bridges: list[dict[str, str]], hr_count: int) -> str:
    return dedent(f"""
    # R05 co-action network v1

    Event-aware co-action package for the original Phase-1 R5 module.

    ## Files

    - `../../data/interim/25_coaction_event_participation_v0.csv` — all {sum(int(row['structured_participant_count']) for row in events)} source-list observations across 67/31/71 events.
    - `event_catalog_v0.csv` — event/action/target/source metadata and identity-layer counts.
    - `actor_event_bipartite_edges_v0.csv` — {sum(int(row['structured_participant_count']) for row in events)} actor/name-to-event edges; no actor-to-actor alliance projection.
    - `repeat_participation_bridges_v0.csv` — {len(bridges)} confirmed current-registry actors appearing in at least two sampled events.
    - `event_overlap_v0.csv` — pairwise overlap using confirmed registry identities only.
    - `source_register_v0.csv` — module-local source locators, archive paths and hashes.
    - `hr020_review_queue_v0.csv` / `HR020_review_packet_v0.md` — {hr_count} unresolved segmentation/alias questions with blank decision fields.
    - `fig_r05_event_bipartite_v0.png` — full event-participant bipartite view; repeated actors labelled, one-off nodes unlabelled.
    - `fig_r05_repeat_bridges_v0.png` — identity composition and readable repeated-participation matrix.
    - `R05_explanatory_brief_v0.md` — what R5 now answers, what it cannot answer, and the mechanism interpretation.
    - `validation_report_v0.md` — generated checks and counts.

    ## Identity rules

    - `registry_actor`: source name is accepted as a match to a current registry actor; only these rows may enter the formal repeated-participation bridge table.
    - `event_only_name`: literal name observed in one source list; it is not silently promoted to the registry or merged across languages.
    - `alias_pending`: possible alias, translation, entity boundary or source-name segmentation requiring HR-020. It remains event-specific until a human decision.

    ## Relation rule

    Every edge is an event participation observation. `repeated_public_participation_*` means repeated appearance across the three sampled actions only. It does not mean stable alliance, membership, funding, hierarchy or continuing coordination.

    Rebuild with:

    ```powershell
    python scripts\\make_r05_coaction_v1.py
    ```
    """)


def validate(rows: list[dict[str, str]], events: list[dict[str, str]], edges: list[dict[str, str]],
             bridges: list[dict[str, str]], overlaps: list[dict[str, str]], sources: list[dict[str, str]],
             queue: list[dict[str, str]], registry: dict[str, dict[str, str]], raw_count_2010: int) -> list[str]:
    checks = []
    expected = {"EV2010_WWF_67": 67, "EV2015_NACSJ_31": 31, "EV2020_OEJP_MMC_71": 71}
    counts = Counter(row["event_id"] for row in rows)
    if counts != Counter(expected):
        raise AssertionError(f"Event counts mismatch: {counts}")
    checks.append("event counts exact: 67 / 31 / 71 = 169")
    if raw_count_2010 != 66:
        raise AssertionError("2010 raw comma split should be 66 before pending segmentation")
    segmentation_rows = [row for row in rows if row["event_observation_status"] == "needs_human_review_source_segmentation"]
    if len(segmentation_rows) != 2 or {row["hr020_queue_ids"] for row in segmentation_rows} != {"HR020-06"}:
        raise AssertionError("Only the two HR020-06 rows may have pending source segmentation")
    checks.append("2010 source anomaly retained: 66 comma tokens, 67 structured rows, HR020-06 pending")
    if len({row["participant_key"] for row in rows}) != 169:
        raise AssertionError("Participant keys must be unique")
    for event_id in expected:
        names = [row["source_name"] for row in rows if row["event_id"] == event_id]
        if len(names) != len(set(names)):
            raise AssertionError(f"Duplicate source name within {event_id}")
    checks.append("participant keys and within-event source names unique")
    if len(edges) != 169 or len({row["edge_id"] for row in edges}) != 169:
        raise AssertionError("Bipartite edge count/id uniqueness failed")
    checks.append("bipartite edges exact: 169")
    for row in rows:
        if row["actor_id"] and row["actor_id"] not in registry:
            raise AssertionError(f"Unknown actor id {row['actor_id']}")
        if row["identity_status"] not in {"registry_actor", "event_only_name", "alias_pending"}:
            raise AssertionError(f"Invalid identity status {row['identity_status']}")
        if row["identity_status"] == "alias_pending" and not row["hr020_queue_ids"]:
            raise AssertionError(f"Pending row lacks HR-020 id: {row['participant_key']}")
        if row["identity_status"] != "registry_actor" and row["actor_id"]:
            raise AssertionError("Only confirmed registry_actor rows may carry actor_id")
    checks.append("identity statuses exclusive; actor ids only on confirmed registry matches")
    decision_fields = ["decision", "human_reviewer", "review_date", "decision_note"]
    if len(queue) != 14:
        raise AssertionError(f"HR-020 count changed: {len(queue)}")
    if any(row[field].strip() for row in queue for field in decision_fields):
        raise AssertionError("HR-020 decision fields must remain blank")
    participant_keys = {row["participant_key"] for row in rows}
    for item in queue:
        if not set(item["participant_keys"].split(";")) <= participant_keys:
            raise AssertionError(f"HR-020 participant FK failed: {item['queue_id']}")
    checks.append("HR-020 exact: 14 questions; decision fields blank; participant FKs valid")
    if any(int(row["event_count"]) < 2 for row in bridges):
        raise AssertionError("Bridge table contains a single-event actor")
    bridge_actor_ids = {row["actor_id"] for row in bridges}
    pending_candidates = {row["candidate_actor_id"] for row in queue if row["candidate_actor_id"]}
    if bridge_actor_ids & pending_candidates and any(
        item["candidate_actor_id"] in bridge_actor_ids and item["queue_id"] in {"HR020-01", "HR020-02", "HR020-03", "HR020-04", "HR020-05"}
        for item in queue
    ):
        # Candidate actors may already bridge through other accepted events; the pending row itself must not be counted.
        for item in queue:
            candidate = item["candidate_actor_id"]
            if not candidate:
                continue
            pending_keys = set(item["participant_keys"].split(";"))
            if any(row["participant_key"] in pending_keys and row["actor_id"] for row in rows):
                raise AssertionError(f"Pending candidate was prematurely merged: {item['queue_id']}")
    checks.append(f"repeat bridge table conservative: {len(bridges)} confirmed actors; pending identities excluded")
    if len(overlaps) != 3:
        raise AssertionError("Expected three pairwise overlap rows")
    checks.append("three pairwise event overlaps generated from confirmed registry identities")
    for source in sources:
        if source["existing_source_id"]:
            local = ROOT / source["local_path"]
            if not local.exists():
                raise AssertionError(f"Missing archived source {local}")
            digest = hashlib.sha256(local.read_bytes()).hexdigest()
            if digest != source["sha256"]:
                raise AssertionError(f"Archive hash mismatch for {source['source_ref']}")
    checks.append("S003-S006 archive paths and SHA-256 hashes verified")
    for path in [BIPARTITE_FIG_PATH, BRIDGE_FIG_PATH]:
        if not path.exists() or path.stat().st_size < 80_000:
            raise AssertionError(f"Figure missing or too small: {path}")
    checks.append("two PNG figures generated and nontrivial in size")
    return checks


def build_validation_report(checks: list[str], rows: list[dict[str, str]], events: list[dict[str, str]],
                            bridges: list[dict[str, str]], queue: list[dict[str, str]]) -> str:
    identity = Counter(row["identity_status"] for row in rows)
    observations = Counter(row["event_observation_status"] for row in rows)
    header = dedent(f"""
    # R05 validation report v0

    - Events: {len(events)}
    - Participation observations / bipartite edges: {len(rows)}
    - Event observation status: accepted={observations['accepted_source_list_observation']}; source_segmentation_pending={observations['needs_human_review_source_segmentation']}
    - Identity rows: registry_actor={identity['registry_actor']}; event_only_name={identity['event_only_name']}; alias_pending={identity['alias_pending']}
    - Confirmed repeat-participation bridges: {len(bridges)}
    - HR-020 questions: {len(queue)}; all decision/reviewer/date/note fields blank

    ## Checks
    """)
    footer = dedent("""
    ## Interpretation assertion

    The package contains event-to-participant observations and repeated-public-participation indicators only. It contains no actor-to-actor stable-alliance edge and does not infer membership, funding, hierarchy or continuous coordination from co-signing.
    """)
    return header + "\n" + "\n".join(f"- PASS — {check}" for check in checks) + "\n\n" + footer


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    registry = {row["actor_id"]: row for row in read_csv(REGISTRY_PATH)}
    rows, raw_count_2010 = build_participation(registry)
    events = build_events(rows)
    edges = build_bipartite(rows)
    bridges = build_bridges(rows, registry)
    overlaps = build_overlap(rows)
    sources = build_sources()
    queue = build_hr020(rows)

    write_csv(PARTICIPATION_PATH, PARTICIPATION_FIELDS, rows)
    write_csv(EVENT_PATH, EVENT_FIELDS, events)
    write_csv(BIPARTITE_PATH, BIPARTITE_FIELDS, edges)
    write_csv(BRIDGE_PATH, BRIDGE_FIELDS, bridges)
    write_csv(OVERLAP_PATH, OVERLAP_FIELDS, overlaps)
    write_csv(SOURCE_PATH, SOURCE_FIELDS, sources)
    write_csv(HR020_PATH, HR020_FIELDS, queue)
    write_text(HR020_PACKET_PATH, build_hr020_packet(queue))
    write_text(BRIEF_PATH, build_brief(events, bridges, overlaps, len(queue)))
    write_text(README_PATH, build_readme(events, bridges, len(queue)))
    plot_bipartite(rows, bridges)
    plot_bridges(events, bridges)
    checks = validate(rows, events, edges, bridges, overlaps, sources, queue, registry, raw_count_2010)
    write_text(VALIDATION_PATH, build_validation_report(checks, rows, events, bridges, queue))

    identity = Counter(row["identity_status"] for row in rows)
    print(
        "R05 generated: "
        f"{len(rows)} participation rows; registry/event-only/pending="
        f"{identity['registry_actor']}/{identity['event_only_name']}/{identity['alias_pending']}; "
        f"{len(bridges)} repeat bridges; HR-020={len(queue)}."
    )


if __name__ == "__main__":
    main()
