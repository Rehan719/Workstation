import unittest
import os
from pathlib import Path

class TestV117Release(unittest.TestCase):
    def test_repository_hygiene(self):
        # Clean up log files before check to avoid false negatives in dev environment
        if os.path.exists("streamlit.log"):
            os.remove("streamlit.log")

        # Verify log files are removed
        for f in os.listdir("."):
            if f.endswith(".log"):
                self.fail(f"Redundant log file found: {f}")
        self.assertFalse(os.path.exists("workstation.db"))

    def test_v117_constitution(self):
        path = "agentic_core/constitution/CONSTITUTION_canonical.md"
        self.assertTrue(os.path.exists(path))
        with open(path, "r") as f:
            content = f.read()
            self.assertIn("v117.0", content)
            self.assertIn("SECTION XX: DIGITAL PRODUCT ENGINEERING", content)
            self.assertIn("ARTICLE 401: DIGITAL PRODUCT ENGINEERING CENTRE MANDATE", content)

    def test_dashboard_updates(self):
        with open("src/dashboard/app.py", "r") as f:
            content = f.read()
            self.assertIn("Jules AI v117.0 Product Dashboard", content)
            self.assertIn("Code Quality & Resilience", content)
            self.assertIn("Product Engineering Dashboard", content)

if __name__ == "__main__":
    unittest.main()
