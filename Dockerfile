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
# W354 — config/ and src/ are on the import path (config.paths + config.loader are imported by
# ai/memory, ai/logger and ~10 more modules app_mvp loads at boot; src/ backs the tool registry):
# omitting them made the shipped image die at import. Verified by a boot-path import audit —
# every top-level package app_mvp imports at boot is now in the COPY set (test_dockerfile_copies_
# every_boot_path_package). The image's own COPY list is the contract; keep it in sync.
COPY agentic_core ./agentic_core
COPY core ./core
COPY config ./config
COPY src ./src

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
