import os
import time
import asyncio
import httpx
from pathlib import Path
from agentic_core.config import data_path
from typing import AsyncIterator
from agentic_core.ai.guardrails import validate_response, screen_reason
from agentic_core.ai.logger import interaction_logger
from agentic_core.ai.memory import memory

_RECONFIG_PATH = data_path("organism_config.json")


# ── W505 (P2.6): the constitutional checkpoint on the AI seam ─────────────────────────────────────────
# Kept at module level, ABOVE the class, and never between a decorator and its function.

_GATE_NAME = "constitutional_policy_gate_v5"


def _policy_verdict(action_type: str, context: dict) -> dict:
    """The pre-gate's verdict. A gate that cannot be consulted does not silently allow: it says so."""
    try:
        from agentic_core.gaas.v5.policy_gate import ConstitutionalPolicyGate
        return ConstitutionalPolicyGate(domain="ai_gateway").validate(action_type, context)
    except Exception as exc:   # pragma: no cover - the gate is a pure module; an import failure is real news
        return {"allowed": True, "reason": None, "article": None,
                "gate_unavailable": f"{type(exc).__name__}: {exc}"}


def _output_verdict(output: str) -> dict:
    try:
        from agentic_core.gaas.v5.policy_gate import ConstitutionalPolicyGate
        return ConstitutionalPolicyGate(domain="ai_gateway").validate_output(output)
    except Exception as exc:   # pragma: no cover
        return {"compliant": True, "violations": [],
                "gate_unavailable": f"{type(exc).__name__}: {exc}"}


def _chain(event: dict) -> dict:
    """Append to the constitutional ledger and report WHETHER it was appended.

    The UEG refuses to append when its chain file cannot be read whole (rather than restarting the chain
    over the old one). That refusal must not take the AI down, and it must not be hidden: a checkpoint
    that claims to be recorded when it is not is worse than having none.
    """
    try:
        from agentic_core.gaas.v5.ueg import UEGLogger
        return {"recorded": True, "event_hash": UEGLogger().log(event)}
    except Exception as exc:
        return {"recorded": False,
                "not_recorded_because": f"the constitutional ledger refused the append: "
                                        f"{type(exc).__name__}: {exc}"}


def _record_halt(agent: str, pre: dict) -> dict:
    """A refused request: chained as a policy_gate_halt, which the UEG classifies as adverse."""
    chained = _chain({"type": "policy_gate_halt", "node": f"ai_gateway:{agent}",
                      "action": "ai_generation", "reason": pre.get("reason"),
                      "article": pre.get("article")})
    return {"gate": _GATE_NAME, "pre_allowed": False, "refused_reason": pre.get("reason"),
            "article": pre.get("article"), "post_checked": False, **chained}


def _record_checkpoint(agent: str, pre: dict, post: dict, screened: bool) -> dict:
    """The checkpoint every completed generation carries.

    A COMPLIANT output is chained as a routine ai.generation_gated event; a non-compliant one as an adverse
    post_validation_failure. Both are recorded, because an audit trail that only holds the bad cases cannot
    show that the good ones were checked at all.
    """
    compliant = bool(post.get("compliant", True))
    violations = list(post.get("violations") or [])
    event = {"type": "ai.generation_gated" if compliant else "post_validation_failure",
             "node": f"ai_gateway:{agent}", "action": "ai_generation",
             "compliant": compliant, "violations": violations,
             "response_screen_withheld": screened,
             #  W656 (R6.4) - what the post-check screened, recorded WITH the verdict it produced
             "post_screened": post.get("screened"), "post_coverage_limit": post.get("coverage_limit")}
    chk = {"gate": _GATE_NAME, "pre_allowed": True, "post_checked": True,
           "post_compliant": compliant, "violations": violations,
           "post_screened": post.get("screened"), "post_coverage_limit": post.get("coverage_limit"),
           # the response screen is a separate, narrower thing from the constitutional gate; saying which
           # one acted is the difference between an auditable record and a shrug.
           "response_screen_withheld": screened,
           **_chain(event)}
    for src, key in ((pre, "gate_unavailable"), (post, "gate_unavailable")):
        if src.get(key):
            chk["gate_unavailable"] = src[key]
    return chk

def _observe_floor() -> None:
    """W658 - tell the immune system a floor-served call was seen. Best-effort; never raises into a completion."""
    try:
        from agentic_core.organism.immune import immune
        immune.observe("model:native")
    except Exception:
        pass


