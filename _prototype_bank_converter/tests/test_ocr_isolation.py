import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import convert_bank_pdf
from core.bank_registry import NoAccountRowsError, ParserExecutionError, SCANNED_IMAGE_ONLY, ScannedPdfError


class TestOcrIsolation(unittest.TestCase):
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.convert_with_adapter")
    def test_without_ocr_uses_adapter_and_never_preprocesses(self, mock_convert, mock_preprocess):
        mock_convert.return_value = ("BOC", Path("out/sample.xlsx"), [])

        result = convert_bank_pdf.convert_one(Path("sample.pdf"), Path("out"), ocr_enabled=False)

        self.assertEqual(result[0], "BOC")
        mock_convert.assert_called_once_with(Path("sample.pdf"), Path("out"))
        mock_preprocess.assert_not_called()

    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.detect_bank")
    def test_text_layer_pdf_with_ocr_enabled_still_uses_existing_parser(self, mock_detect, mock_convert, mock_preprocess):
        mock_detect.return_value = "HSBC"
        mock_convert.return_value = ("HSBC", Path("out/sample.xlsx"), [])

        result = convert_bank_pdf.convert_one(Path("sample.pdf"), Path("out"), ocr_enabled=True)

        self.assertEqual(result[0], "HSBC")
        mock_convert.assert_called_once_with(Path("sample.pdf"), Path("out"), bank_code="HSBC")
        mock_preprocess.assert_not_called()

    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.convert_with_adapter")
    def test_scanned_pdf_without_ocr_keeps_scanned_error_path(self, mock_convert, mock_preprocess):
        mock_convert.side_effect = ScannedPdfError("Image-only scanned PDF detected.")

        with self.assertRaises(ScannedPdfError):
            convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=False)

        mock_convert.assert_called_once_with(Path("scan.pdf"), Path("out"))
        mock_preprocess.assert_not_called()

    @patch("convert_bank_pdf.convert_with_boc_ocr_fallback")
    @patch("convert_bank_pdf.write_ocr_diagnostic")
    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_boc_fallback_runs_only_for_no_account_rows_error(
        self,
        mock_detect,
        mock_preprocess,
        mock_quality,
        mock_convert,
        mock_diagnostic,
        mock_fallback,
    ):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(searchable_pdf=Path("OCR_WORK/scan.ocr.pdf"), text="BANK OF CHINA 2025/04/01 100.00 200.00")
        mock_quality.return_value = SimpleNamespace(bank_code="BOC")
        mock_convert.side_effect = NoAccountRowsError("BOC parser returned no account rows.")
        mock_diagnostic.return_value = Path("OCR_WORK/scan.diagnostic.txt")
        mock_fallback.return_value = ("BOC_OCR_FALLBACK", Path("out/scan.xlsx"), [])

        result = convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=True)

        self.assertEqual(result[0], "BOC_OCR_FALLBACK")
        mock_fallback.assert_called_once()

    @patch("convert_bank_pdf.convert_with_boc_ocr_fallback")
    @patch("convert_bank_pdf.write_ocr_diagnostic")
    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_boc_fallback_does_not_run_for_other_parser_errors(
        self,
        mock_detect,
        mock_preprocess,
        mock_quality,
        mock_convert,
        mock_diagnostic,
        mock_fallback,
    ):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(searchable_pdf=Path("OCR_WORK/scan.ocr.pdf"), text="BANK OF CHINA 2025/04/01 100.00 200.00")
        mock_quality.return_value = SimpleNamespace(bank_code="BOC")
        mock_convert.side_effect = ParserExecutionError("BOC parser failed for scan.pdf: unexpected layout")
        mock_diagnostic.return_value = Path("OCR_WORK/scan.diagnostic.txt")

        with self.assertRaises(ParserExecutionError) as ctx:
            convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=True)

        self.assertIn("fallback was not attempted", str(ctx.exception))
        mock_fallback.assert_not_called()


if __name__ == "__main__":
    unittest.main()
