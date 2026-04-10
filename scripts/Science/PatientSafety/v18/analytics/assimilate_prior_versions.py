import os
import json
from typing import Dict, List, Any

class Assimilator:
    """
    Assimilates outputs from v13.0 to v17.1 into a unified v18.0 context.
    """
    def __init__(self, base_path: str = "outputs/Science/PatientSafety/"):
        self.base_path = base_path
        self.versions = [
            "v13_quadra_veritas",
            "v15_penta_veritas",
            "v16_quinta_veritas",
            "v17_sexta_veritas",
            "v17.1_septima_veritas"
        ]

    def assimilate_all(self) -> Dict[str, Any]:
        consolidated_evidence = {
            "autoimmune": [],
            "germline": [],
            "regulatory": [],
            "prior_scores": []
        }

        for v in self.versions:
            v_dir = os.path.join(self.base_path, v)
            if not os.path.exists(v_dir): continue

            # Extract score
            status_file = self._find_status_file(v_dir)
            if status_file:
                with open(status_file, 'r') as f:
                    s_data = json.load(f)
                    consolidated_evidence["prior_scores"].append({
                        "version": v,
                        "score": s_data.get('overall_convergence_score') or s_data.get('overall_score')
                    })

        return consolidated_evidence

    def _find_status_file(self, directory: str) -> str:
        for f in os.listdir(directory):
            if f.endswith("_status.json"):
                return os.path.join(directory, f)
        return None

if __name__ == "__main__":
    assimilator = Assimilator()
    print(json.dumps(assimilator.assimilate_all(), indent=2))
