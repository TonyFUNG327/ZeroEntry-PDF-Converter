import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const args = process.argv.slice(2);

function argValue(name, fallback = null) {
  const index = args.indexOf(name);
  if (index === -1 || index + 1 >= args.length) return fallback;
  return args[index + 1];
}

const outputXlsx = argValue("--output-xlsx");
if (!outputXlsx) {
  throw new Error("Usage: node build_manual_journals_input_template.mjs --output-xlsx manual_journals_input.xlsx");
}

const workbook = Workbook.create();

function header(range, fill = "#1F4E79") {
  range.format = {
    fill,
    font: { bold: true, color: "#FFFFFF" },
    borders: { preset: "bottom", style: "thin", color: "#BFBFBF" },
  };
}

function note(range) {
  range.format = {
    fill: "#FFF2CC",
    font: { italic: true, color: "#7F6000" },
    wrapText: true,
  };
}

const setup = workbook.worksheets.add("Setup");
setup.showGridLines = false;
setup.getRange("A1:D1").merge();
setup.getRange("A1").values = [["Manual Journals Input Template"]];
setup.getRange("A1").format = { fill: "#17365D", font: { bold: true, color: "#FFFFFF", size: 14 } };
setup.getRange("A3:B9").values = [
  ["Client Name", ""],
  ["Period From", ""],
  ["Period To", ""],
  ["Currency", "HK$"],
  ["Prepared By", ""],
  ["Reviewed By", ""],
  ["Status", "Draft"],
];
setup.getRange("A3:A9").format = { fill: "#D9EAF7", font: { bold: true } };
setup.getRange("A11:D12").merge(true);
setup.getRange("A11").values = [["Fill the Manual Journals sheet only when adjustments are needed. Debit and Credit totals must match before Stage 3 import."]];
note(setup.getRange("A11:D12"));

const mj = workbook.worksheets.add("Manual Journals");
mj.showGridLines = false;
const headers = [
  "Date",
  "Reference",
  "Account ID",
  "Account Description",
  "Description",
  "Debit",
  "Credit",
  "Prepared By",
  "Notes",
];
mj.getRangeByIndexes(0, 0, 1, headers.length).values = [headers];
header(mj.getRangeByIndexes(0, 0, 1, headers.length));
const blankRows = Array.from({ length: 200 }, () => ["", "", "", "", "", "", "", "", ""]);
mj.getRangeByIndexes(1, 0, blankRows.length, headers.length).values = blankRows;
mj.getRange("A2:A201").format.numberFormat = "dd/mm/yyyy";
mj.getRange("F2:G201").format.numberFormat = "#,##0.00";
mj.freezePanes.freezeRows(1);

const check = workbook.worksheets.add("Check");
check.showGridLines = false;
check.getRange("A1:D1").values = [["Metric", "Value", "Status", "Comment"]];
header(check.getRange("A1:D1"));
check.getRange("A2:A5").values = [["Total Debit"], ["Total Credit"], ["Difference"], ["Ready for Import"]];
check.getRange("B2").formulas = [["=SUM('Manual Journals'!F2:F201)"]];
check.getRange("B3").formulas = [["=SUM('Manual Journals'!G2:G201)"]];
check.getRange("B4").formulas = [["=B2-B3"]];
check.getRange("B5").formulas = [["=IF(ROUND(B4,2)=0,\"Yes\",\"No\")"]];
check.getRange("C2:C5").formulas = [[""], [""], ["=IF(ROUND(B4,2)=0,\"Balanced\",\"Check\")"], ["=B5"]];
check.getRange("B2:B4").format.numberFormat = "#,##0.00";
check.getRange("A2:A5").format = { fill: "#D9EAF7", font: { bold: true } };

const coa = workbook.worksheets.add("COA Mapping");
coa.showGridLines = false;
coa.getRange("A1:E1").values = [["Account ID", "Account Description", "Source", "User Confirmed", "Notes"]];
header(coa.getRange("A1:E1"));
coa.getRange("A2:E201").values = Array.from({ length: 200 }, () => ["", "", "", "", ""]);
coa.freezePanes.freezeRows(1);

for (const sheet of [setup, mj, check, coa]) {
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
}

await fs.mkdir(path.dirname(outputXlsx), { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputXlsx);
