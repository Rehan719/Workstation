# Minimisation Event Schema (v1.0.0)
MINIMISATION_EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {
            "enum": [
                "schrodinger_bridge_solved",
                "ot_assignment",
                "diffusion_step",
                "gaas_minimisation_audit",
                "tribunal_task_assignment",
                "omega_macro_cycle",
                "meta_rl_update"
            ]
        },
        "entropy_production": {"type": "number", "minimum": 0},
        "entropy_reduction": {"type": "number"},
        "entropy_export_rate": {"type": "number", "minimum": 0.0},
        "wasserstein_distance": {"type": "number", "minimum": 0},
        "kl_divergence": {"type": "number", "minimum": 0},
        "legal_coverage": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "computational_cost": {"type": "number"},
        "convergence_info": {
            "type": "object",
            "properties": {
                "iterations": {"type": "integer"},
                "tolerance_achieved": {"type": "number"},
                "method_used": {"type": "string"},
                "converged": {"type": "boolean"}
            }
        }
    },
    "required": ["event_type", "entropy_production"]
}
