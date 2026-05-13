class SovereignMeter:
    def __init__(self, db): self.db = db
    def check_quota(self, uid, tier, action): return True
