"""Render the current R9 election-civic non-causal mechanism figure.

This is deliberately a render-only script. It reads the current HR-026-merged
actor-event table plus the two module-local aggregate tables, validates that
they describe the same 19 human-reviewed records, and writes only the F030
PNG/SVG plus a standalone HTML preview. It never edits facts, review queues,
report manifests, captions, or control documents.
"""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVENTS_PATH = ROOT / "data" / "interim" / "33_r09_election_civic_events_v1.csv"
DEFAULT_MODULE_DIR = ROOT / "outputs" / "R09_election_civic_interface_v1"
DEFAULT_OUTPUT_DIR = DEFAULT_MODULE_DIR

MODE_FILENAME = "intervention_mode_counts_v1.csv"
WINDOW_FILENAME = "three_election_windows_v1.csv"
OUTPUT_FILENAMES = {
    "fig_r09_noncausal_mechanism_v1.png",
    "fig_r09_noncausal_mechanism_v1.svg",
    "fig_r09_noncausal_mechanism_v1.html",
}

YEARS = ("2014", "2018", "2022")
ACTIONS = (
    "endorsement",
    "issue_campaign",
    "public_meeting",
    "request",
    "observation",
)
ACTION_LABELS = {
    "endorsement": "公开支持",
    "issue_campaign": "议题行动",
    "public_meeting": "公共讨论",
    "request": "请求／提案",
    "observation": "观察／信息",
}
EXPECTED_ACTION_COUNTS = Counter(
    {
        "observation": 5,
        "endorsement": 4,
        "issue_campaign": 4,
        "request": 4,
        "public_meeting": 2,
    }
)
EXPECTED_YEAR_COUNTS = Counter({"2014": 5, "2018": 7, "2022": 7})


