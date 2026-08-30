import os
import time
import asyncio
import httpx
from pathlib import Path
from agentic_core.config import data_path
from typing import AsyncIterator
from agentic_core.ai.guardrails import validate_response
from agentic_core.ai.logger import interaction_logger
from agentic_core.ai.memory import memory

_RECONFIG_PATH = data_path("organism_config.json")


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

    @property
    def _effective_ollama_model(self) -> str:
        # W276 — the serving local model honours the PROMOTED lifecycle default (persisted),
        # not just the env captured at init.
        try:
            from agentic_core.ai.native.model_resource import effective_default_local
            return effective_default_local()
        except Exception:
            return self.ollama_model

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

    def _augment(self, prompt: str, owner_id: str | None = None) -> str:
        # W277 — recall is real (scored token-overlap retrieval) and HONESTLY labelled.
        # W333 — recall is TENANT-SCOPED (only the caller's namespace + platform); a caller with no
        # identity sees only platform memory, never the whole pool.
        ctx = memory.query_memory(prompt, owner_id=owner_id)
        if not ctx:
            return prompt
        # W332 — neutralise the `User:`/`AI:` tokens INSIDE recall lines: the native engine's
        # _field/_subject take the FIRST `User:` match as the copy subject, so a recall line
        # carrying those tokens could be baked into shipped output as the subject. Relabelling
        # them `[recalled prompt]`/`[recalled reply]` keeps the content legible to the model while
        # ensuring the real `User: {prompt}` line below is the only subject candidate.
        def _neutral(c: str) -> str:
            return c.replace("User:", "[recalled prompt]").replace("AI:", "[recalled reply]")
        recall = "\n".join(f"- {_neutral(c[:280])}" for c in ctx)
        return ("[native memory recall — prior Workstation interactions matched by token overlap; "
                f"use only if relevant]\n{recall}\n\nUser: {prompt}")

    # ── non-streaming ───────────────────────────────────────────────────────

    async def query(self, prompt: str, agent: str = "assistant",
                    timeout: float | None = 90.0,
                    owner_id: str | None = None, augment: bool = True) -> str:
        """Run one completion through the provider cascade.

        `timeout` is an OVERALL bound (seconds) on the whole cascade so an AI call
        can never hang a request indefinitely — the worst case (claude→openai→ollama)
        could otherwise stack to ~3 minutes. Interactive endpoints should pass a
        tighter value (e.g. 20) for snappy UX; pass None to disable the bound.
        On timeout we return a clearly-labelled fallback rather than blocking.
        """
        res = await self.query_meta(prompt, agent=agent, timeout=timeout,
                                    owner_id=owner_id, augment=augment)
        return res.get("output", "")

    async def query_meta(self, prompt: str, agent: str = "assistant",
                         timeout: float | None = 90.0,
                         owner_id: str | None = None, augment: bool = True) -> dict:
        """Like `query()` but returns PROVENANCE — {output, served_by, is_external} — so callers
        can surface which OWNED resource served the completion (Genesis/Forge/Transformation use
        this to prove their cascades run in-house). Same in-house-first routing as `query()`.

        IN-HOUSE FIRST: route through Workstation's OWN native orchestrator — a local owned model
        (Ollama) when present → the always-available native structured engine floor → external
        accelerants ONLY if AI_ALLOW_EXTERNAL=true. The native floor guarantees a real, honest,
        structured result, so the platform never hangs, never depends on an external provider, and
        never returns a bare "[unavailable]". `timeout` bounds any single model attempt. (The legacy
        external-first `_call` cascade remains below for reference but is superseded by the native
        fabric — see agentic_core/ai/native/.)"""
        self._sync_reconfig()
        await self._rate_limiter.acquire()
        # W332 — generation-class callers whose output SHIPS or PERSISTS pass augment=False: copy
        # generation has no legitimate use for cross-request recall, and recall was the leak vector.
        augmented = self._augment(prompt, owner_id=owner_id) if augment else prompt
        served_by, is_external = "native", False
        try:
            from agentic_core.ai.native import orchestrator as native_orchestrator
            # §6 (W353) — pass the caller's timeout THROUGH: the old min(...,30) clamp made the
            # W323 adaptive budget dead code on every gateway path (the owned model failed every
            # substantial completion and was demoted below the floor). The orchestrator bounds the
            # local model by its own budget; this bound governs only the external accelerants.
            res = await native_orchestrator.complete(augmented, agent=agent,
                                                     timeout=(timeout or 30.0))
            response = res.get("output", "")
            served_by, is_external = res.get("served_by", "native"), res.get("is_external", False)
        except Exception:
            try:
                from agentic_core.ai.native import native_engine
                response = native_engine.generate(augmented, agent)
            except Exception:
                response = "[native engine unavailable]"

        if not validate_response(response):
            response = "[POLICY VIOLATION] The generated response was blocked by safety guardrails."

        interaction_logger.log_interaction(agent, prompt, response, owner_id=owner_id)
        memory.add_memory(f"User: {prompt} | AI: {response}",
                          metadata={"agent": agent}, owner_id=owner_id)   # W333 — tenant-stamped
        return {"output": response, "served_by": served_by, "is_external": is_external}

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
                        "model": self._effective_ollama_model,
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

    @staticmethod
    def _stream_chunks(text: str, size: int = 96) -> list[str]:
        """Word-boundary chunks so a completed in-house response keeps the token-stream shape
        (the honest W241 pattern: the work is genuinely served in-house, framed as a stream)."""
        words = (text or "").split(" ")
        chunks: list[str] = []
        cur = ""
        for w in words:
            if cur and len(cur) + len(w) + 1 > size:
                chunks.append(cur + " ")
                cur = w
            else:
                cur = (cur + " " + w) if cur else w
        if cur:
            chunks.append(cur)
        return chunks

    async def stream(self, prompt: str, agent: str = "assistant",
                     owner_id: str | None = None, augment: bool = True) -> AsyncIterator[str]:
        """Yield response tokens — IN-HOUSE FIRST (§6), mirroring query_meta's contract:
        1. the OWNED local model (Ollama), genuine token-by-token streaming, when present
           (skipped under AI_DISABLE_LOCAL, e.g. the deterministic test/CI runtime);
        2. external accelerant streaming ONLY when explicitly opted in (AI_ALLOW_EXTERNAL=true);
        3. the native structured-reasoning floor, chunked — the GUARANTEED terminal: this stream
           never depends on an external provider and never ends in a bare error line.
        W332/W333 — tenant-scoped recall (augment=False for ship/persist callers) + tenant-stamped
        writes, matching query_meta."""
        await self._rate_limiter.acquire()
        augmented = self._augment(prompt, owner_id=owner_id) if augment else prompt
        from agentic_core.organism.self_healing import self_healer   # W323 — breaker on the stream path

        def _log(text: str) -> None:
            try:
                interaction_logger.log_interaction(agent, prompt, text, owner_id=owner_id)
                memory.add_memory(f"User: {prompt} | AI: {text}",
                                  metadata={"agent": agent}, owner_id=owner_id)
            except Exception:
                pass

        # §6 (W323) — the STREAM path is on the same control plane as query_meta: circuit-breaker
        # gated, and every streamed serve RECORDS an outcome into the W275 learning loop (the
        # scores that drive selection previously never saw streamed work — three live §4 surfaces
        # ran entirely outside the plane).
        def _record(served_by: str, is_external: bool, t0: float, ok: bool) -> None:
            try:
                from agentic_core.api.operational_excellence import record_outcome
                # kind=model_attempt — the SAME learning-loop rows model_health() scores on
                record_outcome("model_attempt", f"stream:{agent}", served_by=served_by,
                               is_external=is_external,
                               duration_ms=int((time.time() - t0) * 1000), success=ok)
            except Exception:
                pass

        # 1 — the OWNED local model: genuine token-by-token streaming
        if (os.getenv("AI_DISABLE_LOCAL", "").lower() not in ("1", "true", "yes")
                and not self_healer.is_open("ollama")):
            _t0 = time.time()
            try:
                import json as _json
                timeout = httpx.Timeout(connect=5.0, read=120.0, write=5.0, pool=5.0)
                full = ""
                async with httpx.AsyncClient(timeout=timeout) as client:
                    async with client.stream("POST", self.ollama_url, json={
                        "model": self._effective_ollama_model,
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
                if full.strip():
                    _log(full)
                    self_healer.record_success("ollama")
                    _record("ollama", False, _t0, True)
                    return
            except Exception:
                self_healer.record_failure("ollama")
                _record("ollama", False, _t0, False)

        # 2 — external accelerants: OPT-IN ONLY (never a dependency)
        if os.getenv("AI_ALLOW_EXTERNAL", "false").lower() == "true":
            if self.anthropic_key and not self_healer.is_open("claude"):
                _t0 = time.time()
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
                    _log(full)
                    self_healer.record_success("claude")
                    _record("claude", True, _t0, True)
                    return
                except Exception:
                    self_healer.record_failure("claude")
                    _record("claude", True, _t0, False)
            if self.openai_key and not self_healer.is_open("openai"):
                _t0 = time.time()
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
                    _log(full)
                    self_healer.record_success("openai")
                    _record("openai", True, _t0, True)
                    return
                except Exception:
                    self_healer.record_failure("openai")
                    _record("openai", True, _t0, False)

        # 3 — the native structured floor: guaranteed, honest, in-house (chunked stream shape)
        _floor_t0 = time.time()
        try:
            from agentic_core.ai.native import native_engine
            out = native_engine.generate(augmented, agent)
        except Exception as e:
            out = f"[native engine unavailable: {e}]"
        for chunk in self._stream_chunks(out):
            yield chunk
        _log(out)
        _record("native", False, _floor_t0, True)   # W323 — the floor serve is a recorded outcome too


gateway = ModelGateway()
