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
honours that contract: it returns each requested section, populated with a concise,
deterministic synthesis grounded in the prompt's own content (problem, domain, key terms),
plus a clear provenance marker.
"""
from __future__ import annotations

import re
from typing import List

_MARKER = "_[Workstation native structured engine — owned, no external dependency]_"

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "with", "is", "are",
    "be", "as", "that", "this", "you", "your", "i", "we", "it", "by", "from", "at",
    "will", "should", "must", "can", "given", "below", "above", "using", "use", "define",
    "produce", "design", "assess", "honestly", "context", "user",
}


def _sections(prompt: str) -> List[str]:
    """Pull the requested output sections (lines that begin with markdown ## headers)."""
    out: List[str] = []
    for line in prompt.splitlines():
        m = re.match(r"^\s*#{2,4}\s*(.+?)\s*$", line)
        if m:
            title = m.group(1).strip()
            # strip trailing parentheticals/colons but keep the gist
            title = re.sub(r"\s*\(.*?\)\s*$", "", title).strip().rstrip(":")
            if title and title.lower() not in {s.lower() for s in out}:
                out.append(title)
    return out[:14]


def _keywords(prompt: str, n: int = 10) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", prompt.lower())
    freq: dict[str, int] = {}
    for w in words:
        if w in _STOPWORDS:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:n]]


def _subject(prompt: str) -> str:
    """Best-effort one-line subject: the text after the last 'User:'/'Problem:' marker, else the longest sentence."""
    for marker in ("User:", "Problem:", "Challenge:", "Objective:", "Overall realisation:"):
        idx = prompt.rfind(marker)
        if idx != -1:
            tail = prompt[idx + len(marker):].strip().splitlines()[0].strip()
            if len(tail) > 8:
                return tail[:200]
    sentences = re.split(r"(?<=[.!?])\s+", prompt.strip())
    longest = max(sentences, key=len) if sentences else prompt[:200]
    return longest.strip()[:200]


class NativeReasoningEngine:
    """The platform's own, always-available structured reasoning resource."""

    name = "native"
    is_external = False
    is_model = False  # honest: this is structured reasoning, not an LLM

    def generate(self, prompt: str, agent: str = "native") -> str:
        subject = _subject(prompt)
        kws = _keywords(prompt)
        sections = _sections(prompt)

        if sections:
            blocks = [f"## {title}\n{self._section_body(title, subject, kws)}" for title in sections]
            body = "\n\n".join(blocks)
        else:
            body = (
                f"## Understanding\nThe request concerns: {subject}\n\n"
                f"## Key factors\n{self._bullets(kws)}\n\n"
                f"## Native approach\nWorkstation composes a structured response from its own "
                f"process-intelligence and knowledge for the agent '{agent}', grounded in the input.\n\n"
                f"## Next steps\n- Refine with a model resource if higher-fidelity prose is required "
                f"(local model, or an external accelerant when explicitly enabled)."
            )
        return f"{_MARKER}\n\n{body}"

    # ── helpers ────────────────────────────────────────────────────────────────
    def _section_body(self, title: str, subject: str, kws: List[str]) -> str:
        t = title.lower()
        if any(k in t for k in ("gap", "risk", "failure", "weakness")):
            return ("Structurally-derived considerations for this dimension, grounded in the input "
                    f"({', '.join(kws[:5]) or 'the stated context'}). To be enriched by a model resource "
                    "when available; the native engine flags areas needing attention rather than inventing prose.")
        if any(k in t for k in ("next", "step", "recommend", "action", "plan")):
            return ("- Validate the structured outputs above against the stated objective.\n"
                    "- Route richer generation to a model resource (local-first; external only if enabled).\n"
                    "- Iterate via the orchestrator's cascade and record outcomes to memory/UEG.")
        if any(k in t for k in ("summary", "assessment", "faithful", "understanding", "concept", "boundary")):
            return (f"Subject: {subject}. Native structured synthesis grounded in the input's key terms "
                    f"({', '.join(kws[:6]) or 'n/a'}).")
        return (f"Native structured content for '{title}', grounded in: {subject}. "
                f"Key terms: {', '.join(kws[:6]) or 'n/a'}.")

    def _bullets(self, kws: List[str]) -> str:
        return "\n".join(f"- {k}" for k in kws[:6]) or "- (no salient terms extracted)"


native_engine = NativeReasoningEngine()
