from __future__ import annotations

"""Build the R3 actor--place semantic layer and Sakishima dossiers.

The generator is deliberately non-mutating: it reads the current central
tables but writes only the derived R3 candidate table and module package.  A
semantic label is not a human confirmation of the underlying edge.  The
original evidence level and review status are therefore retained separately,
and all semantic decisions that cannot be frozen mechanically are routed to
HR-025 with blank seed fields.  If reviewers have already populated the task
book, reruns preserve those human fields by stable ``object_id`` instead of
silently resetting them.
"""

import csv
import hashlib
import html
import textwrap
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "R03_spatial_dossier_v1"

ACTORS = DATA / "01_actor_registry_initial_v0.csv"
PLACES = DATA / "04_place_registry_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"
EDGES = DATA / "08_actor_place_edges_initial_v0.csv"
ARCHIVE = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
R4_MATRIX = ROOT / "outputs" / "R04_sakishima_frame_corpus_v0" / "three_place_safe_source_matrix_v0.csv"
R4_SOURCES = ROOT / "outputs" / "R04_sakishima_frame_corpus_v0" / "online_evidence_safe_sources_v0.csv"
R9_CASES = ROOT / "outputs" / "R09_referendum_process_v0" / "case_summary_v0.csv"
R9_STAGES = ROOT / "outputs" / "R09_referendum_process_v0" / "process_stages_reviewed_all_v0.csv"
R9_SOURCES = ROOT / "outputs" / "R09_referendum_process_v0" / "source_register_v0.csv"

DERIVED = DATA / "32_actor_place_semantic_candidates_v1.csv"
SUMMARY = OUT / "actor_place_semantic_summary_v1.csv"
DOSSIER = OUT / "sakishima_actor_place_dossier_v1.csv"
SOURCE_CROSSWALK = OUT / "source_crosswalk_v1.csv"
HR025 = OUT / "HR025_actor_place_semantics_review_v0.csv"
BRIEF = OUT / "R03_spatial_dossier_brief_v1.md"
README = OUT / "README.md"
VALIDATION = OUT / "validation_report_v1.md"

FIG1_PNG = OUT / "fig1_full_actor_place_semantic_matrix_v1.png"
FIG1_SVG = OUT / "fig1_full_actor_place_semantic_matrix_v1.svg"
FIG1_HTML = OUT / "fig1_full_actor_place_semantic_matrix_v1.html"
FIG2_PNG = OUT / "fig2_spatial_relation_type_composition_v1.png"
FIG2_SVG = OUT / "fig2_spatial_relation_type_composition_v1.svg"
FIG2_HTML = OUT / "fig2_spatial_relation_type_composition_v1.html"
FIG3_PNG = OUT / "fig3_sakishima_actor_place_dossiers_v1.png"
FIG3_SVG = OUT / "fig3_sakishima_actor_place_dossiers_v1.svg"
FIG3_HTML = OUT / "fig3_sakishima_actor_place_dossiers_v1.html"

HUMAN_EDGE_STATUSES = {"human_checked", "human_revised"}
VALID_SEMANTICS = {
    "headquarters",
    "site_presence",
    "event_site",
    "advocacy_target",
    "institutional_venue",
    "unclear",
}

HR025_HUMAN_FIELDS = (
    "final_semantic",
    "decision",
    "human_reviewer",
    "review_date",
    "review_note",
)

SEMANTIC_CN = {
    "headquarters": "总部／办公室",
    "site_presence": "持续活动／服务在场",
    "event_site": "事件／程序场域",
    "advocacy_target": "倡议／争议对象",
    "institutional_venue": "制度／机构场域",
    "unclear": "语义未明",
}

SEMANTIC_COLORS = {
    "headquarters": "#355C7D",
    "site_presence": "#2C7A6B",
    "event_site": "#D47A35",
    "advocacy_target": "#A4484D",
    "institutional_venue": "#725A9A",
    "unclear": "#8A9197",
}

# The six sets are an auditable candidate coding of every current AP edge.
# They classify how the place is used in the edge text, not whether the edge is
# true.  The exhaustive validation below prevents row loss or silent defaults.
SEMANTIC_EDGE_SETS = {
    "advocacy_target": set(
        """AP001 AP002 AP003 AP004 AP006 AP007 AP008 AP009 AP010 AP011
        AP012 AP013 AP014 AP020 AP023 AP025 AP027 AP028 AP050 AP051 AP053
        AP054 AP055 AP057 AP058 AP059 AP061 AP062 AP063 AP064 AP065 AP066
        AP067 AP068 AP069 AP070 AP071 AP072 AP073 AP074 AP075 AP076 AP077
        AP078 AP080 AP086 AP087 AP089 AP090 AP098 AP100 AP101 AP102 AP103
        AP104 AP109 AP111 AP113 AP128 AP129 AP132""".split()
    ),
    "site_presence": set(
        """AP015 AP017 AP018 AP021 AP022 AP024 AP026 AP029 AP030 AP031
        AP032 AP033 AP034 AP037 AP038 AP039 AP040 AP041 AP042 AP044 AP081
        AP092 AP097 AP099 AP106 AP107 AP108 AP114 AP115 AP116 AP117 AP118
        AP122 AP123 AP125 AP126 AP127 AP130 AP131 AP135""".split()
    ),
    "event_site": set("AP016 AP019 AP085 AP095 AP112 AP134".split()),
    "headquarters": set("AP079 AP082 AP084 AP120 AP133".split()),
    "institutional_venue": set("AP043 AP045 AP047 AP083 AP119 AP121".split()),
    "unclear": set(
        """AP005 AP035 AP036 AP046 AP048 AP049 AP052 AP056 AP060 AP088
        AP091 AP093 AP094 AP096 AP105 AP110 AP124""".split()
    ),
}

# These rows have a plausible semantic candidate, but the present relation
# text cannot distinguish two nearby meanings without a human reading.  All
# `unclear` rows are added automatically.
AMBIGUOUS_EDGE_IDS = set(
    """AP022 AP024 AP029 AP037 AP038 AP040 AP044 AP081 AP085 AP092 AP095
    AP097 AP099 AP106 AP107 AP108 AP114 AP115 AP116 AP117 AP118 AP122 AP123
    AP125 AP130 AP131 AP132 AP133 AP134 AP135""".split()
)

PLACE_ORDER = [
    "P001", "P020", "P017", "P002", "P003", "P006", "P016", "P019",
    "P004", "P010", "P018", "P005", "P007", "P008", "P009", "P011",
    "P012", "P013", "P014", "P015",
]

