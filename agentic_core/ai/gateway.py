import os
import time
import asyncio
import httpx
from pathlib import Path
from typing import AsyncIterator
from agentic_core.ai.guardrails import validate_response
from agentic_core.ai.logger import interaction_logger
from agentic_core.ai.memory import memory

_RECONFIG_PATH = Path("data/organism_config.json")


class _RateLimiter:
    """Token-bucket rate limiter — prevents runaway API spend."""

    def __init__(self, calls_per_minute: int):
        self._limit = calls_per_minute
        self._tokens = float(calls_per_minute)
        self._last = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last
            self._last = now
            self._tokens = min(self._limit, self._tokens + elapsed * (self._limit / 60.0))
            if self._tokens < 1:
                wait = (1 - self._tokens) * 60.0 / self._limit
                await asyncio.sleep(wait)
                self._tokens = 0
            else:
                self._tokens -= 1


class ModelGateway:
    """
    Priority order:
      1. Anthropic Claude (claude-sonnet-4-6) — best quality, used when key present
      2. OpenAI GPT-4o-mini — fallback when OPENAI_API_KEY set
      3. Ollama llama3.2 — local fallback, always available if Ollama is running

    Rate limit: GATEWAY_RPM env var (default 20 calls/min) prevents runaway spend.
    """

    def __init__(self):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.claude_model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
        self.max_tokens = int(os.getenv("GATEWAY_MAX_TOKENS", "4096"))
        rpm = int(os.getenv("GATEWAY_RPM", "20"))
        self._rate_limiter = _RateLimiter(rpm)
        self._reconfig_last_sync = 0.0
        self._reconfig_cache: dict = {}

    def _sync_reconfig(self) -> None:
        """Read the reconfiguration engine config at most once every 30 seconds."""
        now = time.monotonic()
        if now - self._reconfig_last_sync < 30.0:
            return
        self._reconfig_last_sync = now
        try:
            import json
            data = json.loads(_RECONFIG_PATH.read_text())
            self._reconfig_cache = data
            gw = data.get("gateway", {})
            new_rpm = int(gw.get("rpm_limit", 0))
            if new_rpm and new_rpm != self._rate_limiter._limit:
                self._rate_limiter._limit = new_rpm
                self._rate_limiter._tokens = min(self._rate_limiter._tokens, float(new_rpm))
        except Exception:
            pass

    def _preferred_provider(self) -> str:
        """Return preferred_provider from reconfig, defaulting to 'auto'."""
        return self._reconfig_cache.get("gateway", {}).get("preferred_provider", "auto")

    def _augment(self, prompt: str) -> str:
        ctx = memory.query_memory(prompt)
        return f"Context: {ctx}\n\nUser: {prompt}" if ctx else prompt

    # ── non-streaming ───────────────────────────────────────────────────────

    async def query(self, prompt: str, agent: str = "assistant",
                    timeout: float | None = 90.0) -> str:
        """Run one completion through the provider cascade.

        `timeout` is an OVERALL bound (seconds) on the whole cascade so an AI call
        can never hang a request indefinitely — the worst case (claude→openai→ollama)
        could otherwise stack to ~3 minutes. Interactive endpoints should pass a
        tighter value (e.g. 20) for snappy UX; pass None to disable the bound.
        On timeout we return a clearly-labelled fallback rather than blocking.
        """
        self._sync_reconfig()
        await self._rate_limiter.acquire()
        augmented = self._augment(prompt)
        try:
            if timeout is not None:
                response, provider = await asyncio.wait_for(
                    self._call(augmented, agent=agent), timeout)
            else:
                response, provider = await self._call(augmented, agent=agent)
        except asyncio.TimeoutError:
            try:
                from agentic_core.organism.immune import immune
                from agentic_core.organism.self_healing import self_healer
                immune.record(agent, "timeout")
                self_healer.record_failure("gateway")
            except Exception:
                pass
            return ("[AI unavailable — no provider responded within "
                    f"{int(timeout)}s. Configure ANTHROPIC_API_KEY (or start Ollama) "
                    "for live AI narration; the rest of this view is computed live.]")

        if not validate_response(response):
            response = "[POLICY VIOLATION] The generated response was blocked by safety guardrails."

        interaction_logger.log_interaction(agent, prompt, response)
        memory.add_memory(f"User: {prompt} | AI: {response}")
        return response

    async def _call(self, prompt: str, agent: str = "gateway") -> tuple[str, str]:
        """Try providers in priority order, return (response_text, provider_name)."""
        from agentic_core.organism.immune import immune
        from agentic_core.organism.self_healing import self_healer

        preferred = self._preferred_provider()  # "auto" | "claude" | "openai" | "ollama"

        # 1 — Anthropic Claude
        if self.anthropic_key and not self_healer.is_open("claude") and preferred in ("auto", "claude"):
            try:
                import anthropic
                client = anthropic.AsyncAnthropic(api_key=self.anthropic_key)
                msg = await client.messages.create(
                    model=self.claude_model,
                    max_tokens=self.max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                self_healer.record_success("claude")
                return msg.content[0].text, "claude"
            except Exception:
                immune.record(agent, "ai_failure")
                self_healer.record_failure("claude")

        # 2 — OpenAI
        if self.openai_key and not self_healer.is_open("openai") and preferred in ("auto", "openai"):
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=self.openai_key)
                completion = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    timeout=30,
                    max_tokens=self.max_tokens,
                )
                self_healer.record_success("openai")
                return completion.choices[0].message.content or "", "openai"
            except Exception:
                immune.record(agent, "ai_failure")
                self_healer.record_failure("openai")

        # 3 — Ollama
        if not self_healer.is_open("ollama"):
            try:
                timeout = httpx.Timeout(connect=5.0, read=120.0, write=5.0, pool=5.0)
                async with httpx.AsyncClient(timeout=timeout) as client:
                    res = await client.post(self.ollama_url, json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                    })
                self_healer.record_success("ollama")
                return res.json().get("response", ""), "ollama"
            except httpx.ConnectError:
                immune.record(agent, "ai_failure")
                self_healer.record_failure("ollama")
                return (
                    "AI engine unavailable — start Ollama with `ollama serve` "
                    "or configure ANTHROPIC_API_KEY in your environment.",
                    "error",
                )
            except httpx.ReadTimeout:
                immune.record(agent, "timeout")
                self_healer.record_failure("ollama")
                return "The model is still loading. Please retry in a moment.", "error"
            except Exception as e:
                immune.record(agent, "ai_failure")
                self_healer.record_failure("ollama")
                return f"Unexpected error ({type(e).__name__}). Please try again.", "error"

        return "All AI providers are currently unavailable. The self-healing system is monitoring recovery.", "circuit_open"

    # ── streaming ────────────────────────────────────────────────────────────

    async def stream(self, prompt: str, agent: str = "assistant") -> AsyncIterator[str]:
        """Yield response tokens as they arrive. Falls back to chunked non-streaming."""
        await self._rate_limiter.acquire()
        augmented = self._augment(prompt)

        # 1 — Anthropic streaming
        if self.anthropic_key:
            try:
                import anthropic
                client = anthropic.AsyncAnthropic(api_key=self.anthropic_key)
                full = ""
                async with client.messages.stream(
                    model=self.claude_model,
                    max_tokens=self.max_tokens,
                    messages=[{"role": "user", "content": augmented}],
                ) as s:
                    async for chunk in s.text_stream:
                        full += chunk
                        yield chunk
                interaction_logger.log_interaction(agent, prompt, full)
                memory.add_memory(f"User: {prompt} | AI: {full}")
                return
            except Exception:
                pass

        # 2 — OpenAI streaming
        if self.openai_key:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=self.openai_key)
                full = ""
                async for chunk in await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": augmented}],
                    stream=True,
                    max_tokens=self.max_tokens,
                ):
                    delta = chunk.choices[0].delta.content or ""
                    full += delta
                    if delta:
                        yield delta
                interaction_logger.log_interaction(agent, prompt, full)
                memory.add_memory(f"User: {prompt} | AI: {full}")
                return
            except Exception:
                pass

        # 3 — Ollama streaming
        try:
            import json as _json
            timeout = httpx.Timeout(connect=5.0, read=120.0, write=5.0, pool=5.0)
            full = ""
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream("POST", self.ollama_url, json={
                    "model": self.ollama_model,
                    "prompt": augmented,
                    "stream": True,
                }) as r:
                    async for line in r.aiter_lines():
                        if line:
                            try:
                                obj = _json.loads(line)
                                token = obj.get("response", "")
                                full += token
                                if token:
                                    yield token
                                if obj.get("done"):
                                    break
                            except Exception:
                                continue
            interaction_logger.log_interaction(agent, prompt, full)
            memory.add_memory(f"User: {prompt} | AI: {full}")
        except Exception as e:
            yield f"Error: {e}"


gateway = ModelGateway()
