from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

PERSON_DIR = ROOT / "outputs" / "us_presence_network_wave2_person_disambiguation_supplement_v1"
W2A_DIR = ROOT / "outputs" / "us_presence_network_wave2_w2_a_v1"
ASSESSMENT_PATH = PERSON_DIR / "candidate_assessment_v1.csv"
TIMELINE_PATH = PERSON_DIR / "candidate_timeline_v1.csv"
RESOURCE_PATH = W2A_DIR / "resource_flow_ledger_v1.csv"
PRINCIPAL_RETURN_PATH = ROOT / "docs" / "human_review_return_USN_wave2_prerequisite_partial_v1.md"

FOCAL_ACTORS = {
    "X004": "AWWA",
    "X005": "NOSCO",
    "X006": "KOSC",
    "X007": "OESC",
    "X018": "MTS",
}
EXTERNAL_NODES = {"LIONS_OKINAWA": "Lions Okinawa"}

SCENARIOS = [
    {
        "scenario_id": "SC01_VERY_HIGH_ONLY",
        "label_zh": "仅 very_high",
        "included_tiers": {"very_high"},
        "order": 1,
    },
    {
        "scenario_id": "SC02_ADD_HIGH",
        "label_zh": "再加入 high",
        "included_tiers": {"very_high", "high"},
        "order": 2,
    },
    {
        "scenario_id": "SC03_ADD_MODERATE",
        "label_zh": "再加入 moderate",
        "included_tiers": {"very_high", "high", "moderate"},
        "order": 3,
    },
]

EXPECTED_CONFIRMED_RESOURCE_ROWS = {"RF020", "RF022", "RF024"}
EXPECTED_CONDITIONAL_FOCAL_ROWS = {"RF026", "RF034"}
EXPECTED_BOUNDARY_ROW = "RF054"

