# Workstation IDBO — backend (FastAPI). IN-HOUSE-FIRST AI: boots + fully serves with NO external key
# (the native structured engine is the always-available floor; a self-hosted Ollama model is used when
# present). External providers are OPTIONAL accelerants only (AI_ALLOW_EXTERNAL=true + a key) — never a
# dependency. Building this image incurs NO cost; running it on a paid host is the Owner's decision.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Minimal system deps (scientific/torch wheels are manylinux; curl is for the healthcheck).
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only the live, integrated backend (archived/unwired code in _archive/ and the frontend are excluded
# via .dockerignore — see docs/DEPLOYMENT.md).
COPY agentic_core ./agentic_core
COPY core ./core

# Persistent data dir — mount a volume here (or set DATA_DIR) in production so data survives redeploys.
RUN mkdir -p /app/data && useradd -m app && chown -R app:app /app
USER app

ENV DATA_DIR=/app/data \
    AI_ALLOW_EXTERNAL=false \
    ENVIRONMENT=production \
    PORT=8000

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s \
    CMD curl -fsS "http://localhost:${PORT}/health" || exit 1

CMD ["sh", "-c", "uvicorn agentic_core.app_mvp:app --host 0.0.0.0 --port ${PORT}"]
