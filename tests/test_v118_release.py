import unittest
import os
from pathlib import Path

class TestV118Release(unittest.TestCase):
    def test_repository_structure(self):
        self.assertTrue(os.path.exists("backend/src/app.js"))
        self.assertTrue(os.path.exists("webapp/src/pages/index.js"))
        self.assertTrue(os.path.exists("mobile/App.js"))
        self.assertTrue(os.path.exists("website/index.html"))

    def test_v118_constitution(self):
        path = "agentic_core/constitution/CONSTITUTION_v118.0.0.md"
        if not os.path.exists(path):
            # Generate it if not exists for the test
            from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine
            import asyncio
            engine = GrandSynthesisEngine(["."])
            asyncio.run(engine.run_synthesis(target_version="118.0.0"))

        self.assertTrue(os.path.exists(path))
        with open(path, "r") as f:
            content = f.read()
            self.assertIn("v118.0", content)
            self.assertIn("SECTION XXI: PRODUCT DELIVERY & USER EXCELLENCE", content)
            self.assertIn("ARTICLE 406: PRODUCT DELIVERY MANDATE", content)

    def test_infrastructure_configs(self):
        self.assertTrue(os.path.exists("infrastructure/render.yaml"))
        self.assertTrue(os.path.exists("infrastructure/github/workflows/deploy.yml"))
        self.assertTrue(os.path.exists("website/vercel.json"))

if __name__ == "__main__":
    unittest.main()
