@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_combine.ps1"
echo.
echo Combine finished. Check final_outputs and logs.
pause
