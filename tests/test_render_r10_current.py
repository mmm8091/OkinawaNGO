import hashlib
import importlib.util
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_r10_current",
    ROOT / "scripts" / "render_r10_current.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurrentR10RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = MODULE.load_current()
        MODULE.validate_current(cls.tables)

    def test_current_counts_and_review_layers_are_locked(self):
        self.assertEqual(43, len(self.tables["sample"]))
        self.assertEqual(35, len(self.tables["relations"]))
        self.assertEqual(28, len(self.tables["amounts"]))
        self.assertEqual(43, len(self.tables["functions"]))
        self.assertEqual(
            MODULE.EXPECTED_R10_REVIEW_COUNTS,
            Counter(row["review_status"] for row in self.tables["relations"]),
        )
        self.assertEqual(
            MODULE.EXPECTED_AMOUNT_REVIEW_COUNTS,
            Counter(row["review_status"] for row in self.tables["amounts"]),
        )

    def test_f008_is_current_typed_layer_not_old_evidence_filter(self):
        rows = MODULE.strict_sample_rows(self.tables["sample"])
        self.assertEqual(16, len(rows))
        self.assertEqual(
            MODULE.EXPECTED_STRICT_PANEL_COUNTS,
            Counter(row["graph_eligibility"] for row in rows),
        )
        self.assertEqual(
            Counter({"human_checked": 8, "human_revised": 8}),
            Counter(row["review_status"] for row in rows),
        )
        self.assertFalse(any(row["relation_type"] == "grant_opportunity" for row in rows))

    def test_r10_boundaries_are_preserved(self):
        self.assertEqual(
            MODULE.EXPECTED_MECHANISM_COUNTS,
            Counter(
                MODULE.classify_mechanism(row)
                for row in self.tables["relations"]
            ),
        )
        self.assertEqual(
            MODULE.EXPECTED_AMOUNT_BOUNDARY_COUNTS,
            Counter(MODULE.classify_amount(row) for row in self.tables["amounts"]),
        )
        self.assertEqual(
            5,
            sum(
                row["amount_basis"] == "actual_contract_amount"
                for row in self.tables["amounts"]
            ),
        )
        self.assertEqual(
            14,
            sum(
                MODULE.classify_amount(row) == "项目／事业成本"
                for row in self.tables["amounts"]
            ),
        )
        self.assertTrue(
            all(
                row["financial_inference_allowed"] == "no"
                and row["political_stance_inference_allowed"] == "no"
                for row in self.tables["functions"]
            )
        )

    def test_svg_text_states_the_non_inference_rules(self):
        f008 = MODULE.render_f008(self.tables["sample"])
        f031 = MODULE.render_f031(
            self.tables["relations"],
            self.tables["functions"],
            self.tables["hr032"],
        )
        f032 = MODULE.render_f032(self.tables["amounts"])
        combined = f008 + f031 + f032
        self.assertIn("不等于 award", combined)
        self.assertIn("service 不产生政治立场", combined)
        self.assertIn("co-presence", combined)
        self.assertIn("不生成稳定联盟", combined)
        self.assertIn("不是 actor payment", combined)
        self.assertIn("仅 5 条 amount_basis=actual_contract_amount", combined)

    def test_renderer_writes_only_six_assets_and_does_not_touch_inputs_or_pngs(self):
        inputs = [
            MODULE.RELATION_SAMPLE_PATH,
            MODULE.R10_RELATIONS_PATH,
            MODULE.R10_AMOUNTS_PATH,
            MODULE.R10_FUNCTIONS_PATH,
            MODULE.HR032_SUMMARY_PATH,
        ]
        pngs = [
            MODULE.PHASE1_OUTPUT_DIR / "fig3_support_service_layers_strict.png",
            MODULE.R10_OUTPUT_DIR / "fig_r10_mechanism_ecology.png",
            MODULE.R10_OUTPUT_DIR / "fig_r10_amount_evidence_boundary.png",
        ]
        before = {path: sha256(path) for path in inputs + pngs}
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            phase1 = temp / "phase1"
            r10 = temp / "r10"
            written = MODULE.render_current(phase1, r10)
            self.assertEqual(MODULE.OUTPUT_FILENAMES, {path.name for path in written})
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {path.name for path in temp.rglob("*") if path.is_file()},
            )
        self.assertEqual(before, {path: sha256(path) for path in inputs + pngs})


if __name__ == "__main__":
    unittest.main()
