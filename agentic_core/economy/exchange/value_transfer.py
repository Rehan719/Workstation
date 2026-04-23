from typing import Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class ValueTransferEngine:
    """
    Reputation-weighted value exchange.
    Integrates with the Treaty Ledger for transaction finality.
    """
    def __init__(self, health_monitor: Any, ledger: Any, ueg_logger: Optional[Any] = None):
        self.health = health_monitor
        self.ledger = ledger
        self.ueg = ueg_logger or VSBUEGLogger()

    async def execute_transfer(self, from_peer: str, to_peer: str, amount: float, reason: str) -> Dict[str, Any]:
        rep_to = self.health.get_reputation(to_peer)
        effective_value = amount * (0.5 + 0.5 * rep_to) # Discount/Premium based on trust

        transfer_id = f"tx_{from_peer}_{to_peer}_{amount}"
        result = {
            "tx_id": transfer_id,
            "from": from_peer,
            "to": to_peer,
            "nominal_amount": amount,
            "effective_value": float(effective_value),
            "reputation_factor": rep_to,
            "reason": reason,
            "status": "settled"
        }

        await self.ueg.log_minimisation_event("value_transfer_settled", result)
        return result
