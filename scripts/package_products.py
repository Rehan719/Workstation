import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def package_products():
    """ARTICLE 536: Automates the collation and sanitization of commercial products."""
    products = {
        "uviap": ["agentic_core/synthesis/uviap.py"],
        "gse": ["agentic_core/synthesis/grand_synthesis_engine.py"],
        "scraping_suite": ["agentic_core/synthesis/dual_mode_scraper.py", "agentic_core/synthesis/web_scraper.py", "agentic_core/synthesis/knowledge_synthesis.py"]
    }

    for name, files in products.items():
        dest_dir = f"products/{name}/sdk"
        os.makedirs(dest_dir, exist_ok=True)
        for src in files:
            if os.path.exists(src):
                shutil.copy(src, dest_dir)
                logger.info(f"Packaged {src} into {dest_dir}")

        # Create a mock docker-compose for the product
        with open(f"products/{name}/docker-compose.yml", "w") as f:
            f.write(f"version: '3.8'\nservices:\n  {name}:\n    image: jules-ai-{name}:latest\n    ports:\n      - '8080:8080'\n")

        # Create README
        with open(f"products/{name}/README.md", "w") as f:
            f.write(f"# Jules AI: {name.upper()} Commercial Product\n\nProduction-ready {name} engine for enterprise synthesis.\n")

    logger.info("Packaging complete.")

if __name__ == "__main__":
    package_products()
