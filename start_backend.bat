@echo off
TITLE Workstation - backend
rem W919 (FU-742) - starts the app every deployment starts (agentic_core.app_mvp:app; the Dockerfile and render.yaml
rem run the same one), with the Python environment setup.ps1 makes in .\venv, on http://127.0.0.1:8000.
rem It is running when http://127.0.0.1:8000/health answers. Stop it with Ctrl+C.
cd /d "%~dp0"
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
set PYTHONNOUSERSITE=1
set "VENV_PYTHON=%~dp0venv\Scripts\python.exe"
if not exist "%VENV_PYTHON%" (
    echo The Python environment is not there yet: %VENV_PYTHON%
    echo Run the set-up first:  powershell -ExecutionPolicy Bypass -File .\setup.ps1
    pause
    exit /b 1
)
"%VENV_PYTHON%" -m uvicorn agentic_core.app_mvp:app --host 127.0.0.1 --port 8000
