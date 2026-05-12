import os
from typing import Dict, Any

TIER_CONFIG = {
    "free": {
        "price_id": None,
        "compute": "shared_edge_pool",
        "storage_gb": 1,
        "rate_limits": {"executions_per_day": 50, "api_calls_per_min": 5},
        "support_sla": "automated_best_effort_24h",
        "cognitive_engines": "all_9",
        "transcendent_subsystems": "all_15"
    },
    "standard": {
        "price_id": os.environ.get("STRIPE_STANDARD_PRICE_ID", "price_standard_mock"), # $29/mo
        "compute": "priority_gpu_burst",
        "storage_gb": 50,
        "rate_limits": {"executions_per_day": 2000, "api_calls_per_min": 50},
        "support_sla": "automated_priority_4h",
        "cognitive_engines": "all_9",
        "transcendent_subsystems": "all_15"
    },
    "advanced": {
        "price_id": os.environ.get("STRIPE_ADVANCED_PRICE_ID", "price_advanced_mock"), # $99/mo
        "compute": "dedicated_dgx_node",
        "storage_gb": 500,
        "rate_limits": {"executions_per_day": 10000, "api_calls_per_min": 500},
        "support_sla": "automated_dedicated_1h",
        "cognitive_engines": "all_9+MoE_swarm+VRPR_dedicated",
        "transcendent_subsystems": "all_15"
    }
}
