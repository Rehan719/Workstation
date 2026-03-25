# Workstation v138.0: Galactic Era Setup Script (Windows)

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

# 2. Setup Backend
Write-Host "`nSetting up backend..." -ForegroundColor Cyan

# Ensure data directory and memory.json exist to prevent SQLite errors
if (!(Test-Path "agentic_core/data")) {
    New-Item -ItemType Directory -Path "agentic_core/data" | Out-Null
}
if (!(Test-Path "agentic_core/data/memory.json")) {
    Set-Content -Path "agentic_core/data/memory.json" -Value "{}"
}

poetry install

# 3. Setup Web Frontend
Write-Host "`nSetting up web frontend..." -ForegroundColor Cyan
cd apps/web
npm install
cd ../..

# 4. Setup Mobile App
Write-Host "`nSetting up mobile app..." -ForegroundColor Cyan
cd apps/mobile
npm install
cd ../..

Write-Host "`n🚀 Setup Complete! Run the following to start:" -ForegroundColor Green
Write-Host "Backend: cd agentic_core; poetry run uvicorn main:app --reload"
Write-Host "Frontend: cd apps/web; npm run dev"
Write-Host "Mobile: cd apps/mobile; npx expo start"
