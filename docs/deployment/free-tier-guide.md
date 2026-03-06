# QEP Zero-Cost Deployment Guide

## 🚀 Free-Tier Architecture

To fulfill the mission while maintaining a **No Incurred Costs Policy**, the following architecture is utilized:

### 1. Frontend Hosting: Vercel (Free Tier)
- **Domain**: `qep-sanctuary.vercel.app`
- **Features**: Automatic CI/CD via GitHub, Global Edge Network, SSL included.

### 2. Backend Hosting: Render or Fly.io (Free Tier)
- **Engine**: Dockerized Python (FastAPI).
- **Features**: Free web service instances with automatic sleep/wake cycles.

### 3. Database: Supabase (Free Tier)
- **Engine**: Managed PostgreSQL.
- **Quota**: 500MB storage, 5GB bandwidth.
- **Local Fallback**: SQLite (WAL mode) is used for local development and edge processing.

### 4. Continuous Integration: GitHub Actions
- **Free Quota**: 2000 minutes/month for private repos.
- **Workflows**: `ci.yml`, `release.yml`.

### 5. Media & Assets
- **Images/Patterns**: Embedded SVGs to minimize external requests.
- **Audio**: Cloudinary Free Tier or GitHub LFS.

---
*Status: Verified and Operational.*
