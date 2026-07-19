from __future__ import annotations

"""Merge the principal-approved HR-022/HR-030 source metadata decisions.

Only source metadata and support boundaries are changed. Every reviewed row
is explicitly marked ``relation_or_claim_approved=no`` so source admission
cannot be mistaken for approval of an actor, relation, amount or causal
claim. Archive handling is recorded as a requested resolution; the archive
manifest is updated only by the archive workflow.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_LOG = Path("data/interim/05_source_log_initial_v0.csv")
OVERLAY = Path("outputs/principal_review_merge_v1/source_metadata_overlay_v1.csv")
OUT = Path("outputs/source_metadata_merge_v1")

PRESERVE_HUMAN_CHECKED = {"S158", "S204"}

URL_OVERRIDES = {
    "S137": "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-89731.pdf",
    "S197": (
        "https://www2.pref.okinawa.jp/oki/Gikairep1.nsf/"
        "GoZentai/20180702000000"
    ),
    "S198": (
        "https://www2.pref.okinawa.jp/oki/Gikairep1.nsf/"
        "bf76642d1ed57158492581ed00348311/"
        "6cc4b1801bbb16124925861e00087c7a?OpenDocument"
    ),
}

EXTRA_FIELDS = [
    "locator",
    "support_scope",
    "human_decision",
    "review_task_id",
    "human_reviewer",
    "review_date",
    "reviewed_fields",
    "archive_resolution",
    "decision_source_report",
    "relation_or_claim_approved",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ensure_fields(fields: list[str], additions: list[str]) -> list[str]:
    return fields + [field for field in additions if field not in fields]


def index_unique(
    rows: list[dict[str, str]], key_field: str
) -> dict[str, dict[str, str]]:
    result = {row[key_field]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate {key_field}")
    return result


def append_note(current: str, addition: str) -> str:
    current = current.strip()
    if addition in current:
        return current
    return f"{current} {addition}".strip()


def write_summary(root: Path, summary: dict[str, int]) -> None:
    out = root / OUT
    out.mkdir(parents=True, exist_ok=True)
    write_csv(
        out / "merge_summary_v1.csv",
        ["metric", "value"],
        [{"metric": key, "value": str(value)} for key, value in summary.items()],
    )
    (out / "README.md").write_text(
        "# Source metadata merge v1\n\n"
        "HR-022 and HR-030 principal decisions were applied to the central source log.\n\n"
        "- 71 reviewed source rows received revised metadata, locators and bounded support scopes.\n"
        "- S158 and S204 preserve their earlier `human_checked` status; the other reviewed "
        "rows use `human_revised`.\n"
        "- `relation_or_claim_approved=no` is explicit on every reviewed row.\n"
        "- S137/S197/S198 URL corrections are in the source log; archive retry remains a "
        "separate technical step.\n"
        "- Archive success or failure never expands the approved support scope.\n",
        encoding="utf-8",
    )


def apply_source_metadata_reviews(root: Path = ROOT) -> dict[str, int]:
    source_path = root / SOURCE_LOG
    overlay_path = root / OVERLAY
    fields, source_rows = read_csv(source_path)
    fields = ensure_fields(fields, EXTRA_FIELDS)
    _, overlay_rows = read_csv(overlay_path)

    sources = index_unique(source_rows, "source_id")
    overlay_by_source = index_unique(overlay_rows, "source_id")
    missing = set(overlay_by_source) - set(sources)
    if missing:
        raise ValueError(f"reviewed sources absent from source log: {sorted(missing)}")
    if len(overlay_rows) != 71:
        raise ValueError(f"expected 71 metadata decisions, found {len(overlay_rows)}")

    for source_id, overlay in overlay_by_source.items():
        row = sources[source_id]
        row.update(
            {
                "title": overlay["revised_title"],
                "source_type": overlay["revised_source_type"],
                "year": overlay["revised_year_or_period"],
                "what_it_supports": overlay["revised_support_scope"],
                "evidence_level": overlay["revised_evidence_level"],
                "review_status": (
                    "human_checked"
                    if source_id in PRESERVE_HUMAN_CHECKED
                    else "human_revised"
                ),
                "locator": overlay["revised_locator"],
                "support_scope": overlay["revised_support_scope"],
                "human_decision": (
                    "accept" if overlay["decision"] == "accept" else "revise"
                ),
                "review_task_id": overlay["task_id"],
                "human_reviewer": "project_principal_user",
                "review_date": "2026-07-20",
                "reviewed_fields": (
                    "title;source_type;year_or_period;locator;support_scope;"
                    "evidence_level;archive_resolution"
                ),
                "archive_resolution": overlay["archive_resolution"],
                "decision_source_report": overlay["source_report"],
                "relation_or_claim_approved": "no",
            }
        )
        row["notes"] = append_note(
            row.get("notes", ""),
            "HR source-metadata review: "
            f"{overlay['review_note']} Source inclusion does not approve actors, edges, "
            "alliances, funding, amounts, causality or policy effects.",
        )
        if source_id in URL_OVERRIDES:
            row["url"] = URL_OVERRIDES[source_id]

    write_csv(source_path, fields, source_rows)
    summary = {
        "source_rows": len(source_rows),
        "reviewed_sources": len(overlay_rows),
        "human_revised": sum(
            sources[source_id]["review_status"] == "human_revised"
            for source_id in overlay_by_source
        ),
        "preserved_human_checked": sum(
            sources[source_id]["review_status"] == "human_checked"
            for source_id in overlay_by_source
        ),
        "url_repairs": len(URL_OVERRIDES),
    }
    write_summary(root, summary)
    return summary


if __name__ == "__main__":
    result = apply_source_metadata_reviews()
    print(
        "Source metadata merge complete: "
        f"{result['reviewed_sources']} reviewed sources, "
        f"{result['url_repairs']} URL repairs."
    )
