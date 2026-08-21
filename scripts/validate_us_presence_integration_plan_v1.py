#!/usr/bin/env python3
"""Validate the persisted USN wave-1 plan and synthetic sandbox receipt."""

from pathlib import Path

from plan_usn_wave1_integration_v1 import (
    validate_usn_wave1_plan_package,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    report = validate_usn_wave1_plan_package(
        ROOT,
        ROOT / "outputs/us_presence_integration_plan_v1",
    )
    print(report["status"])
    print(f"plan_id={report['plan_id']}")
    print(f"actions={report['actions']}")
    print(f"source_clusters={report['source_clusters']}")
    print(f"leg_changed_cells={report['leg_changed_cells']}")
    print("central_writeback_authorized=false")


if __name__ == "__main__":
    main()
