import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_errors import OcrDependencyError, OcrError, OcrExecutionError, OcrQualityError


class TestOcrErrors(unittest.TestCase):
    def test_ocr_errors_share_base_class(self):
        self.assertTrue(issubclass(OcrDependencyError, OcrError))
        self.assertTrue(issubclass(OcrExecutionError, OcrError))
        self.assertTrue(issubclass(OcrQualityError, OcrError))


if __name__ == "__main__":
    unittest.main()

