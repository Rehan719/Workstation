# Windows Setup Guide – Workstation v0.9 (Ultimate Flagship)

Welcome to the **Workstation v0.9**. This guide will help you set up and run the entire ecosystem on your Windows 10/11 machine.

## Prerequisites

Before you begin, ensure you have the following installed. Each link leads to the official download page.

1.  **Git**: [Download Git for Windows](https://git-scm.com/download/win)
2.  **Python 3.11–3.12**: [Download Python](https://www.python.org/downloads/windows/) (Ensure you check "Add Python to PATH" during installation).
3.  **Node.js 20 LTS**: [Download Node.js](https://nodejs.org/)
4.  **Poetry**: Open PowerShell and run:
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
5.  **Ollama**: [Download Ollama for Windows](https://ollama.com/download/windows)
6.  **Docker Desktop** (Optional, for PostgreSQL/Redis): [Download Docker](https://www.docker.com/products/docker-desktop/)

---

## Step 1: Clone the Repository

Open a terminal (Command Prompt or PowerShell) and run:

```bash
git clone https://github.com/Rehan719/Workstation.git
cd Workstation
```

---

## Step 2: Automated Setup

We provide a PowerShell script to automate dependency installation and environment preparation.

1.  Open **PowerShell as Administrator**.
2.  Set execution policy (if prompted):
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
3.  Run the setup script:
    ```powershell
    .\setup.ps1
    ```

---

## Step 3: Start the Backend

Open a new terminal window in the root directory:

```bash
cd agentic_core
poetry install
poetry run uvicorn main:app --reload
```

*Note: Ensure Ollama is running in the background. If you need a model, run `ollama run llama3.2`.*

---

## Step 4: Start the Web Frontend

Open another terminal window:

```bash
cd apps/web
npm install
npm run dev
```

The Workstation will be available at [http://localhost:5173](http://localhost:5173).

---

## Step 5: Start the QEP Standalone (Free Tier)

To experience the **QEP Flagship** in its standalone mode:

```bash
cd apps/web
# Set the standalone flag for this session
$env:VITE_QEP_STANDALONE="true"
npm run dev
```

---

## Step 6: Start the Mobile App (Optional)

If you wish to test the mobile parity:

```bash
cd apps/mobile
npm install
npx expo start
```
Use the **Expo Go** app on your phone to scan the QR code.

---

## Troubleshooting

-   **Ollama Connection Error**: Ensure the Ollama app is visible in your system tray. If using Docker, check `OLLAMA_BASE_URL` in `.env`.
-   **Port Conflict**: If port 5173 is in use, the frontend will pick the next available port (e.g., 5174). Check the terminal output.
-   **Missing Dependencies**: If `poetry` or `npm` commands fail, restart your terminal to refresh PATH variables.

## Verification

1.  **AI CEO Chat**: Navigate to `/ceo` and send a message. You should see a streaming response.
2.  **Genome Explorer**: Go to `/genome` to see the 3D Merkle-DAG.
3.  **QEP Dashboard**: Navigate to `/domains/religion/qep` to test the four engines (ESE, ARO, BTO, DRAD).

---
© 2025 Virtual Sovereign Business. All rights reserved.
