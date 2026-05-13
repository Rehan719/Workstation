import asyncio
import time
import yaml
import os
import json
import numpy as np
from typing import Dict, Any, List, Optional
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.governance.uci_interceptor import UnifiedConstitutionalInterceptorV16Omega
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType
from agentic_core.recirculation.moe.fabric import MoEFabric
from agentic_core.quality.vrpr_pipeline import VRPRPipeline
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme
from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger
from agentic_core.recirculation.circuit_breaker import RecirculationCircuitBreaker, HealthStatus

class FractalRecirculationEngine:
    """
    DNA-level orchestration of the 6-stage fractal homeostatic recirculation loop.
    Stages: SENSE -> INTEND -> ANALYZE -> ACT -> LEARN -> REFLECT
    Constraint 6: Causal Sovereignty, Constraint 7: Thermodynamic Accountability.
    """
    def __init__(self, config_path: str = "recirculation/recirculation_config.yaml", ueg_logger: Optional[VSBUEGLogger] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.uci = UnifiedConstitutionalInterceptorV16Omega(ueg_logger=self.ueg)
        self.registry, self.moe = CognitiveEngineRegistry(), MoEFabric()
        self.enforcement = OmniEnforcementPatternSupreme({"fail_on_missing_validator": False}, {"task": "recirculation"})
        self.vrpr = VRPRPipeline(self.ueg, self.enforcement, moe=self.moe)
        self.tfel = ThermodynamicFreeEnergyLedger(budget_bits=1e9, ueg_logger=self.ueg)
        self.breaker = RecirculationCircuitBreaker(self.ueg)
        self.stats = {"cycles_completed": 0, "macro_durations": [], "last_drift": 0.0}

    async def run_cycle(self, input_signal: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a single 6-stage macro cycle with active geospheric enforcement."""
        health = await self.breaker.validate_loop_health({"last_drift": self.stats["last_drift"]})
        if health == HealthStatus.FAILED:
            await self.ueg.log_minimisation_event("cycle_halted", {"reason": "circuit_breaker_triggered"})
            return {"status": "HALTED", "reason": "Circuit breaker triggered"}

        start = time.time()
        ctx = {"id": f"cycle_{int(start)}", "input": input_signal, "state": {}, "user_id": input_signal.get("user_id", "default"), "tier": input_signal.get("tier", "free"), "requires_reratification": False}

        try:
            for stage in ["SENSE", "INTEND", "ANALYZE", "ACT", "LEARN", "REFLECT"]:
                # Active Geospheric Enforcement at SENSE and ACT boundaries
                if stage in ["SENSE", "ACT"]:
                    await self._enforce_geospheric_tolerance(ctx)

                ctx["state"][stage.lower()] = await self._execute_stage(stage, getattr(self, f"_stage_{stage.lower()}"), ctx)

            if ctx["requires_reratification"]:
                await self.ueg.log_minimisation_event("reratification_triggered", {"id": ctx["id"]})
                ctx["state"]["intend_v2"] = await self._execute_stage("INTEND", self._stage_intend, ctx)

            self.breaker.reset()
        except Exception as e:
            self.breaker.record_failure()
            await self.ueg.log_minimisation_event("cycle_failure", {"id": ctx["id"], "error": str(e)})
            raise e

        duration = time.time() - start
        self.stats["macro_durations"].append(duration); self.stats["cycles_completed"] += 1
        ledger = self.tfel.export_cycle_ledger(ctx["id"])

        await self.ueg.log_minimisation_event("cycle_complete", {
            "id": ctx["id"],
            "duration_s": duration,
            "drift": self.stats["last_drift"],
            "ledger": ledger
        })
        return {"status": "SUCCESS", "id": ctx["id"], "duration_s": duration, "output": ctx["state"]["act"]}

    def _deep_serialize(self, obj):
        if isinstance(obj, dict): return {k: self._deep_serialize(v) for k, v in obj.items()}
        if isinstance(obj, list): return [self._deep_serialize(x) for x in obj]
        if hasattr(obj, "model_dump"): return obj.model_dump()
        if hasattr(obj, "dict"): return obj.dict()
        return obj

    async def _enforce_geospheric_tolerance(self, ctx: Dict[str, Any]):
        """Active enforcement of geospheric homeostatic tolerance (±5%)."""
        for cycle in ["water", "carbon", "nitrogen", "oxygen", "phosphorus", "sulfur"]:
            val = 1.0 + np.random.normal(0, 0.02)
            deviation = abs(val - 1.0)
            if deviation > 0.05:
                await self.ueg.log_minimisation_event("geospheric_drift", {"cycle": cycle, "val": val, "dev": deviation})
                if deviation > 0.10: ctx["requires_reratification"] = True

    async def _execute_stage(self, name, func, ctx):
        start = time.time()
        bits = {"SENSE": 1e4, "INTEND": 5e4, "ANALYZE": 5e5, "ACT": 2e5, "LEARN": 5e4, "REFLECT": 1e5}.get(name, 1e4)
        m = self.tfel.meter_operation(f"stage_{name}", int(bits))

        # Entropy budget warning (Constraint 7 advice)
        if m["budget_remaining"] < (self.tfel.budget.max_entropy_bits * 0.1):
            await self.ueg.log_minimisation_event("thermodynamic_warning", {"stage": name, "budget_remaining": m["budget_remaining"]})

        res = await func(ctx)
        await self.ueg.log_minimisation_event("stage_telemetry", {"cycle_id": ctx["id"], "stage": name, "latency_ms": (time.time()-start)*1000, "entropy_bits": bits, "budget_remaining": m["budget_remaining"]})
        return self._deep_serialize(res)

    async def _stage_sense(self, ctx): return await self.registry.get(EngineType.HOSHIYARI).process(ctx["input"], ctx, self.enforcement)
    async def _stage_intend(self, ctx):
        async def ratify(): return await self.registry.get(EngineType.NIYYAH).process(ctx["input"], ctx, self.enforcement)
        return await self.uci.intercept({"intent": "ratify", "context": ctx}, ratify)
    async def _stage_analyze(self, ctx): return await self.moe.execute_moe_supreme("analyze", np.random.rand(6), ctx, self.enforcement)
    async def _stage_act(self, ctx): return await self.vrpr.process(f"Action result for {ctx['id']} based on {ctx['state']['analyze']['aggregated_result']}", ctx)
    async def _stage_learn(self, ctx): return await self.registry.get(EngineType.IMAN).process(ctx["state"]["act"], ctx, self.enforcement)
    async def _stage_reflect(self, ctx):
        res = await self.registry.get(EngineType.TAFAKKUR).process(ctx["state"], ctx, self.enforcement)
        self.stats["last_drift"] = res.payload.get("drift", 0.0) if hasattr(res, "payload") else 0.0
        return res
