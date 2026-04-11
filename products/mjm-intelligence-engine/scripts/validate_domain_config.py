import sys
import os
import yaml
from core.genome_manager import GenomeManager

def validate(domain_id):
    try:
        manager = GenomeManager(genomes_dir="config/domains")
        config = manager.get_domain_config(domain_id)
        if config:
            print(f"✅ Domain '{domain_id}' validated successfully.")
            return True
        else:
            print(f"❌ Domain '{domain_id}' not found or empty.")
            return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_domain_config.py <domain_id>")
        sys.exit(1)

    success = validate(sys.argv[1])
    sys.exit(0 if success else 1)