def read_csv(path: Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_current(
    events_path: Path = DEFAULT_EVENTS_PATH,
    module_dir: Path = DEFAULT_MODULE_DIR,
) -> dict[str, list[dict[str, str]]]:
    """Read only the current central events and current module aggregates."""
    module_dir = Path(module_dir)
    return {
        "events": read_csv(Path(events_path)),
        "modes": read_csv(module_dir / MODE_FILENAME),
        "windows": read_csv(module_dir / WINDOW_FILENAME),
    }


def validate_current(tables: dict[str, list[dict[str, str]]]) -> None:
    """Reject stale, candidate, or internally inconsistent election layers."""
    events = tables["events"]
    if len(events) != 19 or len({row["record_id"] for row in events}) != 19:
        raise ValueError("current R9 election layer must contain 19 unique records")
    if {row["election_year"] for row in events} != set(YEARS):
        raise ValueError("current R9 election layer must cover 2014, 2018 and 2022")
    if any(row["review_status"] != "human_checked" for row in events):
        raise ValueError("F030 may only render the fully human-checked HR-026 layer")
    if any(not row["human_review_decision"] for row in events):
        raise ValueError("every F030 record must retain a human review decision")

    event_statuses = Counter(row["event_status"] for row in events)
    expected_statuses = Counter(
        {
            "confirmed_observed_action": 18,
            "announced_not_occurrence_verified": 1,
        }
    )
    if event_statuses != expected_statuses:
        raise ValueError(f"unexpected R9 event-status boundary: {event_statuses}")
    announced = [
        row
        for row in events
        if row["event_status"] == "announced_not_occurrence_verified"
    ]
    if len(announced) != 1 or announced[0]["record_id"] != "R9EC018":
        raise ValueError("R9EC018 must be the sole announcement-only observation")
    if announced[0]["action_type"] != "public_meeting":
        raise ValueError("R9EC018 must remain an announcement-only public meeting")

    action_counts = Counter(row["action_type"] for row in events)
    if action_counts != EXPECTED_ACTION_COUNTS:
        raise ValueError(f"unexpected R9 action counts: {action_counts}")
    year_counts = Counter(row["election_year"] for row in events)
    if year_counts != EXPECTED_YEAR_COUNTS:
        raise ValueError(f"unexpected R9 year counts: {year_counts}")

    modes = tables["modes"]
    if len(modes) != len(YEARS) * len(ACTIONS):
        raise ValueError("module action table must contain 15 year×action rows")
    mode_keys = {(row["election_year"], row["action_type"]) for row in modes}
    if mode_keys != {(year, action) for year in YEARS for action in ACTIONS}:
        raise ValueError("module action table has a missing or unexpected year×action row")
    for row in modes:
        matching = [
            event
            for event in events
            if event["election_year"] == row["election_year"]
            and event["action_type"] == row["action_type"]
        ]
        expected = (
            len(matching),
            sum(
                event["event_status"] == "confirmed_observed_action"
                for event in matching
            ),
            sum(
                event["event_status"] == "announced_not_occurrence_verified"
                for event in matching
            ),
        )
        observed = (
            int(row["candidate_row_count"]),
            int(row["confirmed_observed_action_count"]),
            int(row["announced_not_occurrence_verified_count"]),
        )
        if observed != expected:
            raise ValueError(
                "module action aggregate disagrees with current events for "
                f"{row['election_year']} {row['action_type']}: {observed} != {expected}"
            )

    windows = tables["windows"]
    if len(windows) != 3 or {row["election_year"] for row in windows} != set(YEARS):
        raise ValueError("module window table must contain exactly three election years")
    for row in windows:
        matching = [
            event for event in events if event["election_year"] == row["election_year"]
        ]
        expected = (
            len(matching),
            sum(
                event["event_status"] == "confirmed_observed_action"
                for event in matching
            ),
            sum(
                event["event_status"] == "announced_not_occurrence_verified"
                for event in matching
            ),
        )
        observed = (
            int(row["candidate_event_rows"]),
            int(row["confirmed_observed_action_rows"]),
            int(row["announced_not_occurrence_verified_rows"]),
        )
        if observed != expected:
            raise ValueError(
                "module election-window aggregate disagrees with current events for "
                f"{row['election_year']}: {observed} != {expected}"
            )


def summarize(events: list[dict[str, str]]) -> dict[str, object]:
    action_counts = Counter(row["action_type"] for row in events)
    year_action_counts: dict[str, Counter[str]] = {
        year: Counter(
            row["action_type"] for row in events if row["election_year"] == year
        )
        for year in YEARS
    }
    year_status_counts: dict[str, Counter[str]] = {
        year: Counter(
            row["event_status"] for row in events if row["election_year"] == year
        )
        for year in YEARS
    }
    return {
        "total": len(events),
        "confirmed": sum(
            row["event_status"] == "confirmed_observed_action" for row in events
        ),
        "announced": sum(
            row["event_status"] == "announced_not_occurrence_verified"
            for row in events
        ),
        "action_counts": action_counts,
        "year_action_counts": year_action_counts,
        "year_status_counts": year_status_counts,
    }


def setup_plotting() -> None:
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
            "figure.facecolor": "#F6F3EC",
            "savefig.facecolor": "#F6F3EC",
            "svg.fonttype": "none",
            "svg.hashsalt": "r9-election-current-v1",
        }
    )


def add_panel(
    ax,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    facecolor: str,
    edgecolor: str = "#42534D",
    linestyle: str = "-",
    linewidth: float = 1.4,
):
    from matplotlib.patches import FancyBboxPatch

    panel = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        transform=ax.transAxes,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        linestyle=linestyle,
    )
    ax.add_patch(panel)
    return panel


def add_flow_arrow(ax, start: tuple[float, float], end: tuple[float, float]) -> None:
    from matplotlib.patches import FancyArrowPatch

    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=ax.transAxes,
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=1.5,
            color="#52635D",
        )
    )


def year_summary_lines(
    action_counts: Counter[str],
    status_counts: Counter[str],
) -> tuple[str, str]:
    parts = [
        f"{ACTION_LABELS[action]} {action_counts[action]}"
        for action in ACTIONS
        if action_counts[action]
    ]
    return (
        " · ".join(parts),
        (
            f"确认发生 {status_counts['confirmed_observed_action']}  "
            f"｜  仅预告 {status_counts['announced_not_occurrence_verified']}"
        ),
    )


