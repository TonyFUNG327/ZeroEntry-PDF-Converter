param(
    [string]$ClosingDate = "",
    [string]$OpeningDate = "",
    [string]$OpeningFile = "",
    [string]$BankFile = "",
    [string]$CashFile = "",
    [string]$ManualFile = "",
    [string]$SampleReport = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Engine = Join-Path $Root "_accounting_engine"
$BB = Join-Path $Root "BB"
$Payloads = Join-Path $Root "payloads"
$ReviewOutputs = Join-Path $Root "review_outputs"
$FinalOutputs = Join-Path $Root "final_outputs"
$Logs = Join-Path $Root "logs"

foreach ($Folder in @($BB, $Payloads, $ReviewOutputs, $FinalOutputs, $Logs)) {
    New-Item -ItemType Directory -Force $Folder | Out-Null
}

$Python = "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$Node = "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$NodeModules = "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"
if (-not (Test-Path $Python)) { $Python = "python" }
if (-not (Test-Path $Node)) { $Node = "node" }
if (Test-Path $NodeModules) { $env:NODE_PATH = $NodeModules }

$LogFile = Join-Path $Logs ("run_executive_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Write-Log {
    param([string]$Message)
    $Line = "[" + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + "] " + $Message
    Write-Host $Line
    Add-Content -Path $LogFile -Value $Line
}

function Invoke-Step {
    param(
        [string]$Name,
        [string]$Command,
        [string[]]$Arguments
    )
    Write-Log "START: $Name"
    Write-Log ("COMMAND: " + $Command + " " + ($Arguments -join " "))
    & $Command @Arguments 2>&1 | Tee-Object -FilePath $LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
    Write-Log "DONE: $Name"
}

function Get-FirstMatch {
    param([string[]]$Patterns)
    $Files = Get-ChildItem -Path $BB -File -Include *.xlsx,*.xlsm,*.xls -Recurse |
        Where-Object { $_.Name -notlike "~$*" } |
        Sort-Object LastWriteTime -Descending
    foreach ($Pattern in $Patterns) {
        $Match = $Files | Where-Object { $_.Name -match $Pattern } | Select-Object -First 1
        if ($Match) { return $Match.FullName }
    }
    return ""
}

function Get-DateFromName {
    param([string]$Path)
    if (-not $Path) { return $null }
    $Name = [IO.Path]::GetFileNameWithoutExtension($Path)
    $Match = [regex]::Match($Name, "(\d{1,2})[.\-](\d{1,2})[.\-](\d{2,4})")
    if (-not $Match.Success) { return $null }
    $Day = [int]$Match.Groups[1].Value
    $Month = [int]$Match.Groups[2].Value
    $Year = [int]$Match.Groups[3].Value
    if ($Year -lt 100) { $Year += 2000 }
    return Get-Date -Year $Year -Month $Month -Day $Day
}

function Ensure-Xlsx {
    param([string]$Path)
    if (-not $Path) { return "" }
    $Ext = [IO.Path]::GetExtension($Path).ToLowerInvariant()
    if ($Ext -in @(".xlsx", ".xlsm")) { return $Path }
    if ($Ext -ne ".xls") { return $Path }

    $Converted = Join-Path $Payloads ([IO.Path]::GetFileNameWithoutExtension($Path) + ".converted.xlsx")
    Write-Log "Converting XLS to XLSX: $Path"
    $Excel = $null
    $Workbook = $null
    try {
        $Excel = New-Object -ComObject Excel.Application
        $Excel.Visible = $false
        $Excel.DisplayAlerts = $false
        $Workbook = $Excel.Workbooks.Open($Path)
        $Workbook.SaveAs($Converted, 51)
    }
    finally {
        if ($Workbook) { $Workbook.Close($false) | Out-Null }
        if ($Excel) {
            $Excel.Quit() | Out-Null
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Excel) | Out-Null
        }
    }
    return $Converted
}

Write-Log "Accounting AI Engine System V.2 run started"
Write-Log "Input folder: $BB"

if (-not $OpeningFile) { $OpeningFile = Get-FirstMatch @("opening", "trial", "\btb\b") }
if (-not $BankFile) { $BankFile = Get-FirstMatch @("bank") }
if (-not $CashFile) { $CashFile = Get-FirstMatch @("cash") }
if (-not $ManualFile) { $ManualFile = Get-FirstMatch @("manual", "journal", "accrual", "ar.*ap") }
if (-not $SampleReport) { $SampleReport = Get-FirstMatch @("sample", "tb.*gl", "tb.*bs", "tb.*pl", "tb.*is") }

if ($OpeningFile) { $OpeningFile = Ensure-Xlsx $OpeningFile }
if ($BankFile) { $BankFile = Ensure-Xlsx $BankFile }
if ($CashFile) { $CashFile = Ensure-Xlsx $CashFile }
if ($ManualFile) { $ManualFile = Ensure-Xlsx $ManualFile }
if ($SampleReport) { $SampleReport = Ensure-Xlsx $SampleReport }

