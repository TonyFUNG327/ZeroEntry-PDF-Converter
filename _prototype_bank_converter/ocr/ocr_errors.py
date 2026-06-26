class OcrError(RuntimeError):
    """Base class for OCR pipeline failures."""


class OcrDependencyError(OcrError):
    """Raised when an external OCR dependency is unavailable."""


class OcrQualityError(OcrError):
    """Raised when OCR output is too weak to trust for conversion."""


class OcrExecutionError(OcrError):
    """Raised when the OCR command fails during execution."""

