# run_scheduler.ps1
# This script runs the Personal AI Employee system once
# You can schedule this in Windows Task Scheduler to run every hour

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

Write-Host "Starting AI Employee Cycle..." -ForegroundColor Cyan
python run_system.py
Write-Host "Cycle Completed." -ForegroundColor Green
