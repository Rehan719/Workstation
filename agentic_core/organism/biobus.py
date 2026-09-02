"""
IDBO Biomimetic Event Bus — the central nervous integration layer.

This is the single point of integration for all organism systems. Every
operational module (projects, VSB, swarm, management, capital, twins)
calls biobus instead of individual organism systems directly.

The bus:
  1. Routes signals to the NervousSystem
  2. Queries immune + self_healing + ATP + circadian to produce health context
  3. Provides a health_gate() so operations can check organism readiness
  4. Records operations to immune + nervous simultaneously
  5. Exposes organism_context() — the full state any AI agent can use to
     adapt its behaviour to the organism's current condition

Biological analogy:
  - NervousSystem  → synaptic signal routing
  - ImmuneSystem   → pathogen / threat detection
  - SelfHealer     → adaptive recovery (circuit breaker)
  - ATPSimulator   → cellular energy availability
  - Circadian      → temporal regulation
  - Genome         → trait expression
  - Reconfiguration → epigenetic adaptation

Usage:
    from agentic_core.organism.biobus import biobus

    biobus.fire_signal("sensory", "projects.create", "New project created", 0.4)
    ctx = biobus.organism_context()
    if not biobus.health_gate("high_cost_operation"):
        return {"degraded": True, "reason": ctx["health_summary"]}
"""
from __future__ import annotations

import datetime
import threading
import time
from typing import Any

# ── Singleton imports ────────────────────────────────────────────────────────

from agentic_core.organism.immune import immune
from agentic_core.organism.nervous import nervous
from agentic_core.organism.self_healing import self_healer


def _get_atp():
    """Lazy import — ATPSimulator may not exist in all environments."""
    try:
        from agentic_core.molecular.atp_simulator import ATPSimulator
        if not hasattr(_get_atp, "_inst"):
            _get_atp._inst = ATPSimulator()
        return _get_atp._inst
    except Exception:
        return None


def _circadian_cycle() -> str:
    hour = datetime.datetime.now().hour
    if 6 <= hour < 9 or 17 <= hour < 20:
        return "ACTIVE_REST"
    if 9 <= hour < 17:
        return "ACTIVE_FOCUS"
    if 20 <= hour < 23:
        return "MAINTENANCE_FOCUS"
    return "MAINTENANCE_REST"


def _get_reconfig():
    """Read runtime config from reconfiguration engine."""
    try:
        from agentic_core.organism.reconfiguration import _load_config
        return _load_config()
    except Exception:
        return {}


