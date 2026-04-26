import asyncio
import json
import os
import sys
import logging

# Ensure agentic_core is in path
sys.path.append(os.getcwd())

from agentic_core.biomimicry.cycles.water_cycle import HydrologicResourceManager
from agentic_core.biomimicry.cycles.carbon_cycle import CarbonDataMetabolism
from agentic_core.biomimicry.cycles.geospheric_orchestrator import GeosphericHomeostaticOrchestrator
from agentic_core.biomimicry.cycles.psi_functional import EcosystemHealthObjective
from agentic_core.crypto.entropy_pool import EntropyPool
from agentic_core.quantum.surrogate import OAM_QKDSurrogate
from agentic_core.mjm.v5.omni_learner_v5 import MJMv5OmniLearner
from agentic_core.change_control import get_regulator, get_reconfigulator

async def test_master_convergence():
    print("--- Testing Master Convergence v∞ ---")

    # 1. Geospheric Hardening
    entropy = EntropyPool()
    orchestrator = GeosphericHomeostaticOrchestrator(entropy_pool=entropy)

    inputs = {
        "current_temp": 350.0,
        "heat_load": 100.0,
        "raw_data_size": 10.0,
        "process_load": 1.0,
        "metabolic_state": "active",
        "input_count": 5,
        "data_to_memory": 2.0,
        "error_severity": 0.1
    }
    context = {
        "system_metrics": {"free_energy": 0.9},
        "legal_compliance": 1.0
    }

    res = orchestrator.step(inputs, context)
    assert res["psi_score"] > 0
    assert res["stability_index"] < 0.5
    print("✅ Geospheric Orchestration: OK")

    # 2. Change Control Consolidation
    reg = get_regulator()
    reconf = get_reconfigulator()

    fault = {"type": "state_mismatch", "component_id": "L9"}
    repaired = await reg.repair(fault, tier="MMR")
    assert repaired["repair_status"] == "reconciled"

    code = "def production_logic(): return True"
    g_hash = await reconf.replicate(code)
    assert len(g_hash) == 128
    print("✅ Change Control Consolidation: OK")

    # 3. Evolution Hardening
    learner = MJMv5OmniLearner(max_depth=5)
    evolved = await learner.evolve({"stabilized": False})
    assert evolved["depth_reached"] <= 5
    print("✅ Evolution Hardening: OK")

    # 4. CLI Integration
    import subprocess
    cli_res = subprocess.run(["python3", "bin/sovereignctl", "status"], capture_output=True, text=True)
    # Check for unicode or version string
    assert "v139.0.0" in cli_res.stdout
    print("✅ CLI Status Check: OK")

async def main():
    try:
        await test_master_convergence()
        print("\n🏆 JULES v∞ MASTER CONVERGED 🏆")
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
