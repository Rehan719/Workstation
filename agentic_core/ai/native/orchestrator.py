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
import time
from typing import Any, Dict, List, Optional

from agentic_core.ai.native.engine import native_engine
from agentic_core.ai.native.model_resource import registry
from agentic_core.ai.native.homeostasis import homeostasis


def _fire(signal_type: str, source: str, msg: str, intensity: float = 0.5) -> None:
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal(signal_type, source, msg[:80], intensity)
    except Exception:
        pass


def _record_model(name: str, success: bool, t0: float) -> None:
    """Record a real per-model-resource attempt (kind=model_attempt) so the orchestrator can
    LEARN which owned/external models actually perform. Best-effort, non-critical."""
    try:
        from agentic_core.api.operational_excellence import record_outcome
        record_outcome("model_attempt", f"model:{name}", served_by=name,
                       is_external=name in ("anthropic", "openai"),
                       duration_ms=int((time.monotonic() - t0) * 1000), success=success)
    except Exception:
        pass


def _breaker_open(name: str) -> bool:
    """§6×§8 (W278) — consult the organism's self-healing circuit breaker before spending a
    timeout on a model that keeps failing. Fail-open: no organism → no skip."""
    try:
        from agentic_core.organism.self_healing import self_healer
        return bool(self_healer.is_open(f"model:{name}"))
    except Exception:
        return False


def _organism_report(name: str, success: bool) -> None:
    """§6×§8 (W278) — the native path re-joins the living organism: a model failure raises immune
    threat AND trips the self-healing circuit breaker (the legacy cascade had this; the native path
    had silently dropped it); a success heals the breaker. Best-effort, never raises."""
    try:
        from agentic_core.organism.self_healing import self_healer
        (self_healer.record_success if success else self_healer.record_failure)(f"model:{name}")
    except Exception:
        pass
    if not success:
        try:
            from agentic_core.organism.immune import immune
            immune.record(f"model:{name}", "ai_failure")
        except Exception:
            pass


_PROBATION_AFTER_S = 600   # a deprioritised model earns ONE fresh try after this long untried


def _reorder_by_health(order: List[str]) -> List[str]:
    """Adapt selection to real recorded performance — the §6 learning loop CLOSED (W275):
    - POSITIVE selection: candidates ahead of the native floor are ordered by their measured
      RECENCY-WINDOWED score (success rate, then speed) once they have ≥3 windowed runs — the
      best-performing owned model is genuinely preferred, not merely the not-yet-failed one.
      Unmeasured models keep their registry position (exploration beats permanent ignorance).
    - Demotion is windowed, not all-time: a model is moved AFTER the native floor only on a
      clearly-poor RECENT record — one bad hour doesn't condemn it forever.
    - PROBATION RETURN: a demoted model untried for _PROBATION_AFTER_S earns one fresh attempt
      (kept in its slot), so exile is never permanent — recovery is measurable.
    Native is NEVER deprioritised; with no recorded data the order is unchanged. Honest: every
    signal is a real recorded row (attempts + measured QMS quality), nothing invented."""
    try:
        from agentic_core.api.operational_excellence import model_health
        health = model_health()
    except Exception:
        return order

    def _age_s(name: str) -> float:
        import calendar
        h = health.get(name) or {}
        try:
            # rows are stamped in UTC — parse as UTC (timegm), NOT local (mktime), or every fresh
            # row looks a timezone-offset old and probation triggers immediately
            return max(0.0, time.time() - calendar.timegm(time.strptime(h.get("last_at", ""),
                                                                        "%Y-%m-%dT%H:%M:%SZ")))
        except (ValueError, OverflowError):
            return float("inf")

    def poor(name: str) -> bool:
        h = health.get(name)
        if not (h and h.get("window_runs", 0) >= 5 and h["success_rate"] < 0.6):
            return False
        return _age_s(name) < _PROBATION_AFTER_S      # long-untried → probation try, not exile

    good = [n for n in order if n == "native" or not poor(n)]
    bad = [n for n in order if n != "native" and poor(n)]

    # positive selection among the measured candidates AHEAD of the native floor
    if "native" in good:
        _floor = good.index("native")
        head, tail = good[:_floor], good[_floor:]
    else:
        head, tail = good, []

    def _score(name: str):
        h = health.get(name) or {}
        if h.get("window_runs", 0) >= 3:
            return (0, -h["success_rate"], h.get("avg_ms", 0))   # measured: best rate, then fastest
        return (1, 0, 0)                                          # unmeasured: keep registry order
    head.sort(key=_score)
    return head + tail + bad


