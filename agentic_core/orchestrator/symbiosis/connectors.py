import logging
import httpx
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class AlQuranCloudConnector:
    """
    ARTICLE 410: Symbiosis Connector for AlQuran Cloud API.
    Provides production-ready access to Quranic text and audio.
    """
    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self.base_url = "https://api.alquran.cloud/v1"
        self.client = client or httpx.AsyncClient(timeout=10.0)

    async def get_ayah(self, reference: str, edition: str = "en.sahih") -> Dict[str, Any]:
        """Fetches a specific ayah with translation."""
        url = f"{self.base_url}/ayah/{reference}/{edition}"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Symbiosis: AlQuranCloud ayah fetch failed: {e}")
            return {"status": "error", "message": str(e)}

    async def get_audio_url(self, reference: str, edition: str = "ar.alafasy") -> str:
        """Returns the audio URL for a specific ayah."""
        # This edition usually returns audio URLs in the response
        res = await self.get_ayah(reference, edition)
        if res.get("status") == "OK":
            return res["data"].get("audio", "")
        return ""

    async def search(self, keyword: str, surah: str = "all") -> Dict[str, Any]:
        """Performs a search for a keyword in the Quran."""
        url = f"{self.base_url}/search/{keyword}/{surah}/en.sahih"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Symbiosis: AlQuranCloud search failed: {e}")
            return {"status": "error", "message": str(e)}

    async def close(self):
        await self.client.aclose()
