from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"

TABLES = {
    "actors": (DATA / "01_actor_registry_initial_v0.csv", "actor_id"),
    "aliases": (DATA / "02_actor_aliases_initial_v0.csv", None),
    "issues": (DATA / "03_issue_taxonomy_v0.csv", "issue_id"),
    "places": (DATA / "04_place_registry_v0.csv", "place_id"),
    "sources": (DATA / "05_source_log_initial_v0.csv", "source_id"),
    "actor_issue": (DATA / "07_actor_issue_edges_initial_v0.csv", "edge_id"),
    "actor_place": (DATA / "08_actor_place_edges_initial_v0.csv", "edge_id"),
    "funding": (DATA / "15_funding_or_support_edges_sample_v0.csv", "edge_id"),
    "legal_cases": (DATA / "17_legal_policy_procedure_cases_v0.csv", "case_id"),
}

VALID_EVIDENCE = {"E0", "E1", "E2", "E3", "E4"}


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]], list[str]]:
    errors: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        raw = list(reader)
    if not raw:
        return [], [], [f"{path}: empty CSV"]
    header = raw[0]
    for line_no, row in enumerate(raw[1:], start=2):
        if len(row) != len(header):
            errors.append(
                f"{path}:{line_no}: expected {len(header)} columns, got {len(row)}"
            )
    if errors:
        return header, [], errors
    return header, [dict(zip(header, row)) for row in raw[1:]], []


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    rows: dict[str, list[dict[str, str]]] = {}

    for name, (path, id_field) in TABLES.items():
        header, table_rows, table_errors = read_table(path)
        errors.extend(table_errors)
        rows[name] = table_rows
        if table_errors:
            continue
        if id_field not in header if id_field else False:
            errors.append(f"{path}: missing id field {id_field}")
        if id_field:
            ids = [row[id_field].strip() for row in table_rows]
            duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
            if duplicates:
                errors.append(f"{path}: duplicate {id_field}: {duplicates}")

    if errors:
        for message in errors:
            print(f"ERROR: {message}")
        return 1

    actor_ids = {row["actor_id"] for row in rows["actors"]}
    issue_ids = {row["issue_id"] for row in rows["issues"]}
    place_ids = {row["place_id"] for row in rows["places"]}

    for row in rows["aliases"]:
        if row["actor_id"] not in actor_ids:
            errors.append(f"aliases: unknown actor_id {row['actor_id']}")
    for row in rows["actor_issue"]:
        if row["actor_id"] not in actor_ids:
            errors.append(f"actor_issue {row['edge_id']}: unknown actor {row['actor_id']}")
        if row["issue_id"] not in issue_ids:
            errors.append(f"actor_issue {row['edge_id']}: unknown issue {row['issue_id']}")
    for row in rows["actor_place"]:
        if row["actor_id"] not in actor_ids:
            errors.append(f"actor_place {row['edge_id']}: unknown actor {row['actor_id']}")
        if row["place_id"] not in place_ids:
            errors.append(f"actor_place {row['edge_id']}: unknown place {row['place_id']}")
    for row in rows["funding"]:
        for field in ("source_actor_id", "target_actor_id"):
            value = row[field]
            if value.startswith(("A", "X")) and value not in actor_ids:
                errors.append(f"funding {row['edge_id']}: unknown {field} {value}")

    for table_name in (
        "actors",
        "sources",
        "actor_issue",
        "actor_place",
        "funding",
        "legal_cases",
    ):
        for row in rows[table_name]:
            value = row.get("evidence_level", "").strip()
            if value and value not in VALID_EVIDENCE:
                identity = row.get("edge_id") or row.get("actor_id") or row.get("source_id")
                errors.append(f"{table_name} {identity}: invalid evidence_level {value!r}")

    if len(rows["actors"]) < 120:
        warnings.append(
            f"actor registry has {len(rows['actors'])} rows; Phase-1 contract minimum is 120"
        )

    whitespace_tokens = 0
    for row in rows["actors"]:
        for token in row.get("issue_tags", "").split(";"):
            if token and token != token.strip():
                whitespace_tokens += 1
    if whitespace_tokens:
        warnings.append(
            f"actor issue_tags contain {whitespace_tokens} tokens with surrounding whitespace"
        )

    seeded = sum(row.get("review_status") == "ai_seeded" for row in rows["actors"])
    second_source = sum(
        row.get("review_status") == "needs_second_source" for row in rows["actors"]
    )
    if seeded or second_source:
        warnings.append(
            f"actor review backlog: {seeded} ai_seeded; {second_source} needs_second_source"
        )

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors:
        return 1

    print(
        "OK: structural CSV, unique-ID, foreign-key and evidence-level checks passed "
        f"({len(rows['actors'])} actors, {len(rows['sources'])} sources)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
