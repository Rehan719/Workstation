"""
agentic_core/ai/llm.py

Thin async wrapper over the ModelGateway.
Exposes a single coroutine:

    await generate(system, prompt) -> str

The gateway handles provider priority:
  Anthropic Claude → OpenAI → Ollama (local fallback).

If ANTHROPIC_API_KEY is absent and no fallback is reachable, the gateway
returns a clearly-labelled mock string so development still runs.
"""
from __future__ import annotations

from agentic_core.ai.gateway import gateway


async def generate(system: str, prompt: str) -> str:
    """
    Generate a completion using the best available AI provider.

    Args:
        system: System instruction for the model.
        prompt: User-facing prompt / task description.

    Returns:
        The model's text response.
    """
    combined = f"{system}\n\n{prompt}" if system else prompt
    return await gateway.query(combined, agent="llm")
