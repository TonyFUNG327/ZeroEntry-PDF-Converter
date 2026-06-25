from pathlib import Path

from openpyxl import load_workbook


bad = []
for path in Path(__file__).resolve().parent.joinpath("output").glob("*.xlsx"):
    workbook = load_workbook(path, data_only=False)
    for sheet in workbook.worksheets:
        for cell in sheet["B"][1:]:
            if cell.value and not (2024 <= cell.value.year <= 2026):
                bad.append((path.name, sheet.title, cell.coordinate, cell.value))
        for cell in sheet["E"][1:]:
            if cell.number_format != '(#,##0.00);(#,##0.00);"-"':
                bad.append((path.name, sheet.title, cell.coordinate, cell.number_format))

print("bad_count", len(bad))
for item in bad[:20]:
    print(item)
