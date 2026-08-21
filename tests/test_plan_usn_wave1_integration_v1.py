from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.plan_usn_wave1_integration_v1 import (
    PlanValidationError,
    make_synthetic_frozen_plan,
    materialize_usn_wave1_plan,
    plan_usn_wave1_integration,
    simulate_usn_wave1_integration,
    validate_usn_wave1_plan_package,
    verify_usn_wave1_plan_in_sandbox,
)


ROOT = Path(__file__).resolve().parents[1]
CENTRAL_PATHS = (
    "data/interim/01_actor_registry_initial_v0.csv",
    "data/interim/02_actor_aliases_initial_v0.csv",
    "data/interim/05_source_log_initial_v0.csv",
    "data/interim/15_funding_or_support_edges_sample_v0.csv",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def seed_plan_root(target: Path) -> None:
    for relative in (
        "outputs/us_presence_network_wave1_v1",
        "outputs/us_presence_controlled_integration_design_v1",
        "outputs/us_presence_service_recon_v1",
        "outputs/us_presence_accountability_recon_v1",
        "outputs/us_presence_network_architecture_v1",
        "outputs/us_presence_relation_retype_v1",
        "outputs/actor_directory_v1",
    ):
        shutil.copytree(ROOT / relative, target / relative, dirs_exist_ok=True)
    for relative in CENTRAL_PATHS:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    for manifest_relative in (
        "outputs/us_presence_network_wave1_v1/post_principal_manifest_v1.json",
        "outputs/us_presence_controlled_integration_design_v1/manifest.json",
    ):
        manifest = json.loads((ROOT / manifest_relative).read_text(encoding="utf-8"))
        for item in manifest["files"]:
            source = ROOT / item["path"]
            destination = target / item["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


class PlanUsnWave1IntegrationV1Tests(unittest.TestCase):
    def test_real_plan_is_read_only_and_reports_the_source_freeze_blocker(self) -> None:
        protected_before = {relative: sha256(ROOT / relative) for relative in CENTRAL_PATHS}
        relation_before = (
            ROOT
            / "outputs/us_presence_relation_retype_v1/"
            "relation_retype_crosswalk_v1.csv"
        ).read_bytes()

        plan = plan_usn_wave1_integration(ROOT)

        self.assertEqual("blocked_pending_source_freeze", plan["status"])
        self.assertFalse(plan["authority"]["central_writeback"])
        self.assertFalse(plan["authority"]["relation_crosswalk_expansion"])
        self.assertFalse(plan["authority"]["publication_adapter"])
        self.assertFalse(plan["authority"]["frontend_writeback"])
        self.assertEqual(37, len(plan["actions"]))
        self.assertEqual(18, len(plan["table_deltas"]))
        self.assertEqual(35, len(plan["test_results"]))
        self.assertEqual(6, len(plan["actor_admission_preview"]))
        self.assertEqual(43, len(plan["relation_overlay_preview"]))
        self.assertEqual(65, len(plan["directory_overlay_preview"]))
        self.assertEqual(
            {"X018", "X019", "X020", "X021", "X022", "X023"},
            {row["actor_id"] for row in plan["actor_admission_preview"]},
        )
        self.assertEqual(
            "pending_official_receipt_review",
            plan["source_admission"]["status"],
        )
        self.assertEqual(9, plan["source_admission"]["propublica_interfaces"])
        self.assertEqual([], plan["source_admission"]["allocated_source_ids"])
        self.assertTrue(
            any(
                blocker["blocker_id"] == "USB-001"
                for blocker in plan["blockers"]
            )
        )
        self.assertEqual(
            protected_before,
            {relative: sha256(ROOT / relative) for relative in CENTRAL_PATHS},
        )
        self.assertEqual(
            relation_before,
            (
                ROOT
                / "outputs/us_presence_relation_retype_v1/"
                "relation_retype_crosswalk_v1.csv"
            ).read_bytes(),
        )

    def test_overlay_is_exact_and_changes_only_two_record_families(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        rows = plan["relation_overlay_preview"]
        self.assertEqual(43, len({row["edge_id"] for row in rows}))
        changed = {
            row["edge_id"]
            for row in rows
            if row["approved_record_family"] != row["proposed_record_family"]
        }
        self.assertEqual({"F017", "F043"}, changed)
        for row in rows:
            if row["edge_id"] in changed:
                self.assertEqual("regional_branch", row["approved_record_family"])
                self.assertEqual("revise", row["mapping_decision"])
            else:
                self.assertEqual(
                    row["proposed_record_family"], row["approved_record_family"]
                )
                self.assertEqual("accept", row["mapping_decision"])

    def test_materialized_plan_is_deterministic_and_contains_no_absolute_paths(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        with tempfile.TemporaryDirectory() as left_dir, tempfile.TemporaryDirectory() as right_dir:
            left = Path(left_dir) / "plan"
            right = Path(right_dir) / "plan"
            materialize_usn_wave1_plan(plan, left)
            materialize_usn_wave1_plan(plan, right)
            self.assertEqual(tree_hash(left), tree_hash(right))
            payload = "\n".join(
                path.read_text(encoding="utf-8-sig", errors="ignore")
                for path in left.rglob("*")
                if path.is_file()
            )
            self.assertNotIn(str(ROOT), payload)
            self.assertNotIn(left_dir, payload)

    def test_source_clusters_preserve_reuse_and_allocate_no_real_source_ids(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        rows = plan["source_clusters"]
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["source_resolution"]] = counts.get(row["source_resolution"], 0) + 1
            self.assertEqual("", row["final_source_id"])
        self.assertEqual(
            {
                "reuse_existing": 4,
                "candidate_new_non_propublica": 44,
                "hold_official_irs_receipt": 9,
            },
            counts,
        )
        self.assertEqual(57, len(rows))
        self.assertEqual(8, len(plan["derived_source_requirements"]))

    def test_plan_stops_on_central_hash_drift_before_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seed_plan_root(root)
            actor_path = root / CENTRAL_PATHS[0]
            actor_path.write_bytes(actor_path.read_bytes() + b"\n")
            with self.assertRaisesRegex(PlanValidationError, "central baseline hash drift"):
                plan_usn_wave1_integration(root)

    def test_plan_stops_on_reserved_actor_collision_even_if_hash_receipt_is_updated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seed_plan_root(root)
            actor_path = root / CENTRAL_PATHS[0]
            with actor_path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                fields = list(reader.fieldnames or [])
                rows = list(reader)
            collision = dict(next(row for row in rows if row["actor_id"] == "X017"))
            collision["actor_id"] = "X018"
            collision["canonical_name"] = "collision fixture"
            rows.append(collision)
            with actor_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            design_manifest_path = (
                root / "outputs/us_presence_controlled_integration_design_v1/manifest.json"
            )
            design_manifest = json.loads(design_manifest_path.read_text(encoding="utf-8"))
            design_manifest["central_baseline"][CENTRAL_PATHS[0]] = sha256(actor_path)
            design_manifest_path.write_text(
                json.dumps(design_manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(PlanValidationError, "reserved actor ID collision: X018"):
                plan_usn_wave1_integration(root)

    def test_leg_projection_is_an_exact_33_cell_copy_transform(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        leg = plan["leg_projection"]
        self.assertEqual(33, len(leg["field_diffs"]))
        self.assertEqual(
            {"LEG0": 3, "LEG1": 9, "LEG2": 0, "LEG3": 0},
            leg["distribution"],
        )
        self.assertEqual(70, len(leg["tables"]["vocabulary"]["rows"]))
        self.assertEqual(44, len(leg["tables"]["validation_rules"]["rows"]))
        self.assertEqual(10, len(leg["tables"]["vertical_slices"]["rows"]))
        self.assertEqual(12, len(leg["tables"]["legitimation_observations"]["rows"]))
        self.assertEqual(10, len(leg["tables"]["table_contracts"]["rows"]))

    def test_typed_projection_keeps_sensitive_semantics_separate(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        typed = plan["typed_fact_projection"]
        rf002 = next(row for row in typed["money"] if row["upstream_id"] == "RF002")
        self.assertEqual(
            ("X007", "X004", "8479", "USD", "2024-07-01", "2025-06-30"),
            (
                rf002["source_endpoint"],
                rf002["target_endpoint"],
                rf002["amount"],
                rf002["currency"],
                rf002["period_start"],
                rf002["period_end"],
            ),
        )
        rf001 = next(row for row in typed["money"] if row["upstream_id"] == "RF001")
        self.assertEqual("hold_no_flow", rf001["disposition"])
        self.assertEqual(2, len(typed["accounting"]))
        self.assertTrue(all(row["directed_money_edge"] == "no" for row in typed["accounting"]))
        self.assertTrue(all(not row["role_start"] for row in typed["person_roles"]))
        self.assertTrue(all(row["derived_actor_dyad"] == "no" for row in typed["person_roles"]))
        usaa005 = next(
            row for row in typed["actions"] if row["observation_id"] == "USAA005"
        )
        self.assertEqual("EO_R5_FUTAMI_TEN_DISTRICTS", usaa005["target_endpoint"])
        self.assertEqual("off_graph", usaa005["graph_eligibility"])
        self.assertEqual(2, len(typed["affiliation"]))
        self.assertEqual(6, len(typed["sponsor_snapshots"]))

    def test_real_blocked_plan_cannot_be_simulated_as_frozen(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        with tempfile.TemporaryDirectory() as sandbox_dir:
            with self.assertRaisesRegex(PlanValidationError, "source plan is not frozen"):
                simulate_usn_wave1_integration(ROOT, Path(sandbox_dir), plan)

    def test_synthetic_sandbox_is_deterministic_and_byte_idempotent(self) -> None:
        real_plan = plan_usn_wave1_integration(ROOT)
        plan = make_synthetic_frozen_plan(real_plan)
        protected_before = {relative: sha256(ROOT / relative) for relative in CENTRAL_PATHS}
        with tempfile.TemporaryDirectory() as sandbox_dir:
            sandbox = Path(sandbox_dir)
            first = simulate_usn_wave1_integration(ROOT, sandbox, plan)
            generation = Path(first["generation_path"])
            first_hash = tree_hash(generation)
            second = simulate_usn_wave1_integration(ROOT, sandbox, plan)

            self.assertTrue(first["created"])
            self.assertFalse(second["created"])
            self.assertEqual(0, second["changed_files"])
            self.assertEqual(first_hash, tree_hash(generation))
            report = json.loads(
                (generation / "sandbox_validation_report_v1.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual("PASS_SYNTHETIC_SANDBOX_ONLY", report["status"])
            self.assertFalse(report["claims_real_writeback_ready"])
            overlay = read_csv(generation / "relation_retype_overlay_v1.csv")
            self.assertEqual(43, len(overlay))
            self.assertEqual(
                {"F017", "F043"},
                {
                    row["edge_id"]
                    for row in overlay
                    if row["mapping_decision"] == "revise"
                },
            )
        self.assertEqual(
            protected_before,
            {relative: sha256(ROOT / relative) for relative in CENTRAL_PATHS},
        )

    def test_failure_injection_leaves_no_generation_or_temporary_files(self) -> None:
        plan = make_synthetic_frozen_plan(plan_usn_wave1_integration(ROOT))
        for stage in ("after_validation", "after_projection", "before_commit"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as sandbox_dir:
                sandbox = Path(sandbox_dir)
                with self.assertRaisesRegex(RuntimeError, f"injected failure: {stage}"):
                    simulate_usn_wave1_integration(
                        ROOT, sandbox, plan, fail_at=stage
                    )
                self.assertFalse((sandbox / "generations").exists())
                self.assertEqual([], list(sandbox.rglob("*.tmp")))

    def test_simulator_refuses_real_or_nested_project_targets(self) -> None:
        plan = make_synthetic_frozen_plan(plan_usn_wave1_integration(ROOT))
        for target in (ROOT, ROOT / "tmp" / "usn-sandbox"):
            with self.subTest(target=target):
                with self.assertRaisesRegex(PlanValidationError, "outside source root"):
                    simulate_usn_wave1_integration(ROOT, target, plan)

    def test_public_sandbox_verifier_reports_only_synthetic_readiness(self) -> None:
        plan = plan_usn_wave1_integration(ROOT)
        receipt = verify_usn_wave1_plan_in_sandbox(ROOT, plan)

        self.assertEqual("PASS_SYNTHETIC_SANDBOX_ONLY", receipt["status"])
        self.assertEqual("blocked_pending_source_freeze", receipt["real_plan_status"])
        self.assertFalse(receipt["claims_real_writeback_ready"])
        self.assertTrue(receipt["first_projection_created"])
        self.assertTrue(receipt["second_projection_byte_noop"])
        self.assertEqual(
            ["after_projection", "after_validation", "before_commit"],
            receipt["failure_injection_stages_passed"],
        )
        self.assertEqual(0, receipt["changed_protected_source_files"])

    def test_materialized_repository_plan_package_validates_against_fresh_plan(self) -> None:
        report = validate_usn_wave1_plan_package(
            ROOT, ROOT / "outputs/us_presence_integration_plan_v1"
        )
        self.assertEqual("PASS_PLAN_PACKAGE_BLOCKED", report["status"])
        self.assertEqual(37, report["actions"])
        self.assertEqual(57, report["source_clusters"])
        self.assertEqual(33, report["leg_changed_cells"])
        self.assertEqual(0, report["central_files_changed"])


if __name__ == "__main__":
    unittest.main()
