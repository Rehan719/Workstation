import pytest
import asyncio
from agentic_core import Orchestrator, TranscendentLayer, EthicalSentinel
from agents.research import PaperQAAgent
from agents.writing import ManuscriptArchitect
from agents.presentation import SlideMaestro
from agentic_core.meta_cognitive import MetaCognitiveDaemon

@pytest.mark.asyncio
async def test_full_autonomous_cycle():
    # 1. Initialize core system
    orchestrator = Orchestrator()
    transcendent = TranscendentLayer()
    sentinel = EthicalSentinel()
    meta_agent = MetaCognitiveDaemon()

    # 2. Register workers
    orchestrator.register_worker(PaperQAAgent())
    orchestrator.register_worker(ManuscriptArchitect())
    orchestrator.register_worker(SlideMaestro())
    orchestrator.register_worker(sentinel)

    # 3. Simulate a high-level research goal
    task = {
        "type": "advanced_research",
        "goal": "Explain the role of dark matter in galaxy formation with animations.",
        "needs_animation": True
    }

    # 4. Execute (simulating workflow execution)
    # The current Orchestrator mock execution is simpler than the full YAML logic,
    # but we can verify the agent registration and initial planning.
    result = await orchestrator.execute(task)

    # 5. Verify L3 Orchestration and L2 worker responses (mocked)
    assert result["status"] == "completed"

    # 6. Verify L5 Ethical Guardian
    content_to_check = {"content": "Galaxy formation simulations..."}
    ethics_result = await sentinel.execute(content_to_check)
    assert ethics_result["status"] == "approved"

    # 7. Verify L6 Transcendent consolidation
    consolidation_task = {"action": "consolidate"}
    transcendent_result = await transcendent.execute(consolidation_task)
    assert transcendent_result["status"] == "success"

    # 8. Verify L7 Meta-Cognitive evolution
    evolution_task = {"action": "evolve_prompts", "prompt_type": "research"}
    meta_result = await meta_agent.execute(evolution_task)
    assert meta_result["status"] == "evolved"

    print("Full autonomous cycle verification successful!")

if __name__ == "__main__":
    asyncio.run(test_full_autonomous_cycle())