def console_pre_gate(agent: str) -> "dict | None":
    """W619 (FU-496, M2 v8 R4.3) — the pre-gate for a call that reaches the orchestrator WITHOUT the gateway (the
    Native AI console's completion and swarm). None when allowed; the chained halt record when refused."""
    pre = _policy_verdict(agent, {"intent": agent, "domain": "ai_gateway"})
    return None if pre.get("allowed", True) else _record_halt(agent, pre)


def console_post_gate(agent: str, output: str) -> dict:
    """The checkpoint such a call carries: the same post-validation and the same ledger event a gateway
    completion records, so "every completion carries its governance checkpoint" holds for these too."""
    pre = _policy_verdict(agent, {"intent": agent, "domain": "ai_gateway"})
    return _record_checkpoint(agent, pre, _output_verdict(output or ""), screened=False)


def language_verdict(requested: str | None, served_by: str, is_floor: bool) -> dict:
    """P3.6 clause (2) — was the output delivered in the requested language, or is that NOT KNOWN?

    Three states, kept apart because they are three different facts and the defect this replaces was
    SILENT ENGLISH — an English answer to a request made in another language, with nothing saying so.

      · nothing requested            → no claim is made at all
      · the deterministic floor served → "en", by construction: it composes English prose from the
        request's labelled fields, so this is a fact and not an inference
      · a model served               → NOT VERIFIED. This platform does not inspect the language of a
        model's output. Reporting the REQUESTED language as delivered would be a claim about an outcome
        derived from the ask, which is the shape this plan exists to remove.
    """
    base = (requested or "").split("-")[0].lower()
    if not base:
        return {"language_requested": None, "language_delivered": None,
                "language_basis": "no language was requested, so no claim is made about the output's"
                                  " language"}
    if is_floor:
        delivered = "en"
        if base == "en":
            note = ("the deterministic native floor composed this, and it composes in English - which is"
                    " what was asked for")
        else:
            note = (f"NOT DELIVERED IN {base.upper()}: the deterministic native floor composed this and it"
                    f" composes in English only. The request's language was recorded and not honoured -"
                    f" an owned model that writes {base.upper()} is not installed, and this platform does"
                    f" not translate its own output")
        return {"language_requested": base, "language_delivered": delivered, "language_basis": note}
    return {"language_requested": base, "language_delivered": None,
            "language_basis": (f"{served_by} served this and the platform does NOT inspect the language of"
                               f" a model's output, so whether it is in {base.upper()} is NOT VERIFIED -"
                               f" reporting the requested language as delivered would be a claim nobody"
                               f" measured")}


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


# W489 (sweep S4.6, C3) — RECALL IS OPTED INTO, NEVER INHERITED.
# Cross-request recall used to be the DEFAULT on all four entry points, so a caller closed the leak
# only by remembering to say so. W332 set augment=False on the callers it knew about and W488 swept
# every `query_meta` call — but the audit grepped one method name, and `query`, `stream` and
# `stream_meta` were left inheriting True: 29 generation-class callers, including the live nine-stage
# synthesis cascade, the CEO blueprint and the digital-twin modeller, still had another request's
# content prepended to the prompt and presented as analysis of the caller's own subject. Fixing the
# callers one by one is what produced that gap twice; the DEFAULT is what needed to change.
# The two callers that genuinely want recall are conversations, and both already opt in by name:
# the avatar (avatars/api.py) and the AI-CEO chat (api/v138/ceo.py). Recall stays tenant-scoped by
# owner_id either way (W333).
_RECALL_OFF = False


