import logging
import json
import os
from typing import Dict, Any, List
from .resolvers import VersionResolver, ConflictResolver
from agentic_core.twinning.reactor_twin import ReactorTwin

logger = logging.getLogger(__name__)

class ConvergenceEngine:
    """v101.0: Multi-objective convergence for the Meta-Cognitive Organism."""
    def __init__(self):
        # Local imports to avoid circularities
        from .resolvers import VersionResolver, ConflictResolver
        self.version_resolver = VersionResolver()
        self.conflict_resolver = ConflictResolver()

    async def run_convergence(self, collation_data: Dict[str, Any]):
        logger.info("QMS: Convergence Division performing design space exploration...")
        converged_configs = {}

        for category, data in collation_data.items():
            latest_v = self.version_resolver.resolve(data.get("versions", []))
            best_var = self.conflict_resolver.resolve_variation(data.get("variations", []))

            config = {
                "category": category,
                "version": latest_v,
                "variation": best_var,
                "strategy": "NSGA-II_Meta",
                "targets": {
                    "fidelity": 0.998, # v101 target
                    "waste": 0.025, # v101 target
                    "team_health": 0.95 # v101 target
                }
            }

            twin = ReactorTwin(f"v101_converge_{category}")
            validation = twin.run_simulation(config)
            config["validation"] = validation

            converged_configs[category] = config

            output_path = f"meta/convergence/{category}_config.json"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=4)

        return converged_configs
