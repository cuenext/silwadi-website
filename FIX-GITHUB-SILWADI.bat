@echo off
setlocal
cd /d "%~dp0"

echo Fixing Git identity and first commit...
git config user.name "cuenext"
git config user.email "cuenext@users.noreply.github.com"
git branch -M main
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin "https://github.com/cuenext/silwadi-website.git"
) else (
  git remote set-url origin "https://github.com/cuenext/silwadi-website.git"
)
git add -A
git commit -m "Initial Silwadi website"
git push -u origin main

echo.
echo If GitHub asks you to sign in, complete the browser login.
echo.
pause
