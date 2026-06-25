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
  throw new Error("Usage: node build_full_period_output.mjs --input-json payload.json --output-xlsx output.xlsx");
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

function section(range, fill = "#D9EAF7") {
  range.format = {
    fill,
    font: { bold: true },
  };
}

function money(range) {
  range.format.numberFormat = "#,##0.00";
}

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["I026 Full Period Accounting Run"]];
summary.getRange("A1").format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 14 },
};

const s = payload.summary;
const summaryRows = [
  ["Source", s.source],
  ["Journal Lines", s.journal_line_count],
  ["TB Debit Total", s.tb_debit_total],
  ["TB Credit Total", s.tb_credit_total],
  ["TB Net Check", s.tb_net_check],
  ["Revenue Total", s.revenue_total],
  ["Expense Total", s.expense_total],
  ["Net Income / (Loss)", s.net_income],
  ["Difference Matched to Sample JV", s.differences_match_sample_manual_jv ? "Yes" : "No"],
  ["Non-JV Difference Accounts", (s.non_jv_difference_accounts || []).join(", ")],
  ["Sample JV References", (s.sample_manual_jv_references || []).join(", ")],
];
summary.getRange(`A3:B${summaryRows.length + 2}`).values = summaryRows;
section(summary.getRange(`A3:A${summaryRows.length + 2}`));
money(summary.getRange("B5:B10"));

const gl = workbook.worksheets.add("GL");
gl.showGridLines = false;
const glHeaders = [
  "Account ID",
  "Account Description",
  "Date",
  "Reference",
  "Jrnl",
  "Trans Description",
  "Debit Amt",
  "Credit Amt",
  "Balance",
  "Source",
];

function accountSortKey(accountId) {
  const parsed = Number.parseInt(accountId, 10);
  return Number.isFinite(parsed) ? parsed : 999999;
}

function dateSortValue(value) {
  const d = value ? new Date(value) : null;
  return d && !Number.isNaN(d.valueOf()) ? d.valueOf() : 0;
}

const byAccount = new Map();
for (const row of payload.gl_rows) {
  const accountId = asText(row.account_id);
  if (!byAccount.has(accountId)) byAccount.set(accountId, []);
  byAccount.get(accountId).push(row);
}

const glRows = [];
for (const accountId of [...byAccount.keys()].sort((a, b) => accountSortKey(a) - accountSortKey(b) || a.localeCompare(b))) {
  const rows = byAccount.get(accountId);
  const accountName = asText(rows[0]?.account_description);
  const openingRows = rows.filter((row) => row.source === "Opening");
  const movementRows = rows
    .filter((row) => row.source !== "Opening")
    .sort((a, b) => dateSortValue(a.date) - dateSortValue(b.date) || asText(a.reference).localeCompare(asText(b.reference)));
  let runningBalance = openingRows.reduce((sum, row) => sum + Number(row.signed_amount || 0), 0);

  glRows.push([
    accountId,
    accountName,
    openingRows[0] ? asDate(openingRows[0].date) : "",
    "Opening balance",
    "GENJ",
    `Opening balance - ${accountName}`,
    0,
    0,
    Number(runningBalance.toFixed(2)),
    "Opening",
  ]);

  for (const row of movementRows) {
    runningBalance += Number(row.signed_amount || 0);
    glRows.push([
      accountId,
      accountName,
      asDate(row.date),
      asText(row.reference),
      asText(row.jrnl),
      asText(row.description),
      Number(row.debit || 0),
      Number(row.credit || 0),
      Number(runningBalance.toFixed(2)),
      asText(row.source),
    ]);
  }

  glRows.push([
    accountId,
    accountName,
    "",
    "",
    "",
    "Closing Balance",
    0,
    0,
    Number(runningBalance.toFixed(2)),
    "",
  ]);
  glRows.push(["", "", "", "", "", "", "", "", "", ""]);
}
gl.getRangeByIndexes(0, 0, glRows.length + 1, glHeaders.length).values = [glHeaders, ...glRows];
header(gl.getRangeByIndexes(0, 0, 1, glHeaders.length));
gl.freezePanes.freezeRows(1);
if (glRows.length) {
  gl.getRangeByIndexes(1, 2, glRows.length, 1).format.numberFormat = "dd/mm/yyyy";
  money(gl.getRangeByIndexes(1, 6, glRows.length, 3));
}

