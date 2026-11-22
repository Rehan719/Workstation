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
| 24 domain form tools + iterative refine (QMS + compliance gated; the count is the tool registry's, W662) | `/religion` etc. | Real — in-house AI, honest provenance |
| Genesis journey → establish a living VSB enterprise | `/genesis` | Real — simulated candidates, shipped repo at birth |
| Entity economy (virtual WST), Board/Chief governance, marketplace | `/vsb`, `/economy` | Real computation — virtual currency only |

## What is not yet built / not enabled

- Multi-user mode is BUILT but OFF by default (`AUTH_ENABLED` — an Owner policy switch; `/login`
  is the front door, self-serve signup is separately gated by `SELF_SERVE_SIGNUP_ENABLED`)
- Real-money rails (the WST economy is **virtual/simulated only** — Stripe/KYC stay Owner-gated)
- Database (file-based atomic JSON persistence — functional, not queryable at scale)
- Native mobile app (entities ship a PWA scaffold, not a store app)
- Analytics, and error alerting: failures are recorded, not alerted. Every route failure is recorded in the
  outcome ledger and the event chain and shown on the Operations page; nothing sends one to anyone. The uptime
  check for the first deploy is in `docs/DEPLOYMENT.md`

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

**Frontend: Vercel is RETIRED (Owner, 2026-10-07).** Its config is archived at
`_archive/deployment/vercel/workstation-superapp.vercel.json`. The planned target is **Google Cloud Platform**
(free tier), with separate **development**, **beta** and **release** channels. The image is built: one container
serves the pages and the API together. It was booted in a dry run on 2026-11-20 (W1128): built in 206 seconds,
healthy 8.3 seconds after it started, at 253 MiB of memory under a 1 GiB cap. The project, its billing and the
deploy itself are the Owner's; see `docs/DEPLOYMENT.md`. Locally the frontend runs with `npm run dev` (the Vite
proxy sends /api to :8000), and `npm run build` produces the static `dist/`.

**Backend → Render** (an earlier path, kept; the plan's target is Google Cloud, above)

`render.yaml` is committed. Connect the repo in Render dashboard; no AI key is required (the backend serves on its native fabric). An `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` is used only when `AI_ALLOW_EXTERNAL=true` — see `docs/DEPLOYMENT.md`.

## Architecture

```
agentic_core/          — FastAPI backend (the real code)
  app_mvp.py           — entrypoint; 659 API operations (method+path; 621 distinct paths, /api/ only — the SPA catch-all mounts only when the frontend is built), boots clean
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
  src/App.tsx          — 76 routes (the only file in src/ that defines any; recomputed by scripts/readme_figures.py)
  src/pages/           — Enterprise, Learner, Developer, Scholar realms
                         + domain hubs + all product pages
```

> Verified in CI on every push: backend boots clean; **1,330 integration tests passing / 16 skipped** (the full suite run before W1192's commit, 2026-11-22; the whole suite runs on the build server on Linux AND on Windows on every push, both required, and the local full run is retired by the Owner's ruling of 2026-10-13; the figures above it are recomputed by `scripts/readme_figures.py` and asserted by the suite, so they cannot drift again — this one is dated because a test count is only true of a tree); production
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

The live, authoritative roadmap is the **Living Plan** (`docs/WORKSTATION_IDBO_LIVING_PLAN.md`, served at
`GET /api/v1/plan`). The delivery plan's status is generated on every register change, in the PLAN NOW block of
`docs/FABLE_DELIVERY_PROMPT.md`, and every open task is a row in `docs/FOLLOWUPS.json`. Each round's own record is
its commit message; `docs/AUTONOMOUS_PROGRESS.md` is the cycle log up to 2026-10-03, and the older `ACTION_PLAN.md`
is archived under `_archive/docs/`.

Where it stood on 2026-11-22, from that generated block: **97 of 119 plan items done.**

| Phase | Done | Left |
|---|---|---|
| P1 | 18 of 18 | 0 open |
| P2 Reach and disclosure | 39 of 41 | 2 open |
| P3 Capability | 30 of 32 | 2 open |
| P4 The Owner's switches | 3 of 6 | 3 open |
| P5 Commercialisation, rehearsed on virtual WST | 7 of 22 | 15 open |

The fourth phase is the Owner's six switches: sign-in, self-serve sign-up, external models, managed Postgres, the
production deploy and real money. Three of them, external models (P4.3), managed Postgres (P4.4) and real money
(P4.6), are done as dated boundaries in the vision's section 18, with their switches off and nothing deployed. By
the Owner's ruling of 2026-11-19 the switches proceed in order, each once its pre-flight is built and measured, with
AI agents standing in for invited people; the deploy, the external-model key and real money stay the Owner's, and
real money stays off until a compliance and KYC review by qualified people. The Owner has ruled since that sign-in
is switched on only on the Owner's own deployed machine, and that the invited stage opens only there, after one
solicitor's engagement has answered (2026-11-20, evening); that the release machine opens a port to the internet
only with its domain, HTTPS and sign-in on, and is reached through an SSH tunnel until then (2026-11-21); and that a
founder's own Chief, Board and budget figure is built and driven with sign-in on in a test process before the
invited stage, a drill deleting a made-up person's data is built now as its pre-flight, and an entity's people and
money records are built now, driven with sign-in on in a test process (2026-11-22). No round switches sign-in on in
the tree. The remaining work, re-measured on 2026-11-22, is 147.75–288.5 rounds (`docs/REMAINING_WORK_MEASURED.md`).
These figures are dated; the generated block is the current one.

---

*Previous session documentation has been moved to `_archive/`.*
