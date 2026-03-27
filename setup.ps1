# Workstation v1.0 Global Launch Setup Script (Windows)

# 1. Check for Prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Cyan

if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✅ Node.js: $(node -v)"
} else {
    Write-Host "❌ Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python: $(python --version)"
} else {
    Write-Host "❌ Python not found. Please install from https://www.python.org/" -ForegroundColor Red
}

if (Get-Command poetry -ErrorAction SilentlyContinue) {
    Write-Host "✅ Poetry found."
} else {
    Write-Host "⚠️ Poetry not found. Installing via pip..."
    pip install poetry
}

# 2. Setup Data Directories and Initial Files
Write-Host "`nSetting up data infrastructure..." -ForegroundColor Cyan

# Run Python initialization script for directories and initial data
python scripts/init_data.py

# 3. Environment Configuration
if (!(Test-Path "agentic_core/.env")) {
    if (Test-Path ".env.template") {
        Copy-Item ".env.template" "agentic_core/.env"
        Write-Host "✅ Created .env from template."
    }
}

# 4. Install Dependencies
Write-Host "`nInstalling backend dependencies..." -ForegroundColor Cyan
cd agentic_core
poetry install
cd ..

Write-Host "`nInstalling frontend dependencies..." -ForegroundColor Cyan
cd apps/web
npm install
cd ..\..

Write-Host "`n🚀 Setup Complete! Run the following to start:" -ForegroundColor Green
Write-Host "Backend: .\start_backend.bat"
Write-Host "Frontend: .\start_frontend.bat"
