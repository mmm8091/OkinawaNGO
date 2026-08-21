from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "outputs" / "actor_directory_v1"
DECISION_PATH = PACKAGE / "HR_USN_actor_directory_decisions_v1.csv"

EXPECTED_REVISE = {
    "USN07-DIR-C006": ("https://www.pronatura.ch/en", "official_site"),
    "USN07-DIR-C010": ("https://www.kogai-net.com/top/counsel/counsel_al/", "parent_org_page"),
    "USN07-DIR-C011": ("https://www.ywca.or.jp/aboutus/japan/", "parent_org_page"),
    "USN07-DIR-C024": ("https://usjapantomodachi.org/", "official_site"),
}
EXPECTED_DEFER = {
    "USN07-DIR-B013",
    "USN07-DIR-B014",
    "USN07-DIR-B038",
    "USN07-DIR-C014",
    "USN07-DIR-C019",
}
EXPECTED_REJECT = {"USN07-DIR-B034", "USN07-DIR-C012"}
ALLOWED_KINDS = {"official_site", "official_subunit", "official_registry", "parent_org_page"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = read_csv(DECISION_PATH)
    candidates = {
        row["actor_id"]: row
        for row in read_csv(PACKAGE / "actor_directory_candidate_v1.csv")
        if row["url_kind"] != "not_found"
    }
    crosswalk = read_csv(PACKAGE / "source_crosswalk_v1.csv")
    selected_pairs = {
        (row["actor_id"], row["candidate_url"])
        for row in crosswalk
        if row["selected"] == "yes"
    }

    assert len(rows) == 65
    assert len({row["review_item_id"] for row in rows}) == 65
    assert len({row["actor_id"] for row in rows}) == 65
    assert {row["actor_id"] for row in rows} == set(candidates)
    assert Counter(row["review_section"] for row in rows) == Counter(
        {"BATCH_CONFIRM_40": 40, "CONFLICT_INDIVIDUAL_25": 25}
    )

    decisions = Counter(row["decision"] for row in rows)
    assert decisions == Counter({"accept": 54, "revise": 4, "defer": 5, "reject": 2})
    assert {row["review_item_id"] for row in rows if row["decision"] == "revise"} == set(EXPECTED_REVISE)
    assert {row["review_item_id"] for row in rows if row["decision"] == "defer"} == EXPECTED_DEFER
    assert {row["review_item_id"] for row in rows if row["decision"] == "reject"} == EXPECTED_REJECT

    for row in rows:
        assert (row["actor_id"], row["candidate_url"]) in selected_pairs
        assert row["review_note"].strip(), f"blank review note: {row['review_item_id']}"
        assert row["reviewer"] == "project_principal_user"
        assert date.fromisoformat(row["review_date"]) == date(2026, 8, 21)
        if row["decision"] == "revise":
            expected_url, expected_kind = EXPECTED_REVISE[row["review_item_id"]]
            assert row["revised_url"] == expected_url
            assert row["revised_url_kind"] == expected_kind in ALLOWED_KINDS
            parsed = urlparse(row["revised_url"])
            assert parsed.scheme in {"http", "https"} and parsed.netloc
        else:
            assert row["revised_url"] == ""
            assert row["revised_url_kind"] == ""

    print(
        json.dumps(
            {
                "status": "PASS",
                "decision_rows": len(rows),
                "decision_counts": dict(decisions),
                "all_review_notes_present": True,
                "all_reviewer_dates_present": True,
                "approved_revisions_exact": True,
                "all_original_candidates_traceable": True,
                "central_writeback_performed": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
