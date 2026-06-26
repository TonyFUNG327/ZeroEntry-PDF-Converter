import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_detector import is_image_only_pdf, ocrmypdf_available


class TestOcrDetector(unittest.TestCase):
    @patch("ocr.ocr_detector.shutil.which")
    def test_ocrmypdf_available(self, mock_which):
        mock_which.return_value = "C:/Tools/ocrmypdf.exe"
        self.assertTrue(ocrmypdf_available())
        mock_which.return_value = None
        self.assertFalse(ocrmypdf_available())

    @patch("ocr.ocr_detector.pdfplumber.open")
    def test_is_image_only_pdf(self, mock_open):
        page = MagicMock()
        page.extract_text.return_value = ""
        page.images = [{"x0": 1}]
        pdf = MagicMock()
        pdf.pages = [page]
        mock_open.return_value.__enter__.return_value = pdf

        self.assertTrue(is_image_only_pdf("scan.pdf"))

    @patch("ocr.ocr_detector.pdfplumber.open")
    def test_text_layer_pdf_is_not_image_only(self, mock_open):
        page = MagicMock()
        page.extract_text.return_value = "HSBC Business Direct"
        page.images = [{"x0": 1}]
        pdf = MagicMock()
        pdf.pages = [page]
        mock_open.return_value.__enter__.return_value = pdf

        self.assertFalse(is_image_only_pdf("text.pdf"))


if __name__ == "__main__":
    unittest.main()

