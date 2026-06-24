class PriorityHierarchy:
    """BT-I: Priority Hierarchy (Immune > Nervous > Digestive > Aging)."""
    def __init__(self):
        self.levels = ["immune", "nervous", "digestive", "aging"]

    def compare(self, source: str, target: str) -> int:
        s_idx = self.levels.index(source.lower())
        t_idx = self.levels.index(target.lower())
        if s_idx < t_idx: return -1 # Source has higher priority
        if s_idx > t_idx: return 1
        return 0
