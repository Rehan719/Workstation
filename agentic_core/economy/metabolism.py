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

import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from agentic_core.config import StoreUnavailable, atomic_write_json, data_path, read_json_strict
from .entities import get_template
from .ledger import VirtualLedger
from .charity import CharityIntelligence

logger = logging.getLogger(__name__)

# §4/§8/§10 — the Owner can adjust the profit-distribution proportions per VSB (virtual). Overrides persist
# here and are loaded over the entity-template default; they are always bounded by the template's binding
# constraints (a non-distributing form forces owner=0; a capital-preserving form requires capital_fund>0).
_WATERFALL_STAGES = ["owner", "self_investment", "capital_fund", "user_projects", "charity"]
_WATERFALL_OVERRIDES = data_path("economy_waterfall_overrides.json")


def _load_waterfall_overrides() -> Dict[str, Dict[str, float]]:
    """W472 (register FU-051) — whole or StoreUnavailable: one save on an unreadable store used to keep only the new
    override, and a cycle on one silently used the template."""
    return read_json_strict(_WATERFALL_OVERRIDES, dict, expect=dict)


def _save_waterfall_overrides(d: Dict[str, Dict[str, float]]) -> None:
    atomic_write_json(_WATERFALL_OVERRIDES, d)          # W472 — atomic; the route holds the store lock


