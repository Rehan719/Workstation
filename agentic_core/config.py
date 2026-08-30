"""
Workstation environment configuration.

Validates required env vars at startup and surfaces missing config clearly.
Provides a single source of truth for all runtime settings.

Usage:
    from agentic_core.config import settings
"""
from __future__ import annotations

import os
import warnings
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    # AI providers — at least one should be set in production
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    ollama_base_url: str = field(default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

    # Auth
    auth_enabled: bool = field(default_factory=lambda: os.getenv("AUTH_ENABLED", "false").lower() == "true")
    jwt_secret: str = field(default_factory=lambda: os.getenv("JWT_SECRET", ""))
    # SECURITY: no hardcoded default — empty means "unset"; the auth bootstrap generates a random
    # admin password and self-heals from this env var once set (agentic_core/auth/core.py).
    admin_password: str = field(default_factory=lambda: os.getenv("ADMIN_PASSWORD", ""))

    # CORS — comma-separated allowed origins; "*" allows all (dev only)
    cors_origins: list[str] = field(default_factory=lambda: [
        o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()
    ])

    # Storage
    data_dir: str = field(default_factory=lambda: os.getenv("DATA_DIR", "data"))
    projects_dir: str = field(default_factory=lambda: os.getenv("PROJECTS_DIR", "data/projects"))

    # Gateway
    gateway_rpm: int = field(default_factory=lambda: int(os.getenv("GATEWAY_RPM", "20")))
    default_model: str = field(default_factory=lambda: os.getenv("DEFAULT_MODEL", "claude-sonnet-4-6"))

    # Environment
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("production", "prod")

    @property
    def has_ai_provider(self) -> bool:
        return bool(self.anthropic_api_key or self.openai_api_key)

    def validate(self) -> list[str]:
        """Return a list of validation warnings (not errors — degraded mode is acceptable)."""
        issues = []
        if not self.has_ai_provider:
            issues.append("No AI provider configured (ANTHROPIC_API_KEY / OPENAI_API_KEY). AI features will be unavailable.")
        if self.is_production and "*" in self.cors_origins:
            issues.append("CORS is set to '*' in production. Set CORS_ORIGINS to specific frontend domains.")
        if self.is_production and not self.auth_enabled:
            issues.append("AUTH_ENABLED is false in production. Consider enabling JWT auth.")
        if self.is_production and self.auth_enabled and not self.admin_password:
            issues.append("ADMIN_PASSWORD is unset with auth enabled in production — the bootstrap "
                          "admin has a random password; set ADMIN_PASSWORD to claim it.")
        return issues


settings = Settings()


def atomic_write_json(path, data, indent: int = 2) -> None:
    """Atomic JSON write (the W241 pattern from ai/memory.py, shared): write to a temp file in the
    SAME directory, then os.replace() it in — atomic on Windows and POSIX — so a reader never
    observes a half-written file and a crash cannot truncate the live store. The heartbeat writes
    stores in the background while API handlers write the same files; bare write_text() interleaves
    and corrupts under that concurrency (the documented memory.json/UEG incident)."""
    import json as _json
    import os as _os
    import tempfile as _tempfile
    from pathlib import Path as _Path
    p = _Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = _tempfile.mkstemp(dir=str(p.parent), prefix=f".{p.name}.", suffix=".tmp")
    try:
        with _os.fdopen(fd, "w", encoding="utf-8") as f:
            _json.dump(data, f, indent=indent)
        # W348/W349 — Windows os.replace raises PermissionError under reader/writer contention
        # (a sharing violation, transient): the Round-10 concurrency audit measured 170/200
        # writes DYING on it (money-shaped loss — purchases charged-then-crashed, recognised
        # revenue destroyed). Bounded retry with backoff makes the replace robust; a persistent
        # failure still raises honestly.
        import time as _time
        for _attempt in range(12):
            try:
                _os.replace(tmp, str(p))
                break
            except PermissionError:
                if _attempt == 11:
                    raise
                _time.sleep(0.01 * (_attempt + 1))
    except Exception:
        try:
            _os.unlink(tmp)
        except OSError:
            pass
        raise


def store_lock(path, timeout_s: float = 10.0, stale_s: float = 30.0):
    """§12/§13 (W348/W349/W351) — a CROSS-PROCESS mutual-exclusion lock for a JSON store's
    load-modify-write cycle. atomic_write_json makes each WRITE atomic, but the read→modify→write
    sequence was unserialised: the Round-10 audit reproduced money-shaped losses (17 sales
    confirmed on an 11-sale balance with ONE charge; 89% of recognised revenue destroyed; 196/200
    constitutional UEG events silently lost). Usage:

        with store_lock(store_path):
            rows = load_json_tolerant(store_path, [])
            ...modify...
            atomic_write_json(store_path, rows)

    Implementation: an O_CREAT|O_EXCL lockfile beside the store (works across processes on
    Windows and POSIX), bounded wait with backoff, and stale-lock breaking (a crashed holder's
    lock older than `stale_s` is removed with a warning — liveness over strictness, honestly)."""
    import os as _os
    import time as _time
    from contextlib import contextmanager
    from pathlib import Path as _Path

    lock_path = _Path(str(path) + ".lock")

    @contextmanager
    def _ctx():
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        deadline = _time.monotonic() + timeout_s
        fd = None
        while True:
            try:
                fd = _os.open(str(lock_path), _os.O_CREAT | _os.O_EXCL | _os.O_WRONLY)
                _os.write(fd, str(_os.getpid()).encode())
                break
            except FileExistsError:
                try:   # stale-lock breaking: a crashed holder must not deadlock the store forever
                    if _time.time() - lock_path.stat().st_mtime > stale_s:
                        lock_path.unlink(missing_ok=True)
                        continue
                except OSError:
                    pass
                if _time.monotonic() > deadline:
                    raise TimeoutError(f"store_lock timeout on {lock_path.name}")
                _time.sleep(0.005)
        try:
            yield
        finally:
            try:
                _os.close(fd)
            except OSError:
                pass
            try:
                lock_path.unlink(missing_ok=True)
            except OSError:
                pass

    return _ctx()


def load_json_tolerant(path, default):
    """Corruption-tolerant JSON load: a partial/interleaved/truncated store returns the recoverable
    JSON prefix when one exists, else the caller's default — never raises into the caller (a corrupt
    cache must never take a live subsystem down; see ai/memory.py W241)."""
    import json as _json
    from pathlib import Path as _Path
    p = _Path(path)
    if not p.exists():
        return default
    try:
        return _json.loads(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return default
    except _json.JSONDecodeError:
        try:
            raw = p.read_text(encoding="utf-8", errors="replace")
            val, _ = _json.JSONDecoder().raw_decode(raw.lstrip())
            return val
        except Exception:
            return default


_STORE_THREAD_LOCKS: dict = {}
_STORE_LOCKS_GUARD = None


def _thread_lock_for(path) -> "object":
    import threading
    global _STORE_LOCKS_GUARD
    if _STORE_LOCKS_GUARD is None:
        _STORE_LOCKS_GUARD = threading.Lock()
    key = str(path)
    with _STORE_LOCKS_GUARD:
        lk = _STORE_THREAD_LOCKS.get(key)
        if lk is None:
            lk = _STORE_THREAD_LOCKS[key] = threading.RLock()
        return lk


class store_lock:
    """§12/§8 (W348/W349/W351) — a per-store CROSS-PROCESS + cross-thread lock guarding the whole
    load→modify→write critical section of a hot JSON store. The atomic_write_json primitive stops a
    reader seeing a half-written file, but does NOT stop two writers each doing load→modify→write
    and the second clobbering the first (the audit reproduced ~89% recognised-revenue loss and a
    marketplace oversell under concurrent writers). This lock serialises that section.

    In-process: a per-path threading.RLock. Cross-process (production uvicorn workers + the
    heartbeat process): an O_CREAT|O_EXCL lockfile beside the store, spin-acquired with a bounded
    timeout, released in __exit__. Honest failure: if the lockfile cannot be acquired within the
    timeout (a crashed holder left a stale file), it is broken after `stale_after` and acquired —
    logged, never a silent deadlock. Use via `with store_lock(path): ...`."""

    def __init__(self, path, timeout: float = 10.0, stale_after: float = 30.0):
        from pathlib import Path as _P
        self._store = _P(path)
        self._lockpath = self._store.with_suffix(self._store.suffix + ".lock")
        self._timeout = timeout
        self._stale_after = stale_after
        self._tlock = _thread_lock_for(path)
        self._fd = None

    def __enter__(self):
        import os as _os, time as _time
        self._tlock.acquire()
        self._store.parent.mkdir(parents=True, exist_ok=True)
        deadline = _time.monotonic() + self._timeout
        while True:
            try:
                self._fd = _os.open(str(self._lockpath), _os.O_CREAT | _os.O_EXCL | _os.O_RDWR)
                return self
            except FileExistsError:
                # a live holder — or a stale lockfile from a crashed process
                try:
                    age = _time.time() - _os.path.getmtime(str(self._lockpath))
                    if age > self._stale_after:
                        try:
                            _os.unlink(str(self._lockpath))
                        except OSError:
                            pass
                        continue
                except OSError:
                    pass
                if _time.monotonic() >= deadline:
                    # bounded — never a silent deadlock; proceed thread-serialised, log loudly
                    import logging
                    logging.getLogger("config.store_lock").warning(
                        "store_lock timeout on %s — proceeding thread-serialised only", self._lockpath)
                    return self
                _time.sleep(0.02)

    def __exit__(self, *exc):
        import os as _os
        try:
            if self._fd is not None:
                _os.close(self._fd)
                try:
                    _os.unlink(str(self._lockpath))
                except OSError:
                    pass
        finally:
            self._fd = None
            self._tlock.release()
        return False


def mutate_json(path, mutator, default):
    """§12 (W349) — the atomic read-modify-write a hot store needs: acquire the per-store lock, load
    the current value (corruption-tolerant), apply `mutator(current) -> new_value`, and atomic-write
    the result — the whole section serialised so no concurrent writer clobbers it. Returns the new
    value. `mutator` must be pure w.r.t. the store (side-effect-free apart from producing the new
    value)."""
    with store_lock(path):
        current = load_json_tolerant(path, default)
        new_value = mutator(current)
        atomic_write_json(path, new_value)
        return new_value


def data_path(*parts: str):
    """Resolve a path under the configured DATA_DIR (default 'data').

    Single source of truth for persistent storage locations so a deployment can point all data at a
    durable volume via the DATA_DIR env var (data survives redeploys). Behaviour is unchanged when
    DATA_DIR is unset — it defaults to 'data', so data_path('vsb_entities') == Path('data/vsb_entities').
    Returns a pathlib.Path (works with open()/Path()/.mkdir()).
    """
    from pathlib import Path
    return Path(settings.data_dir).joinpath(*parts)


# Emit validation warnings at import time — never crash, just warn
for _issue in settings.validate():
    warnings.warn(f"[Workstation Config] {_issue}", stacklevel=2)
