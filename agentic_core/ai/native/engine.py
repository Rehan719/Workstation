"""
Native Reasoning Engine — Workstation's own, always-available, owned structured engine.

This is the FLOOR of the native AI fabric: a deterministic, in-house capability that
produces a real, structured deliverable from a prompt WITHOUT any external dependency.
It is the platform's own structured reasoning — explicitly NOT a large-language model,
and never presented as one. Its job is to guarantee that every AI-mediated workflow
produces a usable, honestly-labelled native result even with no model/key present; when
a local or external model IS available the orchestrator uses that instead for richer prose.

Most Workstation prompts are section-templated (they ask for "## Section" headers — the
process-intelligence engines, Genesis, Forge, the orchestration, etc.). The native engine
honours that contract: it returns each requested section populated with a USEFUL structured
scaffold tailored to that section's archetype (architecture, commercial, research, risk,
plan, timeline, KPI, …), grounded in the prompt's own content (subject, domain, role, key
terms and phrases). It never invents facts — it frames the problem and flags what a model
resource should enrich — and always carries a clear provenance marker.
"""
from __future__ import annotations

import re
from typing import List

_MARKER = "_[Workstation native structured engine — owned, no external dependency]_"

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "with", "is", "are",
    "be", "as", "that", "this", "you", "your", "i", "we", "it", "by", "from", "at",
    "will", "should", "must", "can", "given", "below", "above", "using", "use", "define",
    "produce", "design", "assess", "honestly", "context", "user", "output", "prior",
    "objective", "domain", "problem", "challenge", "concept", "agent", "native", "stage",
}


def _sections(prompt: str) -> List[str]:
    """Pull the requested output sections (lines that begin with markdown ## headers)."""
    out: List[str] = []
    for line in prompt.splitlines():
        m = re.match(r"^\s*#{2,4}\s*(.+?)\s*$", line)
        if m:
            title = m.group(1).strip()
            title = re.sub(r"\s*\(.*?\)\s*$", "", title).strip().rstrip(":")
            if title and title.lower() not in {s.lower() for s in out}:
                out.append(title)
    return out[:14]


def _keywords(prompt: str, n: int = 12) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", prompt.lower())
    freq: dict[str, int] = {}
    for w in words:
        if w in _STOPWORDS:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:n]]


def _phrases(prompt: str, n: int = 6) -> List[str]:
    """Salient two-word terms (adjacent non-stopwords) — richer grounding than single keywords."""
    words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", prompt.lower())
    grams: dict[str, int] = {}
    prev = None
    for w in words:
        if w in _STOPWORDS or len(w) < 3:
            prev = None
            continue
        if prev:
            g = f"{prev} {w}"
            grams[g] = grams.get(g, 0) + 1
        prev = w
    ranked = sorted(grams.items(), key=lambda kv: (kv[1], len(kv[0])), reverse=True)
    seen: set[str] = set()
    out: List[str] = []
    for g, _ in ranked:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return out[:n]


def _field(prompt: str, *labels: str) -> str:
    """Extract the value after a 'Label:' marker (first match wins), one line, trimmed."""
    for lab in labels:
        m = re.search(rf"{re.escape(lab)}\s*[:\-]\s*(.+)", prompt)
        if m:
            return m.group(1).strip().splitlines()[0].strip()[:140]
    return ""


def _role(prompt: str) -> str:
    """The persona the prompt assigns ('You are the X' / 'As a X')."""
    m = re.search(r"(?:You are|As)\s+(?:the|a|an)\s+([A-Za-z][A-Za-z0-9 &/\-]{2,60})", prompt)
    return m.group(1).strip().rstrip(".") if m else ""


def _subject(prompt: str) -> str:
    """Best-effort one-line subject from a labelled field, else the longest sentence."""
    field = _field(prompt, "User", "Problem", "Challenge", "Objective", "Concept", "Topic")
    if len(field) > 8:
        return field[:220]
    sentences = re.split(r"(?<=[.!?])\s+", prompt.strip())
    longest = max(sentences, key=len) if sentences else prompt[:220]
    return longest.strip()[:220]


_CONTENT_LABELS = ("User", "Problem", "Challenge", "Objective", "Concept", "Design",
                   "Topic", "Brief", "Mission", "Vision", "Commercialisation", "Prior context")


def _content(prompt: str) -> str:
    """The substantive content of the prompt (values of its content fields), so term/phrase
    extraction grounds on the actual subject rather than the instruction/section scaffolding."""
    vals = [v for lab in _CONTENT_LABELS if (v := _field(prompt, lab))]
    return " . ".join(vals) if vals else prompt


