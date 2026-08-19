import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_us_presence_accountability_recon_v1",
    ROOT / "scripts" / "make_us_presence_accountability_recon_v1.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def hash_tree(root: Path):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class USPresenceAccountabilityReconTests(unittest.TestCase):
    def test_generator_outputs_bounded_research_package(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "package"
            counts = MODULE.generate(output)
            self.assertEqual(8, counts["actor_scope"])
            self.assertEqual(6, sum(
                row["counts_in_six_actor_accountability_subset"] == "yes"
                for row in read_csv(output / "accountability_actor_scope_v1.csv")
            ))
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("research_only", manifest["status"]["package_scope"])
            self.assertEqual("no", manifest["status"]["central_writeback"])

    def test_money_semantics_do_not_turn_fee_award_or_nofo_into_grants(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "package"
            MODULE.generate(output)
            rows = {
                row["resource_observation_id"]: row
                for row in read_csv(output / "resource_observations_v1.csv")
            }
            self.assertEqual(
                "court_awarded_attorney_fees_and_costs",
                rows["USAR001"]["resource_type"],
            )
            self.assertEqual("", rows["USAR001"]["provider_actor_id"])
            self.assertIn("Do not encode as a donation", rows["USAR001"]["interpretation_limit"])
            self.assertEqual("", rows["USAR002"]["receiver_actor_id"])
            self.assertIn("opportunity", rows["USAR002"]["resource_type"])

    def test_new_relations_are_not_silently_approved(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "package"
            MODULE.generate(output)
            rows = {
                row["observation_id"]: row
                for row in read_csv(output / "action_relation_observations_v1.csv")
            }
            self.assertEqual(
                "candidate_human_review_required", rows["USAA005"]["status"]
            )
            self.assertEqual("no", rows["USAA005"]["central_writeback"])
            self.assertEqual(
                "off_graph_until_endpoint_review", rows["USAA006"]["graph_gate"]
            )

    def test_person_bridge_is_two_roles_not_an_actor_merge(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "package"
            MODULE.generate(output)
            roles = [
                row
                for row in read_csv(output / "person_role_observations_v1.csv")
                if row["person_name_as_source"] == "Hideki Yoshikawa"
            ]
            self.assertEqual({"A001", "A002"}, {row["actor_id_candidate"] for row in roles})
            self.assertTrue(all(row["central_writeback"] == "no" for row in roles))

    def test_generation_is_byte_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            first = Path(temp) / "first"
            second = Path(temp) / "second"
            MODULE.generate(first)
            MODULE.generate(second)
            self.assertEqual(hash_tree(first), hash_tree(second))


if __name__ == "__main__":
    unittest.main()
