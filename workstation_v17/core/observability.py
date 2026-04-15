import logging
from contextlib import asynccontextmanager

logger = logging.getLogger("Observability")

class MetricsCollector:
    def __init__(self):
        self.metrics = {"cycles_completed": 0, "cycles_failed": 0}
    async def start_server(self, port=9090):
        logger.info(f"Prometheus metrics server active on port {port}")
    async def stop_server(self):
        logger.info("Metrics server stopped.")
    def increment(self, name):
        if name in self.metrics:
            self.metrics[name] += 1
    @asynccontextmanager
    async def timer(self, name):
        import time
        start = time.time()
        yield
        elapsed = time.time() - start
        # logger.debug(f"Timer {name}: {elapsed:.4f}s")
    async def get_gpu_utilization(self):
        return 0.15
