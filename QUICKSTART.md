# Jules AI v100.0 APOTHEOSIS OF SYNERGY: Quick Start Guide

## 🚀 One-Click Setup (All-in-One)
Run the following command to install dependencies, synthesize the v100 DNA baseline, run verification tests, and launch the dashboard:

### 🪟 Windows (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -c "pip install -e .; python -m agentic_core.synthesis.grand_synthesis_engine; python -m pytest tests/v100/; streamlit run src/dashboard/app.py"
```

### 🍎 macOS / 🐧 Linux
```bash
pip install -e . && python3 -m agentic_core.synthesis.grand_synthesis_engine && python3 -m pytest tests/v100/ && streamlit run src/dashboard/app.py
```

---

## 🛠️ Verification & Audits
To manually verify the environment integrity and constitutional adherence:
```bash
# Environment Verification
python3 scripts/verify_environment.py

# Constitutional Audit (312+ Articles)
python3 scripts/audit_constitution_v100.py

# Biomimetic Fidelity Score (v100 Target: 0.995)
python3 -m agentic_core.validation.biomimetic_fidelity
```

---

## 🌐 Deployment
Deploy the workstation for free using the following targets:
- **Frontend (Vercel)**: `cd src/qep_frontend && npm install && npm run build` -> Deploy `dist/`
- **Backend (Render)**: Connect repo, set build command `pip install -r requirements.txt`, start command `uvicorn agentic_core.main:app --host 0.0.0.0 --port $PORT`
- **Dashboard (Streamlit)**: Deploy `src/dashboard/app.py` directly to Streamlit Cloud.

---

## 📜 Documentation Reference
- [User Guide (Non-Technical)](USER_GUIDE.md)
- [Architecture Deep Dive](ARCHITECTURE.md)
- [Apotheosis Constitution](CONSTITUTION_v100.0.0.md)
