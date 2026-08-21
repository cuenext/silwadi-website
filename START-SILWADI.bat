@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Silwadi Website Local Server

echo Starting Silwadi website...
echo.

REM Pull updates BEFORE PowerShell loads the server script.
REM This ensures changes to tools\dev-server.ps1 take effect immediately.
where git >nul 2>&1
if not errorlevel 1 if exist ".git" (
  echo [LAUNCHER] Checking GitHub before server startup...
  git pull --ff-only
  echo.
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\dev-server.ps1"

echo.
echo Silwadi server stopped.
pause
