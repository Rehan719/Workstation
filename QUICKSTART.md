# Workstation Quick Start – v137.1

Get the Workstation ecosystem up and running in minutes. This guide covers the **Sentient Civilization Epoch (v137.1)** setup.

## 🚀 One-Click Orchestration
Launch the full development environment (Site, Web App, and Backend) with a single command:

```bash
# Clone and Enter
git clone https://github.com/vsb-ai/workstation.git && cd workstation

# Orchestrate v137.1
./deploy.sh --v137
```

## 🛠️ Manual Setup

### 1. Prerequisites
- **Python 3.12+**
- **Node.js 20+** (for frontend/mobile)
- **Git**

### 2. Environment Configuration
```bash
cp .env.template .env
# Open .env and add your keys for:
# - OpenAI / Claude (for VSB AI CEO)
# - Firebase (for Auth)
# - Google Cloud (for Search/Vision)
```

### 3. Core Engine Installation
```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🧪 Verification
Ensure the system is healthy and constitutionally compliant:

```bash
# Run the logic verification suite
python scripts/verify_v137_logic.py

# Check constitutional fidelity (Articles 1-1095)
python scripts/verify_constitutional_compliance.py
```

## 🌐 Accessing the Dashboards
Once `deploy.sh` is running:
- **Web App (Enterprise/Governance)**: `http://localhost:3000`
- **Scholar Realm (QEP)**: `http://localhost:3001`
- **API Reference**: `http://localhost:8000/docs`

---
*Welcome to the future of sovereign intelligence.*
