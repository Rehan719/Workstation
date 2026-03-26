# Ultimate Windows Onboarding Guide – Workstation v0.9

To set up the Workstation v0.9 on Windows:

1.  **Install Prerequisites**: Git, Python 3.12, Node.js 20, Ollama.
2.  **Clone Repo**: `git clone https://github.com/Rehan719/Workstation.git`.
3.  **Run Setup**: PowerShell (Admin) `.\setup.ps1`.
4.  **Launch Backend**: `cd agentic_core; poetry run uvicorn main:app --reload`.
5.  **Launch Web**: `cd apps/web; npm run dev`.
6.  **Launch QEP Standalone**: `$env:VITE_QEP_STANDALONE="true"; npm run dev`.

Detailed guide committed to `WINDOWS_SETUP_v0.9.md`.
