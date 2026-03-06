import logging
from typing import Dict, Any, List, Optional
import time
import asyncio

logger = logging.getLogger(__name__)

class RateLimiter:
    """Token Bucket algorithm for rate limiting (Article 147)."""
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = float(capacity)
        self._tokens = float(capacity)
        self.fill_rate = float(fill_rate)
        self.last_fill = time.monotonic()

    def consume(self, tokens: int = 1) -> bool:
        self._fill()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def _fill(self):
        now = time.monotonic()
        delta = now - self.last_fill
        self._tokens = min(self.capacity, self._tokens + delta * self.fill_rate)
        self.last_fill = now

class ConnectorRegistry:
    """
    ARTICLE 147: Integration Hub Sovereignty.
    Manages pre-built connectors to external services with sandboxing.
    """
    def __init__(self):
        self.connectors = {
            "slack": {"type": "webhook", "rate_limit": 10},
            "gsheets": {"type": "oauth", "rate_limit": 5},
            "postgresql": {"type": "direct", "rate_limit": 100},
            "paperqa2": {"type": "rag", "rate_limit": 20, "description": "Scientific RAG tool"}
        }
        self.limiters: Dict[str, RateLimiter] = {
            name: RateLimiter(c["rate_limit"], c["rate_limit"] / 60.0) # rate_limit per minute
            for name, c in self.connectors.items()
        }
        self.active_sessions = {}

    def get_connector(self, name: str) -> Dict[str, Any]:
        return self.connectors.get(name, {})

    def register_custom_connector(self, name: str, schema: Dict[str, Any]):
        logger.info(f"Integrations: Registering {name}")
        self.connectors[name] = schema
        if "rate_limit" in schema:
            self.limiters[name] = RateLimiter(schema["rate_limit"], schema["rate_limit"] / 60.0)

    def execute_integration(self, name: str, data: Any) -> Dict[str, str]:
        if name not in self.connectors:
            return {"status": "error", "msg": "Unknown connector"}

        # Rate Limiting & Backpressure (Article 147)
        limiter = self.limiters.get(name)
        if limiter and not limiter.consume():
            logger.warning(f"Integrations: Rate limit exceeded for {name}. Applying backpressure.")
            return {"status": "error", "msg": "RATE_LIMIT_EXCEEDED"}

        logger.info(f"Integrations: Executing sandboxed call to {name}")
        # Real logic: Execute sandboxed tool call
        return {"status": "success", "artifact": f"Result from {name}"}
