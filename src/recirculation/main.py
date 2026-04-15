import asyncio
import logging
from src.recirculation.engine.engine import RecirculationEngine
from src.recirculation.gateway.gateway import IsomorphicGateway, AlphaFoldStub, InSilicoScreeningSimulator, ParticleDynamicsSimulator
from src.recirculation.adapters.biotech import KnowledgeGraphSeed
from src.recirculation.interfaces.protocols import HolographicInterface, VideoStreamAnalyzer, HapticController
from src.recirculation.evolution.agent import EvolutionAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JULES-ORCHESTRATOR")

class JulesOmegaOrchestrator:
    def __init__(self):
        self.gateway = IsomorphicGateway()
        self.knowledge = KnowledgeGraphSeed()
        self.engine = RecirculationEngine()
        self.evolution = EvolutionAgent()
        self.interfaces = {
            "holographic": HolographicInterface(),
            "video": VideoStreamAnalyzer(),
            "haptic": HapticController()
        }

    def setup(self):
        logger.info("Initializing Ω-RECURSION FABRIC...")
        self.gateway.register_adapter("biology", "alphafold", AlphaFoldStub())
        self.gateway.register_adapter("biology", "insilico_screening", InSilicoScreeningSimulator())
        self.gateway.register_adapter("physics", "particle_dynamics", ParticleDynamicsSimulator())

    async def run_initial_cycle(self):
        self.setup()

        # Start the engine in a background task
        engine_task = asyncio.create_task(self.engine.start())

        # Give it a moment to initialize
        await asyncio.sleep(2)

        logger.info("TESTING RECIRCULATION FABRIC ON BIOTECH TASK: Lead Optimization")

        # 1. SENSE/QUERY KNOWLEDGE
        finding = self.knowledge.query("Compound_X")
        logger.info(f"Initial Finding: {finding}")

        # 2. ACT/SIMULATE via GATEWAY
        sequence = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
        structure_res = await self.gateway.route("biology", "alphafold", sequence)
        logger.info(f"AlphaFold Result Latent Vector Size: {len(structure_res['latent_tensor'])}")

        screening_res = await self.gateway.route("biology", "insilico_screening", "CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F")
        logger.info(f"Screening Result: {screening_res['result']}")

        # 3. INTERFACE/VISUALIZE
        await self.interfaces["holographic"].render_scene("SCENE-001", [
            {"type": "Protein", "position": (0,0,0), "properties": {"sequence": "MQIF..."}},
            {"type": "Ligand", "position": (0.5, 0.2, 0.1), "properties": {"smiles": "CC1..."}}
        ])

        await self.interfaces["haptic"].trigger_feedback(0.8, 440, "Right Hand")

        # 4. EVOLVE (Simulated check)
        analysis = await self.evolution.analyze_performance([{"duration_s": 5.0}])
        logger.info(f"Evolution Analysis: {analysis}")

        logger.info("INITIAL TEST CYCLE COMPLETE.")

        # Shutdown
        self.engine.stop()
        await engine_task

if __name__ == "__main__":
    orchestrator = JulesOmegaOrchestrator()
    asyncio.run(orchestrator.run_initial_cycle())
