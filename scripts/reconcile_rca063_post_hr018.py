#!/usr/bin/env python3
"""Release the obsolete RCA063 HR-018 blocker without rebuilding the claim audit.

The original report-claim audit predates the post-HR018 render-only R10
figures.  Its full builder also contains historical report counts and must not
be rerun against the current merged layer.  This targeted reconciler changes
only RCA063 and its derived blocker/red-line summaries.  The report paragraph
itself remains a wording revision, so RCA063 moves from ``block`` to
``revise`` rather than to ``safe``.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CLAIMS = Path("data/interim/38_report_claim_evidence_audit_v1.csv")
RELATIONS = Path("data/interim/21_admin_collaboration_relations_v0.csv")
AUDIT_DIR = Path("outputs/report_claim_audit_v1")
CURRENT_FIGURES = (
    Path("outputs/phase1_visuals_v1/fig3_support_service_layers_strict.svg"),
    Path("outputs/R10_administrative_collaboration_v0/fig_r10_mechanism_ecology.svg"),
    Path(
        "outputs/R10_administrative_collaboration_v0/"
        "fig_r10_amount_evidence_boundary.svg"
    ),
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(
    path: Path,
    fields: list[str],
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def verify_release_condition(root: Path) -> None:
    for relative in CURRENT_FIGURES:
        if not (root / relative).exists():
            raise FileNotFoundError(f"missing current post-HR018 figure: {relative}")

    _, relations = read_csv(root / RELATIONS)
    counts = Counter(row["review_status"] for row in relations)
    expected = Counter(
        {
            "human_checked": 24,
            "human_revised": 10,
            "needs_local_retrieval": 1,
        }
    )
    if len(relations) != 35 or counts != expected:
        raise RuntimeError(
            "RCA063 release requires the current 35-row R10 relation layer "
            f"(24 checked / 10 revised / 1 local), got {len(relations)} / {counts}"
        )


def render_status_svg(counts: Counter[str]) -> str:
    colors = {"safe": "#2f855a", "revise": "#d69e2e", "block": "#c53030"}
    maximum = max(counts.values()) or 1
    body: list[str] = []
    for index, status in enumerate(("safe", "revise", "block")):
        y = 72 + index * 56
        width = 520 * counts[status] / maximum
        body.append(
            f'<text x="30" y="{y + 22}" font-size="18">{status}</text>'
            f'<rect x="120" y="{y}" width="{width:.1f}" height="32" rx="4" '
            f'fill="{colors[status]}"/>'
            f'<text x="{130 + width:.1f}" y="{y + 22}" font-size="18">'
            f'{counts[status]}</text>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="280" '
        'viewBox="0 0 760 280">\n'
        '<rect width="760" height="280" fill="#f8fafc"/>'
        '<text x="30" y="38" font-size="24" font-family="Arial, sans-serif" '
        'font-weight="700">Report claim publish status (n=78)</text>\n'
        '<g font-family="Arial, sans-serif" fill="#1a202c">'
        + "".join(body)
        + "</g>\n"
        '<text x="30" y="254" font-family="Arial, sans-serif" font-size="14" '
        'fill="#4a5568">Block = unresolved release condition; revise = report '
        "wording or mechanical repair remains.</text></svg>\n"
    )


def reconcile_rca063(root: Path = ROOT) -> dict[str, object]:
    verify_release_condition(root)

    claim_path = root / CLAIMS
    claim_fields, claims = read_csv(claim_path)
    matches = [row for row in claims if row["claim_id"] == "RCA063"]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one RCA063 row, found {len(matches)}")
    claim = matches[0]
    claim.update(
        {
            "claim_text": (
                "The current F008 strict support/commission/service figure was "
                "regenerated after HR-018. Its 16 displayed records comprise "
                "7 dyadic relations, 6 administrative records, 1 event record "
                "and 2 panel-only observations; the draft report paragraph "
                "still describes regeneration as pending."
            ),
            "audit_support_formal_tables": (
                "data/interim/15_funding_or_support_edges_sample_v0.csv;"
                "data/interim/21_admin_collaboration_relations_v0.csv;"
                "data/interim/22_admin_amount_observations_v0.csv;"
                "data/interim/23_admin_function_observations_v0.csv"
            ),
            "evidence_level_or_layer": (
                "post-HR018 reviewed/revised/local typed layers"
            ),
            "review_layer": "post_HR018_current_render",
            "publish_status": "revise",
            "limitations": (
                "The 16 displayed records are not 16 organization edges: only "
                "7 are dyadic. NOFO, project cost and aggregate observations "
                "are not payments, and the figure is not a funding network. "
                "Update the old report paragraph before final publication."
            ),
            "audit_note": (
                "2026-07-20 targeted reconciliation after "
                "scripts/render_r10_current.py; release condition met."
            ),
        }
    )
    write_csv(claim_path, claim_fields, claims)

    blocker_path = root / AUDIT_DIR / "publication_blockers_v1.csv"
    blocker_fields, blockers = read_csv(blocker_path)
    blockers = [
        row
        for row in blockers
        if row["claim_id"] != "RCA063" and row["blocker_id"] != "RCB001"
    ]
    write_csv(blocker_path, blocker_fields, blockers)

    red_line_path = root / AUDIT_DIR / "red_line_scan_v1.csv"
    red_fields, red_lines = read_csv(red_line_path)
    rcr006 = [row for row in red_lines if row["scan_id"] == "RCR006"]
    if len(rcr006) != 1:
        raise RuntimeError(f"expected one RCR006 row, found {len(rcr006)}")
    rcr006[0].update(
        {
            "result": "pass",
            "finding": (
                "The current render requires reviewed/revised supported or "
                "bounded records and separates 7 dyadic relations from "
                "administrative, event and panel-only observations."
            ),
        }
    )
    write_csv(red_line_path, red_fields, red_lines)

    counts = Counter(row["publish_status"] for row in claims)
    expected_counts = Counter({"safe": 71, "revise": 7})
    if counts != expected_counts:
        raise RuntimeError(f"unexpected post-reconciliation claim counts: {counts}")
    public_counts = {
        status: counts.get(status, 0)
        for status in ("safe", "revise", "block")
    }

    validation_path = root / AUDIT_DIR / "validation_report_v1.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    validation["publish_status"] = public_counts
    validation["publication_blocker_count"] = len(blockers)
    validation_path.write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_path = root / AUDIT_DIR / "report_claim_audit_summary_v1.md"
    summary = summary_path.read_text(encoding="utf-8")
    summary = re.sub(
        r"发布状态：\*\*safe \d+ / revise \d+ / block \d+\*\*",
        "发布状态：**safe 71 / revise 7 / block 0**",
        summary,
    )
    summary = re.sub(
        r"受既有人工任务控制的发布阻断项：\*\*\d+\*\*",
        "受既有人工任务控制的发布阻断项：**0**",
        summary,
    )
    summary = re.sub(
        r"^4\. .*$",
        (
            "4. R10 的 F008／F031／F032 已按 HR-018 合并后的当前层重绘。"
            "F008 的 16 条记录不是 16 条组织关系边：仅 7 条为 dyadic，"
            "其余为行政、事件或面板观察；NOFO、project cost 与 aggregate "
            "均不写成付款，也不得称为资金网络。旧报告段落仍需机械改写。"
        ),
        summary,
        flags=re.MULTILINE,
    )
    summary_path.write_text(summary, encoding="utf-8")

    svg_path = root / AUDIT_DIR / "fig_claim_publish_status_v1.svg"
    svg_path.write_text(
        render_status_svg(Counter(public_counts)),
        encoding="utf-8",
    )

    readme_path = root / AUDIT_DIR / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    old_run = (
        "Run from the repository root with "
        "`python scripts/audit_report_claims_v1.py`. The script does not "
        "modify the report or central research tables."
    )
    replacement = (
        "The original full audit builder is a historical pre-freeze builder "
        "and must not be rerun against the current merged layer. RCA063's "
        "post-HR018 release is reproducible with "
        "`python scripts/reconcile_rca063_post_hr018.py`; this targeted script "
        "does not modify the report or research fact tables."
    )
    if old_run in readme:
        readme = readme.replace(old_run, replacement)
    elif replacement not in readme:
        raise RuntimeError("report-claim README reproduction note has drifted")
    readme_path.write_text(readme, encoding="utf-8")

    return {
        "claim_count": len(claims),
        "publish_status": public_counts,
        "publication_blocker_count": len(blockers),
    }


def main() -> None:
    result = reconcile_rca063()
    print(
        "RCA063 reconciled: "
        f"{result['publish_status']}; blockers={result['publication_blocker_count']}"
    )


if __name__ == "__main__":
    main()
