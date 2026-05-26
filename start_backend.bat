@echo off
TITLE Workstation v0.9 - Start Backend
echo 🚀 Starting Workstation Backend (v0.9) using local venv...

:: Set PYTHONPATH to the current directory for module resolution
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
:: Ensure we use the local venv's packages only
set PYTHONNOUSERSITE=1

:: Locate the venv's python executable
set "VENV_PYTHON=%~dp0venv\Scripts\python.exe"

if exist "%VENV_PYTHON%" (
    echo Using Virtual Environment: "%VENV_PYTHON%"
    "%VENV_PYTHON%" -c "import sys; print(f'Interpreter: {sys.executable}')"
    "%VENV_PYTHON%" -m uvicorn agentic_core.main:app --reload --host 127.0.0.1 --port 8000
) else (
    echo ❌ ERROR: Virtual environment not found at "%VENV_PYTHON%"
    echo Please run setup.ps1 first.
    pause
)
