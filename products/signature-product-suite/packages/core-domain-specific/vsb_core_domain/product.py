import yaml
import asyncio
import os
import shutil
from vsb_constitutional import DecaVeritasOrchestrator

class CoreDomainSpecific:
    """Template for domain‑specific intelligence creation wizard."""

    @staticmethod
    def create_new_domain(domain_id: str, name: str, description: str):
        template_path = "config/constitutional/domains/core_domain_specific_template.yaml"
        new_config_path = f"config/constitutional/domains/{domain_id}.yaml"

        with open(template_path, 'r') as f:
            config = yaml.safe_load(f)

        config['domain']['id'] = domain_id
        config['domain']['name'] = name
        config['domain']['description'] = description

        with open(new_config_path, 'w') as f:
            yaml.dump(config, f)

        print(f"New domain genome created at {new_config_path}")
        return new_config_path

    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})

    async def run(self, input_data: dict):
        return await self.orchestrator.orchestrate_core_process(input_data)
