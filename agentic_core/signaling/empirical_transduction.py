import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EmpiricalSignalTransduction:
    """Hill saturation transform — where a signal sits on a sigmoidal dose-response curve.

    W437 — this class used to advertise "pulsatile decoding (0.02-0.8 Hz), latency < 90s" and
    return three §4.5-class fields, proved live before the rewrite:
      · `latency` was `45.0 / (1 + input_signal)` — nothing was timed; a constant formula wearing
        a unit ("seconds") and independent of every parameter but the input itself.
      · `frequency` was echoed as if it governed the result; peak intensity was byte-identical
        across the whole advertised band because the sine's max() reduced it to one constant
        scale factor.
      · the sine wrapper made the "activation cascade" trajectory negative half the time, which
        no phosphorylation model produces, and negative inputs silently took the real part of a
        complex power.

    What remains is only what the math actually earns: activation = s^h / (K50^h + s^h), a real
    monotone Hill transform in which `hill` genuinely changes the steepness, plus the honest
    dose-response curve over s ∈ [0,1] (its domain is stated in the payload) so a caller can see
    the shape their signal is transformed by. Nothing is timed, nothing
    pulses, and the supra-threshold boolean is stated for what it is: input_signal >= K50.
    """

    def __init__(self, hill: float = 4.5, k50: float = 0.5):
        if hill <= 0:
            raise ValueError("hill must be > 0")
        if k50 <= 0:
            raise ValueError("k50 must be > 0")
        self.hill = hill
        self.k50 = k50

    def activation(self, signal: float) -> float:
        """Hill transform of one non-negative signal, numerically stable at any magnitude."""
        if signal < 0:
            raise ValueError("input_signal must be >= 0 — a Hill transform of a negative "
                             "concentration has no referent (and s**h is complex)")
        if signal == 0:
            return 0.0
        # 1 / (1 + (K50/s)^h) is algebraically s^h/(K50^h + s^h) but cannot overflow into a 500:
        # an overflowing ratio power IS the mathematical limit (activation → 0), and an underflow
        # to 0.0 is the other limit (activation → 1).
        try:
            r = (self.k50 / signal) ** self.hill
        except OverflowError:
            return 0.0
        return float(1.0 / (1.0 + r))

    def transform(self, input_signal: float, curve_points: int = 101) -> Dict[str, Any]:
        """The signal's activation + the dose-response curve over s ∈ [0, 1].

        (Renamed from `simulate_cascade` in W437 — nothing here simulates or cascades, and the old
        name was half the overclaim.)"""
        act = self.activation(input_signal)
        step = 1.0 / (curve_points - 1) if curve_points > 1 else 1.0
        curve = [self.activation(i * step) for i in range(curve_points)]
        supra = input_signal >= self.k50
        logger.info("SIGNALING: Hill transform s=%.3f h=%.2f K50=%.2f -> activation=%.4f",
                    input_signal, self.hill, self.k50, act)
        return {
            "activation": act,
            "supra_threshold": supra,
            "k50": self.k50,
            "hill": self.hill,
            "dose_response": curve,
            "dose_response_domain": [0.0, 1.0],   # the curve samples s in [0,1]; a signal above 1 sits beyond it
            "basis": (f"activation = s^h / (K50^h + s^h) with s={input_signal}, h={self.hill}, "
                      f"K50={self.k50}; supra_threshold means input_signal >= K50 — a saturation "
                      f"transform of the supplied number, not a timed or observed cascade"),
        }
