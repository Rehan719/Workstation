"""The thermodynamic free-energy ledger — real physics, and no longer a claim about energy consumed.

W546 (P3.17, FU-234) — THE ARITHMETIC HERE WAS ALWAYS RIGHT AND THE LABEL WAS ALWAYS WRONG.
`E_min = k_B * T * ln 2` is the Landauer limit, correctly computed. What the ledger then did with it was
report `bits * E_min` under the field name `energy_joules`, which reads as the energy a computation used.
It is not: it is the thermodynamic MINIMUM to erase that many bits at that temperature, a floor that real
hardware exceeds by many orders of magnitude. A floor presented as a measurement is a claim nobody made.

AND ITS INPUTS WERE INVENTED. Six callers in the recirculation loop passed hardcoded bit counts — 1e4 for
sense, 5e4 for intend, 5e5 for analyse, 2e5 for act, 5e4 for learn, 1e5 for reflect — each recorded BEFORE
the stage did any work, so the figure could not have described what the stage processed even in principle.
That loop runs from the heartbeat, so every beat wrote an imaginary energy into a real ledger. The callers
now meter the measured size of the payload each stage actually handled, and this module says what that
means and what it does not.

`export_cycle_ledger` also returned `"compliance": True` unconditionally, including for a cycle in which
nothing was metered at all — a compliance verdict over an empty ledger. It is three-state now.
"""
import math
import time
from dataclasses import dataclass
from datetime import datetime, timezone

#  Boltzmann's constant, exact (SI 2019 redefinition). Not a tuned parameter.
_K_B = 1.380649e-23

#  W546 — the hardware inefficiency multiplier. It was `self.hw = 1.0` with no name and no provenance,
#  silently asserting that this platform's hardware operates AT the Landauer limit — which no hardware
#  does, by roughly nine orders of magnitude. 1.0 is kept so no figure changes silently, and it is now
#  declared as an unmeasured default rather than implied as a measurement.
_HW_FACTOR_DEFAULT = 1.0
_HW_BASIS = ("DECLARED, NOT MEASURED: the hardware factor is 1.0, which treats this platform as operating "
             "exactly at the Landauer limit. No real hardware does — practical CMOS is some nine orders of "
             "magnitude above it — so the energy figures here are a FLOOR and not an estimate of draw")


@dataclass
class ThermodynamicBudget:
    max_entropy_bits: float
    current_entropy_bits: float = 0.0

    @property
    def remaining(self) -> float:
        return self.max_entropy_bits - self.current_entropy_bits


class ThermodynamicFreeEnergyLedger:
    def __init__(self, budget_bits=1e12, temperature=300.0, ueg_logger=None):
        self.temperature = temperature
        self.E_min = _K_B * temperature * math.log(2)
        self.budget = ThermodynamicBudget(budget_bits)
        self.ueg = ueg_logger
        self.hw = _HW_FACTOR_DEFAULT
        #  how many operations this ledger has actually metered, so a cycle that metered NOTHING can be
        #  told apart from one that metered work and stayed inside its budget
        self.metered_ops = 0
        self.budget_basis = (f"DECLARED, NOT DERIVED: a budget of {budget_bits:g} bits per cycle is a "
                             f"literal carried in this constructor. Nothing measured this platform's "
                             f"actual information throughput to arrive at it")

    def meter_operation(self, name, bits, bits_basis: str = ""):
        """Record an operation's information cost, and return the Landauer FLOOR for it — not its draw.

        `bits_basis` is required of callers in substance if not in syntax: a bit count with no account of
        where it came from is the defect this ledger was built on, and the six callers that passed
        literals passed no basis either because there was nowhere to put one.
        """
        if bits is None:
            #  THE SAME KEY SET AS THE METERED RETURN BELOW. A reader indexing `energy_basis` on this
            #  branch, or `basis` on that one, got undefined — and the branch a reader most needs to
            #  understand is the one that measured nothing.
            return {"op": name, "metered": False, "entropy_bits": None,
                    "bits_basis": bits_basis or "no bit count was supplied by the caller",
                    "landauer_floor_joules": None,
                    "energy_basis": ("NOT COMPUTED: no bit count, so no Landauer floor. A zero would read "
                                     "as a thermodynamically free operation"),
                    "budget_remaining": self.budget.remaining,
                    "basis": ("NOT METERED: no bit count was supplied, so there is nothing to meter. A "
                              "zero would read as a free operation"),
                    "timestamp": time.time()}
        if bits > self.budget.remaining:
            raise PermissionError(f"TFEL: {name} exceeds budget")
        self.budget.current_entropy_bits += bits
        self.metered_ops += 1
        return {
            "op": name,
            "metered": True,
            "entropy_bits": bits,
            "bits_basis": bits_basis or "NOT STATED: the caller supplied no account of this bit count",
            #  RENAMED. `energy_joules` read as the energy this operation used.
            "landauer_floor_joules": bits * self.E_min * self.hw,
            "energy_basis": (f"the thermodynamic MINIMUM to erase {bits:g} bits at {self.temperature}K "
                             f"(k_B*T*ln2 per bit), multiplied by a hardware factor of {self.hw}. This is "
                             f"a FLOOR, not a measurement of energy drawn: nothing here measures power. "
                             f"{_HW_BASIS}"),
            "budget_remaining": self.budget.remaining,
            #  same key set as the not-metered branch above
            "basis": (f"METERED: {bits:g} bits recorded against the cycle budget, "
                      f"{self.budget.remaining:g} bits remaining. {self.budget_basis}"),
            "timestamp": time.time(),
        }

    def export_cycle_ledger(self, cid):
        """Close a cycle. Compliance is three-state: nothing metered is not compliance."""
        _ops = self.metered_ops
        _bits = self.budget.current_entropy_bits
        res = {
            "cycle_id": cid,
            "total_entropy_bits": _bits,
            "metered_operations": _ops,
            #  W546 — this was an unconditional True, returned even for a cycle that metered nothing at
            #  all. A compliance verdict over an empty ledger is the clearest possible case of a claim
            #  with no evidence: the most reassuring answer, available precisely when no work was done.
            "compliance": (True if _ops else None),
            "compliance_basis": (
                f"{_ops} operation(s) were metered and none exceeded the declared budget "
                f"({self.budget.max_entropy_bits:g} bits), so the cycle stayed within it. "
                f"{self.budget_basis}"
                if _ops else
                "NOT ASSESSED: no operation was metered in this cycle, so there is nothing to be compliant "
                "with. This is not compliance — it is an empty ledger"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.budget.current_entropy_bits = 0.0
        self.metered_ops = 0
        return res
