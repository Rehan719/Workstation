# Workstation

**AI-mediated workspace for moving ideas from concept to commercial output.**

Version: 1.0.0 | Status: MVP (Enterprise vertical working end-to-end)

---

## What it does

Workstation gives you an organised AI workspace structured as a virtual company. You enter via an AI CEO, pick a **Realm** (Enterprise · Learning · Developing · Scholarship) and a **Domain** (Religion · Science · Education · Law · Employment · Care), create a **Project**, and run it through **Products** that move it through a lifecycle:

```
Concept → Design → Build → Launch → Commercialise
```

Each Product makes a real LLM call (Anthropic Claude by default) and returns a usable deliverable — a business model, technical spec, research report, marketing plan, or pitch deck — streamed in real time, persisted, and downloadable.

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
| Domain hubs (Religion, Science, Law, etc.) | `/religion` etc. | UI exists; domain-specific AI depth varies |

## What is not yet built

- User authentication (single-user local setup only)
- Database (file-based JSON persistence — functional, not queryable at scale)
- Mobile app
- Marketing website
- Analytics / error monitoring

## Run locally

### Prerequisites

- Python 3.12+, Node 18+
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))
- Optional local fallback: [Ollama](https://ollama.com) — `ollama pull llama3.2`

### 1. Clone

```bash
git clone https://github.com/Rehan719/Workstation.git
cd Workstation
```

### 2. Configure environment

```bash
cp .env.example .env
# Open .env and set ANTHROPIC_API_KEY
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
# Set VITE_API_BASE_URL in Vercel dashboard to your backend URL
vercel deploy
```

**Backend → Render**

`render.yaml` is committed. Connect the repo in Render dashboard; set `ANTHROPIC_API_KEY` in environment variables.

## Architecture

```
agentic_core/          — FastAPI backend (the real code)
  app_mvp.py           — lean entrypoint; 21 routers, boots clean
  ai/gateway.py        — Anthropic → OpenAI → Ollama chain
  projects/api.py      — Project CRUD + SSE AI workflow + lifecycle
  api/products.py      — Factory, Reactor, Incubator (all real AI)
  api/v290/ceo_generate.py  — CEO blueprint generation
  api/csuite.py        — CFO/CTO metrics from real data
  synthesis/api.py     — multi-format document synthesis

apps/workstation-superapp/  — Vite + React 18 + TypeScript frontend
  src/App.tsx          — 100+ routes
  src/pages/           — Enterprise, Learner, Developer, Scholar realms
                         + domain hubs + all product pages
```

Data persists to `data/projects/` and `data/synthesis_outputs/` as JSON files.

## AI providers

The gateway tries providers in order:
1. **Anthropic Claude** (`claude-sonnet-4-6`) — used when `ANTHROPIC_API_KEY` is set
2. **OpenAI GPT-4o-mini** — fallback when `OPENAI_API_KEY` is set
3. **Ollama llama3.2** — local fallback if Ollama is running
4. **Labelled error response** — if nothing is available; dev still runs, never a silent fake

## Roadmap

**Phase 1** (next): authentication, SQLite persistence, one integration test per AI endpoint, clean clone boot verified

**Phase 2**: PostgreSQL, file storage for deliverables, analytics, extend domain-specific AI depth across all Realm × Domain combinations

**Phase 3**: PWA, mobile (Capacitor wrap), marketing site

---

*Previous session documentation has been moved to `/archive`.*
