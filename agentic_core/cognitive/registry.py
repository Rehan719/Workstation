from enum import Enum
from typing import Dict, Any, Type, List


class EngineTier(str, Enum):
    """The five tiers. A tier is a property of an engine, not a place to keep it."""
    FOUNDATIONAL = "foundational"
    META = "meta"
    AUXILIARY = "auxiliary"
    MJM = "mjm"
    BME = "bme"


class EngineType(str, Enum):
    """All twenty-three engines the architecture declares — Owner ruling 2026-09-30.

    This enum was NINE while `docs/COGNITIVE_ENGINE_ARCHITECTURE.md:15` declared twelve, so the entire
    auxiliary tier was missing and the registry could not report engines the architecture names. Declaring
    them does not build them: seventeen have no module, and `register_all()` reports each as absent.
    """
    # ── foundational (6) — these have modules and run, returning stated refusals (P3.12, W520)
    INKASHAF = "inkashaf"
    AQAL = "aqal"
    SAMAJH = "samajh"
    HOSHIYARI = "hoshiyari"
    SOCH = "soch"
    IMAN = "iman"
    # ── meta-regulative (3) — no module yet; built by P3.13 as refusals by default
    TAWAZUN = "tawazun"
    NIYYAH = "niyyah"
    TAFAKKUR = "tafakkur"
    # ── auxiliary (3) — built by P3.16. MUSHAWARA is deliberation and gate 1 of the clearance chain;
    #    it is NOT Mushahida, which is MJM's observation stage below.
    TAHQEEQ = "tahqeeq"
    MUSHAWARA = "mushawara"
    MUDRIK = "mudrik"
    # ── MJM (3) — Mushahida/Jaiza/Muaina. They exist as METHODS on MJMOrchestratorV4 today, which the
    #    Owner ruled stays as their composer; as engines they are unbuilt.
    MUSHAHIDA = "mushahida"
    JAIZA = "jaiza"
    MUAINA = "muaina"
    # ── BME (8) — the Biomimetic Minimisation Engine's terms (architecture doc Part II, line 179).
    #    OMEGA_FUNCTIONAL is both the eighth engine and the composer of five of the others, and it weights
    #    only five: DIFFUSION_PROCESS, LEAST_ACTION and LANDAUER_METER sit outside its weighted sum.
    VARIATIONAL_FREE_ENERGY = "variational_free_energy"
    SCHRODINGER_BRIDGE = "schrodinger_bridge"
    ENTROPIC_OPTIMAL_TRANSPORT = "entropic_optimal_transport"
    DIFFUSION_PROCESS = "diffusion_process"
    LEAST_ACTION = "least_action"
    MURRAY_LAW = "murray_law"
    LANDAUER_METER = "landauer_meter"
    OMEGA_FUNCTIONAL = "omega_functional"


#  Which tier each engine belongs to. Every EngineType member appears exactly once; a guard asserts that,
#  because a partial map would let a tier count silently omit an engine.
ENGINE_TIERS: Dict[EngineType, EngineTier] = {
    EngineType.INKASHAF: EngineTier.FOUNDATIONAL,
    EngineType.AQAL: EngineTier.FOUNDATIONAL,
    EngineType.SAMAJH: EngineTier.FOUNDATIONAL,
    EngineType.HOSHIYARI: EngineTier.FOUNDATIONAL,
    EngineType.SOCH: EngineTier.FOUNDATIONAL,
    EngineType.IMAN: EngineTier.FOUNDATIONAL,
    EngineType.TAWAZUN: EngineTier.META,
    EngineType.NIYYAH: EngineTier.META,
    EngineType.TAFAKKUR: EngineTier.META,
    EngineType.TAHQEEQ: EngineTier.AUXILIARY,
    EngineType.MUSHAWARA: EngineTier.AUXILIARY,
    EngineType.MUDRIK: EngineTier.AUXILIARY,
    EngineType.MUSHAHIDA: EngineTier.MJM,
    EngineType.JAIZA: EngineTier.MJM,
    EngineType.MUAINA: EngineTier.MJM,
    EngineType.VARIATIONAL_FREE_ENERGY: EngineTier.BME,
    EngineType.SCHRODINGER_BRIDGE: EngineTier.BME,
    EngineType.ENTROPIC_OPTIMAL_TRANSPORT: EngineTier.BME,
    EngineType.DIFFUSION_PROCESS: EngineTier.BME,
    EngineType.LEAST_ACTION: EngineTier.BME,
    EngineType.MURRAY_LAW: EngineTier.BME,
    EngineType.LANDAUER_METER: EngineTier.BME,
    EngineType.OMEGA_FUNCTIONAL: EngineTier.BME,
}

