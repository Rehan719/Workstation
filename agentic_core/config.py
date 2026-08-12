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
