import os
import logging
import httpx
import json
import time
from typing import Dict, Any, List, Optional, Union
from .base import SovereignLLMClient

logger = logging.getLogger(__name__)

class DeepSeekAdapter(SovereignLLMClient):
    """
    Adapter for DeepSeek API (OpenAI-compatible).
    Focus: High-throughput document ingestion & embeddings.
    """
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        super().__init__("deepseek")
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
            "model": kwargs.get("model", "deepseek-chat"),
            "messages": messages,
            "stream": False,
            **kwargs
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()

                latency = (time.time() - start_time) * 1000
                logger.info(f"DeepSeek: Completion successful. Latency: {latency:.2f}ms")

                return {
                    "provider": self.provider_name,
                    "content": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {}),
                    "latency_ms": latency
                }
            except Exception as e:
                logger.error(f"DeepSeek: API Error: {e}")
                raise

    async def get_embeddings(self, text: Union[str, List[str]]) -> List[List[float]]:
        # DeepSeek currently doesn't expose a dedicated embedding endpoint in the same way OpenAI does,
        # but if it did or via a proxy, it would go here.
        # Fallback to a placeholder or local model for now if needed.
        logger.warning("DeepSeek: Embedding endpoint not natively supported in all regions yet.")
        return []
