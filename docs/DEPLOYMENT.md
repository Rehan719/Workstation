# Deployment Runbook — Workstation IDBO

The current architecture: **FastAPI backend on Render** + **Vite/React frontend on Vercel**. The
backend is configured by [`render.yaml`](../render.yaml); the frontend by
[`apps/workstation-superapp/vercel.json`](../apps/workstation-superapp/vercel.json), which rewrites
`/api/*` to the Render service. CI ([`.github/workflows/spine.yml`](../.github/workflows/spine.yml))
boots the backend + runs the integration suite and builds the frontend on every push.

> Older guides under `docs/deployment/`, `docs/deployment_guide.md`, and `DEPLOY_QEP.md` are kept
> for reference but this file is the current source of truth.

## AI posture — in-house-first (no external key required)

The platform runs on its **own native AI fabric** (`agentic_core/ai/native/`): an always-available
native structured-reasoning engine (the floor), plus a self-hosted local model (Ollama) when
present. **The backend boots and fully serves with no AI key at all.** External providers
(Anthropic/OpenAI) are *optional accelerants*, used only when `AI_ALLOW_EXTERNAL=true` **and** a key
is configured. Provenance (`served_by`, `is_external`) is reported throughout, and the Operational
Excellence page (`/operations`) surfaces the in-house rate.

## Backend (Render)

1. Connect the repo; Render reads `render.yaml` (Blueprint) — Python web service,
   `pip install -r requirements.txt`, `uvicorn agentic_core.app_mvp:app`, health check `/health`.
2. Set env vars (most have safe defaults in `render.yaml`):

   | Var | Default | Notes |
   |-----|---------|-------|
   | `AI_ALLOW_EXTERNAL` | `false` | Keep `false` for pure in-house. Set `true` only to allow external accelerants. |
   | `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | unset | Optional. Only used when `AI_ALLOW_EXTERNAL=true`. OpenAI also enables avatar voice/vision. |
   | `OLLAMA_URL` | unset | Optional self-hosted model; absent → native floor. |
   | `AI_DISABLE_LOCAL` | unset | Set `1` to skip the local model and always use the native floor (fast/deterministic). |
   | `CORS_ORIGINS` | — | Your frontend origin(s), e.g. `https://<app>.vercel.app`. |
   | `AUTH_ENABLED` / `JWT_SECRET` / `ADMIN_PASSWORD` | `false` / auto / — | Set before a public launch. |
   | `DATA_DIR` | `data` | **All** persistent stores resolve through `config.data_path()` and honour `DATA_DIR` (locked by `test_data_dir_configurable`). Point it at a Render disk / mounted volume so data survives redeploys. Default (`data/`) is unchanged. |

3. **Payments are virtual/simulated by default and safe.** See the safety section below — do **not**
   set a live Stripe key.

## Docker / self-host (any container host) — COST-FREE by default

A production [`Dockerfile`](../Dockerfile) (+ [`.dockerignore`](../.dockerignore)) and
[`docker-compose.yml`](../docker-compose.yml) ship the **live backend only** (`_archive/`, the frontend,
and tests are excluded). In-house-first, file persistence on a local volume, no paid services:

```bash
docker compose up --build        # backend on :8000, persistent local volume — $0
```

The image runs `uvicorn agentic_core.app_mvp:app` as a non-root user with a `/health` healthcheck and
`DATA_DIR=/app/data` (mount a volume there for durable data). Optional managed Postgres is commented in
`docker-compose.yml` — enable only if/when you choose (it incurs hosting cost; the app does not require it).

## Cost summary (what is / isn't chargeable)

**$0 by default:** local/Docker run, in-house native AI + self-hosted Ollama, file persistence, Stripe
**test** mode. **Costs money only when YOU enable it on your own account:** hosting the backend
(Render/any host), a managed Postgres, an external AI key (per-token), Stripe **live** mode (real money +
fees). Nothing chargeable is triggered autonomously.

## Frontend (Vercel)

- Root: `apps/workstation-superapp` (npm workspace). Build `npm run build` → `dist` (Vite).
- `vercel.json` already rewrites `/api/(.*)` → `https://workstation-api.onrender.com/api/$1` and
  serves the SPA. If your Render URL differs, update that destination.

## Payments & money safety (READ BEFORE LAUNCH)

The payments rails (`agentic_core/api/v310/payments.py`) operate in modes
`simulation → test → live_gated → live`. **Live charges require BOTH a `sk_live_` key AND
`STRIPE_LIVE_ENABLED=true`** — otherwise the code refuses to move real money.

- Keep money **virtual/simulated**: leave `STRIPE_SECRET_KEY` unset (or a `sk_test_` test key) and
  **do not** set `STRIPE_LIVE_ENABLED`.
- ⚠️ **Security finding:** a real `sk_live_` key currently lives in the local (gitignored, untracked)
  `.env` and is auto-loaded at boot. The payments code correctly *gates* it (refuses to charge), but
  the recommendation stands: **swap the local `.env` to a `sk_test_` key.** Never commit `.env` (it
  is gitignored), never set `STRIPE_LIVE_ENABLED`, and never deploy the live key to Render.

## Verify before deploy

```bash
python -c "import agentic_core.app_mvp"                       # backend imports/boots
pytest integration_tests/test_mvp_spine.py --noconftest -q    # integration suite (AI_DISABLE_LOCAL=1 → fast)
npm --prefix apps/workstation-superapp run build              # frontend tsc + vite build
```

CI (`spine.yml`) runs the backend boot+suite and the frontend build on every push; require it green
before promoting a deploy.
