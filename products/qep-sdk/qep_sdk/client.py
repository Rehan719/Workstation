import httpx
import logging
from typing import Dict, Any, List, Optional

class QEPSDKClient:
    """
    Sovereign Digital Life: QEP-as-a-Service Client v130.1.0.
    Provides tiered access to Quranic scholarship, morphology, and AI quizzes.
    """
    def __init__(self, api_key: str, base_url: str = "https://api.vsb.ai/qep/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.Client(headers={"Authorization": f"Bearer {api_key}"})

    def get_ayah(self, reference: str) -> Dict[str, Any]:
        resp = self.client.get(f"{self.base_url}/ayah/{reference}")
        resp.raise_for_status()
        return resp.json()

    def get_morphology(self, reference: str) -> List[Dict[str, Any]]:
        resp = self.client.get(f"{self.base_url}/morphology/{reference}")
        resp.raise_for_status()
        return resp.json()["analysis"]

    def generate_quiz(self, reference: str, count: int = 5) -> Dict[str, Any]:
        resp = self.client.post(f"{self.base_url}/quiz/generate", json={"reference": reference, "count": count})
        resp.raise_for_status()
        return resp.json()

    def list_annotations(self, reference: str) -> List[Dict[str, Any]]:
        resp = self.client.get(f"{self.base_url}/annotations/{reference}")
        resp.raise_for_status()
        return resp.json()["annotations"]
