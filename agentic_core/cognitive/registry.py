from enum import Enum
from typing import Dict, Any, Type, List

class EngineType(str, Enum):
    INKASHAF = "inkashaf"
    AQAL = "aqal"
    SAMAJH = "samajh"
    HOSHIYARI = "hoshiyari"
    SOCH = "soch"
    IMAN = "iman"
    TAWAZUN = "tawazun"
    NIYYAH = "niyyah"
    TAFAKKUR = "tafakkur"

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
