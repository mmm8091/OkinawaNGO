from __future__ import annotations

import csv
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_history_1998_2012_online_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("make_history_1998_2012_online_v1", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def tree_hashes(path: Path) -> dict[str, str]:
    return {
        item.name: hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.iterdir())
        if item.is_file()
    }


class NR05PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def build_temp(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        out = Path(temp_dir.name) / "nr05"
        self.module.build(out)
        return temp_dir, out

    def test_contract_counts_constants_and_sensitive_gates(self) -> None:
        temp_dir, out = self.build_temp()
        self.addCleanup(temp_dir.cleanup)

        expected_files = {
            "historical_anchor_candidates.csv",
            "organization_status_candidates.csv",
            "source_candidates.csv",
            "search_log.md",
            "online_exhausted_gaps.csv",
            "human_review_queue.csv",
            "brief.md",
            "README.md",
            "validation_report.md",
            "fig1_carrier_venue_trace_timeline_v1.svg",
            "fig1_carrier_venue_trace_timeline_v1_brief.md",
        }
        self.assertEqual({item.name for item in out.iterdir()}, expected_files)

        anchors = read_csv(out / "historical_anchor_candidates.csv")
        statuses = read_csv(out / "organization_status_candidates.csv")
        sources = read_csv(out / "source_candidates.csv")
        gaps = read_csv(out / "online_exhausted_gaps.csv")
        reviews = read_csv(out / "human_review_queue.csv")

        self.assertEqual(len(anchors), 15)
        self.assertEqual(len(statuses), 11)
        self.assertEqual(len(sources), 32)
        self.assertEqual(len(gaps), 10)
        self.assertEqual(len(reviews), 20)

        for row in [*anchors, *statuses, *sources, *gaps, *reviews]:
            self.assertEqual(row["package_scope"], "research_only")
            self.assertEqual(row["claim_status"], "candidate")
            self.assertEqual(row["review_status"], "ai_seeded")
            self.assertEqual(row["frontend_eligibility"], "not_frontend_ready")
            self.assertEqual(row["central_writeback"], "no")

        anchor_by_id = {row["anchor_id"]: row for row in anchors}
        self.assertEqual(anchor_by_id["H98_001"]["source_relationship"], "secondary")
        self.assertIn("not a census", anchor_by_id["H98_001"]["relation_boundary"].lower())
        self.assertIn(
            "not this project's base-accountability actors",
            anchor_by_id["H98_002"]["relation_boundary"],
        )
        self.assertIn(
            "not converted into an organization",
            anchor_by_id["H98_006"]["relation_boundary"],
        )
        self.assertEqual(anchor_by_id["H98_009"]["actor_ids"], "")
        self.assertIn(
            "not the organizational plaintiff",
            anchor_by_id["H98_009"]["claim_text_candidate"],
        )
        self.assertEqual(anchor_by_id["H98_011"]["actor_ids"], "A005")
        self.assertIn(
            "not a stable alliance",
            anchor_by_id["H98_011"]["relation_boundary"],
        )
        self.assertEqual(anchor_by_id["H98_015"]["source_relationship"], "lead")
        self.assertEqual(anchor_by_id["H98_015"]["evidence_level_proposed"], "E2")
        self.assertEqual(anchor_by_id["H98_003"]["event_date_end"], "2009-05-14")

        for row in anchors:
            self.assertTrue(row["source_publication_date_precision"])
            self.assertTrue(row["event_date_start"])
            self.assertTrue(row["event_date_end"])
            self.assertTrue(row["event_date_precision"])
            self.assertTrue(row["actor_active_period"])
            self.assertTrue(row["claim_period"])

        for row in reviews:
            self.assertEqual(row["queue_role"], "research_candidate_pool")
            self.assertEqual(row["formal_hr_dispatch_status"], "not_dispatched")
            self.assertEqual(row["human_decision"], "")
            self.assertEqual(row["reviewer"], "")
            self.assertEqual(row["review_date"], "")

    def test_source_vocabulary_locator_terminology_and_catalog_boundary(self) -> None:
        temp_dir, out = self.build_temp()
        self.addCleanup(temp_dir.cleanup)
        sources = read_csv(out / "source_candidates.csv")

        allowed = {
            "contemporaneous_primary",
            "retrospective",
            "secondary",
            "lead",
        }
        self.assertLessEqual({row["source_relationship"] for row in sources}, allowed)
        self.assertTrue(all(row["exact_locator"] for row in sources))
        self.assertTrue(all(row["interpretation_limit"] for row in sources))

        source_by_id = {row["source_candidate_id"]: row for row in sources}
        catalog = source_by_id["NR05S026"]
        self.assertEqual(catalog["source_relationship"], "lead")
        self.assertIn("not the underlying document", catalog["interpretation_limit"])

        spencer = source_by_id["NR05S029"]
        self.assertIn("not a novel project finding", spencer["support_scope"])

        onc_portal = source_by_id["NR05S031"]
        self.assertIn("2009-05-14", onc_portal["document_coverage_period"])
        self.assertIn("設立認証年月日 2009年05月14日", onc_portal["exact_locator"])

        npo_hub = source_by_id["NR05S032"]
        self.assertIn("exit-event lower bounds", npo_hub["support_scope"])

        package_text = "\n".join(
            item.read_text(encoding="utf-8")
            for item in out.iterdir()
            if item.suffix in {".md", ".csv", ".svg"}
        )
        self.assertNotIn("recognized-NPO", package_text)
        self.assertNotIn("recognized NPO", package_text)

    def test_known_exclusions_denominators_and_figure_contract(self) -> None:
        temp_dir, out = self.build_temp()
        self.addCleanup(temp_dir.cleanup)

        validation = (out / "validation_report.md").read_text(encoding="utf-8")
        search_log = (out / "search_log.md").read_text(encoding="utf-8")
        brief = (out / "brief.md").read_text(encoding="utf-8")
        svg = (out / "fig1_carrier_venue_trace_timeline_v1.svg").read_text(
            encoding="utf-8"
        )
        figure_brief = (
            out / "fig1_carrier_venue_trace_timeline_v1_brief.md"
        ).read_text(encoding="utf-8")

        self.assertIn("A068→A019", validation)
        self.assertIn("1997 event", validation)
        self.assertIn("does not reopen or rewrite central `LC002`", search_log)
        self.assertIn("denominator differs", search_log)
        self.assertIn("not a count of this project's actors", brief)
        self.assertIn("not a new finding", brief)
        self.assertIn("maintenance/exit costs", brief)
        self.assertIn("online-rich", brief)
        self.assertIn("独立数量轴", svg)
        self.assertIn("禁止与下方面板节点数相除", svg)
        self.assertIn("载体／组织形式", svg)
        self.assertIn("制度场域", svg)
        self.assertIn("留存材料", svg)
        self.assertIn("do not share a numeric y-axis", figure_brief)

    def test_builder_is_byte_deterministic(self) -> None:
        temp_dir, out = self.build_temp()
        self.addCleanup(temp_dir.cleanup)
        first = tree_hashes(out)
        self.module.build(out)
        second = tree_hashes(out)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
