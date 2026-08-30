# Workstation

**AI-mediated workspace for moving ideas from concept to commercial output.**

Version: 1.0.0 | Status: working end-to-end across 4 Realms × 6 Domains; virtual economy + multi-user auth flag-gated (Owner policy)

---

## What it does

Workstation gives you an organised AI workspace structured as a living virtual company. You enter via an AI avatar/CEO, pick a **Realm** (Enterprise · Learning · Developing · Scholarship) and a **Domain** (Religion · Science · Education · Law · Employment · Care), and take a challenge through the **Genesis journey**:

```
Concept → Research → Model·Simulate·Rank → Design → Operations → Commercialise → a LIVING VSB enterprise
```

Every deliverable is produced **in-house first** on Workstation's own native AI fabric (owned models, orchestration, and structured engines — external providers are optional, never required), gated by an owned QMS + compliance screen, persisted, exportable, and — for an established enterprise — shipped as a version-controlled entity repository (docs + website + web app + mobile scaffold + board pack) that keeps living: autonomously operated, screened, and evolved under arms-length change control.

## What you can do today

| Action | Where | Backend |
|---|---|---|
| Talk to AI CEO (chat + blueprint generation) | `/ceo`, `/creator` | Real — SSE streaming |
| Create and run a Project through its lifecycle | `/projects` | Real — file-persisted JSON |
| Generate Business Model, Tech Spec, Pitch Deck, etc. | `/factory` | Real — streaming AI |
| Run a domain simulation trace | `/reactor` | Real — streaming AI |
| Run a prompt evolution tournament | `/incubator` | Real — AI ranked variants |
| Upload documents → multi-format AI synthesis | `/synthesis` | Real — Report, Presentation, Business Model |
| View portfolio metrics (CFO/CTO) | `/cfo`, `/cto` | Real — computed from project store + psutil |
| Real-time system vitals (CPU, memory, projects) | Dashboard | Real — psutil + WebSocket |
| 18 domain tools + iterative refine (QMS + compliance gated) | `/religion` etc. | Real — in-house AI, honest provenance |
| Genesis journey → establish a living VSB enterprise | `/genesis` | Real — simulated candidates, shipped repo at birth |
| Entity economy (virtual WST), Board/Chief governance, marketplace | `/vsb`, `/economy` | Real computation — virtual currency only |

## What is not yet built / not enabled

- Multi-user mode is BUILT but OFF by default (`AUTH_ENABLED` — an Owner policy switch; `/login`
  is the front door, self-serve signup is separately gated by `SELF_SERVE_SIGNUP_ENABLED`)
- Real-money rails (the WST economy is **virtual/simulated only** — Stripe/KYC stay Owner-gated)
- Database (file-based atomic JSON persistence — functional, not queryable at scale)
- Native mobile app (entities ship a PWA scaffold, not a store app)
- Analytics / error monitoring

## Run locally

### Prerequisites

