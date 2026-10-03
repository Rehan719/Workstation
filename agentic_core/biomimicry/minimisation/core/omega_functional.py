"""The Ω-functional, recovered — and a term nobody measured can no longer be the best possible term.

P3.17's bar: "every Ω term computes its named quantity or says it cannot". This is the second half.

WHAT THE ARCHIVED VERSION DID, measured from
`_archive/jules-unwired/agentic_core/biomimicry/minimisation/core/omega_functional.py`:

  J(π) = α·F[π] + β·W_ε(μ,ν) + γ·KL(π||R) + δ·S_export[π] + ζ·M[π]

  (a) EVERY TERM DEFAULTED TO ZERO. `policy_metrics.get("free_energy", 0.0)` and the same for the other
      four. This is a MINIMISATION objective, so zero is not a neutral default — IT IS THE OPTIMUM. A
      policy that supplied no metrics at all scored 0.0 and beat every policy that actually reported
      one. The least-measured candidate always won, and the arithmetic was correct throughout.
  (b) THE HARD CONSTRAINT CLEARED ITSELF. `legal_compliance: float = 1.0` meant a caller who measured no
      compliance passed the non-negotiable legal check by omission, because the test is
      `legal_compliance < 1.0`. The one constraint described as non-negotiable was the easiest to pass.
  (c) IT IMPORTED torch AT MODULE LEVEL AND NEVER USED IT, which would have broken this platform's
      optional-torch invariant: importing the application must not require torch, and a top-level import
      here made `import agentic_core.app_mvp` fail without it.

WHAT THIS VERSION REFUSES TO DO. A partial sum is not a smaller cost — it is an unknown one, so J is
reported only when every weighted term is assessable, and otherwise the terms are returned individually
with their reasons. That is stricter than it sounds and it is the whole point: a minimisation that scores
an incomplete candidate rewards incompleteness.

ONE TERM HAS A REAL PRODUCER TODAY. `entropy_export` can be read from the thermodynamic ledger, whose bit
counts became measurements in W546. The other four have none: free energy has no producer at all, optimal
transport has no solver installed, the Schrödinger bridge is archived, and Murray's law is unimplemented.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

#  The weights the archive declared. They sum to 1.0, which is the only property anything checks about
#  them — nothing derived or tuned them against this platform's data.
_DEFAULT_WEIGHTS = {
    "free_energy": 0.30,        # surprise minimisation
    "optimal_transport": 0.25,  # resource efficiency
    "schrodinger_bridge": 0.20, # path likelihood
    "entropy_export": 0.15,     # thermodynamic efficiency
    "murray_law": 0.10,         # branching network efficiency
}
_WEIGHTS_BASIS = ("DECLARED, NOT DERIVED: these five weights are the ones the archived objective carried. "
                  "They sum to 1.0 and nothing tuned them against this platform's data, so the relative "
                  "importance they assert is an authored choice rather than a finding")

#  Where each term's quantity would have to come from. Naming the producer is what makes "says it cannot"
#  an instruction rather than a shrug.
_TERM_PRODUCERS = {
    "free_energy": ("no producer exists on this platform. A variational free energy needs a generative "
                    "model and an observation to be surprised by, and neither is implemented"),
    "optimal_transport": ("agentic_core/biomimicry/minimisation/core/optimal_transport.py is a real "
                          "Sinkhorn router whose solver (POT) is not installed, so it reports itself "
                          "unavailable rather than returning a plan"),
    "schrodinger_bridge": ("the IPF/Sinkhorn bridge is archived at _archive/jules-unwired/agentic_core/"
                           "biomimicry/minimisation/core/schrodinger_bridge.py and is imported by "
                           "nothing live"),
    "entropy_export": ("core/transcendent_subsystems/tfel.py measures this one: its bit counts became "
                       "measurements of real payload sizes in W546, so a caller can supply it"),
    "murray_law": ("no producer exists. Murray's law relates branch radii in a transport network and "
                   "nothing here models one"),
}


class MinimisationObjective:
    """J(π) over five terms, each assessable or refused by name."""

    def __init__(self, weights: Optional[Dict[str, float]] = None,
                 legal_precision_weight: float = 1.0):
        self.weights = dict(weights or _DEFAULT_WEIGHTS)
        self.legal_precision_weight = legal_precision_weight
        self.weights_basis = _WEIGHTS_BASIS

    def evaluate(self, policy_metrics: Dict[str, float], context: Dict[str, Any],
                 legal_compliance: Optional[float] = None) -> Dict[str, Any]:
        """Evaluate J(π), or report which terms prevented it.

        `legal_compliance` has NO DEFAULT. It defaulted to 1.0, so a caller who measured nothing passed
        the constraint the objective itself calls non-negotiable. None means not assessed, and a legal
        domain cannot be cleared by a figure nobody produced.
        """
        terms: Dict[str, Any] = {}
        for name, weight in self.weights.items():
            raw = policy_metrics.get(name)
            if isinstance(raw, (int, float)):
                terms[name] = {"assessable": True, "value": float(raw), "weight": weight,
                               "contribution": weight * float(raw),
                               "basis": f"supplied by the caller as {raw}"}
            else:
                #  NO `value` KEY AT ALL, and emphatically not 0.0: in a minimisation a zero is the best
                #  possible term, so defaulting an unmeasured quantity to it makes ignorance win.
                terms[name] = {"assessable": False, "weight": weight,
                               "basis": f"NOT ASSESSED: {_TERM_PRODUCERS.get(name, 'no producer named')}"}

        _unassessable = [n for n, t in terms.items() if not t["assessable"]]
        _is_legal = (context.get("layer") == "L12_Policy" or context.get("domain") == "legal")

        #  THE HARD CONSTRAINT, and it can no longer be passed by omission.
        if _is_legal and legal_compliance is None:
            return self._result(None, terms, _unassessable, _is_legal, legal_compliance,
                                ("REFUSED: this is a legal domain and no legal-compliance figure was "
                                 "supplied. The objective calls this constraint non-negotiable, and a "
                                 "constraint that passes when nobody measured it is not one"))
        if _is_legal and legal_compliance < 1.0:
            return self._result(float("inf"), terms, _unassessable, _is_legal, legal_compliance,
                                (f"INFINITE: a legal domain with compliance {legal_compliance} below "
                                 f"1.0. The hard constraint holds"))

        if _unassessable:
            return self._result(None, terms, _unassessable, _is_legal, legal_compliance,
                                (f"NOT COMPUTED: {len(_unassessable)} of {len(self.weights)} term(s) "
                                 f"have no measurement ({', '.join(sorted(_unassessable))}). A partial "
                                 f"sum is not a smaller cost, it is an unknown one — and in a "
                                 f"MINIMISATION, scoring an incomplete candidate rewards incompleteness"))

        score = sum(t["contribution"] for t in terms.values())
        _soft = None
        if not _is_legal and isinstance(legal_compliance, (int, float)) and legal_compliance < 1.0:
            #  the archive's large declared penalty, named rather than implied
            _soft = (1.0 - legal_compliance) * 1000.0
            score += _soft
        return self._result(score, terms, _unassessable, _is_legal, legal_compliance,
                            (f"computed over {len(self.weights)} assessable term(s); "
                             + (f"plus a declared soft penalty of {_soft} for compliance "
                                f"{legal_compliance} (the 1000.0 multiplier is the archive's literal, "
                                f"not a derived figure). " if _soft else "")
                             + self.weights_basis), soft_penalty=_soft)

    def _result(self, j, terms, unassessable, is_legal, legal_compliance, basis, soft_penalty=None):
        """One constructor, so no exit can carry a field another lacks."""
        return {
            "J": j,
            "terms": terms,
            "assessable_terms": sorted(n for n, t in terms.items() if t["assessable"]),
            "unassessable_terms": sorted(unassessable),
            "legal_domain": is_legal,
            "legal_compliance": legal_compliance,
            "soft_penalty": soft_penalty,
            "weights_basis": self.weights_basis,
            "basis": basis,
        }
