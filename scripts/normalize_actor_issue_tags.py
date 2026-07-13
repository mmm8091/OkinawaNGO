"""Normalize delimiter whitespace in actor registry issue tags without recoding."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "interim" / "01_actor_registry_initial_v0.csv"


def main() -> None:
    with REGISTRY.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    changed_rows = 0
    for row in rows:
        before = row.get("issue_tags", "")
        before_tokens = [token.strip() for token in before.split(";") if token.strip()]
        after = ";".join(before_tokens)
        after_tokens = [token for token in after.split(";") if token]
        if before_tokens != after_tokens:
            raise ValueError(f"Semantic token change for {row.get('actor_id', '')}")
        if before != after:
            row["issue_tags"] = after
            changed_rows += 1

    with REGISTRY.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Normalized issue_tags in {changed_rows} actor rows; actors={len(rows)}")


if __name__ == "__main__":
    main()
