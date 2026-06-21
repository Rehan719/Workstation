"""
EconomicMetabolism — the living, biomimetic economic cycle of a VSB.

Value flows through the VSB like a biogeochemical nutrient cycle, mapped onto the
organism's metabolism:

    INTAKE (revenue)          ≈ feeding / photosynthesis  → raises metabolic energy
    HOMEOSTASIS (reserves)    ≈ internal balance kept first (legal/operating)
    CIRCULATION (waterfall)   ≈ cardiovascular distribution to organs:
        owner            ≈ nourishing the sovereign/host
        self_investment  ≈ growth & tissue repair (anabolism)
        capital_fund     ≈ energy storage (fat/glycogen)
        user_projects    ≈ symbiosis / seeding offspring (mutualism, pollination)
        charity          ≈ the nutrient-RETURN loop (decomposition → shared soil)
    ADAPTATION                ≈ homeostatic + evolutionary self-tuning

Runs continuously and adaptively, under governance, integrated with the ATP
metabolic system and the nervous signal bus. Virtual/simulated throughout.
"""
from __future__ import annotations

import time
from typing import Any, Dict, Optional

from .entities import get_template
from .ledger import VirtualLedger
from .charity import CharityIntelligence

_CYCLE_ROLE = {
    "owner": "nourishing the sovereign (host)",
    "self_investment": "growth & tissue repair (anabolism)",
    "capital_fund": "energy storage (fat/glycogen)",
    "user_projects": "symbiosis — seeding offspring ventures",
    "charity": "nutrient-return loop — giving back to the shared ecosystem",
}


class EconomicMetabolism:
    def __init__(self, vsb_id: str, entity_type: str = "waqf_ltd_hybrid", owner: str = "Rehan"):
        self.vsb_id = vsb_id
        self.owner = owner
        self.template = get_template(entity_type)
        self.entity_type = entity_type
        self.waterfall = dict(self.template["waterfall"])
        self.ledger = VirtualLedger(vsb_id)
        self.charity = CharityIntelligence()

    # ── the living cycle ──────────────────────────────────────────────────────
    def run_cycle(self, revenue: float, costs: float = 0.0, reserve_rate: float = 0.20) -> Dict[str, Any]:
        """One metabolic cycle: intake → homeostasis → circulation → giving-back → adaptation."""
        revenue = max(0.0, float(revenue))
        costs = max(0.0, float(costs))

        # 1. Intake
        self.ledger.record("revenue", revenue, memo="cycle intake (revenue)")

        # 2. Homeostasis — reserves first (legal/operating + prudential)
        reserves = round(costs + revenue * reserve_rate, 2)
        self.ledger.record("reserves", reserves, memo="homeostasis (reserves + costs)")

        # 3. Distributable profit
        distributable = round(max(0.0, revenue - reserves), 2)

        # 4. Circulation — the waterfall
        splits: Dict[str, float] = {}
        for stage, frac in self.waterfall.items():
            amount = round(distributable * frac, 2)
            splits[stage] = amount
            if amount > 0:
                self.ledger.record(stage, amount, memo=f"circulation → {_CYCLE_ROLE.get(stage, stage)}")

        # 5. Giving-back — intelligent charity allocation (nutrient-return loop)
        charity_alloc = self.charity.allocate(splits.get("charity", 0.0)) if splits.get("charity", 0.0) > 0 else None

        # 6. Biomimetic links — metabolic energy + nervous signal
        metabolic_energy = self._atp_ratio()
        self._fire_signal(revenue, distributable)

        report = {
            "vsb_id": self.vsb_id,
            "entity_type": self.entity_type,
            "entity_name": self.template["name"],
            "cycle_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "intake_revenue": revenue,
            "homeostasis_reserves": reserves,
            "distributable_profit": distributable,
            "circulation": {k: {"amount_wst": v, "role": _CYCLE_ROLE.get(k, k)} for k, v in splits.items()},
            "giving_back": charity_alloc,
            "metabolic_energy": metabolic_energy,
            "capital_preserved": self.template["capital_preserved"],
            "biogeochemical_model": "nutrient cycle: intake → homeostasis → circulation → return → storage → growth",
            "disclaimer": "Virtual/simulated WST — no real funds moved.",
        }
        return report

    # ── adaptation (self-improvement; called by the Sovereign Evolution Office) ─
    def tune(self, adjustments: Dict[str, float]) -> Dict[str, Any]:
        """Adapt the waterfall within bounds, then re-normalise. Owner-bounded self-improvement."""
        for stage, frac in adjustments.items():
            if stage in self.waterfall:
                self.waterfall[stage] = max(0.0, min(1.0, float(frac)))
        total = sum(self.waterfall.values()) or 1.0
        self.waterfall = {k: round(v / total, 4) for k, v in self.waterfall.items()}
        return {"waterfall": self.waterfall, "status": "adapted"}

    def status(self) -> Dict[str, Any]:
        return {
            "vsb_id": self.vsb_id,
            "owner": self.owner,
            "entity_type": self.entity_type,
            "entity_name": self.template["name"],
            "waterfall": self.waterfall,
            "capital_preserved": self.template["capital_preserved"],
            "metabolic_energy": self._atp_ratio(),
            "ledger": self.ledger.statement(),
        }

    # ── biomimetic integration helpers (guarded) ──────────────────────────────
    @staticmethod
    def _atp_ratio() -> Optional[float]:
        try:
            from agentic_core.molecular.atp_simulator import ATPSimulator
            # ATPSimulator.ratio is the ATP/ADP energy state (0.5–15); normalise to 0–1.
            return round(float(ATPSimulator().ratio) / 15.0, 3)
        except Exception:
            return None

    def _fire_signal(self, revenue: float, distributable: float) -> None:
        try:
            from agentic_core.organism.biobus import biobus
            biobus.fire_signal("motor", f"economy.metabolism.{self.vsb_id}",
                               f"cycle: rev {revenue} → dist {distributable}",
                               min(1.0, 0.4 + revenue / 100000))
        except Exception:
            pass
