import logging
from contextlib import asynccontextmanager
class MetricsCollector:
    def __init__(self):
        self.metrics = {"cycles_completed": 0, "cycles_failed": 0}
    async def start_server(self, port=9090):
        pass
    async def stop_server(self):
        pass
    def increment(self, name):
        self.metrics[name] += 1
    @asynccontextmanager
    async def timer(self, name):
        yield
    async def get_gpu_utilization(self):
        return 0.15
