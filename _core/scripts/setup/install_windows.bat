@echo off
setlocal

REM Run from repo root regardless of where the batch file is launched.
pushd "%~dp0\..\..\.." >nul

set "PS1_PATH=_core\scripts\setup\install_windows.ps1"

where powershell >nul 2>nul
if %ERRORLEVEL%==0 (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1_PATH%" %*
  set "EXITCODE=%ERRORLEVEL%"
  popd >nul
  exit /b %EXITCODE%
)

where pwsh >nul 2>nul
if %ERRORLEVEL%==0 (
  pwsh -NoProfile -ExecutionPolicy Bypass -File "%PS1_PATH%" %*
  set "EXITCODE=%ERRORLEVEL%"
  popd >nul
  exit /b %EXITCODE%
)

echo Could not find PowerShell. Install Windows PowerShell or PowerShell 7 and try again.
popd >nul
exit /b 1
