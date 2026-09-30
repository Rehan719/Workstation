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


def atp_depletion_state() -> dict:
    """Whether the ATP figure CAN fall, computed from the model's own constants. W506 (P2.7(4)).

    `ATPSimulator.update` consumes `0.1 * metabolic_load` (load clamped to 0-1) and produces
    `0.5 * circadian_efficiency`. `_update_atp` passes an efficiency of 1.0 or 0.8 and nothing else. So at the
    worst combination reachable in this code production is 0.4 against a consumption of 0.1 and the ratio only
    rises, to its 15.0 ceiling.

    This is DERIVED rather than stated, so it stops saying "cannot deplete" by itself if a low-efficiency path
    is ever added - the previous basis asserted the conclusion AND the wrong reason for it (a 0.5 floor that
    never binds), which is the defect class W494 removed from the CCA's basis strings.
    """
    max_consumption = 0.1 * 1.0                 # load is clamped to 1.0 in both the caller and the simulator
    efficiencies = (1.0, 0.8)                   # every value _update_atp can pass
    min_production = 0.5 * min(efficiencies)
    can_deplete = max_consumption > min_production
    return {
        "can_deplete": can_deplete,
        "max_consumption_per_tick": round(max_consumption, 4),
        "min_production_per_tick": round(min_production, 4),
        "efficiencies_this_code_passes": list(efficiencies),
        "floor": 0.5, "ceiling": 15.0, "scale": "the raw ratio is 0.5-15.0; callers report it divided by 15",
        "basis": (
            f"consumption is at most {max_consumption:.2f} per tick (0.1 x a load clamped to 1.0) and "
            f"production at least {min_production:.2f} (0.5 x the lowest efficiency this code passes, "
            f"{min(efficiencies)}), so production exceeds consumption at every reachable combination and the "
            f"ratio only RISES to its ceiling. It does not deplete - and NOT because of the 0.5 floor, which "
            f"never binds."
            if not can_deplete else
            f"consumption reaches {max_consumption:.2f} per tick against a production floor of "
            f"{min_production:.2f}, so the ratio CAN fall"),
        # OWNER RULING 2026-09-30 (18.1) - the budget that CAN run down, reported beside the one that
        # cannot. `can_deplete` above is UNCHANGED and still describes the SIMULATOR: re-pointing it
        # would break every reader who takes it to mean exactly that. What this adds is the honest
        # instrument and its unit, so no reader has to infer that a ratio between 0.5 and 15.0 measures
        # anything.
        # WHICH SURFACE SHOWS THIS (the pre-flight asks, and the answer is indirect but real):
        # app_mvp.py appends the budget - its unit, seconds spent, capacity and whether it gates
        # anything - onto `atp_basis`, which already reaches the viewer (ResourceFabric.tsx renders the
        # organism tooltip that carries it). No page reads THIS key by name, and that is deliberate:
        # adding a second channel for one claim is how two surfaces come to disagree.
        "the_figure_that_can_deplete": _work_budget_state(),
        "ratio_is_a_label_not_a_measurement": (
            "the ATP ratio names no unit and cannot fall; the work budget beside it is measured in "
            "wall-clock seconds actually spent and reaches its capacity. Where a threshold needs a real "
            "energy figure, read the budget"),
    }


