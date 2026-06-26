import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


APP_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_ROOT.parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import convert_bank_pdf
from core.bank_registry import SCANNED_IMAGE_ONLY, ScannedPdfError
from ocr.ocr_errors import OcrDependencyError, OcrQualityError


class TestConvertBankPdfOcrFlag(unittest.TestCase):
    def test_cli_accepts_ocr_flag(self):
        args = convert_bank_pdf.build_arg_parser().parse_args(["BB", "-o", "BB2", "--ocr"])
        self.assertTrue(args.ocr)
        self.assertEqual(str(args.input), "BB")

    @patch("convert_bank_pdf.convert_with_adapter")
    def test_no_ocr_keeps_scanned_pdf_error_path(self, mock_convert):
        mock_convert.side_effect = ScannedPdfError("scan needs OCR")
        with self.assertRaises(ScannedPdfError):
            convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=False)
        mock_convert.assert_called_once()

    @patch("convert_bank_pdf.convert_with_adapter")
    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_ocr_enabled_scanned_pdf_enters_preprocessor(self, mock_detect, mock_preprocess, mock_quality, mock_convert):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(
            searchable_pdf=Path("OCR_WORK/scan.ocr.pdf"),
            text="HSBC Business Direct 2025/01/01 100.00 200.00",
        )
        mock_quality.return_value = SimpleNamespace(bank_code="HSBC")
        mock_convert.return_value = ("HSBC", Path("out/scan.xlsx"), [])

        result = convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=True)

        self.assertEqual(result[0], "HSBC")
        mock_preprocess.assert_called_once_with(Path("scan.pdf"))
        mock_quality.assert_called_once()
        mock_convert.assert_called_once_with(
            Path("OCR_WORK/scan.ocr.pdf"),
            Path("out"),
            bank_code="HSBC",
            output_stem="scan",
        )

    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_ocr_dependency_error_bubbles_up(self, mock_detect, mock_preprocess):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.side_effect = OcrDependencyError("missing OCRmyPDF")
        with self.assertRaises(OcrDependencyError):
            convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=True)

    @patch("convert_bank_pdf.validate_ocr_quality")
    @patch("convert_bank_pdf.preprocess_pdf_for_ocr")
    @patch("convert_bank_pdf.detect_bank")
    def test_ocr_quality_error_bubbles_up(self, mock_detect, mock_preprocess, mock_quality):
        mock_detect.return_value = SCANNED_IMAGE_ONLY
        mock_preprocess.return_value = SimpleNamespace(searchable_pdf=Path("OCR_WORK/scan.ocr.pdf"), text="bad")
        mock_quality.side_effect = OcrQualityError("too short")
        with self.assertRaises(OcrQualityError):
            convert_bank_pdf.convert_one(Path("scan.pdf"), Path("out"), ocr_enabled=True)

    def test_gitignore_contains_ocr_work(self):
        gitignore = REPO_ROOT / ".gitignore"
        self.assertIn("_prototype_bank_converter/OCR_WORK/", gitignore.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

