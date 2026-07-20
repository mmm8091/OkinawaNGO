from __future__ import annotations

"""Create an analytical comparison of claim-translation episodes.

The unit is an episode, not an alliance edge.  The comparison distinguishes
public claim visibility, entry into a legal/administrative/democratic/workplace
venue, observable intermediate output, bounded gain/participatory decision,
and change to the underlying project or policy in the claimed direction.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "translation_episode_comparison_v1"

STAGES = [
    ("public_claim", "公开诉求可见"),
    ("venue_entry", "进入制度／策略场域"),
    ("intermediate_output", "产生可观察中间产出"),
    ("bounded_gain", "有限救济／参与性决定"),
    ("underlying_change", "底层项目／政策按诉求改变"),
]

STATUS_CODE = {"unknown": 0, "no": 1, "mixed": 2, "yes": 3}
STATUS_LABEL = {"unknown": "?", "no": "否", "mixed": "部分", "yes": "是"}


EPISODES = [
    {
        "episode_id": "TE01", "module": "R8", "case_id": "R8C01", "short_label": "儒艮海外诉讼",
        "actor_ids": "A045;A086;A020;A076;A009", "place": "Henoko;Oura Bay",
        "route_family": "international_legal", "local_problem": "基地建设与儒艮影响",
        "translation_frame": "文化财程序义务／NHPA §402", "venue": "美国联邦法院／APA review",
        "observable_output": "Section 402 适用与可审查标准、公开记录", "substantive_result": "2020 维持 DoD 胜诉；未停止工程",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "no", "underlying_change": "no",
        "source_refs": "S093;S128;S129", "evidence_level": "E4", "review_status": "human_checked",
        "interpretation_limit": "程序标准与信息生产不等于工程被阻止；原告身份严格按各案 caption／当事人表核定。",
    },
    {
        "episode_id": "TE02", "module": "R8", "case_id": "R8C02", "short_label": "边野古 EIA 意见",
        "actor_ids": "A004", "place": "Henoko;Oura Bay", "route_family": "administrative_EIA",
        "local_problem": "基地建设与生态影响", "translation_frame": "调查、预测与减缓充分性",
        "venue": "日本 EIA 方法书／补正评价书程序", "observable_output": "NACSJ 科学批评进入正式行政记录",
        "substantive_result": "补正 EIA 完成；不证明意见获采纳或工程停止",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "no", "underlying_change": "no",
        "source_refs": "S130;S131;S132", "evidence_level": "E4", "review_status": "human_checked",
        "interpretation_limit": "正式提交意见不等于采纳。",
    },
    {
        "episode_id": "TE03", "module": "R8", "case_id": "R8C03", "short_label": "嘉手纳第三次噪音诉讼",
        "actor_ids": "A052", "place": "Kadena;Chatan;Okinawa City", "route_family": "noise_civil_litigation",
        "local_problem": "航空器噪音与日常负担", "translation_frame": "人格／生活损害与差止",
        "venue": "日本民事差止／损害赔偿诉讼", "observable_output": "法院确认部分过去期间噪音损害",
        "substantive_result": "获部分赔偿；差止与未来损害请求被驳回",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "yes", "underlying_change": "no",
        "source_refs": "S133;S134", "evidence_level": "E4", "review_status": "human_checked",
        "interpretation_limit": "赔偿不表示噪音停止；原告团不等于所有个体或轮次恒定。",
    },
    {
        "episode_id": "TE04", "module": "R8", "case_id": "R8C04", "short_label": "普天间周边噪音诉讼",
        "actor_ids": "A053", "place": "Futenma;Ginowan", "route_family": "noise_civil_litigation",
        "local_problem": "噪音与睡眠／健康负担", "translation_frame": "特定期间损害",
        "venue": "日本损害赔偿诉讼", "observable_output": "列名原告获指定期间赔偿",
        "substantive_result": "部分原告／期间获赔；无运营禁令",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "yes", "underlying_change": "no",
        "source_refs": "S135;S136", "evidence_level": "E4", "review_status": "human_checked",
        "interpretation_limit": "案件特定 plaintiff group；不跨轮次泛化。",
    },
    {
        "episode_id": "TE05", "module": "R8/R9", "case_id": "R8C05/R9C_ISHIGAKI_2018_2024", "short_label": "石垣部署公投诉讼",
        "actor_ids": "A011", "place": "Ishigaki", "route_family": "referendum_litigation",
        "local_problem": "陆自部署与居民决定权", "translation_frame": "公投实施义务／地方自治",
        "venue": "条例直接请求、议会与义务付诉讼", "observable_output": "签名门槛达成；议会两度否决；法院认定举行公投不属于义务付诉讼对象",
        "substantive_result": "未举行投票；义务付请求被程序性驳回",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "no", "underlying_change": "no",
        "source_refs": "S137;S138;S139;R9S010;R9S011", "evidence_level": "E4", "review_status": "human_checked",
        "interpretation_limit": "A011 是 requester／运动体，不是具名组织原告。",
    },
    {
        "episode_id": "TE06", "module": "R8", "case_id": "R8C06", "short_label": "泡濑公金诉讼",
        "actor_ids": "A055;A020", "place": "Awase;Okinawa City", "route_family": "public_funds_litigation",
        "local_problem": "填海生态、经济与灾害风险", "translation_frame": "公共支出合法性／合理性",
        "venue": "住民监查请求与公金支出差止诉讼", "observable_output": "生态争议转成支出与行政裁量审查",
        "substantive_result": "第一波限制未来支出；第二波居民败诉，结果相反",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "mixed", "underlying_change": "mixed",
        "source_refs": "S140;S141;S142;S143", "evidence_level": "E4", "review_status": "human_checked",
        "interpretation_limit": "两波结果必须分列；A055/A020 是 supporter，不是组织原告。",
    },
    {
        "episode_id": "TE07", "module": "R9", "case_id": "R9C_NAGO_1997", "short_label": "名护 1997 公投",
        "actor_ids": "A068", "place": "Nago", "route_family": "municipal_referendum",
        "local_problem": "海上直升机场／基地建设", "translation_frame": "地方自治法第74条直接请求",
        "venue": "签名、议会条例与咨询型住民投票", "observable_output": "17,539 有效签名；四选项条例；实际投票",
        "substantive_result": "反对多数；三日后市长接受基地并辞职",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "yes", "underlying_change": "no",
        "source_refs": "R9S001;R9S002;R9S003;R9S022", "evidence_level": "E4", "review_status": "accepted_process",
        "interpretation_limit": "咨询型反对多数不是法律否决；A068 已人审正名，并记录为 1997 年发展性改组至 A019；这不等于两者为同一 actor，也不证明 A068 此后持续。",
    },
    {
        "episode_id": "TE08", "module": "R9", "case_id": "R9C_YONAGUNI_2015", "short_label": "与那国 2015 公投",
        "actor_ids": "A014;A015", "place": "Yonaguni", "route_family": "municipal_referendum",
        "local_problem": "陆自部署、前线化与岛内决定", "translation_frame": "自治体个别条例与公众动员",
        "venue": "町条例、选管投票与行政解释", "observable_output": "投票举行；地方报道 632 赞成、445 反对",
        "substantive_result": "町长将结果解释为推进依据；组织级身份仍需当地材料",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "yes", "underlying_change": "no",
        "source_refs": "R9S005;R9S006;R9S007;R9S032;R9S034", "evidence_level": "E3", "review_status": "accepted_process_with_local_gap",
        "interpretation_limit": "A014/A015 为 E2 组织线索；不能写成投票发起／实施者或长期组织。",
    },
    {
        "episode_id": "TE09", "module": "R9", "case_id": "R9C_PREF_2019", "short_label": "2019 边野古县民投票",
        "actor_ids": "A051", "place": "Okinawa Prefecture", "route_family": "prefectural_referendum",
        "local_problem": "边野古填海与县民意", "translation_frame": "全县直接请求／条例化",
        "venue": "92,848 有效签名、县议会条例、全41市町村投票", "observable_output": "反对 434,273（71.7%）；知事通知日美政府",
        "substantive_result": "民意转化为条例与通知资源；工程未因此自动停止",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "yes", "underlying_change": "no",
        "source_refs": "R9S009;R9S010;R9S011;R9S012;R9S013", "evidence_level": "E4", "review_status": "accepted_process",
        "interpretation_limit": "签名者／请求代表不自动等于 A051 成员；投票不直接停止工程。",
    },
    {
        "episode_id": "TE10", "module": "HR027/R2-R4", "case_id": "HR027E002", "short_label": "宫古地下水行政往来",
        "actor_ids": "A112", "place": "Miyako", "route_family": "administrative_exchange",
        "local_problem": "饮用地下水与设施排水风险", "translation_frame": "监测、条例与水源保护",
        "venue": "研究会意见／宫古岛市正式书面回答", "observable_output": "2023 市政府逐条回答形成行政记录",
        "substantive_result": "可证行政接口；不证明市方接受风险解释或政策改变",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "unknown", "underlying_change": "unknown",
        "source_refs": "S269;S270;S271", "evidence_level": "E4", "review_status": "analytic_candidate_event_pending",
        "interpretation_limit": "HR027 只批准 actor；事件仍待逐条 HR，且不得写实际污染／健康损害。",
    },
    {
        "episode_id": "TE11", "module": "HR027/R2-R4", "case_id": "HR027E004;HR027E005", "short_label": "宜野湾 PFAS 土壤采样→议会",
        "actor_ids": "A113", "place": "Ginowan;Futenma", "route_family": "resident_sampling_petition",
        "local_problem": "学校／社区 PFAS 风险", "translation_frame": "居民筹资土壤采样与健康调查请求",
        "venue": "土壤采样、请愿与市议会意见书", "observable_output": "市议会正式记录土壤采样，并形成污染对策意见",
        "substantive_result": "程序和记录可证；污染源、健康因果与后续实施不确定",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "mixed", "underlying_change": "unknown",
        "source_refs": "S273;S274;S275;S276", "evidence_level": "E4", "review_status": "analytic_candidate_event_pending",
        "interpretation_limit": "HR027 只批准 actor；事件待审，不强化污染源盖然性为确定因果。",
    },
    {
        "episode_id": "TE12", "module": "HR027/R5-R7", "case_id": "HR027E010", "short_label": "石垣港罢工",
        "actor_ids": "A114", "place": "Ishigaki", "route_family": "workplace_port_power",
        "local_problem": "民用港军事使用与港湾劳动安全", "translation_frame": "职业安全／劳动行动",
        "venue": "港口工作场域与罢工", "observable_output": "2024-03-11–13 石垣港罢工实际执行",
        "substantive_result": "行动发生可证；合法性、实际效果与政治影响未判定",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "unknown", "underlying_change": "unknown",
        "source_refs": "S287;S288", "evidence_level": "E4", "review_status": "analytic_candidate_event_pending",
        "interpretation_limit": "HR027 只批准 actor；不得从行动发生推断政策效果或稳定联盟。",
    },
    {
        "episode_id": "TE13", "module": "HR027/R9", "case_id": "HR027E014", "short_label": "新妇人县本部公投动员",
        "actor_ids": "A115", "place": "Okinawa Prefecture", "route_family": "membership_signature_mobilization",
        "local_problem": "边野古与县民决定", "translation_frame": "会员制群众组织的签名动员",
        "venue": "2018 县民投票条例签名运动", "observable_output": "县本部有日期的签名启动行动可见",
        "substantive_result": "只证参与渠道；不能把全县 92,848 份签名或条例结果归因于 A115",
        "public_claim": "yes", "venue_entry": "yes", "intermediate_output": "yes", "bounded_gain": "unknown", "underlying_change": "no",
        "source_refs": "S283", "evidence_level": "E4", "review_status": "analytic_candidate_event_pending",
        "interpretation_limit": "HR027 只批准 actor；不转嫁全国本部行动，不作组织贡献因果估计。",
    },
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def configure_fonts() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Microsoft YaHei", "Yu Gothic", "Meiryo", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"):
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def main() -> None:
    configure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    fields = [
        "episode_id", "module", "case_id", "short_label", "actor_ids", "place", "route_family",
        "local_problem", "translation_frame", "venue", "observable_output", "substantive_result",
        *[stage[0] for stage in STAGES], "source_refs", "evidence_level", "review_status", "interpretation_limit",
    ]
    write_csv(OUT / "translation_episode_candidates_v1.csv", EPISODES, fields)

    matrix = np.array([[STATUS_CODE[row[field]] for field, _ in STAGES] for row in EPISODES], dtype=int)
    cmap = ListedColormap(["#f7f7f3", "#d8dadd", "#e6b45d", "#3f8a67"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    fig, ax = plt.subplots(figsize=(14.8, 10.2))
    ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(range(len(STAGES)), labels=[label for _, label in STAGES], fontsize=10.5)
    ax.set_yticks(range(len(EPISODES)), labels=[f"{row['episode_id']}  {row['short_label']}" for row in EPISODES], fontsize=9.5)
    ax.xaxis.tick_top()
    ax.tick_params(length=0, pad=8)
    for i, row in enumerate(EPISODES):
        for j, (field, _) in enumerate(STAGES):
            status = row[field]
            ax.text(j, i, STATUS_LABEL[status], ha="center", va="center", fontsize=9,
                    color="white" if status == "yes" else "#30383d", fontweight="bold" if status in {"yes", "mixed"} else "normal")
    for i in range(len(EPISODES) + 1):
        ax.axhline(i - 0.5, color="white", linewidth=1.4)
    for j in range(len(STAGES) + 1):
        ax.axvline(j - 0.5, color="white", linewidth=1.4)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.suptitle("跨模块转译阶梯：公开诉求进入场域后，通常产出什么？", x=0.05, ha="left", fontsize=18, fontweight="bold")
    fig.text(0.05, 0.935, "R8/R9 已核案件与 HR027 新 actor 的分析候选并列。本图有意选取已进入某种场域的 episode，前3列不是总体成功率；横向也不是因果链证明。", fontsize=10.3, color="#4a5962")
    legend = "  ■ 是    ■ 部分／混合    ■ 否    □ 未知／待审"
    fig.text(0.05, 0.045, legend, fontsize=10, color="#3a454b")
    fig.text(0.05, 0.018, "核心边界：程序产出、赔偿、投票、行政回答或罢工发生，都不能自动等同于政策效果；TE10–TE13 的事件仍在 HR027 候选层。", fontsize=9.2, color="#7a3e2e")
    fig.subplots_adjust(left=0.27, right=0.98, top=0.86, bottom=0.08)
    fig.savefig(OUT / "fig_translation_ladder_v1.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    stage_summary = []
    for field, label in STAGES:
        counts = {status: sum(row[field] == status for row in EPISODES) for status in STATUS_CODE}
        stage_summary.append({"stage": field, "stage_label": label, **counts})
    write_csv(OUT / "stage_status_summary_v1.csv", stage_summary, ["stage", "stage_label", "yes", "mixed", "no", "unknown"])

    readme = """# Translation episode comparison v1

This is an analytical comparison layer, not a new factual relation table. It makes one project-wide distinction visible: among episodes selected because they reached a formal or strategic venue, an observable record is common while substantive change to the underlying base, deployment or infrastructure project is rarer. The first three columns therefore cannot be read as a population success rate.

R8 rows are human-checked case facts. R9 rows use the accepted process layer, with Yonaguni's local-source limits retained. TE10–TE13 use HR-027-approved actors but candidate events; they must not enter the central AEV layer before event-level human review.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Translation comparison: {len(EPISODES)} episodes; candidate-only HR027 episodes=4")


if __name__ == "__main__":
    main()
