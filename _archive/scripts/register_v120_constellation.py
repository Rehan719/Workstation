import asyncio
import logging
from agentic_core.reactor.ecosystem.registry import ReactorRegistry
import importlib
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOMAINS = ["science", "religion", "law", "career", "education"]

async def register_all_v120():
    registry = ReactorRegistry()

    for domain in DOMAINS:
        domain_dir = f"agentic_core/reactor/{domain}"
        if not os.path.exists(domain_dir):
            continue

        for filename in os.listdir(domain_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                sub_domain = filename[:-3]
                module_path = f"agentic_core.reactor.{domain}.{sub_domain}"

                try:
                    module = importlib.import_module(module_path)
                    class_name = "".join([word.capitalize() for word in sub_domain.split("_")]) + "Reactor"

                    if hasattr(module, class_name):
                        reactor_class = getattr(module, class_name)
                        registry.register(reactor_class())
                    else:
                        logger.warning(f"Class {class_name} not found in {module_path}")
                except Exception as e:
                    logger.error(f"Error registering {module_path}: {e}")

    print(f"v120.0: Registered {len(registry.reactors)} hyper-specialized sub-reactors.")

if __name__ == "__main__":
    asyncio.run(register_all_v120())
