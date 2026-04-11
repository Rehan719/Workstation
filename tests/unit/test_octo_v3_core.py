import unittest
import os
from products.OctoVeritasEngine.pipelines.registry import PipelineRegistry
from products.OctoVeritasEngine.modes.mode_router import ModeRouter

class TestOctoV3Core(unittest.TestCase):
    def test_pipeline_registry(self):
        registry = PipelineRegistry()
        self.assertEqual(registry.get_pipeline_priority("Introspection"), 3)
        self.assertTrue(registry.is_pipeline_allowed_in_mode("Scraping", "mushahida"))
        self.assertFalse(registry.is_pipeline_allowed_in_mode("Scraping", "muaina"))

    def test_mode_router(self):
        router = ModeRouter()
        router.set_mode("muaina")
        self.assertEqual(router.get_mode(), "muaina")
        self.assertEqual(router.get_default_formats(), ["PDF", "DOCX"])

        with self.assertRaises(ValueError):
            router.set_mode("invalid_mode")

if __name__ == "__main__":
    unittest.main()
