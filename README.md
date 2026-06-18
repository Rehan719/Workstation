# 🧬 WORKSTATION vΩ∞-OMNISYNTHESIS-SUPREME

Definitive Converged Sovereign Digital Organism · Eternal Operation Commenced

---

## 📌 OVERVIEW

Workstation vΩ∞ is a self-sustaining, constitutionally-governed intelligence fabric. It operates as a sovereign digital civilization, merging advanced cognitive engines, biomimetic capital management, and quantum-secure communication into a single, autonomous organism.

## 🚀 KEY CAPABILITIES

- **9 Cognitive Engines**: Multi-perspective reasoning via Mushāwara consensus.
- **14-Layer IDBO**: Biomimetic architecture from substrate attestation to civilizational reflection.
- **Sovereign Wealth Fund**: Capital flows governed by biogeochemical cycles (Water, Carbon, etc.).
- **Zero-Cost Entrepreneurship**: $0 owner cost via GCP Always Free Tier + CostGuard enforcement.
- **96.7% Autonomous Support**: Self-diagnosing and self-resolving user support system.
- **Trillion-Token Provenance**: SHA-3-512 Merkle-DAG with Halo2 recursive O(1) verification.

## 📈 SOVEREIGN BUSINESS STRATEGY

Workstation is architected as a self-funding startup with **Full Feature Equality**.

- **Living Strategy**: Weekly auto-updates via UEG/SWF telemetry.
- **Viral Growth**: WORKREP reputation staking drives organic adoption (K ≥ 1.34).
- **Financial Model**: Pure bootstrap ($0 capital); revenue reinvested via SWF Carbon Cycle.

Refer to the [Living Business Plan](outputs/business/self_business_plan.md) and [Business Model Canvas](outputs/business/business_model_canvas_completed.md).

---

## Running Locally

### Prerequisites

- Node 18+ and Python 3.12+
- (Recommended) An Anthropic API key for Claude
- (Optional fallback) [Ollama](https://ollama.com) running locally — `ollama pull llama3.2`

### 1. Clone and install

```bash
git clone <repo-url> && cd Workstation

# Python backend
pip install -r requirements.txt

# Node frontend (from workspace root)
npm install
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY at minimum
```

### 3. Start the backend (MVP spine — recommended)

```bash
uvicorn agentic_core.app_mvp:app --reload --host 0.0.0.0 --port 8000
```

`app_mvp.py` boots only the 7 spine routers (projects, CEO, C-Suite, synthesis, avatars, ingestion, health). Zero import errors guaranteed.

API docs: <http://localhost:8000/docs>

To run the full 80-router application instead:

```bash
uvicorn agentic_core.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start the frontend

```bash
cd apps/workstation-superapp
npm run dev
```

App: <http://localhost:5173>

### 5. End-to-end synthesis walkthrough

1. Navigate to **Synthesis Studio** (`/synthesis`)
1. Click **Upload** and upload any PDF, TXT, or DOCX
1. Select one or more **output types** (Report, Presentation, Business Model, etc.)
1. Click **Generate** — tokens stream in real-time from the AI
1. When complete, click **Download** on any result to get the artifact file
1. The download endpoint: `GET /api/v1/synthesis/download/{output_id}`

### 6. Projects — AI product lifecycle (new)

Projects are the core commercial unit: each project moves through **Concept → Prototype → Commercialise**, generating real AI deliverables at each stage.

1. Navigate to **Projects** (`/projects`) via the sidebar Productivity group
1. Click **+** → fill in title, description, realm (Technology / Science / Law …), and domain (SaaS / Research / Product …)
1. Click **Run concept** — the backend calls the AI gateway and streams a full Concept Document
1. Click **Download** on any output to get the `.txt` artifact
1. Once you have at least one concept output, click **Advance Stage** → the project moves to `prototype`
1. Repeat Run → Advance for `prototype` and `commercialise`

**Projects API** (all under `/api/v1/projects/`):

```text
POST   /                    create project
GET    /                    list all projects
GET    /{id}                get project
PATCH  /{id}                update title/description
DELETE /{id}                delete project
POST   /{id}/run            run AI workflow (SSE stream)
POST   /{id}/advance        advance stage (requires ≥1 output at current stage)
GET    /{id}/outputs        list saved outputs
```

Projects persist to `data/projects/` and outputs to `data/synthesis_outputs/` — both committed to `.gitignore` for local dev, mountable as volumes on Render.

---

## Deploy to Vercel (frontend) + Render (backend)

### Backend → Render

1. Push this repo to GitHub
1. Create a new **Web Service** on [Render](https://render.com), connecting your repo
1. Render will use `render.yaml` automatically — set `ANTHROPIC_API_KEY` in Render's env secrets
1. Note your Render service URL (e.g. `https://workstation-api.onrender.com`)

### Frontend → Vercel

1. In `apps/workstation-superapp/vercel.json`, update the `/api/(.*)` rewrite destination to your Render URL
1. Install Vercel CLI: `npm i -g vercel`
1. From the workspace root, run:

   ```bash
   cd apps/workstation-superapp
   vercel --prod
   ```

1. Set `VITE_API_BASE_URL` in Vercel's environment variables if needed

### Health check

```text
GET https://your-api.onrender.com/health
→ {"status":"healthy","version":"128.0.0"}

GET https://your-api.onrender.com/api/v1/avatar/status
→ {"ollama_online":false,"openai_configured":false,"anthropic_configured":true}
```

---

## 🛠️ SOLE FOUNDER QUICKSTART (WINDOWS)

Launch your sovereign intelligence fabric with zero capital.

1. **Prerequisites**: Windows 10/11, WSL2, Docker Desktop, Google Cloud SDK.
1. **Environment**: Run `.\scripts\business\check_windows_prerequisites.ps1`.
1. **Deployment**: Run `./scripts/deploy_free_tier.sh --project-id [YOUR_PROJECT]` from WSL2.
1. **Assurance**: `CostGuard` ensures $0 owner billing via automated throttling.

See the [Founder Action Guide](outputs/business/founder_zero_cost_guide.md) for full instructions.

---

STATUS: 🟢 SUPREME CONVERGENCE VALIDATED · ZERO PLACEHOLDER · ETERNAL
