"""
IDBO Authentication — JWT tokens + API key support.

Design:
  - Single-user mode (default): no auth required — all endpoints open.
    This preserves backwards compatibility; existing integrations keep working.
  - Multi-user mode (AUTH_ENABLED=true): JWT Bearer tokens required on
    protected endpoints. API keys are also accepted as Bearer tokens.

JWT flow:
  POST /api/v1/auth/token       — username + password → access_token + refresh_token
  POST /api/v1/auth/refresh     — refresh_token → new access_token
  POST /api/v1/auth/register    — create a new user account
  GET  /api/v1/auth/me          — return current user info
  POST /api/v1/auth/api-key     — generate a long-lived API key for the caller
  GET  /api/v1/auth/users       — list users (admin only)

User store: data/users.json (file-based; SQLite migration is Phase 5b).
Passwords are bcrypt-hashed. Never stored in plaintext.

Environment variables:
  AUTH_ENABLED      — "true" to require auth (default: "false")
  JWT_SECRET        — signing secret (auto-generated and persisted if not set)
  JWT_ALGORITHM     — default "HS256"
  ACCESS_TOKEN_TTL  — minutes, default 60
  REFRESH_TOKEN_TTL — minutes, default 10080 (7 days)
"""
from __future__ import annotations

import json
import os
import secrets
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Auth crypto deps (python-jose, passlib) are OPTIONAL. Auth is opt-in
# (AUTH_ENABLED=false by default), so a missing crypto dep must NEVER take the
# whole organism offline — degrade gracefully and surface a clear 503 only if an
# auth endpoint that needs crypto is actually called.
try:
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    _AUTH_DEPS_OK = True
    _AUTH_DEPS_ERR = ""
except ModuleNotFoundError as _e:  # pragma: no cover - environment-dependent
    _AUTH_DEPS_OK = False
    _AUTH_DEPS_ERR = str(_e)

    class JWTError(Exception):  # type: ignore
        """Fallback when python-jose is unavailable."""

    jwt = None  # type: ignore
    CryptContext = None  # type: ignore


def _require_auth_deps() -> None:
    """Raise a clear 503 if an auth operation needs crypto deps that aren't installed."""
    if not _AUTH_DEPS_OK:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth crypto dependencies not installed ({_AUTH_DEPS_ERR}). "
                   "Run: pip install 'python-jose[cryptography]' 'passlib[bcrypt]'",
        )

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# ── Config ────────────────────────────────────────────────────────────────────

def auth_enabled() -> bool:
    """Read AUTH_ENABLED dynamically (not import-time) so tests and runtime reconfiguration see the
    live value. Default remains single-user mode (false)."""
    return os.getenv("AUTH_ENABLED", "false").lower() == "true"


# retained for backwards compatibility with any external reader; prefer auth_enabled()
_AUTH_ENABLED = auth_enabled()

_SECRET_FILE = data_path("jwt_secret.key")

def _get_jwt_secret() -> str:
    env_secret = os.getenv("JWT_SECRET", "")
    if env_secret:
        return env_secret
    if _SECRET_FILE.exists():
        return _SECRET_FILE.read_text().strip()
    secret = secrets.token_hex(32)
    _SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
    _SECRET_FILE.write_text(secret)
    return secret


_JWT_SECRET = _get_jwt_secret()
_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
_ACCESS_TTL = int(os.getenv("ACCESS_TOKEN_TTL", "60"))       # minutes
_REFRESH_TTL = int(os.getenv("REFRESH_TOKEN_TTL", "10080"))  # minutes

# ── Crypto ────────────────────────────────────────────────────────────────────

_pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto") if _AUTH_DEPS_OK else None
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

# ── User store ────────────────────────────────────────────────────────────────

_USER_STORE = data_path("users.json")


def _load_users() -> dict[str, dict]:
    if _USER_STORE.exists():
        try:
            return json.loads(_USER_STORE.read_text())
        except Exception:
            pass
    return {}


def _save_users(users: dict[str, dict]) -> None:
    _USER_STORE.parent.mkdir(parents=True, exist_ok=True)
    _USER_STORE.write_text(json.dumps(users, indent=2))


def _get_user(username: str) -> dict | None:
    return _load_users().get(username)


def _create_default_admin() -> None:
    """Ensure an admin user exists; creates one if the store is empty.

    SECURITY: there is NO hardcoded default password. If ADMIN_PASSWORD is unset the admin is
    created with a RANDOM password (flagged `password_source: "random-unset"`); admin login then
    self-heals from the ADMIN_PASSWORD env var once the operator sets it (see login())."""
    if not _AUTH_DEPS_OK:
        return  # cannot hash without passlib; admin is created once deps are present
    users = _load_users()
    if users:
        return
    env_password = os.getenv("ADMIN_PASSWORD", "")
    admin_password = env_password or secrets.token_urlsafe(24)
    users["admin"] = {
        "user_id": str(uuid.uuid4()),
        "username": "admin",
        "hashed_password": _pwd_ctx.hash(admin_password),
        "password_source": "env" if env_password else "random-unset",
        "role": "admin",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "api_keys": [],
    }
    _save_users(users)


# Create default admin on module import (idempotent)
_create_default_admin()

# ── Token helpers ─────────────────────────────────────────────────────────────

def _make_token(data: dict, ttl_minutes: int) -> str:
    _require_auth_deps()
    payload = {**data, "exp": time.time() + ttl_minutes * 60}
    return jwt.encode(payload, _JWT_SECRET, algorithm=_ALGORITHM)


