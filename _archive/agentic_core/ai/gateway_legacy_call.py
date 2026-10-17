"""ARCHIVED (W744, 2026-10-16) from agentic_core/ai/gateway.py: ModelGateway._call and ModelGateway._preferred_provider.

A RECORD, NOT A MODULE: nothing imports this file. The class below is a shell holding the two methods verbatim, as
they stood; the gateway's module-level imports (httpx among them) are not repeated.

_call was the legacy external-first cascade: Anthropic, then OpenAI, then a local Ollama model, returning
(text, provider). Nothing called it - a whole-tree search for the method, for its name as a string and for
_preferred_provider (read only by _call) found the definition, query_meta's docstring, two comments, unrelated
test-local names and the ledgers that had recorded it as dead (v3, v5, v8, v9, v15, v16, with their
docs/fidelity_runs copies). It read neither AI_ALLOW_EXTERNAL nor the orchestrator's hourly external cap,
so a future caller would have reached an external provider without the opt-in every live path requires. The
native orchestrator serves query/query_meta and stream_meta orders its own resources; ModelGateway's docstring
states both orders.

Its failure records were the only writer of the immune kind "timeout", which left RECORDED_KINDS
(agentic_core/organism/immune.py) with it. A model timeout on a live path is recorded by the orchestrator as
"ai_failure".

To restore: git revert the commit that added this file - or paste both methods back into class ModelGateway, put
"timeout" back into the first row of RECORDED_KINDS, name ai/gateway.py again as a writer in the immune module
docstring and in the two writer tuples of integration_tests/test_mvp_spine.py, and remove the archive legs of the
W744 guard.
"""


class ModelGateway:   # a shell: the two archived methods only
    def _preferred_provider(self) -> str:
        """Return preferred_provider from reconfig, defaulting to 'auto'."""
        return self._reconfig_cache.get("gateway", {}).get("preferred_provider", "auto")

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
