from __future__ import annotations

import csv
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "registry_expansion_gate_v1"
GATE = OUT / "registry_expansion_gate_v1.csv"
SOURCES = OUT / "source_proposals_v1.csv"
HR013 = OUT / "HR013_evidence_addendum_v1.csv"
HR011 = OUT / "HR011_C015_reopen_addendum_v1.csv"
MERGE = OUT / "merge_field_candidates_v1.csv"
INTERIM = ROOT / "data" / "interim" / "29_registry_expansion_gate_v1.csv"
REPORT = OUT / "validation_report_v1.md"

EXPECTED = {"C010", "C011", "C015", "C029", "C030", "C031", "C032", "C033", "C034"}
EXPECTED_HR013 = EXPECTED - {"C015"}
ALLOWED_GATES = {"ready_for_human_decision", "not_ready_online", "out_of_scope_candidate"}
BLANK_REVIEW_FIELDS = ("decision", "reviewer", "review_date", "review_note")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def refs(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    gate = read_csv(GATE)
    sources = read_csv(SOURCES)
    hr013 = read_csv(HR013)
    hr011 = read_csv(HR011)
    merge = read_csv(MERGE)

    gate_ids = [row["candidate_id"] for row in gate]
    require(set(gate_ids) == EXPECTED, f"gate IDs differ: {gate_ids}")
    require(len(gate_ids) == len(set(gate_ids)) == 9, "gate must contain 9 unique candidates")
    require(all(row["machine_gate"] in ALLOWED_GATES for row in gate), "unknown gate value")

    source_ids = [row["proposal_id"] for row in sources]
    require(len(source_ids) == len(set(source_ids)), "duplicate source proposal ID")
    source_id_set = set(source_ids)
    require(all(row["claim_or_relation_approved"] == "no" for row in sources), "source proposal approved a claim/relation")

    for row in gate:
        missing = refs(row["source_proposal_refs"]) - source_id_set
        require(not missing, f"{row['candidate_id']} missing source refs: {sorted(missing)}")
        require(row["non_oneoff_signatory_test"].startswith("pass"), f"{row['candidate_id']} failed one-off test")

    require({row["candidate_id"] for row in hr013} == EXPECTED_HR013, "HR-013 addendum IDs differ")
    require([row["candidate_id"] for row in hr011] == ["C015"], "HR-011 reopen must contain only C015")
    for row in hr013 + hr011:
        for field in BLANK_REVIEW_FIELDS:
            require(row[field] == "", f"{row['candidate_id']} has prefilled {field}")
        missing = refs(row["source_proposal_refs"]) - source_id_set
        require(not missing, f"{row['candidate_id']} HR packet has missing source refs")

    require(all(row["human_decision"] == "" for row in merge), "merge candidate has a prefilled human decision")
    require(all(row["candidate_id"] in EXPECTED for row in merge), "merge field contains unknown candidate")

    by_id = {row["candidate_id"]: row for row in gate}
    require(by_id["C015"]["hr_route"] == "HR-011-C015 reopen addendum", "C015 HR route is wrong")
    require(by_id["C030"]["machine_gate"] == "out_of_scope_candidate", "C030 scope gate drifted")
    require(by_id["C030"]["machine_count_ready"] == "no", "C030 must not be count-ready")
    require(by_id["C034"]["origin_layer_proposed"] == "mixed_or_network", "C034 mixed origin lost")
    require("A094" in by_id["C011"]["existing_actor_collision_check"], "C011/A094 dedup note missing")
    require(not any(row["origin_layer_proposed"] == "japan_domestic" for row in gate), "mainland-solidarity candidate must be separately layered")

    counts = Counter(row["machine_gate"] for row in gate)
    require(counts["ready_for_human_decision"] >= 2, "fewer than two candidates reached the human-decision gate")

    shutil.copyfile(GATE, INTERIM)
    report = (
        "# Registry expansion gate validation v1\n\n"
        "- candidates: 9/9\n"
        f"- ready_for_human_decision: {counts['ready_for_human_decision']}\n"
        f"- not_ready_online: {counts['not_ready_online']}\n"
        f"- out_of_scope_candidate: {counts['out_of_scope_candidate']}\n"
        f"- source proposals: {len(sources)}; claim/relation approvals: 0\n"
        f"- HR-013 addendum rows: {len(hr013)}; HR-011-C015 reopen rows: {len(hr011)}\n"
        "- human decision/reviewer/date/note fields: all blank\n"
        "- one-off signatory shortcuts: 0\n"
        "- registry/source-log/main-edge writes: 0\n"
        f"- interim copy: `{INTERIM.relative_to(ROOT).as_posix()}`\n"
    )
    REPORT.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
