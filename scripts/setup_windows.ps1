# Jules AI v99 Windows Setup Script
Write-Host "?? Awaken Transcendent: Initializing v99 Environment on Windows..." -ForegroundColor Cyan

# 1. Create Virtual Environment
if (!(Test-Path venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# 2. Activate Environment
Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

# 3. Upgrade Pip & Install Dependencies
Write-Host "Installing dependencies (this may take a few minutes)..."
python -m pip install --upgrade pip
python -m pip install -e .

# 4. Install Dev Dependencies
Write-Host "Installing development tools..."
python -m pip install pytest pytest-asyncio

# 5. Run Grand Synthesis
Write-Host "?? Synchronizing Transcendent DNA..."
python -m agentic_core.synthesis.grand_synthesis_engine

# 6. Verify Installation (skip if verify_environment.py missing)
if (Test-Path scripts/verify_environment.py) {
    Write-Host "?? Verifying environment integrity..."
    python scripts/verify_environment.py
} else {
    Write-Host "Verification script not found ? skipping."
}

Write-Host "`n? Jules AI v99.0 is operational and ready for evolution." -ForegroundColor Green
Write-Host "To start the dashboard, run: streamlit run src/dashboard/app.py" -ForegroundColor Yellow
