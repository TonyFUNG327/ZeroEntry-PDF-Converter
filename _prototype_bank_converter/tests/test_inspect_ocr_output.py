import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import inspect_ocr_output


class TestInspectOcrOutput(unittest.TestCase):
    def test_inspect_text_output_writes_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "sample.ocr.txt"
            input_path.write_text("BANK OF CHINA 2025/04/01 100.00 200.00", encoding="utf-8")
            with patch("builtins.print"):
                exit_code = inspect_ocr_output.main([str(input_path)])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "sample.ocr.txt.diagnostic.txt").exists())
            self.assertTrue((Path(tmp) / "sample.ocr.txt.diagnostic.json").exists())


if __name__ == "__main__":
    unittest.main()

