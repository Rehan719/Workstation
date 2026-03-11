import unittest
import os
from pathlib import Path

class TestV112Release(unittest.TestCase):
    def test_repository_hygiene(self):
        # Verify log files are removed
        for f in os.listdir("."):
            if f.endswith(".log"):
                self.fail(f"Redundant log file found: {f}")
        self.assertFalse(os.path.exists("workstation.db"))
        self.assertFalse(os.path.exists("vercel.json"))

    def test_security_hardening(self):
        # Verify hardcoded secret is gone
        auth_file = "agentic_core/collaboration/workspace_manager.py"
        with open(auth_file, "r") as f:
            content = f.read()
            self.assertNotIn("fallback-secret-for-testing-only-v99", content)
            self.assertIn("secrets.token_hex(32)", content)

    def test_v112_constitution(self):
        path = "agentic_core/constitution/CONSTITUTION_canonical.md"
        self.assertTrue(os.path.exists(path))
        with open(path, "r") as f:
            content = f.read()
            self.assertIn("v112.0", content)
            self.assertIn("SECTION XV: EXPERT QUALITY ASSURANCE", content)
            self.assertIn("ARTICLE 381: CODE QUALITY MANDATE", content)

    def test_quality_report(self):
        self.assertTrue(os.path.exists("docs/code_review/quality_report.md"))

    def test_dashboard_updates(self):
        with open("src/dashboard/app.py", "r") as f:
            content = f.read()
            self.assertIn("Jules AI v112.0 Expert Dashboard", content)
            self.assertIn("Code Quality & Resilience", content)

if __name__ == "__main__":
    unittest.main()
