@echo off
TITLE Workstation v0.9 - Start Backend
echo 🚀 Starting Workstation Backend (v0.9) using local venv...
set PYTHONPATH=C:\Users\rehan\Workstation
set PYTHONNOUSERSITE=1
C:\Users\rehan\Workstation\venv\Scripts\python.exe -c "import sys; print(f'Interpreter: {sys.executable}')"
C:\Users\rehan\Workstation\venv\Scripts\python.exe -m uvicorn agentic_core.main:app --reload --host 127.0.0.1 --port 8000
pause
