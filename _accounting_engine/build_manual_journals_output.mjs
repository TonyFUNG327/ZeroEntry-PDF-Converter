import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const args = process.argv.slice(2);

function argValue(name, fallback = null) {
  const index = args.indexOf(name);
  if (index === -1 || index + 1 >= args.length) return fallback;
  return args[index + 1];
}

const inputJson = argValue("--input-json");
const outputXlsx = argValue("--output-xlsx");
const previewPng = argValue("--preview-png");

if (!inputJson || !outputXlsx) {
  throw new Error("Usage: node build_manual_journals_output.mjs --input-json payload.json --output-xlsx output.xlsx [--preview-png preview.png]");
}

const payload = JSON.parse(await fs.readFile(inputJson, "utf8"));

function asText(value) {
  if (value === null || value === undefined) return "";
  return String(value);
}

function toRows(lines) {
  const headers = [
    "Source",
    "Date",
    "Reference",
    "Line Type",
    "Account Code",
    "Account Name",
    "Description",
    "Debit",
    "Credit",
  ];
  const rows = lines.map((line) => [
    asText(line.source),
    line.date ? new Date(line.date) : "",
    asText(line.reference),
    asText(line.line_type),
    asText(line.account_code),
    asText(line.account_name),
    asText(line.description),
    Number(line.debit || 0),
    Number(line.credit || 0),
  ]);
  return [headers, ...rows];
}

function styleHeader(range) {
  range.format = {
    fill: "#1F4E79",
    font: { bold: true, color: "#FFFFFF" },
    borders: { preset: "bottom", style: "thin", color: "#D9E2F3" },
  };
}

const workbook = Workbook.create();

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["Manual Journals Import Summary"]];
summary.getRange("A1").format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 14 },
};

const metadata = payload.metadata || {};
const summaryRows = [
  ["Manual Journals Provided", payload.manual_journals_provided ? "Yes" : "No"],
  ["Manual Entry Enabled", payload.manual_entry_enabled ? "Yes" : "No"],
  ["Client Name", asText(metadata.client_name)],
  ["Period Label", asText(metadata.period_label)],
  ["File No.", asText(metadata.file_no)],
  ["Currency", asText(metadata.currency)],
  ["Period From", asText(metadata.period_from)],
  ["Period To", asText(metadata.period_to)],
  ["Journal References", payload.summary?.journal_reference_count || 0],
  ["Journal Lines", payload.summary?.journal_line_count || 0],
  ["Total Debit", Number(payload.summary?.total_debit || 0)],
  ["Total Credit", Number(payload.summary?.total_credit || 0)],
  ["Net Check", Number(payload.summary?.net || 0)],
  ["Warnings", (payload.warnings || []).length],
];
summary.getRange(`A3:B${summaryRows.length + 2}`).values = summaryRows;
summary.getRange("A3:A16").format = { font: { bold: true }, fill: "#D9EAF7" };
summary.getRange("B13:B15").format.numberFormat = "#,##0.00";
summary.getRange("A18:H18").merge();
summary.getRange("A18").values = [[asText(payload.manual_entry_note)]];
summary.getRange("A18").format = {
  fill: "#FFF2CC",
  font: { italic: true, color: "#7F6000" },
};

const sourceSummary = Object.entries(payload.summary?.by_source || {});
summary.getRange("D3:H3").values = [["Source", "Debit", "Credit", "Net", "Status"]];
styleHeader(summary.getRange("D3:H3"));
if (sourceSummary.length) {
  const rows = sourceSummary.map(([source, values]) => [
    source,
    Number(values.debit || 0),
    Number(values.credit || 0),
    Number(values.net || 0),
    Math.round(Number(values.net || 0) * 100) / 100 === 0 ? "Balanced" : "Check",
  ]);
  summary.getRangeByIndexes(3, 3, rows.length, 5).values = rows;
  summary.getRangeByIndexes(3, 4, rows.length, 3).format.numberFormat = "#,##0.00";
}

const lines = workbook.worksheets.add("Journal Lines");
lines.showGridLines = false;
const lineRows = toRows(payload.journal_lines || []);
lines.getRangeByIndexes(0, 0, lineRows.length, lineRows[0].length).values = lineRows;
styleHeader(lines.getRangeByIndexes(0, 0, 1, lineRows[0].length));
lines.freezePanes.freezeRows(1);
if (lineRows.length > 1) {
  lines.getRangeByIndexes(1, 1, lineRows.length - 1, 1).format.numberFormat = "dd/mm/yyyy";
  lines.getRangeByIndexes(1, 7, lineRows.length - 1, 2).format.numberFormat = "#,##0.00";
}

const manual = workbook.worksheets.add("Manual Entry");
manual.showGridLines = false;
manual.getRange("A1:H1").merge();
manual.getRange("A1").values = [["Manual JV Entry Area"]];
manual.getRange("A1").format = {
  fill: "#548235",
  font: { bold: true, color: "#FFFFFF", size: 13 },
};
manual.getRange("A3:H3").values = [[
  "Date",
  "Reference",
  "Line Type",
  "Account Code",
  "Account Name",
  "Description",
  "Debit",
  "Credit",
]];
styleHeader(manual.getRange("A3:H3"));
const blankRows = Array.from({ length: 50 }, () => ["", "", "", "", "", "", "", ""]);
manual.getRange("A4:H53").values = blankRows;
manual.getRange("A4:A53").format.numberFormat = "dd/mm/yyyy";
manual.getRange("G4:H53").format.numberFormat = "#,##0.00";
manual.freezePanes.freezeRows(3);
manual.getRange("A55:H55").merge();
manual.getRange("A55").values = [[
  "Manual Journals are optional. If the schedule workbook is not supplied, enter JV lines here after bank/cash import.",
]];
manual.getRange("A55").format = {
  fill: "#E2F0D9",
  font: { italic: true, color: "#375623" },
};

for (const sheet of [summary, lines, manual]) {
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
}

await fs.mkdir(path.dirname(outputXlsx), { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputXlsx);

if (previewPng) {
  const preview = await workbook.render({
    sheetName: "Summary",
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.mkdir(path.dirname(previewPng), { recursive: true });
  await fs.writeFile(previewPng, new Uint8Array(await preview.arrayBuffer()));
}
