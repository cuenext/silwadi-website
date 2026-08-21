@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Diagnose Silwadi Phone Access

echo.
echo =====================================================
echo        SILWADI PHONE ACCESS - DIAGNOSTICS
echo =====================================================
echo.
echo IMPORTANT: Keep START-SILWADI.bat running in another window.
echo.

echo [1] NETWORK PROFILE
powershell.exe -NoProfile -Command "Get-NetConnectionProfile | Format-Table Name,InterfaceAlias,NetworkCategory,IPv4Connectivity -AutoSize"
echo.

echo [2] LAPTOP IPv4 ADDRESSES
ipconfig | findstr /I /C:"IPv4 Address" /C:"IPv4-adresse" /C:"IPv4"
echo.

echo [3] PORT 5500 LISTENER
netstat -ano | findstr /I "LISTENING" | findstr ":5500"
if errorlevel 1 echo NO LISTENER FOUND ON PORT 5500
echo.

echo [4] HTTP URL PERMISSION
netsh http show urlacl url=http://+:5500/
echo.

echo [5] WINDOWS FIREWALL RULE
netsh advfirewall firewall show rule name="Silwadi Website Phone Preview"
echo.

echo [6] HTTP TESTS FROM THIS LAPTOP
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ip = $null; try { $ip = Get-NetIPConfiguration ^| Where-Object { $_.IPv4DefaultGateway -and $_.IPv4Address } ^| ForEach-Object { $_.IPv4Address.IPAddress } ^| Where-Object { $_ -and $_ -ne '127.0.0.1' -and $_ -notlike '169.254.*' } ^| Select-Object -First 1 } catch {}; Write-Host ('Detected LAN IP: ' + $ip); foreach($url in @('http://127.0.0.1:5500/', ('http://' + $ip + ':5500/'))) { if($url -match '^http://:') { continue }; try { $r = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 5; Write-Host ($url + '  --  HTTP ' + [int]$r.StatusCode) -ForegroundColor Green } catch { Write-Host ($url + '  --  FAILED: ' + $_.Exception.Message) -ForegroundColor Red } }"
echo.

echo [7] ACTIVE WIFI / ETHERNET ADAPTERS
powershell.exe -NoProfile -Command "Get-NetAdapter | Where-Object Status -eq 'Up' | Format-Table Name,InterfaceDescription,Status,LinkSpeed -AutoSize"
echo.

echo =====================================================
echo TAKE A SCREENSHOT OF THIS WHOLE WINDOW AND SEND IT
echo TO CHATGPT. DO NOT CHANGE ANYTHING YET.
echo =====================================================
echo.
pause
