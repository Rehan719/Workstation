import logging
import json
import base64
import hashlib
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AvatarFrontendInterface:
    """
    Sovereign API Interface for the Living Avatar.
    Handles real-time streaming and constitutional overrides.
    """
    def __init__(self, recirculation_orchestrator: Any, ueg_logger: Any):
        self.orchestrator = recirculation_orchestrator
        self.ueg = ueg_logger
        self.active_session = True

    async def handle_user_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Entry point for user interaction."""
        if not self.active_session:
            return {"error": "Session inactive"}

        # ARTICLE 1136: Constitutional Override check
        if message.strip().upper() == "CONSTITUTIONAL_OVERRIDE":
            return await self._handle_override("GLOBAL_VETO")

        user_context = {**context, "input": message}
        result = await self.orchestrator.execute_cycle(user_context)
        return result

    async def _handle_override(self, override_type: str) -> Dict[str, Any]:
        """Immediately halts avatar and logs signed receipt."""
        self.active_session = False

        #  W658 - THIS IS A LABEL, NOT A SIGNED RECEIPT. It is the digest of the override's type: the same for
        #  every halt of that type, signed by no key, proving nothing about who halted what. It used to be
        #  returned with a second digest under a name that said it was signed.
        receipt_id = hashlib.sha256(f"OVERRIDE_{override_type}".encode()).hexdigest()[:8]
        receipt_basis = ("a fixed label for this override type - a digest of the type's name, not a signature "
                         "and not unique to this halt")

        await self.ueg.log_event("CONSTITUTIONAL_OVERRIDE_TRIGGERED", {
            "type": override_type,
            "receipt_id": receipt_id,
            "receipt_basis": receipt_basis
        })

        logger.warning(f"CONSTITUTIONAL OVERRIDE: Avatar halted. Receipt: {receipt_id}")

        return {
            "status": "HALTED",
            "reason": "Constitutional Override Activated",
            "receipt": receipt_id,
            "receipt_basis": receipt_basis
        }
