import unittest
import os
import shutil
import sys
from unittest.mock import MagicMock

# Aggressive mocking of problematic dependencies
for mod in ['shap', 'yaml', 'jwt', 'matplotlib', 'matplotlib.pyplot', 'three']:
    sys.modules[mod] = MagicMock()

# Mock internal modules that have missing dependencies
sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.omnimedia.injector import OmnimediaInjector
from agentic_core.omnimedia.factory import MultimediaAsset

class TestOmnimediaInjector(unittest.TestCase):
    def setUp(self):
        self.output_dir = "outputs/test_injector"
        self.injector = OmnimediaInjector(self.output_dir)
        self.assets = [
            MultimediaAsset("Test Image", "png", None),
            MultimediaAsset("Test Video", "video", None),
            MultimediaAsset("Test Audio", "audio", None)
        ]

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_pdf_injection(self):
        path = self.injector.inject_into_pdf("test.pdf", self.assets)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".pdf"))

    def test_docx_injection(self):
        path = self.injector.inject_into_docx("test.docx", self.assets)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".docx"))

    def test_pptx_injection(self):
        path = self.injector.inject_into_pptx("test.pptx", self.assets)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".pptx"))

    def test_xlsx_injection(self):
        path = self.injector.inject_into_xlsx("test.xlsx", self.assets)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".xlsx"))

    def test_html_injection(self):
        path = self.injector.inject_into_html("test.html", self.assets)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith(".html"))

if __name__ == "__main__":
    unittest.main()
