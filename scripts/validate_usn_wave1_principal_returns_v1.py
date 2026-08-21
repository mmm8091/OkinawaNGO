from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    service = read_csv("outputs/us_presence_service_recon_v1/human_review_queue_v1.csv")
    accountability = read_csv("outputs/us_presence_accountability_recon_v1/human_review_queue_v1.csv")
    directory = read_csv("outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv")
    relation_rules = read_csv(
        "outputs/us_presence_relation_retype_v1/HR_USN_relation_retype_rules_v1.csv"
    )
    relation_crosswalk = read_csv(
        "outputs/us_presence_relation_retype_v1/relation_retype_crosswalk_v1.csv"
    )
    architecture = json.loads(
        (ROOT / "outputs/us_presence_network_architecture_v1/principal_checkpoint_return_v1.json")
        .read_text(encoding="utf-8")
    )
    validation_report = json.loads(
        (ROOT / "outputs/us_presence_network_wave1_v1/post_principal_validation_report_v1.json")
        .read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (ROOT / "outputs/us_presence_network_wave1_v1/post_principal_manifest_v1.json")
        .read_text(encoding="utf-8")
    )
    relation_return_manifest = json.loads(
        (ROOT / "outputs/us_presence_relation_retype_v1/post_return_manifest_v1.json")
        .read_text(encoding="utf-8")
    )

    assert len(service) == 13
    assert len({row["hr_id"] for row in service}) == 13
    assert all(row["principal_decision"].strip() for row in service)
    assert all(row["principal_note"].strip() for row in service)

    assert len(accountability) == 9
    assert len({row["review_item_id"] for row in accountability}) == 9
    assert Counter(row["principal_decision"] for row in accountability) == Counter(
        {"revise": 7, "accept": 2}
    )
    assert all(row["principal_note"].strip() for row in accountability)

    assert len(directory) == 65
    assert len({row["review_item_id"] for row in directory}) == 65
    assert Counter(row["decision"] for row in directory) == Counter(
        {"accept": 54, "revise": 4, "defer": 5, "reject": 2}
    )
    assert all(row["review_note"].strip() for row in directory)
    assert all(row["reviewer"] == "project_principal_user" for row in directory)
    assert all(row["review_date"] == "2026-08-21" for row in directory)

    assert len(relation_rules) == 6
    assert Counter(row["decision"] for row in relation_rules) == Counter(
        {"accept": 5, "revise": 1}
    )
    assert sum(int(row["row_count"]) for row in relation_rules) == 43
    assert all(row["principal_note_or_exceptions"].strip() for row in relation_rules)
    assert all(row["reviewer"] == "project_principal_user" for row in relation_rules)
    assert all(row["review_date"] == "2026-08-21" for row in relation_rules)

    assert len(relation_crosswalk) == 43
    assert len({row["edge_id"] for row in relation_crosswalk}) == 43
    assert all(row["mapping_decision"] == "" for row in relation_crosswalk)

    assert architecture["status"] == "principal_confirmed"
    assert architecture["reviewer"] == "project_principal_user"
    assert architecture["review_date"] == "2026-08-21"
    assert architecture["decision_counts"] == {"accept": 2, "revise": 3, "defer": 0}
    arch_decisions = {
        row["item_id"]: row["decision"] for row in architecture["decisions"]
    }
    assert arch_decisions == {
        "USN-ARCH-01": "accept",
        "USN-ARCH-02": "revise",
        "USN-ARCH-03": "revise",
        "USN-ARCH-04": "revise",
        "USN-ARCH-05": "accept",
    }
    assert architecture["central_writeback_authorized"] is False
    assert architecture["publication_adapter_authorized"] is False
    assert architecture["frontend_writeback_authorized"] is False

    assert validation_report["status"] == "PASS"
    assert validation_report["counts"] == {
        "service_decisions": 13,
        "accountability_decisions": 9,
        "directory_decisions": 65,
        "relation_group_decisions": 6,
        "relation_rows_covered": 43,
        "architecture_decisions": 5,
    }
    assert validation_report["checks"]["relation_crosswalk_expanded"] is False
    assert (
        validation_report["checks"]["central_data_source_archive_prototype_diff_detected"]
        is False
    )

    assert manifest["status"] == "principal_returns_complete_merge_ready"
    assert manifest["central_writeback_performed"] is False
    assert manifest["relation_crosswalk_expanded"] is False
    assert manifest["machine_leg_alias_migration"] == "pending"
    assert len(manifest["files"]) == 23
    for receipt in manifest["files"]:
        path = ROOT / receipt["path"]
        assert path.is_file(), receipt["path"]
        assert path.stat().st_size == receipt["bytes"], receipt["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"], receipt[
            "path"
        ]

    assert relation_return_manifest["status"] == (
        "principal_confirmed_rules_validated_crosswalk_unexpanded"
    )
    assert len(relation_return_manifest["files"]) == 6
    for receipt in relation_return_manifest["files"]:
        path = ROOT / receipt["path"]
        assert path.is_file(), receipt["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"], receipt[
            "path"
        ]

    required_returns = [
        "docs/human_review_return_USN_service_ecology_v1.md",
        "docs/human_review_return_USN_accountability_v1.md",
        "docs/human_review_return_USN_actor_directory_v1.md",
        "docs/human_review_return_USN_relation_retype_v1.md",
        "docs/human_review_return_USN_architecture_checkpoint_v1.md",
    ]
    assert all((ROOT / path).is_file() for path in required_returns)

    print(
        json.dumps(
            {
                "status": "PASS",
                "principal_return_sets": 5,
                "service_decisions": 13,
                "accountability_decisions": 9,
                "directory_decisions": 65,
                "relation_group_decisions": 6,
                "relation_rows_covered": 43,
                "architecture_decisions": 5,
                "manifest_files_verified": len(manifest["files"]),
                "nested_relation_manifest_files_verified": len(
                    relation_return_manifest["files"]
                ),
                "relation_crosswalk_expanded": False,
                "machine_leg_alias_migration": "pending",
                "central_writeback_validation": "not_performed_by_this_validator",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
