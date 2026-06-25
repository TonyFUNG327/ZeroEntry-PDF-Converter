from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
BB_DIR = APP_ROOT / "BB"
BB2_DIR = APP_ROOT / "BB2"
BB3_DIR = APP_ROOT / "BB3"
GENERATED_OUTPUT_DIR = APP_ROOT / "generated_output"


def ensure_output_dir(path):
    output_dir = Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def collect_pdf_paths(input_path):
    input_path = Path(input_path)
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"Input file is not a PDF: {input_path}")
        return [input_path]
    if input_path.is_dir():
        return sorted(path for path in input_path.iterdir() if path.is_file() and path.suffix.lower() == ".pdf")
    raise FileNotFoundError(f"Input path does not exist: {input_path}")

