from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS_DIR = ROOT / "outputs" / "research_wave_v2_synthesis"
CHECKPOINT = ROOT / "docs" / "research_wave_v2_principal_checkpoint.md"
HYPOTHESES = SYNTHESIS_DIR / "hypothesis_status_v2.csv"
DECISIONS = SYNTHESIS_DIR / "principal_decision_queue_v2.csv"
README = SYNTHESIS_DIR / "README.md"
REPORT = SYNTHESIS_DIR / "validation_report_v2.md"

UPSTREAM_FILES = [
    ROOT
    / "outputs"
    / "research_wave_h1_documentation_visibility_v2"
    / "method_brief_v2.md",
    ROOT
    / "outputs"
    / "research_wave_h2_recipient_permeability_v1"
    / "mechanism_competing_explanations_brief_v1.md",
    ROOT
    / "outputs"
    / "research_wave_h3_frontline_memory_v2"
    / "frontline_memory_brief_v2.md",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(write_report: bool = True) -> list[str]:
    required = [CHECKPOINT, HYPOTHESES, DECISIONS, README, *UPSTREAM_FILES]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise AssertionError(f"Missing synthesis inputs: {missing}")

    hypothesis_rows = read_rows(HYPOTHESES)
    if {row["topic_id"] for row in hypothesis_rows} != {"H1", "H2", "H3"}:
        raise AssertionError("Hypothesis register must contain exactly H1, H2 and H3.")
    for row in hypothesis_rows:
        if row["package_scope"] != "research_only":
            raise AssertionError(f"{row['topic_id']} escaped research_only.")
        if row["frontend_eligibility"] != "not_frontend_ready":
            raise AssertionError(f"{row['topic_id']} escaped the frontend gate.")
        if row["central_writeback"] != "no":
            raise AssertionError(f"{row['topic_id']} enabled central writeback.")

    decision_rows = read_rows(DECISIONS)
    if {row["decision_id"] for row in decision_rows} != {
        "PDV2-01",
        "PDV2-02",
        "PDV2-03",
        "PDV2-04",
    }:
        raise AssertionError("Principal decision queue must contain PDV2-01 through PDV2-04.")
    for row in decision_rows:
        if row["principal_decision"] or row["principal_note"]:
            raise AssertionError(f"{row['decision_id']} is not a blank principal decision.")
        if row["review_status"] != "needs_human_decision":
            raise AssertionError(f"{row['decision_id']} has an invalid review gate.")
        if (
            row["package_scope"] != "research_only"
            or row["frontend_eligibility"] != "not_frontend_ready"
            or row["central_writeback"] != "no"
        ):
            raise AssertionError(f"{row['decision_id']} escaped an integration gate.")

    checkpoint_text = CHECKPOINT.read_text(encoding="utf-8")
    required_phrases = [
        "不能据此说“中心性就是留存能力”",
        "历史材料削弱“长期完全封闭”的外推",
        "共同文件开始把分散设施构造成一个跨地域对象",
        "生命周期连续性候选",
        "不能转成 35×35 联盟关系",
        "不启动下一轮广泛检索",
    ]
    absent = [phrase for phrase in required_phrases if phrase not in checkpoint_text]
    if absent:
        raise AssertionError(f"Checkpoint lost required boundaries: {absent}")

    lines = [
        "# Research wave v2 synthesis validation",
        "",
        "- Result: **PASS**",
        f"- Hypothesis rows: {len(hypothesis_rows)} (H1/H2/H3)",
        f"- Principal decisions: {len(decision_rows)} (all blank and human-gated)",
        "- Upstream H1/H2/H3 briefs: present",
        "- All hypothesis and decision rows: research_only / not_frontend_ready / central_writeback=no",
        "- Required non-transfer boundaries: present",
        "- This validator does not approve central facts or human decisions.",
        "",
    ]
    if write_report:
        REPORT.write_text("\n".join(lines), encoding="utf-8")
    return lines


if __name__ == "__main__":
    validate(write_report=True)
    print("PASS: research wave v2 synthesis boundaries validated")
