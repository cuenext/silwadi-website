@echo off
setlocal
cd /d "%~dp0"
title Update Silwadi Website

where git >nul 2>&1
if errorlevel 1 (
  echo Git is not installed.
  pause
  exit /b 1
)

if not exist ".git" (
  echo This folder is not connected to GitHub yet.
  echo Run CONNECT-GITHUB.bat first.
  pause
  exit /b 1
)

echo Pulling latest version...
git pull --ff-only
echo.
echo Done. Refresh http://127.0.0.1:5500 in your browser.
pause
