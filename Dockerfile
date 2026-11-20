# Workstation IDBO — the backend (FastAPI) and the pages it serves. IN-HOUSE-FIRST AI: boots + fully serves with NO
# external key (the native structured engine is the always-available floor; a self-hosted Ollama model is used when
# present). External providers are OPTIONAL accelerants only (AI_ALLOW_EXTERNAL=true + a key) — never a
# dependency. Building this image incurs NO cost; running it on a paid host is the Owner's decision.

# W1128 (FU-1156, P4.5's dry run) - THE PAGES, built in a stage of their own the way CI builds them: the workspace's
# install from its lock, then the app's build. The image that runs carries the built pages and no Node; the backend
# serves apps/workstation-superapp/dist when it is present (app_mvp's single-service SPA serving).
FROM node:20-slim AS pages
WORKDIR /build
COPY package.json package-lock.json ./
COPY packages ./packages
COPY apps/workstation-superapp ./apps/workstation-superapp
# onnxruntime-node (which @huggingface/transformers needs) fetches GPU binaries when it installs unless told not to;
# the pages are built for the browser and need none, and its CPU binaries ship in the package
ENV ONNXRUNTIME_NODE_INSTALL_CUDA=skip
RUN npm ci --no-audit --no-fund && npm run build --workspace=apps/workstation-superapp

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# W1128 (FU-603) - NO SYSTEM PACKAGES. Every pin the floor installs has a prebuilt Linux wheel but docopt, which
# is pure Python, so no compiler is needed; the healthcheck asks with Python rather than curl. The image keeps
# the base's own packages and adds none.

COPY requirements.txt .
# W1128 (FU-603) - THE FLOOR. The first deploy runs the floor only (OWNER RULING 2026-10-12), so the image installs
# the pinned set without the GPU learning stack: torch, torchsde, triton and their CUDA libraries. requirements.txt
# pins the whole resolved set, so --no-deps installs exactly what is listed; the three modules that use torch guard
# its import, and the platform boots without it (test_w506).
RUN grep -v -E '^(torch|torchsde|triton|nvidia-[a-z0-9-]+|cuda-[a-z0-9-]+)==' requirements.txt > requirements-floor.txt \
    && pip install --no-cache-dir --no-deps -r requirements-floor.txt

# Only the live, integrated backend (archived/unwired code in _archive/ is excluded via .dockerignore — see
# docs/DEPLOYMENT.md).
# W354 — config/ is on the import path (config.paths + config.loader are imported by ai/memory, ai/logger and ~10
# more modules app_mvp loads at boot): omitting it made the shipped image die at import. Verified by a boot-path
# import audit — every top-level package app_mvp imports at boot is in the COPY set
# (test_dockerfile_copies_every_boot_path_package). The image's own COPY list is the contract; keep it in sync.
# W883b - no `COPY core ./core`: W877 moved core/ out of the tree, and a COPY with no source fails the build. Every
# COPY source must exist (test_w883b).
# W896 (FU-1168) - no `COPY src ./src`: src/'s three live modules moved into agentic_core, the rest to _archive/.
COPY agentic_core ./agentic_core
COPY config ./config
# W1128 (FU-1156) - what the routes read besides the code: the plan, the register and the sources (docs/), the law
# corpus and the other knowledge (knowledge/), the product catalogue (products/), and the built pages.
# .dockerignore keeps every private folder out of the build context, whatever a working copy holds.
COPY docs ./docs
COPY knowledge ./knowledge
COPY products ./products
COPY --from=pages /build/apps/workstation-superapp/dist ./apps/workstation-superapp/dist

# Persistent data dir — mount a volume here (or set DATA_DIR) in production so data survives redeploys.
RUN mkdir -p /app/data && useradd -m app && chown -R app:app /app
USER app

# W1138 (FU-1287) - matplotlib keeps its font cache under /tmp, so a running image writes nothing beside the code
ENV DATA_DIR=/app/data \
    MPLCONFIGDIR=/tmp/matplotlib \
    AI_ALLOW_EXTERNAL=false \
    ENVIRONMENT=production \
    PORT=8000

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://localhost:%s/health' % os.environ.get('PORT', '8000'), timeout=4)" || exit 1

CMD ["sh", "-c", "uvicorn agentic_core.app_mvp:app --host 0.0.0.0 --port ${PORT}"]