class BiomimeticBus:
    """
    Central event bus and health aggregator for the IDBO organism.
    Thread-safe singleton — safe to call from async FastAPI handlers.
    """

    # Minimum immune health to allow high-cost operations
    HEALTH_GATE_THRESHOLD = 0.2

    def __init__(self):
        self._lock = threading.Lock()
        self._op_count = 0
        self._atp_last_update = 0.0

    # ── Signal Routing ────────────────────────────────────────────────────────

    def fire_signal(
        self,
        signal_type: str,   # sensory | motor | reflex | cognitive
        source: str,        # e.g. "projects.create", "vsb.spawn", "swarm.cascade"
        payload: str = "",
        intensity: float = 0.5,
    ) -> None:
        """Fire a nervous system signal. Non-blocking — never raises."""
        try:
            nervous.fire(signal_type, source, payload, intensity)
        except Exception:
            pass

    # ── Error Recording ───────────────────────────────────────────────────────

    def record_error(self, source: str, error_type: str = "ai_failure") -> None:
        """Record an operational error to the immune system."""
        try:
            immune.record(source, error_type)
        except Exception:
            pass
        self.fire_signal("reflex", source, f"error:{error_type}", 0.8)

    def record_success(self, endpoint: str) -> None:
        """Record a successful operation to the self-healing system."""
        try:
            self_healer.record_success(endpoint)
        except Exception:
            pass

    # ── Health Gate ───────────────────────────────────────────────────────────

    def health_gate(self, operation: str = "default") -> bool:
        """
        Returns True if the organism is healthy enough to run this operation.
        Operations should check this before starting resource-intensive work.
        """
        try:
            imm = immune.status()
            if imm["health"] < self.HEALTH_GATE_THRESHOLD:
                return False
            if self_healer.is_open(operation):
                return False
        except Exception:
            pass
        return True

    def should_throttle(self) -> bool:
        """Returns True if the organism is under stress and should slow down."""
        try:
            imm = immune.status()
            return imm["threat_level"] in ("HIGH", "CRITICAL")
        except Exception:
            return False

    # ── ATP update ────────────────────────────────────────────────────────────

    def _update_atp(self, metabolic_load: float = 0.3) -> float:
        """Update ATP simulator and return ratio. Throttled to once per second."""
        now = time.monotonic()
        if now - self._atp_last_update < 1.0:
            atp = _get_atp()
            # normalise to 0-1 (same scale as the non-throttled path) — the raw simulator ratio is 0.5-15.0;
            # returning it raw here corrupted atp_ratio/composite_health on rapid successive reads.
            return round(max(0.0, min(1.0, atp.ratio / 15.0)), 3) if atp else 0.8
        self._atp_last_update = now
        atp = _get_atp()
        if atp:
            cycle = _circadian_cycle()
            efficiency = 1.0 if cycle == "ACTIVE_FOCUS" else 0.8
            atp.update(dt=1.0, metabolic_load=metabolic_load, circadian_efficiency=efficiency)
            return round(max(0.0, min(1.0, atp.ratio / 15.0)), 3)
        return 0.8

    # ── Organism Context ──────────────────────────────────────────────────────

    def organism_context(self, metabolic_load: float = 0.3) -> dict[str, Any]:
        """
        Full organism state for AI decision-making.

        Any agent or workflow can call this to get:
        - Current health scores (immune, metabolic, circuit breaker)
        - Circadian cycle (affects energy and priority)
        - Nervous system arousal (reflects current activity level)
        - Recommended behaviour modifiers (throttle, degrade, full-power)
        - Genome-guided trait axes (if available)

        Used by: VSB spawn CEO prompt, swarm cascade, intelligence engines.
        """
        try:
            imm = immune.status()
            ns = nervous.status()
            sh = self_healer.status()
            cycle = _circadian_cycle()
            atp_ratio = self._update_atp(metabolic_load)
            reconfig = _get_reconfig()

            immune_health = imm["health"]
            # W438 — self-healing honestly reports health None when ZERO circuits are tracked (a
            # fresh process has measured nothing). For the composite, an untracked breaker registry
            # contributes no evidence of harm: treat as 1.0 here, but the terms below disclose it.
            _sh_raw = sh["overall_health"]
            sh_untracked = _sh_raw is None
            sh_health = 1.0 if sh_untracked else _sh_raw
            metabolic = atp_ratio
            composite_health = round((immune_health * 0.4 + sh_health * 0.4 + metabolic * 0.2), 3)
            # §8 · §17.2 (W422) — the metabolic term is 20% of this score and is SIMULATED, not
            # measured: ATPSimulator is driven by a constant metabolic_load (default 0.3) and the
            # circadian phase, so it is a function of time and constants rather than of anything the
            # platform actually does. immune_health and sh_health ARE measured. The composite is left
            # unchanged because live thresholds read it (change_control gates on >= 0.6), but it must
            # never again be presented as wholly measured — so the measured-only score travels beside
            # it, and the simulated term is named.
            # W438 refuter catch: with the breaker registry untracked, sh_health is a DEFAULT, so
            # folding it into a score named "measured only" at 50% weight made a fresh process read
            # 100% measured health; measured-only is immune-alone until self-healing has evidence
            _measured_only = round(immune_health, 3) if sh_untracked else round(
                (immune_health * 0.5 + sh_health * 0.5), 3)

            # Recommended behaviour
            if composite_health >= 0.8 and cycle == "ACTIVE_FOCUS":
                mode = "FULL_POWER"
                temperature = "creative"
            elif composite_health >= 0.5:
                mode = "NOMINAL"
                temperature = "neutral"
            elif composite_health >= 0.2:
                mode = "DEGRADED"
                temperature = "precise"
            else:
                mode = "EMERGENCY"
                temperature = "precise"

            return {
                "composite_health": composite_health,
                "composite_health_measured_only": _measured_only,
                "composite_health_terms": {
                    "immune_health": {"weight": 0.4, "value": immune_health, "measured": True},
                    "self_healing_health": {"weight": 0.4, "value": sh_health,
                                            "measured": not sh_untracked,
                                            **({"basis": "no circuits tracked yet — defaulted to 1.0, "
                                                         "not a measurement"} if sh_untracked else {})},
                    "metabolic": {"weight": 0.2, "value": metabolic, "measured": False,
                                  "basis": "ATPSimulator on a constant metabolic_load — simulated, "
                                           "not a measurement of this platform"},
                },
                "mode": mode,
                "immune": {
                    "health": immune_health,
                    "threat_level": imm["threat_level"],
                    "errors_in_window": imm["errors_in_window"],
                },
                "nervous": {
                    "arousal_state": ns["arousal_state"],
                    "signal_rate": ns["signal_rate_per_second"],
                    "signals_last_60s": ns["signals_last_60s"],
                },
                "self_healing": {
                    "overall_health": sh_health,
                    "open_circuits": sh["open_circuits"],
                },
                "metabolic": {
                    "atp_ratio": atp_ratio,
                },
                "circadian": {
                    "cycle": cycle,
                    "is_peak_focus": cycle == "ACTIVE_FOCUS",
                },
                "recommended": {
                    "temperature": temperature,
                    "should_throttle": composite_health < 0.5,
                    "max_parallel_agents": 3 if composite_health >= 0.7 else 1,
                    "priority": "high" if cycle == "ACTIVE_FOCUS" else "normal",
                },
                "runtime_config": {
                    "rpm_limit": reconfig.get("gateway", {}).get("rpm_limit", 20),
                    "preferred_provider": reconfig.get("gateway", {}).get("preferred_provider", "auto"),
                    "features": reconfig.get("features", {}),
                },
                "health_summary": self._health_summary(composite_health, mode, cycle),
            }
        except Exception as e:
            # W438 — this fallback used to omit "recommended"/"circadian", so /health-summary
            # 500'd (KeyError) at exactly the moment the organism was least healthy, and its
            # constant 0.9 travelled undisclosed. The dict is now shape-complete and the constant
            # carries its basis; live threshold consumers keep working (0.9 >= their gates).
            return {
                "composite_health": 0.9,
                "composite_health_basis": ("FALLBACK CONSTANT — the organism context errored; "
                                           "0.9 is not a measurement"),
                "composite_health_measured_only": None,
                "composite_health_terms": None,
                "mode": "NOMINAL",
                "error": str(e),
                "immune": {"health": None, "threat_level": "UNKNOWN"},
                "circadian": {"cycle": "UNKNOWN", "is_peak_focus": False},
                "metabolic": {"atp_ratio": None},
                "recommended": {"should_throttle": False, "max_parallel_agents": 2,
                                "temperature": "neutral", "priority": "normal"},
                "runtime_config": {"rpm_limit": 20, "preferred_provider": "auto", "features": {}},
                "health_summary": "Organism context unavailable — running at nominal (fallback).",
            }

    def _health_summary(self, health: float, mode: str, cycle: str) -> str:
        summaries = {
            "FULL_POWER":  f"Organism at peak — {cycle} cycle, health {health:.0%}. Full cognitive power available.",
            "NOMINAL":     f"Organism nominal — {cycle} cycle, health {health:.0%}. Standard operations active.",
            "DEGRADED":    f"Organism under stress — health {health:.0%}. Reduced parallelism, precise mode.",
            "EMERGENCY":   f"Organism critical — health {health:.0%}. Emergency mode. Minimal operations only.",
        }
        return summaries.get(mode, f"Organism health: {health:.0%}")

    # ── Operation Recording ───────────────────────────────────────────────────

    def record_operation(
        self,
        operation: str,
        source: str,
        success: bool = True,
        payload: str = "",
    ) -> None:
        """
        Record a completed operation — updates immune + nervous simultaneously.
        Call this at the end of every major workflow operation.
        """
        with self._lock:
            self._op_count += 1

        if success:
            signal_type = "motor"
            self.fire_signal(signal_type, source, payload or f"{operation} completed", 0.4)
        else:
            self.record_error(source, error_type=operation)

    # ── Genome Context ────────────────────────────────────────────────────────

    def get_genome_context(self, entity_id: str) -> dict[str, Any]:
        """
        Returns the genome trait vector for a VSB/project entity.
        Used by CEO/C-Suite to adapt their reasoning to the entity's traits.
        """
        try:
            from agentic_core.organism.genome import _load_genome
            genome = _load_genome(entity_id)
            if genome and "traits" in genome:
                return {"traits": genome["traits"], "generation": genome.get("generation", 0)}
        except Exception:
            pass
        return {}

    def genome_prompt_modifier(self, entity_id: str) -> str:
        """
        Returns a natural-language genome modifier to prepend to AI prompts.
        Lets the CEO/swarm adapt behaviour to the entity's genetic profile.
        """
        ctx = self.get_genome_context(entity_id)
        if not ctx or "traits" not in ctx:
            return ""
        traits = ctx["traits"]
        modifiers = []
        if traits.get("innovation", 0.5) > 0.7:
            modifiers.append("favour novel and experimental approaches")
        if traits.get("commerciality", 0.5) > 0.7:
            modifiers.append("prioritise revenue and commercial viability")
        if traits.get("urgency", 0.5) > 0.7:
            modifiers.append("optimise for speed to market")
        if traits.get("sustainability", 0.5) > 0.7:
            modifiers.append("emphasise long-term sustainability over short-term gain")
        if traits.get("regulation", 0.5) > 0.6:
            modifiers.append("ensure full regulatory compliance")
        if not modifiers:
            return ""
        return f"Entity genome traits: {'; '.join(modifiers)}. "


# Singleton — import this everywhere
biobus = BiomimeticBus()
