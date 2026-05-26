"""
Canonical memory_v01 module.
"""
class MemoryV01:
    def __init__(self):
        self.data = {}
    def query(self, *args, **kwargs):
        return []
    def add_exchange(self, *args, **kwargs):
        pass

memory_v01 = MemoryV01()
meeting_log = type('Mock', (), {
    'get_recent_debate': lambda: "No recent debates recorded.",
    'post_argument': lambda *a: None,
    'export_minutes': lambda: "# Minutes",
    'log': []
})()
