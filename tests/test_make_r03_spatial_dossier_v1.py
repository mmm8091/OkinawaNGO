import importlib.util
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_r03_spatial_dossier_v1",
    ROOT / "scripts" / "make_r03_spatial_dossier_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class SpatialDossierMergeRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edges = MODULE.read_csv(MODULE.EDGES)
        actors = {row["actor_id"]: row for row in MODULE.read_csv(MODULE.ACTORS)}
        places = {row["place_id"]: row for row in MODULE.read_csv(MODULE.PLACES)}
        cls.rows = MODULE.build_semantic_rows(cls.edges, actors, places)

    def test_reviewed_spatial_overlay_is_applied(self):
        inclusion = Counter(row["analysis_inclusion"] for row in self.rows)
        freeze = Counter(row["semantic_freeze_status"] for row in self.rows)
        self.assertEqual(inclusion, {"active": 130, "excluded": 5})
        self.assertEqual(freeze["human_frozen"], 42)
        self.assertEqual(freeze["retired_by_human_review"], 5)
        self.assertEqual(freeze["needs_human_semantic_review"], 0)

    def test_ap123_is_resolved_to_camp_foster(self):
        row = next(row for row in self.rows if row["edge_id"] == "AP123")
        self.assertEqual(row["place_id"], "P007")
        self.assertEqual(row["place_name_integrity"], "match")
        self.assertEqual(row["semantic_candidate_v1"], "site_presence")
        self.assertEqual(row["semantic_freeze_status"], "human_frozen")


if __name__ == "__main__":
    unittest.main()
