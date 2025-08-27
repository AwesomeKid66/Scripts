# Self-elevating PowerShell script
# Save as disable-wake.ps1

# Check if running as Administrator
$currUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Restarting script with administrator privileges..." -ForegroundColor Yellow
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# ------------------------
# Main script logic below
# ------------------------

# Get list of wake-enabled devices
$wakeDevices = powercfg -devicequery wake_armed

Write-Host "Devices currently allowed to wake the computer:" -ForegroundColor Cyan
$wakeDevices | ForEach-Object { Write-Host " - $_" }

foreach ($device in $wakeDevices) {
    Write-Host "Disabling wake for: $device" -ForegroundColor Yellow
    powercfg -devicedisablewake "$device"
}

Write-Host "`nAll listed devices have been disabled from waking the computer." -ForegroundColor Green
Write-Host "Only the power button should now be able to turn your PC on." -ForegroundColor Green
