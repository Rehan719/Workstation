import os
import sys
from typing import Dict, Any

# The constitutional-core sibling folder contains hyphens, so it cannot be
# imported via a normal dotted path. Resolve it on sys.path instead.
_CC_DIR = os.path.join(os.path.dirname(__file__), "..", "constitutional-core")
if _CC_DIR not in sys.path:
    sys.path.insert(0, _CC_DIR)
from vsb_constitutional_core import UCIV12Interceptor

class DomainSpecificEngine:
    """Configurable Domain Process Intelligence v12.0."""
    def __init__(self, node_id: str, domain: str):
        self.node_id = node_id
        self.domain = domain
        self.uci = UCIV12Interceptor(node_id)

    async def execute_domain_task(self, task: str, context: Dict[str, Any]):
        async def action():
            return f"Task '{task}' executed in domain: {self.domain}. Status: CERTIFIED."

        full_context = {**context, "stream": "domain_specific", "domain": self.domain}
        return await self.uci.intercept_call("autogen", full_context, action)
