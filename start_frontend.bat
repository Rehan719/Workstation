@echo off
TITLE Workstation - frontend
rem W919 (FU-742) - the frontend is apps\workstation-superapp. It serves on the address vite prints (port 5173 unless
rem that port is taken) and sends /api to the backend on 127.0.0.1:8000 (vite.config.js). Start the backend first.
cd /d "%~dp0apps\workstation-superapp"
call npm run dev
pause
