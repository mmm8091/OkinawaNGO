from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "us_presence_network_wave2_w2_d_v1"
SCRIPT = ROOT / "scripts" / "build_us_presence_network_wave2_w2_d_v1.py"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (OUT / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class TestW2DBridgeAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)

    def test_selection_frame_and_matrix_counts(self) -> None:
        matrix = rows("bridge_audit_matrix_v1.csv")
        self.assertEqual(len(matrix), 4482)
        counts: dict[str, int] = {}
        for row in matrix:
            counts[row["selection_frame_id"]] = counts.get(row["selection_frame_id"], 0) + 1
        self.assertEqual(counts["USF-W2D-BRIDGE-TRACER15-2026-08-22"], 324)
        self.assertEqual(counts["USF-W2D-ECOLOGY-S0-A1R-2026-08-22"], 2214)
        self.assertEqual(counts["USF-W2D-SENSITIVITY-S0-A1C-2026-08-22"], 1944)

    def test_audited_zero_is_narrowly_gated(self) -> None:
        matrix = rows("bridge_audit_matrix_v1.csv")
        zeros = [row for row in matrix if row["audit_result"] == "audited_public_record_zero"]
        self.assertEqual(len(zeros), 36)
        self.assertTrue(all(row["selection_frame_id"] == "USF-W2D-BRIDGE-TRACER15-2026-08-22" for row in zeros))
        self.assertTrue(all(row["relation_family"] == "direct_organization_relation" for row in zeros))
        self.assertTrue(all(row["pair_observability"] == "both_endpoints_observed_in_window" for row in zeros))

    def test_no_cross_ecology_actor_bridge_is_synthesized(self) -> None:
        matrix = rows("bridge_audit_matrix_v1.csv")
        self.assertFalse(any(row["audit_result"] == "confirmed_bridge" for row in matrix))
        edges = rows("typed_egonet_edges_v1.csv")
        self.assertFalse(any(row["counts_as_cross_ecology_actor_bridge"] == "yes" for row in edges))
        dod = [row for row in edges if "DOD" in {row["source_node_id"], row["target_node_id"]}]
        self.assertGreaterEqual(len(dod), 3)
        self.assertTrue(all(row["counts_as_cross_ecology_actor_bridge"] == "no" for row in dod))

    def test_shared_place_and_shared_funder_boundaries(self) -> None:
        matrix = rows("bridge_audit_matrix_v1.csv")
        places = [row for row in matrix if row["relation_family"] == "shared_place_background"]
        self.assertTrue(all(row["audit_result"] != "confirmed_bridge" for row in places))
        funders = [row for row in matrix if row["relation_family"] == "shared_funder_or_sponsor"]
        self.assertFalse(any(row["audit_result"] == "audited_public_record_zero" for row in funders))

    def test_source_coverage_and_review_status(self) -> None:
        coverage = rows("source_family_actor_coverage_v1.csv")
        self.assertEqual(len(coverage), 75)
        self.assertEqual(len({row["actor_id"] for row in coverage}), 15)
        self.assertEqual(len({row["source_family"] for row in coverage}), 5)
        self.assertTrue(all(row["review_status"] == "ai_seeded" for row in coverage))
        self.assertTrue(all(row["package_scope"] == "research_only" for row in coverage))
        self.assertTrue(all(row["frontend_status"] == "not_frontend_ready" for row in coverage))
        self.assertTrue(all(row["central_writeback"] == "no" for row in coverage))

    def test_direct_zero_claim_is_queued_for_principal_review(self) -> None:
        claims = {row["claim_id"]: row for row in rows("claim_table_v1.csv")}
        queue = rows("principal_review_queue_v1.csv")
        self.assertEqual(claims["W2D-CL001"]["principal_decision_needed"], "yes")
        self.assertTrue(any(row["review_item_id"] == "W2D-PR001" for row in queue))

    def test_arc_nmcrs_edge_is_directed_candidate_pending_principal(self) -> None:
        edges = rows("typed_egonet_edges_v1.csv")
        arc_nmcrs = [row for row in edges if row["relation_family"] == "service_intermediation"]
        self.assertEqual(len(arc_nmcrs), 1)
        self.assertEqual(arc_nmcrs[0]["source_node_id"], "X009")
        self.assertEqual(arc_nmcrs[0]["target_node_id"], "X008")
        self.assertEqual(arc_nmcrs[0]["edge_status"], "official_source_supported_candidate_pending_principal")
        self.assertIn("NMCRS delegates", arc_nmcrs[0]["direction_semantics"])
        claims = {row["claim_id"]: row for row in rows("claim_table_v1.csv")}
        self.assertEqual(claims["W2D-CL008"]["principal_decision_needed"], "yes")

    def test_validation_passes_and_receipts_close(self) -> None:
        validation = json.loads((OUT / "validation_report_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(validation["status"], "PASS_RESEARCH_ONLY_W2_D")
        self.assertTrue(all(validation["checks"].values()))
        for row in rows("source_receipts_v1.csv"):
            if row["artifact_path"]:
                self.assertEqual(digest(ROOT / row["artifact_path"]), row["sha256"])

    def test_rebuild_is_byte_deterministic(self) -> None:
        before = {path.name: digest(path) for path in OUT.iterdir() if path.is_file()}
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
        after = {path.name: digest(path) for path in OUT.iterdir() if path.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
