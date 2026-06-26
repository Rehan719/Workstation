import asyncio
import logging
from agentic_core.orchestrator.synergy import SynergyOrchestrator
from agentic_core.reactor.ecosystem.registry import ReactorRegistry
from agentic_core.reactor.science.physics import PhysicsReactor
from agentic_core.reactor.religion.tafsir import TafsirReactor
from agentic_core.reactor.law.contract import ContractReactor
from agentic_core.reactor.employment.resume import ResumeReactor
from agentic_core.reactor.education.k12 import K12Reactor

logging.basicConfig(level=logging.INFO)

async def run_demos():
    orchestrator = SynergyOrchestrator()
    registry = ReactorRegistry()

    # Pre-register gold standards
    registry.register(PhysicsReactor())
    registry.register(TafsirReactor())
    registry.register(ContractReactor())
    registry.register(ResumeReactor())
    registry.register(K12Reactor())

    # 1. Startup Ecosystem Mega-Twin
    print("\n--- 1. Startup Ecosystem Mega-Twin ---")
    res1 = await orchestrator.execute_mega_twin(
        "Design Sharia-compliant Biotech Startup",
        ["law:contract", "religion:tafsir", "employment:resume"],
        "founder_jules"
    )
    print(f"Status: {res1['status']} | VTF: {res1['team_id']}")

    # 2. Educational Impact Mega-Twin
    print("\n--- 2. Educational Impact Mega-Twin ---")
    res2 = await orchestrator.execute_mega_twin(
        "Simulate Quantum Physics K-12 Learning Path",
        ["education:k12", "science:physics"],
        "student_anwa"
    )
    print(f"Status: {res2['status']} | VTF: {res2['team_id']}")

if __name__ == "__main__":
    asyncio.run(run_demos())
