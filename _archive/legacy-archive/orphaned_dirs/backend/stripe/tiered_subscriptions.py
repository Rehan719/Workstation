import os
TIER_CONFIG = {
    "free": {"price_id": None, "compute": "shared_edge_pool", "cognitive_engines": "all_9", "transcendent_subsystems": "all_15"},
    "standard": {"price_id": "price_std", "compute": "priority_gpu_burst", "cognitive_engines": "all_9", "transcendent_subsystems": "all_15"},
    "advanced": {"price_id": "price_adv", "compute": "dedicated_dgx_node", "cognitive_engines": "all_9+MoE", "transcendent_subsystems": "all_15"}
}
