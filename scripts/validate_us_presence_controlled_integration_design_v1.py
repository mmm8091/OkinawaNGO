#!/usr/bin/env python3
"""Validate the USN wave-1 controlled integration *design* without writing data."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "outputs" / "us_presence_controlled_integration_design_v1"

CENTRAL_HASHES = {
    "data/interim/01_actor_registry_initial_v0.csv": "c77dbc62e2a1019269a9a5ef5d64d1ac14f4cd54e4abf4b45953e33a67c22df4",
    "data/interim/02_actor_aliases_initial_v0.csv": "e1e8160d33aa975d6374ba38f8490e182b832a96b7bbed285cd94d29b522b52d",
    "data/interim/05_source_log_initial_v0.csv": "363f21256d074cc9577752728b1f950c5c899991fefeea633e86fb78c2aaf902",
    "data/interim/15_funding_or_support_edges_sample_v0.csv": "3b11795150e7630ccf4cdab371ac135fab019c260609ee1272df518638f3ef23",
}

DECISION_MAPS = {
    "service": (
        "outputs/us_presence_service_recon_v1/human_review_queue_v1.csv",
        "hr_id",
        "principal_decision",
        13,
        "94676e4f19d06d697d0c42e8d9316b17757f67bc18a38b34f8a7b76612ccbc2d",
    ),
    "accountability": (
        "outputs/us_presence_accountability_recon_v1/human_review_queue_v1.csv",
        "review_item_id",
        "principal_decision",
        9,
        "74a5c861cff5086463670a15e3e23848e65a6545c38e8769b7e7250b2b46522b",
    ),
    "directory": (
        "outputs/actor_directory_v1/HR_USN_actor_directory_decisions_v1.csv",
        "review_item_id",
        "decision",
        65,
        "3456b50fbb659a94810ab0f57d1f608206b1b04aee8e16661a4769039f85191b",
    ),
    "relation_rules": (
        "outputs/us_presence_relation_retype_v1/HR_USN_relation_retype_rules_v1.csv",
        "mapping_rule_id",
        "decision",
        6,
        "3d5f643c3d7ca1b51c1f077da2dcad70fa58bcad2b568816ca2c40a837e22629",
    ),
}

EXPECTED_DESIGN_COUNTS = {
    "expected_central_actions_v1.csv": ("action_id", 37),
    "expected_table_deltas_v1.csv": ("delta_id", 18),
    "id_namespace_plan_v1.csv": ("namespace", 13),
    "source_admission_plan_v1.csv": ("step_id", 10),
    "test_matrix_v1.csv": ("test_id", 35),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_authoritative_manifest() -> None:
    path = ROOT / "outputs/us_presence_network_wave1_v1/post_principal_manifest_v1.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    files = manifest["files"]
    require(len(files) == 23, f"Expected 23 authoritative files, found {len(files)}")
    for item in files:
        target = ROOT / item["path"]
        require(target.is_file(), f"Missing authoritative file: {item['path']}")
        require(sha256(target) == item["sha256"], f"Authoritative hash drift: {item['path']}")
        require(target.stat().st_size == item["bytes"], f"Authoritative byte drift: {item['path']}")
    require(manifest["central_writeback_performed"] is False, "Upstream manifest unexpectedly reports central writeback")
    require(manifest["relation_crosswalk_expanded"] is False, "Relation crosswalk must remain unexpanded")


def validate_exact_decision_maps() -> None:
    for label, (relative, id_col, decision_col, expected_count, expected_hash) in DECISION_MAPS.items():
        rows = read_csv(ROOT / relative)
        require(len(rows) == expected_count, f"{label} decision count drift")
        pairs = sorted(f"{row[id_col]}={row[decision_col]}" for row in rows)
        require(len(pairs) == len(set(pairs)), f"{label} duplicate ID-decision pair")
        digest = hashlib.sha256("\n".join(pairs).encode("utf-8")).hexdigest()
        require(digest == expected_hash, f"{label} exact ID-to-decision mapping drift")

    arch_path = ROOT / "outputs/us_presence_network_architecture_v1/principal_checkpoint_return_v1.json"
    arch = json.loads(arch_path.read_text(encoding="utf-8"))
    pairs = sorted(f"{row['item_id']}={row['decision']}" for row in arch["decisions"])
    digest = hashlib.sha256("\n".join(pairs).encode("utf-8")).hexdigest()
    require(len(pairs) == 5, "Architecture decision count drift")
    require(digest == "77deaa00e36d71768fa653b34373094ae0fadb7452e9a4b1fc5123e73c9f28df", "Architecture exact decision mapping drift")
    require(arch["central_writeback_authorized"] is False, "Central writeback must remain unauthorized")
    require(arch["publication_adapter_authorized"] is False, "Publication adapter must remain unauthorized")
    require(arch["frontend_writeback_authorized"] is False, "Frontend writeback must remain unauthorized")


def validate_central_baseline() -> None:
    for relative, expected in CENTRAL_HASHES.items():
        require(sha256(ROOT / relative) == expected, f"Central baseline drift: {relative}")
    actors = read_csv(ROOT / "data/interim/01_actor_registry_initial_v0.csv")
    actor_ids = {row["actor_id"] for row in actors}
    require(all(f"X{number:03d}" not in actor_ids for number in range(18, 24)), "Reserved actor ID X018-X023 already occupied")


def validate_design_tables() -> None:
    for filename, (id_col, expected_count) in EXPECTED_DESIGN_COUNTS.items():
        rows = read_csv(PKG / filename)
        require(len(rows) == expected_count, f"{filename} expected {expected_count} rows, found {len(rows)}")
        ids = [row[id_col] for row in rows]
        require(all(ids), f"{filename} has blank {id_col}")
        require(len(ids) == len(set(ids)), f"{filename} has duplicate {id_col}")

    actions = {row["action_id"]: row for row in read_csv(PKG / "expected_central_actions_v1.csv")}
    require(actions["USI-015"]["proposed_value"] == "regional_branch", "F017 plan is not regional_branch")
    require(actions["USI-016"]["proposed_value"] == "regional_branch", "F043 plan is not regional_branch")
    require(actions["USI-018"]["proposed_value"] == "no flow", "KOSC 2580 hold is missing")
    require(actions["USI-037"]["authorization"] == "explicitly_not_authorized", "Publication prohibition is missing")

    deltas = {row["delta_id"]: row for row in read_csv(PKG / "expected_table_deltas_v1.csv")}
    require(deltas["USD-004"]["future_delta"] == "0", "Legacy relation central delta must be zero")
    require(deltas["USD-018"]["future_delta"] == "0", "Publication/frontend delta must be zero")

    tests = {row["test_id"] for row in read_csv(PKG / "test_matrix_v1.csv")}
    require("UST-002" in tests, "Exact ID-to-decision mapping test is missing")
    require("UST-031" in tests, "Failure injection test is missing")
    require("UST-033" in tests, "Publication leakage test is missing")


def validate_unexpanded_relation_crosswalk() -> None:
    rows = read_csv(ROOT / "outputs/us_presence_relation_retype_v1/relation_retype_crosswalk_v1.csv")
    require(len(rows) == 43, "Relation crosswalk no longer has 43 rows")
    require(len({row["edge_id"] for row in rows}) == 43, "Relation crosswalk edge IDs are not unique")
    require(all(not row["mapping_decision"] for row in rows), "Relation crosswalk was expanded before authorization")


def validate_design_manifest() -> None:
    manifest_path = PKG / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["status"] == "design_only_no_central_writeback", "Wrong package status")
    for item in manifest["files"]:
        target = ROOT / item["path"]
        require(target.is_file(), f"Missing design file: {item['path']}")
        require(sha256(target) == item["sha256"], f"Design manifest hash drift: {item['path']}")
        require(target.stat().st_size == item["bytes"], f"Design manifest byte drift: {item['path']}")


def main() -> None:
    validate_authoritative_manifest()
    validate_exact_decision_maps()
    validate_central_baseline()
    validate_design_tables()
    validate_unexpanded_relation_crosswalk()
    validate_design_manifest()
    require(not (ROOT / "data/interim/usn_v1").exists(), "Typed central directory exists before writeback approval")
    require(not (ROOT / "scripts/integrate_usn_wave1_v1.py").exists(), "Apply merger exists before authorization")
    print("PASS_DESIGN_ONLY")
    print("authoritative_files=23")
    print("central_files_unchanged=4")
    print("design_actions=37")
    print("mandatory_tests=35")


if __name__ == "__main__":
    main()
