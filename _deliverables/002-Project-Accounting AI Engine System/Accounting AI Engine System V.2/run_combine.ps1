param(
    [string]$SampleReport = "",
    [string]$OutputName = "full_period_tb_gl_bs_is.xlsx"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Engine = Join-Path $Root "_accounting_engine"
$BB = Join-Path $Root "BB"
$Payloads = Join-Path $Root "payloads"
$FinalOutputs = Join-Path $Root "final_outputs"
$Logs = Join-Path $Root "logs"

foreach ($Folder in @($BB, $Payloads, $FinalOutputs, $Logs)) {
    New-Item -ItemType Directory -Force $Folder | Out-Null
}

$Python = "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$Node = "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$NodeModules = "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"
if (-not (Test-Path $Python)) { $Python = "python" }
if (-not (Test-Path $Node)) { $Node = "node" }
if (Test-Path $NodeModules) { $env:NODE_PATH = $NodeModules }

$LogFile = Join-Path $Logs ("run_combine_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

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

Write-Log "Accounting AI Engine System V.2 combine-only run started"
Write-Log "Payload folder: $Payloads"

$OpeningPayload = Join-Path $Payloads "opening_payload.json"
$BankPayload = Join-Path $Payloads "bank_payload.json"
$CashPayload = Join-Path $Payloads "cash_payload.json"
$ManualPayload = Join-Path $Payloads "manual_payload.json"
$FullPayload = Join-Path $Payloads "full_period_payload.json"

if (-not $SampleReport) {
    $SampleReport = Get-FirstMatch @("sample", "tb.*gl", "tb.*bs", "tb.*pl", "tb.*is")
}

if (-not (Test-Path $OpeningPayload)) {
    throw "Missing payloads\opening_payload.json. Run run_executive first or generate Stage 1 opening payload."
}

if (-not ((Test-Path $BankPayload) -or (Test-Path $CashPayload) -or (Test-Path $ManualPayload))) {
    throw "Missing Stage 2 payload. Expected at least one of bank_payload.json, cash_payload.json, or manual_payload.json in payloads."
}

$CombinerArgs = @(
    (Join-Path $Engine "full_period_combiner.py"),
    "--opening-json", $OpeningPayload,
    "--out-json", $FullPayload
)
if (Test-Path $BankPayload) {
    Write-Log "Using Bank payload: $BankPayload"
    $CombinerArgs += @("--bank-json", $BankPayload)
}
if (Test-Path $CashPayload) {
    Write-Log "Using Cash payload: $CashPayload"
    $CombinerArgs += @("--cash-json", $CashPayload)
}
if (Test-Path $ManualPayload) {
    Write-Log "Using Manual Journals payload: $ManualPayload"
    $CombinerArgs += @("--manual-json", $ManualPayload)
}
if ($SampleReport -and (Test-Path $SampleReport)) {
    Write-Log "Using sample report: $SampleReport"
    $CombinerArgs += @("--sample-report", $SampleReport)
}

Invoke-Step "Full-period combiner" $Python $CombinerArgs
Invoke-Step "Final TB GL BS IS workbook" $Node @(
    (Join-Path $Engine "build_full_period_output.mjs"),
    "--input-json", $FullPayload,
    "--output-xlsx", (Join-Path $FinalOutputs $OutputName)
)

Write-Log "Combine-only run completed"
Write-Log "Final output: $(Join-Path $FinalOutputs $OutputName)"
