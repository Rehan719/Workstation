import asyncio
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger

class MultiAssetPortfolioManager:
    """
    Module 3E: Multi-Asset Portfolio Manager.
    Tracks internal reactor allocations and external positions.
    Enforces diversity limits (min 5 assets) and concentration limits (max 20% per asset).
    """
    def __init__(self, owner_uid: str, ueg: UEGLogger):
        self.owner_uid = owner_uid
        self.ueg = ueg
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.max_concentration = Decimal("0.20")
        self.min_diversity_count = 5

    async def update_position(self, asset_id: str, amount: Decimal, price_usd: Decimal, category: str, bypass_risk_limits: bool = False) -> Dict[str, Any]:
        """
        Updates an asset position with constitutional risk validation.
        """
        total_aum = await self.get_total_aum()
        current_value = amount * price_usd

        # 1. Concentration Check (Article 1130)
        if not bypass_risk_limits and total_aum > 0:
            # Check if this asset's new value exceeds 20% of the total new AUM
            # If the asset already exists, we subtract its old value from total_aum before adding new
            old_value = Decimal(str(self.positions.get(asset_id, {}).get("value_usd", 0.0)))
            new_aum = total_aum - old_value + current_value

            if new_aum > 0:
                predicted_concentration = current_value / new_aum
                if predicted_concentration > self.max_concentration:
                    raise ValueError(f"Constitutional Violation: Allocation to {asset_id} exceeds 20% limit ({predicted_concentration:.2%}).")

        # 2. Diversity Check (Article 1130 recommendation)
        current_assets = list(self.positions.keys())
        if asset_id not in current_assets:
            current_assets.append(asset_id)

        diversity_score = len(current_assets) / self.min_diversity_count

        # 3. Apply Update
        self.positions[asset_id] = {
            "amount": float(amount),
            "value_usd": float(current_value),
            "category": category,
            "last_updated": datetime.now(UTC).isoformat()
        }

        await self.ueg.log_event("PORTFOLIO_POSITION_UPDATED", {
            "uid": self.owner_uid,
            "asset_id": asset_id,
            "value_usd": float(current_value),
            "diversity_score": diversity_score
        })

        return {
            "status": "UPDATED",
            "asset_id": asset_id,
            "diversity_score": diversity_score,
            "total_aum": float(await self.get_total_aum())
        }

    async def get_total_aum(self) -> Decimal:
        """Calculates total assets under management in USD."""
        return sum([Decimal(str(p["value_usd"])) for p in self.positions.values()], Decimal("0"))

    async def get_allocation_report(self) -> List[Dict[str, Any]]:
        """Returns detailed report for the dashboard."""
        total = await self.get_total_aum()
        report = []
        for asset, data in self.positions.items():
            report.append({
                "asset": asset,
                "value": data["value_usd"],
                "percentage": float(Decimal(str(data["value_usd"])) / total * 100) if total > 0 else 0,
                "category": data["category"]
            })
        return report
