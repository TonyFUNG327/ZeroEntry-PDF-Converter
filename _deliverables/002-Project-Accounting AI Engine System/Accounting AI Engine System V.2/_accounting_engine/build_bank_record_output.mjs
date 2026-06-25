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
  throw new Error("Usage: node build_bank_record_output.mjs --input-json payload.json --output-xlsx output.xlsx");
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
  range.format.numberFormat = "#,##0.00";
}

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:I1").merge();
summary.getRange("A1").values = [["I026 Bank Record Import Summary"]];
summary.getRange("A1").format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 14 },
};

const s = payload.summary;
const summaryRows = [
  ["Source File", payload.source_file],
  ["Bank Sheets Imported", s.sheet_count],
  ["Transactions", s.transaction_count],
  ["Journal Lines", s.journal_line_count],
  ["References", s.reference_count],
  ["Debit Total", s.debit_total],
  ["Credit Total", s.credit_total],
  ["Net Check", s.net_check],
  ["Warnings", s.warning_count],
  ["Skipped Sheets", (payload.skipped_sheets || []).length],
];
summary.getRange(`A3:B${summaryRows.length + 2}`).values = summaryRows;
summary.getRange(`A3:A${summaryRows.length + 2}`).format = {
  fill: "#D9EAF7",
  font: { bold: true },
};
money(summary.getRange("B8:B10"));

summary.getRange("D3:I3").values = [[
  "Sheet",
  "Bank Account ID",
  "Transactions",
  "Journal Lines",
  "Bank Total",
  "Net Check",
]];
header(summary.getRange("D3:I3"));
if ((payload.sheet_summaries || []).length) {
  const sheetRows = payload.sheet_summaries.map((row) => [
    asText(row.source_sheet),
    asText(row.bank_account_id),
    Number(row.transaction_count || 0),
    Number(row.journal_line_count || 0),
    Number(row.bank_amount_total || 0),
    Number(row.net_check || 0),
  ]);
  summary.getRangeByIndexes(3, 3, sheetRows.length, 6).values = sheetRows;
  money(summary.getRangeByIndexes(3, 7, sheetRows.length, 2));
}

const warningStart = 8 + Math.max((payload.sheet_summaries || []).length, 1);
if ((payload.warnings || []).length || (payload.skipped_sheets || []).length) {
  summary.getRangeByIndexes(warningStart, 3, 1, 6).merge();
  summary.getRangeByIndexes(warningStart, 3, 1, 6).values = [["Warnings / Skipped"]];
  header(summary.getRangeByIndexes(warningStart, 3, 1, 6), "#C65911");
  const notes = [
    ...(payload.warnings || []),
    ...(payload.skipped_sheets || []).map((item) => `${item.source_sheet}: ${item.reason}`),
  ].map((item) => [item]);
  summary.getRangeByIndexes(warningStart + 1, 3, notes.length, 1).values = notes;
  summary.getRangeByIndexes(warningStart + 1, 3, notes.length, 6).merge(true);
  summary.getRangeByIndexes(warningStart + 1, 3, notes.length, 6).format = {
    fill: "#FCE4D6",
    font: { color: "#7F3F00" },
    wrapText: true,
  };
}

const journal = workbook.worksheets.add("Bank Journal Lines");
journal.showGridLines = false;
const journalHeaders = [
  "Source Sheet",
  "Date",
  "Reference",
  "Account ID",
  "Account Description",
  "Description",
  "Debit",
  "Credit",
  "Source Row",
];
const journalRows = (payload.journal_lines || []).map((line) => [
  asText(line.source_sheet),
  asDate(line.date),
  asText(line.reference),
  asText(line.account_id),
  asText(line.account_description),
  asText(line.description),
  Number(line.debit || 0),
  Number(line.credit || 0),
  Number(line.source_row || 0),
]);
journal.getRangeByIndexes(0, 0, journalRows.length + 1, journalHeaders.length).values = [
  journalHeaders,
  ...journalRows,
];
header(journal.getRangeByIndexes(0, 0, 1, journalHeaders.length));
journal.freezePanes.freezeRows(1);
if (journalRows.length) {
  journal.getRangeByIndexes(1, 1, journalRows.length, 1).format.numberFormat = "dd/mm/yyyy";
  money(journal.getRangeByIndexes(1, 6, journalRows.length, 2));
}

const account = workbook.worksheets.add("Account Summary");
account.showGridLines = false;
const accountHeaders = [
  "Account ID",
  "Account Description",
  "Debit",
  "Credit",
  "Signed Amount",
];
const accountRows = (s.account_totals || []).map((row) => [
  asText(row.account_id),
  asText(row.account_description),
  Number(row.debit || 0),
  Number(row.credit || 0),
  Number(row.signed_amount || 0),
]);
account.getRangeByIndexes(0, 0, accountRows.length + 1, accountHeaders.length).values = [
  accountHeaders,
  ...accountRows,
];
header(account.getRangeByIndexes(0, 0, 1, accountHeaders.length));
account.freezePanes.freezeRows(1);
if (accountRows.length) {
  money(account.getRangeByIndexes(1, 2, accountRows.length, 3));
}

for (const sheet of [summary, journal, account]) {
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
}

await fs.mkdir(path.dirname(outputXlsx), { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputXlsx);

if (previewPng) {
  const preview = await workbook.render({
    sheetName: "Bank Journal Lines",
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.mkdir(path.dirname(previewPng), { recursive: true });
  await fs.writeFile(previewPng, new Uint8Array(await preview.arrayBuffer()));
}
