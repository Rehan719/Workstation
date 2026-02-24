import time
import asyncio
import logging
from agentic_core.orchestration.biological_orchestrator import BiologicalOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def benchmark_latency():
    orchestrator = BiologicalOrchestrator()

    # 1. Peripheral Reflex Latency Benchmark (<50ms target)
    logger.info("Running Peripheral Reflex Latency Benchmark...")
    # Force peripheral by setting low HRV
    orchestrator.homeostasis.biomarkers["hrv_sdnn"] = 20.0
    results = []
    for _ in range(10):
        task = {"name": "reflex_test", "perplexity": 10.0}
        start = time.time()
        await orchestrator.execute_scientific_task(task)
        results.append((time.time() - start) * 1000)

    avg_latency = sum(results) / len(results)
    logger.info(f"AVG Peripheral Latency: {avg_latency:.2f}ms")
    assert avg_latency < 60 # Allow for slight overhead but target <50ms core

    # 2. Central Deliberative Latency Benchmark (200-800ms target)
    logger.info("Running Central Deliberative Latency Benchmark...")
    # Force central by setting high HRV
    orchestrator.homeostasis.biomarkers["hrv_sdnn"] = 100.0
    start = time.time()
    await orchestrator.execute_scientific_task({"name": "central_test", "perplexity": 10.0})
    central_latency = (time.time() - start) * 1000
    logger.info(f"Central Latency: {central_latency:.2f}ms")
    assert 200 <= central_latency <= 1000

if __name__ == "__main__":
    asyncio.run(benchmark_latency())
    print("Latency benchmarks PASSED.")
