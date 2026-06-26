import asyncio
import logging
from core.business.living_strategy_system import LivingStrategySystem

async def main():
    logging.basicConfig(level=logging.INFO)
    lss = LivingStrategySystem()
    while True:
        await lss.run_reflection_cycle()
        # Run every 7 virtual days (simulated) or 1 hour real-time for the demo
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