PLACE_LABELS = {
    "P001": "冲绳全县",
    "P020": "那霸",
    "P017": "名护",
    "P002": "边野古",
    "P003": "大浦湾",
    "P006": "Camp Schwab",
    "P016": "高江",
    "P019": "泡濑",
    "P004": "普天间",
    "P010": "MCAS Futenma",
    "P018": "宜野湾",
    "P005": "嘉手纳",
    "P007": "Camp Foster",
    "P008": "Camp Hansen",
    "P009": "Camp Kinser",
    "P011": "与那国",
    "P012": "石垣",
    "P013": "宫古",
    "P014": "JICA Okinawa",
    "P015": "美国总领馆",
}

DOSSIER_PLACES = {
    "P011": ("Yonaguni", "与那国"),
    "P012": ("Ishigaki", "石垣"),
    "P013": ("Miyako", "宫古"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def normalize_generated_svg(path: Path) -> None:
    """Remove Matplotlib path-line trailing spaces deterministically."""
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip(" \t") for line in lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def configure_fonts() -> None:
    candidates = [
        "Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC",
        "Noto Sans CJK JP", "SimHei", "Arial Unicode MS", "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["svg.hashsalt"] = "r03-spatial-dossier-v1"


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def short(value: str, width: int) -> str:
    return value if len(value) <= width else value[: width - 1] + "…"


def semantic_for_edge(edge_id: str) -> str:
    found = [semantic for semantic, ids in SEMANTIC_EDGE_SETS.items() if edge_id in ids]
    if len(found) != 1:
        raise ValueError(f"{edge_id} must have exactly one semantic candidate; found {found}")
    return found[0]


def semantic_basis(semantic: str) -> str:
    return {
        "headquarters": "edge text explicitly locates a headquarters, office, or organizational base",
        "site_presence": "edge text describes recurring activity, service, chapter, monitoring, or local organizational presence",
        "event_site": "edge text locates a bounded referendum, campaign, request, or mobilization process",
        "advocacy_target": "place is the object or issue geography of advocacy, litigation, statement, or solidarity",
        "institutional_venue": "place functions as an administrative, service, grant, or institutional channel",
        "unclear": "current edge text does not distinguish location, scope, target, or relation venue",
    }[semantic]


def interpretation_limit(edge: dict[str, str], semantic: str, place_match: bool) -> str:
    base = {
        "headquarters": "候选仅表示总部／办公室位置；不外推组织在全地理范围的活动或政治代表性。",
        "site_presence": "候选仅表示公开活动、服务或网络节点在场；不等于总部、法定登记地、稳定联盟或政治立场。",
        "event_site": "候选仅表示特定活动／公投／程序的发生场域；不外推为长期据点或持续组织能力。",
        "advocacy_target": "地点是公开诉求、声明、诉讼或声援的对象；不证明组织在当地设点、驻在或结盟。",
        "institutional_venue": "地点是制度／服务／行政渠道；不等于与场所拥有者结盟、获资助或共享政治立场。",
        "unclear": "当前关系文本不足以安全区分总部、持续在场、事件场域、倡议对象或制度场域。",
    }[semantic]
    special = {
        "AP012": "HR-002 已限定为声明／声援语境，不是现场在场。",
        "AP020": "HR-003 指出该意见广告委员会主要由八重山／石垣侧推动；与那国是议题对象，不是办公室位置。",
        "AP029": "现有备注明确要求核实 Camp Schwab 的具体 USO 中心／项目。",
        "AP035": "对 USO Okinawa 的捐赠不能反向证明赞助者总部或实体据点在 P001。",
        "AP036": "赞助名单只能证明项目语境，不能定位赞助者自身。",
        "AP046": "TOMODACHI 的冲绳特定连接尚未确认。",
        "AP047": "NOFO／grant opportunity 只证明机会及发布场域，不证明受款者。",
        "AP048": "NED 仅为 watchlist，未确认冲绳 recipient。",
        "AP049": "Peace Winds Japan 的冲绳连接未确认。",
        "AP088": "相邻受影响地区与原告团组织据点不能相互替代。",
        "AP105": "‘Okinawa node’ 仍需第二来源，不能先写成正式分支。",
        "AP110": "在冲绳开展活动不等于在那霸设办公室。",
        "AP123": "输入存在键值冲突：P006 在 place registry 是 Camp Schwab，但本行 place_name 写 Camp Foster；不得静默选择其一。",
        "AP124": "Torii Station／基地特定性仍需独立来源。",
        "AP125": "HR-013 只支持全县性活动场域；不得推定具体市町总部或据点。",
        "AP126": "HR-011 只支持沖縄YWCA的全县活动场域；不得推定具体总部、边野古现场在场或稳定联盟。",
        "AP127": "HR-011 只支持全县网络与公共动员场域；63 团体／个人构成不自动生成稳定联盟边。",
        "AP128": "嘉手纳是第四次爆音诉讼的案件／受影响场域，不是律师团办公室位置。",
        "AP129": "边野古是大阪声援行动的倡议对象，不是冲绳本地据点或现场在场。",
    }.get(edge["edge_id"], "")
    integrity = "" if place_match else " 地点键值冲突在人工确认前保持显式。"
    return " ".join(part for part in [base, special, integrity] if part).strip()


def build_semantic_rows(
    edges: list[dict[str, str]],
    actors_by_id: dict[str, dict[str, str]],
    places_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for edge in edges:
        actor = actors_by_id.get(edge["actor_id"])
        place = places_by_id.get(edge["place_id"])
        if not actor:
            raise ValueError(f"unknown actor in {edge['edge_id']}: {edge['actor_id']}")
        if not place:
            raise ValueError(f"unknown place in {edge['edge_id']}: {edge['place_id']}")
        semantic = semantic_for_edge(edge["edge_id"])
        place_match = edge["place_name"] == place["place_name"]
        needs_review = semantic == "unclear" or edge["edge_id"] in AMBIGUOUS_EDGE_IDS or not place_match
        edge_human = edge["review_status"] in HUMAN_EDGE_STATUSES
        dossier = DOSSIER_PLACES.get(edge["place_id"], ("", ""))[0]
        rows.append({
            "edge_id": edge["edge_id"],
            "actor_id": edge["actor_id"],
            "actor_name": actor["canonical_name"],
            "actor_class": actor["actor_class"],
            "actor_origin_type": actor["origin_type"],
            "actor_review_status": actor["review_status"],
            "place_id": edge["place_id"],
            "place_name_original": edge["place_name"],
            "place_name_registry": place["place_name"],
            "place_type": place["place_type"],
            "place_region": place["region"],
            "place_name_integrity": "match" if place_match else "id_name_mismatch",
            "relation_basis_original": edge["relation_basis"],
            "semantic_candidate_v1": semantic,
            "semantic_candidate_zh": SEMANTIC_CN[semantic],
            "semantic_classification_basis": semantic_basis(semantic),
            "semantic_confidence": "low" if semantic == "unclear" or not place_match else "medium" if needs_review else "high",
            "semantic_freeze_status": "needs_human_semantic_review" if needs_review else "mechanically_classified_candidate",
            "semantic_review_status": "ai_seeded_candidate",
            "source_ref_original": edge["source_ref"],
            "evidence_level_original": edge["evidence_level"],
            "edge_review_status_original": edge["review_status"],
            "edge_review_layer": "human_reviewed_edge" if edge_human else "candidate_edge",
            "dossier_place": dossier,
            "interpretation_limit": interpretation_limit(edge, semantic, place_match),
            "notes_original": edge["notes"],
        })
    return rows


def build_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_semantic: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_semantic[str(row["semantic_candidate_v1"])].append(row)
    output: list[dict[str, object]] = []
    order = ["advocacy_target", "site_presence", "institutional_venue", "event_site", "headquarters", "unclear"]
    for semantic in order:
        items = by_semantic[semantic]
        output.append({
            "semantic_candidate_v1": semantic,
            "semantic_candidate_zh": SEMANTIC_CN[semantic],
            "edge_count": len(items),
            "human_reviewed_edge_count": sum(r["edge_review_layer"] == "human_reviewed_edge" for r in items),
            "candidate_edge_count": sum(r["edge_review_layer"] == "candidate_edge" for r in items),
            "E4_count": sum(r["evidence_level_original"] == "E4" for r in items),
            "E3_count": sum(r["evidence_level_original"] == "E3" for r in items),
            "E2_count": sum(r["evidence_level_original"] == "E2" for r in items),
            "needs_human_semantic_review_count": sum(r["semantic_freeze_status"] == "needs_human_semantic_review" for r in items),
            "interpretation_limit": "Counts describe coded actor--place rows in the current public-source sample, not real-world organizational density.",
        })
    return output


def build_hr025(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        if row["semantic_freeze_status"] != "needs_human_semantic_review":
            continue
        candidate = str(row["semantic_candidate_v1"])
        output.append({
            "task_id": f"HR025-{row['edge_id']}",
            "object_id": row["edge_id"],
            "actor_id": row["actor_id"],
            "actor_name": row["actor_name"],
            "place_id": row["place_id"],
            "place_name_original": row["place_name_original"],
            "place_name_registry": row["place_name_registry"],
            "relation_basis_original": row["relation_basis_original"],
            "candidate_semantic_v1": candidate,
            "review_question": (
                "请在 headquarters/site_presence/event_site/advocacy_target/"
                "institutional_venue/unclear 中确认；同时核查地点键与来源是否足以支持该语义。"
            ),
            "source_ref_original": row["source_ref_original"],
            "evidence_level_original": row["evidence_level_original"],
            "edge_review_status_original": row["edge_review_status_original"],
            "interpretation_limit": row["interpretation_limit"],
            "final_semantic": "",
            "decision": "",
            "human_reviewer": "",
            "review_date": "",
            "review_note": "",
        })
    return output


def preserve_hr025_human_fields(
    seed_rows: list[dict[str, object]],
    existing_path: Path,
) -> list[dict[str, object]]:
    """Carry completed review fields forward by the stable AP object ID.

    A populated task that disappears from the regenerated seed set is a hard
    error: silently dropping it would be equivalent to deleting human work.
    """
    if not existing_path.exists():
        return seed_rows

    existing_rows = read_csv(existing_path)
    existing_by_object: dict[str, dict[str, str]] = {}
    for row in existing_rows:
        object_id = row.get("object_id", "").strip()
        if not object_id:
            raise ValueError("existing HR025 row lacks object_id")
        if object_id in existing_by_object:
            raise ValueError(f"duplicate existing HR025 object_id: {object_id}")
        missing = [field for field in HR025_HUMAN_FIELDS if field not in row]
        if missing:
            raise ValueError(f"existing HR025 schema lacks human fields: {missing}")
        existing_by_object[object_id] = row

    seed_ids = {str(row["object_id"]) for row in seed_rows}
    populated_orphans = [
        object_id
        for object_id, row in existing_by_object.items()
        if object_id not in seed_ids
        and any(row[field].strip() for field in HR025_HUMAN_FIELDS)
    ]
    if populated_orphans:
        raise ValueError(
            "regenerated HR025 would drop populated review objects: "
            + ";".join(sorted(populated_orphans))
        )

    for row in seed_rows:
        object_id = str(row["object_id"])
        existing = existing_by_object.get(object_id)
        if not existing:
            continue
        for field in HR025_HUMAN_FIELDS:
            row[field] = existing[field]
    return seed_rows


def build_source_crosswalk(
    rows: list[dict[str, object]],
    sources_by_id: dict[str, dict[str, str]],
    archive_by_id: dict[str, dict[str, str]],
    actors_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        for ref in split_refs(str(row["source_ref_original"])):
            source = sources_by_id.get(ref, {})
            archived = archive_by_id.get(ref, {})
            actor_ref = actors_by_id.get(ref, {})
            output.append({
                "usage_scope": "actor_place_edge",
                "usage_object_id": row["edge_id"],
                "place": row["place_name_registry"],
                "reference_id": ref,
                "existing_main_source_id": ref if source else "",
                "reference_kind": "main_source_id" if source else "legacy_actor_or_placeholder_ref" if actor_ref or ref.startswith("X") else "unresolved_ref",
                "title": source.get("title", actor_ref.get("canonical_name", "")),
                "url": source.get("url", ""),
                "source_type": source.get("source_type", ""),
                "evidence_level": source.get("evidence_level", str(row["evidence_level_original"])),
                "review_status": source.get("review_status", "not_in_main_source_log"),
                "archive_status": archived.get("archive_status", "not_in_archive_manifest"),
                "supports_or_relation_basis": row["relation_basis_original"],
                "interpretation_limit": "Source/ref inclusion preserves provenance only; it does not approve the edge or semantic candidate.",
            })

    # R4 sources are contextual dossier evidence, never a substitute for an
    # actor--place edge or a stable organizational relation.
    for source in read_csv(R4_SOURCES):
        place = source["place"]
        if place not in {"Yonaguni", "Ishigaki", "Miyako", "Sakishima"}:
            continue
        main_id = source.get("existing_source_id", "")
        archived = archive_by_id.get(main_id, {}) if main_id else {}
        output.append({
            "usage_scope": "r4_sakishima_frame_context",
            "usage_object_id": source["corpus_source_id"],
            "place": place,
            "reference_id": source["corpus_source_id"],
            "existing_main_source_id": main_id,
            "reference_kind": "module_source_with_main_crosswalk" if main_id else "module_local_source",
            "title": source["title"],
            "url": source["url"],
            "source_type": source["source_type"],
            "evidence_level": source["evidence_level"],
            "review_status": source["review_status"],
            "archive_status": archived.get("archive_status", "module_source_not_in_main_archive"),
            "supports_or_relation_basis": source["paraphrase_zh"],
            "interpretation_limit": source["interpretation_limit"],
        })

    case_place = {
        row["case_id"]: row["place"]
        for row in read_csv(R9_CASES)
        if row["place"] in {"Yonaguni", "Ishigaki"}
    }
    for source in read_csv(R9_SOURCES):
        if source.get("disposition") != "accepted" or source["case_id"] not in case_place:
            continue
        main_id = source.get("existing_source_id", "")
        archived = archive_by_id.get(main_id, {}) if main_id else {}
        output.append({
            "usage_scope": "r9_referendum_process_context",
            "usage_object_id": source["case_id"],
            "place": case_place[source["case_id"]],
            "reference_id": source["source_id"],
            "existing_main_source_id": main_id,
            "reference_kind": "module_source_with_main_crosswalk" if main_id else "module_local_source",
            "title": source["title"],
            "url": source["url"],
            "source_type": source["source_type"],
            "evidence_level": source["evidence_level"],
            "review_status": source["review_status"],
            "archive_status": archived.get("archive_status", "module_source_not_in_main_archive"),
            "supports_or_relation_basis": source["supports"],
            "interpretation_limit": source.get("interpretation_limit", "") or "Process evidence does not establish organizational continuity or electoral causality.",
        })
    return output


def build_dossier(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    frame_rows = read_csv(R4_MATRIX)
    frames_by_place: dict[str, list[dict[str, str]]] = defaultdict(list)
    for frame in frame_rows:
        frames_by_place[frame["place"]].append(frame)

    cases_by_place = {row["place"]: row for row in read_csv(R9_CASES) if row["place"] in {"Yonaguni", "Ishigaki"}}
    accepted_stage_counts = Counter(
        row["place"]
        for row in read_csv(R9_STAGES)
        if row["review_status"] == "accepted" and row["place"] in {"Yonaguni", "Ishigaki"}
    )

    output: list[dict[str, object]] = []
    for row in rows:
        place_en = str(row["dossier_place"])
        if not place_en:
            continue
        frame_bits = []
        for frame in sorted(frames_by_place[place_en], key=lambda x: (-int(x["safe_source_count"]), x["frame_label"])):
            frame_bits.append(f"{frame['frame_label_zh']}={frame['safe_source_count']}")
        case = cases_by_place.get(place_en, {})
        if row["edge_review_layer"] == "human_reviewed_edge" and row["evidence_level_original"] in {"E3", "E4"}:
            fact_layer = "human_reviewed_actor_place_edge"
        elif row["edge_review_status_original"] in {"needs_local_retrieval", "needs_second_source"}:
            fact_layer = "candidate_with_explicit_evidence_gap"
        else:
            fact_layer = "source_backed_candidate_edge"

        local_gap = {
            "A014": "需八重山／与那国地方材料确认执委会正式名称、代表与持续性。",
            "A015": "需意见广告实物或八重山报刊确认组织层身份；与那国仅为声援对象。",
            "A016": "活动及组织已交叉支持；成立、代表、持续组织细节仍需当地材料。",
            "A065": "需独立来源确认三岛节点、成员关系与持续性。",
            "A012": "需核正式全称、持续性及与其他宫古地下水组织的关系。",
        }.get(str(row["actor_id"]), "当前无需由本空间语义包新增当地任务；先完成人工语义／边级复核。")

        place_guardrail = {
            "Yonaguni": "主框架为前线／台湾邻近、自治／公投与生命安全；本包不将其强行环境化。",
            "Ishigaki": "自治程序、反部署与生活安全分层；地下水线索不能从宫古类推。",
            "Miyako": "地下水／饮用水是地方生活条件；一般环保活动不能自动写成反部署。",
        }[place_en]
        output.append({
            "place": place_en,
            "place_zh": DOSSIER_PLACES[str(row["place_id"])][1],
            "edge_id": row["edge_id"],
            "actor_id": row["actor_id"],
            "actor_name": row["actor_name"],
            "actor_class": row["actor_class"],
            "semantic_candidate_v1": row["semantic_candidate_v1"],
            "semantic_candidate_zh": row["semantic_candidate_zh"],
            "fact_layer": fact_layer,
            "evidence_level_original": row["evidence_level_original"],
            "edge_review_status_original": row["edge_review_status_original"],
            "source_ref_original": row["source_ref_original"],
            "r4_safe_source_visibility": ";".join(frame_bits),
            "r4_measurement_limit": "bounded QA-safe online excerpts; counts are not local prevalence",
            "r9_case_id": case.get("case_id", ""),
            "r9_accepted_stage_count": accepted_stage_counts.get(place_en, 0),
            "r9_mechanism_summary": case.get("mechanism_summary", "当前 R9 正式包未建立该地公投案例链；这只是模块范围边界。"),
            "candidate_explanation": row["interpretation_limit"],
            "local_retrieval_gap": local_gap,
            "place_guardrail": place_guardrail,
        })
    return output


def save_figure(fig: plt.Figure, png: Path, svg: Path) -> None:
    fig.savefig(
        png,
        dpi=180,
        bbox_inches="tight",
        facecolor="white",
        metadata={"Software": "make_r03_spatial_dossier_v1.py"},
    )
    fig.savefig(
        svg,
        bbox_inches="tight",
        facecolor="white",
        metadata={"Date": None, "Creator": "make_r03_spatial_dossier_v1.py"},
    )
    plt.close(fig)


def html_wrapper(svg_name: str, title: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>body{{margin:0;background:#eceae4;font-family:'Microsoft YaHei',sans-serif}}main{{max-width:1800px;margin:24px auto;background:white;box-shadow:0 8px 28px #0002}}img{{display:block;width:100%;height:auto}}</style></head>
<body><main><img src="{html.escape(svg_name)}" alt="{html.escape(title)}"></main></body></html>"""


def plot_full_matrix(rows: list[dict[str, object]]) -> None:
    place_index = {place_id: index for index, place_id in enumerate(PLACE_ORDER)}
    by_actor: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_actor[str(row["actor_id"])].append(row)
    actor_order = sorted(
        by_actor,
        key=lambda actor_id: (
            min(place_index[str(r["place_id"])] for r in by_actor[actor_id]),
            actor_id.startswith("X"),
            actor_id,
        ),
    )
    actor_index = {actor_id: index for index, actor_id in enumerate(actor_order)}

    fig, ax = plt.subplots(figsize=(22, 31))
    ax.set_facecolor("#FBFAF7")
    for x in range(len(PLACE_ORDER)):
        if x % 2:
            ax.axvspan(x - 0.5, x + 0.5, color="#F1F0EC", zorder=0)
    ax.axvspan(place_index["P011"] - 0.5, place_index["P013"] + 0.5, color="#E8F2EF", alpha=0.65, zorder=0)

    sizes = {"E2": 44, "E3": 62, "E4": 82}
    for row in rows:
        x = place_index[str(row["place_id"])]
        y = actor_index[str(row["actor_id"])]
        semantic = str(row["semantic_candidate_v1"])
        color = SEMANTIC_COLORS[semantic]
        size = sizes.get(str(row["evidence_level_original"]), 46)
        if row["place_name_integrity"] != "match":
            ax.scatter(x, y, s=size * 1.45, marker="D", facecolors="none", edgecolors="#C62027", linewidths=2.1, zorder=5)
        elif row["edge_review_layer"] == "human_reviewed_edge":
            ax.scatter(x, y, s=size, marker="o", facecolors=color, edgecolors="#1F2D29", linewidths=0.8, zorder=4)
        else:
            ax.scatter(x, y, s=size, marker="o", facecolors="white", edgecolors=color, linewidths=1.5, zorder=3)

    actor_names = {
        str(row["actor_id"]): str(row["actor_name"])
        for row in rows
    }
    ax.set_yticks(range(len(actor_order)))
    ax.set_yticklabels([f"{actor_id}  {short(actor_names[actor_id], 31)}" for actor_id in actor_order], fontsize=7.6)
    ax.set_xticks(range(len(PLACE_ORDER)))
    ax.set_xticklabels([PLACE_LABELS[p] for p in PLACE_ORDER], rotation=52, ha="right", fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(-0.65, len(PLACE_ORDER) - 0.35)
    ax.set_ylim(len(actor_order) - 0.4, -1.6)
    ax.grid(axis="y", color="#E4E3DE", linewidth=0.34)
    ax.grid(axis="x", color="#D7D5CF", linewidth=0.6)
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle(f"R3 全量组织 × 地点空间关系（{len(rows)} 条候选／人审边）", x=0.12, y=0.995, ha="left", fontsize=22, fontweight="bold")
    fig.text(
        0.12, 0.982,
        "每个点对应中央 actor–place 表的一条边；实心＝底层边已人审，空心＝候选边；颜色＝空间语义候选，大小＝E2/E3/E4。语义候选本身尚未人审。",
        ha="left", va="top", fontsize=10.5, color="#4D5955",
    )
    fig.text(
        0.78, 0.982,
        "绿色底纹：先岛三地",
        ha="left", va="top", fontsize=10.5, color="#2C6A60",
    )

    semantic_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor=SEMANTIC_COLORS[s], markeredgewidth=1.8, markersize=8, label=SEMANTIC_CN[s])
        for s in ["advocacy_target", "site_presence", "event_site", "headquarters", "institutional_venue", "unclear"]
    ]
    layer_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#456E68", markeredgecolor="#1F2D29", markersize=8, label="底层边已人审"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor="#456E68", markeredgewidth=1.7, markersize=8, label="底层候选边"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor="white", markeredgecolor="#C62027", markeredgewidth=1.8, markersize=8, label="地点键冲突"),
    ]
    first = ax.legend(handles=semantic_handles, loc="upper left", bbox_to_anchor=(0, 1.013), ncol=3, frameon=False, fontsize=8.5)
    ax.add_artist(first)
    ax.legend(handles=layer_handles, loc="upper right", bbox_to_anchor=(1, 1.013), ncol=3, frameon=False, fontsize=8.5)
    fig.subplots_adjust(left=0.28, right=0.985, top=0.958, bottom=0.04)
    save_figure(fig, FIG1_PNG, FIG1_SVG)


def plot_composition(rows: list[dict[str, object]], summary: list[dict[str, object]]) -> None:
    order = ["advocacy_target", "site_presence", "unclear", "institutional_venue", "event_site", "headquarters"]
    summary_by = {str(row["semantic_candidate_v1"]): row for row in summary}
    fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), gridspec_kw={"width_ratios": [1.08, 1]})

    ax = axes[0]
    y = list(range(len(order)))
    human = [int(summary_by[s]["human_reviewed_edge_count"]) for s in order]
    candidate = [int(summary_by[s]["candidate_edge_count"]) for s in order]
    colors = [SEMANTIC_COLORS[s] for s in order]
    ax.barh(y, human, color=colors, edgecolor="#24332E", linewidth=0.7, label="底层边已人审")
    ax.barh(y, candidate, left=human, color=colors, alpha=0.25, edgecolor=colors, linewidth=1.1, hatch="///", label="底层候选边")
    ax.set_yticks(y, [SEMANTIC_CN[s] for s in order])
    ax.invert_yaxis()
    ax.set_xlabel("actor–place 边数")
    ax.set_title("语义构成：目标关系占多数", loc="left", fontsize=15, fontweight="bold")
    ax.grid(axis="x", color="#E1E0DA", linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    for i, s in enumerate(order):
        total = int(summary_by[s]["edge_count"])
        ax.text(total + 0.55, i, str(total), va="center", fontsize=10, fontweight="bold")
    ax.legend(frameon=False, loc="lower right")

    ax = axes[1]
    evidence_colors = {"E4": "#294F4A", "E3": "#D18B3D", "E2": "#B8BFC2"}
    left = [0] * len(order)
    for ev in ["E4", "E3", "E2"]:
        values = [int(summary_by[s][f"{ev}_count"]) for s in order]
        ax.barh(y, values, left=left, color=evidence_colors[ev], label=ev)
        left = [a + b for a, b in zip(left, values)]
    ax.set_yticks(y, [SEMANTIC_CN[s] for s in order])
    ax.invert_yaxis()
    ax.set_xlabel("actor–place 边数")
    ax.set_title("证据等级并不等于语义已人审", loc="left", fontsize=15, fontweight="bold")
    ax.grid(axis="x", color="#E1E0DA", linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="lower right")

    fig.suptitle("R3 空间关系类型与证据层", x=0.055, y=0.988, ha="left", fontsize=20, fontweight="bold")
    fig.text(
        0.055, 0.91,
        "‘倡议／争议对象’主要来自边野古声明、诉讼与声援；不能读取为现场据点。底层边人审与空间语义人审是两个不同层次。",
        fontsize=10.5, color="#4D5955",
    )
    fig.subplots_adjust(left=0.12, right=0.98, top=0.81, bottom=0.12, wspace=0.36)
    save_figure(fig, FIG2_PNG, FIG2_SVG)


def plot_dossiers(dossier: list[dict[str, object]]) -> None:
    by_place: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in dossier:
        by_place[str(row["place"])].append(row)
    order = [("Yonaguni", "与那国"), ("Ishigaki", "石垣"), ("Miyako", "宫古")]
    fig, axes = plt.subplots(1, 3, figsize=(19, 10.5))
    card_colors = {"Yonaguni": "#E9F0EE", "Ishigaki": "#EEF0E7", "Miyako": "#E8EEF3"}

    for ax, (place, place_zh) in zip(axes, order):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        card = FancyBboxPatch((0.015, 0.015), 0.97, 0.965, boxstyle="round,pad=0.012,rounding_size=0.025", facecolor=card_colors[place], edgecolor="#C8CFCC", linewidth=1.0)
        ax.add_patch(card)
        rows = sorted(by_place[place], key=lambda r: (str(r["semantic_candidate_v1"]), str(r["actor_id"])))
        human_count = sum(r["fact_layer"] == "human_reviewed_actor_place_edge" for r in rows)
        gap_count = sum(r["fact_layer"] == "candidate_with_explicit_evidence_gap" for r in rows)
        ax.text(0.06, 0.935, place_zh, fontsize=21, fontweight="bold", va="top")
        ax.text(0.06, 0.89, f"{len(rows)} 条空间边 · {human_count} 条底层边人审 · {gap_count} 条显式补证缺口", fontsize=9.5, color="#52605A", va="top")

        y = 0.825
        for row in rows:
            semantic = str(row["semantic_candidate_v1"])
            marker = "●" if row["fact_layer"] == "human_reviewed_actor_place_edge" else "○"
            ax.text(0.065, y, marker, color=SEMANTIC_COLORS[semantic], fontsize=14, va="center", fontweight="bold")
            ax.text(0.105, y + 0.008, f"{row['actor_id']}  {short(str(row['actor_name']), 23)}", fontsize=9.5, va="center", fontweight="bold")
            ax.text(0.105, y - 0.027, f"{SEMANTIC_CN[semantic]} · {row['evidence_level_original']} · {row['edge_review_status_original']}", fontsize=8.1, va="center", color="#59645F")
            y -= 0.083

        frame_summary = str(rows[0]["r4_safe_source_visibility"]) if rows else ""
        r9_summary = str(rows[0]["r9_mechanism_summary"]) if rows else ""
        guardrail = str(rows[0]["place_guardrail"]) if rows else ""
        ax.text(0.065, 0.31, "已证／正式上下文", fontsize=10.5, fontweight="bold", color="#243A34")
        ax.text(0.065, 0.275, "\n".join(textwrap.wrap(frame_summary, 38)), fontsize=8.7, va="top", color="#364640")
        ax.text(0.065, 0.205, "制度链／候选解释", fontsize=10.5, fontweight="bold", color="#243A34")
        ax.text(0.065, 0.17, "\n".join(textwrap.wrap(r9_summary, 39)), fontsize=8.35, va="top", color="#364640")
        ax.text(0.065, 0.085, "\n".join(textwrap.wrap(guardrail, 39)), fontsize=8.5, va="top", color="#8A3F42", fontweight="bold")

    fig.suptitle("R3 先岛三地 actor–place dossier", x=0.045, y=0.99, ha="left", fontsize=21, fontweight="bold")
    fig.text(
        0.045, 0.915,
        "actor–place 行、R4 有限线上框架语料与 R9 正式程序链分层呈现；圆点实心仅表示底层空间边已人审，不表示组织关系或地方代表性。",
        fontsize=10.3, color="#4D5955",
    )
    fig.subplots_adjust(left=0.035, right=0.985, top=0.85, bottom=0.035, wspace=0.035)
    save_figure(fig, FIG3_PNG, FIG3_SVG)


def render_brief(
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    dossier: list[dict[str, object]],
    crosswalk: list[dict[str, object]],
    hr025: list[dict[str, object]],
) -> str:
    semantics = Counter(str(r["semantic_candidate_v1"]) for r in rows)
    places = Counter(str(r["place_id"]) for r in rows)
    human = sum(r["edge_review_layer"] == "human_reviewed_edge" for r in rows)
    mismatch = [r for r in rows if r["place_name_integrity"] != "match"]
    dossier_by: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in dossier:
        dossier_by[str(row["place"])].append(row)
    main_sources = sum(r["reference_kind"] == "main_source_id" for r in crosswalk)
    legacy_refs = sum(r["reference_kind"] == "legacy_actor_or_placeholder_ref" for r in crosswalk)
    broad_share = (places["P001"] + places["P002"]) / len(rows)
    filled_hr025 = sum(
        any(str(row[field]).strip() for field in HR025_HUMAN_FIELDS)
        for row in hr025
    )

    def actor_line(place: str) -> str:
        items = dossier_by[place]
        return "；".join(
            f"{r['actor_id']} {r['actor_name']}（{r['semantic_candidate_zh']}／{r['edge_review_status_original']}）"
            for r in items
        )

    return f"""# R3 空间语义与先岛 dossier v1

日期：2026-07-13

口径：{len(rows)} 条中央 actor–place 边的**候选空间语义层**。本包不修改基础中央表，只重生派生 interim32；语义候选不等于人审结论。

## 直接回答

当前空间表不能直接读成“组织在哪里有据点”。{len(rows)} 条边中：

- 倡议／争议对象 **{semantics['advocacy_target']}** 条；
- 持续活动／服务在场 **{semantics['site_presence']}** 条；
- 制度／机构场域 **{semantics['institutional_venue']}** 条；
- 事件／程序场域 **{semantics['event_site']}** 条；
- 总部／办公室 **{semantics['headquarters']}** 条；
- 当前语义未明 **{semantics['unclear']}** 条。

底层边只有 **{human}/{len(rows)}** 条为 `human_checked`／`human_revised`，其余 **{len(rows)-human}** 条仍是候选或补证状态。空间语义本身全部是机器候选；其中 **{len(hr025)}** 条因目标／在场／总部／制度场域难以机械区分而进入 HR-025。当前 **{filled_hr025}** 条已有人工字段；生成器按稳定 `object_id` 保留这些字段，不把它们改回空值。

## 最重要的解释增量

1. **边野古可见度主要是“目标”，不是“据点”。** P002 有 {places['P002']} 条关系，其中大量来自 2010／2015 声明、法律说明与本土／国际声援。把这些点画成同一种“组织在场”会把事件性倡议误写成地方组织密度。
2. **P001 是宽泛容器。** 冲绳全县有 {places['P001']} 条关系，混合了组织活动范围、项目语境、赞助／服务网络、行政辖区和弱连接，不能视为 40 个县级总部。
3. **空间表存在明显的可见度偏置。** P001 与 P002 合计 {places['P001'] + places['P002']}/{len(rows)}（{broad_share:.1%}）。这描述当前公开资料和编码方式，不代表现实组织密度。
4. **服务／行政空间与政治倡议空间必须分层。** USO／军属服务的基地中心、JICA／领馆等制度场域，只说明服务或行政渠道；不自动带出反基地／亲基地立场、资助关系或联盟。
5. **有一处地点键冲突不能静默修复。** {mismatch[0]['edge_id']} 的 place_id={mismatch[0]['place_id']} 在 place registry 对应 `{mismatch[0]['place_name_registry']}`，但边表写 `{mismatch[0]['place_name_original']}`。本包用红色菱形标记并送 HR-025。

## 与那国 dossier

空间行：{actor_line('Yonaguni')}

可安全说明的是：A016 的与那国公开活动关系已由 HR-003 人审；A014 是 2015 公投反对侧执委会的事件场域，A015 的与那国关系是意见广告／声援对象；A017、A018 与 A065 仍是琉球弧／南西诸岛网络层的候选空间解释。R4 有限线上语料把与那国首先放在台湾邻近／前线、安全环境、自治／公投与生命安全之中；**没有把环境—部署零条目解释成“当地没有环境问题”**。当地材料仍需确认 A014/A015 的组织身份与 A016 的成立／代表／持续性。

## 石垣 dossier

空间行：{actor_line('Ishigaki')}

A010 是持续反部署公民网络的地方在场候选；A011 的关系依据是住民投票请求过程，因此编码为事件／程序场域；A065 的石垣节点仍需第二来源。R9 的石垣正式链显示 14,263 份有效签名之后仍经过两次议会门槛和两条司法路径；这说明自治诉求会发生场域转移，但不能把 A011 写成具名组织原告，也不能从程序共现推导稳定联盟或结果因果。

## 宫古 dossier

空间行：{actor_line('Miyako')}

三条现有边均是地方活动／网络在场候选：A012 的组织全称和持续性仍需第二来源，A013 是反导弹部署网络，A065 的宫古节点仍需确认。R4 安全语料支持“地下水／饮用水作为生活条件”的地方框架，同时明确一般环境政策或环保活动不自动等于反部署。当前 R9 包没有宫古正式公投链；这只是本包范围边界，不是“没有地方自治行动”的结论。

## 来源与复核边界

- source crosswalk 共 **{len(crosswalk)}** 行，其中 actor–place 主 source ID 引用 {main_sources} 行；另有 {legacy_refs} 行仍是 `X...` 旧式 actor／placeholder 引用而非 source log ID。
- R4、R9 来源仅作为 dossier 的框架／程序上下文；不替代 actor–place 关系证据。
- 同一地点、同一声明、同一程序或共同出现都不建立组织间稳定联盟。
- E4 是来源强度，不等于本轮空间语义已获人工确认。

## 文件

- 全量候选语义表：`data/interim/32_actor_place_semantic_candidates_v1.csv`
- 类型汇总：`actor_place_semantic_summary_v1.csv`
- 三地 dossier：`sakishima_actor_place_dossier_v1.csv`
- 来源交叉表：`source_crosswalk_v1.csv`
- 人工语义任务：`HR025_actor_place_semantics_review_v0.csv`
- 图 1：`fig1_full_actor_place_semantic_matrix_v1.*`
- 图 2：`fig2_spatial_relation_type_composition_v1.*`
- 图 3：`fig3_sakishima_actor_place_dossiers_v1.*`
"""


def validate(
    edges: list[dict[str, str]],
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    dossier: list[dict[str, object]],
    crosswalk: list[dict[str, object]],
    hr025: list[dict[str, object]],
) -> None:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ValueError(message)

    input_ids = [row["edge_id"] for row in edges]
    derived_ids = [str(row["edge_id"]) for row in rows]
    expected_edge_count = 135
    require(len(edges) == expected_edge_count, f"expected {expected_edge_count} central actor-place edges, found {len(edges)}")
    require(len(rows) == expected_edge_count, f"expected {expected_edge_count} derived semantic rows, found {len(rows)}")
    require(len(set(input_ids)) == expected_edge_count and set(input_ids) == set(derived_ids), "edge coverage or uniqueness failed")

    coded_ids: list[str] = []
    for semantic, ids in SEMANTIC_EDGE_SETS.items():
        require(semantic in VALID_SEMANTICS, f"invalid semantic set: {semantic}")
        coded_ids.extend(ids)
    require(len(coded_ids) == expected_edge_count and len(set(coded_ids)) == expected_edge_count, "manual semantic coding is not exhaustive/disjoint")
    require(set(coded_ids) == set(input_ids), "semantic coding IDs differ from current edge table")
    require({str(row["semantic_candidate_v1"]) for row in rows}.issubset(VALID_SEMANTICS), "invalid semantic value")
    require(sum(int(row["edge_count"]) for row in summary) == expected_edge_count, f"summary does not sum to {expected_edge_count}")
    require(sum(row["edge_review_layer"] == "human_reviewed_edge" for row in rows) == 17, "expected 17 human-reviewed underlying edges")
    require(sum(row["edge_review_layer"] == "candidate_edge" for row in rows) == 118, "expected 118 candidate underlying edges")

    mismatch = [row for row in rows if row["place_name_integrity"] != "match"]
    require(len(mismatch) == 1 and mismatch[0]["edge_id"] == "AP123", "place ID/name mismatch audit changed")
    require(any(row["object_id"] == "AP123" for row in hr025), "AP123 must be routed to HR025")

    expected_hr = {
        str(row["edge_id"])
        for row in rows
        if row["semantic_freeze_status"] == "needs_human_semantic_review"
    }
    require({row["object_id"] for row in hr025} == expected_hr, "HR025 does not exactly match unresolved semantic rows")
    require(
        all(
            not row["final_semantic"] or row["final_semantic"] in VALID_SEMANTICS
            for row in hr025
        ),
        "HR025 contains an invalid preserved final_semantic",
    )

    expected_dossier_ids = {row["edge_id"] for row in edges if row["place_id"] in DOSSIER_PLACES}
    require(len(expected_dossier_ids) == 14, f"expected 14 Sakishima actor-place rows, found {len(expected_dossier_ids)}")
    require({str(row["edge_id"]) for row in dossier} == expected_dossier_ids, "dossier edge coverage failed")
    require(len([row for row in dossier if row["place"] == "Yonaguni"]) == 6, "Yonaguni dossier must have six rows")
    require(len([row for row in dossier if row["place"] == "Ishigaki"]) == 4, "Ishigaki dossier must have four rows")
    require(len([row for row in dossier if row["place"] == "Miyako"]) == 4, "Miyako dossier must have four rows")
    require(all("不将其强行环境化" in str(row["place_guardrail"]) for row in dossier if row["place"] == "Yonaguni"), "Yonaguni framing guardrail missing")

    edge_crosswalk = [row for row in crosswalk if row["usage_scope"] == "actor_place_edge"]
    expected_ref_count = sum(len(split_refs(row["source_ref"])) for row in edges)
    require(len(edge_crosswalk) == expected_ref_count == 186, "actor-place source crosswalk must expand all 186 refs")
    require({row["usage_object_id"] for row in edge_crosswalk} == set(input_ids), "source crosswalk misses an edge")
    require(all(row["interpretation_limit"] for row in crosswalk), "source crosswalk lacks interpretation boundary")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    configure_fonts()

    actors = read_csv(ACTORS)
    places = read_csv(PLACES)
    sources = read_csv(SOURCES)
    edges = read_csv(EDGES)
    archive = read_csv(ARCHIVE)
    actors_by_id = {row["actor_id"]: row for row in actors}
    places_by_id = {row["place_id"]: row for row in places}
    sources_by_id = {row["source_id"]: row for row in sources}
    archive_by_id = {row["source_id"]: row for row in archive}

    rows = build_semantic_rows(edges, actors_by_id, places_by_id)
    summary = build_summary(rows)
    hr025 = preserve_hr025_human_fields(build_hr025(rows), HR025)
    dossier = build_dossier(rows)
    crosswalk = build_source_crosswalk(rows, sources_by_id, archive_by_id, actors_by_id)
    validate(edges, rows, summary, dossier, crosswalk, hr025)

    derived_fields = list(rows[0].keys())
    summary_fields = list(summary[0].keys())
    dossier_fields = list(dossier[0].keys())
    crosswalk_fields = list(crosswalk[0].keys())
    hr025_fields = list(hr025[0].keys())
    write_csv(DERIVED, rows, derived_fields)
    write_csv(SUMMARY, summary, summary_fields)
    write_csv(DOSSIER, dossier, dossier_fields)
    write_csv(SOURCE_CROSSWALK, crosswalk, crosswalk_fields)
    write_csv(HR025, hr025, hr025_fields)

    plot_full_matrix(rows)
    plot_composition(rows, summary)
    plot_dossiers(dossier)
    for svg in [FIG1_SVG, FIG2_SVG, FIG3_SVG]:
        normalize_generated_svg(svg)
    write_text(FIG1_HTML, html_wrapper(FIG1_SVG.name, "R3 全量组织地点空间关系"))
    write_text(FIG2_HTML, html_wrapper(FIG2_SVG.name, "R3 空间关系类型构成"))
    write_text(FIG3_HTML, html_wrapper(FIG3_SVG.name, "R3 先岛三地 dossier"))

    filled_hr025 = sum(
        any(str(row[field]).strip() for field in HR025_HUMAN_FIELDS)
        for row in hr025
    )
    brief = render_brief(rows, summary, dossier, crosswalk, hr025)
    write_text(BRIEF, brief)
    write_text(
        README,
        f"""# R03 spatial dossier v1

Generated by `python scripts/make_r03_spatial_dossier_v1.py`.

    - {len(rows)}/{len(rows)} actor-place edges receive one candidate semantic.
    - {sum(row['edge_review_layer'] == 'human_reviewed_edge' for row in rows)} underlying edges are human-reviewed; {sum(row['edge_review_layer'] == 'candidate_edge' for row in rows)} remain candidate/status-limited.
- {len(hr025)} unresolved semantic decisions are routed to HR-025; {filled_hr025} rows currently contain preserved human fields.
- Sakishima dossier coverage: Yonaguni 6, Ishigaki 3, Miyako 3 actor-place rows.
    - The source crosswalk has {len(crosswalk)} rows, including all {sum(row['usage_scope'] == 'actor_place_edge' for row in crosswalk)} expanded refs from the actor-place table.

No base registry, source, place, event, or relation table is changed; the
derived interim32 table is regenerated. Candidate semantics and shared places
do not establish stable alliances, organizational headquarters, political
stance, funding, or causal effects.
""",
    )

    # Round-trip and visual artifact validation.
    require_roundtrip = read_csv(DERIVED)
    if len(require_roundtrip) != len(edges) or {r["edge_id"] for r in require_roundtrip} != {r["edge_id"] for r in edges}:
        raise ValueError("derived CSV round-trip failed")
    for svg in [FIG1_SVG, FIG2_SVG, FIG3_SVG]:
        ET.parse(svg)
        if svg.stat().st_size < 10_000:
            raise ValueError(f"SVG unexpectedly small: {svg}")
        if any(line.endswith((" ", "\t")) for line in svg.read_text(encoding="utf-8").splitlines()):
            raise ValueError(f"SVG contains trailing whitespace: {svg}")
    for png in [FIG1_PNG, FIG2_PNG, FIG3_PNG]:
        if png.stat().st_size < 20_000:
            raise ValueError(f"PNG unexpectedly small: {png}")
    if f"{len(rows)} 条" not in BRIEF.read_text(encoding="utf-8"):
        raise ValueError("brief count missing")

    output_hashes = {
        path.name: file_sha256(path)
        for path in [DERIVED, SUMMARY, DOSSIER, SOURCE_CROSSWALK, HR025, BRIEF, README, FIG1_PNG, FIG1_SVG, FIG2_PNG, FIG2_SVG, FIG3_PNG, FIG3_SVG]
    }
    write_text(
        VALIDATION,
        f"""# R3 spatial dossier validation v1

- Central actor-place input: {len(rows)} unique edges.
- Derived semantics: {len(rows)} unique rows; six allowed candidate values; no default or missing classification.
- Underlying review layer: {sum(row['edge_review_layer'] == 'human_reviewed_edge' for row in rows)} human-reviewed / {sum(row['edge_review_layer'] == 'candidate_edge' for row in rows)} candidate or evidence-gap rows.
- HR-025: {len(hr025)} semantic items; {filled_hr025} rows contain preserved human fields and reruns retain them by stable `object_id`.
- Sakishima: 14/14 rows (Yonaguni 6 / Ishigaki 4 / Miyako 4).
- Source crosswalk: {len(crosswalk)} rows; actor-place refs expanded {sum(row['usage_scope'] == 'actor_place_edge' for row in crosswalk)}.
- Place-key integrity: one explicit mismatch, AP123, retained for human review.
- SVG XML parse and trailing-whitespace check: pass for 3/3 figures. PNG size check: pass for 3/3 figures.
- Yonaguni guardrail: frontline/Taiwan proximity, autonomy/referendum and life-safety retained; no forced environmental framing.

Deterministic artifact hashes are generated in-memory for the checks above; the
report intentionally omits them so reruns remain concise. No base central
table was modified; derived interim32 was regenerated.
""",
    )

    # Use the variable to ensure every generated artifact was readable at the
    # point of completion without making the validation report path-dependent.
    if not all(output_hashes.values()):
        raise ValueError("artifact hash failure")
    print(
        f"R3 spatial dossier OK: {len(rows)} semantics; "
        f"{sum(row['edge_review_layer'] == 'human_reviewed_edge' for row in rows)} human/"
        f"{sum(row['edge_review_layer'] == 'candidate_edge' for row in rows)} candidate edges; "
        f"{len(hr025)} HR025 items; 14 Sakishima rows; {len(crosswalk)} source crosswalk rows."
    )


if __name__ == "__main__":
    main()
