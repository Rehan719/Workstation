import numpy as np
from typing import Dict, Any, List, Optional
import math

class BiomimeticGeneticImmuneCascadeController:
    """
    Unified control system mimicking biological signal transduction, genetic regulation, and immune defense.
    J(π) = α·F[π] + β·W_ε(μ,ν) + γ·KL(π||R) + δ·S_export[π] + ζ·M[π] + η·C_bio[π] + θ·C_genetic[π] + ι·C_immune[π]

    All hard constraints (Legal, Quantum, Biomimetic, Genetic, Immune) act as multipliers.
    """
    def __init__(self, weights: Dict[str, float] = None, legal_precision_weight: float = 1.0):
        self.weights = weights or {
            "free_energy": 0.15,          # Surprise minimisation
            "optimal_transport": 0.15,    # Resource efficiency
            "schrodinger_bridge": 0.12,   # Path likelihood
            "entropy_export": 0.12,       # Thermodynamic efficiency
            "murray_law": 0.08,           # Branching network efficiency
            "quantum_security": 0.04,     # OAM-QKD emulation fidelity
            "hyperdimensional_transfer": 0.08,  # MJM v4.0 transfer
            "biomimetic_fidelity": 0.04,  # Biological analogue validation
            "genetic_integrity": 0.12,    # Reconfigulator compliance
            "immune_defense": 0.10        # Immune Defense effectiveness
        }
        self.legal_precision_weight = legal_precision_weight

    def evaluate(self, policy: Any, context: Any,
                legal_compliance: float = 1.0, quantum_security: float = 1.0,
                biomimetic_fidelity: float = 1.0, genetic_integrity: float = 1.0,
                immune_defense: float = 1.0) -> float:

        # --- HARD CONSTRAINTS ---
        # L12 or Legal domain must have 100% compliance
        is_legal = getattr(context, "domain", "") == "legal" or getattr(context, "layer", "") == "L12_Policy"
        if is_legal and legal_compliance < 1.0:
            return float('inf')

        if getattr(context, "requires_quantum_security", False) and quantum_security < 1.0:
            return float('inf')

        if biomimetic_fidelity < 0.9:
            return float('inf')

        if genetic_integrity < 1.0:
            return float('inf')

        if immune_defense < 0.95:
            return float('inf')

        # --- SOFT COMPONENTS (Weighted Sum) ---
        # Extract components from policy/context or use passed-in verified metrics
        component_scores = {
            "free_energy": getattr(policy, "free_energy", 0.1),
            "optimal_transport": getattr(policy, "ot_cost", 0.1),
            "schrodinger_bridge": getattr(policy, "sb_likelihood", 0.1),
            "entropy_export": getattr(policy, "entropy_export", 0.1),
            "murray_law": getattr(policy, "network_efficiency", 0.1),
            "quantum_security": quantum_security,
            "hyperdimensional_transfer": getattr(policy, "mjm_efficiency", 0.1),
            "biomimetic_fidelity": biomimetic_fidelity,
            "genetic_integrity": genetic_integrity,
            "immune_defense": immune_defense
        }

        base_score = sum(self.weights[k] * component_scores.get(k, 0.0) for k in self.weights)

        # Final evaluation: Base Score * Hard Constraint Multipliers
        return base_score
