import json
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

    def test_inspect_text_output_with_boc_parser_writes_parser_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "sample.ocr.txt"
            input_path.write_text(
                "\n".join(
                    [
                        "BANK OF CHINA HKD CURRENT ACCOUNT",
                        "2025/04/01 B/F BALANCE 1,000.00",
                        "2025/04/02 RECEIPT 100.00 1,100.00",
                        "2025/04/03 BROKEN OCR 500.00 9,999.00",
                    ]
                ),
                encoding="utf-8",
            )
            with patch("builtins.print"):
                exit_code = inspect_ocr_output.main([str(input_path), "--parser", "BOC"])

            self.assertEqual(exit_code, 0)
            json_path = Path(tmp) / "sample.ocr.txt.diagnostic.json"
            report = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(report["parsed_transaction_row_count"], 2)
            self.assertEqual(report["skipped_candidate_line_count"], 1)
            self.assertTrue(report["parsed_rows"])
            self.assertEqual(report["skipped_lines"][0]["reason"], "Could not classify deposit/withdrawal")


if __name__ == "__main__":
    unittest.main()
