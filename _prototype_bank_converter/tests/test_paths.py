import sys
import tempfile
import unittest
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.paths import BB2_DIR, BB3_DIR, BB_DIR, GENERATED_OUTPUT_DIR, collect_pdf_paths


class TestPaths(unittest.TestCase):
    def test_default_paths_keep_bb_workflow(self):
        self.assertEqual(BB_DIR.name, "BB")
        self.assertEqual(BB2_DIR.name, "BB2")
        self.assertEqual(BB3_DIR.name, "BB3")
        self.assertEqual(GENERATED_OUTPUT_DIR.name, "generated_output")

    def test_collect_pdf_paths_from_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            first = tmp_path / "a.pdf"
            second = tmp_path / "b.PDF"
            ignored = tmp_path / "notes.txt"
            first.write_text("a")
            second.write_text("b")
            ignored.write_text("ignored")

            self.assertEqual(collect_pdf_paths(tmp_path), [first, second])

    def test_collect_pdf_paths_rejects_non_pdf_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            text_file = Path(tmp) / "notes.txt"
            text_file.write_text("not a pdf")
            with self.assertRaises(ValueError):
                collect_pdf_paths(text_file)


if __name__ == "__main__":
    unittest.main()