def render_figure(summary: dict[str, object]):
    import matplotlib.pyplot as plt

    setup_plotting()
    fig, ax = plt.subplots(figsize=(14, 7.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(
        0.045,
        0.945,
        "R9 选举—市民组织接口：可观察顺序，不是选举因果",
        fontsize=24,
        fontweight="bold",
        ha="left",
        va="top",
        color="#17231F",
    )
    fig.text(
        0.046,
        0.892,
        "HR-026 已合并；箭头只组织资料中的公开行动与接口，不表示行动导致得票、胜负或政策结果。",
        fontsize=11.5,
        ha="left",
        va="top",
        color="#5C6763",
    )

    add_panel(ax, 0.045, 0.515, 0.185, 0.29, facecolor="#DDE9E5")
    ax.text(
        0.065,
        0.765,
        "人审事实入口",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color="#1C302A",
    )
    ax.text(
        0.065,
        0.675,
        str(summary["total"]),
        transform=ax.transAxes,
        fontsize=34,
        fontweight="bold",
        color="#1E6D5B",
    )
    ax.text(
        0.119,
        0.685,
        "条 actor–event 观察",
        transform=ax.transAxes,
        fontsize=11,
        color="#34443F",
    )
    ax.text(
        0.065,
        0.615,
        f"{summary['confirmed']} 条确认发生",
        transform=ax.transAxes,
        fontsize=11.5,
        fontweight="bold",
        color="#246A57",
    )
    ax.text(
        0.065,
        0.565,
        f"{summary['announced']} 条仅有预告",
        transform=ax.transAxes,
        fontsize=11.5,
        fontweight="bold",
        color="#A46817",
    )

    add_flow_arrow(ax, (0.232, 0.66), (0.275, 0.66))
    add_panel(ax, 0.278, 0.515, 0.215, 0.29, facecolor="#E9DECC")
    ax.text(
        0.298,
        0.765,
        "公开介入方式（记录数）",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color="#3B2F24",
    )
    action_counts = summary["action_counts"]
    assert isinstance(action_counts, Counter)
    display_actions = (
        "observation",
        "endorsement",
        "issue_campaign",
        "request",
        "public_meeting",
    )
    for index, action in enumerate(display_actions):
        suffix = " *" if action == "public_meeting" else ""
        ax.text(
            0.305,
            0.713 - index * 0.041,
            f"{ACTION_LABELS[action]}",
            transform=ax.transAxes,
            fontsize=10.8,
            color="#463C33",
        )
        ax.text(
            0.466,
            0.713 - index * 0.041,
            f"{action_counts[action]}{suffix}",
            transform=ax.transAxes,
            fontsize=10.8,
            fontweight="bold",
            ha="right",
            color="#463C33",
        )
    ax.text(
        0.305,
        0.535,
        "* 公共讨论含 1 条仅预告记录",
        transform=ax.transAxes,
        fontsize=8.6,
        color="#8B5F22",
    )

    add_flow_arrow(ax, (0.495, 0.66), (0.538, 0.66))
    add_panel(ax, 0.541, 0.515, 0.185, 0.29, facecolor="#DDE5F0")
    ax.text(
        0.561,
        0.765,
        "可观察公共接口",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color="#26394A",
    )
    for index, line in enumerate(
        (
            "出马／政策请求",
            "议题公开行动",
            "讨论／问卷／政策比较",
            "组织声明与选后解释",
        )
    ):
        ax.text(
            0.6335,
            0.704 - index * 0.047,
            line,
            transform=ax.transAxes,
            fontsize=10.8,
            ha="center",
            color="#334858",
        )
    ax.text(
        0.6335,
        0.545,
        "只编码公开可核的角色与记录",
        transform=ax.transAxes,
        fontsize=8.8,
        ha="center",
        color="#637687",
    )

    add_flow_arrow(ax, (0.728, 0.66), (0.771, 0.66))
    add_panel(ax, 0.774, 0.515, 0.18, 0.29, facecolor="#DDE8D2")
    ax.text(
        0.794,
        0.765,
        "资料可以说明",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color="#2F472A",
    )
    for index, line in enumerate(
        (
            "谁／何种事件节点",
            "何时公开介入",
            "采用何种行动形式",
            "留下何种公开记录",
        )
    ):
        ax.text(
            0.864,
            0.704 - index * 0.047,
            line,
            transform=ax.transAxes,
            fontsize=10.8,
            ha="center",
            color="#3E5638",
        )
    ax.text(
        0.864,
        0.545,
        "临时 collective 不自动 actor 化",
        transform=ax.transAxes,
        fontsize=8.8,
        ha="center",
        color="#66775E",
    )

    year_action_counts = summary["year_action_counts"]
    year_status_counts = summary["year_status_counts"]
    assert isinstance(year_action_counts, dict)
    assert isinstance(year_status_counts, dict)
    year_x = {"2014": 0.045, "2018": 0.355, "2022": 0.665}
    for year in YEARS:
        add_panel(
            ax,
            year_x[year],
            0.255,
            0.29,
            0.16,
            facecolor="#FBFAF6",
            edgecolor="#A89D8E",
            linewidth=1.1,
        )
        action_line, status_line = year_summary_lines(
            year_action_counts[year],
            year_status_counts[year],
        )
        ax.text(
            year_x[year] + 0.018,
            0.375,
            year,
            transform=ax.transAxes,
            fontsize=17,
            fontweight="bold",
            color="#1F6B63",
        )
        ax.text(
            year_x[year] + 0.018,
            0.329,
            action_line,
            transform=ax.transAxes,
            fontsize=9.3,
            color="#3F4643",
        )
        ax.text(
            year_x[year] + 0.018,
            0.282,
            status_line,
            transform=ax.transAxes,
            fontsize=9.2,
            color="#6B655D",
        )

    add_panel(
        ax,
        0.045,
        0.075,
        0.91,
        0.095,
        facecolor="#F2D9D5",
        edgecolor="#A9544B",
        linestyle="--",
        linewidth=1.5,
    )
    ax.text(
        0.065,
        0.132,
        "本资料不能识别",
        transform=ax.transAxes,
        fontsize=12.5,
        fontweight="bold",
        color="#8B3932",
    )
    ax.text(
        0.205,
        0.132,
        "票数变化  ·  投票率变化  ·  胜负原因  ·  说服效果  ·  政策吸收  ·  稳定联盟",
        transform=ax.transAxes,
        fontsize=11.1,
        color="#8B3932",
    )
    ax.text(
        0.065,
        0.095,
        "R9EC018 仅确认活动预告；未找到会后记录，因此不计入已举行事件。",
        transform=ax.transAxes,
        fontsize=9.3,
        color="#75423D",
    )
    fig.tight_layout(pad=0)
    return fig


def standalone_html(svg: str) -> str:
    title = "R9 选举—市民组织非因果接口机制"
    return (
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>body{margin:0;background:#eceae4}"
        "main{max-width:1400px;margin:24px auto;background:#fff;"
        "box-shadow:0 8px 28px #0002}svg{display:block;width:100%;height:auto}"
        "</style></head><body><main>"
        f"{svg}</main></body></html>\n"
    )


def render_current(
    events_path: Path = DEFAULT_EVENTS_PATH,
    module_dir: Path = DEFAULT_MODULE_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> set[Path]:
    """Validate current data and write only the three declared F030 assets."""
    tables = load_current(Path(events_path), Path(module_dir))
    validate_current(tables)
    summary = summarize(tables["events"])

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "fig_r09_noncausal_mechanism_v1.png"
    svg_path = output_dir / "fig_r09_noncausal_mechanism_v1.svg"
    html_path = output_dir / "fig_r09_noncausal_mechanism_v1.html"

    fig = render_figure(summary)
    fig.savefig(
        png_path,
        dpi=180,
        bbox_inches="tight",
        metadata={"Software": "render_r09_election_mechanism_current.py"},
    )
    fig.savefig(
        svg_path,
        bbox_inches="tight",
        metadata={
            "Creator": "render_r09_election_mechanism_current.py",
            "Date": "2026-07-20",
        },
    )
    import matplotlib.pyplot as plt

    plt.close(fig)
    svg = (
        "\n".join(
            line.rstrip()
            for line in svg_path.read_text(encoding="utf-8").splitlines()
        )
        + "\n"
    )
    svg_path.write_text(svg, encoding="utf-8")
    html_path.write_text(standalone_html(svg), encoding="utf-8")

    written = {png_path, svg_path, html_path}
    if {path.name for path in written} != OUTPUT_FILENAMES:
        raise ValueError("F030 renderer output set drifted beyond declared assets")
    return written


def main() -> None:
    written = render_current()
    print(
        "Current R9 F030 render OK: "
        f"{len(written)} assets from 19 human-checked rows "
        "(18 confirmed observed actions + 1 announcement-only)."
    )


if __name__ == "__main__":
    main()
