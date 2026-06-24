import asyncio
import logging
import re
from typing import Any, Dict, List

import httpx

logger = logging.getLogger(__name__)

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"
ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"


def _clean_text(text: str, max_len: int = 120) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:max_len]


async def _search_remotive(client: httpx.AsyncClient, query: str, limit: int) -> List[Dict[str, Any]]:
    try:
        resp = await client.get(REMOTIVE_URL, params={"search": query, "limit": limit}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for job in data.get("jobs", [])[:limit]:
            results.append({
                "source": "Remotive",
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("candidate_required_location"),
                "url": job.get("url"),
                "salary": job.get("salary") or None,
                "tags": job.get("tags", []),
                "published": job.get("publication_date"),
                "description": _clean_text(re.sub(r"<[^>]+>", " ", job.get("description") or ""), 400),
            })
        return results
    except Exception as e:
        logger.warning(f"Remotive job search failed: {e}")
        return []


async def _search_arbeitnow(client: httpx.AsyncClient, query: str, limit: int) -> List[Dict[str, Any]]:
    try:
        resp = await client.get(ARBEITNOW_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        keywords = [k.lower() for k in query.split() if len(k) > 2]
        results = []
        for job in data.get("data", []):
            haystack = " ".join([
                job.get("title", ""), job.get("company_name", ""), " ".join(job.get("tags", []))
            ]).lower()
            if not keywords or any(k in haystack for k in keywords):
                results.append({
                    "source": "Arbeitnow",
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "url": job.get("url"),
                    "salary": None,
                    "tags": job.get("tags", []),
                    "published": job.get("created_at"),
                    "description": _clean_text(job.get("description") or "", 400),
                })
            if len(results) >= limit:
                break
        return results
    except Exception as e:
        logger.warning(f"Arbeitnow job search failed: {e}")
        return []


async def search_jobs(query: str, limit: int = 10) -> Dict[str, Any]:
    """Performs a real, live multi-source web search across public job board APIs."""
    cleaned_query = _clean_text(query) or "remote"
    async with httpx.AsyncClient() as client:
        remotive_results, arbeitnow_results = await asyncio.gather(
            _search_remotive(client, cleaned_query, limit),
            _search_arbeitnow(client, cleaned_query, limit),
        )

    combined = remotive_results + arbeitnow_results
    seen_urls = set()
    deduped: List[Dict[str, Any]] = []
    for job in combined:
        url = job.get("url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        deduped.append(job)

    return {
        "query": cleaned_query,
        "sources_used": sorted({j["source"] for j in combined}),
        "count": len(deduped),
        "results": deduped[: limit * 2],
    }