class NativeReasoningEngine:
    """The platform's own, always-available structured reasoning resource."""

    name = "native"
    is_external = False
    is_model = False  # honest: this is structured reasoning, not an LLM

    def generate(self, prompt: str, agent: str = "native") -> str:
        subject = _subject(prompt)
        domain = _field(prompt, "Domain") or "the stated domain"
        role = _role(prompt)
        content = _content(prompt)
        kws = _keywords(content)
        phrases = _phrases(content)
        terms = phrases + [k for k in kws if k not in " ".join(phrases)]  # phrases first, then singles
        sections = _sections(prompt)

        lead = ""
        if role:
            lead = f"_Acting as: {role}._\n\n"

        if sections:
            blocks = [f"## {title}\n{self._section_body(title, subject, domain, terms)}" for title in sections]
            body = lead + "\n\n".join(blocks)
        else:
            body = (
                f"{lead}## Understanding\nThe request concerns: {subject} (domain: {domain}).\n\n"
                f"## Key factors\n{self._bullets(terms, 6)}\n\n"
                f"## Native approach\nWorkstation composes a structured response from its own "
                f"process-intelligence and knowledge for the agent '{agent}', grounded in the input above.\n\n"
                f"## Next steps\n{self._plan(domain)}"
            )
        return f"{_MARKER}\n\n{body}"

    # ── per-archetype structured scaffolds (useful, grounded, never fabricated) ──
    def _section_body(self, title: str, subject: str, domain: str, terms: List[str]) -> str:
        t = title.lower()

        def has(*ks: str) -> bool:
            return any(k in t for k in ks)

        if has("risk", "gap", "failure", "weakness", "threat", "limitation"):
            return ("Structured risk frame for this dimension — surface, don't invent:\n"
                    + self._dims(terms, "Exposure on") +
                    "\n- Likelihood × impact to be scored; mitigations and owners to be assigned.\n"
                    "- The native engine flags areas needing attention; a model resource details them.")
        if has("architecture", "component", "system", "technical", "build", "mvp", "stack", "blueprint"):
            return (f"Structured architecture frame for: {subject}.\n"
                    f"- Core capability: address {terms[0] if terms else 'the primary need'}.\n"
                    + self._dims(terms[:4], "Component for") +
                    "\n- Interfaces & data: specify inputs/outputs and contracts.\n"
                    f"- Non-functionals: reliability, security, and constitutional governance (gaas.v5), fit for {domain}.")
        if has("revenue", "pricing", "monetis", "monetiz", "unit econ"):
            return (f"Structured revenue frame for: {subject}.\n"
                    "- Units: what is charged for, and the pricing model.\n"
                    "- Unit economics: cost-to-serve vs price; contribution margin (to be quantified).\n"
                    + self._dims(terms[:3], "Stream from") +
                    "\n- Sensitivity: the key drivers to stress-test.")
        if has("market", "value", "business model", "go-to-market", "gtm",
               "commercial", "demand", "customer", "segment"):
            return (f"Structured go-to-market frame for: {subject}.\n"
                    "- Segment & need: who is served and the job-to-be-done.\n"
                    + self._dims(terms[:3], "Positioning wedge from") +
                    "\n- Channels: how the segment is reached (CAC to be measured).\n"
                    "- Moat: the durable advantage that compounds.")
        if has("method", "finding", "evidence", "hypothesis", "research", "literature", "experiment", "viability"):
            return (f"Structured research frame for: {subject}.\n"
                    "- Question/hypothesis: state it falsifiably.\n"
                    + self._dims(terms[:4], "Variable") +
                    "\n- Method: how evidence is gathered; controls and validity threats.\n"
                    "- Findings/verdict: to be populated from real evidence — the native engine sets the rigour, not the claims.")
        if has("timeline", "days", "roadmap", "phase", "milestone", "delivery plan"):
            return ("Structured phased frame (deterministic scaffold):\n"
                    "- Phase 1 — validate: cheapest test of the riskiest assumption.\n"
                    "- Phase 2 — build: the smallest end-to-end slice that delivers value.\n"
                    "- Phase 3 — launch & learn: ship, instrument, iterate.\n"
                    f"- Each phase grounded in {domain}; dates to be set against capacity.")
        if has("kpi", "metric", "measure", "success", "what success looks like"):
            return ("Structured measurement frame:\n"
                    + self._dims(terms[:4], "Candidate KPI from") +
                    "\n- Each KPI needs a baseline, target, and cadence; tie to the objective above.")
        if has("variant", "evaluation", "ranking", "recommended"):
            return (f"Structured option frame for: {subject}.\n"
                    "- Generate ≥3 distinct variants of the approach.\n"
                    "- Score each against value, feasibility, risk, and values-fit (halal/beneficence).\n"
                    "- Recommend the highest-scoring; record why — to be enriched by a model resource.")
        if has("next", "step", "action", "plan", "recommend", "directive", "framing", "first 90"):
            return self._plan(domain)
        if has("summary", "assessment", "faithful", "understanding", "concept", "boundary",
               "synthesis", "deliverable", "integrated"):
            return (f"Subject: {subject} (domain: {domain}).\n"
                    f"Native structured synthesis grounded in the input's salient terms:\n{self._bullets(terms, 6)}")
        # generic, still grounded
        return (f"Native structured content for '{title}', grounded in: {subject} (domain: {domain}).\n"
                f"{self._bullets(terms, 5)}")

    # ── small builders ───────────────────────────────────────────────────────────
    def _dims(self, terms: List[str], prefix: str) -> str:
        picks = terms[:4] or ["the stated context"]
        return "\n".join(f"- {prefix} {p}." for p in picks)

    def _bullets(self, terms: List[str], n: int) -> str:
        return "\n".join(f"- {k}" for k in terms[:n]) or "- (no salient terms extracted)"

    def _plan(self, domain: str) -> str:
        return ("- Validate the structured outputs above against the stated objective.\n"
                "- Route richer generation to a model resource (local-first; external only if enabled).\n"
                f"- Iterate via the orchestrator's cascade for {domain}; record outcomes to memory/UEG.")


native_engine = NativeReasoningEngine()
