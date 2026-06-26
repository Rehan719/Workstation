# QEP Zero-Cost Architecture Plan

## 1. Core Principles
- **No Incurred Costs**: Zero spending for development, hosting, or users.
- **Expert Reliability**: High availability and performance on free tiers.
- **Transparency**: Fully documented resource quotas.

## 2. Infrastructure Stack

### Frontend Hosting
- **Primary**: Vercel (Free Tier)
  - Automatic SSL, Edge Caching, CI/CD.
  - Quota: 100GB bandwidth/month (sufficient for ~500k monthly visitors with optimized assets).

### Backend Hosting
- **Primary**: Render (Free Instance) or fly.io
  - Dockerized Python API.
  - Mitigation: Use sleep/wake cycles; implement local development primary paths.

### Database Layer
- **Primary**: Supabase (Free Tier)
  - Managed PostgreSQL + Real-time.
  - Quota: 500MB storage (sufficient for ~250k user spiritual profiles).
- **Secondary**: Local SQLite (WAL mode)
  - Used for edge processing and offline-first data persistence.

### CI/CD & Automation
- **GitHub Actions** (Free Tier)
  - 2000 minutes/month.
  - Mitigation: Optimize Docker builds with multi-stage layers and caching.

### Monitoring & Observability
- **Sentry** (Developer Free Tier): Error tracking.
- **UptimeRobot** (Free): Uptime monitoring.
- **Self-Hosted Metrics**: Prometheus/Grafana simulation on local workstation.

## 3. Cost Mitigation Strategies
| Potential Cost | Risk | Mitigation |
|----------------|------|------------|
| Bandwidth | High usage of audio/video | Brotli compression, Opus codec @ 32kbps, CDN caching. |
| Database Size | Growing telemetry logs | Aggregate logs periodically; move cold data to local archival files. |
| API Fees | Commercial LLM usage | Standardize on open-source local-first models (e.g. Qwen-7B, Llama-3 via local Ollama/Llama.cpp). |

## 4. Implementation Path
1. Initialize Vercel deployment for `src/qep_frontend/`.
2. Configure GitHub Actions workflows for zero-cost build.
3. Establish Supabase schema for spiritual metrics.
