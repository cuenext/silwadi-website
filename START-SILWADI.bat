@echo off
setlocal
cd /d "%~dp0"
title Silwadi Website Local Server

echo Starting Silwadi website...
echo.

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\dev-server.ps1"

echo.
echo Silwadi server stopped.
pause
