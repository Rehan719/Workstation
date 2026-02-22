from typing import Any, Dict, List, Optional
import asyncio
import logging
import yaml
import os
import random
from datetime import datetime
from ..observatory.observatory import Observatory
from .evolution_nexus import EvolutionNexus

class SelfImprovementEngine:
    """
    v52.0 Self-Improvement Engine: Autonomous Intelligence Amplification.
    Manages the Real-Time Signals Loop and Scheduled Batch Analysis.
    v52.0 Expansion: Functional parameter mutation and recalibration.
    """
    def __init__(self, observatory: Observatory, evolution_nexus: EvolutionNexus):
        self.observatory = observatory
        self.evolution_nexus = evolution_nexus
        self.is_running = False
        self.logger = logging.getLogger("self_improvement")
        self.config_path = "config/evolution/genotype.yaml"

    async def start_signals_loop(self):
        """
        Real-Time Signals Loop: Ingests telemetry and triggers rapid recalibration.
        """
        self.is_running = True
        self.logger.info("Starting v52.0 Real-Time Signals Loop...")
        while self.is_running:
            signals = await self.observatory.capture_live_telemetry()
            if self._should_recalibrate(signals):
                await self._perform_rapid_recalibration(signals)
            await asyncio.sleep(60)

    async def run_batch_analysis(self):
        """
        Scheduled Batch Analysis: Runs evolutionary mutation on the system codebase.
        """
        self.logger.info("Initiating v52.0 Scheduled Batch Analysis...")
        current_genotype = self._load_genotype()

        mutations = await self.evolution_nexus.propose_mutations(current_genotype)

        for mutation in mutations:
            if await self.evolution_nexus.verify_in_sandbox(mutation):
                self.logger.info(f"Applying verified mutation: {mutation['id']}")
                self._apply_mutation_to_config(mutation)
            else:
                self.logger.warning(f"Mutation {mutation['id']} failed sandbox verification.")

    def _should_recalibrate(self, signals: Dict[str, Any]) -> bool:
        error_rate = signals.get("error_rate", 0.0)
        return error_rate > 0.05

    async def _perform_rapid_recalibration(self, signals: Dict[str, Any]):
        self.logger.info("Performing rapid recalibration based on telemetry signals.")
        current_genotype = self._load_genotype()
        # Heuristic: if error rate is high, decrease learning rate
        current_genotype['learning_rate'] = max(0.0001, current_genotype.get('learning_rate', 0.001) * 0.9)
        self._save_genotype(current_genotype)

    def _load_genotype(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _save_genotype(self, genotype: Dict[str, Any]):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(genotype, f)

    def _apply_mutation_to_config(self, mutation: Dict[str, Any]):
        genotype = self._load_genotype()
        changes = mutation.get("changes", {})
        genotype.update(changes)
        self._save_genotype(genotype)
        self.logger.info(f"Genotype updated with changes: {changes}")

    def stop_signals_loop(self):
        self.is_running = False
