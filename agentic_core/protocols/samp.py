from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

class SAMPMessage(BaseModel):
    """
    Structured Agent Messaging Protocol v6.0
    """
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    layer: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
    provenance_chain: List[str] = []
    ethical_flags: Dict[str, Any] = {}
    payload: Dict[str, Any]

    def add_to_provenance(self, agent_id: str):
        self.provenance_chain.append(agent_id)
