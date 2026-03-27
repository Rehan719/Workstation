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

$DataDirs = @(
    "agentic_core/data",
    "agentic_core/data/memory",
    "agentic_core/data/chroma",
    "agentic_core/layers/l7_module_library",
    "logs/autonomy",
    "logs/metacognition",
    "models"
)

foreach ($dir in $DataDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir"
    }
}

# Initial JSON Files
if (!(Test-Path "agentic_core/data/memory.json")) {
    Set-Content -Path "agentic_core/data/memory.json" -Value "{}"
}
if (!(Test-Path "agentic_core/layers/l7_module_library/registry.json")) {
    Set-Content -Path "agentic_core/layers/l7_module_library/registry.json" -Value "{}"
}
if (!(Test-Path "agentic_core/data/meeting_log.json")) {
    Set-Content -Path "agentic_core/data/meeting_log.json" -Value "[]"
}

# Initial Database Files
if (!(Test-Path "agentic_core/data/interactions.db")) {
    # Create empty file for SQLite
    New-Item -ItemType File -Path "agentic_core/data/interactions.db" -Force | Out-Null
}

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