const tb = workbook.worksheets.add("TB");
tb.showGridLines = false;
const tbHeaders = ["Account ID", "Account Description", "Debit Amt", "Credit Amt"];
const tbRows = payload.tb_rows.map((row) => [
  asText(row.account_id),
  asText(row.account_description),
  Number(row.debit || 0),
  Number(row.credit || 0),
]);
tb.getRangeByIndexes(0, 0, tbRows.length + 1, tbHeaders.length).values = [tbHeaders, ...tbRows];
header(tb.getRangeByIndexes(0, 0, 1, tbHeaders.length));
money(tb.getRangeByIndexes(1, 2, tbRows.length, 2));
const tbTotalRow = tbRows.length + 2;
tb.getRangeByIndexes(tbTotalRow - 1, 1, 1, 3).values = [[
  "Total:",
  Number(s.tb_debit_total || 0),
  Number(s.tb_credit_total || 0),
]];
section(tb.getRangeByIndexes(tbTotalRow - 1, 1, 1, 1));
money(tb.getRangeByIndexes(tbTotalRow - 1, 2, 1, 2));

const isSheet = workbook.worksheets.add("IS");
isSheet.showGridLines = false;
isSheet.getRange("A1:D1").merge();
isSheet.getRange("A1").values = [["Income Statement"]];
isSheet.getRange("A1").format = { fill: "#17365D", font: { bold: true, color: "#FFFFFF", size: 13 } };
let rowCursor = 3;
isSheet.getRange(`A${rowCursor}:D${rowCursor}`).values = [["Revenues", "", "", ""]];
section(isSheet.getRange(`A${rowCursor}:D${rowCursor}`));
rowCursor += 1;
for (const row of payload.is_rows.revenue) {
  isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 4).values = [[
    row.account_description,
    Math.abs(Number(row.signed_amount || 0)),
    "",
    "",
  ]];
  rowCursor += 1;
}
isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 2).values = [["Total Revenues", Number(payload.is_rows.revenue_total || 0)]];
section(isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 1));
money(isSheet.getRangeByIndexes(3, 1, Math.max(rowCursor - 3, 1), 1));
rowCursor += 2;
isSheet.getRange(`A${rowCursor}:D${rowCursor}`).values = [["Expenses", "", "", ""]];
section(isSheet.getRange(`A${rowCursor}:D${rowCursor}`));
rowCursor += 1;
for (const row of payload.is_rows.expense) {
  isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 2).values = [[
    row.account_description,
    Number(row.signed_amount || 0),
  ]];
  rowCursor += 1;
}
isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 2).values = [["Total Expenses", Number(payload.is_rows.expense_total || 0)]];
section(isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 1));
rowCursor += 2;
isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 2).values = [["Net Income / (Loss)", Number(payload.is_rows.net_income || 0)]];
section(isSheet.getRangeByIndexes(rowCursor - 1, 0, 1, 1), "#FFF2CC");
money(isSheet.getRange(`B3:B${rowCursor}`));

