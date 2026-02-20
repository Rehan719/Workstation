import httpx
from typing import Any, Dict, List, Optional

class CrossrefAPI:
    """
    Wrapper for the CrossRef API to fetch metadata by DOI.
    """
    def __init__(self, email: Optional[str] = None):
        self.base_url = "https://api.crossref.org/works"
        self.email = email

    async def get_metadata(self, doi: str) -> Optional[Dict[str, Any]]:
        params = {}
        if self.email:
            params["mailto"] = self.email

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{doi}", params=params)
            if response.status_code == 200:
                return response.json().get("message")
            return None
