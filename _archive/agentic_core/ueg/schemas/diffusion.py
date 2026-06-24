DIFFUSION_EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {
            "enum": [
                "diffusion_merge",
                "ui_complexity_diffusion",
                "sde_step",
                "diffusion_rollback"
            ]
        },
        "params_reduced_pct": {"type": "number", "minimum": 0.0, "maximum": 100.0},
        "legal_coverage": {"type": "number", "const": 1.0},
        "rollback_token": {"type": "string", "pattern": "^[a-f0-9]{128}$"},
        "lipschitz_constant": {"type": "number", "minimum": 0.0},
        "stability_index": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "entropy_delta": {"type": "number"}
    },
    "required": ["event_type", "legal_coverage", "rollback_token"]
}
