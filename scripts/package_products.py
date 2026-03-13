import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def package_products():
    """
    ARTICLE 536-540: Packaging UVIAP, GSE, and Scraping Suite as commercial products.
    """
    products = {
        "uviap": {
            "source": "agentic_core/synthesis/uviap.py",
            "dependencies": ["agentic_core/ueg/", "agentic_core/genetics/"]
        },
        "gse": {
            "source": "agentic_core/synthesis/grand_synthesis_engine.py",
            "dependencies": ["agentic_core/synthesis/uviap.py", "agentic_core/ueg/"]
        },
        "scraping_suite": {
            "source": "agentic_core/synthesis/dual_mode_scraper.py",
            "dependencies": ["agentic_core/synthesis/knowledge_synthesis.py", "agentic_core/governance/ledger.py"]
        }
    }

    base_dir = "products"
    os.makedirs(base_dir, exist_ok=True)

    for name, config in products.items():
        product_dir = os.path.join(base_dir, name)
        os.makedirs(product_dir, exist_ok=True)

        # Copy main source
        dest_src = os.path.join(product_dir, os.path.basename(config["source"]))
        shutil.copy(config["source"], dest_src)
        logger.info(f"Packaged {name} source: {config['source']} -> {dest_src}")

        # Create Docker Compose template
        with open(os.path.join(product_dir, "docker-compose.yml"), "w") as f:
            f.write(f"""version: '3.8'
services:
  {name}:
    build: .
    ports:
      - "8080:8080"
    environment:
      - APP_MODE=COMMERCIAL
      - PRODUCT_NAME={name.upper()}
""")

        # Create basic README
        with open(os.path.join(product_dir, "README.md"), "w") as f:
            f.write(f"# {name.upper()} Commercial SDK\n\nThis is a standalone enterprise-grade module from the Jules AI Workstation.\n\n## Deployment\n`docker-compose up -d`")

    logger.info("All products packaged successfully.")

if __name__ == "__main__":
    package_products()