def _work_budget_state() -> dict:
    """The work budget, or the reason it could not be read. Never raises into a status call."""
    try:
        from agentic_core.molecular import work_budget
        return work_budget.state()
    except Exception as exc:                                  # noqa: BLE001 - said, never substituted
        return {"unavailable": f"{exc.__class__.__name__}: {exc}",
                "note": "no budget figure is substituted; an unreadable budget is not a full one"}


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
        """Update ATP simulator and return ratio. Throttled to once per second.

        W494 (refutation) — the load arrives from callers and from a user-reconfigurable fabric param
        declared "float 0-1"; an out-of-domain value here drains the PROCESS-WIDE singleton and makes
        every threshold written against the term fire at once. Clamped at this entry as well as in the
        simulator, so the figure this method reports is the figure it actually used."""
        try:
            metabolic_load = max(0.0, min(1.0, float(metabolic_load)))
        except (TypeError, ValueError):
            metabolic_load = 0.3
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

            # §8 (W494, FU-116/FU-110/FU-107) — THE MODE IS DECIDED ON WHAT WAS MEASURED.
            # This used to branch on the BLENDED score, of which 60% is not a measurement when no
            # circuit is tracked: self-healing defaults to 1.0 and the metabolic term is a simulator.
            # The consequence was observed live: immune health 0.0 with threat_level CRITICAL and 11
            # errors in the window, and this returned mode NOMINAL with the summary "Standard
            # operations active", because 0.4·0.0 + 0.4 + 0.2·1.0 = 0.6. The blend could not fall
            # below 0.6 for ANY immune value, so the mode was not an assessment of anything.
            # An unmeasured term contributes no evidence either way, so it cannot vote.
            _measured_weight = 0.4 if sh_untracked else 0.8   # metabolic is never measured
            _decider = _measured_only
            if _decider >= 0.8 and cycle == "ACTIVE_FOCUS":
                mode = "FULL_POWER"
                temperature = "creative"
            elif _decider >= 0.5:
                mode = "NOMINAL"
                temperature = "neutral"
            elif _decider >= 0.2:
                mode = "DEGRADED"
                temperature = "precise"
            else:
                mode = "EMERGENCY"
                temperature = "precise"
            _mode_basis = (
                f"decided on the MEASURED-only score {_decider} "
                f"({_measured_weight:.0%} of the blend's weight is measured: immune"
                + ("" if sh_untracked else " and self-healing")
                + f"). The blended figure {composite_health} also carries "
                + ("a self-healing term defaulted to 1.0 and " if sh_untracked else "")
                + "a simulated metabolic term, so it cannot be read as a measurement.")

            # §8 (W494, FU-117) — the metabolic term can only RISE, which is why it cannot decide
            # anything. atp_simulator.update() adds 0.5·efficiency (efficiency is 1.0 or 0.8) and
            # subtracts 0.1·load with load in 0–1, so production always exceeds consumption. The
            # ratio starts at 5.0 of 15.0 (0.333 normalised) and climbs to 1.0. Every threshold
            # written against it — the economy's reserve raise and native "protected" at < 0.3, the
            # heartbeat's self_recovery at < 0.3 and metabolic_throttle at < 0.2 — is therefore
            # unreachable for the whole life of the process. This states that where it is read.
            # W494 (refutation) — the first version asserted "never falls" flatly. That was FALSE while
            # the load was unvalidated: one fabric composition with metabolic_load=100 took this term
            # from 0.358 to 0.033. The load is now clamped to its declared 0-1 domain in both the
            # simulator and this class's entry, which is what makes the claim true — so the basis says
            # what the claim RESTS ON rather than asserting it as a bare fact.
            _atp_inert = ("the metabolic term is an ATPSimulator on a load clamped to its declared 0-1 "
                          "domain, where production (0.5 x efficiency, efficiency 0.8 or 1.0) always "
                          "exceeds consumption (0.1 x load), so within that domain it only rises — from "
                          "0.333 at boot to 1.0 — and the thresholds written against it cannot fire. It "
                          "is a simulation, not a reading of this platform's energy.")

            return {
                "composite_health": composite_health,
                # W494 — only the error fallback carried a basis, so the healthy path handed every
                # consumer a blended number with nothing attached. Each reader had to re-derive it.
                "composite_health_basis": (
                    f"{_measured_weight:.0%} of this figure's weight is measured (immune"
                    + ("" if sh_untracked else " and self-healing")
                    + "); the rest is "
                    + ("a self-healing term defaulted to 1.0 and " if sh_untracked else "")
                    + "a simulated metabolic term. The measured-only score is "
                    + f"{_measured_only}, and that is what decides the mode and every gate."),
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
                "mode_basis": _mode_basis,
                "composite_health_measured_weight": _measured_weight,
                "mode_decided_on": "composite_health_measured_only",
                # W494 (refutation) — these two fields disagreed with the gates the same round wrote.
                # `mode_decidable` was `_measured_weight >= 0.5`, which is False for the whole ordinary
                # life of a process (no circuit tracked), and its basis said a gate "should HOLD" —
                # while all three gates decide on `composite_health_measured_only is not None` and
                # grant. Publishing advice the platform does not follow is a claim it cannot back. The
                # field now says what the gates actually test, and the SHARE is reported separately as
                # the plain fact it is, with no instruction attached.
                "mode_decidable": _measured_only is not None,
                "mode_decidable_basis": (
                    f"at least one term is measured (immune"
                    + ("" if sh_untracked else " and self-healing")
                    + f"), so the mode and every gate decide on the measured-only score "
                    + f"{_measured_only}. This is the same test the gates apply."),
                "measured_weight_below_half": bool(_measured_weight < 0.5),
                "measured_weight_basis": (
                    f"{_measured_weight:.0%} of the blend's weight is measured"
                    + ("; no circuit is tracked yet, so self-healing is a default rather than a "
                       "reading, and the metabolic term is a simulation" if sh_untracked else
                       "; only the metabolic term is a simulation")
                    + ". This is the confidence behind the figure, not a rule about who may decide."),
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
                    # W494 (FU-117) — read by any surface or lever that quotes this number
                    "measured": False,
                    "can_fall": False,
                    "basis": _atp_inert,
                },
                "circadian": {
                    "cycle": cycle,
                    "is_peak_focus": cycle == "ACTIVE_FOCUS",
                },
                "recommended": {
                    "temperature": temperature,
                    # W494 — both of these branched on the blend, which cannot fall below 0.6 while a
                    # circuit registry is untracked, so neither could ever advise caution
                    "should_throttle": _decider < 0.5,
                    "max_parallel_agents": 3 if _decider >= 0.7 else 1,
                    "priority": "high" if cycle == "ACTIVE_FOCUS" else "normal",
                },
                "runtime_config": {
                    "rpm_limit": reconfig.get("gateway", {}).get("rpm_limit", 20),
                    "preferred_provider": reconfig.get("gateway", {}).get("preferred_provider", "auto"),
                    "features": reconfig.get("features", {}),
                },
                "health_summary": self._health_summary(_decider, mode, cycle,
                                                       measured_weight=_measured_weight,
                                                       blended=composite_health),
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
                # W494 — a fallback constant decided a mode, so the least healthy moment reported
                # NOMINAL. Nothing was measured here, so nothing decides: the mode is UNKNOWN and the
                # consumers that gate on it get an explicit "cannot decide" rather than a pass.
                "mode": "UNKNOWN",
                "mode_basis": ("nothing was measured — the organism context errored, so no mode is "
                               "decided; 0.9 is a fallback constant, not a reading"),
                "composite_health_measured_weight": 0.0,
                "mode_decided_on": None,
                "mode_decidable": False,
                "mode_decidable_basis": "the organism context errored: no term was measured",
                "measured_weight_below_half": True,
                "measured_weight_basis": "nothing was measured — 0.9 is a fallback constant",
                "error": str(e),
                "immune": {"health": None, "threat_level": "UNKNOWN", "errors_in_window": None},
                # W494 (found by the round's own pre-flight, `returns`) — W438 made this fallback
                # "shape-complete" for recommended/circadian and stopped there, so these two stayed
                # missing while organism_status.py:494 indexes ctx["self_healing"]["open_circuits"] and
                # ctx["nervous"]["arousal_state"]. That branch is entered on DEGRADED/EMERGENCY, which
                # the fallback's mode avoided by accident rather than by design. Complete now.
                "self_healing": {"overall_health": None, "open_circuits": None},
                "nervous": {"arousal_state": "UNKNOWN", "signal_rate": None, "signals_last_60s": None},
                "circadian": {"cycle": "UNKNOWN", "is_peak_focus": False},
                # W494 (refutation) — the success path's metabolic dict carries measured/can_fall/basis
                # and organism_status forwards ctx["metabolic"] verbatim, so on this path the API handed
                # consumers an atp figure with none of the qualifiers the round said travel with it.
                "metabolic": {"atp_ratio": None, "measured": False, "can_fall": False,
                              "basis": ("nothing was measured — the organism context errored, so no ATP "
                                        "reading was taken; the term is a simulation in any case")},
                # W494 (refutation) — clause (1) of this round's own rule is that where nothing was
                # measured the decision HOLDS rather than being granted. The success path was fixed and
                # this fallback was left granting full capacity on absent evidence: no throttle and two
                # parallel agents, read by the native homeostasis controller. It holds now.
                "recommended": {"should_throttle": True, "max_parallel_agents": 1,
                                "temperature": "precise", "priority": "normal",
                                "basis": ("nothing was measured — the organism context errored, so this "
                                          "advice HOLDS rather than granting capacity on absent "
                                          "evidence")},
                "runtime_config": {"rpm_limit": 20, "preferred_provider": "auto", "features": {}},
                # W494 (refutation) — this said "running at nominal" in the same dict whose mode had just
                # been changed to UNKNOWN because "a fallback constant decided a mode". It is the one
                # prose sentence both HTTP surfaces pass through, so the page showed the badge
                # "Not assessed" directly above a sentence claiming the organism was nominal.
                "health_summary": ("Organism context unavailable — nothing was measured, so no mode is "
                                   "decided; 0.9 is a fallback constant, not a reading."),
            }

    def _health_summary(self, health: float, mode: str, cycle: str,
                        measured_weight: float | None = None,
                        blended: float | None = None) -> str:
        """W494 (FU-110/FU-116) — the percentage in this sentence is the MEASURED figure, and the
        sentence says how much of the blend it covers. It used to quote the blended score, so the
        summary read "health 60% · Standard operations active" while the only measured term was 0.0
        and CRITICAL. "Full cognitive power available" is a claim about capacity nothing measured, so
        the FULL_POWER line no longer makes it."""
        summaries = {
            "FULL_POWER":  f"Organism at peak on what is measured — {cycle} cycle, measured health {health:.0%}.",
            "NOMINAL":     f"Organism nominal on what is measured — {cycle} cycle, measured health {health:.0%}.",
            "DEGRADED":    f"Organism under stress — measured health {health:.0%}. Reduced parallelism, precise mode.",
            "EMERGENCY":   f"Organism critical — measured health {health:.0%}. Emergency mode. Minimal operations only.",
        }
        out = summaries.get(mode, f"Organism measured health: {health:.0%}")
        if measured_weight is not None:
            out += (f" {measured_weight:.0%} of the composite's weight is measured"
                    + (f"; the blended figure is {blended:.0%}." if blended is not None else "."))
        return out

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
