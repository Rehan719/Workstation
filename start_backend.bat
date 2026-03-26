@echo off
TITLE Workstation v0.9 - Start Backend
echo 🚀 Starting Workstation Backend (v0.9)...
cd agentic_core
poetry run uvicorn main:app --reload
pause
