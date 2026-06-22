"""
Native Orchestrator — Workstation's OWN AI control plane.

Not a thin gateway: this OWNS routing, in-house-first selection, graceful degradation,
biomimetic mediation (fires nervous signals), and bespoke agent-cascade ("swarm")
composition — over the Model Resource Registry. External providers are optional
accelerants (flag-gated); a local owned model (Ollama) is used when present; and the
native structured engine is the always-available floor. Every result reports `served_by`.
"""
from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List

from agentic_core.ai.native.engine import native_engine
from agentic_core.ai.native.model_resource import registry


def _fire(signal_type: str, source: str, msg: str, intensity: float = 0.5) -> None:
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal(signal_type, source, msg[:80], intensity)
    except Exception:
        pass


class NativeOrchestrator:
    """In-house-first orchestration over owned + local + (optional) external model resources."""

    async def complete(self, prompt: str, agent: str = "assistant",
                       timeout: float = 30.0, prefer_external: bool = False) -> Dict[str, Any]:
        order = registry.select(prefer_external=prefer_external)
        tried: List[str] = []
        _fire("cognitive", f"native.{agent}", f"orchestrate: {prompt[:60]}", 0.5)
        for name in order:
            tried.append(name)
            try:
                if name == "native":
                    out = native_engine.generate(prompt, agent)
                    _fire("motor", f"native.{agent}", "served by native engine", 0.4)
                    return {"output": out, "served_by": "native", "is_external": False, "resources_tried": tried}
                out = await asyncio.wait_for(self._run_model(name, prompt), timeout)
                if out and out.strip():
                    _fire("motor", f"native.{agent}", f"served by {name}", 0.5)
                    return {"output": out, "served_by": name,
                            "is_external": name in ("anthropic", "openai"), "resources_tried": tried}
            except Exception:
                continue
        # the native floor guarantees we never reach here, but be safe:
        out = native_engine.generate(prompt, agent)
        return {"output": out, "served_by": "native", "is_external": False, "resources_tried": tried}

    async def _run_model(self, name: str, prompt: str) -> str:
        if name == "ollama":
            import httpx
            url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
            to = httpx.Timeout(connect=3.0, read=25.0, write=3.0, pool=3.0)
            async with httpx.AsyncClient(timeout=to) as client:
                r = await client.post(url, json={"model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                                                 "prompt": prompt, "stream": False})
                return r.json().get("response", "")
        if name == "anthropic":
            import anthropic
            client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            msg = await client.messages.create(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6"),
                                               max_tokens=int(os.getenv("GATEWAY_MAX_TOKENS", "4096")),
                                               messages=[{"role": "user", "content": prompt}])
            return msg.content[0].text
        if name == "openai":
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            comp = await client.chat.completions.create(model="gpt-4o-mini", timeout=25,
                                                        messages=[{"role": "user", "content": prompt}])
            return comp.choices[0].message.content or ""
        return ""

    async def swarm(self, agent: str, stages: List[Dict[str, str]],
                    context: str = "", prefer_external: bool = False,
                    timeout: float = 30.0) -> Dict[str, Any]:
        """Run a bespoke agent-cascade tree: each stage = {role, instruction}. Each stage is
        completed in-house-first and feeds the next — a reconfigurable, reusable swarm resource.
        `timeout` bounds each stage's model attempt (a slow local model falls to the native floor)."""
        trace: List[Dict[str, Any]] = []
        carry = context
        external_used = False
        for i, stage in enumerate(stages):
            role = stage.get("role", f"agent_{i+1}")
            instruction = stage.get("instruction", "")
            prompt = (f"You are the '{role}' agent in Workstation's native swarm.\n"
                      f"{('Prior context:\\n' + carry[:1200] + '\\n\\n') if carry else ''}"
                      f"Task: {instruction}\n\n## {role} output")
            res = await self.complete(prompt, agent=f"{agent}:{role}", timeout=timeout, prefer_external=prefer_external)
            external_used = external_used or res.get("is_external", False)
            carry = res["output"]
            trace.append({"step": i + 1, "role": role, "served_by": res["served_by"], "output": res["output"]})
        return {"agent": agent, "stages": len(stages), "trace": trace,
                "final": carry, "any_external": external_used}


orchestrator = NativeOrchestrator()
