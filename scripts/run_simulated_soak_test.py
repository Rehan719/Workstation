import time
import logging
from agentic_core.twinning.reactor_twin import ReactorTwin
from agentic_core.optimization.aro_engine import AROEngine
from agentic_core.teams.team_orchestrator import TeamOrchestrator
from agentic_core.drad.assembler import DRADAssembler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SoakTest")

def run_soak():
    logger.info("Starting 72-hour simulated soak test (compressed)...")

    twin = ReactorTwin("global_twin")
    aro = AROEngine()
    teams = TeamOrchestrator()
    drad = DRADAssembler()

    # Simulate 72 hours in 7.2 seconds (10h per second)
    for i in range(72):
        logger.info(f"Simulating hour {i+1}...")

        # Twinning sync
        twin.sync_telemetry({"load": i % 10, "health": 1.0})

        # ARO allocation
        aro.allocate_resources(f"task_{i}", priority=(i % 3) + 1)

        # Team formation
        if i % 10 == 0:
            teams.form_team(["scholar", "validator"], f"obj_{i}")

        # DRAD assembly/disassembly
        res_id = drad.assemble_resource({"type": "ephemeral"})
        drad.disassemble_resource(res_id)

        # Check metrics
        assert aro.compute_waste() <= 0.05
        assert twin.current_fidelity >= 0.98

        time.sleep(0.1) # Compression factor

    logger.info("72-hour simulated soak test PASSED.")

if __name__ == "__main__":
    run_soak()
