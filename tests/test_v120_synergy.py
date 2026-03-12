import asyncio
import logging
import pytest
from agentic_core.orchestrator.synergy import SynergyOrchestrator

@pytest.mark.asyncio
async def test_synergy():
    logging.basicConfig(level=logging.INFO)
    orchestrator = SynergyOrchestrator()

    reactors = ["science:physics", "religion:quranic_studies", "law:corporate_law"]
    objective = "Verify cross-domain impact of a new educational policy on startup growth."

    result = await orchestrator.execute_mega_twin(
        objective=objective,
        reactors=reactors,
        user_id="user_123",
        domain="startup_ecosystem",
        tier="free"
    )

    print("\n--- Synergy Execution Result ---")
    print(f"Status: {result['status']}")
    print(f"Team ID: {result['team_id']}")
    print(f"Pool ID: {result['pool_id']}")
    print(f"Average Fidelity: {result['avg_fidelity']:.4f}")
    print(f"Message: {result['message']}")
    print("--------------------------------\n")

if __name__ == "__main__":
    asyncio.run(test_synergy())
