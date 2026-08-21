from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "outputs" / "us_presence_relation_retype_v1"
RULES_PATH = PACKAGE / "HR_USN_relation_retype_rules_v1.csv"
CROSSWALK_PATH = PACKAGE / "relation_retype_crosswalk_v1.csv"

EXPECTED = {
    "USN-RT-R01": {
        "table_id": "USN02",
        "table_name": "money_flows",
        "edge_ids": "F001;F002;F021;F025;F026;F027;F034;F035",
        "decision": "accept",
    },
    "USN-RT-R02": {
        "table_id": "USN04",
        "table_name": "service_recipient",
        "edge_ids": "F028;F029;F030;F036",
        "decision": "accept",
    },
    "USN-RT-R03": {
        "table_id": "USN05",
        "table_name": "affiliation_control",
        "edge_ids": "F006;F007;F017;F022;F023;F024;F037;F038;F043",
        "decision": "revise",
    },
    "USN-RT-R04": {
        "table_id": "USN06",
        "table_name": "action_institution",
        "edge_ids": "F003;F004;F005;F009;F010;F011;F013;F014;F015;F016;F018;F019;F020;F031;F032;F033;F039;F040;F041;F042",
        "decision": "accept",
    },
    "USN-RT-R05": {
        "table_id": "LEAD",
        "table_name": "research_lead",
        "edge_ids": "F012",
        "decision": "accept",
    },
    "USN-RT-R06": {
        "table_id": "EXCLUDE",
        "table_name": "history_only",
        "edge_ids": "F008",
        "decision": "accept",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rules = read_csv(RULES_PATH)
    crosswalk = read_csv(CROSSWALK_PATH)

    assert len(rules) == 6
    assert {row["mapping_rule_id"] for row in rules} == set(EXPECTED)
    assert len(crosswalk) == 43
    assert len({row["edge_id"] for row in crosswalk}) == 43
    assert all(row["mapping_decision"] == "" for row in crosswalk)

    rule_by_id = {row["mapping_rule_id"]: row for row in rules}
    all_rule_edges: set[str] = set()
    for rule_id, expected in EXPECTED.items():
        row = rule_by_id[rule_id]
        expected_edges = expected["edge_ids"].split(";")
        assert row["proposed_usn_table_id"] == expected["table_id"]
        assert row["proposed_table_name"] == expected["table_name"]
        assert row["row_count"] == str(len(expected_edges))
        assert row["edge_ids"] == expected["edge_ids"]
        assert row["decision"] == expected["decision"]
        assert row["principal_note_or_exceptions"].strip()
        assert row["reviewer"] == "project_principal_user"
        assert date.fromisoformat(row["review_date"]) == date(2026, 8, 21)

        group_rows = [item for item in crosswalk if item["mapping_rule_id"] == rule_id]
        assert {item["edge_id"] for item in group_rows} == set(expected_edges)
        assert all(item["proposed_usn_table_id"] == expected["table_id"] for item in group_rows)
        assert all(item["proposed_table_name"] == expected["table_name"] for item in group_rows)
        all_rule_edges.update(expected_edges)

    assert all_rule_edges == {row["edge_id"] for row in crosswalk}
    assert sum(int(row["row_count"]) for row in rules) == 43

    r03_note = rule_by_id["USN-RT-R03"]["principal_note_or_exceptions"]
    assert all(token in r03_note for token in ("F017", "F043", "regional_branch"))
    assert {
        row["edge_id"]: row["proposed_record_family"]
        for row in crosswalk
        if row["edge_id"] in {"F017", "F043"}
    } == {"F017": "organizational_affiliation", "F043": "organizational_affiliation"}

    special_rows = {row["edge_id"]: row for row in crosswalk}
    assert special_rows["F008"]["proposed_usn_table_id"] == "EXCLUDE"
    assert special_rows["F008"]["proposed_record_family"] == "rejected_duplicate"
    assert special_rows["F012"]["proposed_usn_table_id"] == "LEAD"
    assert special_rows["F012"]["proposed_record_family"] == "opportunity_not_award"
    assert all(
        special_rows[edge_id]["proposed_usn_table_id"] == "USN06"
        and special_rows[edge_id]["proposed_record_family"] == "public_commission_role"
        for edge_id in ("F031", "F032", "F033")
    )

    decisions = Counter(row["decision"] for row in rules)
    assert decisions == Counter({"accept": 5, "revise": 1})

    print(
        json.dumps(
            {
                "status": "PASS",
                "rule_rows": len(rules),
                "covered_crosswalk_rows": len(all_rule_edges),
                "decision_counts": dict(decisions),
                "all_notes_reviewer_dates_present": True,
                "r03_exceptions_explicit": ["F017", "F043"],
                "lead_exclude_commission_boundaries_verified": True,
                "crosswalk_expansion_performed": False,
                "central_writeback_validation": "not_performed_by_this_validator",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