class NativeOrchestrator:
    """In-house-first orchestration over owned + local + (optional) external model resources."""

    async def complete(self, prompt: str, agent: str = "assistant",
                       timeout: float = 30.0, prefer_external: bool = False,
                       prefer: str = "auto") -> Dict[str, Any]:
        # §6/§7 user design control over WHICH owned tier serves:
        #   "auto"   — in-house-first selection (local model → native floor → opt-in external)
        #   "native" — force the deterministic native FLOOR (fast · free · reproducible)
        #   "local"  — require the local owned model (Ollama), falling back to the floor if it is unavailable
        if prefer == "native":
            order = ["native"]
        elif prefer == "local":
            order = ["ollama", "native"]   # require the local model first; floor only as graceful fallback
        elif prefer.startswith("ollama:") or prefer.startswith("local:"):
            # route to a SPECIFIC owned local model by name (floor fallback if it cannot serve)
            order = [f"ollama:{prefer.split(':', 1)[1]}", "native"]
        else:
            order = _reorder_by_health(registry.select(prefer_external=prefer_external))
        tried: List[str] = []
        _fire("cognitive", f"native.{agent}", f"orchestrate: {prompt[:60]}", 0.5)
        for name in order:
            if name != "native" and _breaker_open(name):
                tried.append(f"{name} (circuit-open, skipped)")   # §6×§8 (W278) — honest skip
                continue
            tried.append(name)
            if name == "native":
                out = native_engine.generate(prompt, agent)
                _fire("motor", f"native.{agent}", "served by native engine", 0.4)
                return {"output": out, "served_by": "native", "is_external": False, "resources_tried": tried}
            _t = time.monotonic()
            try:
                out = await asyncio.wait_for(self._run_model(name, prompt), timeout)
                if out and out.strip():
                    _record_model(name, True, _t)        # learned: this model performed
                    _organism_report(name, True)         # §6×§8 (W278) — breaker heals on success
                    _fire("motor", f"native.{agent}", f"served by {name}", 0.5)
                    return {"output": out, "served_by": name,
                            "is_external": name in ("anthropic", "openai"), "resources_tried": tried}
                _record_model(name, False, _t)           # empty output = failure
                _organism_report(name, False)            # §6×§8 (W278) — raises immune + breaker
            except Exception:
                _record_model(name, False, _t)           # error/timeout = failure
                _organism_report(name, False)
                continue
        # the native floor guarantees we never reach here, but be safe:
        out = native_engine.generate(prompt, agent)
        return {"output": out, "served_by": "native", "is_external": False, "resources_tried": tried}

    async def ensemble(self, prompt: str, agent: str = "ensemble", models: Optional[List[str]] = None,
                       synthesize: bool = True, timeout: float = 30.0) -> Dict[str, Any]:
        """§6 — run a prompt across MULTIPLE owned models in parallel, then synthesise a consensus. Owned
        orchestration as a composable resource. Defaults to the discovered local models (each routed by name)
        plus the native floor; every member reports which owned resource served it."""
        if not models:
            # W276 — default orchestration draws on the ACTIVE estate (discovered minus retired)
            from agentic_core.ai.native.model_resource import active_local_models
            lm = active_local_models()
            models = ([f"ollama:{m}" for m in lm] + ["native"]) if lm else ["native"]
        models = [m for m in models if m][:5]
        _fire("cognitive", f"native.{agent}", f"ensemble across {len(models)} owned models", 0.6)
        results = await asyncio.gather(
            *[self.complete(prompt, agent=f"{agent}-{i}", prefer=m, timeout=timeout) for i, m in enumerate(models)],
            return_exceptions=True)
        members: List[Dict[str, Any]] = []
        for m, r in zip(models, results):
            if isinstance(r, Exception):
                members.append({"model": m, "error": str(r)[:160]})
            else:
                members.append({"model": m, "served_by": r.get("served_by"),
                                "is_external": r.get("is_external", False), "output": r.get("output", "")})
        synthesis = None
        produced = [x for x in members if x.get("output")]
        if synthesize and len(produced) > 1:
            combined = "\n\n".join(f"[{x['model']} · served by {x.get('served_by')}]:\n{x['output'][:800]}" for x in produced)
            syn = await self.complete(
                "You are an ensemble synthesiser. Given these model outputs for the SAME prompt, produce the "
                "single best consensus answer — combine strengths, resolve disagreements, and note any genuine "
                f"divergence.\n\nPrompt: {prompt}\n\nMODEL OUTPUTS:\n{combined}\n\n"
                "## Consensus Answer\n## Notable Agreement / Disagreement", agent=f"{agent}-synth",
                prefer="auto", timeout=timeout)
            synthesis = {"output": syn.get("output", ""), "served_by": syn.get("served_by")}
        return {"prompt": prompt[:200], "models_run": models, "members": members, "synthesis": synthesis,
                "method": "parallel ensemble across owned models → consensus synthesis"}

    async def _run_model(self, name: str, prompt: str) -> str:
        if name == "ollama" or name.startswith("ollama:"):
            # AI_DISABLE_LOCAL=1 means NO local inference at all (deterministic deployments / the test suite),
            # even for a directly-named model route — fall through to the native floor.
            if os.getenv("AI_DISABLE_LOCAL", "").lower() in ("1", "true", "yes"):
                return ""
            import httpx
            # "ollama" → the default model; "ollama:<name>" → that specific owned local model.
            # W276 — the default local model honours the PROMOTED lifecycle default (persisted),
            # falling back to the OLLAMA_MODEL env; explicit ollama:<name> stays the user's choice.
            from agentic_core.ai.native.model_resource import effective_default_local
            model = name.split(":", 1)[1] if ":" in name else effective_default_local()
            url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
            to = httpx.Timeout(connect=3.0, read=25.0, write=3.0, pool=3.0)
            async with httpx.AsyncClient(timeout=to) as client:
                r = await client.post(url, json={"model": model, "prompt": prompt, "stream": False})
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

    def _immune_threat(self) -> str:
        """Current immune threat level — the living organism's self-protection signal."""
        try:
            from agentic_core.organism.immune import immune
            return immune.status().get("threat_level", "NOMINAL")
        except Exception:
            return "NOMINAL"

    # §6↔§7 "the fabric is the bus": the swarm can autonomously SELECT fabric resources for
    # decomposed goals — restricted to LIGHT, BOUNDED, side-effect-free handlers (readings, checks,
    # single completions). Cognition-heavy engines (the staged PI pipelines, cascades) stay
    # human-composed — the tree must not silently multiply its own cost.
    _TREE_FABRIC_ALLOWED = (
        "compliance", "products_catalogue", "capital_fund", "resource_optimizer",
        "federation_mesh", "omnimedia", "immune", "self_healing", "metabolic",
        "circadian", "genome", "digital_twin",
    )

    def _match_fabric_resource(self, text: str) -> Optional[tuple]:
        """Deterministic capability match: score each ALLOWED fabric resource by how many of its
        registry capability/name words (≥5 chars) appear in the node's task text. ≥2 hits → a match
        (returns (resource_id, hits)); below → None. No AI, no guessing — the match reason is the
        word overlap itself."""
        import re as _re
        try:
            from agentic_core.api.resource_fabric import _BY_ID
        except Exception:
            return None
        low = f" {(text or '').lower()} "
        best_hits, best_rid = 0, None
        for rid in self._TREE_FABRIC_ALLOWED:
            r = _BY_ID.get(rid)
            if not r:
                continue
            words = set()
            for cap in (r.get("capabilities") or []):
                words.update(_re.findall(r"[a-z]{5,}", str(cap).lower()))
            words.update(_re.findall(r"[a-z]{5,}", str(r.get("name", "")).lower()))
            hits = sum(1 for w in words if w in low)
            if hits > best_hits:
                best_hits, best_rid = hits, rid
        return (best_rid, best_hits) if best_rid and best_hits >= 2 else None

    def _plan_tree(self, goal: str) -> List[Dict[str, Any]]:
        """Autonomously decompose a goal into a workflow TREE (DAG): a framing node, several
        investigation branches that run in PARALLEL (adapted to the goal's content), a synthesis that
        depends on all branches, and a critical review. Honest: a principled analytical decomposition —
        real dependency structure + real per-node in-house reasoning; the branch set adapts to the goal."""
        g = (goal or "").lower()
        nodes: List[Dict[str, Any]] = [
            {"id": "frame", "role": "framing analyst", "depends_on": [],
             "task": f"Frame the goal precisely: scope, success criteria, and the key questions to resolve. Goal: {goal}"},
        ]
        branches: List[tuple] = [
            ("research", "research analyst", "Gather the key facts, prior art, and constraints relevant to the goal."),
            ("design", "solution designer", "Design the approach and the main options to achieve the goal."),
        ]
        if any(k in g for k in ("build", "implement", "deliver", "ship", "develop", "create", "launch", "make")):
            branches.append(("implementation", "delivery planner", "Produce a concrete, sequenced implementation plan with milestones."))
        if any(k in g for k in ("risk", "complian", "legal", "safe", "secur", "govern", "ethic", "halal", "assur")):
            branches.append(("risk", "risk & assurance", "Identify risks, compliance/assurance needs, and concrete mitigations."))
        if any(k in g for k in ("cost", "budget", "econom", "price", "fund", "invest", "revenue", "profit")):
            branches.append(("economics", "economics analyst", "Assess costs, value, and economic viability."))
        for bid, role, task in branches:
            nodes.append({"id": bid, "role": role, "depends_on": ["frame"], "task": task})
        nodes.append({"id": "synthesise", "role": "chief synthesiser", "depends_on": [b[0] for b in branches],
                      "task": "Synthesise the branch outputs into one coherent recommendation/plan for the goal."})
        nodes.append({"id": "review", "role": "critical reviewer", "depends_on": ["synthesise"],
                      "task": "Critically review the synthesis: gaps, risks, and a clear go/no-go with next actions."})
        return nodes

    async def orchestrate_tree(self, goal: str, context: str = "", max_parallel: int = 4,
                               prefer_external: bool = False, timeout: float = 30.0) -> Dict[str, Any]:
        """Plan + run an autonomous workflow TREE for a goal — the living-organism cascade: the goal is
        decomposed into a dependency tree, executed IN-HOUSE-FIRST per node with PARALLEL branches,
        biomimetically mediated (immune-throttled parallelism + biobus nervous signals + the learning
        loop via complete()). Every node reports which OWNED resource served it; never fabricated."""
        nodes = self._plan_tree(goal)
        by_id = {n["id"]: n for n in nodes}
        threat = self._immune_threat()
        # BIOMIMETIC HOMEOSTASIS (§8 → §6): admit cognitive work as a function of the WHOLE living-organism
        # state — immune threat + circadian cycle + metabolic ATP + composite health — not immune alone; and
        # FEED the cognitive demand back into metabolic load (heavier swarms expend more ATP). Fail-open.
        homeo = homeostasis.assess(demand_nodes=len(nodes), requested_parallel=max_parallel)
        max_parallel = max(1, int(homeo["max_parallel"]))
        _fire("cognitive", "native.tree", f"plan {len(nodes)} nodes ({homeo['posture']}): {goal[:48]}", 0.6)

        results: Dict[str, Dict[str, Any]] = {}
        fabric_drawn: set = set()   # each fabric resource is drawn ONCE per run (downstream nodes
                                    # inherit its genuine result through the dependency context)

        async def run_node(nid: str) -> tuple:
            n = by_id[nid]
            dep_ctx = "\n\n".join(f"[{d}] {results[d]['output'][:600]}" for d in n["depends_on"] if d in results)
            prompt = (
                f"You are the '{n['role']}' agent in Workstation's native swarm, executing node '{nid}' "
                f"of an autonomously-planned workflow tree.\n"
                f"{('Overall context:\\n' + context[:600] + '\\n\\n') if context else ''}"
                f"Overall goal: {goal}\n"
                f"{('Inputs from upstream nodes:\\n' + dep_ctx + '\\n\\n') if dep_ctx else ''}"
                f"Your task: {n['task']}\n\n## {nid} output"
            )
            res = await self.complete(prompt, agent=f"tree:{nid}", timeout=timeout, prefer_external=prefer_external)
            # §6↔§7 — when a fabric resource genuinely matches this node's task, ALSO run its REAL
            # handler and fold the genuine result into the node (honest provenance: resource id +
            # endpoint + the word-overlap score). Fail-soft: a fabric error never breaks the node.
            match = self._match_fabric_resource(f"{n['task']} {goal}")
            if match and match[0] not in fabric_drawn:
                rid, hits = match
                fabric_drawn.add(rid)
                try:
                    from agentic_core.api.resource_fabric import _run_real_resource
                    fr = await _run_real_resource(rid, {}, goal, "general")
                    if fr and not fr.get("error"):
                        res["fabric"] = {"resource": rid, "ran": fr.get("ran"), "match_hits": hits}
                        res["output"] = (res.get("output", "") +
                                         f"\n\n[fabric:{rid} · ran {fr.get('ran')}] " +
                                         str(fr.get("output", ""))[:400])
                        _fire("motor", "native.tree", f"node {nid} drew fabric resource {rid}", 0.5)
                except Exception:
                    pass
            return nid, res

        levels: List[List[str]] = []
        done: set = set()
        any_external = False
        while len(done) < len(nodes):
            ready = [n["id"] for n in nodes if n["id"] not in done and all(d in done for d in n["depends_on"])]
            if not ready:
                break  # dependency-cycle guard (the planner never produces one)
            levels.append(ready)
            for i in range(0, len(ready), max_parallel):       # bounded parallelism within the level
                chunk = ready[i:i + max_parallel]
                for nid, res in await asyncio.gather(*[run_node(x) for x in chunk]):
                    results[nid] = res
                    any_external = any_external or bool(res.get("is_external"))
                    done.add(nid)
                    _fire("motor", "native.tree", f"node {nid} served by {res['served_by']}", 0.4)

        final = (results.get("review") or results.get("synthesise") or {}).get("output", "")
        order = [n["id"] for n in nodes]

        # VBS GOVERNANCE (in-house integration): the OWNED VBS Quality + Document-Control systems govern
        # the in-house AI's output — a real ISO-aligned quality gate on the synthesis + a real SHA3-512
        # versioned commit to the document-control ledger. Best-effort: never breaks the orchestration.
        governance: Dict[str, Any] = None
        try:
            from agentic_core.vbs.registry import qms, dcms
            coverage_proxy = min(1.0, len(final.strip()) / 600.0)   # substantive synthesis ≈ "covered"
            qms_passed = await qms.run_quality_gates({"coverage": coverage_proxy, "stubs_found": not final.strip()})
            dcms_hash = await dcms.commit_artifact(f"tree:{(goal or '')[:48]}",
                                                   {"goal": goal, "final": final[:2000], "nodes": len(nodes)}, "native.tree")
            governance = {"governed_by": "VBS QMS + DCMS (owned, real)", "qms_passed": bool(qms_passed),
                          "qms_coverage_proxy": round(coverage_proxy, 3),
                          "dcms_hash": dcms_hash, "dcms_algo": "sha3_512",
                          "dcms_version": len(dcms.registry.get(f"tree:{(goal or '')[:48]}", []))}
            _fire("reflex", "native.tree", f"VBS governance: qms={'pass' if qms_passed else 'fail'}", 0.4)
        except Exception:
            governance = None

        # VALIDATION (owned): a REAL difflib check — did the synthesis genuinely INTEGRATE the branches,
        # or just near-copy one? (difflib SequenceMatcher excels at near-duplication detection.) High
        # overlap with a single branch ⇒ not a real synthesis; moderate/low ⇒ genuine integration.
        validation: Dict[str, Any] = None
        try:
            from agentic_core.validation.accuracy_validator import AccuracyValidator
            av = AccuracyValidator(target_accuracy=0.85)
            overlaps = []
            for n in nodes:
                if n["depends_on"] == ["frame"] and n["id"] in results:
                    bo = results[n["id"]]["output"]
                    if bo.strip() and final.strip():
                        overlaps.append(float(av.validate_output(final, bo, task_type="SEMANTIC")["confidence"]))
            if overlaps:
                max_ov = max(overlaps)
                validation = {"max_branch_overlap": round(max_ov, 3), "integrated": bool(max_ov < 0.85),
                              "branches_checked": len(overlaps),
                              "method": "difflib SequenceMatcher (owned validation)"}
        except Exception:
            validation = None

        # MINIMAX DECISION (owned cognition): a REAL maximin decision over {proceed · refine · hold} under
        # worst-case stressors, grounded in the run's ACTUAL signals (QMS gate, immune threat, in-house,
        # coverage). The in-house AI uses an owned decision algorithm — not LLM text — to recommend.
        decision: Dict[str, Any] = None
        try:
            from agentic_core.cognition.minimax_optimizer import MinimaxOptimizer
            qms_ok = bool(governance and governance.get("qms_passed"))
            cov = float((governance or {}).get("qms_coverage_proxy", 0.5))
            st = {"qms_passed": qms_ok, "immune": threat, "in_house": (not any_external), "coverage": cov}

            def _util(state: Dict[str, Any], action: str, stressor: str) -> float:
                base = {"proceed": 0.92, "refine": 0.84, "hold": 0.78}.get(action, 0.70)
                if not state["qms_passed"]:
                    base -= 0.15 if action == "proceed" else 0.05
                if state["immune"] != "NOMINAL":
                    base -= 0.12 if action == "proceed" else 0.04
                if not state["in_house"]:
                    base -= 0.05
                base += (state["coverage"] - 0.5) * 0.10
                sens = {"proceed": 0.30, "refine": 0.18, "hold": 0.10}.get(action, 0.20)
                smag = {"hypoxia": 1.0, "oxidative_burst": 0.8, "high_load": 0.6, "thermal_stress": 0.5}.get(stressor, 0.5)
                return max(0.0, base - sens * smag * 0.4)

            mm = MinimaxOptimizer(threshold=0.8)
            res = mm.evaluate_strategy(st, ["proceed", "refine", "hold"], _util)
            decision = {"recommendation": res["selected_action"], "consistency": round(float(res["consistency_score"]), 3),
                        "worst_case_utility": round(float(res["worst_case_utility"]), 3),
                        "method": "minimax adversarial (owned cognition)",
                        "stressors": ["hypoxia", "oxidative_burst", "high_load", "thermal_stress"]}
            _fire("cognitive", "native.tree", f"minimax decision: {res['selected_action']}", 0.5)
        except Exception:
            decision = None

        # SWARM CONSENSUS (owned): the tree's INDEPENDENT owned checks VOTE — do they agree? Real
        # threshold consensus (agentic_core/swarm.ConsensusEngine) over the QMS · validation · minimax ·
        # immune signals. Consensus "proceed" ⇒ the independent governance/decision layers concur.
        consensus: Dict[str, Any] = None
        try:
            from agentic_core.swarm.conflict_resolution import ConsensusEngine
            voters = {
                "qms": "proceed" if (governance or {}).get("qms_passed") else "caution",
                "validation": "proceed" if (validation or {}).get("integrated") else "caution",
                "minimax": "proceed" if (decision or {}).get("recommendation") == "proceed" else "caution",
                "immune": "proceed" if threat == "NOMINAL" else "caution",
            }
            ce = ConsensusEngine(threshold=0.66)
            for voter, choice in voters.items():
                ce.record_vote("tree", voter, choice)
            agreed = ce.check_consensus("tree", len(voters))
            proceed_votes = sum(1 for c in voters.values() if c == "proceed")
            consensus = {"reached": agreed is not None, "choice": agreed, "threshold": ce.threshold,
                         "votes": voters, "proceed_fraction": round(proceed_votes / len(voters), 3),
                         "method": "threshold consensus (owned swarm)"}
            _fire("cognitive", "native.tree", f"swarm consensus: {agreed or 'none'}", 0.4)
        except Exception:
            consensus = None

        # BIOMIMETIC SIGNAL TRANSDUCTION (owned): model whether the run's signal is strong enough to
        # PROPAGATE through the organism's biochemical cascade — a REAL Hill-equation (sigmoidal)
        # response to the run's consensus strength. peak >= 0.5 ⇒ supra-threshold (the signal fires).
        signal_response: Dict[str, Any] = None
        try:
            from agentic_core.signaling.empirical_transduction import EmpiricalSignalTransduction
            strength = float((consensus or {}).get("proceed_fraction", 0.5))
            casc = EmpiricalSignalTransduction(frequency=0.5, hill=4.5).simulate_cascade(strength)
            peak = float(casc["peak_intensity"])
            signal_response = {"input_strength": round(strength, 3), "peak_intensity": round(peak, 4),
                               "latency_s": round(float(casc["latency"]), 2), "propagated": bool(peak >= 0.5),
                               "hill": 4.5, "method": "Hill-equation cascade (owned signaling)"}
            _fire("sensory", "native.tree", f"signal transduction peak={peak:.2f}", 0.4)
        except Exception:
            signal_response = None

        # UEG PROVENANCE (owned ledger): record this run to the real hash-chained SHA3-512 Merkle-DAG
        # audit ledger — the in-house AI's actions get verifiable, tamper-evident provenance. Best-effort.
        ueg_hash = None
        try:
            from agentic_core.ueg.registry import ueg_ledger
            ueg_hash = await ueg_ledger.log_event("native.tree.run", {
                "goal": (goal or "")[:200],
                "node_count": len(nodes),
                "parallel_levels": sum(1 for lv in levels if len(lv) > 1),
                "immune_threat": threat,
                "any_external": any_external,
                "qms_passed": (governance or {}).get("qms_passed"),
                "decision": (decision or {}).get("recommendation"),
            }, actor="native.tree")
        except Exception:
            ueg_hash = None

        return {
            "goal": goal,
            "posture": "in-house-first",
            "tree": [{"id": n["id"], "role": n["role"], "depends_on": n["depends_on"]} for n in nodes],
            "levels": levels,
            "node_count": len(nodes),
            "parallel_levels": sum(1 for lv in levels if len(lv) > 1),
            "max_parallel": max_parallel,
            "immune_threat": threat,
            "homeostasis": homeo,   # §8→§6: how the living organism modulated this cognition (+ ATP expended)
            "governance": governance,
            "validation": validation,
            "decision": decision,
            "consensus": consensus,
            "signal_response": signal_response,
            "ueg_hash": ueg_hash,
            "ueg_ledger": "hash-chained SHA3-512 Merkle-DAG (owned, verifiable)" if ueg_hash else None,
            "fabric_resources_drawn": sorted({(results[nid].get("fabric") or {}).get("resource")
                                              for nid in order if nid in results and results[nid].get("fabric")}
                                             - {None}),
            "nodes": [{"id": nid, "role": by_id[nid]["role"], "depends_on": by_id[nid]["depends_on"],
                       "served_by": results[nid]["served_by"], "is_external": results[nid]["is_external"],
                       "fabric": results[nid].get("fabric"),
                       "output": results[nid]["output"]} for nid in order if nid in results],
            "final": final,
            "any_external": any_external,
        }

    async def swarm(self, agent: str, stages: List[Dict[str, str]],
                    context: str = "", prefer_external: bool = False,
                    timeout: float = 30.0) -> Dict[str, Any]:
        """Run a bespoke agent-cascade tree: each stage = {role, instruction}. Each stage is
        completed in-house-first and feeds the next — a reconfigurable, reusable swarm resource.
        `timeout` bounds each stage's model attempt (a slow local model falls to the native floor)."""
        trace: List[Dict[str, Any]] = []
        carry = context
        external_used = False
        # §8→§6: a bespoke swarm cascade is cognitive work too — register its demand with the homeostatic
        # controller so it EXPENDS metabolic ATP (the cascade runs sequentially, so concurrency isn't capped,
        # but the metabolic loop + posture still apply). Best-effort; never blocks the cascade.
        homeo = homeostasis.assess(demand_nodes=len(stages), requested_parallel=1)
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
                "final": carry, "any_external": external_used, "homeostasis": homeo}


orchestrator = NativeOrchestrator()
