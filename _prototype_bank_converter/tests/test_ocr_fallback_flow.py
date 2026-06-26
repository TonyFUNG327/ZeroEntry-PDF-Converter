import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import convert_bank_pdf
from core.bank_registry import ParserExecutionError, SCANNED_IMAGE_ONLY


class TestOcrFallbackFlow(unittest.TestCase):
    @patch("convert_bank_pdf.convert_with_boc_ocr_fallback")
    @patch("convert_bank_pdf.write_ocr_diagnostic")
    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_boc_ocr_fallback_runs_when_existing_parser_has_no_rows(
        self,
        mock_detect,
        mock_preprocess,
        mock_quality,
        mock_convert,
        mock_diagnostic,
        mock_fallback,
    ):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(searchable_pdf=Path("OCR_WORK/BOC 4.25.ocr.pdf"), text="BANK OF CHINA 2025/04/01 100.00 200.00")
        mock_quality.return_value = SimpleNamespace(bank_code="BOC")
        mock_convert.side_effect = ParserExecutionError("BOC parser returned no account rows.")
        mock_diagnostic.return_value = Path("OCR_WORK/BOC 4.25.diagnostic.txt")
        mock_fallback.return_value = ("BOC_OCR_FALLBACK", Path("out/BOC 4.25.xlsx"), [])

        result = convert_bank_pdf.convert_one(Path("BOC 4.25.pdf"), Path("out"), ocr_enabled=True)

        self.assertEqual(result[0], "BOC_OCR_FALLBACK")
        mock_fallback.assert_called_once()

    @patch("convert_bank_pdf.convert_with_boc_ocr_fallback")
    @patch("convert_bank_pdf.write_ocr_diagnostic")
    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_boc_ocr_fallback_does_not_run_for_non_no_rows_parser_error(
        self,
        mock_detect,
        mock_preprocess,
        mock_quality,
        mock_convert,
        mock_diagnostic,
        mock_fallback,
    ):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(searchable_pdf=Path("OCR_WORK/BOC 4.25.ocr.pdf"), text="BANK OF CHINA 2025/04/01 100.00 200.00")
        mock_quality.return_value = SimpleNamespace(bank_code="BOC")
        mock_convert.side_effect = ParserExecutionError("BOC parser failed for BOC 4.25.pdf: unexpected layout")
        mock_diagnostic.return_value = Path("OCR_WORK/BOC 4.25.diagnostic.txt")

        with self.assertRaises(ParserExecutionError) as ctx:
            convert_bank_pdf.convert_one(Path("BOC 4.25.pdf"), Path("out"), ocr_enabled=True)

        self.assertIn("fallback was not attempted", str(ctx.exception))
        mock_fallback.assert_not_called()

    @patch("convert_bank_pdf.convert_with_boc_ocr_fallback")
    @patch("convert_bank_pdf.write_ocr_diagnostic")
    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_non_boc_ocr_failure_does_not_use_boc_fallback(
        self,
        mock_detect,
        mock_preprocess,
        mock_quality,
        mock_convert,
        mock_diagnostic,
        mock_fallback,
    ):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(searchable_pdf=Path("OCR_WORK/scan.ocr.pdf"), text="HSBC Business Direct 2025/04/01 100.00 200.00")
        mock_quality.return_value = SimpleNamespace(bank_code="HSBC")
        mock_convert.side_effect = ParserExecutionError("HSBC parser returned no account rows.")
        mock_diagnostic.return_value = Path("OCR_WORK/scan.diagnostic.txt")

        with self.assertRaises(ParserExecutionError):
            convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=True)
        mock_fallback.assert_not_called()


if __name__ == "__main__":
    unittest.main()
