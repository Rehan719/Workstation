from backend.stripe.tiered_subscriptions import TIER_CONFIG
class TierManager:
    def __init__(self, meter): self.meter, self.tiers = meter, TIER_CONFIG
    def get_tier_config(self, tier): return self.tiers.get(tier, self.tiers["free"])
    def get_resource_limits(self, tier):
        c = self.get_tier_config(tier)
        l = {"free": {"cpu": "1000m", "mem": "512Mi", "pri": 0, "con": 1}, "standard": {"cpu": "4000m", "mem": "16Gi", "pri": 10, "con": 5}, "advanced": {"cpu": "unlimited", "mem": "128Gi", "pri": 100, "con": 20}}
        return {**c, **l.get(tier, l["free"])}
