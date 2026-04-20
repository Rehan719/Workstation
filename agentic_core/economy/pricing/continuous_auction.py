import time
from typing import List, Dict, Any, Tuple, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class ContinuousDoubleAuction:
    """
    Dynamic pricing engine for mesh resources.
    Uses bid/ask matching with SB-driven price discovery simulation.
    """
    def __init__(self, resource_type: str, ueg_logger: Optional[Any] = None):
        self.resource_type = resource_type
        self.ueg = ueg_logger or VSBUEGLogger()
        self.bids: List[Dict[str, Any]] = [] # Buys
        self.asks: List[Dict[str, Any]] = [] # Sells
        self.last_price = 1.0

    async def submit_order(self, peer_id: str, side: str, price: float, volume: float) -> Optional[Dict[str, Any]]:
        order = {"peer_id": peer_id, "price": price, "volume": volume, "ts": time.time()}

        if side == "bid":
            self.bids.append(order)
            self.bids.sort(key=lambda x: x["price"], reverse=True)
        else:
            self.asks.append(order)
            self.asks.sort(key=lambda x: x["price"])

        return await self._match_orders()

    async def _match_orders(self) -> Optional[Dict[str, Any]]:
        if not self.bids or not self.asks:
            return None

        best_bid = self.bids[0]
        best_ask = self.asks[0]

        if best_bid["price"] >= best_ask["price"]:
            match_price = (best_bid["price"] + best_ask["price"]) / 2
            match_volume = min(best_bid["volume"], best_ask["volume"])

            self.last_price = match_price

            self.bids.pop(0)
            self.asks.pop(0)

            match = {
                "resource": self.resource_type,
                "price": float(match_price),
                "volume": float(match_volume),
                "buyer": best_bid["peer_id"],
                "seller": best_ask["peer_id"]
            }
            await self.ueg.log_minimisation_event("market_trade_executed", match)
            return match

        return None
