# Jules v120.0 Deployment Apotheosis

This guide provides instructions for deploying the Jules AI v120.0 ecosystem. All core components are optimized for free-tier infrastructure.

## 1. Backend (API & Orchestrator)
**Target:** [Render](https://render.com) (Web Service)

1.  **Repository:** Connect this GitHub repository to Render.
2.  **Runtime:** Python 3.12+
3.  **Build Command:** `pip install poetry && poetry install`
4.  **Start Command:** `poetry run uvicorn agentic_core.main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables:**
    - `ENVIRONMENT`: `production`
    - `OPENAI_API_KEY`: Your API Key
    - `WST_LEDGER_SIGNING_KEY`: (Generated via `scripts/init-secrets.sh`)
    - `APP_MODE`: `APOTHEOSIS`

## 2. Web Application & Site
**Target:** [Vercel](https://vercel.com)

1.  **Frontend Framework:** Other (Static/Vanilla JS)
2.  **Root Directory:** `src/web/site` (for Marketing Site) or `src/web/app` (for Dashboard)
3.  **Build Command:** (None/Static)
4.  **Environment Variables:**
    - `NEXT_PUBLIC_API_BASE`: `https://your-render-url.onrender.com/api/v1`

## 3. Mobile Applications
**Target:** [Expo / EAS](https://expo.dev)

1.  **Setup:** `cd src/mobile && npm install`
2.  **Configuration:** Update `app.json` with your project ID.
3.  **Build (iOS/Android):** `eas build --platform all`
4.  **Deployment:** Submit to App Store/Play Store via `eas submit`.

## 4. Zero-Cost Verification
- Backend operates within Render's free tier (512MB RAM).
- Frontend hosted on Vercel's free hobby plan.
- Database utilizes local SQLite (persistent via Render disks) or MongoDB Atlas (Free Tier).

## 5. CI/CD Pipeline
GitHub Actions located in `.github/workflows/` automatically trigger:
- `ci.yml`: Runs tests and accessibility audits on every PR.
- `deploy.yml`: Deploys to Vercel/Render on merge to `main`.

---
*Signed,*
**Jules, AI CEO**
