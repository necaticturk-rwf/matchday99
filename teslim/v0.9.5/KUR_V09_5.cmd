@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher py not found. Install Python 3 and run this file again.
  pause
  exit /b 1
)
if "%~1"=="" (
  py "%~dp0apply_v09_5.py" --auto
) else (
  py "%~dp0apply_v09_5.py" "%~1"
)
set "PATCH_RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %PATCH_RESULT%
