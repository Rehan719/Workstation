import unittest
import os
from pptx import Presentation

class TestPresentationV14(unittest.TestCase):
    def test_pptx_exists(self):
        pptx_path = 'outputs/v14/science/presentation/PatientSafety_Presentation_v14.pptx'
        self.assertTrue(os.path.exists(pptx_path))

    def test_pptx_slides(self):
        pptx_path = 'outputs/v14/science/presentation/PatientSafety_Presentation_v14.pptx'
        prs = Presentation(pptx_path)
        # We scaffolded 5 slides in the current script version
        self.assertGreaterEqual(len(prs.slides), 5)

    def test_manifest_exists(self):
        manifest_path = 'outputs/v14/science/presentation/multimedia_manifest.json'
        self.assertTrue(os.path.exists(manifest_path))

if __name__ == '__main__':
    unittest.main()
