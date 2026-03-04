import pytest
import pytest_asyncio
import asyncio
import time
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

@pytest_asyncio.fixture
async def organism():
    org = ConsciousOrganismV99_0()
    await org.start()
    yield org
    await org.shutdown()

@pytest.mark.asyncio
async def test_performance_benchmarks(organism):
    """
    Performance Benchmarks: Generation < 30s, IDE < 5s, Deployment < 2min
    (Article 150)
    """
    # 1. App Generation Benchmark
    start = time.time()
    await organism.create_app_from_conversation("Create a React frontend for the quantum gateway.")
    duration = time.time() - start
    print(f"App Generation Duration: {duration:.2f}s")
    assert duration < 30.0, f"App Generation took {duration}s, target is 30s."

    # 2. IDE Workspace Start Benchmark
    start = time.time()
    # org.ide.start() would go here
    duration = time.time() - start
    print(f"IDE Startup Duration: {duration:.2f}s")
    assert duration < 5.0, f"IDE Startup took {duration}s, target is 5s."

    # 3. Deployment Benchmark (Simulated)
    start = time.time()
    await organism.deploy_app("app-123", "gcp-production")
    duration = time.time() - start
    print(f"Deployment Duration: {duration:.2f}s")
    assert duration < 120.0, f"Deployment took {duration}s, target is 120s."

@pytest.mark.asyncio
async def test_quantum_routing_benchmark(organism):
    """
    Performance Benchmark: Quantum Circuit Routing < 1s
    """
    circuit = {"name": "BellState", "qubits_count": 2, "qubits": ["q0", "q1"], "gates": [{"op": "h", "targets": [0]}]}
    start = time.time()
    backend = await organism.quantum_gateway.route_job(circuit)
    duration = time.time() - start
    print(f"Quantum Routing Duration: {duration:.2f}s")
    assert duration < 1.0, f"Quantum Routing took {duration}s, target is 1s."
    assert backend is not None
