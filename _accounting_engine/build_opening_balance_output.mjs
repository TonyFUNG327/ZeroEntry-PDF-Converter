import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const args = process.argv.slice(2);

function argValue(name) {
  const index = args.indexOf(name);
  if (index === -1 || index + 1 >= args.length) return null;
  return args[index + 1];
}

const inputJson = argValue("--input-json");
const outputXlsx = argValue("--output-xlsx");
const previewPng = argValue("--preview-png");

if (!inputJson || !outputXlsx) {
  throw new Error("Usage: node build_opening_balance_output.mjs --input-json payload.json --output-xlsx output.xlsx");
}

const payload = JSON.parse(await fs.readFile(inputJson, "utf8"));
const workbook = Workbook.create();

function asText(value) {
  if (value === null || value === undefined) return "";
  return String(value);
}

function asDate(value) {
  return value ? new Date(value) : "";
}

function header(range, fill = "#1F4E79") {
  range.format = {
    fill,
    font: { bold: true, color: "#FFFFFF" },
    borders: { preset: "bottom", style: "thin", color: "#BFBFBF" },
  };
}

function money(range) {
  range.format.numberFormat = "#,##0.00;[Red]-#,##0.00;0.00";
}

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["I026 Opening Balance Conversion"]];
summary.getRange("A1").format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 14 },
};

const s = payload.summary;
const summaryRows = [
  ["Source Sheet", s.source_sheet],
  ["Requested Closing Date", asDate(s.requested_closing_date)],
  ["Opening Date", asDate(s.opening_date)],
  ["TB Rows", s.tb_row_count],
  ["Balance Sheet Rows Carried", s.balance_sheet_row_count],
  ["P&L Rows Closed", s.profit_and_loss_row_count],
  ["Closing Debit Total", s.closing_debit_total],
  ["Closing Credit Total", s.closing_credit_total],
  ["Closing Net Check", s.closing_net_check],
  ["P&L Closed to Retained Earnings", s.pl_signed_amount_closed_to_retained_earnings],
  ["Opening Debit Total", s.opening_debit_total],
  ["Opening Credit Total", s.opening_credit_total],
  ["Opening Net Check", s.opening_net_check],
  ["Warnings", (payload.warnings || []).length],
];
summary.getRange(`A3:B${summaryRows.length + 2}`).values = summaryRows;
summary.getRange(`A3:A${summaryRows.length + 2}`).format = {
  fill: "#D9EAF7",
  font: { bold: true },
};
summary.getRange("B4:B5").format.numberFormat = "dd/mm/yyyy";
money(summary.getRange("B9:B15"));
if ((payload.warnings || []).length) {
  const warningRows = payload.warnings.map((warning) => [warning]);
  summary.getRange("D3:H3").merge();
  summary.getRange("D3").values = [["Warnings"]];
  header(summary.getRange("D3:H3"), "#C65911");
  summary.getRangeByIndexes(3, 3, warningRows.length, 1).values = warningRows;
  summary.getRangeByIndexes(3, 3, warningRows.length, 5).merge(true);
  summary.getRangeByIndexes(3, 3, warningRows.length, 5).format = {
    fill: "#FCE4D6",
    font: { color: "#7F3F00" },
    wrapText: true,
  };
}

const opening = workbook.worksheets.add("Opening Balances");
opening.showGridLines = false;
const openingHeaders = [
  "Opening Date",
  "Account ID",
  "Account Description",
  "Opening Signed Amount",
  "Opening Debit",
  "Opening Credit",
];
const openingRows = payload.opening_balance_rows.map((row) => [
  asDate(row.opening_date),
  asText(row.account_id),
  asText(row.account_description),
  Number(row.opening_signed_amount || 0),
  Number(row.opening_debit || 0),
  Number(row.opening_credit || 0),
]);
opening.getRangeByIndexes(0, 0, openingRows.length + 1, openingHeaders.length).values = [
  openingHeaders,
  ...openingRows,
];
header(opening.getRangeByIndexes(0, 0, 1, openingHeaders.length));
opening.freezePanes.freezeRows(1);
opening.getRangeByIndexes(1, 0, openingRows.length, 1).format.numberFormat = "dd/mm/yyyy";
money(opening.getRangeByIndexes(1, 3, openingRows.length, 3));

for (const sheet of [summary, opening]) {
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
}

await fs.mkdir(path.dirname(outputXlsx), { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputXlsx);

if (previewPng) {
  const preview = await workbook.render({
    sheetName: "Opening Balances",
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.mkdir(path.dirname(previewPng), { recursive: true });
  await fs.writeFile(previewPng, new Uint8Array(await preview.arrayBuffer()));
}
