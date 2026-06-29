import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import calibrate_ocr_output


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


class TestCalibrateOcrOutput(unittest.TestCase):
    def test_calibrate_redacted_boc_fixture_writes_reports(self):
        source = FIXTURE_DIR / "boc_scanned_sample_02_redacted.txt"
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / source.name
            input_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            with patch("builtins.print"):
                exit_code = calibrate_ocr_output.main([str(input_path), "--parser", "BOC"])

            self.assertEqual(exit_code, 0)
            diagnostic_json = Path(tmp) / "boc_scanned_sample_02_redacted.txt.diagnostic.json"
            summary_json = Path(tmp) / "boc_scanned_sample_02_redacted.txt.calibration_summary.json"
            self.assertTrue(diagnostic_json.exists())
            self.assertTrue(summary_json.exists())

            report = json.loads(diagnostic_json.read_text(encoding="utf-8"))
            summary = json.loads(summary_json.read_text(encoding="utf-8"))
            self.assertTrue(report["parsed_rows"])
            self.assertTrue(report["skipped_lines"])
            self.assertIn("Could not classify deposit/withdrawal", summary["skip_reason_counts"])
            self.assertGreater(summary["parse_success_ratio"], 0)

    def test_calibrate_output_dir_writes_reports_to_selected_folder(self):
        source = FIXTURE_DIR / "boc_scanned_sample_01_redacted.txt"
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / source.name
            output_dir = Path(tmp) / "calibration" / "reports"
            input_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            with patch("builtins.print"):
                exit_code = calibrate_ocr_output.main([str(input_path), "--parser", "BOC", "--output-dir", str(output_dir)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "boc_scanned_sample_01_redacted.txt.diagnostic.txt").exists())
            self.assertTrue((output_dir / "boc_scanned_sample_01_redacted.txt.diagnostic.json").exists())
            self.assertTrue((output_dir / "boc_scanned_sample_01_redacted.txt.calibration_summary.json").exists())
            self.assertFalse((Path(tmp) / "boc_scanned_sample_01_redacted.txt.diagnostic.txt").exists())


if __name__ == "__main__":
    unittest.main()
