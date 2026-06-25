@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_executive.ps1"
echo.
echo Run finished. Check logs, review_outputs, and final_outputs.
pause
