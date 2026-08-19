"""Build the bounded 17-row U.S.-origin analytical scope overlay."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/interim/01_actor_registry_initial_v0.csv"
DIRECTORY = ROOT / "outputs/actor_directory_v1/actor_directory_candidate_v1.csv"
OUT = ROOT / "outputs/us_presence_network_wave1_v1"

SERVICE = {"X001", "X004", "X005", "X006", "X007", "X008", "X009", "X016", "X017"}
ACCOUNTABILITY = {"A009", "A033", "A042", "A045", "A070", "A086"}
PUBLIC_DIPLOMACY = {"X013"}
FUNDER_WATCHLIST = {"X014"}

GROUPS = {
    **{actor_id: "service_charity_comparison" for actor_id in SERVICE},
    **{actor_id: "accountability_comparison" for actor_id in ACCOUNTABILITY},
    **{actor_id: "public_diplomacy_program_node" for actor_id in PUBLIC_DIPLOMACY},
    **{actor_id: "funder_watchlist_node" for actor_id in FUNDER_WATCHLIST},
}

GROUP_BASIS = {
    "service_charity_comparison": "H2 nine-actor service/charity comparison core",
    "accountability_comparison": "six U.S.-origin actors with Okinawa accountability/event evidence",
    "public_diplomacy_program_node": "U.S. Consulate program opportunity node; not an NGO comparison actor",
    "funder_watchlist_node": "NED observation/watchlist node; no Okinawa named award in current evidence",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_rows() -> list[dict[str, str]]:
    registry = {row["actor_id"]: row for row in read_csv(REGISTRY)}
    directory = {row["actor_id"]: row for row in read_csv(DIRECTORY)}
    rows = []
    for actor_id, group in sorted(GROUPS.items()):
        actor = registry[actor_id]
        site = directory[actor_id]
        rows.append(
            {
                "scope_row_id": f"USOS-{actor_id}",
                "selection_frame_id": "USF-US-ORIGIN17-2026-08-19",
                "actor_id": actor_id,
                "canonical_name": actor["canonical_name"],
                "actor_class": actor["actor_class"],
                "origin_type": actor["origin_type"],
                "analytical_group": group,
                "group_basis": GROUP_BASIS[group],
                "official_url_candidate": site["official_url"],
                "official_url_kind_candidate": site["url_kind"],
                "official_url_review_status": site["review_status_candidate"],
                "actor_review_status": actor["review_status"],
                "scope_status": actor["scope_status"],
                "selection_status": "research_comparison_frame",
                "human_decision": "",
                "package_scope": "research_only",
                "frontend_eligibility": "excluded_pending_human_review",
                "interpretation_limit": (
                    "Analytical-group membership defines a comparison frame, not a fixed pro-/anti-U.S. "
                    "actor stance. Function must be coded on dated actions or relations."
                ),
            }
        )
    return rows


def main() -> None:
    rows = build_rows()
    if len(rows) != 17 or len({row["actor_id"] for row in rows}) != 17:
        raise ValueError("The U.S.-origin scope must contain 17 unique actors")
    if Counter(row["analytical_group"] for row in rows) != Counter(
        {
            "service_charity_comparison": 9,
            "accountability_comparison": 6,
            "public_diplomacy_program_node": 1,
            "funder_watchlist_node": 1,
        }
    ):
        raise ValueError("Unexpected analytical group counts")
    if any(row["origin_type"] != "us_origin" for row in rows):
        raise ValueError("Every row must be us_origin in the current registry")
    if any(row["human_decision"] for row in rows):
        raise ValueError("AI build must leave human decisions blank")

    fields = list(rows[0])
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "us_origin_actor_scope_v1.csv"
    write_csv(output, rows, fields)

    counts = Counter(row["analytical_group"] for row in rows)
    summary = [
        {"analytical_group": group, "actor_count": str(count)}
        for group, count in sorted(counts.items())
    ]
    summary_output = OUT / "us_origin_actor_scope_summary_v1.csv"
    write_csv(summary_output, summary, ["analytical_group", "actor_count"])

    manifest = {
        "package": "us_presence_network_wave1_v1",
        "generated_on": "2026-08-19",
        "status": "research_only_selection_frame_not_frontend_ready",
        "inputs": {
            str(REGISTRY.relative_to(ROOT)): sha256(REGISTRY),
            str(DIRECTORY.relative_to(ROOT)): sha256(DIRECTORY),
        },
        "counts": dict(sorted(counts.items())),
        "total": len(rows),
        "all_human_decisions_blank": True,
        "central_writeback": False,
        "outputs": {
            output.name: {"rows": len(rows), "sha256": sha256(output)},
            summary_output.name: {"rows": len(summary), "sha256": sha256(summary_output)},
        },
    }
    readme = OUT / "README.md"
    if readme.exists():
        manifest["documentation"] = {"README.md": {"sha256": sha256(readme)}}
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
