from typing import Any, Dict, List, Optional

class CapabilityHierarchyManager:
    """
    Article R (Revised): The Hierarchical Quantum-AI Capability Prioritization Mandate.
    Enforces a binding three-tiered hierarchy, with Tier 1 as a mandatory foundation.
    """
    def __init__(self):
        self.tiers = {
            'tier1': {'name': 'Hybrid Optimization', 'stable': False, 'metrics': {}},
            'tier2': {'name': 'Quantum Federated Learning', 'stable': False, 'metrics': {}},
            'tier3': {'name': 'Domain Applications', 'stable': False, 'metrics': {}}
        }
        self.dependencies = {
            'tier2': ['tier1'],
            'tier3': ['tier1', 'tier2']
        }

    async def check_tier_stability(self, tier: str) -> bool:
        """Check if a tier has met stability criteria."""
        if tier not in self.tiers:
            return False

        # Mock metric collection
        metrics = self.tiers[tier]['metrics']

        if tier == 'tier1':
            # convergence_rate > 0.9, error_rate < 0.05
            stable = (metrics.get('convergence_rate', 0.95) > 0.9 and
                     metrics.get('error_rate', 0.01) < 0.05)
        elif tier == 'tier2':
            # federated_accuracy > 0.85, privacy_preservation > 0.95
            stable = (metrics.get('federated_accuracy', 0.88) > 0.85 and
                     metrics.get('privacy_preservation', 0.98) > 0.95)
        else:
            # application_success_rate > 0.8
            stable = (metrics.get('application_success_rate', 0.85) > 0.8)

        self.tiers[tier]['stable'] = stable
        return stable

    async def ensure_tier_prerequisites(self, target_tier: str) -> bool:
        """
        Ensures all prerequisite tiers are stable before allowing execution (Mandatory Tier 1).
        """
        if target_tier not in self.dependencies:
            # Tier 1 has no dependencies
            if target_tier == 'tier1':
                return True
            return True

        for prereq in self.dependencies[target_tier]:
            is_stable = await self.check_tier_stability(prereq)
            if not is_stable:
                raise PermissionError(f"Prerequisite tier {prereq} not stable. Cannot execute {target_tier} tasks (Article R).")

        return True

    def update_tier_metrics(self, tier: str, metrics: Dict[str, float]):
        if tier in self.tiers:
            self.tiers[tier]['metrics'].update(metrics)
