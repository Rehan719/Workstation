import asyncio
import logging
from agentic_core.main import app
import httpx
from uvicorn import Config, Server

async def verify_backend():
    logging.basicConfig(level=logging.INFO)

    config = Config(app=app, host="127.0.0.1", port=8000, log_level="info")
    server = Server(config=config)

    # Run server in background
    loop = asyncio.get_event_loop()
    server_task = loop.create_task(server.serve())

    # Wait for server to start
    await asyncio.sleep(2)

    async with httpx.AsyncClient() as client:
        # 1. Health check
        res = await client.get("http://127.0.0.1:8000/health")
        print(f"Health: {res.json()}")
        assert res.json()["version"] == "120.0.0"

        # 2. QEP Ayah check
        print("Testing QEP Ayah...")
        res = await client.get("http://127.0.0.1:8000/api/v1/qep/ayah/1:1")
        print(f"Ayah 1:1: {res.json()['translation']}")
        assert "Merciful" in res.json()["translation"]

        # 3. Governance check
        print("Testing Governance...")
        res = await client.get("http://127.0.0.1:8000/api/v1/governance/okrs")
        print(f"Governance Report: {res.json()['global_pas']}")
        assert res.json()["global_pas"] >= 0.0

    print("Backend Verification SUCCESSFUL.")
    server.should_exit = True
    await server_task

if __name__ == "__main__":
    asyncio.run(verify_backend())
