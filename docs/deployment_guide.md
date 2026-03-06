# Jules AI: Deployment Guide (v99.0)

This guide provides instructions for deploying the Jules AI Workstation in production environments.

## 📋 Prerequisites
- Python 3.12+
- SQLite (default) or PostgreSQL
- Environment variables configured (see `.env.template`)

## 🚀 Deployment Options

### 1. Local / On-Premise Installation
```bash
git clone https://github.com/Rehan719/jules-ai.git
cd jules-ai
pip install -e .
python -m agentic_core.orchestrator.conscious_organism_v99
```

### 2. Cloud Deployment (AWS/GCP/Azure)
Jules AI supports automated deployment via the `DeploymentOrchestrator`.
- **AWS:** Uses ECS/Fargate for compute and RDS for PostgreSQL.
- **GCP:** Uses Cloud Run and Cloud SQL.
- **Managed Cloud:** Jules' internal high-fidelity hosting environment.

### 🔒 SSL Setup
SSL is automatically provisioned for all `*.jules.ai` subdomains during deployment. For custom domains, configure your certificate ARN in `config/settings.json`.

## ⚙️ Configuration
Centralized configuration is managed in `agentic_core/config/loader.py`.
Key settings:
- `JULES_DB_URL`: Database connection string.
- `JULES_JWT_SECRET`: Secret key for authentication.
- `JULES_API_PORT`: Port for the workspace API.

## 📈 Scaling
- **Horizontal Scaling:** Deploy multiple instances of the `ConsciousOrganism` behind a load balancer.
- **Collaboration Sync:** Ensure `CRDTManager` is connected to a shared Redis instance for real-time collaboration across nodes.
