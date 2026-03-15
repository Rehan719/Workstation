import unittest
import os
import shutil
import sys

# Add current directory to path
sys.path.append(os.getcwd())

# Mock necessary modules to avoid heavy dependencies
from unittest.mock import MagicMock
sys.modules['shap'] = MagicMock()
sys.modules['matplotlib'] = MagicMock()
sys.modules['matplotlib.pyplot'] = MagicMock()
sys.modules['seaborn'] = MagicMock()
sys.modules['plotly'] = MagicMock()
sys.modules['plotly.graph_objects'] = MagicMock()
sys.modules['networkx'] = MagicMock()
sys.modules['scipy'] = MagicMock()
sys.modules['scipy.stats'] = MagicMock()
sys.modules['sklearn'] = MagicMock()
sys.modules['sklearn.ensemble'] = MagicMock()
sys.modules['z3'] = MagicMock()
sys.modules['sympy'] = MagicMock()
sys.modules['qiskit'] = MagicMock()
sys.modules['pennylane'] = MagicMock()
sys.modules['camel_tools'] = MagicMock()
sys.modules['quran'] = MagicMock()

from agentic_core.governance.credentials.vault import CredentialVault

class TestCredentialVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_vault_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.vault_path = os.path.join(self.test_dir, "vault.json")
        self.vault = CredentialVault(vault_path=self.vault_path)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_store_and_get_secret(self):
        self.vault.store_secret("TEST_KEY", "super_secret_value", "admin", "production")
        value = self.vault.get_secret("TEST_KEY", "tester")
        self.assertEqual(value, "super_secret_value")

    def test_metadata_tracking(self):
        self.vault.store_secret("META_KEY", "val", "owner_jules", "staging")
        metadata = self.vault.list_metadata()
        self.assertIn("META_KEY", metadata)
        self.assertEqual(metadata["META_KEY"]["owner"], "owner_jules")
        self.assertEqual(metadata["META_KEY"]["environment"], "staging")

if __name__ == "__main__":
    unittest.main()
