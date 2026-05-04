import asyncio
from agentic_core.consultation.interface import ConsultationRequest, UrgencyLevel
from agentic_core.consultation.uc_consult import UCIConsultHandler
from agentic_core.consultation.mushawara.consultation_orchestrator import MushawaraOrchestrator
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4
from agentic_core.nemoclaw_runtime import NemoclawRuntime
from agentic_core.cognitive.inkashaf_engine import InkashafEngine
from agentic_core.cognitive.aqal_engine import AqalEngine
from agentic_core.cognitive.samajh_engine import SamajhEngine
from agentic_core.mjm.mjm import MJMOrchestratorV4

async def test_mushawara_e2e_session():
    # Setup
    gaas = GaaSValidatorV4(
        genome_path="configs/constitutional_genome_v138.yaml",
        legal_path="configs/legal_precision.yaml"
    )
    nemoclaw = NemoclawRuntime()
    uci = UCIConsultHandler(gaas=gaas)

    # Register Engines
    uci.register_engine("inkashaf", InkashafEngine())
    uci.register_engine("aqal", AqalEngine())
    uci.register_engine("samajh", SamajhEngine())
    uci.register_engine("mjm", MJMOrchestratorV4())

    orchestrator = MushawaraOrchestrator(gaas=gaas, nemoclaw=nemoclaw, uci_handler=uci)

    # Execute
    query = "Optimize workplace diversity policy for UK Employment Tribunal compliance"
    participants = ["inkashaf", "aqal", "samajh", "mjm"]

    response = await orchestrator.initiate_session(
        query=query,
        participants=participants,
        domain="legal",
        context={"jurisdiction": "UK"}
    )

    # Assertions
    print(f"\nConstitutional Validation Passed: {response.constitutional_validation.passed}")
    print(f"Violations: {response.constitutional_validation.violations}")
    print(f"Synthesized Answer: {response.answer}")
    print(f"Confidence: {response.confidence}")

    assert response.confidence > 0.0
    print("SUCCESS")

if __name__ == "__main__":
    asyncio.run(test_mushawara_e2e_session())
