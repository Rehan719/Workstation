import time
import logging
from typing import Dict, Any, List, Optional

class WorkstationToken:
    """
    Simulated WST (ERC-20) Smart Contract on Polygon.
    """
    def __init__(self):
        self.balances: Dict[str, float] = {}
        self.sovereign_liability_fund = 100000.0 # Article 1103

    def transfer(self, sender: str, recipient: str, amount: float) -> bool:
        if self.balances.get(sender, 0.0) >= amount:
            self.balances[sender] -= amount
            self.balances[recipient] = self.balances.get(recipient, 0.0) + amount
            return True
        return False

    def mint(self, recipient: str, amount: float):
        self.balances[recipient] = self.balances.get(recipient, 0.0) + amount

class AgentMarketplace:
    """
    Agent Marketplace for buying/selling modules and agents using WST.
    Includes Escrow and Reputation.
    """
    def __init__(self, token: WorkstationToken, ueg_callback=None):
        self.token = token
        self.ueg_callback = ueg_callback
        self.logger = logging.getLogger("Marketplace")

        # Listings: listing_id -> {agent_id, price, owner}
        self.listings: Dict[str, Dict[str, Any]] = {}
        self.reputation: Dict[str, float] = {} # agent_id -> score

    def list_agent(self, agent_id: str, price: float, owner: str):
        listing_id = f"list_{int(time.time() * 1000)}"
        self.listings[listing_id] = {
            "agent_id": agent_id,
            "price": price,
            "owner": owner,
            "status": "ACTIVE"
        }
        self.logger.info(f"Marketplace: Agent {agent_id} listed for {price} WST.")
        return listing_id

    def purchase_agent(self, buyer: str, listing_id: str):
        """Executes a purchase via simulated escrow."""
        listing = self.listings.get(listing_id)
        if not listing or listing["status"] != "ACTIVE":
            return False

        price = listing["price"]
        self.logger.info(f"Marketplace: {buyer} purchasing {listing['agent_id']} for {price} WST.")

        # 1. Transfer WST
        if self.token.transfer(buyer, listing["owner"], price):
            # 2. Update Status
            listing["status"] = "SOLD"

            # 3. Apply Metabolic Tax (1%)
            tax = price * 0.01
            self.token.transfer(listing["owner"], "SOVEREIGN_VAULT", tax)

            self._emit_event("MARKET_PURCHASE", {
                "buyer": buyer,
                "listing_id": listing_id,
                "agent_id": listing["agent_id"],
                "tax_wst": tax
            })
            return True

        return False

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "AgentMarketplace",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    token = WorkstationToken()
    token.mint("user_A", 500.0)
    market = AgentMarketplace(token)

    l_id = market.list_agent("law_bot_v2", 100.0, "developer_X")
    success = market.purchase_agent("user_A", l_id)
    print(f"Purchase Success: {success}")
    print(f"User A balance: {token.balances.get('user_A')}")