if ($OpeningFile -and (-not $ClosingDate -or -not $OpeningDate)) {
    $DetectedClosing = Get-DateFromName $OpeningFile
    if ($DetectedClosing) {
        if (-not $ClosingDate) { $ClosingDate = $DetectedClosing.ToString("yyyy-MM-dd") }
        if (-not $OpeningDate) { $OpeningDate = $DetectedClosing.AddDays(1).ToString("yyyy-MM-dd") }
    }
}
if (-not $ClosingDate) { $ClosingDate = "2024-12-31" }
if (-not $OpeningDate) { $OpeningDate = "2025-01-01" }

Write-Log "Opening file: $OpeningFile"
Write-Log "Bank file: $BankFile"
Write-Log "Cash file: $CashFile"
Write-Log "Manual file: $ManualFile"
Write-Log "Sample report: $SampleReport"
Write-Log "Closing date: $ClosingDate"
Write-Log "Opening date: $OpeningDate"

$OpeningPayload = Join-Path $Payloads "opening_payload.json"
$BankPayload = Join-Path $Payloads "bank_payload.json"
$CashPayload = Join-Path $Payloads "cash_payload.json"
$ManualPayload = Join-Path $Payloads "manual_payload.json"
$FullPayload = Join-Path $Payloads "full_period_payload.json"

if ($OpeningFile) {
    Invoke-Step "Opening balance parser" $Python @(
        (Join-Path $Engine "opening_balance_parser.py"),
        $OpeningFile,
        "--closing-date", $ClosingDate,
        "--opening-date", $OpeningDate,
        "--out-json", $OpeningPayload
    )
    Invoke-Step "Opening balance review workbook" $Node @(
        (Join-Path $Engine "build_opening_balance_output.mjs"),
        "--input-json", $OpeningPayload,
        "--output-xlsx", (Join-Path $ReviewOutputs "opening_balance_review.xlsx")
    )
}

if ($BankFile) {
    Invoke-Step "Bank record parser" $Python @(
        (Join-Path $Engine "bank_record_parser.py"),
        $BankFile,
        "--out-json", $BankPayload
    )
    Invoke-Step "Bank Journal Lines workbook" $Node @(
        (Join-Path $Engine "build_bank_record_output.mjs"),
        "--input-json", $BankPayload,
        "--output-xlsx", (Join-Path $ReviewOutputs "bank_journal_lines.xlsx")
    )
}

if ($CashFile) {
    Invoke-Step "Cash record parser" $Python @(
        (Join-Path $Engine "cash_record_parser.py"),
        $CashFile,
        "--out-json", $CashPayload
    )
    Invoke-Step "Cash Journal Lines workbook" $Node @(
        (Join-Path $Engine "build_cash_record_output.mjs"),
        "--input-json", $CashPayload,
        "--output-xlsx", (Join-Path $ReviewOutputs "cash_journal_lines.xlsx")
    )
}

if ($ManualFile) {
    Invoke-Step "Manual Journals parser" $Python @(
        (Join-Path $Engine "manual_journals_parser.py"),
        "--manual-journals", $ManualFile,
        "--out-json", $ManualPayload
    )
    Invoke-Step "Manual Journals review workbook" $Node @(
        (Join-Path $Engine "build_manual_journals_output.mjs"),
        "--input-json", $ManualPayload,
        "--output-xlsx", (Join-Path $ReviewOutputs "manual_journals_review.xlsx")
    )
}

if (-not (Test-Path $OpeningPayload)) {
    throw "Opening payload is missing. Put an Opening TB workbook in BB or pass -OpeningFile."
}

$CombinerArgs = @(
    (Join-Path $Engine "full_period_combiner.py"),
    "--opening-json", $OpeningPayload,
    "--out-json", $FullPayload
)
if (Test-Path $BankPayload) { $CombinerArgs += @("--bank-json", $BankPayload) }
if (Test-Path $CashPayload) { $CombinerArgs += @("--cash-json", $CashPayload) }
if (Test-Path $ManualPayload) { $CombinerArgs += @("--manual-json", $ManualPayload) }
if ($SampleReport -and (Test-Path $SampleReport)) { $CombinerArgs += @("--sample-report", $SampleReport) }

if (-not ((Test-Path $BankPayload) -or (Test-Path $CashPayload) -or (Test-Path $ManualPayload))) {
    throw "No Bank, Cash, or Manual Journals payload was generated. Put at least one current-period source file in BB."
}

Invoke-Step "Full-period combiner" $Python $CombinerArgs
Invoke-Step "Final TB GL BS IS workbook" $Node @(
    (Join-Path $Engine "build_full_period_output.mjs"),
    "--input-json", $FullPayload,
    "--output-xlsx", (Join-Path $FinalOutputs "full_period_tb_gl_bs_is.xlsx")
)

Write-Log "Accounting AI Engine System V.2 run completed"
Write-Log "Review outputs: $ReviewOutputs"
Write-Log "Final outputs: $FinalOutputs"
