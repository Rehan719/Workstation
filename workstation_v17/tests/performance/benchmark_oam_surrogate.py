import time
import numpy as np
from workstation_v17.core.quantum.surrogate import ClassicalOAMQKDSurrogate

async def benchmark():
    surrogate = ClassicalOAMQKDSurrogate(n_modes=48)
    print("OAM Surrogate Performance Benchmark: START")
    start = time.time()
    for _ in range(100):
        await surrogate.generate_secure_key(128)
    end = time.time()
    stats = surrogate.validate_statistical_thresholds()
    print(f"Benchmark Complete. Time per key: {(end-start)/100:.4f}s")
    print(f"Floor 20 Compliance: {stats}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(benchmark())
