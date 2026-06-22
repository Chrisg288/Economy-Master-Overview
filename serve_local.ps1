$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "Serving Economy Master Modular Rebuild at http://localhost:8000/"
Start-Process "http://localhost:8000/"
python -m http.server 8000
