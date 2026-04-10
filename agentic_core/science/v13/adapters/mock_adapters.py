import random
import time

class ScientificAdapterMock:
    """Mock adapter for external scientific and regulatory databases."""
    def __init__(self, source_name):
        self.source_name = source_name

    def fetch_latest(self, query):
        print(f"[{self.source_name}] Searching for: {query}...")
        time.sleep(0.5)
        # Mocked response based on prompt requirements
        return {
            "source": self.source_name,
            "results": [
                {
                    "title": f"New findings in {query}",
                    "date": "2026-04-01",
                    "relevance": random.uniform(0.8, 0.99),
                    "impact_factor": "High"
                }
            ]
        }

class PubMedAdapter(ScientificAdapterMock):
    def __init__(self):
        super().__init__("PubMed")

class FDAAdapter(ScientificAdapterMock):
    def __init__(self):
        super().__init__("FDA")

class EMAAdapter(ScientificAdapterMock):
    def __init__(self):
        super().__init__("EMA")
