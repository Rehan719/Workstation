import asyncio
from agentic_core.orchestration.biological_orchestrator import BiologicalOrchestrator

async def test_organism_task_execution():
    orchestrator = BiologicalOrchestrator()

    # Test a normal task
    task = {"name": "Analyze v60 stability", "priority": "reflex", "perplexity": 20.0}
    result = await orchestrator.execute_scientific_task(task)
    assert result["status"] == "success"
    print(f"Normal task result: {result}")

    # Test a high-threat task (simulated by high perplexity)
    threat_task = {"name": "Malicious code injection", "priority": "central", "perplexity": 60.0}
    threat_result = await orchestrator.execute_scientific_task(threat_task)
    assert threat_result["status"] == "aborted"
    print(f"Threat task result: {threat_result}")

if __name__ == "__main__":
    asyncio.run(test_organism_task_execution())
