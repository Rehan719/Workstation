"""
Auth-enabled backend runner (§14, W297) — for live multi-user verification.

launch.json cannot inject environment variables, so this wrapper sets the auth posture
programmatically and serves the app (including the built SPA dist) on :8020:

  AUTH_ENABLED=true                 — multi-user isolation active (the W252/W295 guards enforce)
  SELF_SERVE_SIGNUP_ENABLED as-is   — signup stays whatever the Owner set (default OFF)

Run via the "Backend Auth (:8020, AUTH_ENABLED)" launch configuration or:
  venv/Scripts/python.exe scripts/run_auth_backend.py
"""
import os

os.environ.setdefault("AUTH_ENABLED", "true")

import uvicorn  # noqa: E402  (env must be set before the app imports)

if __name__ == "__main__":
    uvicorn.run("agentic_core.app_mvp:app", host="127.0.0.1", port=8020)
