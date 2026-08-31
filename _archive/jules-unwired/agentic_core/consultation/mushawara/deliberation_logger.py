import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Dict

from agentic_core.ueg.ueg_manager import UEGManager

logger = logging.getLogger("DeliberationLogger")


class DeliberationLogger:
    """
    Immutable logging of all consultation events to UEG Merkle-DAG.
    Enforces SHA-3-512 cryptographic integrity.
    """

    def __init__(self):
        self.ueg = UEGManager()
        self.merkle_root = "0" * 64

    async def log_event(self, event_type: str, payload: Dict[str, Any]):
        """
        Logs a deliberation event with cryptographic chaining.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "payload": payload,
            "previous_hash": self.merkle_root,
        }

        entry_json = json.dumps(entry, sort_keys=True)
        self.merkle_root = hashlib.sha3_512(entry_json.encode()).hexdigest()

        await self.ueg.log_event(
            event_type=f"mushawara_{event_type}",
            payload=payload,
            merkle_root=self.merkle_root,
        )

        logger.debug(
            f"Mushawara: Logged {event_type} with root {self.merkle_root[:16]}"
        )
