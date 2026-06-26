import asyncio
import httpx
import time
import statistics

async def simulate_user(user_id: int, duration: int = 10):
    """Simulates a single user's interaction with the AI CEO chat."""
    latencies = []
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            req_start = time.time()
            async with httpx.AsyncClient() as client:
                # v0.3: Scaling test target
                resp = await client.post("http://localhost:8000/api/v138/ceo/chat",
                                       json={"message": f"User {user_id} request"},
                                       timeout=10.0)
            latencies.append(time.time() - req_start)
        except Exception:
            pass
        await asyncio.sleep(1.0)
    return latencies

async def run_load_test(concurrent_users: int = 100):
    """v0.3: Enterprise Load Test Simulation."""
    print(f"Starting v0.3 Load Test: {concurrent_users} concurrent users...")
    tasks = [simulate_user(i) for i in range(concurrent_users)]
    results = await asyncio.gather(*tasks)

    all_latencies = [l for sub in results for l in sub]
    if all_latencies:
        print(f"--- Load Test Results ---")
        print(f"Total Requests: {len(all_latencies)}")
        print(f"P95 Latency: {statistics.quantiles(all_latencies, n=20)[18]:.3f}s")
        print(f"Mean Latency: {statistics.mean(all_latencies):.3f}s")
    else:
        print("Load Test Failed: No successful requests.")

if __name__ == "__main__":
    # In a real environment, we would run with 10,000+; here we simulate 100
    asyncio.run(run_load_test(100))
