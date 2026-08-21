$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   SILWADI WEBSITE - LOCAL DEVELOPMENT SERVER" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# -------------------------------
# Git sync
# -------------------------------
$git = Get-Command git -ErrorAction SilentlyContinue
$syncJob = $null

if ($git -and (Test-Path (Join-Path $repo ".git"))) {
    Write-Host "[SYNC] Pulling latest GitHub version..." -ForegroundColor Yellow
    try {
        git -C $repo pull --ff-only
    } catch {
        Write-Host "[SYNC] Pull failed. Continuing with local files." -ForegroundColor DarkYellow
    }

    $syncJob = Start-Job -ScriptBlock {
        param($repoPath)

        while ($true) {
            Start-Sleep -Seconds 5

            try {
                $changes = git -C $repoPath status --porcelain 2>$null

                # Don't overwrite local edits.
                if (-not $changes) {
                    git -C $repoPath pull --ff-only 2>$null | Out-Null
                }
            } catch {
                # Ignore temporary network/Git issues and continue watching.
            }
        }
    } -ArgumentList $repo

    Write-Host "[SYNC] GitHub watcher active." -ForegroundColor Green
} else {
    Write-Host "[SYNC] Git is not connected yet. Running local files only." -ForegroundColor DarkYellow
}

# -------------------------------
# Pure PowerShell static server
# No Python / Node required
# -------------------------------
$port = 5500
$prefix = "http://127.0.0.1:$port/"
$listener = New-Object System.Net.HttpListener

try {
    $listener.Prefixes.Add($prefix)
    $listener.Start()
} catch {
    Write-Host ""
    Write-Host "[ERROR] Could not start the server on port $port." -ForegroundColor Red
    Write-Host "Another program may already be using this port." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try closing any old Silwadi server window, then run START-SILWADI.bat again." -ForegroundColor Yellow

    if ($syncJob) {
        Stop-Job $syncJob -ErrorAction SilentlyContinue
        Remove-Job $syncJob -ErrorAction SilentlyContinue
    }

    Read-Host "Press Enter to close"
    exit 1
}

Write-Host "[SERVER] Running at $prefix" -ForegroundColor Green
Write-Host "[SERVER] Keep this window open while previewing." -ForegroundColor Gray
Write-Host "[SERVER] Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""

Start-Process $prefix

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".webp" = "image/webp"
    ".ico"  = "image/x-icon"
    ".txt"  = "text/plain; charset=utf-8"
}

function Send-Response {
    param(
        [System.Net.HttpListenerContext]$Context,
        [int]$StatusCode,
        [byte[]]$Bytes,
        [string]$ContentType
    )

    $Context.Response.StatusCode = $StatusCode
    $Context.Response.ContentType = $ContentType
    $Context.Response.ContentLength64 = $Bytes.Length
    $Context.Response.Headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

    $Context.Response.OutputStream.Write($Bytes, 0, $Bytes.Length)
    $Context.Response.OutputStream.Close()
}

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()

        try {
            $rawPath = [System.Uri]::UnescapeDataString($context.Request.Url.AbsolutePath)
            $relative = $rawPath.TrimStart("/")

            if ([string]::IsNullOrWhiteSpace($relative)) {
                $relative = "index.html"
            }

            # Block path traversal
            $candidate = Join-Path $repo $relative
            $fullPath = [System.IO.Path]::GetFullPath($candidate)
            $repoFull = [System.IO.Path]::GetFullPath($repo)

            if (-not $fullPath.StartsWith($repoFull, [System.StringComparison]::OrdinalIgnoreCase)) {
                $msg = [System.Text.Encoding]::UTF8.GetBytes("403 Forbidden")
                Send-Response $context 403 $msg "text/plain; charset=utf-8"
                continue
            }

            # If a directory was requested, serve index.html inside it.
            if (Test-Path $fullPath -PathType Container) {
                $fullPath = Join-Path $fullPath "index.html"
            }

            if (-not (Test-Path $fullPath -PathType Leaf)) {
                $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
                Send-Response $context 404 $msg "text/plain; charset=utf-8"
                continue
            }

            $ext = [System.IO.Path]::GetExtension($fullPath).ToLowerInvariant()
            $contentType = $mimeTypes[$ext]

            if (-not $contentType) {
                $contentType = "application/octet-stream"
            }

            $bytes = [System.IO.File]::ReadAllBytes($fullPath)
            Send-Response $context 200 $bytes $contentType
        }
        catch {
            try {
                $msg = [System.Text.Encoding]::UTF8.GetBytes("500 Server Error")
                Send-Response $context 500 $msg "text/plain; charset=utf-8"
            } catch {}
        }
    }
}
finally {
    try { $listener.Stop() } catch {}
    try { $listener.Close() } catch {}

    if ($syncJob) {
        Stop-Job $syncJob -ErrorAction SilentlyContinue
        Remove-Job $syncJob -ErrorAction SilentlyContinue
    }
}
