from __future__ import annotations


def _torch():
    """The torch module, or a refusal naming what is missing. W506 (P2.7(5)).

    torch is OPTIONAL by the 17.5 invariant: importing the platform must never require it. A top-level
    import here meant `import agentic_core.app_mvp` raised ModuleNotFoundError without it, so only the one
    function body that needs the module asks for it.
    """
    try:
        import torch
        return torch
    except Exception as exc:
        raise RuntimeError(
            "this operation needs PyTorch and it is not installed in this deployment: "
            f"{exc.__class__.__name__}: {exc}. Nothing was computed."
        ) from exc

#  W636 — AN OPTIONAL LIBRARY THAT FAILS TO LOAD IS ABSENT, WHATEVER IT RAISED. This caught ImportError
#  only. POT imports scikit-learn, which imports scipy.stats, and with torch blocked that chain raised an
#  AttributeError at import — so on a machine where POT is installed the whole platform failed to boot,
#  through a library every caller already treats as optional. Not seen on CI, which does not install POT.
#  The reason is kept and reported by availability(), so "not installed" is never said of a library that
#  is installed and broken.
_OT_IMPORT_ERROR = ""
try:
    import ot
except ImportError:
    ot = None
except Exception as _ot_exc:  # noqa: BLE001 — any import-time failure of an optional dependency
    ot = None
    _OT_IMPORT_ERROR = f"{_ot_exc.__class__.__name__}: {str(_ot_exc)[:160]}"
from typing import Dict, Tuple, Optional, Any
from ._utils import get_backend, to_numpy

class OptimalTransportRouter:
    """
    Wasserstein-based resource allocation with entropic regularisation.
    Uses POT (Python Optimal Transport) library for Sinkhorn solving.
    """

    def __init__(self, epsilon: float = 0.01, max_iter: int = 1000, tol: float = 1e-4):
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.tol = tol

    def availability(self) -> Dict[str, Any]:
        """Whether this router can solve anything, answerable WITHOUT calling it.

        W548 (FU-236) — the only way to discover the solver was missing used to be to call solve() and
        be thrown out of it by a RuntimeError. A component that can only report its own unavailability
        by failing cannot be asked about itself, which is what P3.17's bar means by reporting it.
        """
        return {
            "available": ot is not None,
            "solver": "POT (ot) — entropic Sinkhorn",
            "epsilon": self.epsilon,
            "max_iter": self.max_iter,
            "tolerance": self.tol,
            "basis": ("the POT solver is importable, so this router can compute a transport plan"
                      if ot is not None else
                      #  W636 — installed-but-failed-to-load is a different fact from not installed
                      (f"NOT AVAILABLE: the POT solver (`ot`) is installed but failed to load "
                       f"({_OT_IMPORT_ERROR}), so no transport plan and no Wasserstein distance can be "
                       "computed. Nothing is estimated in its place.")
                      if _OT_IMPORT_ERROR else
                      "NOT AVAILABLE: the POT solver (`ot`) is not installed in this deployment, so no "
                      "transport plan and no Wasserstein distance can be computed. Nothing is estimated "
                      "in its place — an entropic optimal transport problem has no cheap approximation "
                      "that would deserve the same name"),
        }

    def _solve_meta(self, log: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """What the solve actually did — three-state where POT did not say.

        `converged: True` was a literal and `iterations` reported `max_iter`, the CAP, as the count. So a
        solve that exhausted its iteration budget was described in exactly the same words as one that
        converged, which is the single distinction a caller needs from a Sinkhorn run.
        """
        _errs = (log or {}).get("err") or []
        _final = float(_errs[-1]) if _errs else None
        _iters = len(_errs) if _errs else None
        if _final is None:
            _converged, _basis = None, (
                "NOT KNOWN: the solver returned no convergence log, so whether it converged or exhausted "
                "its iteration budget cannot be determined. This is not a convergence claim")
        elif _final <= self.tol:
            _converged, _basis = True, (
                f"the final marginal error {_final:g} is at or below the tolerance {self.tol:g}")
        else:
            _converged, _basis = False, (
                f"NOT CONVERGED: the final marginal error {_final:g} exceeds the tolerance {self.tol:g} "
                f"after {_iters} iteration(s); the transport plan is the last iterate, not a solution")
        return {
            "available": True,
            #  the real count where POT reported one, never the cap standing in for it
            "iterations": _iters,
            "iterations_basis": (f"{_iters} iteration(s) recorded by the solver"
                                 if _iters is not None else
                                 f"NOT REPORTED: the solver gave no per-iteration log. The cap is "
                                 f"{self.max_iter} and is not a count of what ran"),
            "converged": _converged,
            "converged_basis": _basis,
            "final_error": _final,
            "epsilon": self.epsilon,
            "method": "pot_sinkhorn",
        }

    def solve(
        self,
        source: torch.Tensor,
        target: torch.Tensor,
        cost_matrix: torch.Tensor,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Tuple[torch.Tensor, float, Dict]:
        """
        Solve entropic optimal transport problem using POT.
        """
        if ot is None:
            #  W548 (FU-236) — A REFUSAL IS AN OUTCOME, NOT A CRASH. This raised, so a caller asking an
            #  unavailable router for a plan got an exception where it expected a result, and the only
            #  way to learn the router is unavailable was to call it and be thrown out of. P3.17's bar
            #  asks the router to REPORT itself unavailable; `availability()` below answers without
            #  calling, and this returns the same three-state shape the solve path returns.
            return (None, None, self.availability())
        # Convert to NumPy for POT compatibility
        mu = source.detach().cpu().numpy()
        nu = target.detach().cpu().numpy()
        C = cost_matrix.detach().cpu().numpy()

        # Ensure normalisation
        mu = mu / (mu.sum() + 1e-10)
        nu = nu / (nu.sum() + 1e-10)

        # Solve using POT Sinkhorn
        # Mask infinite costs with a very large finite number for POT stability
        C_max = C[C < float('inf')].max() * 10 if C[C < float('inf')].size > 0 else 1e6
        C_stable = np.where(C == float('inf'), C_max, C)

        #  W548 — ASK POT FOR ITS LOG. `converged: True` was a literal and `iterations` reported the
        #  CAP as the count, with a comment admitting the base call does not return one. So the router
        #  announced convergence in exactly the same words whether it converged or hit the iteration
        #  limit — the one distinction a caller needs from a Sinkhorn solve.
        _log = None
        try:
            plan, _log = ot.sinkhorn(mu, nu, C_stable, reg=self.epsilon, numItermax=self.max_iter,
                                     stopThr=self.tol, log=True)
        except TypeError:
            plan = ot.sinkhorn(mu, nu, C_stable, reg=self.epsilon, numItermax=self.max_iter,
                               stopThr=self.tol)

        # Wasserstein distance
        # Use original cost for distance calculation to reflect infinite cost penalties
        wasserstein = float(np.sum(plan * C_stable))

        return (
            _torch().from_numpy(plan).float(),
            wasserstein,
            self._solve_meta(_log)
        )

import numpy as np
