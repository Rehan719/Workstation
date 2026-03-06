import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SpanOfControlEngine:
    """
    ARTICLE 183: Span of Control Engine.
    Dynamic scope negotiation with activation predicates and control decay.
    """
    def __init__(self):
        self.active_scopes: Dict[str, float] = {}

    def negotiate_scope(self, agent_id: str, requested_scope: str, predicate: bool) -> bool:
        """Evaluates activation predicate and sets control decay timeout."""
        if predicate:
            decay_timeout = time.time() + 300 # 5-minute decay
            self.active_scopes[f"{agent_id}:{requested_scope}"] = decay_timeout
            logger.info(f"SPAN: Scope {requested_scope} granted to {agent_id}. Expires in 300s.")
            return True
        return False

    def check_scope_validity(self, agent_id: str, scope: str) -> bool:
        key = f"{agent_id}:{scope}"
        if key in self.active_scopes:
            if time.time() < self.active_scopes[key]:
                return True
            else:
                del self.active_scopes[key]
                logger.warning(f"SPAN: Scope {scope} for {agent_id} has decayed.")
        return False
