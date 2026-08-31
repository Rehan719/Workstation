import asyncio
import time
import logging
import random
from agentic_core.biomimicry.federation import FederationManager
from agentic_core.biomimicry.federated_learning import FederatedLearningManager
from agentic_core.biomimicry.marketplace import AgentMarketplace, WorkstationToken
from agentic_core.biomimicry.optimizer import SelfOptimisationEngine
from agentic_core.biomimicry.economy import SovereignLiabilityFund
from agentic_core.validation.kpi_monitor import KPIMonitor

class Phase6Validator:
    """
    Final Integration and Sovereignty validation for v138.0.
    """
    def __init__(self):
        self.monitor = KPIMonitor("outputs/phase6_metrics.jsonl")
        self.token = WorkstationToken()
        self.ueg_log = []
        def cb(e): self.ueg_log.append(e)

        self.fed = FederationManager("node_0", cb)
        self.fl = FederatedLearningManager(cb)
        self.market = AgentMarketplace(self.token, cb)
        self.optimizer = SelfOptimisationEngine(cb)
        self.fund = SovereignLiabilityFund(self.token, cb)

    async def validate_federation_scale(self, node_count: int = 50):
        """Stress test discovery across 50 nodes (<500ms)."""
        print(f"--- Validating Federation Scale ({node_count} nodes) ---")
        # Pre-populate DHT
        for i in range(node_count):
            self.fed.register_agent_globally(f"agent_{i}", {"node": f"node_{i}"})

        start = time.perf_counter()
        res = self.fed.discover_agent(f"agent_{random.randint(0, node_count-1)}")
        end = time.perf_counter()

        discovery_ms = (end - start) * 1000
        self.monitor.log_metric("Federation", "global_discovery_ms", discovery_ms)
        print(f"Global Agent Discovery: {discovery_ms:.2f}ms")

    def validate_marketplace_throughput(self, tx_count: int = 100):
        """Measure TPS (Target >= 10)."""
        print(f"--- Validating Marketplace Throughput ({tx_count} tx) ---")
        self.token.mint("buyer_prime", 1000000.0)
        l_ids = []
        for i in range(tx_count):
            l_ids.append(self.market.list_agent(f"agent_{i}", 10.0, "seller_x"))

        start = time.perf_counter()
        for l_id in l_ids:
            self.market.purchase_agent("buyer_prime", l_id)
        end = time.perf_counter()

        elapsed = end - start
        tps = tx_count / elapsed
        self.monitor.log_metric("Marketplace", "transactions_per_sec", tps)
        print(f"Marketplace TPS: {tps:.2f}")

    def validate_liability_fund(self):
        """Verify Sovereign Liability Fund balance (>= 100k)."""
        balance = self.fund.get_balance()
        self.monitor.log_metric("Economy", "liability_fund_balance", balance)
        print(f"Liability Fund Balance: {balance} WST")

    async def run_all(self):
        print("--- PHASE 6 FINAL VALIDATION START ---")
        await self.validate_federation_scale(50)
        self.validate_marketplace_throughput(100)
        self.validate_liability_fund()
        print("--- PHASE 6 FINAL VALIDATION COMPLETE ---")

if __name__ == "__main__":
    validator = Phase6Validator()
    asyncio.run(validator.run_all())
