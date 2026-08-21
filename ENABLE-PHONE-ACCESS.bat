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
echo [2/2] Allowing port 5500 through Windows Firewall...
echo       Scope: any Windows network profile, LOCAL SUBNET ONLY.
netsh advfirewall firewall delete rule name="Silwadi Website Phone Preview" >nul 2>&1
netsh advfirewall firewall add rule name="Silwadi Website Phone Preview" dir=in action=allow protocol=TCP localport=5500 profile=any remoteip=LocalSubnet

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
echo The firewall now allows port 5500 from devices on your local Wi-Fi/LAN
echo even if Windows labels this Wi-Fi network as Public.
echo.
echo Next:
echo   1. Keep START-SILWADI.bat running.
echo   2. Open the cyan [PHONE] address shown there on your phone.
echo   3. Make sure the phone is on the SAME Wi-Fi as this laptop.
echo.
pause
