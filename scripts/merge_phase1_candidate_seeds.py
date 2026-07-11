from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
META = ROOT / "data" / "metadata"
REG_OUT = ROOT / "outputs" / "registry_expansion_v1"
R8_OUT = ROOT / "outputs" / "R08_legal_procedure_v0"
FOUNDATION_OUT = ROOT / "outputs" / "phase1_foundation_v1"

# E4, add_first_batch, and no known merge/identity ambiguity.
SAFE_ACTOR_CANDIDATES = {
    "C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008",
    "C013", "C014", "C016", "C017", "C018", "C019", "C020", "C021",
    "C022", "C024", "C025", "C035",
}

SOURCE_TYPE_MAP = {
    "official_npo_portal": "official_portal",
    "organization_website": "organization_site",
    "official_government": "official_data",
    "official_municipal_record": "local_official",
    "official_prefectural_record": "local_official",
    "court_opinion": "court_record",
    "official_case_register": "court_record",
    "catalog_of_formal_case_record": "official_data",
    "formal_litigation_material": "legal_source",
    "formal_comment": "organization_statement",
    "official_EIA": "official_data",
    "official_litigation_report": "official_data",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def next_numeric_id(existing: list[dict[str, str]], field: str, prefix: str) -> int:
    values = []
    for row in existing:
        match = re.fullmatch(rf"{re.escape(prefix)}(\d+)", row.get(field, ""))
        if match:
            values.append(int(match.group(1)))
    return max(values, default=0) + 1


def infer_year(title: str, fallback: str) -> str:
    match = re.search(r"(?:19|20)\d{2}", title)
    if match:
        return match.group(0)
    return fallback[:4] if fallback else "2026"


def normalize_url(url: str) -> str:
    return url.strip().rstrip("/")


def main() -> None:
    actor_path = DATA / "01_actor_registry_initial_v0.csv"
    source_path = DATA / "05_source_log_initial_v0.csv"
    actors = read_csv(actor_path)
    sources = read_csv(source_path)
    original_source_count = len(sources)
    actor_candidates = read_csv(REG_OUT / "candidate_actors_v1.csv")
    registry_sources = read_csv(REG_OUT / "source_candidates_v1.csv")
    r8_sources = read_csv(R8_OUT / "source_candidates_v0.csv")
    r8_cases = read_csv(R8_OUT / "cases_v0.csv")

    safe = [row for row in actor_candidates if row["candidate_id"] in SAFE_ACTOR_CANDIDATES]
    if len(safe) != len(SAFE_ACTOR_CANDIDATES):
        found = {row["candidate_id"] for row in safe}
        raise ValueError(f"Missing safe actor candidates: {sorted(SAFE_ACTOR_CANDIDATES - found)}")
    for row in safe:
        if row["evidence_level"] != "E4" or row["triage_recommendation"] != "add_first_batch":
            raise ValueError(f"Unsafe actor candidate configuration: {row['candidate_id']}")

    needed_registry_source_ids = {
        source_id
        for row in safe
        for source_id in row["source_candidate_ids"].split(";")
        if source_id
    }
    source_candidates: list[tuple[str, dict[str, str], str]] = []
    for row in registry_sources:
        if row["source_candidate_id"] in needed_registry_source_ids:
            source_candidates.append((row["source_candidate_id"], row, "registry"))
    for row in r8_sources:
        if row["evidence_level"] in {"E3", "E4"}:
            source_candidates.append((row["candidate_source_id"], row, "r8"))

    url_to_source = {normalize_url(row["url"]): row["source_id"] for row in sources}
    candidate_to_source: dict[str, str] = {}
    next_source = next_numeric_id(sources, "source_id", "S")

    case_by_id = {row["case_id"]: row for row in r8_cases}
    for candidate_id, row, source_scope in source_candidates:
        url_key = normalize_url(row["url"])
        if url_key in url_to_source:
            candidate_to_source[candidate_id] = url_to_source[url_key]
            continue

        source_id = f"S{next_source:03d}"
        next_source += 1
        url_to_source[url_key] = source_id
        candidate_to_source[candidate_id] = source_id

        if source_scope == "registry":
            source_type = SOURCE_TYPE_MAP.get(row["source_type"], row["source_type"])
            evidence_level = "E4"
            year = infer_year(row["title"], row.get("accessed_date", "2026"))
            support = f"REG-01 {row['candidates_supported']}: {row['why_useful']}"
            bias_note = row["limitations"]
            notes = (
                f"Merged from {candidate_id}; accessed {row.get('accessed_date', '')}; "
                "actor identity may be merged before classification/edge human review."
            )
        else:
            source_type = SOURCE_TYPE_MAP.get(row["source_type"], row["source_type"])
            evidence_level = row["evidence_level"]
            case = case_by_id[row["case_id"]]
            year = infer_year(row["title"], case.get("end_or_decision_date", "2026"))
            support = f"R8-01 {row['case_id']}: {row['used_for']}"
            bias_note = row["notes"]
            notes = (
                f"Merged from {candidate_id}; primary/secondary={row['primary_or_secondary']}; "
                "legal outcome and actor-role wording remain subject to HR-014."
            )

        sources.append(
            {
                "source_id": source_id,
                "source_type": source_type,
                "title": row["title"],
                "year": year,
                "url": row["url"],
                "what_it_supports": support,
                "evidence_level": evidence_level,
                "bias_note": bias_note,
                "review_status": "ai_seeded",
                "notes": notes,
            }
        )

    existing_candidate_map = {
        match.group(1): row
        for row in actors
        if (match := re.search(r"REG-01 (C\d{3})", row.get("notes", "")))
    }
    next_actor = next_numeric_id(actors, "actor_id", "A")
    merge_manifest: list[dict[str, str]] = []
    for row in safe:
        candidate_id = row["candidate_id"]
        if candidate_id in existing_candidate_map:
            existing = existing_candidate_map[candidate_id]
            merge_manifest.append(
                {
                    "candidate_id": candidate_id,
                    "actor_id": existing["actor_id"],
                    "source_refs": existing["source_refs"],
                    "merge_scope": "identity_only_ai_seeded",
                    "human_review_task": "HR-010",
                }
            )
            continue
        actor_id = f"A{next_actor:03d}"
        next_actor += 1
        source_refs = ";".join(
            candidate_to_source[source_id]
            for source_id in row["source_candidate_ids"].split(";")
            if source_id
        )
        actors.append(
            {
                "actor_id": actor_id,
                "canonical_name": row["name_jp"] or row["canonical_name"],
                "actor_class": row["actor_class"],
                "origin_type": row["origin_type"],
                "legal_status_guess": row["legal_status"],
                "primary_places": ";".join(
                    part.strip() for part in row["primary_places"].split(";") if part.strip()
                ),
                "issue_tags": ";".join(
                    part.strip() for part in row["issue_tags"].split(";") if part.strip()
                ),
                "source_refs": source_refs,
                "evidence_level": "E4",
                "review_status": "ai_seeded",
                "needs_local_retrieval": "no",
                "review_priority": row["priority"],
                "notes": (
                    f"REG-01 {candidate_id} safe identity merge from E4 primary source(s). "
                    "Actor classification, issue/place tags, aliases, and analysis edges require HR-010."
                ),
            }
        )
        merge_manifest.append(
            {
                "candidate_id": candidate_id,
                "actor_id": actor_id,
                "source_refs": source_refs,
                "merge_scope": "identity_only_ai_seeded",
                "human_review_task": "HR-010",
            }
        )

    # Merge factual case registry as an AI-seeded side table. Actor roles remain in the candidate package.
    case_rows: list[dict[str, str]] = []
    for row in r8_cases:
        mapped_refs = ";".join(
            candidate_to_source.get(source_id, source_id)
            for source_id in row["primary_source_refs"].split(";")
            if source_id
        )
        case_rows.append(
            {
                **row,
                "primary_source_refs": mapped_refs,
                "review_status": "needs_human_review",
                "interpretation_limit": (
                    row["interpretation_limit"] + " Legal summary/outcome requires HR-014."
                ),
            }
        )

    write_csv(actor_path, actors, list(actors[0].keys()))
    write_csv(source_path, sources, list(sources[0].keys()))
    write_csv(
        DATA / "17_legal_policy_procedure_cases_v0.csv",
        case_rows,
        list(case_rows[0].keys()),
    )
    write_csv(
        META / "venue_taxonomy_v0.csv",
        read_csv(FOUNDATION_OUT / "venue_taxonomy_v0.csv"),
        list(read_csv(FOUNDATION_OUT / "venue_taxonomy_v0.csv")[0].keys()),
    )
    write_csv(
        REG_OUT / "merge_manifest_v1.csv",
        merge_manifest,
        ["candidate_id", "actor_id", "source_refs", "merge_scope", "human_review_task"],
    )

    print(
        f"Merged {len(merge_manifest)} E4 actor identities, "
        f"added {len(sources) - original_source_count} sources, "
        f"{len(case_rows)} legal/procedure cases, and venue taxonomy."
    )
    print(f"Actor registry now has {len(actors)} rows; source log has {len(sources)} rows.")


if __name__ == "__main__":
    main()
