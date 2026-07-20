"""Render only the current R5 figure in the third-sync preparation package.

The historical all-figure builder predates the merged HR-020 identity layer.
This renderer instead reads the current central participation table, checks it
against the current R5 event/bridge/overlap tables, and writes only figure 6's
CSV and PNG. It never edits facts, review queues, the other five sync figures,
or either Markdown draft.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARTICIPATION_PATH = (
    ROOT / "data" / "interim" / "25_coaction_event_participation_v0.csv"
)
DEFAULT_R5_DIR = ROOT / "outputs" / "R05_coaction_v1"
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "formal_comm_v2"

EVENT_CATALOG_FILENAME = "event_catalog_v0.csv"
BRIDGE_FILENAME = "repeat_participation_bridges_v0.csv"
OVERLAP_FILENAME = "event_overlap_v0.csv"
DATA_FILENAME = "fig6_event_reassembly_v2.csv"
FIGURE_FILENAME = "fig6_event_reassembly_v2.png"
OUTPUT_RELATIVE_PATHS = {
    f"data/{DATA_FILENAME}",
    f"fig/{FIGURE_FILENAME}",
}

EVENT_IDS = (
    "EV2010_WWF_67",
    "EV2015_NACSJ_31",
    "EV2020_OEJP_MMC_71",
)
EVENT_LABELS = {
    "EV2010_WWF_67": "2010 WWF 声明",
    "EV2015_NACSJ_31": "2015 NACSJ／Peace Boat 声明",
    "EV2020_OEJP_MMC_71": "2020 OEJP／MMC 请求",
}
ACTION_LABELS = {
    "EV2010_WWF_67": "共同声明",
    "EV2015_NACSJ_31": "共同声明",
    "EV2020_OEJP_MMC_71": "请求信／公民社会报告",
}
TARGET_LABELS = {
    "EV2010_WWF_67": "日本政府",
    "EV2015_NACSJ_31": "日美两国政府",
    "EV2020_OEJP_MMC_71": "美国海洋哺乳动物委员会",
}
EXPECTED_EVENT_IDENTITY_COUNTS = {
    "EV2010_WWF_67": Counter(
        {
            "registry_actor": 16,
            "event_only_identity_human_checked": 11,
            "event_only_name": 40,
        }
    ),
    "EV2015_NACSJ_31": Counter({"registry_actor": 31}),
    "EV2020_OEJP_MMC_71": Counter(
        {
            "registry_actor": 17,
            "event_only_identity_human_checked": 11,
            "event_only_name": 43,
        }
    ),
}
EXPECTED_STRUCTURED_COUNTS = {
    "EV2010_WWF_67": 67,
    "EV2015_NACSJ_31": 31,
    "EV2020_OEJP_MMC_71": 71,
}
EXPECTED_ACTION_TYPES = {
    "EV2010_WWF_67": "joint_statement",
    "EV2015_NACSJ_31": "joint_statement",
    "EV2020_OEJP_MMC_71": "request_letter_and_civil_society_report",
}
EXPECTED_TARGETS = {
    "EV2010_WWF_67": "Prime Minister; Minister of Defense; Minister for Foreign Affairs",
    "EV2015_NACSJ_31": "Government of Japan; Government of the United States",
    "EV2020_OEJP_MMC_71": "U.S. Marine Mammal Commission",
}
EXPECTED_EVENT_OBSERVATION_COUNTS = Counter(
    {
        "accepted_source_list_observation": 167,
        "human_checked_source_segmentation": 2,
    }
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = [
        "event",
        "source_list_rows",
        "confirmed_registry_rows",
        "target_or_venue",
        "action",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_current(
    participation_path: Path = DEFAULT_PARTICIPATION_PATH,
    r5_dir: Path = DEFAULT_R5_DIR,
) -> dict[str, list[dict[str, str]]]:
    r5_dir = Path(r5_dir)
    return {
        "participation": read_csv(Path(participation_path)),
        "events": read_csv(r5_dir / EVENT_CATALOG_FILENAME),
        "bridges": read_csv(r5_dir / BRIDGE_FILENAME),
        "overlaps": read_csv(r5_dir / OVERLAP_FILENAME),
    }


def identity_event_sets(
    participation: list[dict[str, str]],
    identity_status: str,
) -> dict[str, set[str]]:
    event_sets: dict[str, set[str]] = defaultdict(set)
    for row in participation:
        if row["identity_status"] != identity_status:
            continue
        if identity_status == "registry_actor":
            key = row["actor_id"]
        else:
            key = row["identity_group_id"]
        if not key:
            raise ValueError(
                f"{identity_status} row {row['participant_key']} lacks a stable identity key"
            )
        event_sets[key].add(row["event_id"])
    return dict(event_sets)


def registry_pairwise_overlap(
    registry_events: dict[str, set[str]],
) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    for index, event_a in enumerate(EVENT_IDS):
        for event_b in EVENT_IDS[index + 1 :]:
            counts[(event_a, event_b)] = sum(
                event_a in event_ids and event_b in event_ids
                for event_ids in registry_events.values()
            )
    return counts


def validate_current(tables: dict[str, list[dict[str, str]]]) -> None:
    participation = tables["participation"]
    if len(participation) != 169:
        raise ValueError("current R5 participation layer must contain 169 rows")
    if len({row["participant_key"] for row in participation}) != 169:
        raise ValueError("current R5 participant_key values must be unique")
    if {row["event_id"] for row in participation} != set(EVENT_IDS):
        raise ValueError("current R5 layer must contain exactly the three sampled events")

    allowed_statuses = set().union(
        *(set(counts) for counts in EXPECTED_EVENT_IDENTITY_COUNTS.values())
    )
    observed_statuses = {row["identity_status"] for row in participation}
    if observed_statuses != allowed_statuses:
        raise ValueError(f"unexpected R5 identity statuses: {observed_statuses}")
    observation_counts = Counter(
        row["event_observation_status"] for row in participation
    )
    if observation_counts != EXPECTED_EVENT_OBSERVATION_COUNTS:
        raise ValueError(
            "unexpected R5 source-list observation boundary: "
            f"{observation_counts}"
        )

    observed_event_counts = {
        event_id: Counter(
            row["identity_status"]
            for row in participation
            if row["event_id"] == event_id
        )
        for event_id in EVENT_IDS
    }
    if observed_event_counts != EXPECTED_EVENT_IDENTITY_COUNTS:
        raise ValueError(f"current R5 identity-layer drift: {observed_event_counts}")

    events = tables["events"]
    event_lookup = {row["event_id"]: row for row in events}
    if len(events) != 3 or set(event_lookup) != set(EVENT_IDS):
        raise ValueError("R5 event catalog must contain exactly the three current events")
    for event_id in EVENT_IDS:
        row = event_lookup[event_id]
        observed = (
            int(row["structured_participant_count"]),
            int(row["registry_actor_rows"]),
            int(row["human_reviewed_event_only_rows"]),
            int(row["event_only_name_rows"]),
            int(row["alias_pending_rows"]),
        )
        identity_counts = EXPECTED_EVENT_IDENTITY_COUNTS[event_id]
        expected = (
            EXPECTED_STRUCTURED_COUNTS[event_id],
            identity_counts["registry_actor"],
            identity_counts["event_only_identity_human_checked"],
            identity_counts["event_only_name"],
            0,
        )
        if observed != expected:
            raise ValueError(
                f"R5 event catalog disagrees with current identities for {event_id}: "
                f"{observed} != {expected}"
            )
        if row["action_type"] != EXPECTED_ACTION_TYPES[event_id]:
            raise ValueError(f"unexpected action type for {event_id}")
        if row["target_institution"] != EXPECTED_TARGETS[event_id]:
            raise ValueError(f"unexpected target institution for {event_id}")

    registry_events = identity_event_sets(participation, "registry_actor")
    human_event_events = identity_event_sets(
        participation, "event_only_identity_human_checked"
    )
    registry_repeats = {
        key: event_ids for key, event_ids in registry_events.items() if len(event_ids) >= 2
    }
    human_event_repeats = {
        key: event_ids
        for key, event_ids in human_event_events.items()
        if len(event_ids) >= 2
    }
    if len(registry_repeats) != 15:
        raise ValueError("current registry-only repeat skeleton must contain 15 actors")
    if sum(len(event_ids) == 3 for event_ids in registry_repeats.values()) != 3:
        raise ValueError("exactly three registry actors must span all three events")
    if len(human_event_repeats) != 6:
        raise ValueError("six human-reviewed event-only identities must repeat")

    bridge_lookup = {row["entity_key"]: row for row in tables["bridges"]}
    if len(bridge_lookup) != 21 or len(tables["bridges"]) != 21:
        raise ValueError("current R5 bridge table must contain 21 unique identities")
    expected_bridge_keys = {
        *(f"ACTOR:{key}" for key in registry_repeats),
        *(f"EVENT_ONLY:{key}" for key in human_event_repeats),
    }
    if set(bridge_lookup) != expected_bridge_keys:
        raise ValueError("R5 bridge table disagrees with current participation identities")
    if Counter(row["identity_scope"] for row in tables["bridges"]) != Counter(
        {"registry_actor": 15, "human_reviewed_event_only": 6}
    ):
        raise ValueError("R5 bridge identity scopes must remain 15 registry plus 6 event-only")
    for entity_key, event_ids in {
        **{f"ACTOR:{key}": value for key, value in registry_repeats.items()},
        **{
            f"EVENT_ONLY:{key}": value
            for key, value in human_event_repeats.items()
        },
    }.items():
        bridge = bridge_lookup[entity_key]
        if int(bridge["event_count"]) != len(event_ids):
            raise ValueError(f"bridge event_count drift for {entity_key}")
        if set(bridge["event_ids"].split(";")) != event_ids:
            raise ValueError(f"bridge event_ids drift for {entity_key}")

    derived_overlaps = registry_pairwise_overlap(registry_events)
    observed_overlaps: dict[tuple[str, str], int] = {}
    if len(tables["overlaps"]) != 3:
        raise ValueError("R5 overlap table must contain exactly three pairs")
    for row in tables["overlaps"]:
        key = (row["event_a"], row["event_b"])
        observed_overlaps[key] = int(row["shared_confirmed_registry_actors"])
        event_a_count = EXPECTED_EVENT_IDENTITY_COUNTS[key[0]]["registry_actor"]
        event_b_count = EXPECTED_EVENT_IDENTITY_COUNTS[key[1]]["registry_actor"]
        if int(row["confirmed_registry_actors_a"]) != event_a_count:
            raise ValueError(f"overlap event-a registry count drift for {key}")
        if int(row["confirmed_registry_actors_b"]) != event_b_count:
            raise ValueError(f"overlap event-b registry count drift for {key}")
    if observed_overlaps != derived_overlaps:
        raise ValueError("R5 overlap table disagrees with current registry identities")
    if observed_overlaps != {
        ("EV2010_WWF_67", "EV2015_NACSJ_31"): 10,
        ("EV2010_WWF_67", "EV2020_OEJP_MMC_71"): 8,
        ("EV2015_NACSJ_31", "EV2020_OEJP_MMC_71"): 3,
    }:
        raise ValueError(f"unexpected current R5 registry overlaps: {observed_overlaps}")


def summarize(tables: dict[str, list[dict[str, str]]]) -> dict[str, object]:
    participation = tables["participation"]
    event_lookup = {row["event_id"]: row for row in tables["events"]}
    event_identity_counts = {
        event_id: Counter(
            row["identity_status"]
            for row in participation
            if row["event_id"] == event_id
        )
        for event_id in EVENT_IDS
    }
    registry_events = identity_event_sets(participation, "registry_actor")
    human_event_events = identity_event_sets(
        participation, "event_only_identity_human_checked"
    )
    registry_repeats = {
        key: event_ids for key, event_ids in registry_events.items() if len(event_ids) >= 2
    }
    human_event_repeats = {
        key: event_ids
        for key, event_ids in human_event_events.items()
        if len(event_ids) >= 2
    }
    return {
        "total_rows": len(participation),
        "event_lookup": event_lookup,
        "event_identity_counts": event_identity_counts,
        "registry_repeat_count": len(registry_repeats),
        "registry_all_three_count": sum(
            len(event_ids) == 3 for event_ids in registry_repeats.values()
        ),
        "human_event_only_repeat_count": len(human_event_repeats),
        "registry_pairwise_overlap": registry_pairwise_overlap(registry_events),
    }


def build_export_rows(summary: dict[str, object]) -> list[dict[str, object]]:
    event_lookup = summary["event_lookup"]
    event_identity_counts = summary["event_identity_counts"]
    registry_overlaps = summary["registry_pairwise_overlap"]
    assert isinstance(event_lookup, dict)
    assert isinstance(event_identity_counts, dict)
    assert isinstance(registry_overlaps, dict)

    rows: list[dict[str, object]] = []
    for event_id in EVENT_IDS:
        event = event_lookup[event_id]
        counts = event_identity_counts[event_id]
        rows.append(
            {
                "event": EVENT_LABELS[event_id],
                "source_list_rows": int(event["structured_participant_count"]),
                "confirmed_registry_rows": counts["registry_actor"],
                "target_or_venue": TARGET_LABELS[event_id],
                "action": ACTION_LABELS[event_id],
            }
        )
    pair_labels = {
        ("EV2010_WWF_67", "EV2015_NACSJ_31"): "2010↔2015",
        ("EV2010_WWF_67", "EV2020_OEJP_MMC_71"): "2010↔2020",
        ("EV2015_NACSJ_31", "EV2020_OEJP_MMC_71"): "2015↔2020",
    }
    for key, label in pair_labels.items():
        rows.append(
            {
                "event": label,
                "source_list_rows": "",
                "confirmed_registry_rows": registry_overlaps[key],
                "target_or_venue": "registry 两事件重叠",
                "action": "",
            }
        )
    rows.extend(
        [
            {
                "event": "至少出现两次",
                "source_list_rows": "",
                "confirmed_registry_rows": summary["registry_repeat_count"],
                "target_or_venue": "registry 重复骨架",
                "action": "",
            },
            {
                "event": "贯穿三次",
                "source_list_rows": "",
                "confirmed_registry_rows": summary["registry_all_three_count"],
                "target_or_venue": "registry 重复骨架",
                "action": "",
            },
            {
                "event": "人审 event-only 跨事件",
                "source_list_rows": "",
                "confirmed_registry_rows": summary["human_event_only_repeat_count"],
                "target_or_venue": "registry 外身份层",
                "action": "",
            },
        ]
    )
    return rows


def configure_plotting() -> None:
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    candidates = [
        "Microsoft YaHei",
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "SimHei",
        "DejaVu Sans",
    ]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    font = next((name for name in candidates if name in installed), "DejaVu Sans")
    plt.rcParams.update(
        {
            "font.family": font,
            "axes.unicode_minus": False,
            "figure.facecolor": "#F7F5F1",
            "savefig.facecolor": "#F7F5F1",
            "svg.fonttype": "none",
            "svg.hashsalt": "formal-comm-v2-r5-current",
        }
    )


def add_box(
    figure,
    x: float,
    y: float,
    width: float,
    height: float,
    facecolor: str,
    *,
    edgecolor: str = "#C7C7C3",
    linewidth: float = 1.0,
):
    from matplotlib.patches import FancyBboxPatch

    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        transform=figure.transFigure,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
    )
    figure.add_artist(box)
    return box


def render_figure(summary: dict[str, object]):
    import matplotlib.pyplot as plt

    configure_plotting()
    figure = plt.figure(figsize=(13.33, 7.5))
    ink = "#18364B"
    text = "#27333B"
    muted = "#68747C"
    teal = "#2F7F79"
    teal_light = "#DCEBE8"
    blue = "#397596"
    blue_light = "#DCE8EE"
    orange = "#C97927"
    orange_light = "#F0D6AE"
    purple = "#75629A"
    purple_light = "#E7E1EE"
    rust = "#9A513C"

    figure.text(
        0.055,
        0.945,
        "公开行动呈现小型 registry 骨架与事件性重组外围",
        ha="left",
        va="top",
        fontsize=22.5,
        fontweight="bold",
        color=ink,
    )
    figure.text(
        0.055,
        0.893,
        "三次目的性公开行动共 169 条名单观察；registry 层 15 个组织至少重复一次，3 个贯穿三次。",
        ha="left",
        va="top",
        fontsize=11.2,
        color=muted,
    )

    event_lookup = summary["event_lookup"]
    event_identity_counts = summary["event_identity_counts"]
    assert isinstance(event_lookup, dict)
    assert isinstance(event_identity_counts, dict)
    card_x = (0.055, 0.365, 0.675)
    accents = (blue, teal, orange)
    lights = (blue_light, teal_light, orange_light)
    for event_id, x, accent, light in zip(EVENT_IDS, card_x, accents, lights):
        event = event_lookup[event_id]
        counts = event_identity_counts[event_id]
        add_box(figure, x, 0.50, 0.27, 0.275, "#EFEEE9", edgecolor="#D2D1CC")
        add_box(
            figure,
            x + 0.018,
            0.688,
            0.234,
            0.054,
            light,
            edgecolor=accent,
        )
        figure.text(
            x + 0.135,
            0.715,
            EVENT_LABELS[event_id],
            ha="center",
            va="center",
            fontsize=10.3,
            fontweight="bold",
            color=accent,
        )
        figure.text(
            x + 0.057,
            0.625,
            event["structured_participant_count"],
            ha="center",
            va="center",
            fontsize=25,
            fontweight="bold",
            color=ink,
        )
        figure.text(
            x + 0.057,
            0.584,
            "来源名单行",
            ha="center",
            va="center",
            fontsize=8.5,
            color=muted,
        )
        figure.text(
            x + 0.195,
            0.625,
            str(counts["registry_actor"]),
            ha="center",
            va="center",
            fontsize=25,
            fontweight="bold",
            color=accent,
        )
        figure.text(
            x + 0.195,
            0.584,
            "当前 registry 行",
            ha="center",
            va="center",
            fontsize=8.5,
            color=muted,
        )
        figure.text(
            x + 0.135,
            0.547,
            (
                f"另：人审 event-only {counts['event_only_identity_human_checked']}  "
                f"｜  其他名称 {counts['event_only_name']}"
            ),
            ha="center",
            va="center",
            fontsize=8.15,
            color=muted,
        )
        figure.text(
            x + 0.135,
            0.515,
            f"{ACTION_LABELS[event_id]} → {TARGET_LABELS[event_id]}",
            ha="center",
            va="center",
            fontsize=8.3,
            color=text,
        )

    overlaps = summary["registry_pairwise_overlap"]
    assert isinstance(overlaps, dict)
    overlap_specs = [
        (
            0.28,
            "2010 与 2015",
            overlaps[("EV2010_WWF_67", "EV2015_NACSJ_31")],
            blue,
        ),
        (
            0.47,
            "2010 与 2020",
            overlaps[("EV2010_WWF_67", "EV2020_OEJP_MMC_71")],
            teal,
        ),
        (
            0.66,
            "2015 与 2020",
            overlaps[("EV2015_NACSJ_31", "EV2020_OEJP_MMC_71")],
            orange,
        ),
    ]
    for x, label, value, accent in overlap_specs:
        add_box(figure, x, 0.39, 0.15, 0.072, "#E9ECEE", edgecolor=accent)
        figure.text(
            x + 0.075,
            0.436,
            label,
            ha="center",
            va="center",
            fontsize=8.4,
            color=muted,
        )
        figure.text(
            x + 0.075,
            0.407,
            f"registry 重叠 {value}",
            ha="center",
            va="center",
            fontsize=10.5,
            fontweight="bold",
            color=accent,
        )

    add_box(figure, 0.055, 0.155, 0.89, 0.17, "#EFEEE9")
    add_box(figure, 0.075, 0.207, 0.155, 0.085, teal_light, edgecolor=teal)
    figure.text(
        0.1525,
        0.261,
        f"{summary['registry_repeat_count']} 个",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color=teal,
    )
    figure.text(
        0.1525,
        0.229,
        "registry 至少两次",
        ha="center",
        va="center",
        fontsize=8.5,
        color=muted,
    )
    add_box(figure, 0.25, 0.207, 0.155, 0.085, purple_light, edgecolor=purple)
    figure.text(
        0.3275,
        0.261,
        f"{summary['registry_all_three_count']} 个",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color=purple,
    )
    figure.text(
        0.3275,
        0.229,
        "registry 贯穿三次",
        ha="center",
        va="center",
        fontsize=8.5,
        color=muted,
    )
    figure.text(
        0.445,
        0.263,
        "小型 registry 重复骨架在不同对象之间持续接入，\n较大的事件参与外围则随具体行动重新组合。",
        ha="left",
        va="center",
        fontsize=10.8,
        fontweight="bold",
        color=ink,
    )
    figure.text(
        0.075,
        0.18,
        (
            f"另有 {summary['human_event_only_repeat_count']} 个经人审 event-only identity "
            "跨事件重复；因未进入 registry，单列而不并入组织骨架。"
        ),
        ha="left",
        va="center",
        fontsize=8.8,
        color=rust,
    )
    figure.text(
        0.055,
        0.065,
        "边界：三个名单均为目的性样本；同场或重复署名只表示公开参与，不等于成员关系、稳定联盟或持续协调。",
        fontsize=8.9,
        color=rust,
    )
    return figure


def render_current(
    participation_path: Path = DEFAULT_PARTICIPATION_PATH,
    r5_dir: Path = DEFAULT_R5_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> list[Path]:
    import matplotlib.pyplot as plt

    tables = load_current(participation_path, r5_dir)
    validate_current(tables)
    summary = summarize(tables)
    output_dir = Path(output_dir)
    data_path = output_dir / "data" / DATA_FILENAME
    figure_path = output_dir / "fig" / FIGURE_FILENAME
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(data_path, build_export_rows(summary))
    figure = render_figure(summary)
    figure.savefig(
        figure_path,
        dpi=180,
        facecolor="#F7F5F1",
        bbox_inches="tight",
        pad_inches=0.12,
        metadata={"Software": "render_formal_comm_v2_r5_current.py"},
    )
    plt.close(figure)
    return [data_path, figure_path]


def main() -> None:
    written = render_current()
    print(
        "Current formal_comm_v2 R5 figure written: "
        + ", ".join(str(path.relative_to(ROOT)) for path in written)
    )


if __name__ == "__main__":
    main()
