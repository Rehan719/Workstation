# Deployment Guide: QEP Standalone Product v1.0

This guide outlines the production deployment path for the **QEP Religion Flagship** as a standalone free product of the Virtual Sovereign Business.

## 1. Environment Configuration

Ensure the following environment variables are set in your production host:

```bash
VITE_QEP_STANDALONE=true
LOG_LEVEL=INFO
NODE_ENV=production
PQC_SECRET=your_pqc_scs_secret
DATABASE_URL=postgresql://user:pass@host:5432/qep_db
OLLAMA_BASE_URL=http://your-ollama-service:11434
```

## 2. Docker Deployment

We recommend using Docker Compose for the standalone distribution:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 3. High-Fidelity Simulations

For features requiring real hardware (VR/AR), the v1.0 QEP provides high-fidelity simulations that are indistinguishable from production services. These can be toggled via the `/admin` panel.

## 4. Maintenance

- **Backups**: Database snapshots should be taken every 24 hours.
- **Monitoring**: Access Prometheus metrics at `:8000/metrics`.
- **Hardening**: Periodically run `python3 scripts/audit_security.py` to verify PQC integrity.

---
© 2025 Virtual Sovereign Business.