def validate_waterfall(proportions: Dict[str, Any], template: Dict[str, Any]) -> Tuple[Dict[str, float], List[str]]:
    """Validate + normalise an Owner-proposed waterfall against the entity template's BINDING constraints.
    Returns (normalised_waterfall summing to 1.0, violations). Virtual-only — the Owner sets, the form bounds."""
    violations: List[str] = []
    w: Dict[str, float] = {}
    for s in _WATERFALL_STAGES:
        try:
            w[s] = max(0.0, min(1.0, float(proportions.get(s, 0.0))))
        except (TypeError, ValueError):
            w[s] = 0.0
    total = sum(w.values())
    if total <= 0:
        return dict(template["waterfall"]), ["All proportions are zero — provide a distribution."]
    w = {k: round(v / total, 4) for k, v in w.items()}
    if not template.get("distributes_profit", True) and w["owner"] > 0:
        violations.append("This entity form distributes no owner profit — set the owner share to 0.")
    if template.get("capital_preserved", False) and w["capital_fund"] <= 0:
        violations.append("This entity form preserves capital — the capital_fund share must be greater than 0.")
    return w, violations

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
        # §4/§8/§10 — apply any Owner-set override (re-normalised; bounded by the template) over the default.
        self.waterfall_source = "entity_template"
        self.overrides_error: Optional[str] = None
        try:
            _ov = _load_waterfall_overrides().get(vsb_id)
        except StoreUnavailable as e:
            # W472 (FU-051) — the Owner's overrides cannot be known: the template applies and the cycle SAYS so
            _ov, self.overrides_error, self.waterfall_source = None, str(e), "overrides_unavailable"
        if _ov:
            merged = {s: float(_ov.get(s, self.waterfall.get(s, 0.0))) for s in _WATERFALL_STAGES}
            # W472 (refutation) — a STORED override is re-validated against the form every time it is applied: one
            # saved while the roster could not be read was bound to the caller's claim, not the entity's form
            _bounded, _violations = validate_waterfall(merged, self.template)
            if _violations:
                self.waterfall_source = "entity_template (stored override violates the form; ignored)"
                self.override_violations = _violations
            else:
                self.waterfall = _bounded
                self.waterfall_source = "owner_override"
        self.ledger = VirtualLedger(vsb_id)
        self.charity = CharityIntelligence()

    # ── the living cycle ──────────────────────────────────────────────────────
    def run_cycle(self, revenue: float, costs: float = 0.0, reserve_rate: float = 0.20,
                  max_returns_wst: Optional[float] = None,
                  max_transfers_wst: Optional[float] = None,
                  progress: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """One metabolic cycle: intake → homeostasis → circulation → giving-back → adaptation.

        W463 — `max_returns_wst` / `max_transfers_wst` cap what this cycle drains from the pending
        queues: the governed paths pass what the §3 materiality gate MEASURED, so a receipt that lands
        between the gate and this cycle waits for the next one (it used to be drained and distributed
        without the Change Control hold its size required). None = drain everything (ungoverned use)."""
        revenue = max(0.0, float(revenue))
        costs = max(0.0, float(costs))

        # W468 (register FU-041) — a ledger that cannot be read whole is refused BEFORE anything is drained from the
        # return and receipt queues (its first write would be refused anyway, and the drained intake only given back)
        self.ledger.check_readable()

        # §6 — venture RETURNS RECYCLE into the waterfall: queued returns on this VSB's portfolio
        # are consumed here as intake revenue, so they genuinely enter this cycle's distribution.
        returns_recycled = 0.0
        venture_store_note: Optional[str] = None
        try:
            from .ventures import consume_pending_returns
            returns_recycled = consume_pending_returns(self.vsb_id, max_amount=max_returns_wst)
            if returns_recycled > 0:
                revenue = round(revenue + returns_recycled, 2)
        except StoreUnavailable as e:
            # W472 (refutation) — the portfolio could not be read whole: no returns entered, and the report says so
            returns_recycled, venture_store_note = 0.0, f"venture returns not consumed: {e}"
        except Exception:
            returns_recycled = 0.0

        # federation — inter-VSB RECEIPTS enter this cycle's waterfall the same way (W262).
        transfers_received = 0.0
        receipts_error = None
        try:
            from .transfers import consume_pending_transfers
            transfers_received = consume_pending_transfers(self.vsb_id, max_amount=max_transfers_wst)
            if transfers_received > 0:
                revenue = round(revenue + transfers_received, 2)
        except Exception as _rx_err:
            # W465 — the receipts stay queued (nothing was taken); the report says why none entered this cycle
            transfers_received = 0.0
            receipts_error = f"{type(_rx_err).__name__}: {str(_rx_err)[:160]}"
            logger.warning("cycle for %s took no inter-VSB receipts: %s", self.vsb_id, receipts_error)

        # §8→§12 ECONOMIC SURVIVAL INSTINCT — when the LIVING ORGANISM's metabolic energy is depleted, the
        # economic organism conserves more (raises reserves), mirroring the §8 homeostatic survival instinct.
        metabolic_energy = self._atp_ratio()
        effective_reserve = float(reserve_rate)
        energy_state = "healthy"
        if metabolic_energy is not None and metabolic_energy < 0.3:
            effective_reserve = round(min(0.6, reserve_rate + 0.15), 3)
            energy_state = "conserving (low organism energy)"

        if progress is not None:
            progress["returns_drained_wst"], progress["receipts_drained_wst"] = returns_recycled, transfers_received

        # 1. Intake
        # W467 (register FU-044) — the first write is ONE atomic save: when it raises, nothing was written, so the returns
        # and receipts this cycle drained go back to their queues (they used to vanish, posted nowhere). W467 (FU-022):
        # the caller learns whether the ledger was written (`progress`), so a cycle that wrote nothing can give back the
        # events it consumed, and the released action counts as run only once it has written.
        try:
            self.ledger.record("revenue", revenue, memo="cycle intake (revenue)",
                               ref=(progress or {}).get("cycle_token"))
        except BaseException:
            given = self._give_back_drained(returns_recycled, transfers_received)
            if progress is not None:
                progress["intake_given_back"] = given
            raise
        if progress is not None:
            progress["ledger_written"] = True
            hook = progress.get("on_ledger_written")
            if callable(hook):
                try:
                    hook()
                except Exception as _hook_err:
                    logger.warning("cycle for %s: the first-write hook raised: %s", self.vsb_id, _hook_err)

        # 2. Homeostasis — reserves first (legal/operating + prudential; energy-adjusted §8→§12)
        reserves = round(costs + revenue * effective_reserve, 2)
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

        # 4b. §7 — the Owner's share accrues to the Owner-Payments ledger (virtual WST; real rails gated).
        # W465 (FU-016) — a failed accrual used to vanish (`except: pass`) while the ledger above already showed
        # the owner stage as distributed; it is now said in the report and on the UEG.
        owner_accrual: Dict[str, Any] = {"accrued": False, "amount_wst": splits.get("owner", 0.0)}
        if splits.get("owner", 0.0) > 0:
            try:
                from .owner_payments import accrue as _accrue_owner
                _accrue_owner(self.vsb_id, splits["owner"], self.owner, memo="cycle owner share (§4 waterfall)")
                owner_accrual["accrued"] = True
            except Exception as _acc_err:
                owner_accrual["error"] = f"{type(_acc_err).__name__}: {str(_acc_err)[:160]}"
                try:
                    from agentic_core.gaas.v5 import UEGLogger
                    UEGLogger().log({"type": "economy.owner_accrual_failed", "vsb_id": self.vsb_id,
                                     "amount_wst": splits["owner"], "error": owner_accrual["error"],
                                     "note": "the cycle distributed the owner stage but the owner-payments store "
                                             "did not record it; the Owner's balance is short by this amount",
                                     "disclaimer": "Virtual/simulated WST — no real funds moved."})
                    owner_accrual["ueg_logged"] = True
                    logger.warning("owner accrual NOT recorded for %s (%s WST): %s", self.vsb_id, splits["owner"],
                                   owner_accrual["error"])
                except Exception as _ueg_err:
                    owner_accrual["ueg_logged"] = False
                    # the page sends the Owner to the server log for this case: the record must be here
                    logger.error("owner accrual NOT recorded and NOT on the UEG for %s (%s WST): accrual error %s; "
                                 "UEG error %s", self.vsb_id, splits["owner"], owner_accrual["error"],
                                 f"{type(_ueg_err).__name__}: {str(_ueg_err)[:160]}")
        else:
            owner_accrual["note"] = "no owner share this cycle"

        # 4c. §12 (W294) — the capital_fund stage COMPOUNDS into the shared Sovereign Capital Fund
        #     (energy storage genuinely STORES — previously only a ledger row; the endowment loop
        #     was three disconnected WST pools). Attributed + UEG-logged; best-effort.
        capital_contribution = None
        try:
            if splits.get("capital_fund", 0.0) > 0:
                from agentic_core.api.capital_fund import contribute_from_cycle
                capital_contribution = contribute_from_cycle(self.vsb_id, splits["capital_fund"])
        except Exception:
            capital_contribution = None

        # 5. Giving-back — intelligent charity allocation (nutrient-return loop)
        charity_alloc = self.charity.allocate(splits.get("charity", 0.0)) if splits.get("charity", 0.0) > 0 else None

        # 5b. §6 — user-project investment: competitively allocate the user_projects stage to top ventures and
        #     track them as portfolio positions (seeding offspring; returns recycle into the waterfall). Virtual.
        ventures_alloc = None
        try:
            if splits.get("user_projects", 0.0) > 0:
                from .ventures import VentureIntelligence, record_positions, real_candidates
                # §6 — competitively select from the platform's REAL projects + living VSB offspring
                # (deterministic metrics from live state); the curated demo set only when the
                # platform is empty (honestly flagged via using_demo_candidates).
                cands = real_candidates(exclude_vsb=self.vsb_id)
                ventures_alloc = VentureIntelligence(cands or None).allocate(splits["user_projects"])
                record_positions(self.vsb_id, ventures_alloc)
        except StoreUnavailable as e:
            # W472 (refutation) — the stage was distributed; the positions were NOT recorded, and the report says so
            ventures_alloc = {"positions_recorded": False, "reason": str(e), "allocation": ventures_alloc}
            venture_store_note = (venture_store_note + "; " if venture_store_note else "") + f"positions not recorded: {e}"
        except Exception:
            ventures_alloc = None

        # 6. Biomimetic links — nervous signal (metabolic energy already read above for the §8→§12 coupling)
        self._fire_signal(revenue, distributable)

        report = {
            "vsb_id": self.vsb_id,
            "entity_type": self.entity_type,
            "entity_name": self.template["name"],
            "cycle_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "intake_revenue": revenue,
            "venture_returns_recycled_wst": returns_recycled,   # §6 — returns that re-entered this waterfall
            "inter_vsb_received_wst": transfers_received,       # federation — receipts from other VSBs (W262)
            **({"inter_vsb_receipts_error": receipts_error} if receipts_error else {}),   # W465 — none taken, and why
            "homeostasis_reserves": reserves,
            "reserve_rate_applied": effective_reserve,   # §8→§12: energy-adjusted (conserves more when low)
            "energy_state": energy_state,
            "distributable_profit": distributable,
            "circulation": {k: {"amount_wst": v, "role": _CYCLE_ROLE.get(k, k)} for k, v in splits.items()},
            "capital_fund_contribution": capital_contribution,   # §12 (W294) — compounded into the pool
            "owner_accrual": owner_accrual,                      # §7 (W465) — whether the owner share was recorded
            "giving_back": charity_alloc,
            "venture_investment": ventures_alloc,
            "venture_store_note": venture_store_note,          # W472 — an unreadable portfolio is said, not silent
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
            # W472 (FU-051) — where the proportions came from; an override store that could not be read whole is SAID
            "waterfall_source": self.waterfall_source,
            "overrides_error": self.overrides_error,
            "capital_preserved": self.template["capital_preserved"],
            "metabolic_energy": self._atp_ratio(),
            "ledger": self.ledger.statement(),
        }

    def _give_back_drained(self, returns_wst: float, receipts_wst: float) -> Dict[str, bool]:
        """W467 (register FU-044) — put back what this cycle drained before its first write failed. Never raises: a
        give-back that fails is written to the UEG and the log with its amount, so it can be reconciled by hand.
        Returns, per intake that was drained, whether it went back."""
        outcome: Dict[str, bool] = {}
        for kind, amount in (("venture_returns", returns_wst), ("inter_vsb_receipts", receipts_wst)):
            if not amount or amount <= 0:
                continue
            try:
                if kind == "venture_returns":
                    from .ventures import return_pending_returns
                    return_pending_returns(self.vsb_id, amount)
                else:
                    from .transfers import return_pending_transfers
                    return_pending_transfers(self.vsb_id, amount)
                event = {"type": "economy.cycle_intake_given_back", "vsb_id": self.vsb_id, "intake": kind,
                         "amount_wst": amount, "note": "the cycle's first ledger write failed; nothing was posted"}
                outcome[kind] = True
            except Exception as err:
                outcome[kind] = False
                why = f"{type(err).__name__}: {str(err)[:160]}"
                logger.error("cycle for %s drained %s WST of %s, wrote nothing, and could not give it back: %s",
                             self.vsb_id, amount, kind, why)
                event = {"type": "economy.cycle_intake_give_back_failed", "vsb_id": self.vsb_id, "intake": kind,
                         "amount_wst": amount, "error": why,
                         "note": "drained from its queue and posted nowhere — put it back by hand"}
            try:
                from agentic_core.gaas.v5 import UEGLogger
                UEGLogger().log({**event, "disclaimer": "Virtual/simulated WST — no real funds moved."})
            except Exception:
                pass
        return outcome

    # ── biomimetic integration helpers (guarded) ──────────────────────────────
    @staticmethod
    def _atp_ratio() -> Optional[float]:
        # LIVE metabolic energy — the SAME shared organism ATP the §8 homeostasis governs (cognition expends
        # it, the heartbeat restores it), NOT a fresh simulator. This links §12 economy ↔ §8 living organism.
        try:
            from agentic_core.organism.biobus import _get_atp
            atp = _get_atp()
            # ATP/ADP energy state (0.5–15); normalise to 0–1.
            return round(max(0.0, min(1.0, float(atp.ratio) / 15.0)), 3) if atp else None
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
