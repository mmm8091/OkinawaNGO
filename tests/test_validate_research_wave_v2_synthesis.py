from __future__ import annotations

import unittest

from scripts.validate_research_wave_v2_synthesis import validate


class ResearchWaveV2SynthesisTest(unittest.TestCase):
    def test_synthesis_boundaries(self) -> None:
        lines = validate(write_report=False)
        self.assertIn("- Result: **PASS**", lines)
        self.assertTrue(
            any("research_only / not_frontend_ready" in line for line in lines)
        )


if __name__ == "__main__":
    unittest.main()

