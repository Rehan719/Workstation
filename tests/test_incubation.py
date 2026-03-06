import asyncio
from agentic_core.incubation.adaptive_incubation_engine import AdaptiveIncubationEngine

async def test_incubation_flow():
    engine = AdaptiveIncubationEngine()
    result = await engine.start_incubation(
        goal="Generate a report on v60 biological systems",
        constraints={"duration": "1h"}
    )

    assert result["status"] == "incubating"
    assert result["goal"] == "Generate a report on v60 biological systems"
    print("Incubation flow test PASSED.")

if __name__ == "__main__":
    asyncio.run(test_incubation_flow())
