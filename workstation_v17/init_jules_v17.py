#!/usr/bin/env python3
"""Initialization script for JULES v17.0 Final Beta."""
import asyncio
import argparse
import sys
import os
import logging

# Ensure project root and workstation_v17 are in path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "workstation_v17"))

from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17

async def main():
    parser = argparse.ArgumentParser(description="JULES v17.0 Final Beta Initialization")
    parser.add_argument("--role", default="opus_central_director")
    parser.add_argument("--vertical", default="biotech_materials_discovery_and_uk_employment_law")
    parser.add_argument("--fractal_scaling", default="enabled")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("JULES_BOOT")

    logger.info(f"🟢 INITIALIZING JULES v17.0 FINAL BETA")
    logger.info(f"Role: {args.role} | Vertical: {args.vertical}")

    organism = JulesOmegaOrganismV17(config_path="config/constitutional_genome_v17.yaml")

    try:
        await organism.initialize()

        # Run first validation cycle
        logger.info("Executing First Macro-cycle (Golden Master II Validation)...")
        result = await organism.run_recirculation_cycle({
            "text": f"Optimizing {args.vertical}",
            "goal": "Golden Master II Discovery"
        })

        logger.info(f"Cycle 1 Complete. Status: {result['status']} | Neural Gain: {result['gain']}")

        # Enter infinite loop (simulated here for one more cycle)
        # while True: await asyncio.sleep(60)

    except Exception as e:
        logger.error(f"Critical failure during initialization: {e}")
    finally:
        await organism.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
