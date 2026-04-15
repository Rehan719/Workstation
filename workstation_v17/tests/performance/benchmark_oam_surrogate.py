import asyncio
import time
import numpy as np
from workstation_v17.core.quantum.surrogate import OAM_QKDSurrogate

async def main():
    surrogate = OAM_QKDSurrogate(n_modes=48)
    print("OAM: Starting Statistical Validation Benchmark (10,000 trials)...")
    start = time.time()
    results = surrogate.run_statistical_validation(10000)
    end = time.time()

    print(f"Benchmark duration: {end-start:.2f}s")
    print(f"QBER 95% CI Upper: {results['qber_ci_upper']:.4f}")
    print(f"Key Rate 95% CI Lower: {results['key_rate_ci_lower']:.4f}")
    print(f"Floor 20 Certification: {'PASSED' if results['passed'] else 'FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())
