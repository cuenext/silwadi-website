@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Enable Silwadi Phone Preview

:: -------------------------------------------------
:: Request Administrator privileges once.
:: -------------------------------------------------
net session >nul 2>&1
if not "%errorlevel%"=="0" (
  echo Requesting Administrator permission...
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

echo.
echo ===============================================
echo       ENABLE SILWADI PHONE PREVIEW
echo ===============================================
echo.

echo [1/2] Allowing the local web server on port 5500...
netsh http delete urlacl url=http://+:5500/ >nul 2>&1
netsh http add urlacl url=http://+:5500/ user="%USERDOMAIN%\%USERNAME%"

if errorlevel 1 (
  echo.
  echo [ERROR] Windows could not add the URL permission.
  echo Send ChatGPT a screenshot of this window.
  echo.
  pause
  exit /b 1
)

echo.
echo [2/2] Allowing port 5500 through Windows Firewall on PRIVATE networks...
netsh advfirewall firewall delete rule name="Silwadi Website Phone Preview" >nul 2>&1
netsh advfirewall firewall add rule name="Silwadi Website Phone Preview" dir=in action=allow protocol=TCP localport=5500 profile=private

if errorlevel 1 (
  echo.
  echo [ERROR] Windows Firewall rule could not be created.
  echo Send ChatGPT a screenshot of this window.
  echo.
  pause
  exit /b 1
)

echo.
echo ===============================================
echo            PHONE ACCESS ENABLED
echo ===============================================
echo.
echo You only need to run this setup once.
echo.
echo Next:
echo   1. Close any old Silwadi server window.
echo   2. Double-click START-SILWADI.bat.
echo   3. Look for the cyan [PHONE] address.
echo   4. Open that address on your phone while both devices are on the same Wi-Fi.
echo.
echo IMPORTANT:
echo Your Windows Wi-Fi network should be set to Private for the firewall rule to apply.
echo.
pause
