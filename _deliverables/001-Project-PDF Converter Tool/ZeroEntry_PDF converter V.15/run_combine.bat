@echo off
setlocal
cd /d "%~dp0"

if not exist "BB2" (
    echo BB2 folder not found.
    pause
    exit /b 1
)

if not exist "BB3" mkdir "BB3"

python -m pip show openpyxl >nul 2>nul
if errorlevel 1 (
    echo Installing required package openpyxl...
    python -m pip install -r requirements.txt
)

python combine_bank_excels.py BB2 -o BB3
echo.
echo Combine completed. Check BB3 for the combined workbook and report.
pause
