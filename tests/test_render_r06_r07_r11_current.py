import hashlib
import importlib.util
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_r06_r07_r11_current",
    ROOT / "scripts" / "render_r06_r07_r11_current.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurrentPathwayRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = MODULE.load_current()
        MODULE.validate_current(cls.tables)

    def test_current_reviewed_counts_are_locked(self):
        self.assertEqual(6, len(self.tables["r6"]))
        self.assertEqual(9, len(self.tables["r7"]))
        self.assertEqual(53, len(self.tables["r11"]))
        self.assertEqual(
            MODULE.EXPECTED_DOMAIN_COUNTS,
            Counter(row["entry_domain"] for row in self.tables["r11"]),
        )

    def test_r11_explicit_object_classification(self):
        counts = Counter(
            (row["entry_domain"], MODULE.classify_r11_object(row))
            for row in self.tables["r11"]
        )
        self.assertEqual(MODULE.EXPECTED_OBJECT_COUNTS, counts)
        a066 = next(
            row for row in self.tables["r11"] if row["entry_actor_id"] == "A066"
        )
        self.assertEqual(
            "Prefecture/base-policy",
            MODULE.classify_r11_object(a066),
        )
        self.assertNotEqual("USO/service", MODULE.classify_r11_object(a066))

    def test_r6_uses_short_display_labels(self):
        svg = MODULE.render_r6(self.tables["r6"])
        self.assertIn("国际机构请求", svg)
        self.assertIn("行政协作／受托", svg)
        self.assertNotIn("international_institution_request", svg)
        self.assertNotIn("domestic_environmental_solidarity", svg)

    def test_renderer_writes_only_six_figure_files(self):
        input_hashes = {
            filename: sha256(MODULE.DEFAULT_INPUT_DIR / filename)
            for filename in MODULE.INPUT_FILENAMES.values()
        }
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            written = MODULE.render_current(MODULE.DEFAULT_INPUT_DIR, output_dir)
            self.assertEqual(MODULE.OUTPUT_FILENAMES, {path.name for path in written})
            self.assertEqual(
                MODULE.OUTPUT_FILENAMES,
                {path.name for path in output_dir.iterdir()},
            )
        self.assertEqual(
            input_hashes,
            {
                filename: sha256(MODULE.DEFAULT_INPUT_DIR / filename)
                for filename in MODULE.INPUT_FILENAMES.values()
            },
        )

    def test_r11_svg_names_prefecture_column_and_current_total(self):
        svg = MODULE.render_r11(self.tables["r11"])
        self.assertIn("Prefecture/", svg)
        self.assertIn("base-policy", svg)
        self.assertIn("53 条已核进入观察", svg)
        self.assertIn("A066", svg)


if __name__ == "__main__":
    unittest.main()
