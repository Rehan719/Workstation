"""
IDBO Authentication — JWT tokens + API key support.

Design:
  - Single-user mode (default): no auth required — all endpoints open.
    This preserves backwards compatibility; existing integrations keep working.
  - Multi-user mode (AUTH_ENABLED=true): JWT Bearer tokens required on
    protected endpoints. An issued API key is accepted as the Bearer value: it is found by its
    stored prefix and admitted only when its stored hash verifies (W683). A key does not expire; its owner
    can revoke it, and a revoked key admits nobody.

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

import contextlib
import json
import os
import secrets
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
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
    """W369 — ATOMIC write. This was a plain write_text: two concurrent writers left the users file
    truncated mid-JSON, and because _load_users() tolerates a decode error by returning {}, a torn
    write silently emptied the entire account store (and would let the admin bootstrap mint a fresh
    admin). Reproduced: 20 concurrent registrations -> JSONDecodeError, all accounts gone.
    Deliberately does NOT take store_lock — callers hold it around the read-modify-write, and
    store_lock is not reentrant."""
    from agentic_core.config import atomic_write_json
    _USER_STORE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(_USER_STORE, users)


@contextlib.contextmanager
def _users_mutation():
    """W369 — serialise a users read-modify-write across threads AND processes. Without it two
    concurrent registrations each loaded the same dict and wrote back their own copy, so one
    account was silently discarded."""
    from agentic_core.config import store_lock
    try:
        with store_lock(_USER_STORE):
            yield
    except TimeoutError:
        # Identity writes must never be silently dropped: surface it rather than pretend success.
        raise HTTPException(status_code=503,
                            detail="User store busy — please retry.") from None


def _get_user(username: str) -> dict | None:
    return _load_users().get(username)


def _create_default_admin() -> None:
    """Ensure an admin user exists; creates one if the store is empty.

    SECURITY: there is NO hardcoded default password. If ADMIN_PASSWORD is unset the admin is
    created with a RANDOM password (flagged `password_source: "random-unset"`); admin login then
    self-heals from the ADMIN_PASSWORD env var once the operator sets it (see login())."""
    if not _AUTH_DEPS_OK:
        return  # cannot hash without passlib; admin is created once deps are present
    with _users_mutation():                      # W369
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

API_KEY_MARK = "wstn_"
API_KEY_PREFIX_LEN = 12          # what `generate_api_key` stores as `key_prefix`


def _user_for_api_key(raw_key: str) -> dict | None:
    """The user an issued key belongs to, or None. The stored prefix only FINDS candidates; the stored hash is
    what admits. Every candidate is verified, so two keys sharing a prefix cannot admit the wrong person."""
    _require_auth_deps()
    prefix = raw_key[:API_KEY_PREFIX_LEN]
    for user in _load_users().values():
        for rec in (user.get("api_keys") or []):
            if not isinstance(rec, dict) or rec.get("key_prefix") != prefix or rec.get("revoked"):
                continue
            try:
                if _pwd_ctx.verify(raw_key, rec.get("hashed_key") or ""):
                    return user
            except Exception:          # noqa: BLE001 - an unreadable stored hash admits nobody
                continue
    return None


READ_ONLY_ROLE = "viewer"
READING_METHODS = ("GET", "HEAD", "OPTIONS")


def _refuse_a_write_by_a_reader(user: dict, request) -> None:
    """THE READ-ONLY ROLE, AT THE FLOOR. Every route that asks who is calling passes through the caller
    dependency, so the refusal lives here and no route has to remember it. A reader may read; anything that is
    not a reading method is refused before the handler runs. It covers exactly the routes that ask - which the
    perimeter check keeps at every route that is not declared public."""
    if request is None or not isinstance(user, dict) or user.get("role") != READ_ONLY_ROLE:
        return
    if str(getattr(request, "method", "GET")).upper() not in READING_METHODS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=(
            "This account can read and cannot change anything: its role is read-only."))


async def get_current_user(token: Optional[str] = Depends(_oauth2_scheme), request: Request = None) -> dict | None:
    """
    Returns the current user dict, or None if auth is disabled.
    Raises 401 if auth is enabled and the token is missing or invalid.
    `request` is supplied by the framework on a real request; a direct call from code passes none, and then
    there is no method to judge and nothing is refused here.
    """
    if not auth_enabled():
        return None

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #  AN ISSUED KEY AUTHENTICATES (the Owner's ruling for the readiness round). It has its own shape, so a
    #  signed token never reaches this branch and a key never reaches the token decoder.
    if token.startswith(API_KEY_MARK):
        user = _user_for_api_key(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key not recognised.",
                                headers={"WWW-Authenticate": "Bearer"})
        _refuse_a_write_by_a_reader(user, request)
        return user

    payload = _decode_token(token)

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Token missing subject.")

    user = _get_user(sub)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    _refuse_a_write_by_a_reader(user, request)
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


def entity_owner_stamp(user: dict | None, requested: str | None = None) -> dict:
    """W753 (FU-1048; the Owner's ruling of 2026-10-14) - THE OWNER A NEW ENTITY RECORD CARRIES, and how it was
    decided: {"owner_id", "owner_stamped": True, "owner_stamp_basis"}, written onto the record by every door that
    makes an entity. With sign-in on nothing changes: request_owner_id's stamp, the signed-in person. With it off,
    an owner the request named is kept (the suite names its own, which the quarantine rule reads), and a request
    that named none, or sent the old single-user label, gets the configured single-user owner, never the label.
    ENTITY DOORS ONLY: profiles and workspaces keep calling request_owner_id, so the Owner's saved profile stays
    under the key it has always had."""
    from agentic_core.config import SINGLE_USER_LABEL, single_user_owner
    named = str(requested or "").strip()
    if auth_enabled():
        return {"owner_id": request_owner_id(user, named or SINGLE_USER_LABEL), "owner_stamped": True,
                "owner_stamp_basis": ("the signed-in person who made it" if user else
                                      "sign-in is on and no person was on this call, so the owner the request "
                                      "carried (the old label when it carried none)")}
    if named and named != SINGLE_USER_LABEL:
        return {"owner_id": named, "owner_stamped": True,
                "owner_stamp_basis": "named by the request that made it (sign-in is off)"}
    so = single_user_owner()
    return {"owner_id": so["owner_id"], "owner_stamped": True, "owner_stamp_basis": so["basis"]}


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

#  W865 (FU-1089) - A LIMIT ON ATTEMPTS. A failed sign-in counts against the name tried and the address it came from;
#  past either limit within the window the next attempt is answered 429, before any password is checked. Signup counts
#  the accounts created from an address. Kept in this process's memory: a restart clears the counts and each worker counts its own. The address
#  is the connection's peer: a forwarded-for header is not trusted, because anyone can write one.
SIGNIN_FAILS_PER_NAME = 5
SIGNIN_FAILS_PER_ADDRESS = 20
SIGNUPS_PER_ADDRESS = 5
ATTEMPT_WINDOW_S = 15 * 60
_ATTEMPTS: dict = {}


def _attempt_address(request: Request | None) -> str:
    return str(getattr(getattr(request, "client", None), "host", None) or "unknown")


def _attempt_wait(key: str, limit: int) -> int:
    """Seconds until `key` may try again, or 0 when it is under its limit within the window."""
    now = time.monotonic()
    stamps = [t for t in _ATTEMPTS.get(key, []) if now - t < ATTEMPT_WINDOW_S]
    _ATTEMPTS[key] = stamps
    if len(stamps) < limit:
        return 0
    return max(1, int(ATTEMPT_WINDOW_S - (now - stamps[-limit])) + 1)


def _attempt_count(key: str) -> None:
    _ATTEMPTS.setdefault(key, []).append(time.monotonic())


def _too_many(what: str, wait: int) -> HTTPException:
    return HTTPException(status_code=429, headers={"Retry-After": str(wait)}, detail=(
        f"Too many {what}: try again in {wait} second(s). Nothing was checked or created. The count is kept "
        f"for {ATTEMPT_WINDOW_S // 60} minutes."))


@router.post("/token", response_model=TokenResponse)
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    _require_auth_deps()
    _name865 = "signin:name:" + " ".join(str(form.username or "").split()).casefold()
    _addr865 = "signin:addr:" + _attempt_address(request)
    _wait865 = (_attempt_wait(_name865, SIGNIN_FAILS_PER_NAME)
                or _attempt_wait(_addr865, SIGNIN_FAILS_PER_ADDRESS))
    if _wait865:
        raise _too_many("failed sign-ins for this name or from this address", _wait865)
    user = _get_user(form.username)
    # Self-heal: an admin created with a random password (ADMIN_PASSWORD was unset at bootstrap)
    # adopts the env password once the operator sets it — no hardcoded default ever exists.
    if (user and user.get("username") == "admin" and user.get("password_source") == "random-unset"):
        env_pw = os.getenv("ADMIN_PASSWORD", "")
        if env_pw:
            with _users_mutation():                      # W369
                users = _load_users()
                users["admin"]["hashed_password"] = _pwd_ctx.hash(env_pw)
                users["admin"]["password_source"] = "env"
                _save_users(users)
                user = users["admin"]
    if not user or not _pwd_ctx.verify(form.password, user["hashed_password"]):
        _attempt_count(_name865)
        _attempt_count(_addr865)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _ATTEMPTS.pop(_name865, None)                 # W865 - a successful sign-in clears its name's count
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


#  W864 (FU-1152) - NAMES NO PERSON MAY HOLD. Records made while sign-in was off are owned under the label 'default'
#  (older ones) or the configured single-user owner (W753), and user_can_access compares a record's owner with the
#  username: an account under either name would be shown every such record. The label is refused at register and
#  signup; the configured owner's name is refused at signup and allowed only at the admin register route, where the
#  Owner creates their own account.
def _reserved_name_refusal(username: str, *, admin_register: bool) -> str | None:
    from agentic_core.config import SINGLE_USER_LABEL, single_user_owner
    name = " ".join(str(username or "").split()).casefold()
    if name == SINGLE_USER_LABEL.casefold():
        return (f"'{SINGLE_USER_LABEL}' is the label records made while sign-in was off carry, so an account under it "
                f"would be shown every one of them: it cannot be an account's name. Nothing was created.")
    owner = str(single_user_owner().get("owner_id") or "").casefold()
    if not admin_register and owner and name == owner:
        return ("that is the name records made while sign-in was off are owned under (this deployment's single-user "
                "owner), so an account under it would be shown every one of them. Only the Owner's own account, "
                "created by an admin, may hold it. Nothing was created.")
    return None


@router.post("/register")
async def register(req: RegisterRequest, _admin: dict = Depends(require_admin)):
    """Register a new user. Admin only."""
    _require_auth_deps()
    _why864 = _reserved_name_refusal(req.username, admin_register=True)
    if _why864:
        raise HTTPException(status_code=409, detail=_why864)
    with _users_mutation():                      # W369
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


def self_serve_signup_enabled() -> bool:
    """§14 (W297) — self-serve signup is an OWNER POLICY, not a default: the mechanism exists,
    the switch stays with the Owner (SELF_SERVE_SIGNUP_ENABLED=true). Off by default."""
    return os.getenv("SELF_SERVE_SIGNUP_ENABLED", "false").lower() == "true"


@router.get("/config")
async def auth_config():
    """The auth surface's honest public configuration — what the front door may truthfully offer.
    (No secrets: just which modes are on, so the UI never renders signup theatre.)"""
    return {"auth_enabled": auth_enabled(),
            "self_serve_signup_enabled": self_serve_signup_enabled(),
            "registration": ("self-serve (Owner-enabled)" if self_serve_signup_enabled()
                             else "Owner-curated (admin creates accounts)")}


class SignupRequest(BaseModel):
    username: str
    password: str


@router.post("/signup")
async def self_serve_signup(req: SignupRequest, request: Request = None):
    """§14 (W297) — PUBLIC self-serve signup, active ONLY when the Owner enables
    SELF_SERVE_SIGNUP_ENABLED (403 otherwise — never silently open). Always creates role 'user'
    (self-serve can never mint admins); auth must also be enabled for signup to be meaningful."""
    if not auth_enabled():
        raise HTTPException(status_code=409,
                            detail="Auth is disabled (single-user mode) — signup is meaningless until "
                                   "the Owner enables AUTH_ENABLED.")
    if not self_serve_signup_enabled():
        raise HTTPException(status_code=403,
                            detail="Self-serve signup is not enabled — accounts are Owner-curated. "
                                   "Ask the Owner for access.")
    _require_auth_deps()
    #  W865 (FU-1089) - signup counts the accounts created from an address: mass creation is what a limit stops
    _addr_su865 = "signup:addr:" + _attempt_address(request)
    _wait_su865 = _attempt_wait(_addr_su865, SIGNUPS_PER_ADDRESS)
    if _wait_su865:
        raise _too_many("accounts created from this address", _wait_su865)
    if len(req.username.strip()) < 3 or len(req.password) < 8:
        raise HTTPException(status_code=422,
                            detail="Username must be ≥3 chars and password ≥8 chars.")
    _why864 = _reserved_name_refusal(req.username, admin_register=False)
    if _why864:
        raise HTTPException(status_code=409, detail=_why864)
    with _users_mutation():                      # W369
        users = _load_users()
        if req.username in users:
            raise HTTPException(status_code=409, detail=f"Username '{req.username}' already exists.")
        users[req.username] = {
            "user_id": str(uuid.uuid4()),
            "username": req.username.strip(),
            "hashed_password": _pwd_ctx.hash(req.password),
            "role": "user",                     # NEVER admin via self-serve
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "api_keys": [],
        }
        _save_users(users)
    _attempt_count(_addr_su865)                  # W865 - an account was created from this address
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "auth.self_serve_signup", "username": req.username.strip()})
    except Exception:
        pass
    return {"status": "created", "username": req.username.strip(), "role": "user"}


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

    raw_key = f"{API_KEY_MARK}{secrets.token_hex(24)}"
    with _users_mutation():                      # W369
        users = _load_users()
        user = users.get(current_user["username"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        key_record = {
            "key_id": uuid.uuid4().hex[:8],
            "key_prefix": raw_key[:API_KEY_PREFIX_LEN],
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
        "accepted": True,
        "accepted_basis": ("send it as the bearer value. It is accepted wherever a signed token is, as the same "
                           "person with the same role; it does not expire. Revoke it with DELETE /api/v1/auth/api-key/{key_id}."),
    }


@router.delete("/api-key/{key_id}")
async def revoke_api_key(key_id: str, current_user: dict | None = Depends(get_current_user)):
    """Revoke one of the caller's OWN keys. The record is kept and marked, so the key's history stays readable;
    a revoked key admits nobody from that moment."""
    if not auth_enabled():
        return {"message": "Auth disabled — API keys not required in single-user mode."}
    with _users_mutation():
        users = _load_users()
        user = users.get(current_user["username"])
        rec = next((r for r in ((user or {}).get("api_keys") or [])
                    if isinstance(r, dict) and r.get("key_id") == key_id), None)
        if rec is None:
            #  another person's key id is answered exactly as one that does not exist
            raise HTTPException(status_code=404, detail="No such key.")
        if not rec.get("revoked"):
            rec["revoked"] = True
            rec["revoked_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            users[current_user["username"]] = user
            _save_users(users)
    return {"key_id": key_id, "revoked": True, "revoked_at": rec.get("revoked_at")}


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
    """Auth system status — safe to call without credentials. It says the mode and whether the sign-in parts
    are installed; it reads no account and gives no count of them (W693)."""
    return {
        "auth_enabled": auth_enabled(),
        "mode": "multi-user" if auth_enabled() else "single-user",
        "algorithm": _ALGORITHM,
        "access_token_ttl_minutes": _ACCESS_TTL,
        "crypto_deps_installed": _AUTH_DEPS_OK,
    }
