import asyncio
import logging
from agentic_core.synthesis.uviap import UVIAP

logging.basicConfig(level=logging.INFO)

async def main():
    """v125.0: Helper script to trigger QEP source ingestion."""
    print("🧬 Jules AI: Triggering v125.0 QEP Ingestion Pipeline...")
    uviap = UVIAP()
    await uviap.run_full_pipeline(modes=["ingest-urls", "ingest-local", "rectify-qep-insights"])
    print("✅ Ingestion and Rectification complete.")

if __name__ == "__main__":
    asyncio.run(main())
