# Workstation - set-up on Windows (W919, FU-742).
#
# Run it once, from the repository folder, in PowerShell:
#     powershell -ExecutionPolicy Bypass -File .\setup.ps1
#
# It makes a Python environment in .\venv and installs the backend's pinned dependencies into it from
# requirements.txt, the same list the Windows CI job installs. It installs the frontend's dependencies with
# npm install, as the frontend CI job does. It copies .env.example to .env when there is no .env; every switch in
# it is off. Then it checks that the app imports. It switches nothing on. Apart from pip's and npm's own caches, it
# writes nothing outside this folder. Each step stops the set-up if it fails, and says which step it was.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Step([string]$What, [scriptblock]$Run) {
    Write-Host ""
    Write-Host $What -ForegroundColor Cyan
    & $Run
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $What (exit code $LASTEXITCODE). Nothing after it was run." -ForegroundColor Red
        exit 1
    }
}

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not on PATH. Install Python 3.12 from python.org, then run this again." -ForegroundColor Red
    exit 1
}
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "npm is not on PATH. Install Node.js 20 from nodejs.org, then run this again." -ForegroundColor Red
    exit 1
}

if (!(Test-Path "venv\Scripts\python.exe")) {
    Step "Making the Python environment in .\venv" { python -m venv venv }
}
Step "Installing the backend's pinned dependencies (requirements.txt)" { .\venv\Scripts\python.exe -m pip install -r requirements.txt }
Step "Installing the frontend's dependencies (npm install)" { npm install }
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Copied .env.example to .env. Every switch in it is off." -ForegroundColor Green
}
Step "Checking that the app imports" { .\venv\Scripts\python.exe -c "import agentic_core.app_mvp; print('boot ok')" }

Write-Host ""
Write-Host "Set-up done. Start the backend with .\start_backend.bat and the frontend with .\start_frontend.bat." -ForegroundColor Green
