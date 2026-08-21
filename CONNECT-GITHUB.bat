@echo off
setlocal
cd /d "%~dp0"
title Connect Silwadi Website to GitHub

echo.
echo ===============================================
echo       CONNECT SILWADI WEBSITE TO GITHUB
echo ===============================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo Git is not installed.
  echo Install Git for Windows, then run this again.
  echo https://git-scm.com/download/win
  pause
  exit /b 1
)

if exist ".git" (
  echo This folder is already a Git repository.
  echo.
  git remote -v
  echo.
  pause
  exit /b 0
)

set "REPO_URL=https://github.com/cuenext/silwadi-website.git"

echo Repository:
echo %REPO_URL%
echo.

git init
git branch -M main
git add .
git commit -m "Initial Silwadi website"
git remote add origin "%REPO_URL%"
git push -u origin main

if errorlevel 1 (
  echo.
  echo GitHub push did not complete.
  echo If GitHub opened a browser login, finish signing in.
  echo Then run CONNECT-GITHUB.bat again.
  pause
  exit /b 1
)

echo.
echo ===============================================
echo GitHub connected successfully.
echo ===============================================
echo.
echo Now use START-SILWADI.bat.
echo.
pause