const bs = workbook.worksheets.add("BS");
bs.showGridLines = false;
bs.getRange("A1:C1").merge();
bs.getRange("A1").values = [["Balance Sheet"]];
bs.getRange("A1").format = { fill: "#17365D", font: { bold: true, color: "#FFFFFF", size: 13 } };
let bsRow = 3;
bs.getRange(`A${bsRow}:C${bsRow}`).values = [["ASSETS", "", ""]];
section(bs.getRange(`A${bsRow}:C${bsRow}`));
bsRow += 1;
for (const row of payload.bs_rows.assets) {
  bs.getRangeByIndexes(bsRow - 1, 0, 1, 2).values = [[row.account_description, Number(row.signed_amount || 0)]];
  bsRow += 1;
}
bs.getRangeByIndexes(bsRow - 1, 0, 1, 2).values = [["Total Assets", Number(payload.bs_rows.asset_total || 0)]];
section(bs.getRangeByIndexes(bsRow - 1, 0, 1, 1));
bsRow += 2;
bs.getRange(`A${bsRow}:C${bsRow}`).values = [["LIABILITIES AND EQUITY", "", ""]];
section(bs.getRange(`A${bsRow}:C${bsRow}`));
bsRow += 1;
for (const row of payload.bs_rows.liabilities_equity) {
  bs.getRangeByIndexes(bsRow - 1, 0, 1, 2).values = [[row.account_description, Math.abs(Number(row.signed_amount || 0))]];
  bsRow += 1;
}
bs.getRangeByIndexes(bsRow - 1, 0, 1, 2).values = [["Current Year Income / (Loss)", Number(payload.is_rows.net_income || 0)]];
bsRow += 1;
const liabEquityAfterIncome = Number(payload.bs_rows.liability_equity_total || 0) + Number(payload.is_rows.net_income || 0);
bs.getRangeByIndexes(bsRow - 1, 0, 1, 2).values = [["Total Liabilities and Equity", liabEquityAfterIncome]];
section(bs.getRangeByIndexes(bsRow - 1, 0, 1, 1));
bsRow += 1;
bs.getRangeByIndexes(bsRow - 1, 0, 1, 2).values = [["Check", Number(payload.bs_rows.asset_total || 0) - liabEquityAfterIncome]];
section(bs.getRangeByIndexes(bsRow - 1, 0, 1, 1), "#FFF2CC");
money(bs.getRange(`B3:B${bsRow}`));

const comp = workbook.worksheets.add("TB Comparison vs Sample");
comp.showGridLines = false;
const compHeaders = [
  "Account ID",
  "Account Description",
  "Generated Signed",
  "Sample Signed",
  "Sample - Generated",
  "Sample JV Signed",
  "Unexplained",
  "Matched to JV",
  "JV References",
];
const compRows = payload.tb_comparison
  .filter((row) => Math.abs(Number(row.difference_sample_less_generated || 0)) > 0.01 || Math.abs(Number(row.unexplained_difference || 0)) > 0.01)
  .map((row) => [
    asText(row.account_id),
    asText(row.account_description),
    Number(row.generated_signed_amount || 0),
    Number(row.sample_signed_amount || 0),
    Number(row.difference_sample_less_generated || 0),
    Number(row.sample_manual_jv_signed_amount || 0),
    Number(row.unexplained_difference || 0),
    row.matched_to_manual_jv ? "Yes" : "No",
    asText(row.manual_jv_references),
  ]);
comp.getRangeByIndexes(0, 0, compRows.length + 1, compHeaders.length).values = [compHeaders, ...compRows];
header(comp.getRangeByIndexes(0, 0, 1, compHeaders.length));
comp.freezePanes.freezeRows(1);
if (compRows.length) {
  money(comp.getRangeByIndexes(1, 2, compRows.length, 5));
}

for (const sheet of [summary, gl, tb, isSheet, bs, comp]) {
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
}

await fs.mkdir(path.dirname(outputXlsx), { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputXlsx);

if (previewPng) {
  const preview = await workbook.render({ sheetName: "Summary", autoCrop: "all", scale: 1, format: "png" });
  await fs.mkdir(path.dirname(previewPng), { recursive: true });
  await fs.writeFile(previewPng, new Uint8Array(await preview.arrayBuffer()));
}