REGISTER_COLUMNS = [
    "lead_id",
    "package_id",
    "record_kind",
    "chain_id",
    "parent_lead_id",
    "recon_step",
    "discovered_on",
    "lead_title",
    "observation",
    "why_unexpected",
    "source_or_query_locator",
    "next_test",
    "potential_value",
    "stop_reason",
    "workflow_status",
    "claim_eligibility",
    "central_writeback",
    "human_review_trigger",
    "publication_eligibility",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=columns,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_text_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evidence_tier(value: str) -> str:
    if value.startswith("very_high"):
        return "very_high"
    if value.startswith("high"):
        return "high"
    if value.startswith("moderate"):
        return "moderate"
    raise ValueError(f"Unmapped evidence strength: {value!r}")


def actor_ids_from_scope(scope: str) -> list[str]:
    ids = re.findall(r"\bX\d{3}\b", scope)
    return list(dict.fromkeys(ids))


def connected_components(nodes: list[str], pairs: set[tuple[str, str]]) -> list[list[str]]:
    adjacency: dict[str, set[str]] = {node: set() for node in nodes}
    for left, right in pairs:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(nodes)
    components: list[list[str]] = []
    while unseen:
        start = min(unseen)
        queue: deque[str] = deque([start])
        component: list[str] = []
        unseen.remove(start)
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbor in sorted(adjacency[node]):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    return sorted(components, key=lambda group: (-len(group), group))


def normalized_pair(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def display_candidate_names(timeline: list[dict[str, str]]) -> dict[str, str]:
    names: dict[str, list[str]] = defaultdict(list)
    for row in timeline:
        candidate_id = row["candidate_id"]
        name = row["name_as_recorded"].strip()
        if name and name not in names[candidate_id]:
            names[candidate_id].append(name)
    return {candidate_id: " / ".join(values) for candidate_id, values in names.items()}


def build_svg(
    summaries: list[dict[str, object]],
    person_pair_rows: list[dict[str, object]],
    within_actor_rows: list[dict[str, object]],
) -> str:
    width, height = 1500, 1010
    panel_width = 470
    margin = 30
    colors = {
        "bg": "#f7f5ee",
        "panel": "#fffdf8",
        "ink": "#173e46",
        "muted": "#667a7d",
        "grid": "#ccd9d6",
        "person": "#7a5a9e",
        "resource": "#c67a2d",
        "node": "#0f6870",
        "external": "#8a9695",
        "overlap": "#a34762",
    }

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="#c67a2d"/></marker>',
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{colors["bg"]}"/>',
        f'<text x="{margin}" y="38" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="{colors["ink"]}">服务侧人物候选 × 已核资源流：三档情景</text>',
        f'<text x="{margin}" y="66" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="14" fill="{colors["muted"]}">人物边均为“若同一人判断成立”的条件投影；资源边单独成层。未做中心性排名。</text>',
    ]

    person_by_scenario: dict[str, dict[tuple[str, str], list[str]]] = defaultdict(lambda: defaultdict(list))
    for row in person_pair_rows:
        pair = normalized_pair(str(row["actor_id_1"]), str(row["actor_id_2"]))
        person_by_scenario[str(row["scenario_id"])][pair].append(str(row["candidate_short_label"]))
    within_by_scenario: dict[str, list[str]] = defaultdict(list)
    for row in within_actor_rows:
        within_by_scenario[str(row["scenario_id"])].append(str(row["candidate_short_label"]))

    for index, summary in enumerate(summaries):
        x0 = margin + index * (panel_width + 15)
        y0 = 90
        scenario_id = str(summary["scenario_id"])
        parts.extend(
            [
                f'<rect x="{x0}" y="{y0}" width="{panel_width}" height="850" rx="18" fill="{colors["panel"]}" stroke="{colors["grid"]}"/>',
                f'<text x="{x0 + 20}" y="{y0 + 35}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="{colors["ink"]}">{html.escape(str(summary["scenario_label_zh"]))}</text>',
                f'<text x="{x0 + 20}" y="{y0 + 59}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" fill="{colors["muted"]}">纳入：{html.escape(str(summary["included_tiers"]))}</text>',
                f'<text x="{x0 + 20}" y="{y0 + 94}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="{colors["person"]}">人物候选层（条件边）</text>',
            ]
        )

        px = {
            "X004": (x0 + 235, y0 + 240),
            "X006": (x0 + 82, y0 + 160),
            "X007": (x0 + 388, y0 + 160),
            "X005": (x0 + 82, y0 + 315),
            "X018": (x0 + 388, y0 + 315),
        }
        for pair, labels in person_by_scenario[scenario_id].items():
            left, right = pair
            x1, y1 = px[left]
            x2, y2 = px[right]
            parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colors["person"]}" stroke-width="2.2" stroke-dasharray="7 5"/>'
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 7
            label = f"{len(labels)}项人物候选"
            parts.append(
                f'<text x="{mx}" y="{my}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="11" fill="{colors["person"]}">{label}</text>'
            )
        for actor_id, (x, y) in px.items():
            parts.append(f'<circle cx="{x}" cy="{y}" r="27" fill="#ffffff" stroke="{colors["node"]}" stroke-width="2"/>')
            parts.append(
                f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="{colors["ink"]}">{FOCAL_ACTORS[actor_id]}</text>'
            )
        if within_by_scenario[scenario_id]:
            parts.append(
                f'<text x="{x0 + 20}" y="{y0 + 365}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="11" fill="{colors["muted"]}">另有 OESC 内部连续性候选：Lesilee（不形成组织间边）</text>'
            )

        parts.extend(
            [
                f'<line x1="{x0 + 20}" y1="{y0 + 392}" x2="{x0 + panel_width - 20}" y2="{y0 + 392}" stroke="{colors["grid"]}"/>',
                f'<text x="{x0 + 20}" y="{y0 + 425}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="{colors["resource"]}">资金／资源层（已核边界）</text>',
            ]
        )
        rx = {
            "X004": (x0 + 235, y0 + 520),
            "X007": (x0 + 388, y0 + 470),
            "X018": (x0 + 82, y0 + 590),
            "LIONS_OKINAWA": (x0 + 235, y0 + 650),
        }
        x1, y1 = rx["X007"]
        x2, y2 = rx["X004"]
        parts.append(
            f'<line x1="{x1 - 28}" y1="{y1 + 8}" x2="{x2 + 28}" y2="{y2 - 8}" stroke="{colors["resource"]}" stroke-width="2.5" marker-end="url(#arrow)"/>'
        )
        parts.append(
            f'<text x="{x0 + 326}" y="{y0 + 505}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="11" fill="{colors["resource"]}">3笔已核（跨3税期）</text>'
        )
        x1, y1 = rx["X018"]
        x2, y2 = rx["LIONS_OKINAWA"]
        parts.append(
            f'<line x1="{x1 + 27}" y1="{y1 + 8}" x2="{x2 - 28}" y2="{y2 - 8}" stroke="{colors["resource"]}" stroke-width="2.5" marker-end="url(#arrow)"/>'
        )
        parts.append(
            f'<text x="{x0 + 150}" y="{y0 + 625}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="11" fill="{colors["resource"]}">USD 10k（止于中介）</text>'
        )
        for actor_id in ("X004", "X007", "X018"):
            x, y = rx[actor_id]
            parts.append(f'<circle cx="{x}" cy="{y}" r="27" fill="#ffffff" stroke="{colors["node"]}" stroke-width="2"/>')
            parts.append(
                f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="{colors["ink"]}">{FOCAL_ACTORS[actor_id]}</text>'
            )
        x, y = rx["LIONS_OKINAWA"]
        parts.append(f'<circle cx="{x}" cy="{y}" r="27" fill="#ffffff" stroke="{colors["external"]}" stroke-width="2"/>')
        parts.append(
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="10" font-weight="700" fill="{colors["ink"]}">Lions</text>'
        )
        parts.append(
            f'<text x="{x}" y="{y + 42}" text-anchor="middle" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="10" fill="{colors["muted"]}">外部中介节点</text>'
        )

        parts.extend(
            [
                f'<line x1="{x0 + 20}" y1="{y0 + 710}" x2="{x0 + panel_width - 20}" y2="{y0 + 710}" stroke="{colors["grid"]}"/>',
                f'<text x="{x0 + 20}" y="{y0 + 743}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="{colors["ink"]}">五个焦点组织的联合投影</text>',
                f'<text x="{x0 + 20}" y="{y0 + 770}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" fill="{colors["ink"]}">连通分量：{summary["focal_combined_component_count"]}　AWWA分量：{summary["awwa_component_size"]}/5</text>',
                f'<text x="{x0 + 20}" y="{y0 + 795}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" fill="{colors["ink"]}">人物×资源重叠对：{summary["multilayer_overlap_pair_count"]}　AWWA相邻组织：{summary["awwa_combined_neighbor_count"]}</text>',
                f'<text x="{x0 + 20}" y="{y0 + 820}" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="11" fill="{colors["muted"]}">移除AWWA后，其原分量拆为 {summary["awwa_component_fragments_after_removal"]} 个部分（仅本情景）。</text>',
            ]
        )

    parts.extend(
        [
            f'<line x1="30" y1="966" x2="78" y2="966" stroke="{colors["person"]}" stroke-width="2.2" stroke-dasharray="7 5"/>',
            f'<text x="88" y="971" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" fill="{colors["muted"]}">条件人物边（非负责人已认定事实）</text>',
            f'<line x1="345" y1="966" x2="393" y2="966" stroke="{colors["resource"]}" stroke-width="2.5" marker-end="url(#arrow)"/>',
            f'<text x="405" y="971" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" fill="{colors["muted"]}">已核资源边界；方向保留</text>',
            f'<text x="720" y="971" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="12" fill="{colors["muted"]}">连通性按五个焦点组织的无向弱投影计算，不含外部Lions。</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assessments = read_csv(ASSESSMENT_PATH)
    timeline = read_csv(TIMELINE_PATH)
    resource_rows = read_csv(RESOURCE_PATH)
    principal_return = PRINCIPAL_RETURN_PATH.read_text(encoding="utf-8")

    assert len(assessments) == 5, "Expected the five HR-USN2-01 candidate groups"
    candidate_names = display_candidate_names(timeline)
    assessment_by_id = {row["candidate_id"]: row for row in assessments}

    candidates: list[dict[str, object]] = []
    for row in assessments:
        actor_ids = actor_ids_from_scope(row["comparison_scope"])
        unknown = set(actor_ids) - set(FOCAL_ACTORS)
        assert not unknown, f"Unknown focal actor IDs in candidate scope: {unknown}"
        candidates.append(
            {
                **row,
                "tier": evidence_tier(row["evidence_strength_after_supplement"]),
                "actor_ids": actor_ids,
                "candidate_label": candidate_names[row["candidate_id"]],
                "is_cross_org": len(actor_ids) >= 2,
            }
        )

    resource_by_id = {row["flow_observation_id"]: row for row in resource_rows}
    confirmed_resources = [
        row
        for row in resource_rows
        if row["flow_observation_id"] in EXPECTED_CONFIRMED_RESOURCE_ROWS
        and row["review_status"] == "human_checked"
        and row["fact_status"] == "research_only_principal_confirmed_anchor"
    ]
    assert {row["flow_observation_id"] for row in confirmed_resources} == EXPECTED_CONFIRMED_RESOURCE_ROWS

    assert "MTS→Lions" in principal_return and "accept_current_boundary" in principal_return
    boundary_resource = resource_by_id[EXPECTED_BOUNDARY_ROW]
    assert boundary_resource["source_actor_id"] == "X018"
    assert boundary_resource["target_id"] == "LIONS_OKINAWA"
    assert boundary_resource["transaction_closure"] == "provider_to_intermediary_only"

    resource_layer_rows: list[dict[str, object]] = []
    for row in confirmed_resources:
        resource_layer_rows.append(
            {
                "resource_edge_id": row["flow_observation_id"],
                "source_actor_id": row["source_actor_id"],
                "source_actor_label": FOCAL_ACTORS[row["source_actor_id"]],
                "target_id": row["target_id"],
                "target_label": FOCAL_ACTORS[row["target_id"]],
                "target_scope": "focal_actor",
                "period_start": row["period_start"],
                "period_end": row["period_end"],
                "event_date": row["event_date"],
                "amount": row["amount"],
                "currency": row["currency"],
                "resource_type": row["resource_type"],
                "direction": "directed",
                "admission_basis": "W2A_human_checked_principal_confirmed_anchor",
                "transaction_closure": row["transaction_closure"],
                "review_status": row["review_status"],
                "fact_status": row["fact_status"],
                "source_receipt_ids": row["source_receipt_ids"],
                "component_use": "focal_weak_projection",
                "caution": "Each row is one tax-period filing observation; do not sum across periods as one annual amount.",
            }
        )
    resource_layer_rows.append(
        {
            "resource_edge_id": boundary_resource["flow_observation_id"],
            "source_actor_id": boundary_resource["source_actor_id"],
            "source_actor_label": FOCAL_ACTORS[boundary_resource["source_actor_id"]],
            "target_id": boundary_resource["target_id"],
            "target_label": EXTERNAL_NODES[boundary_resource["target_id"]],
            "target_scope": "external_intermediary",
            "period_start": boundary_resource["period_start"],
            "period_end": boundary_resource["period_end"],
            "event_date": boundary_resource["event_date"],
            "amount": boundary_resource["amount"],
            "currency": boundary_resource["currency"],
            "resource_type": boundary_resource["resource_type"],
            "direction": "directed",
            "admission_basis": "principal_accept_current_boundary_2026-08-22",
            "transaction_closure": boundary_resource["transaction_closure"],
            "review_status": "principal_confirmed_boundary",
            "fact_status": "research_only_principal_confirmed_current_boundary",
            "source_receipt_ids": boundary_resource["source_receipt_ids"],
            "component_use": "external_stub_not_in_focal_component_count",
            "caution": "The edge stops at Lions; no Lions-to-final-child-health endpoint is created.",
        }
    )

    excluded_rows: list[dict[str, object]] = []
    for flow_id in sorted(EXPECTED_CONDITIONAL_FOCAL_ROWS):
        row = resource_by_id[flow_id]
        excluded_rows.append(
            {
                "input_type": "resource_flow",
                "input_id": flow_id,
                "source_id": row["source_actor_id"],
                "target_id": row["target_id"],
                "observed_value": row["amount"],
                "unit": row["currency"],
                "input_status": f'{row["review_status"]}/{row["fact_status"]}',
                "exclusion_reason": "Official filing candidate is not principal-confirmed; excluded from confirmed resource layer.",
                "effect_if_later_accepted": "Would connect MTS to AWWA inside the five-actor focal frame.",
            }
        )

    node_rows: list[dict[str, object]] = []
    incidence_rows: list[dict[str, object]] = []
    person_pair_rows: list[dict[str, object]] = []
    within_actor_rows: list[dict[str, object]] = []
    component_rows: list[dict[str, object]] = []
    overlap_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    focal_resource_pairs = {
        normalized_pair(str(row["source_actor_id"]), str(row["target_id"]))
        for row in resource_layer_rows
        if row["target_scope"] == "focal_actor"
    }

    timeline_by_candidate_actor: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in timeline:
        actor_id = row["actor_id"]
        if actor_id in FOCAL_ACTORS:
            timeline_by_candidate_actor[(row["candidate_id"], actor_id)].append(
                f'{row["name_as_recorded"]}: {row["role_as_recorded"]} [{row["date_start"]}–{row["date_end_or_point"]}]'
            )

    for scenario in SCENARIOS:
        scenario_id = scenario["scenario_id"]
        included = [candidate for candidate in candidates if candidate["tier"] in scenario["included_tiers"]]

        for actor_id, label in FOCAL_ACTORS.items():
            node_rows.append(
                {
                    "scenario_id": scenario_id,
                    "node_id": actor_id,
                    "node_type": "focal_organization",
                    "label": label,
                    "evidence_status": "selected_focal_actor",
                    "person_identity_decision": "not_applicable",
                    "central_writeback": "no",
                    "frontend_eligible": "no",
                }
            )
        node_rows.append(
            {
                "scenario_id": scenario_id,
                "node_id": "LIONS_OKINAWA",
                "node_type": "external_intermediary",
                "label": "Lions Okinawa",
                "evidence_status": "principal_confirmed_current_boundary",
                "person_identity_decision": "not_applicable",
                "central_writeback": "no",
                "frontend_eligible": "no",
            }
        )

        person_pairs: set[tuple[str, str]] = set()
        pair_candidate_counts: dict[tuple[str, str], list[str]] = defaultdict(list)
        for candidate in included:
            candidate_id = str(candidate["candidate_id"])
            candidate_node_id = f"HYP_{candidate_id}"
            short_label = str(candidate["candidate_label"])
            node_rows.append(
                {
                    "scenario_id": scenario_id,
                    "node_id": candidate_node_id,
                    "node_type": "hypothetical_identity_candidate_not_person_node",
                    "label": short_label,
                    "evidence_status": candidate["evidence_strength_after_supplement"],
                    "person_identity_decision": "principal_review_pending",
                    "central_writeback": "no",
                    "frontend_eligible": "no",
                }
            )
            actor_ids = list(candidate["actor_ids"])
            for actor_id in actor_ids:
                incidence_rows.append(
                    {
                        "scenario_id": scenario_id,
                        "candidate_id": candidate_id,
                        "candidate_node_id": candidate_node_id,
                        "candidate_label": short_label,
                        "evidence_tier": candidate["tier"],
                        "actor_id": actor_id,
                        "actor_label": FOCAL_ACTORS[actor_id],
                        "role_observation_summary": " | ".join(timeline_by_candidate_actor[(candidate_id, actor_id)]),
                        "edge_semantics": "conditional_candidate_incidence",
                        "principal_same_person_decision": "pending",
                        "fact_status": "research_only_scenario_not_fact",
                        "central_writeback": "no",
                        "frontend_eligible": "no",
                    }
                )
            if len(actor_ids) >= 2:
                for left_index, left in enumerate(actor_ids):
                    for right in actor_ids[left_index + 1 :]:
                        pair = normalized_pair(left, right)
                        person_pairs.add(pair)
                        pair_candidate_counts[pair].append(candidate_id)
                        person_pair_rows.append(
                            {
                                "scenario_id": scenario_id,
                                "candidate_id": candidate_id,
                                "candidate_short_label": short_label,
                                "evidence_tier": candidate["tier"],
                                "actor_id_1": pair[0],
                                "actor_label_1": FOCAL_ACTORS[pair[0]],
                                "actor_id_2": pair[1],
                                "actor_label_2": FOCAL_ACTORS[pair[1]],
                                "projection_semantics": "if_same_person_then_shared_person_pair",
                                "principal_same_person_decision": "pending",
                                "fact_status": "research_only_scenario_not_fact",
                                "central_writeback": "no",
                                "frontend_eligible": "no",
                            }
                        )
            else:
                actor_id = actor_ids[0]
                within_actor_rows.append(
                    {
                        "scenario_id": scenario_id,
                        "candidate_id": candidate_id,
                        "candidate_short_label": short_label,
                        "evidence_tier": candidate["tier"],
                        "actor_id": actor_id,
                        "actor_label": FOCAL_ACTORS[actor_id],
                        "network_effect": "within_actor_timeline_normalization_only",
                        "fact_status": "research_only_scenario_not_fact",
                    }
                )

        combined_pairs = person_pairs | focal_resource_pairs
        person_components = connected_components(sorted(FOCAL_ACTORS), person_pairs)
        resource_components = connected_components(sorted(FOCAL_ACTORS), focal_resource_pairs)
        combined_components = connected_components(sorted(FOCAL_ACTORS), combined_pairs)

        def component_map(components: list[list[str]], prefix: str) -> dict[str, tuple[str, int]]:
            result: dict[str, tuple[str, int]] = {}
            for index, component in enumerate(components, start=1):
                component_id = f"{prefix}{index:02d}"
                for actor_id in component:
                    result[actor_id] = (component_id, len(component))
            return result

        person_map = component_map(person_components, "P")
        resource_map = component_map(resource_components, "R")
        combined_map = component_map(combined_components, "C")

        person_neighbors: dict[str, set[str]] = {actor_id: set() for actor_id in FOCAL_ACTORS}
        resource_neighbors: dict[str, set[str]] = {actor_id: set() for actor_id in FOCAL_ACTORS}
        combined_neighbors: dict[str, set[str]] = {actor_id: set() for actor_id in FOCAL_ACTORS}
        for left, right in person_pairs:
            person_neighbors[left].add(right)
            person_neighbors[right].add(left)
        for left, right in focal_resource_pairs:
            resource_neighbors[left].add(right)
            resource_neighbors[right].add(left)
        for left, right in combined_pairs:
            combined_neighbors[left].add(right)
            combined_neighbors[right].add(left)

        for actor_id in sorted(FOCAL_ACTORS):
            component_rows.append(
                {
                    "scenario_id": scenario_id,
                    "actor_id": actor_id,
                    "actor_label": FOCAL_ACTORS[actor_id],
                    "person_component_id": person_map[actor_id][0],
                    "person_component_size": person_map[actor_id][1],
                    "resource_component_id": resource_map[actor_id][0],
                    "resource_component_size": resource_map[actor_id][1],
                    "combined_component_id": combined_map[actor_id][0],
                    "combined_component_size": combined_map[actor_id][1],
                    "person_unique_neighbors": len(person_neighbors[actor_id]),
                    "resource_unique_neighbors": len(resource_neighbors[actor_id]),
                    "combined_unique_neighbors": len(combined_neighbors[actor_id]),
                    "interpretation_boundary": "Weak undirected connectivity among five focal organizations; external Lions excluded from component count.",
                }
            )

        union_pairs = sorted(person_pairs | focal_resource_pairs)
        for left, right in union_pairs:
            person_candidate_ids = pair_candidate_counts.get((left, right), [])
            resource_observations = [
                row
                for row in resource_layer_rows
                if row["target_scope"] == "focal_actor"
                and normalized_pair(str(row["source_actor_id"]), str(row["target_id"])) == (left, right)
            ]
            overlap_rows.append(
                {
                    "scenario_id": scenario_id,
                    "actor_id_1": left,
                    "actor_label_1": FOCAL_ACTORS[left],
                    "actor_id_2": right,
                    "actor_label_2": FOCAL_ACTORS[right],
                    "person_layer_present": "yes" if person_candidate_ids else "no",
                    "person_candidate_count": len(person_candidate_ids),
                    "person_candidate_ids": ";".join(person_candidate_ids),
                    "resource_layer_present": "yes" if resource_observations else "no",
                    "resource_observation_count": len(resource_observations),
                    "resource_observation_ids": ";".join(str(row["resource_edge_id"]) for row in resource_observations),
                    "multilayer_overlap": "yes" if person_candidate_ids and resource_observations else "no",
                    "allowed_reading": "Layer co-presence on an organization pair; it does not prove control, earmarking or the same causal channel.",
                }
            )

        awwa_component = next(component for component in combined_components if "X004" in component)
        remaining_nodes = [node for node in awwa_component if node != "X004"]
        remaining_pairs = {
            pair
            for pair in combined_pairs
            if pair[0] in remaining_nodes and pair[1] in remaining_nodes
        }
        fragments = connected_components(remaining_nodes, remaining_pairs) if remaining_nodes else []
        overlap_pairs = person_pairs & focal_resource_pairs
        isolated = [component[0] for component in combined_components if len(component) == 1]
        summary_rows.append(
            {
                "scenario_order": scenario["order"],
                "scenario_id": scenario_id,
                "scenario_label_zh": scenario["label_zh"],
                "included_tiers": "+".join(sorted(scenario["included_tiers"], key=("very_high", "high", "moderate").index)),
                "included_candidate_groups": len(included),
                "cross_org_person_candidate_count": sum(1 for candidate in included if candidate["is_cross_org"]),
                "within_actor_continuity_candidate_count": sum(1 for candidate in included if not candidate["is_cross_org"]),
                "unique_person_org_pair_count": len(person_pairs),
                "confirmed_resource_observation_count": len(resource_layer_rows),
                "focal_resource_pair_count": len(focal_resource_pairs),
                "external_resource_edge_count": sum(1 for row in resource_layer_rows if row["target_scope"] != "focal_actor"),
                "focal_person_component_count": len(person_components),
                "focal_resource_component_count": len(resource_components),
                "focal_combined_component_count": len(combined_components),
                "largest_focal_combined_component_size": max(map(len, combined_components)),
                "awwa_person_neighbor_count": len(person_neighbors["X004"]),
                "awwa_resource_neighbor_count": len(resource_neighbors["X004"]),
                "awwa_combined_neighbor_count": len(combined_neighbors["X004"]),
                "awwa_component_size": len(awwa_component),
                "awwa_component_fragments_after_removal": len(fragments),
                "awwa_is_cut_vertex_in_its_modeled_component": "yes" if len(fragments) > 1 else "no",
                "multilayer_overlap_pair_count": len(overlap_pairs),
                "multilayer_overlap_pairs": ";".join(f"{FOCAL_ACTORS[a]}--{FOCAL_ACTORS[b]}" for a, b in sorted(overlap_pairs)),
                "isolated_focal_nodes_in_combined": ";".join(FOCAL_ACTORS[node] for node in isolated),
                "allowed_reading": "Conditional sensitivity result only; AWWA's modeled connector position is not an influence ranking.",
            }
        )

    expected = {
        "SC01_VERY_HIGH_ONLY": (4, 3, 0, 3),
        "SC02_ADD_HIGH": (3, 3, 1, 3),
        "SC03_ADD_MODERATE": (2, 2, 1, 4),
    }
    for row in summary_rows:
        assert (
            int(row["focal_person_component_count"]),
            int(row["focal_combined_component_count"]),
            int(row["multilayer_overlap_pair_count"]),
            int(row["awwa_component_size"]),
        ) == expected[str(row["scenario_id"])]

    write_csv(
        OUT / "scenario_nodes_v1.csv",
        node_rows,
        [
            "scenario_id",
            "node_id",
            "node_type",
            "label",
            "evidence_status",
            "person_identity_decision",
            "central_writeback",
            "frontend_eligible",
        ],
    )
    write_csv(
        OUT / "person_layer_incidence_edges_v1.csv",
        incidence_rows,
        [
            "scenario_id",
            "candidate_id",
            "candidate_node_id",
            "candidate_label",
            "evidence_tier",
            "actor_id",
            "actor_label",
            "role_observation_summary",
            "edge_semantics",
            "principal_same_person_decision",
            "fact_status",
            "central_writeback",
            "frontend_eligible",
        ],
    )
    write_csv(
        OUT / "person_pair_projection_v1.csv",
        person_pair_rows,
        [
            "scenario_id",
            "candidate_id",
            "candidate_short_label",
            "evidence_tier",
            "actor_id_1",
            "actor_label_1",
            "actor_id_2",
            "actor_label_2",
            "projection_semantics",
            "principal_same_person_decision",
            "fact_status",
            "central_writeback",
            "frontend_eligible",
        ],
    )
    write_csv(
        OUT / "within_actor_continuity_by_scenario_v1.csv",
        within_actor_rows,
        [
            "scenario_id",
            "candidate_id",
            "candidate_short_label",
            "evidence_tier",
            "actor_id",
            "actor_label",
            "network_effect",
            "fact_status",
        ],
    )
    write_csv(
        OUT / "resource_layer_edges_v1.csv",
        resource_layer_rows,
        [
            "resource_edge_id",
            "source_actor_id",
            "source_actor_label",
            "target_id",
            "target_label",
            "target_scope",
            "period_start",
            "period_end",
            "event_date",
            "amount",
            "currency",
            "resource_type",
            "direction",
            "admission_basis",
            "transaction_closure",
            "review_status",
            "fact_status",
            "source_receipt_ids",
            "component_use",
            "caution",
        ],
    )
    write_csv(
        OUT / "scenario_node_components_v1.csv",
        component_rows,
        [
            "scenario_id",
            "actor_id",
            "actor_label",
            "person_component_id",
            "person_component_size",
            "resource_component_id",
            "resource_component_size",
            "combined_component_id",
            "combined_component_size",
            "person_unique_neighbors",
            "resource_unique_neighbors",
            "combined_unique_neighbors",
            "interpretation_boundary",
        ],
    )
    write_csv(
        OUT / "scenario_pair_overlap_v1.csv",
        overlap_rows,
        [
            "scenario_id",
            "actor_id_1",
            "actor_label_1",
            "actor_id_2",
            "actor_label_2",
            "person_layer_present",
            "person_candidate_count",
            "person_candidate_ids",
            "resource_layer_present",
            "resource_observation_count",
            "resource_observation_ids",
            "multilayer_overlap",
            "allowed_reading",
        ],
    )
    write_csv(
        OUT / "scenario_summary_v1.csv",
        summary_rows,
        [
            "scenario_order",
            "scenario_id",
            "scenario_label_zh",
            "included_tiers",
            "included_candidate_groups",
            "cross_org_person_candidate_count",
            "within_actor_continuity_candidate_count",
            "unique_person_org_pair_count",
            "confirmed_resource_observation_count",
            "focal_resource_pair_count",
            "external_resource_edge_count",
            "focal_person_component_count",
            "focal_resource_component_count",
            "focal_combined_component_count",
            "largest_focal_combined_component_size",
            "awwa_person_neighbor_count",
            "awwa_resource_neighbor_count",
            "awwa_combined_neighbor_count",
            "awwa_component_size",
            "awwa_component_fragments_after_removal",
            "awwa_is_cut_vertex_in_its_modeled_component",
            "multilayer_overlap_pair_count",
            "multilayer_overlap_pairs",
            "isolated_focal_nodes_in_combined",
            "allowed_reading",
        ],
    )
    write_csv(
        OUT / "excluded_inputs_v1.csv",
        excluded_rows,
        [
            "input_type",
            "input_id",
            "source_id",
            "target_id",
            "observed_value",
            "unit",
            "input_status",
            "exclusion_reason",
            "effect_if_later_accepted",
        ],
    )
    write_csv(OUT / "unexpected_findings_register_v1.csv", [], REGISTER_COLUMNS)

    svg = build_svg(summary_rows, person_pair_rows, within_actor_rows) + "\n"
    write_text_lf(OUT / "fig_service_person_scenarios_v1.svg", svg)

    output_files = [
        "README.md",
        "build_service_person_scenarios_v1.py",
        "scenario_nodes_v1.csv",
        "person_layer_incidence_edges_v1.csv",
        "person_pair_projection_v1.csv",
        "within_actor_continuity_by_scenario_v1.csv",
        "resource_layer_edges_v1.csv",
        "scenario_node_components_v1.csv",
        "scenario_pair_overlap_v1.csv",
        "scenario_summary_v1.csv",
        "excluded_inputs_v1.csv",
        "unexpected_findings_register_v1.csv",
        "fig_service_person_scenarios_v1.svg",
    ]
    validation = {
        "status": "PASS",
        "package_status": "research_only_not_frontend_ready",
        "input_hashes": {
            str(ASSESSMENT_PATH.relative_to(ROOT)): sha256(ASSESSMENT_PATH),
            str(TIMELINE_PATH.relative_to(ROOT)): sha256(TIMELINE_PATH),
            str(RESOURCE_PATH.relative_to(ROOT)): sha256(RESOURCE_PATH),
            str(PRINCIPAL_RETURN_PATH.relative_to(ROOT)): sha256(PRINCIPAL_RETURN_PATH),
        },
        "row_counts": {
            "scenario_nodes_v1.csv": len(node_rows),
            "person_layer_incidence_edges_v1.csv": len(incidence_rows),
            "person_pair_projection_v1.csv": len(person_pair_rows),
            "within_actor_continuity_by_scenario_v1.csv": len(within_actor_rows),
            "resource_layer_edges_v1.csv": len(resource_layer_rows),
            "scenario_node_components_v1.csv": len(component_rows),
            "scenario_pair_overlap_v1.csv": len(overlap_rows),
            "scenario_summary_v1.csv": len(summary_rows),
            "excluded_inputs_v1.csv": len(excluded_rows),
            "unexpected_findings_register_v1.csv": 0,
        },
        "invariants": {
            "candidate_groups": sorted(assessment_by_id),
            "confirmed_resource_rows": sorted(EXPECTED_CONFIRMED_RESOURCE_ROWS),
            "principal_boundary_row": EXPECTED_BOUNDARY_ROW,
            "unapproved_mts_awwa_rows_excluded": sorted(EXPECTED_CONDITIONAL_FOCAL_ROWS),
            "scenario_expected_tuples": {
                key: {
                    "person_components": value[0],
                    "combined_components": value[1],
                    "multilayer_overlap_pairs": value[2],
                    "awwa_component_size": value[3],
                }
                for key, value in expected.items()
            },
            "person_and_resource_files_separate": True,
            "central_writeback": False,
            "frontend_ready": False,
            "human_review_created": False,
            "publication_eligible": False,
        },
    }
    write_text_lf(
        OUT / "validation_report_v1.json",
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
    )

    manifest = {
        "package_id": "USN_W2_SERVICE_PERSON_SCENARIO_V1",
        "generated_by": "build_service_person_scenarios_v1.py",
        "status": "research_only_not_frontend_ready",
        "files": {},
    }
    for filename in output_files + ["validation_report_v1.json"]:
        path = OUT / filename
        manifest["files"][filename] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    write_text_lf(
        OUT / "manifest_v1.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )


if __name__ == "__main__":
    main()
