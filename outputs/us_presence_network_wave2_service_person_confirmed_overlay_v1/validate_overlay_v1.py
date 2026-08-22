from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROW_LEVEL_FILES = (
    "person_nodes_principal_confirmed_v1.csv",
    "person_actor_role_edges_principal_confirmed_v1.csv",
    "actor_person_projection_principal_confirmed_v1.csv",
    "money_edges_principal_confirmed_v1.csv",
    "layered_network_nodes_v1.csv",
    "layered_network_edges_v1.csv",
)
EXPECTED_ROW_VALUE = "not_applicable_service_only"


def read_csv(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []

    for name in ROW_LEVEL_FILES:
        rows = read_csv(name)
        for line_number, row in enumerate(rows, start=2):
            if row.get("service_side_only") != "yes":
                errors.append(f"{name}:{line_number}: service_side_only must be yes")
            if row.get("cross_ecology_bridge") != EXPECTED_ROW_VALUE:
                errors.append(
                    f"{name}:{line_number}: cross_ecology_bridge must be "
                    f"{EXPECTED_ROW_VALUE!r}, got {row.get('cross_ecology_bridge')!r}"
                )

    structure = {row["metric_id"]: row for row in read_csv("structure_change_summary_v1.csv")}
    cross_status = structure.get("SPN-SC008")
    if cross_status is None:
        errors.append("structure_change_summary_v1.csv: missing SPN-SC008")
    else:
        expected = {
            "before_hr_usn2_01": "not_assessed",
            "after_hr_usn2_01": "not_assessed",
            "delta": "not_applicable",
        }
        for field, value in expected.items():
            if cross_status.get(field) != value:
                errors.append(
                    f"SPN-SC008 {field} must be {value!r}, got {cross_status.get(field)!r}"
                )

    layered = read_csv("layered_network_edges_v1.csv")
    person_count = sum(row["relation_layer"] == "person_role" for row in layered)
    money_count = sum(row["relation_layer"] == "money_flow" for row in layered)
    if (person_count, money_count) != (13, 4):
        errors.append(
            f"layered edge counts must be person_role=13/money_flow=4, "
            f"got {person_count}/{money_count}"
        )

    unresolved = read_csv("unresolved_identity_pairs_v1.csv")
    if len(unresolved) != 1 or unresolved[0].get("projection_excluded") != "yes":
        errors.append("01b must remain one unresolved row excluded from projection")

    money = read_csv("money_edges_principal_confirmed_v1.csv")
    oesc_awwa_total = sum(
        int(row["amount"]) for row in money if row["target_actor_id"] == "X004"
    )
    if oesc_awwa_total != 39158:
        errors.append(f"OESC-to-AWWA money total must be 39158, got {oesc_awwa_total}")

    manifest = json.loads((PACKAGE / "manifest_v1.json").read_text(encoding="utf-8"))
    if manifest["boundaries"].get("cross_ecology_bridge_status") != "not_assessed":
        errors.append("manifest package-level cross_ecology_bridge_status must be not_assessed")
    for item in manifest["files"]:
        path = PACKAGE / item["path"]
        if not path.is_file():
            errors.append(f"manifest missing file: {item['path']}")
            continue
        if path.stat().st_size != item["bytes"]:
            errors.append(f"manifest byte mismatch: {item['path']}")
        if sha256(path) != item["sha256"]:
            errors.append(f"manifest hash mismatch: {item['path']}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "PASS: service-person overlay keeps 50 service-only rows as "
        "not_applicable_service_only and package-level cross-ecology status as not_assessed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
