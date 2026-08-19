from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "outputs" / "actor_directory_v1"


def read_csv(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_path(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


EXPECTED_CONFLICT_IDS = {
    "A002", "A033", "A040", "A042", "A045", "A046", "A070", "A086",
    "A103", "A104", "A107", "A109", "A114", "A115", "X001", "X003",
    "X004", "X005", "X007", "X008", "X009", "X010", "X011", "X012",
    "X016",
}

DECISION_FIELDS = (
    "decision",
    "revised_url",
    "revised_url_kind",
    "review_note",
    "reviewer",
    "review_date",
)


def main() -> None:
    directory = read_csv("actor_directory_candidate_v1.csv")
    decisions = read_csv("HR_USN_actor_directory_decisions_v1.csv")
    crosswalk = read_csv("source_crosswalk_v1.csv")
    conflicts = read_csv("official_url_conflicts_v1.csv")
    source_log = read_path(ROOT / "data" / "interim" / "05_source_log_initial_v0.csv")

    candidates = {row["actor_id"]: row for row in directory if row["url_kind"] != "not_found"}
    decision_ids = [row["actor_id"] for row in decisions]
    sections = Counter(row["review_section"] for row in decisions)
    conflict_ids = {row["actor_id"] for row in decisions if row["review_section"] == "CONFLICT_INDIVIDUAL_25"}
    original_selected_conflict_ids = {row["actor_id"] for row in conflicts if row["actor_id"] in candidates}

    assert len(candidates) == 65, f"expected 65 URL candidates, got {len(candidates)}"
    assert len(decisions) == 65, f"expected 65 decision rows, got {len(decisions)}"
    assert len(decision_ids) == len(set(decision_ids)), "duplicate actor_id in decision sheet"
    assert set(decision_ids) == set(candidates), "decision actor set does not match the 65 non-not_found candidates"
    assert sections == Counter({"BATCH_CONFIRM_40": 40, "CONFLICT_INDIVIDUAL_25": 25}), sections
    assert conflict_ids == EXPECTED_CONFLICT_IDS, "conflict review set drifted"
    assert original_selected_conflict_ids <= conflict_ids, "a selected actor already flagged in conflicts is missing"
    assert len(EXPECTED_CONFLICT_IDS - original_selected_conflict_ids) == 4, "expected four supplemental traceability/hosting conflicts"
    assert "A072" not in decision_ids

    allowed_kinds = {"official_site", "official_subunit", "official_registry", "parent_org_page"}
    selected_rows = [row for row in crosswalk if row["selected"] == "yes"]
    selected_pairs = [(row["actor_id"], row["candidate_url"]) for row in selected_rows]
    assert len(selected_pairs) == len(set(selected_pairs)), "duplicate selected source crosswalk pair"
    selected_trace = {pair: row for pair, row in zip(selected_pairs, selected_rows)}
    central_source_ids = {row["source_id"] for row in source_log}

    for row in decisions:
        actor = candidates[row["actor_id"]]
        assert row["candidate_url"] == actor["official_url"]
        assert row["candidate_url_kind"] == actor["url_kind"] in allowed_kinds
        parsed = urlparse(row["candidate_url"])
        assert parsed.scheme in {"http", "https"} and parsed.netloc
        trace = selected_trace.get((row["actor_id"], row["candidate_url"]))
        assert trace is not None, f"missing selected source crosswalk for {row['actor_id']}"
        assert row["evidence_ref"], f"missing evidence ref for {row['actor_id']}"
        assert row["source_url"], f"missing source URL for {row['actor_id']}"
        assert row["evidence_entry"], f"missing evidence entry for {row['actor_id']}"
        if row["source_id"]:
            assert row["source_id"] in central_source_ids
            assert row["source_id"] == trace["source_id"]
        else:
            assert row["evidence_ref"] == trace["candidate_ref"]
            assert row["evidence_ref"].startswith("WEB-")
        assert all(row[field] == "" for field in DECISION_FIELDS), f"AI-filled decision field in {row['actor_id']}"
        if row["review_section"] == "CONFLICT_INDIVIDUAL_25":
            assert row["conflict_type"]
            assert row["conflict_explanation"]
            assert row["recommended_judgment"]
        else:
            assert not row["conflict_type"]
            assert not row["conflict_explanation"]

    result = {
        "status": "PASS",
        "decision_rows": len(decisions),
        "unique_actor_ids": len(set(decision_ids)),
        "batch_confirm_rows": sections["BATCH_CONFIRM_40"],
        "individual_conflict_rows": sections["CONFLICT_INDIVIDUAL_25"],
        "original_selected_conflict_actors_covered": len(original_selected_conflict_ids),
        "supplemental_conflict_actors": len(EXPECTED_CONFLICT_IDS - original_selected_conflict_ids),
        "all_candidates_traceable": True,
        "all_decision_fields_blank": True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
