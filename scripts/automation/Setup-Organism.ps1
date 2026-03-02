# Jules AI v71.0 Setup Automation (PowerShell)
Write-Host "Awakening Jules AI v71.0 Beta..." -ForegroundColor Cyan

# 1. Environment Check
$PythonVersion = python --version
Write-Host "Detected Python: $PythonVersion"

# 2. Dependency Installation
Write-Host "Installing organism-grade dependencies..."
pip install -r requirements.txt

# 3. Directory Initialization
New-Item -ItemType Directory -Force -Path "meta", "logs", "artifacts"

# 4. Constitutional Synthesis
Write-Host "Executing Grand Synthesis Engine..."
python -c "import asyncio; from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine; engine = GrandSynthesisEngine(['.']); asyncio.run(engine.run_synthesis())"

Write-Host "Setup Complete. Organism DNA established." -ForegroundColor Green
