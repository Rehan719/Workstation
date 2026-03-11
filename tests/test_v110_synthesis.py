import asyncio
import unittest
from unittest import IsolatedAsyncioTestCase
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine
import sys
import os

class TestUltimateRerun(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = GrandSynthesisEngine(["."])
        # Mock sys.argv to include --ultimate-rerun
        self.original_argv = sys.argv
        sys.argv = ["test_script.py", "--ultimate-rerun"]

    async def asyncTearDown(self):
        sys.argv = self.original_argv

    async def test_ultimate_synthesis(self):
        print("Testing v110.0 Ultimate Grand Synthesis...")
        config = await self.engine.run_synthesis(target_version="110.0.0")
        self.assertEqual(config.get("version"), "110.0.0")

        # Verify guides exist
        guides = [
            "docs/guides/repo_owner_v3.md",
            "docs/guides/developer_v3.md",
            "docs/guides/user_v3.md",
            "docs/guides/platform_features_v3.md",
            "docs/guides/background_v3.md",
            "docs/guides/transcendent_whitepaper.md",
            "docs/guides/ultimate_rerun_guide.md"
        ]
        for guide in guides:
            self.assertTrue(os.path.exists(guide), f"Guide {guide} should exist")
            with open(guide, "r") as f:
                content = f.read()
                self.assertIn("Transcendent Generation Provenance Certificate", content)

        # Verify constitution
        self.assertTrue(os.path.exists("CONSTITUTION_v110.0.0.md"))
        with open("CONSTITUTION_v110.0.0.md", "r") as f:
            content = f.read()
            self.assertIn("v110.0", content)
            self.assertIn("ARTICLE 371: PREDICTIVE META-ORCHESTRATOR 3.0", content)

if __name__ == "__main__":
    unittest.main()
