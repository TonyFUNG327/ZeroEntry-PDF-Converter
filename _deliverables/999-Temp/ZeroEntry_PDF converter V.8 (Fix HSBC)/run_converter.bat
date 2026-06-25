@echo off
setlocal
cd /d "%~dp0"

if not exist "BB" mkdir "BB"
if not exist "BB2" mkdir "BB2"

python --version >nul 2>nul
if errorlevel 1 (
  echo Python is not installed or not added to PATH.
  echo Please install Python 3.10 or newer from https://www.python.org/downloads/
  pause
  exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Failed to install required Python packages.
  pause
  exit /b 1
)

python convert_bank_pdf.py
pause
