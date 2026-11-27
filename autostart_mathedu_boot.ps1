# Auto-start Mathedu 24/7 daemons and Antigravity CLI in D:\mathedu on Windows logon
$ErrorActionPreference = 'Continue'
$WorkDir = 'D:\mathedu'
$LogPath = Join-Path $WorkDir '.agents\boot_autostart.log'
$PythonW = 'C:\Python\Python312\pythonw.exe'
$WtExe   = Join-Path $env:LOCALAPPDATA 'Microsoft\WindowsApps\wt.exe'
$AgyExe  = 'C:\Users\min\AppData\Local\agy\bin\agy.EXE'

# Wait up to 30s for D:\mathedu after boot
for ($i = 0; $i -lt 15; $i++) {
    if (Test-Path $WorkDir) { break }
    Start-Sleep -Seconds 2
}
if (-not (Test-Path $WorkDir)) { exit 1 }

Set-Location $WorkDir
$ts = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
New-Item -ItemType Directory -Force -Path (Split-Path $LogPath) | Out-Null
Add-Content -Path $LogPath -Encoding UTF8 -Value "[$ts] Boot autostart triggered in $WorkDir"

# 1. Immediately ensure both 24/7 Mathedu daemons are running from D:\mathedu
if (Test-Path $PythonW) {
    Start-Process -FilePath $PythonW -WorkingDirectory $WorkDir -ArgumentList @('-X', 'utf8', (Join-Path $WorkDir 'mathedu_foundation_daemon.py'), '--daemon-ensure') -WindowStyle Hidden
    Start-Process -FilePath $PythonW -WorkingDirectory $WorkDir -ArgumentList @('-X', 'utf8', (Join-Path $WorkDir 'mathedu_telegram_bridge.py'), '--watchdog-ensure') -WindowStyle Hidden
    Add-Content -Path $LogPath -Encoding UTF8 -Value "[$ts] Ensured foundation_daemon and telegram_bridge from $WorkDir"
}

# 2. Launch Antigravity CLI in Windows Terminal inside D:\mathedu (duplicate-safe)
$existingAgy = Get-Process -Name 'agy' -ErrorAction SilentlyContinue
if ($existingAgy) {
    $pids = ($existingAgy | Select-Object -ExpandProperty Id) -join ','
    Add-Content -Path $LogPath -Encoding UTF8 -Value "[$ts] agy already running (PID=$pids) -> skipped duplicate launch"
} elseif (Test-Path $AgyExe) {
    Start-Sleep -Seconds 5
    $innerCmd = "Set-Location '$WorkDir'; & '$AgyExe' --continue"
    if (Test-Path $WtExe) {
        Start-Process -FilePath $WtExe -WorkingDirectory $WorkDir -ArgumentList @(
            '-d', $WorkDir,
            '--title', 'Antigravity (D:\mathedu)',
            'powershell.exe', '-NoExit', '-Command', $innerCmd
        )
        Add-Content -Path $LogPath -Encoding UTF8 -Value "[$ts] Launched Windows Terminal -> agy --continue in $WorkDir"
    } else {
        Start-Process -FilePath 'powershell.exe' -WorkingDirectory $WorkDir -ArgumentList @('-NoExit', '-Command', $innerCmd)
        Add-Content -Path $LogPath -Encoding UTF8 -Value "[$ts] Launched PowerShell -> agy --continue in $WorkDir"
    }
} else {
    Add-Content -Path $LogPath -Encoding UTF8 -Value "[$ts] ERROR: agy.EXE not found at $AgyExe"
}
