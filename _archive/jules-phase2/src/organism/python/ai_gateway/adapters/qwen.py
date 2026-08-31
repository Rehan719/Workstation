import logging
import httpx
import time
from typing import Dict, Any, List, Union
from .base import SovereignLLMClient

logger = logging.getLogger(__name__)

class QwenAdapter(SovereignLLMClient):
    """
    Adapter for Qwen.ai (DashScope/Alibaba).
    Focus: UK Employment Law reasoning & strategic research.
    """
    def __init__(self, api_key: str, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__("qwen")
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": kwargs.get("model", "qwen-max"),
            "messages": messages,
            **kwargs
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()

                latency = (time.time() - start_time) * 1000
                return {
                    "provider": self.provider_name,
                    "content": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {}),
                    "latency_ms": latency
                }
            except Exception as e:
                logger.error(f"Qwen: API Error: {e}")
                raise

    async def get_embeddings(self, text: Union[str, List[str]]) -> List[List[float]]:
        # Qwen has dedicated embedding models (e.g., gte-qwen2)
        logger.info("Qwen: Generating embeddings...")
        return []
