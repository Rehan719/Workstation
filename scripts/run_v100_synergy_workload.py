import asyncio
import logging
from agentic_core.orchestrator.synergy import SynergyOrchestrator
from agentic_core.reactor.ecosystem.registry import ReactorRegistry
from agentic_core.reactor.science.biology import BiologyReactor
from agentic_core.reactor.religion.fiqh import FiqhReactor
from agentic_core.reactor.law.international import InternationalReactor
from agentic_core.reactor.science.engineering import EngineeringReactor
from agentic_core.reactor.science.environmental import EnvironmentalReactor
from agentic_core.reactor.religion.islamic_finance import Islamic_financeReactor
from agentic_core.reactor.employment.career_path import Career_pathReactor
from agentic_core.reactor.education.higher_ed import Higher_edReactor
from agentic_core.reactor.employment.skill_dev import Skill_devReactor

logging.basicConfig(level=logging.INFO)

async def run_workloads():
    orchestrator = SynergyOrchestrator()
    registry = ReactorRegistry()

    # Register required reactors
    registry.register(BiologyReactor())
    registry.register(FiqhReactor())
    registry.register(InternationalReactor())
    registry.register(EngineeringReactor())
    registry.register(EnvironmentalReactor())
    registry.register(Islamic_financeReactor())
    registry.register(Career_pathReactor())
    registry.register(Higher_edReactor())
    registry.register(Skill_devReactor())

    print("\n🚀 EXECUTING v100.0 APOTHEOSIS SYNERGY WORKLOADS")

    # 1. Bio-Ethics Legal Opinion
    print("\n--- [WORKFLOW 1] Bio-Ethics Legal Opinion ---")
    res1 = await orchestrator.execute_mega_twin(
        "Generate Bio-Ethics Legal Framework for CRISPR Research",
        ["science:biology", "religion:fiqh", "law:international"],
        "governance_board"
    )
    print(f"Outcome: {res1['message']} | VTF: {res1['team_id']}")

    # 2. Sustainable Engineering Project
    print("\n--- [WORKFLOW 2] Sustainable Engineering Project ---")
    res2 = await orchestrator.execute_mega_twin(
        "Design Sustainable Desalination Plant with Green Sukuk Funding",
        ["science:engineering", "science:environmental", "religion:islamic_finance"],
        "project_omega"
    )
    print(f"Outcome: {res2['message']} | VTF: {res2['team_id']}")

    # 3. Career-Education Pathway
    print("\n--- [WORKFLOW 3] Career-Education Pathway ---")
    res3 = await orchestrator.execute_mega_twin(
        "Map AI Engineering Career Path with Integrated Higher-Ed Degree",
        ["employment:career_path", "education:higher_ed", "employment:skill_dev"],
        "student_user"
    )
    print(f"Outcome: {res3['message']} | VTF: {res3['team_id']}")

if __name__ == "__main__":
    asyncio.run(run_workloads())
