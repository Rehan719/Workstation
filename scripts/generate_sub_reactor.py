import os
import sys

TEMPLATE = """from typing import Dict, Any
from agentic_core.reactor.ecosystem.base import SpecializedReactor

class {class_name}(SpecializedReactor):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("{domain}", "{sub_domain}", config)

    async def incubate(self, input_data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        return {{"status": "SUCCESS", "message": "Incubated {sub_domain} solution"}}

    async def interact(self, state: Any, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {{"action": action, "result": "PROCESSED"}}

    async def visualize(self, data: Any, mode: str) -> Dict[str, Any]:
        return {{"view": "3D_DYNAMIC_MODEL"}}

    async def analyze(self, data: Any) -> Dict[str, Any]:
        return {{"market_fit": 0.95}}

    async def validate_truth(self, content: Any) -> Dict[str, Any]:
        return {{"is_truth": True, "confidence": 0.992}}

    async def generate_artifact(self, data: Any, format: str = "pdf") -> Dict[str, Any]:
        return {{"artifact_url": f"https://cdn.v100.io/{{self.sub_domain}}.{{format}}"}}
"""

def generate(domain, sub_domain):
    class_name = sub_domain.capitalize() + "Reactor"
    content = TEMPLATE.format(class_name=class_name, domain=domain, sub_domain=sub_domain)

    path = f"agentic_core/reactor/{domain}/{sub_domain}.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)
    print(f"Generated {path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_sub_reactor.py <domain> <sub_domain>")
    else:
        generate(sys.argv[1], sys.argv[2])
