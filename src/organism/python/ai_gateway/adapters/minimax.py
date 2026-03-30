import os
import logging
import httpx
import time
from typing import Dict, Any, List, Optional, Union
from .base import SovereignLLMClient

logger = logging.getLogger(__name__)

class MinimaxAdapter(SovereignLLMClient):
    """
    Adapter for Minimax.io.
    Focus: Codebase reasoning & autonomous assistance.
    """
    def __init__(self, api_key: str, group_id: str):
        super().__init__("minimax")
        self.api_key = api_key
        self.group_id = group_id
        self.base_url = f"https://api.minimax.chat/v1/text/chat_completion_v2?GroupId={self.group_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        start_time = time.time()

        # Minimax v2 API format
        payload = {
            "model": kwargs.get("model", "abab6.5-chat"),
            "messages": messages,
            **kwargs
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, headers=self.headers, json=payload)
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
                logger.error(f"Minimax: API Error: {e}")
                raise

    async def get_embeddings(self, text: Union[str, List[str]]) -> List[List[float]]:
        logger.info("Minimax: Generating embeddings...")
        return []
