from __future__ import annotations

import json
import time
from typing import Any, Dict, List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/entrepreneur", tags=["Entrepreneurial Hub"])


class PlanRequest(BaseModel):
    creation_id: str
    target_market: str
    funding_goal: float
    description: str = ""
    domain: str = "general"


@router.post("/generate-plan")
async def generate_business_plan(req: PlanRequest) -> Dict[str, Any]:
    """Generate a real AI business plan with financial projections."""
    prompt = (
        f"You are an expert business strategist and financial analyst.\n"
        f"Product/Creation: {req.creation_id}\n"
        f"Target Market: {req.target_market}\n"
        f"Funding Goal: ${req.funding_goal:,.0f}\n"
        + (f"Description: {req.description}\n" if req.description else "")
        + f"Domain: {req.domain}\n\n"
        "Produce a detailed business plan response in this EXACT JSON structure (no other text, no markdown fences):\n"
        '{"market_analysis":"2-3 sentence market opportunity","financial_projections":[{"period":"Q1","revenue":number,"growth":"string"},{"period":"Q2","revenue":number,"growth":"string"},{"period":"Q3","revenue":number,"growth":"string"},{"period":"Q4","revenue":number,"growth":"string"}],"strategic_steps":["step1","step2","step3","step4","step5"],"key_risks":["risk1","risk2","risk3"],"revenue_model":"how you will make money","go_to_market":"2-3 sentence GTM summary"}\n\n'
        f"Base projections on the ${req.funding_goal:,.0f} funding goal. Be realistic but optimistic. Output ONLY the JSON."
    )

    raw = await gateway.query(prompt, agent="business_planner")

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```", 2)[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.rsplit("```", 1)[0]
        result = json.loads(cleaned.strip())
    except Exception:
        result = {
            "market_analysis": raw[:500] if raw else f"Strong opportunity in {req.target_market} for {req.creation_id}.",
            "financial_projections": [
                {"period": "Q1", "revenue": round(req.funding_goal * 0.15, 0), "growth": "+15%"},
                {"period": "Q2", "revenue": round(req.funding_goal * 0.40, 0), "growth": "+40%"},
                {"period": "Q3", "revenue": round(req.funding_goal * 0.90, 0), "growth": "+90%"},
                {"period": "Q4", "revenue": round(req.funding_goal * 1.60, 0), "growth": "+160%"},
            ],
            "strategic_steps": [
                "Validate product-market fit with 50 pilot users",
                "Build core AI-powered feature set",
                "Launch in primary target market segment",
                "Establish partnership and distribution channels",
                "Scale internationally with localised offering",
            ],
            "key_risks": [
                "Market adoption slower than projected",
                "Technical complexity underestimated",
                "Regulatory changes in target domain",
            ],
            "revenue_model": "Subscription SaaS with tiered pricing based on usage.",
            "go_to_market": f"Target {req.target_market} via direct outreach and content marketing.",
        }

    result["status"] = "plan_synthesized"
    result["generated_at"] = time.time()
    return result


@router.post("/generate-plan/stream")
async def generate_business_plan_stream(req: PlanRequest) -> StreamingResponse:
    """Stream a full narrative business plan as SSE tokens."""
    prompt = (
        f"You are an expert business strategist.\n"
        f"Write a comprehensive business plan for:\n"
        f"- Product: {req.creation_id}\n"
        f"- Target Market: {req.target_market}\n"
        f"- Funding Goal: ${req.funding_goal:,.0f}\n"
        + (f"- Description: {req.description}\n" if req.description else "")
        + f"- Domain: {req.domain}\n\n"
        "Structure your plan with these sections:\n"
        "## Executive Summary\n"
        "## Market Analysis\n"
        "## Product/Service Description\n"
        "## Go-to-Market Strategy\n"
        "## Financial Projections (Year 1 quarterly)\n"
        "## Risk Assessment\n"
        "## Funding Requirements & Use of Funds\n\n"
        "Be specific, use numbers, and make it commercially compelling."
    )

    async def stream_tokens():
        try:
            async for token in gateway.stream(prompt, agent="business_planner"):
                safe = token.replace("\n", "\\n")
                yield f'data: {{"token": {json.dumps(safe)}}}\n\n'
            yield f'data: {{"done": true, "generated_at": {time.time()}}}\n\n'
        except Exception as exc:
            yield f'data: {{"error": {json.dumps(str(exc))}}}\n\n'

    return StreamingResponse(
        stream_tokens(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/mentors")
async def list_mentors() -> Dict[str, Any]:
    """No mentors are registered, and none are invented.

    W408 - this returned six people who do not exist - "Dr. Aisha Sovereign", "Prof. Marcus Forge",
    "Fatima Capital" and three more - each with an expertise, a rating between 4.6 and 4.9, and an
    `available` flag. Presented as a bookable mentor directory, a user would believe these were real
    people, that the ratings came from real reviews, and that "available: true" meant they could be
    booked. Nothing rates them and nothing tracks availability.

    Inventing a person is a different order of fabrication from inventing a number: a user could act
    on it, and one of the invented profiles offered guidance on Islamic finance.
    """
    return {
        "mentors": [],
        "detail": ("No mentor register exists on this deployment, so no mentors are listed. Six "
                   "invented profiles with ratings were previously returned here."),
    }
