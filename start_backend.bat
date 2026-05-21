@echo off
TITLE Workstation v0.9 - Start Backend
echo 🚀 Starting Workstation Backend (v0.9) using local venv...
cd agentic_core
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
