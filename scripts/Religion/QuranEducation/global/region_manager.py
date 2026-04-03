import random
import json
import os
from datetime import datetime

class RegionManager:
    """
    Simulation of Global Scale Regions (Middle East, Europe, North America, Asia Pacific, Africa).
    Handles regional compliance (GDPR), latency simulation, and localized content routing.
    """
    def __init__(self, base_path=None):
        self.base_path = base_path or "archive/qep-v8.7-global-distribution/"
        self.regions = {
            "middle_east": {
                "name": "Middle East",
                "compliance": ["local_religious_norms", "sharia_compliance"],
                "latency_range": [20, 50],
                "language_priority": ["Arabic", "English", "Urdu", "Turkish"],
                "region_id": "ME-001"
            },
            "europe": {
                "name": "Europe",
                "compliance": ["GDPR", "EU_Privacy_Shield", "Digital_Services_Act"],
                "latency_range": [10, 30],
                "language_priority": ["English", "French", "Spanish", "German", "Turkish"],
                "region_id": "EU-001"
            },
            "north_america": {
                "name": "North America",
                "compliance": ["CCPA", "PIPEDA", "Safe_Harbor"],
                "latency_range": [15, 40],
                "language_priority": ["English", "Spanish", "French"],
                "region_id": "NA-001"
            },
            "asia_pacific": {
                "name": "Asia Pacific",
                "compliance": ["APEC_Privacy", "ASEAN_Standards"],
                "latency_range": [30, 80],
                "language_priority": ["Indonesian", "Malay", "English", "Urdu"],
                "region_id": "AP-001"
            },
            "africa": {
                "name": "Africa",
                "compliance": ["AU_Privacy_Framework", "Regional_Standards"],
                "latency_range": [50, 150],
                "language_priority": ["English", "French", "Arabic", "Swahili"],
                "region_id": "AF-001"
            }
        }

    def simulate_request(self, region_name, content_id="lesson_01"):
        """
        Simulates a content request from a specific region and performs compliance checks.
        """
        if region_name not in self.regions:
            raise ValueError(f"Region {region_name} not available for simulation.")

        region = self.regions[region_name]
        latency = random.randint(*region["latency_range"])

        print(f"GLOBAL SCALE: Serving {content_id} to region {region_name} (latency: {latency}ms)...")

        compliance_check = {
            "status": "COMPLIANT",
            "enforced_rules": region["compliance"],
            "data_masking_applied": True if "GDPR" in region["compliance"] else False,
            "region_id": region["region_id"]
        }

        # Log regional request to archive
        request_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "region": region_name,
            "content_id": content_id,
            "latency_ms": latency,
            "compliance_result": compliance_check
        }

        target_path = os.path.join(self.base_path, region_name, f"request_log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            json.dump(request_log, f, indent=2)

        return request_log

    def get_regional_availability(self):
        """
        Returns the availability and health of all regions.
        """
        return {
            region_name: {
                "status": "STABLE",
                "primary_languages": data["language_priority"],
                "compliance_mode": data["compliance"][0]
            }
            for region_name, data in self.regions.items()
        }

if __name__ == "__main__":
    rm = RegionManager()
    for region in rm.regions.keys():
        print(json.dumps(rm.simulate_request(region), indent=2))
    print(json.dumps(rm.get_regional_availability(), indent=2))