class ModelGateway:
    """WHO SERVES A COMPLETION - in-house first, and the two entry paths do not order resources the same way.

    query / query_meta - the native orchestrator decides (ai/native/orchestrator.py):
      1. the owned local model (Ollama), when its server answers with a model pulled - skipped when
         AI_DISABLE_LOCAL is set or its circuit breaker is open, and moved behind the floor when its recent
         record is effectively dead (W380);
      2. the native deterministic floor, which always answers, so it is the last resource this path tries.
         The external accelerants (Anthropic, OpenAI: a key AND AI_ALLOW_EXTERNAL=true) are listed after it
         and are therefore never attempted here - this gateway never passes prefer_external.

    stream / stream_meta - ordered in this class:
      1. the owned local model, token by token - skipped when AI_DISABLE_LOCAL is set or its circuit
         breaker is open;
      2. the external accelerants, before the floor, ONLY when AI_ALLOW_EXTERNAL=true and a key is set
         (Anthropic, then OpenAI) - outside the orchestrator's hourly external cap (W335);
      3. the native floor, chunked - the guaranteed terminal.

    With AI_ALLOW_EXTERNAL off (the default) neither path reaches an external provider. With it on, a
    streamed reply can be served externally before the floor and a gateway query cannot (orchestrator callers
    that pass prefer_external can) - the switch is the Owner's (P4.3).

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
            # W492 (FU-183) — effective_default_local() now answers the REPORTING question (what
            # actually serves) and is None when no local model is installed. An attempt is not a
            # claim: this path still tries the configured name, and the surfaces say the floor served.
            from agentic_core.ai.native.model_resource import (effective_default_local,
                                                              configured_default_local)
            return effective_default_local() or configured_default_local() or self.ollama_model
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

    @staticmethod
    def _is_floor(served_by: str | None) -> bool:
        """True when the deterministic floor served this, not a model.

        W505 (P2.1) — "floor output is never STORED for recall". The floor's structured prose is this
        engine's own framing; storing it means that the moment recall is switched on, the floor recalls
        its own scaffolding as though it were prior knowledge. The engine's declared name is imported
        rather than the string "native" hardcoded, so renaming it cannot silently re-enable storing."""
        try:
            from agentic_core.ai.native.engine import NativeReasoningEngine as _NSE
            floor_name = getattr(_NSE, "name", "native")
        except Exception:
            floor_name = "native"
        return (served_by or floor_name) == floor_name

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
            # W475 (ledger v4 R3.1) — a recalled prompt's persona ('You are the CGO …') must not become THIS
            # call's '_Acting as:' line: the engine reads the first persona in the text it is given.
            c = __import__("re").sub(r"\b(?:You are|As)\s+(?:the|a|an)\b", "[recalled role]", c)
            return c.replace("User:", "[recalled prompt]").replace("AI:", "[recalled reply]")
        recall = "\n".join(f"- {_neutral(c[:280])}" for c in ctx)
        # W507 (FU-256b, OWNER RULING 2026-09-29) — THE DISCLOSURE THE OWNER CHOSE OVER REGENERATION.
        # W489 found 29 generation callers inheriting the recall default as ON, so rows stored before that
        # flip may hold
        # another request's content. A stored row carries no timestamp, so an UNMARKED row cannot be
        # distinguished from a clean one - and the rows marked `from_augmented_prompt` are only those written
        # since W507. Saying the pool is clean would be false; saying it is all blended would be false too.
        # This states which it is and why, because a recalled line is about to be read as prior knowledge.
        return ("[native memory recall — prior Workstation interactions matched by token overlap; "
                "use only if relevant. PROVENANCE LIMIT: a recalled line written before W507 carries no "
                "marker saying whether it was itself produced from a prompt that had another request's "
                "content prepended (the defect W489 stopped), so it MAY contain material from a different "
                "subject. Treat a recalled line as a prior interaction, never as established fact about "
                f"this one]\n{recall}\n\nUser: {prompt}")

    # ── non-streaming ───────────────────────────────────────────────────────

    async def query(self, prompt: str, agent: str = "assistant",
                    timeout: float | None = 90.0,
                    owner_id: str | None = None, augment: bool = _RECALL_OFF,
                    governance: dict | None = None, user_text: str | None = None) -> str:
        """Run one completion through `query_meta` and return its text only - who served it and the
        governance checkpoint are dropped, so a caller that must say who served it uses `query_meta`.

        `timeout` is handed to the orchestrator, which applies it to an external accelerant attempt only,
        and this path never attempts one (see the class docstring). The owned local model runs on its own
        budget (orchestrator.local_model_budget_s) and the native floor answers in-process.
        None is read as 30.
        """
        res = await self.query_meta(prompt, agent=agent, timeout=timeout,
                                    owner_id=owner_id, augment=augment, governance=governance,
                                    user_text=user_text)
        return res.get("output", "")

    async def query_meta(self, prompt: str, agent: str = "assistant",
                         timeout: float | None = 90.0,
                         owner_id: str | None = None, augment: bool = _RECALL_OFF,
                         governance: dict | None = None,
                         language: str | None = None, user_text: str | None = None) -> dict:
        """Like `query()` but returns PROVENANCE — {output, served_by, is_external} — so callers
        can surface which OWNED resource served the completion (Genesis/Forge/Transformation use
        this to prove their cascades run in-house). Same in-house-first routing as `query()`.

        IN-HOUSE FIRST: route through Workstation's OWN native orchestrator — a local owned model
        (Ollama) when present → the always-available native structured engine floor, which answers, so
        the external accelerants the registry lists after it (a key AND AI_ALLOW_EXTERNAL=true) are never
        attempted on this path. The native floor guarantees a real, honest,
        structured result, so the platform never hangs, never depends on an external provider, and
        never returns a bare "[unavailable]". `timeout` reaches the orchestrator, which applies it to an
        external attempt only; the local model runs on its own budget. (The legacy external-first `_call`
        cascade, which nothing called, is archived at _archive/agentic_core/ai/gateway_legacy_call.py.)"""
        self._sync_reconfig()
        await self._rate_limiter.acquire()
        #  W741 (S18.1) - the token bases are the orchestrator's own sentences, imported rather than retyped
        from agentic_core.ai.native.orchestrator import FLOOR_TOKENS_BASIS, REFUSED_TOKENS_BASIS
        # W505 (P2.6) — THE CONSTITUTIONAL PRE-GATE, on the seam every generation passes through. Before
        # this the gate had four callers and none of them was the AI gateway, so the claim that every
        # action is constitutionally gated held for the economy and not for a single completion.
        _gov = dict(governance or {})
        _gate_ctx = {"intent": agent, "domain": "ai_gateway", **_gov}
        # The gate screens its action_type argument; `context["intent"]` is only consulted when
        # action_type is falsy, so passing a constant there would screen the constant and nothing else -
        # a gate that cannot refuse. The DECLARED INTENT is the action type; the constant is the domain.
        _pre = _policy_verdict(agent, _gate_ctx)
        if not _pre.get("allowed", True):
            _halt = _record_halt(agent, _pre)
            return {"output": f"[CONSTITUTIONAL REFUSAL] {_pre.get('reason')}",
                    "served_by": "constitutional_policy_gate", "is_external": False,
                    #  shape-complete with the success return: a caller reading the language verdict on a
                    #  refusal gets one rather than a KeyError, and a refusal is not in any language
                    **language_verdict(language, "constitutional_policy_gate", False),
                    #  and the recall keys, for the same reason: a refusal entered no recall pool, and
                    #  saying so is not the same as the key being absent
                    "recall_stored": False,
                    "recall_not_stored_because": ("the request was refused by the constitutional gate, so there was no answer to store"),
                    "recall_stored": False,
                    "recall_not_stored_because": "the request was refused before any model ran, so there "
                                                 "is no completion to recall",
                    "profile_applied": False,
                    "profile_state": "not_read", "profile_basis": "the request was refused before any profile was read",
                    "governance_checkpoint": _halt,
                    #  W741 (S18.1) - shape-complete: a refusal ran no model, so nothing counted
                    "model_tokens": None, "model_tokens_basis": REFUSED_TOKENS_BASIS}
        #  W734 (FU-932) - THE FAITH RULING SCREEN AT THE FLOOR. The four doors that screened a request for a
        #  religious ruling were four of many: authorship, solve, BDP, design-dev and the Genesis journey asked a
        #  model with no screen. It runs here, over the PERSON'S OWN WORDS only (an instruction a route wrote
        #  cannot trigger it), and answers with the constitutional refusal's own shape. A request it does not
        #  refuse was not found sound: it may refuse, never clear.
        from agentic_core.religious_domain.composed_text import faith_ruling_refusal
        _faith = faith_ruling_refusal(user_text, "request")
        if _faith:
            return {"output": f"[CONSTITUTIONAL REFUSAL] {_faith['message']}",
                    "served_by": "constitutional_policy_gate", "is_external": False, "refused": True,
                    "faith_refusal": _faith,
                    **language_verdict(language, "constitutional_policy_gate", False),
                    "recall_stored": False,
                    "recall_not_stored_because": "the request was refused before any model ran, so there "
                                                 "is no completion to recall",
                    "profile_applied": False,
                    "profile_state": "not_read", "profile_basis": "the request was refused before any profile was read",
                    "governance_checkpoint": _record_halt(agent, {"allowed": False, "reason": _faith["message"],
                                                                   "article": "A.9.5: no AI gives a religious ruling"}),
                    "model_tokens": None, "model_tokens_basis": REFUSED_TOKENS_BASIS}   # W741 (S18.1)
        # W332 — generation-class callers whose output SHIPS or PERSISTS must not carry cross-request
        # recall: recall was the leak vector. W489 made that the DEFAULT (see _RECALL_OFF above)
        # rather than a convention each caller had to remember, because two rounds of fixing callers
        # one at a time still left twenty-nine of them inheriting it.
        augmented = self._augment(prompt, owner_id=owner_id) if augment else prompt
        # §4.2 (W428) — the person's OWN explicit profile, applied INDEPENDENTLY of `augment`.
        # That independence is the point: no generation-class caller receives recall (W332 by
        # recall was the leak vector), and those are exactly the surfaces where "understand the
        # person" was missing. Recall is inference over other requests; this is the user's own
        # words, which they wrote, can read back, and can delete. Different trust, different switch.
        from agentic_core.ai.user_context import preamble_state
        _pstate = preamble_state(owner_id)          # W616 (FU-397) — which fact produced the preamble
        _preamble = _pstate["preamble"]
        augmented = _preamble + augmented
        served_by, is_external = "native", False
        #  W741 (OWNER RULING S18.1) - the token count the serving model reported, carried to the reply. It
        #  starts as the floor's answer because the except branch below IS the floor; the orchestrator's reply
        #  replaces it with what counted, or why nothing did.
        _mt, _mt_basis = None, FLOOR_TOKENS_BASIS
        try:
            from agentic_core.ai.native import orchestrator as native_orchestrator
            # §6 (W353) — pass the caller's timeout THROUGH: the old min(...,30) clamp made the
            # W323 adaptive budget dead code on every gateway path (the owned model failed every
            # substantial completion and was demoted below the floor). The orchestrator bounds the
            # local model by its own budget; this bound governs only the external accelerants.
            res = await native_orchestrator.complete(augmented, agent=agent,
                                                     timeout=(timeout or 30.0), user_text=user_text,
                                                     language=language)      # W738 - the Arabic rule's exception
            response = res.get("output", "")
            _arabic738 = res.get("arabic")
            served_by, is_external = res.get("served_by", "native"), res.get("is_external", False)
            _mt = res.get("model_tokens")
            _mt_basis = (res.get("model_tokens_basis")
                         or "NOT COUNTED - the orchestrator's reply carried no token count; null, never 0")
        except Exception:
            try:
                from agentic_core.ai.native import native_engine
                response = native_engine.generate(augmented, agent, user_text=user_text)
                _observe_floor()           # W658 - a floor-served call is a call the organism saw
            except Exception:
                response = "[native engine unavailable]"
            from agentic_core.religious_domain.composed_text import apply_arabic_rule
            response, _arabic738 = apply_arabic_rule(response, language)     # W738 - the fallback floor too

        _screen = screen_reason(response)
        if _screen:
            # W505 (P2.6) — the basis travels with the refusal. A bare "[POLICY VIOLATION]" told the person
            # nothing they could act on or dispute.
            response = ("[POLICY VIOLATION] The generated response was withheld by the response screen: "
                        f"{_screen}.")
        # W505 (P2.6) — the POST gate FLAGS and chains; it does not replace. validate_output matches
        # `DROP TABLE` and `rm -rf /`, so replacing on a match would destroy a correct answer ABOUT them.
        _post = _output_verdict(response)
        _chk = _record_checkpoint(agent, _pre, _post, screened=bool(_screen))

        interaction_logger.log_interaction(agent, prompt, response, owner_id=owner_id)
        # W505 (P2.1) — the FLOOR'S OUTPUT is not stored for recall; the USER'S OWN WORDS still are.
        # A first cut dropped the whole "User: … | AI: …" record when the floor served, which also threw
        # away the half recall exists for: what the person said. The interaction LOG above keeps both
        # either way - that is an audit trail, not a recall pool.
        _floor = self._is_floor(served_by)
        _stored = not _floor
        if _floor:
            memory.add_memory(f"User: {prompt}",
                              metadata={"agent": agent, "ai_reply_withheld": "served by the "
                                        "deterministic floor - its structured prose is the engine's own "
                                        "framing, not prior knowledge to recall",
                                        # W507 (FU-256c) — whether THIS row was produced from a prompt that
                                        # had another request's content prepended. Only a write can know it,
                                        # and without it no per-row disclosure is possible at all.
                                        **({"from_augmented_prompt": True} if augment else {})},
                              owner_id=owner_id)   # W333 — tenant-stamped
        else:
            memory.add_memory(f"User: {prompt} | AI: {response}",
                              metadata={"agent": agent,
                                        **({"from_augmented_prompt": True} if augment else {})},
                              owner_id=owner_id)   # W333 — tenant-stamped
        # W428 — DISCLOSED, not silent. A profile that shapes output without the caller being able
        # to tell is the same opacity §10 spent this cycle removing from the quality record.
        return {"output": response, "served_by": served_by, "is_external": is_external,
                #  P3.6 clause (2) — the language verdict travels WITH the output, because a disclosure on
                #  the settings page is not a label on the text
                **language_verdict(language, served_by, _floor),
                # W505 (P2.1) — said, not silent: a caller can tell whether this answer entered the
                # recall pool, and why it did not.
                "recall_stored": _stored,
                #  SHAPE-COMPLETE, not conditional. This was spread in only when the answer was NOT
                #  stored, so a caller indexing it after a stored answer got a KeyError. None means it
                #  WAS stored, which is a different fact from the key being absent.
                "recall_not_stored_because": (
                    None if _stored else
                    "the deterministic floor served this, so its structured prose was withheld from the "
                    "recall pool - it is the engine's own framing, not prior knowledge. Your own "
                    "message was kept."),
                #  W623 (FU-533, M1 v9 R5.0) — APPLIED MEANS READ. The preamble is prepended for every server, and
                #  the deterministic floor does not read a profile: it composes from labelled fields. So a floor reply
                #  reported profile_applied=True and the avatar showed "your saved profile shaped this answer". A
                #  profile reached the prompt; it shaped the answer only when a model served it.
                "profile_applied": bool(_preamble) and not self._is_floor(served_by),
                "profile_state": ("not_usable_by_floor" if (_preamble and self._is_floor(served_by)) else _pstate["state"]),
                "profile_basis": (("your saved profile reached the prompt, but the deterministic floor served this and "
                                   "it does not read a profile, so the profile did NOT shape this answer")
                                  if (_preamble and self._is_floor(served_by)) else _pstate["basis"]),
                # W505 (P2.6) — every gateway response carries its governance checkpoint: what the gate
                # decided before and after, and whether the constitutional ledger actually recorded it.
                "governance_checkpoint": _chk,
                #  W738 - what the Arabic rule did to this answer (withheld passages, or kept and labelled)
                "arabic": _arabic738,
                #  W741 (S18.1) - what the serving model reported it spent, or null and why nothing counted
                "model_tokens": _mt, "model_tokens_basis": _mt_basis}

    #  W744 - `_call`, the legacy external-first cascade (Anthropic, then OpenAI, then a local model), and
    #  `_preferred_provider`, which only it read, are archived verbatim at
    #  _archive/agentic_core/ai/gateway_legacy_call.py. Nothing called either, and `_call` read neither
    #  AI_ALLOW_EXTERNAL nor the hourly external cap.

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

    async def _stream_owned_model(self, augmented: str) -> AsyncIterator[str]:
        """W451 — the OWNED local model's token stream, factored out so the provenance seam can be
        proved both ways (a test substitutes this and the final event must name the model)."""
        import json as _json
        timeout = httpx.Timeout(connect=5.0, read=120.0, write=5.0, pool=5.0)
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
                            if token:
                                yield token
                            if obj.get("done"):
                                #  W741 (S18.1) - the final object carries the server's token count. It is
                                #  yielded as a ZERO-LENGTH CountedText that the stream reads and does not
                                #  stream: a count is not text
                                from agentic_core.ai.native.orchestrator import ollama_counted
                                yield ollama_counted("", obj)
                                break
                        except Exception:
                            continue

    async def stream_meta(self, prompt: str, agent: str = "assistant",
                          owner_id: str | None = None, augment: bool = _RECALL_OFF,
                          user_text: str | None = None, language: str | None = None) -> AsyncIterator[dict]:
        """W738 - the stream with the Arabic rule: each token passes ArabicStreamFilter (unless the person asked
        for an Arabic-script language), and the terminal frame's text is ruled inside _final."""
        from agentic_core.religious_domain.composed_text import ArabicStreamFilter, arabic_script_requested
        _keep = arabic_script_requested(language)
        _flt = ArabicStreamFilter()
        async for ev in self._stream_meta_inner(prompt, agent=agent, owner_id=owner_id, augment=augment,
                                                user_text=user_text, language=language):
            if "token" in ev and not _keep:
                _t = _flt.feed(ev["token"])
                if _t:
                    yield {"token": _t}
                continue
            yield ev

    async def _stream_meta_inner(self, prompt: str, agent: str = "assistant",
                                 owner_id: str | None = None, augment: bool = _RECALL_OFF,
                                 user_text: str | None = None, language: str | None = None) -> AsyncIterator[dict]:
        """Yield {"token": …} events then ONE terminal {"done": True, "served_by", "is_external",
        "output", "guardrail_passed", "profile_applied"} — IN-HOUSE FIRST (§6), in its own order, which
        differs from query_meta's (see the class docstring):
        1. the OWNED local model (Ollama), genuine token-by-token streaming, when present
           (skipped under AI_DISABLE_LOCAL, e.g. the deterministic test/CI runtime);
        2. external accelerant streaming ONLY when explicitly opted in (AI_ALLOW_EXTERNAL=true);
        3. the native structured-reasoning floor, chunked — the GUARANTEED terminal: this stream
           never depends on an external provider and never ends in a bare error line.
        W451 (P1.3) — the stream path used to swallow WHO served it (recorded into the learning
        loop, never surfaced), so no SSE consumer could tell a user the floor answered; and it
        applied neither the §4.2 profile preamble nor the guardrail that query_meta applies.
        W332/W333 — tenant-scoped recall (off by default since W489; two conversational callers opt
        back in by name) + tenant-stamped
        writes, matching query_meta."""
        await self._rate_limiter.acquire()
        from agentic_core.ai.native.orchestrator import FLOOR_TOKENS_BASIS, REFUSED_TOKENS_BASIS   # W741 (S18.1)
        # W619 (FU-496, M2 v8 R4.3) — THE STREAM PATH IS GATED AS query_meta IS. stream_meta applied the response
        # guardrail and neither the constitutional pre-gate nor the post-checkpoint, so the CEO chat, the projects
        # stream, the business plan and the synthesis stream produced completions with no governance record.
        _pre = _policy_verdict(agent, {"intent": agent, "domain": "ai_gateway"})
        if not _pre.get("allowed", True):
            yield {"done": True, "served_by": "constitutional_policy_gate", "is_external": False,
                   "output": f"[CONSTITUTIONAL REFUSAL] {_pre.get('reason')}", "guardrail_passed": None,
                   "profile_applied": False, "governance_checkpoint": _record_halt(agent, _pre),
                   "model_tokens": None, "model_tokens_basis": REFUSED_TOKENS_BASIS}   # W741 (S18.1)
            return
        #  W734 (FU-932) - the faith ruling screen on the STREAM path too (the second writer, W475)
        from agentic_core.religious_domain.composed_text import faith_ruling_refusal
        _faith = faith_ruling_refusal(user_text, "request")
        if _faith:
            yield {"done": True, "served_by": "constitutional_policy_gate", "is_external": False, "refused": True,
                   "output": f"[CONSTITUTIONAL REFUSAL] {_faith['message']}", "guardrail_passed": None,
                   "faith_refusal": _faith, "profile_applied": False,
                   "governance_checkpoint": _record_halt(agent, {"allowed": False, "reason": _faith["message"],
                                                                   "article": "A.9.5: no AI gives a religious ruling"}),
                   "model_tokens": None, "model_tokens_basis": REFUSED_TOKENS_BASIS}   # W741 (S18.1)
            return
        augmented = self._augment(prompt, owner_id=owner_id) if augment else prompt
        from agentic_core.religious_domain.composed_text import apply_arabic_rule      # W738
        from agentic_core.ai.user_context import load_preamble
        _preamble = load_preamble(owner_id)
        augmented = _preamble + augmented
        from agentic_core.organism.self_healing import self_healer   # W323 — breaker on the stream path

        def _log(text: str, served_by: str | None = None) -> None:
            try:
                interaction_logger.log_interaction(agent, prompt, text, owner_id=owner_id)
                # W505 (P2.1) — the same rule as query_meta, at the second writer. A truth fix is done
                # only when EVERY writer says the new truth (W475), and this path stores too: the user's
                # words are kept, the floor's prose is not.
                if self._is_floor(served_by):
                    memory.add_memory(f"User: {prompt}",
                                      metadata={"agent": agent, "ai_reply_withheld": "served by the "
                                                "deterministic floor",
                                                **({"from_augmented_prompt": True} if augment else {})},
                                      owner_id=owner_id)
                else:
                    memory.add_memory(f"User: {prompt} | AI: {text}",
                                      metadata={"agent": agent,
                                                **({"from_augmented_prompt": True} if augment else {})},
                                      owner_id=owner_id)
            except Exception:
                pass

        # §6 (W323) — the STREAM path is on the same control plane as query_meta: circuit-breaker
        # gated, and every streamed serve RECORDS an outcome into the W275 learning loop.
        def _record(served_by: str, is_external: bool, t0: float, ok: bool, tokens: int | None = None) -> None:
            try:
                from agentic_core.api.operational_excellence import record_outcome
                record_outcome("model_attempt", f"stream:{agent}", served_by=served_by,
                               is_external=is_external,
                               duration_ms=int((time.time() - t0) * 1000), success=ok,
                               tokens=tokens)        # W741 (S18.1) - one spend with the seconds
            except Exception:
                pass

        _NOTICE = "\n[POLICY VIOLATION] The generated response was blocked by safety guardrails."

        def _final(full: str, served_by: str, is_external: bool, model_tokens: int | None = None,
                   model_tokens_basis: str | None = None) -> dict:
            """The terminal frame — and the guardrail is applied BEFORE anything is persisted (refuter
            F2: the first cut logged the raw text into tenant memory, then judged it). A streamed
            reply cannot be retracted, so the notice is a token every consumer sees; what is
            logged and remembered is the replacement, exactly as query_meta persists it."""
            full, _arabic738s = apply_arabic_rule(full, language)          # W738 - before anything is kept
            ok = validate_response(full)
            _log(full if ok else _NOTICE.strip(), served_by)
            return {"done": True, "served_by": served_by, "is_external": is_external,
                    "output": full if ok else _NOTICE.strip(),
                    "guardrail_passed": ok, "profile_applied": bool(_preamble) and not self._is_floor(served_by),
                    "governance_checkpoint": _record_checkpoint(agent, _pre, _output_verdict(full),
                                                                screened=not ok),
                    "arabic": _arabic738s,
                    #  W741 (S18.1) - the count the serving model reported, or null and why nothing counted
                    "model_tokens": model_tokens,
                    "model_tokens_basis": model_tokens_basis or (
                        FLOOR_TOKENS_BASIS if self._is_floor(served_by) else
                        f"NOT COUNTED - {served_by} served this and this platform reads no token count from it; "
                        "null, never 0")}

        # 1 — the OWNED local model: genuine token-by-token streaming
        if (os.getenv("AI_DISABLE_LOCAL", "").lower() not in ("1", "true", "yes")
                and not self_healer.is_open("ollama")):
            _t0 = time.time()
            try:
                full = ""
                _count = None     # W741 (S18.1) - the zero-length CountedText the stream ends with, if any
                async for token in self._stream_owned_model(augmented):
                    if getattr(token, "model_tokens_basis", None):   # the server's count, not text
                        _count = token
                        continue
                    full += token
                    yield {"token": token}
                _mt = getattr(_count, "model_tokens", None)
                _mt_basis = (getattr(_count, "model_tokens_basis", None)
                             or "NOT COUNTED - no count was read from the local model's stream; null, never 0")
                if full.strip():
                    self_healer.record_success("ollama")
                    _record("ollama", False, _t0, True, tokens=_mt)
                    _fin = _final(full, f"ollama:{self._effective_ollama_model}", False, _mt, _mt_basis)
                    if not _fin["guardrail_passed"]:
                        yield {"token": _NOTICE}
                    yield _fin
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
                            yield {"token": chunk}
                    self_healer.record_success("claude")
                    _record("claude", True, _t0, True)
                    _fin = _final(full, "claude", True)
                    if not _fin["guardrail_passed"]:
                        yield {"token": _NOTICE}
                    yield _fin
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
                            yield {"token": delta}
                    self_healer.record_success("openai")
                    _record("openai", True, _t0, True)
                    _fin = _final(full, "openai", True)
                    if not _fin["guardrail_passed"]:
                        yield {"token": _NOTICE}
                    yield _fin
                    return
                except Exception:
                    self_healer.record_failure("openai")
                    _record("openai", True, _t0, False)

        # 3 — the native structured floor: guaranteed, honest, in-house (chunked stream shape)
        _floor_t0 = time.time()
        try:
            from agentic_core.ai.native import native_engine
            out = native_engine.generate(augmented, agent, user_text=user_text)
            _observe_floor()               # W658
        except Exception as e:
            out = f"[native engine unavailable: {e}]"
        for chunk in self._stream_chunks(out):
            yield {"token": chunk}
        _record("native", False, _floor_t0, True)   # W323 — the floor serve is a recorded outcome too
        _fin = _final(out, "native", False)
        if not _fin["guardrail_passed"]:
            yield {"token": _NOTICE}
        yield _fin

    async def stream(self, prompt: str, agent: str = "assistant",
                     owner_id: str | None = None, augment: bool = _RECALL_OFF,
                     user_text: str | None = None) -> AsyncIterator[str]:
        """Token-only view of `stream_meta` (the three older SSE consumers keep their shape)."""
        async for ev in self.stream_meta(prompt, agent=agent, owner_id=owner_id, augment=augment,
                                         user_text=user_text):
            if "token" in ev:
                yield ev["token"]

gateway = ModelGateway()
