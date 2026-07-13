"""Build the standalone HR-016 human-review packet for R4 Sakishima."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "outputs" / "R04_sakishima_frame_corpus_v0"
ACTOR_QUEUE = MODULE / "human_review_queue_v0.csv"
SOURCE_QUEUE = MODULE / "source_review_queue_v0.csv"
SAFE_SOURCES = MODULE / "online_evidence_safe_sources_v0.csv"
SOURCE_CANDIDATES = MODULE / "source_excerpt_locators_v0.csv"
OUTPUT_CSV = MODULE / "hr016_review_items_v0.csv"
OUTPUT_MD = MODULE / "HR016_human_review_packet.md"

EXPECTED_ACTORS = {"R4E001", "R4E008", "R4E009", "R4E016", "R4E017", "R4E024", "R4E025"}
EXPECTED_SOURCES = {"R4S002", "R4S007", "R4S008", "R4S015", "R4S024"}

ACTOR_QUESTIONS = {
    "R4E001": (
        "R4S003 具名的是“6・11自衛隊配備を止める市民集会”実行委員会。请判定它是否与 A012 "
        "为同一持续组织；若不能确认，是否 revise 为一次性 provisional event committee，只保留 2016 集会层级？"
    ),
    "R4E008": (
        "请把久貝美奈子议员的提问与総務部長答复分开，判定 local_autonomy_referendum 是否只能归给"
        "具名议员个人，而不能归给整个宫古岛市议会。"
    ),
    "R4E009": (
        "请核 R4S008 中台湾有事／全岛撤离陈述的具体 speaker，判定 F_FTE 应归给久貝美奈子个人、"
        "行政答复方，还是因归属不清而拒绝。"
    ),
    "R4E016": (
        "请逐条核 R4S015 的匿名居民发言与箭头后的行政答复，判定是否可将 F_FTE 仅编码为“该场 23 人"
        "意见交换会中的匿名发言”，而不建立 RESIDENTS_ISHIGAKI 稳定 actor。"
    ),
    "R4E017": (
        "请逐条核 R4S015 中关于撤离义务与决策的匿名问题，判定 F_AUT 是否可保留为会议样本中的匿名"
        "程序疑问；不得概括为石垣全体居民立场。"
    ),
    "R4E024": (
        "R4S024 只直接证明防卫省举办新导弹部队说明会及其“增进理解”目的。请判定本行是否 revise 为"
        " MOD_JAPAN 的 F_FTE 制度事件；没有居民程序评价时不得保留 F_PROC。"
    ),
    "R4E025": (
        "R4S021 覆盖先岛五市町村。请判定是否 revise 为 place=Sakishima 的区域级 GOV_OKINAWA_PREF "
        "life_safety 观察；不得作为与那国特有事实。"
    ),
}

ACTOR_IMPACTS = {
    "R4E001": ("R4E001（若通过则新增/修订正式事实）", "entity-frame 图与 R4 brief；三地 source 图当前已计 R4S003"),
    "R4E008": ("候选 R4E008", "entity-frame 图、三地 source 图与 R4 brief"),
    "R4E009": ("候选 R4E009", "entity-frame 图、三地 source 图与 R4 brief"),
    "R4E016": ("候选 R4E016", "entity-frame 图、三地 source 图与 R4 brief"),
    "R4E017": ("候选 R4E017", "entity-frame 图、三地 source 图与 R4 brief"),
    "R4E024": ("候选 R4E024", "entity-frame 图、三地 source 图与与那国解释"),
    "R4E025": ("候选 R4E025（只能区域级）", "entity-frame 图与区域背景；不得增加与那国专属计数"),
}

ACTOR_BOUNDARIES = {
    "R4E001": "默认不 crosswalk 到 A012；保留一次性事件委员会候选，不证明组织持续性。",
    "R4E008": "个人议员不等于市议会；待 speaker 人审前不进正式事实。",
    "R4E009": "个人提问、行政答复和议会机构必须分开；预案讨论不等于实际撤离。",
    "R4E016": "匿名 23 人会议样本不等于全市居民，也不形成稳定 actor。",
    "R4E017": "匿名程序疑问不等于统一自治立场；待逐条 speaker 复核。",
    "R4E024": "说明会存在不等于程序公平或居民同意；默认只保留候选 F_FTE。",
    "R4E025": "先岛区域材料不得落为与那国特有事实。",
}

SOURCE_QUESTIONS = {
    "R4S002": (
        "请确认 p.6 地下水文字的 speaker 是县环境部行政回应还是陈情者原文。若只确认行政回应，是否"
        " revise 为 government_response 的地下水背景来源，并继续禁止回指 A013？"
    ),
    "R4S007": (
        "请在 PDF 中补出 Pattern 1 的稳定印刷页码，并确认“市全域の住民及び観光客”所在页；页码可"
        "复核后才可 accept 到安全来源及 R4E007 source_ref。"
    ),
    "R4S008": (
        "请按印刷 p.139–140 分段标出久貝美奈子提问与総務部長上地俊暢答复，分别判定 F_AUT、F_FTE"
        " 与 life_safety 的 speaker 归属。"
    ),
    "R4S015": (
        "请逐条拆分 p.1 起的匿名居民意见与箭头后的防灾危机管理课答复，并判断哪些短句可进入 F_FTE"
        " 或 F_AUT；23 名参加者不得代表全市。"
    ),
    "R4S024": (
        "请确认正文第16行只支持说明会事件及防卫省宣称的“增进理解”目的。若无居民回应或程序评价，"
        "是否 revise 为 F_FTE-only source，并拒绝 procedural_fairness？"
    ),
}

SOURCE_IMPACTS = {
    "R4S002": ("不自动恢复 R4E002；若要归给 A013 必须另有具名陈情原文", "三地 source 图的宫古地下水计数及 brief"),
    "R4S007": ("正式 R4E007 的 source_ref 可补入 R4S007", "三地 source 图的宫古 F_FTE/life_safety 计数"),
    "R4S008": ("候选 R4E008、R4E009", "entity-frame 图、三地 source 图与 brief"),
    "R4S015": ("候选 R4E016、R4E017", "entity-frame 图、三地 source 图与 brief"),
    "R4S024": ("候选 R4E024", "entity-frame 图、三地 source 图与与那国解释"),
}

SOURCE_BOUNDARIES = {
    "R4S002": "行政答复不能替代 A013 的自有措辞；默认留在 source 人审队列。",
    "R4S007": "没有稳定页码前不进入安全 source register。",
    "R4S008": "个人议员、行政官员与议会机构不得合并。",
    "R4S015": "匿名居民、行政答复与全市居民不得合并。",
    "R4S024": "举办说明会不证明 procedural fairness 或居民同意。",
}


FIELDS = [
    "review_item_id",
    "item_type",
    "original_id",
    "related_ids",
    "place",
    "precise_question",
    "open_url",
    "source_locator",
    "existing_source_ids",
    "decision_options",
    "affected_formal_fact",
    "affected_figures_or_brief",
    "default_boundary",
    "review_decision",
    "human_reviewer",
    "review_date",
    "review_note",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def join_unique(values: list[str]) -> str:
    return ";".join(dict.fromkeys(value for value in values if value))


def render_packet(rows: list[dict[str, str]]) -> str:
    lines = [
        "# HR-016：R4 先岛框架人工复核包",
        "",
        "范围：7 条 actor/frame semantic-human 项与 5 条 source locator/speaker 项。",
        "",
        "## 复核方法",
        "",
        "1. 打开 CSV 中的 URL，并按 source locator 回到原页。",
        "2. 在 `review_decision` 填 `accept`、`revise` 或 `reject`；同时填写 reviewer、日期与理由。",
        "3. `revise` 必须写明修订后的 actor/speaker、place、frame 或 locator。",
        "4. 人审完成前，12 项均不进入正式事实或图；人物不等于机构、匿名样本不等于总体、会议不等于同意。",
        "",
        "## Actor / frame（7）",
        "",
    ]
    for row in [item for item in rows if item["item_type"] == "actor_frame_semantic"]:
        lines.extend(
            [
                f"### {row['review_item_id']} · {row['original_id']}",
                "",
                f"- 问题：{row['precise_question']}",
                f"- 打开：{row['open_url']}；定位：{row['source_locator']}",
                f"- 影响：{row['affected_formal_fact']}；{row['affected_figures_or_brief']}",
                f"- 默认边界：{row['default_boundary']}",
                "",
            ]
        )
    lines.extend(["## Source locator / speaker（5）", ""])
    for row in [item for item in rows if item["item_type"] == "source_locator_speaker"]:
        lines.extend(
            [
                f"### {row['review_item_id']} · {row['original_id']}",
                "",
                f"- 问题：{row['precise_question']}",
                f"- 打开：{row['open_url']}；定位：{row['source_locator']}",
                f"- 影响：{row['affected_formal_fact']}；{row['affected_figures_or_brief']}",
                f"- 默认边界：{row['default_boundary']}",
                "",
            ]
        )
    lines.extend(
        [
            "## 完成条件",
            "",
            "CSV 12 条均有决定、复核者、日期和理由；所有 revise 项写明新编码。完成前不得更新正式事实或图。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    actor_rows = read_csv(ACTOR_QUEUE)
    source_rows = read_csv(SOURCE_QUEUE)
    all_sources = {
        row["corpus_source_id"]: row
        for row in read_csv(SOURCE_CANDIDATES) + read_csv(SAFE_SOURCES) + read_csv(SOURCE_QUEUE)
    }

    if {row["candidate_edge_id"] for row in actor_rows} != EXPECTED_ACTORS:
        raise ValueError("HR-016 actor queue is not the expected seven-item set")
    if {row["corpus_source_id"] for row in source_rows} != EXPECTED_SOURCES:
        raise ValueError("HR-016 source queue is not the expected five-item set")

    output: list[dict[str, str]] = []
    counter = 1
    for actor in actor_rows:
        actor_id = actor["candidate_edge_id"]
        refs = split_refs(actor["corpus_source_ids"])
        linked_sources = [all_sources[ref] for ref in refs]
        impact_fact, impact_fig = ACTOR_IMPACTS[actor_id]
        output.append(
            {
                "review_item_id": f"HR016-{counter:03d}",
                "item_type": "actor_frame_semantic",
                "original_id": actor_id,
                "related_ids": ";".join(refs),
                "place": actor["place"],
                "precise_question": ACTOR_QUESTIONS[actor_id],
                "open_url": join_unique([row["url"] for row in linked_sources]),
                "source_locator": " | ".join(
                    f"{row['corpus_source_id']}: {row['locator']}" for row in linked_sources
                ),
                "existing_source_ids": join_unique(
                    [row.get("existing_source_id", "") for row in linked_sources]
                ),
                "decision_options": "accept|revise|reject",
                "affected_formal_fact": impact_fact,
                "affected_figures_or_brief": impact_fig,
                "default_boundary": ACTOR_BOUNDARIES[actor_id],
                "review_decision": "",
                "human_reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )
        counter += 1

    for source in source_rows:
        source_id = source["corpus_source_id"]
        impact_fact, impact_fig = SOURCE_IMPACTS[source_id]
        output.append(
            {
                "review_item_id": f"HR016-{counter:03d}",
                "item_type": "source_locator_speaker",
                "original_id": source_id,
                "related_ids": "",
                "place": source["place"],
                "precise_question": SOURCE_QUESTIONS[source_id],
                "open_url": source["url"],
                "source_locator": source["locator"],
                "existing_source_ids": source.get("existing_source_id", ""),
                "decision_options": "accept|revise|reject",
                "affected_formal_fact": impact_fact,
                "affected_figures_or_brief": impact_fig,
                "default_boundary": SOURCE_BOUNDARIES[source_id],
                "review_decision": "",
                "human_reviewer": "",
                "review_date": "",
                "review_note": "",
            }
        )
        counter += 1

    if len(output) != 12:
        raise ValueError(f"expected 12 HR-016 items, found {len(output)}")
    if len({row["review_item_id"] for row in output}) != 12:
        raise ValueError("duplicate HR-016 review item ID")
    if len({(row["item_type"], row["original_id"]) for row in output}) != 12:
        raise ValueError("duplicate HR-016 original item")
    for row in output:
        required = [
            "precise_question", "open_url", "source_locator", "decision_options",
            "affected_formal_fact", "affected_figures_or_brief", "default_boundary",
        ]
        if any(not row[field].strip() for field in required):
            raise ValueError(f"incomplete HR-016 item {row['review_item_id']}")
        if row["decision_options"] != "accept|revise|reject":
            raise ValueError(f"invalid decision options on {row['review_item_id']}")
        if any(row[field] for field in ("review_decision", "human_reviewer", "review_date", "review_note")):
            raise ValueError(f"script must not pre-decide {row['review_item_id']}")

    write_csv(OUTPUT_CSV, output)
    OUTPUT_MD.write_text(render_packet(output), encoding="utf-8")
    if read_csv(OUTPUT_CSV) != output:
        raise ValueError("HR-016 CSV roundtrip mismatch")
    print("HR-016 packet OK: 12 items (7 actor/frame + 5 source locator/speaker); 0 pre-decisions.")


if __name__ == "__main__":
    main()
