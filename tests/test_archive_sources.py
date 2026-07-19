import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "archive_sources", ROOT / "scripts" / "archive_sources.py"
)
ARCHIVE_SOURCES = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(ARCHIVE_SOURCES)


class ArchiveSourceHeaderTests(unittest.TestCase):
    def test_default_request_headers_identify_project_archiver(self):
        headers = ARCHIVE_SOURCES.request_headers("https://example.org/report.pdf")
        self.assertEqual(headers["User-Agent"], ARCHIVE_SOURCES.USER_AGENT)
        self.assertNotIn("Referer", headers)

    def test_researchmap_attachment_uses_parent_referer(self):
        url = "https://researchmap.jp/teppy/presentations/10378736/attachment_file.pdf"
        headers = ARCHIVE_SOURCES.request_headers(url)
        self.assertEqual(headers["User-Agent"], ARCHIVE_SOURCES.BROWSER_USER_AGENT)
        self.assertEqual(
            headers["Referer"],
            "https://researchmap.jp/teppy/presentations/10378736",
        )


if __name__ == "__main__":
    unittest.main()