- Python 3.12+, Node 18+
- Nothing else is required — the platform runs on its own native AI fabric out of the box
- Optional: an Anthropic/OpenAI API key or [Ollama](https://ollama.com) (`ollama pull llama3.2`)
  for richer external-model output — never a dependency

### 1. Clone

```bash
git clone https://github.com/Rehan719/Workstation.git
cd Workstation
```

### 2. Configure environment

```bash
cp .env.example .env
# Optional: set ANTHROPIC_API_KEY / OPENAI_API_KEY for external-model output.
# Leave unset to run fully in-house on the native fabric.
```

### 3. Backend

```bash
pip install -r requirements.txt
uvicorn agentic_core.app_mvp:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 4. Frontend

```bash
cd apps/workstation-superapp
npm install
npm run dev
```

App: http://localhost:5173

### 5. Verify it works

1. Open http://localhost:5173
2. Navigate to **Enterprise** realm
3. Click **Create Enterprise Project** → fill in title, click Save
4. Click **Run** on your project → a real AI document streams in (~20–40 seconds)
5. Click **Download** → `.txt` deliverable saved locally

Or go straight to `/factory` → New Production Line → Business Model → Produce.

## Deploy

**Frontend → Vercel**

```bash
cd apps/workstation-superapp
# IMPORTANT: set your backend URL in apps/workstation-superapp/vercel.json — the
# `/api/(.*)` rewrite destination. Vercel does NOT interpolate env vars in rewrites,
# so it must be a literal URL. It currently defaults to the Render service
# (https://workstation-api.onrender.com); change it to your actual backend URL.
# (In local dev the Vite proxy handles /api → :8000; this rewrite is prod-only.)
vercel deploy
```

**Backend → Render**

`render.yaml` is committed. Connect the repo in Render dashboard; set `ANTHROPIC_API_KEY` in environment variables.

## Architecture

```
agentic_core/          — FastAPI backend (the real code)
  app_mvp.py           — entrypoint; 466 routes, boots clean
  ai/                  — the NATIVE fabric: owned models, orchestration, swarm, memory, homeostasis
  ai/gateway.py        — in-house-first routing (native fabric → optional external providers)
  gaas/v5/             — constitutional interceptor engine + hash-chained UEG audit log
  organism/            — biomimetic systems: nervous, immune, self-healing, ATP,
                         heartbeat (continuous circadian autonomy)
  projects/api.py      — Project CRUD + SSE AI workflow + lifecycle
  api/genesis.py       — Concept → Design → Commercialisation journey orchestrator
  api/board.py         — Board of Directors (Chief = owner's digital twin, above the AI CEO)
  api/economy.py       — living VSB economic metabolism (virtual/simulated currency only)
  api/transformation.py — live vision → realisation → transformation engine
  api/forge.py · api/resource_fabric.py — digital-resource pipelines + reconfigurable resource fabric
  api/integration_surface.py — federates 18 frontend endpoints to real backend data
  synthesis/ · api/intelligence.py — multi-format synthesis + cognitive/MJM/Nexus engines

apps/workstation-superapp/  — Vite + React 18 + TypeScript frontend
  src/App.tsx          — 140+ routes (64 verified operational end-to-end)
  src/pages/           — Enterprise, Learner, Developer, Scholar realms
                         + domain hubs + all product pages
```

> Verified in CI on every push: backend boots clean; **≈295 integration tests passing / 15 skipped** (last CI-green full run; grows every round); production
> build (`tsc && vite build`) succeeds.

Data persists under `data/` as atomically-written JSON files.

## AI resources (in-house first)

Workstation's ★ critical mandate is that its AI is its **own reconfigurable resource** — models,
orchestration, and swarm are native, not API wrappers. The gateway routes:
1. **Native fabric** — owned models + the structured engine; always available, honest provenance
   (`served_by` on every response)
2. **External providers** (optional, labelled `is_external`) — Anthropic / OpenAI when a key is
   set, Ollama when running — enrichment, never a dependency

## Roadmap

The live, authoritative roadmap is the **Living Plan** (`docs/WORKSTATION_IDBO_LIVING_PLAN.md`,
served at `GET /api/v1/plan`) and **`docs/AUTONOMOUS_PROGRESS.md`** (the cycle-by-cycle log; the
older `ACTION_PLAN.md` is archived under `_archive/docs/`); cycle-by-cycle progress is in
**`docs/AUTONOMOUS_PROGRESS.md`**. Summary:

**Phase 1 — ✅ done**: authentication (opt-in JWT, resilient crypto imports), integration test
suite (≈295 passing at the last CI-green run), clean boot verified, frontend↔backend integration (all 18 previously-broken
endpoints wired), production build verified + code-split.

**Phase 2 — in progress (non-gated)**: deeper domain-specific AI depth across Realm × Domain,
broader test coverage, data-fidelity + operational hardening, SQLite/Postgres persistence.

**Phase 3 — ⛔ Owner-gated (launch/commercial)**: real-money rails (Stripe — virtual/simulated
until directed), production deployment hardening, live AI key in the running environment.

---

*Previous session documentation has been moved to `/archive`.*