class CognitiveEngineRegistry:
    _engines = {}
    _bootstrap_attempted = False
    _bootstrap_report = None

    @classmethod
    def register(cls, engine_type, engine_instance): cls._engines[engine_type] = engine_instance

    @classmethod
    def _bootstrap(cls):
        """Populate from the engine modules that exist — once, on the first miss.

        WHY THIS EXISTS AT ALL. FU-221's defect was that nothing ever populated this registry, so every
        live reader was told no engine existed. W520 wrote the populator (`agentic_core.cognitive.
        register_all`) and then measured that the ONLY caller was its own guard — which means the guard was
        creating the condition it went on to assert, and production was left exactly as broken as before.
        A populator nothing invokes is not a fix.

        WHY LAZILY RATHER THAN AT PACKAGE IMPORT. `register_all` imports six engine modules, and those pull
        in the consultation contract and the biomimicry decorators. Doing that from this module's package
        `__init__` would make importing the bare enum drag the whole stack in, on an import path that
        already has a cycle available to it. On the first miss there is no such ordering to get wrong.

        Never raises: a registry that throws on one engine's import leaves every other reader with none.
        `_bootstrap_attempted` is set BEFORE the work, so a re-entrant `get` cannot loop.
        """
        cls._bootstrap_attempted = True
        try:
            import importlib
            cls._bootstrap_report = importlib.import_module("agentic_core.cognitive").register_all()
        except Exception as exc:                          # noqa: BLE001 — reported, never silently skipped
            cls._bootstrap_report = {"bootstrap_failed": f"{exc.__class__.__name__}: {exc}"}
        return cls._bootstrap_report

    @classmethod
    def report(cls):
        """What registration actually found — bootstrapping once if nothing has yet.

        A surface that wants to say how many engines exist should ask THIS rather than keep its own list:
        `agentic_core/api/cognitive.py` kept a parallel table and reported six while this registry held
        zero, which is how FU-221 stayed invisible. Bootstrapping happens once per process, so a route may
        call this per request without re-instantiating six engines each time.
        """
        if not cls._bootstrap_attempted:
            cls._bootstrap()
        return dict(cls._bootstrap_report or {})

    @classmethod
    def get(cls, engine_type):
        if engine_type not in cls._engines and not cls._bootstrap_attempted:
            cls._bootstrap()
        if engine_type not in cls._engines:
            # The reason matters: an engine DECLARED in EngineType with no module is a different fact from
            # one whose import failed, and a bare "not found" made the two indistinguishable.
            rep = cls._bootstrap_report or {}
            name = getattr(engine_type, "value", engine_type)
            if name in (rep.get("declared_but_absent") or []):
                raise ValueError(
                    f"Engine {name} is declared in EngineType and has NO module: nothing can consult it. "
                    f"{rep.get('declared_but_absent_basis', {}).get(name, '')}".strip())
            why = (rep.get("unavailable") or {}).get(name) or rep.get("bootstrap_failed")
            raise ValueError(f"Engine {engine_type} not found"
                             + (f" — registration reported: {why}" if why else ""))
        return cls._engines[engine_type]
