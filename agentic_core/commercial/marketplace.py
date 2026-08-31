import logging
import uuid
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MarketplaceIntegrator:
    """
    ARTICLE 686, 706: Global Marketplace Integration v127.0.
    Lists VSB services on external marketplaces and handles automated billing.
    """
    def __init__(self):
        self.listings = []
        from .marketplace_integrators.connectors import RapidAPIConnector, AWSMarketplaceConnector
        self.rapid_api = RapidAPIConnector()
        self.aws_market = AWSMarketplaceConnector()

    async def list_on_external(self, service_id: str, marketplace: str, pricing: Dict[str, Any]):
        """Transitions from simulation to real connector calls."""
        logger.info(f"Marketplace: Listing {service_id} on {marketplace}")

        result = {"status": "ERROR"}
        if marketplace.lower() == "rapidapi":
            result = await self.rapid_api.list_product({"name": service_id, "pricing": pricing})
        elif marketplace.lower() == "aws":
            result = await self.aws_market.create_listing(service_id)

        listing = {
            "id": result.get("id", result.get("listing_id", f"EXT_{uuid.uuid4().hex[:4]}")),
            "service_id": service_id,
            "marketplace": marketplace,
            "pricing": pricing,
            "status": "LIVE" if result.get("status") == "LIVE" or "listing_id" in result else "PENDING"
        }
        self.listings.append(listing)
        return listing

    def process_external_transaction(self, listing_id: str, amount_wst: int) -> Dict[str, Any]:
        """Compute the ARTICLE 746 revenue split for a marketplace sale.

        This does NOT settle anything: no billing API is called, no ledger is written and no
        account is credited. The returned split is a proposed allocation, not a payment.
        """
        # W415 — this was documented "v128.0: Live marketplace billing and revenue distribution
        # logic" and returned {"transaction_id": tx_id, "status": "COMPLETED", "distribution":
        # {...}, "receipt_url": "https://api.jules-ai.com/receipts/<tx>"}, which a consumer reads
        # as a settled billing transaction with a retrievable receipt. Nothing settled: the method
        # touched no ledger (agentic_core/commercial/token_ledger.py is the real signed WST ledger
        # and is never called from here), no store and no external billing API — it multiplied its
        # own argument by four percentages, logged, and returned. "COMPLETED" was a string literal,
        # and api.jules-ai.com is a leftover host from the prior Jules build that this codebase
        # never calls and does not own, so the receipt URL 404s by construction. The four-way split
        # allocated funds (liability fund / scholar rewards / operational costs / charity) that no
        # account ever receives. The arithmetic is real and is kept as an explicitly UNAPPLIED
        # plan; the settlement, the receipt and the COMPLETED verdict are reported absent.
        logger.info(f"Marketplace: Computing revenue split for {listing_id} - {amount_wst} WST (no settlement)")

        # ARTICLE 746: Revenue Allocation — arithmetic only, credited to nobody.
        # 40% Liability, 30% Scholars, 20% Ops, 10% Charity
        distribution = {
            "liability_fund": int(amount_wst * 0.40),
            "scholar_rewards": int(amount_wst * 0.30),
            "operational_costs": int(amount_wst * 0.20),
            "charity": int(amount_wst * 0.10)
        }

        ref_id = f"TXREF_{uuid.uuid4().hex[:10]}"
        logger.info(f"Marketplace: {ref_id} computed (NOT settled). Proposed distribution: {distribution}")

        return {
            "transaction_id": None,
            "reference_id": ref_id,
            "status": "NOT_SETTLED",
            "settled": False,
            "amount": amount_wst,
            "distribution": distribution,
            "distribution_applied": False,
            "receipt_url": None,
            "detail": (
                "No marketplace billing backend is wired in this build. The split above is the "
                "ARTICLE 746 allocation this amount WOULD carry; no funds moved, no ledger entry "
                "was written and no receipt exists."
            )
        }