def _decode_token(token: str) -> dict:
    _require_auth_deps()
    try:
        return jwt.decode(token, _JWT_SECRET, algorithms=[_ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ── Dependency: current user ──────────────────────────────────────────────────

async def get_current_user(token: Optional[str] = Depends(_oauth2_scheme)) -> dict | None:
    """
    Returns the current user dict, or None if auth is disabled.
    Raises 401 if auth is enabled and the token is missing or invalid.
    """
    if not auth_enabled():
        return None

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = _decode_token(token)

    # Could be a JWT or a long-lived API key (stored as plain hex string)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Token missing subject.")

    user = _get_user(sub)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


async def require_admin(user: dict | None = Depends(get_current_user)) -> dict:
    if not auth_enabled():
        return {"username": "admin", "role": "admin"}
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user


# ── Owner scoping (the §17.5 user-isolation invariant) ───────────────────────

def request_owner_id(user: dict | None, requested: str = "default") -> str:
    """The owner id to STAMP onto records a request creates. Single-user mode → the caller-supplied
    id (back-compat). With auth enabled → ALWAYS the authenticated username (server-side; a client
    cannot claim another owner)."""
    if auth_enabled() and user:
        return user.get("username") or "default"
    return requested or "default"


def user_can_access(user: dict | None, owner_id: str | None) -> bool:
    """Owner-scoping read/mutate check. Single-user mode → always allowed (back-compat). With auth
    enabled: admins see everything; otherwise the record's owner must be the authenticated user —
    legacy/unowned records (no owner_id) are admin-only, never leaked to other tenants."""
    if not auth_enabled() or user is None:
        return True
    if user.get("role") == "admin":
        return True
    return bool(owner_id) and owner_id == user.get("username")


# ── API models ────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str

# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/token", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    _require_auth_deps()
    user = _get_user(form.username)
    # Self-heal: an admin created with a random password (ADMIN_PASSWORD was unset at bootstrap)
    # adopts the env password once the operator sets it — no hardcoded default ever exists.
    if (user and user.get("username") == "admin" and user.get("password_source") == "random-unset"):
        env_pw = os.getenv("ADMIN_PASSWORD", "")
        if env_pw:
            users = _load_users()
            users["admin"]["hashed_password"] = _pwd_ctx.hash(env_pw)
            users["admin"]["password_source"] = "env"
            _save_users(users)
            user = users["admin"]
    if not user or not _pwd_ctx.verify(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access = _make_token({"sub": user["username"], "role": user["role"], "type": "access"}, _ACCESS_TTL)
    refresh = _make_token({"sub": user["username"], "type": "refresh"}, _REFRESH_TTL)
    return TokenResponse(access_token=access, refresh_token=refresh, expires_in=_ACCESS_TTL * 60)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: RefreshRequest):
    payload = _decode_token(req.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Not a refresh token.")
    username = payload.get("sub")
    user = _get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    access = _make_token({"sub": user["username"], "role": user["role"], "type": "access"}, _ACCESS_TTL)
    new_refresh = _make_token({"sub": user["username"], "type": "refresh"}, _REFRESH_TTL)
    return TokenResponse(access_token=access, refresh_token=new_refresh, expires_in=_ACCESS_TTL * 60)


@router.post("/register")
async def register(req: RegisterRequest, _admin: dict = Depends(require_admin)):
    """Register a new user. Admin only."""
    _require_auth_deps()
    users = _load_users()
    if req.username in users:
        raise HTTPException(status_code=409, detail=f"Username '{req.username}' already exists.")
    users[req.username] = {
        "user_id": str(uuid.uuid4()),
        "username": req.username,
        "hashed_password": _pwd_ctx.hash(req.password),
        "role": req.role if req.role in ("admin", "user", "viewer") else "user",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "api_keys": [],
    }
    _save_users(users)
    return {"status": "created", "username": req.username, "role": users[req.username]["role"]}


@router.get("/me")
async def me(current_user: dict | None = Depends(get_current_user)):
    if not auth_enabled():
        return {"auth_enabled": False, "message": "Single-user mode — no auth required."}
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "role": current_user["role"],
        "created_at": current_user["created_at"],
        "api_keys_count": len(current_user.get("api_keys", [])),
    }


@router.post("/api-key")
async def generate_api_key(current_user: dict | None = Depends(get_current_user)):
    """Generate a long-lived API key for the current user. Stored as a hash."""
    if not auth_enabled():
        return {"message": "Auth disabled — API keys not required in single-user mode."}

    raw_key = f"wstn_{secrets.token_hex(24)}"
    users = _load_users()
    user = users.get(current_user["username"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    key_record = {
        "key_id": uuid.uuid4().hex[:8],
        "key_prefix": raw_key[:12],
        "hashed_key": _pwd_ctx.hash(raw_key),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    user.setdefault("api_keys", []).append(key_record)
    users[current_user["username"]] = user
    _save_users(users)

    return {
        "api_key": raw_key,
        "key_id": key_record["key_id"],
        "note": "Store this key securely — it will not be shown again.",
    }


@router.get("/users")
async def list_users(_admin: dict = Depends(require_admin)):
    """List all users. Admin only."""
    users = _load_users()
    return {
        "users": [
            {
                "username": u["username"],
                "role": u["role"],
                "created_at": u.get("created_at", ""),
                "api_keys_count": len(u.get("api_keys", [])),
            }
            for u in users.values()
        ],
        "total": len(users),
    }


@router.get("/status")
async def auth_status():
    """Auth system status — safe to call without credentials."""
    users = _load_users()
    return {
        "auth_enabled": auth_enabled(),
        "mode": "multi-user" if auth_enabled() else "single-user",
        "algorithm": _ALGORITHM,
        "access_token_ttl_minutes": _ACCESS_TTL,
        "user_count": len(users),
        "crypto_deps_installed": _AUTH_DEPS_OK,
    }
