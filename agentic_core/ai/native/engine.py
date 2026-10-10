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
from typing import List, Optional

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


# W505 (P2.1) — CARRIED CONTEXT IS NOT THE SUBJECT. A stage's output becomes the next stage's input, so
# this engine's own framing came back as the thing it was asked about: a live cascade produced
# "Structured go-to-market frame for: Your officer's plan: _[Workstation native structured engine — owned,
# no external dependency]_ · _Acting as: Chief Legal Officer._ · ## Intent & Values …" at level 3. Three
# shapes do it, and all three are emitted by this platform's own code (the marker below; the `lead` line in
# generate(); and orchestrator.py:565/854, which append "## {role} output" to a carried task):
#  W637 (FU-593) — UNANCHORED. This required the marker to fill a line of its own, so a caller that carried
#  a previous stage's output without a real newline in front of it (orchestrator.swarm did, for many rounds)
#  left the banner in place and its words were counted as the user's. The marker is this engine's own
#  literal and appears in no user's request, so removing it anywhere costs nothing and closes the class.
_CARRIED_MARKER_RE = re.compile(re.escape(_MARKER))
#  W650 (FU-626, ledger v14 R1) - THE ROLE LINE SAYS WHAT IT IS. The floor opened its output "_Acting as: <role>._".
#  On the Religion tools that printed "Acting as: Islamic scholar and Quranic exegete" above a frame no scholar
#  wrote. The floor takes no role: it echoes the role the PROMPT asked for. The opening words live here, once,
#  and every stripper imports them - the old wording stays in ROLE_LEAD_OPENINGS because stored journeys,
#  plans and pages written before this round still carry it, and a stripper that forgot it would publish them.
ROLE_LEAD_OPEN = "_Role the prompt asked for:"
ROLE_LEAD_OPENINGS = (ROLE_LEAD_OPEN, "_Acting as:")
_CARRIED_ACTING_RE = re.compile(
    r"^[ \t]*(?:" + "|".join(re.escape(o) for o in ROLE_LEAD_OPENINGS) + r").*?_[ \t]*$", re.M)
# a "<role> output" header, not any header ending in the word output: a role name then the bare word
_CARRIED_ROLE_OUTPUT_RE = re.compile(r"^[ \t]*##[ \t]+[A-Za-z][A-Za-z0-9 &/\-]{1,60}[ \t]+output[ \t]*$",
                                     re.M | re.I)


def _strip_carried(prompt: str) -> str:
    """Remove this engine's OWN framing from a prompt before anything is read out of it.

    Applied once, to the whole prompt, before `_subject`/`_keywords`/`_role`/`_content`/`_phrases`/
    `_sections` — one point rather than six, so a new extractor cannot forget it. It removes only shapes
    this platform emits; a user who writes "## Design output" in their own brief loses that header, which
    is the accepted cost of not letting a previous stage's header choose this stage's sections."""
    out = _CARRIED_MARKER_RE.sub("", prompt)
    out = _CARRIED_ACTING_RE.sub("", out)
    out = _CARRIED_ROLE_OUTPUT_RE.sub("", out)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


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


#  W631 (FU-557) - words that mark a request about a PERSON's work (pay, a role, a CV), not a venture's market
_PERSONAL_MARKERS = ("salary", "negotiation coach", "compensation", "career", "curriculum vitae", " cv ",
                     "résumé", "resume", "interview", "job offer", "pay rise", "target role")


def _field(prompt: str, *labels: str) -> str:
    """Extract the value after a 'Label:' marker (first match wins), one line, trimmed.

    W627 (FU-530) - an exact-case label is tried first, as before, so the label order still decides. Only if
    NO label matched exactly is each tried again ignoring case, as a whole word and with a colon only: Studio
    writes 'CHALLENGE:' and the tree writes 'Overall goal:' / 'Your task:', and an exact-case scan dropped all
    three and then told the reader the request had no subject. The hyphen separator stays exact-case so
    'user-friendly' in running text is never read as a 'User' field."""
    for lab in labels:
        m = re.search(rf"{re.escape(lab)}\s*[:\-]\s*(.+)", prompt)
        if m:
            return m.group(1).strip().splitlines()[0].strip()[:140]
    for lab in labels:
        #  [ \t]* not \s*: a value on the NEXT line is a block, not this field ('Prior context:\n<carried
        #  output>' was read as a 'Context' field and the previous stage's headings became the user's terms)
        m = re.search(rf"(?<![A-Za-z]){re.escape(lab)}[ \t]*:[ \t]*(\S.*)", prompt, re.IGNORECASE)
        if m:
            return m.group(1).strip().splitlines()[0].strip()[:140]
    return ""


#  W627 (FU-530) - a prompt that is ONE line and carries no 'Label:' marker at all IS the request: nothing
#  the platform adds (a realm directive, a carried stage, a preamble) arrives on the same line without a label.
_ANY_LABEL = re.compile(r"(?m)^\s*[A-Za-z][\w /&'-]{0,40}:\s")


def _unlabelled_request(prompt: str) -> str:
    text = (prompt or "").strip()
    if not text or "\n" in text or _ANY_LABEL.search(text):
        return ""
    return text[:220]


def _role(prompt: str) -> str:
    """The persona the prompt assigns ('You are the X' / 'As a X')."""
    #  W637 (FU-597) — TO THE END OF THE SENTENCE, TRIMMED AT A WORD. The class excluded the comma and the
    #  limit was a character count, so "an experienced, fair teacher and examiner" printed as "experienced"
    #  and a 68-character persona printed with its last word cut in half. The first character is still a
    #  letter, so a quoted swarm role yields nothing, as before.
    m = re.search(r"(?:You are|As)[ \t]+(?:the|a|an)[ \t]+([A-Za-z][^.:\n]{2,160})", prompt)
    if not m:
        return ""
    role = m.group(1).strip()
    if len(role) > 110:
        role = role[:110].rsplit(" ", 1)[0]
    return role.rstrip(" ,;-")


#  W593 (P2.20 a.i) — the labels that may become a SUBJECT, as a constant beside `_CONTENT_LABELS` so the
#  relationship between the two is readable without parsing a function body. THE INVARIANT: every label here
#  must also be in `_CONTENT_LABELS`. Not the reverse — a body field (Background, Prior context, Current
#  draft) is substantive without being a topic, and a 220-character slice of a body is not a subject. The
#  direction that must hold is the one that was broken: bare `Task` was here and not there, so a delegated
#  prompt had a subject and no content and its terms came from the platform's own scaffolding.
_SUBJECT_LABELS = ("User", "Problem", "Challenge", "Objective", "Mission", "Concept", "Topic",
                   "Research question", "Question", "Task / question", "Task", "Hypothesis",
                   "Target role", "Current situation", "Concern", "Subject", "Search query",
                   "Brief", "Design", "Vision", "Commercialisation", "Product", "Scope", "Description",
                   #  W627 (FU-530) - the tree's node prompt names its subject 'Overall goal:' / 'Goal:'
                   "Goal")


def _subject(prompt: str) -> str:
    """Best-effort one-line subject from a labelled field, else the longest sentence.
    §3A (W336) — the label set covers the labels the domain routers ACTUALLY use, so the floor's
    output grounds in the user's own input instead of the prompt scaffolding (the audit found
    Offering-1 floor outputs that never contained the user's input at all)."""
    # W505 (P2.1) — "Task" and "Mission" join the subject labels. "Objective" and "Challenge" were
    # already here; bare "Task" was not, and only "Task / question" was, which cannot match the "Task:"
    # that orchestrator.py:854 emits for every delegated instruction. It is listed AFTER "Task / question"
    # so the more specific label still wins where both could apply.
    #   "Mission" was the MEASURED cause of a live cascade's level 3 still carrying its predecessor's text
    # after the stripping above fixed level 2: swarm.py builds the CoE prompt with the user's subject under
    # `Mission:`, this list did not contain it, so `_subject` fell through to "the longest sentence" and the
    # longest sentence was inside the carried `Your officer's plan: …` blob. Note that `_CONTENT_LABELS`
    # below DOES list "Mission" - the two lists disagreed about whether a mission is substantive, and the
    # content list was the right one.
    #  W593 (P2.20 a.i) — the seven labels that NAME a topic joined this list: Brief, Design, Vision,
    #  Commercialisation, Product, Scope, Description. `_CONTENT_LABELS` already called all of them
    #  substantive, and `Brief` is what a deliverable carries, so without it the fall-through below chose
    #  the subject for every deliverable. The sixteen labels that hold a BODY are deliberately NOT here
    #  (Background, Prior context, Current draft, Refinement instruction, Experience, Clinical context,
    #  Identified care needs, Prior knowledge, Context, Profile, Company, Current role, Care setting,
    #  Ingredients, Candidate experience, Assessment): a 220-character slice of a body is not a subject,
    #  and taking one would replace a false subject with a different false subject. The two lists SHOULD
    #  differ; what must not happen is a prompt that one list reads and the other falls through on.
    #  W637 (FU-594) — THE TREE'S OWN GOAL LINE IS READ FIRST. `Goal` sits last in the label order, so in a
    #  node prompt with upstream inputs the subject was this node's `Your task:` instruction, or any
    #  exact-case label inside a CARRIED upstream output — never the user's goal. `Overall goal:` is written
    #  by the tree alone, ahead of the upstream block, and holds the request itself. A precedence here rather
    #  than a new label: `Goal` already reads this line for the content, and listing it twice would count
    #  the user's words twice in the term list.
    _goal = _field(prompt, "Overall goal")
    if len(_goal) > 8:
        return _goal[:220]
    field = _field(prompt, *_SUBJECT_LABELS)
    if len(field) > 8:
        return field[:220]
    #  W627 (FU-530) - an unlabelled one-line request is its own subject ('Write a mission statement for a
    #  bakery cooperative' was answered "the request carries no labelled subject")
    _whole = _unlabelled_request(prompt)
    if len(_whole) > 8:
        return _whole
    #  NO LABEL MATCHED, SO THERE IS NO SUBJECT TO REPORT. This returned THE LONGEST SENTENCE, and in a
    #  prompt carrying a realm directive the longest sentence IS the directive - which is how a report on a
    #  Kenyan clinic opened "Subject: Lead with the decision and its cost...". A fall-through presented as a
    #  reading is the defect; returning nothing lets the one rendering site say the request named no
    #  subject, which is true and checkable.
    return ""


# §3A (W336) — the census of SUBSTANTIVE labels the domain routers + refine genuinely emit
# (scaffolding labels like 'Structure as'/'Respond with a JSON object' deliberately excluded).
_CONTENT_LABELS = ("User", "Problem", "Challenge", "Objective", "Concept", "Design",
                   "Topic", "Brief", "Mission", "Vision", "Commercialisation", "Prior context",
                   "Research question", "Hypothesis", "Question", "Task / question",
                   "Target role", "Current role", "Current situation", "Concern",
                   "Clinical context", "Background", "Candidate experience", "Company",
                   "Profile", "Experience", "Subject", "Assessment", "Description",
                   "Current draft", "Refinement instruction", "Search query", "Scope",
                   "Product", "Ingredients", "Care setting", "Identified care needs",
                   "Prior knowledge", "Context", "Task", "Goal",
                   #  W593 — THE REALM IS PART OF THE REQUEST. It reached the composition only through
                   #  `_subject`'s fall-through to the longest sentence (the unlabelled realm DIRECTIVE
                   #  line), so removing that fall-through made two realms produce a byte-identical
                   #  blueprint - the defect W434 fixed, reopened by fixing R1.0. Declared here instead,
                   #  and excluded from the term list below because "Enterprise" is the platform's
                   #  vocabulary for a choice, not a word the user wrote.
                   "Realm")

#  W593 (P2.20 a.ii) — labels whose value is NOT what the user wrote in THIS request. `Prior context` holds
#  the PREVIOUS STAGE'S OUTPUT: orchestrator.py is its only emitter and it is always `carry`. A list headed
#  "most frequent in your request" may not be counted over it. Excluded from the TERM source only - the
#  content keeps it, because for composition it genuinely is context.
#  `Realm` is the second kind: the founder chose it, so it is real context for the composition, but
#  "Enterprise" is this platform's label for that choice and not a word the user typed - counting it under
#  "most frequent in your request" would make the heading false in the same way.
_CARRIED_LABELS = ("Prior context", "Realm")


#  W618 (FU-500, M2 v8 R5.1) — FIELDS WHOSE VALUE IS A BLOCK, NOT A LINE. The Law Document Analyser sends
#  "DOCUMENT:\n<the user's document>" and the Care tools "Patient profile:\n  key: value …"; `_field` reads one
#  line after a label and its labels are case-sensitive, so none of these reached the floor, which printed
#  "(no salient terms extracted)" under "Red Flags" over a document it never read. A block runs to the next
#  blank line.
_BLOCK_LABELS = ("DOCUMENT", "Patient profile", "Patient observations/data (as recorded)")


def _block(prompt: str, label: str, limit: int = 3000) -> str:
    m = re.search(rf"(?m)^{re.escape(label)}\s*:[ \t]*\n?(.*?)(?:\n[ \t]*\n|\Z)", prompt, re.S)
    return m.group(1).strip()[:limit] if m else ""


def _content_parts(prompt: str, *, for_terms: bool = False) -> List[str]:
    """The prompt's content-field values, ONE PER FIELD, so nothing is read across a field boundary.

    W593 — `_content` joined these with " . " and `_phrases` then formed bigrams over the join, so the
    user's last word paired with the next field's first: a probe returned "kitchen understanding", the
    user's word joined to this engine's own "## Understanding" heading, under a heading that calls the list
    the user's own terms. Phrases are built per part instead; unigrams cannot span a boundary.

    `for_terms` drops the labels whose value is not the user's own wording - a previous stage's output, and
    the platform's name for a choice the founder made - because a term list about the user's request may not
    be counted over either.
    """
    labels = tuple(lab for lab in _CONTENT_LABELS
                   if not (for_terms and lab in _CARRIED_LABELS))
    return ([v for lab in labels if (v := _field(prompt, lab))]
            + [b for lab in _BLOCK_LABELS if (b := _block(prompt, lab))])


def _content(prompt: str) -> str:
    """The substantive content of the prompt (values of its content fields), so term/phrase
    extraction grounds on the actual subject rather than the instruction/section scaffolding.

    W593 — the fall-through to the whole prompt is KEPT here and removed from the TERM path. This value is
    the composition's context, where falling back to the prompt degrades quality; the term list is a CLAIM
    about the user's request, where falling back makes the claim false.
    """
    vals = _content_parts(prompt)
    return " . ".join(vals) if vals else prompt


#  W640 - said ONCE per reply when the caller did not identify the person's words. It states a fact about the
#  call, never an omission by the person: the old sentence said a request carried no subject when it had one.
_NOT_TOLD = ("This engine was not told which part of its input you wrote, so it states no subject for your "
             "request and attributes nothing to you. That is a limit of the tool that called it, not of what "
             "you asked")
#  ...and what a section frame names in the subject's place, so no frame reads "frame for: ."
_SUBJECT_NOT_TOLD = "the subject (not identified to this engine by the tool that called it)"


class NativeReasoningEngine:
    """The platform's own, always-available structured reasoning resource."""

    name = "native"
    is_external = False
    is_model = False  # honest: this is structured reasoning, not an LLM

    def generate(self, prompt: str, agent: str = "native", user_text: Optional[str] = None) -> str:
        #  W640 (Owner ruling 2026-10-09, late) - THE DEFAULT IS TO WITHHOLD, NOT TO GUESS. This engine cannot
        #  know which part of a prompt a person wrote: a labelled field reaches it the same way whether the
        #  person typed it, a router composed it, or an upstream stage produced it. It used to guess by
        #  scanning for labels, and the guess was fixed one caller at a time (W593, W615, W637) and found
        #  again on the callers nobody had touched (ledger v14). So the CALLER says: `user_text` is the
        #  person's own words, and the subject and the terms are read from it and from nothing else. Without
        #  it this engine attributes nothing to the person - no subject, no terms, no omission - and says once
        #  that it was not told. A caller that passes text the person did not write is the caller's defect,
        #  and a countable one: grep the call.
        _told = isinstance(user_text, str) and bool(user_text.strip())
        # W505 (P2.1) — strip this engine's own framing ONCE, before anything is read out of the prompt.
        # A stage's output is the next stage's input, so without this the marker line, the "_Acting as:"
        # lead and a carried "## <role> output" header became the subject, the keywords and the section
        # list of the stage that followed.
        prompt = _strip_carried(prompt)
        #  W649 (FU-634, ledger v14 R2) - A CUT SUBJECT SAYS IT WAS CUT. The line printed the first characters
        #  of what the person wrote and stopped, with nothing to show the actual ask had been dropped.
        _whole = " ".join(user_text.split()) if _told else ""
        subject = (_whole if len(_whole) <= 220 else
                   _whole[:220].rsplit(" ", 1)[0] + f" … [cut at 220 of {len(_whole)} characters]")
        #  W631 (FU-556) - an unnamed domain is WITHHELD, not filled with a placeholder that reads as a reading.
        #  W640 - and its absence is the CALL's, not the person's: the Domain line is written by a router.
        domain = _field(prompt, "Domain") or "WITHHELD — no domain was declared for this call"
        role = _role(prompt)
        content = _content(prompt)
        #  W593 (P2.20 a.ii) — THE TERMS COME FROM THE USER'S OWN FIELDS, PER FIELD. The carried labels are
        #  dropped (a previous stage's output is not "your request") and phrases are built within each field
        #  so no bigram spans two sources. Unigrams cannot span a boundary, so they stay on the joined text.
        #  one part per LINE of what the person wrote: a caller naming two fields sends two lines, and a
        #  phrase is never built across them (W593's per-field rule, kept)
        _term_parts = [ln.strip() for ln in user_text.splitlines() if ln.strip()] if _told else []
        kws = _keywords(" . ".join(_term_parts)) if _term_parts else []
        phrases = [p for part in _term_parts for p in _phrases(part)]
        terms = phrases + [k for k in kws if k not in " ".join(phrases)]  # phrases first, then singles
        sections = _sections(prompt)

        lead = ""
        if role:
            lead = (f"{ROLE_LEAD_OPEN} {role}. The native floor takes no role - what follows is a frame, "
                    f"not that role's work._\n\n")
        #  W593 — THE REALM IS RECORDED, AND THE LIMIT IS STATED. W434 put the realm into the prompt to
        #  stop it reaching nothing, and the only thing that carried it into the composition was
        #  `_subject`'s fall-through to the longest sentence - the realm DIRECTIVE line - so fixing R1.0
        #  made two realms produce a byte-identical blueprint. The sections branch composes from
        #  subject/domain/terms and never reads the content fields, so no label could fix it there. The
        #  precedent is this engine's own: a floor cannot act on a style directive, and the honest move is
        #  to say so rather than to look as though it did (W434's candidates ruling, W498's withheld
        #  sections). A served model DOES act on the directive, and then this line is still true.
        #  W627 (FU-519) - ATTACHED MATERIAL IS NAMED IN EVERY STAGE. The terms above are counted over all
        #  the labelled fields, and in a later stage the earlier stages' text outnumbers an attached survey,
        #  so 212 households, rainwater and greywater reached no stage after the concept. The document's own
        #  terms are listed under a line that says what they are.
        _doc = _block(prompt, "DOCUMENT")
        if _doc:
            _dt = [p for p in _phrases(_doc)] + [k for k in _keywords(_doc, n=8)]
            _dt = [t for i, t in enumerate(_dt) if t not in _dt[:i]][:10]
            if _dt:
                lead += (f"_Attached material considered — its most frequent terms: {', '.join(_dt)}. This "
                         f"engine lists them; it does not analyse the material._\n\n")
        _realm_named = _field(prompt, "Realm")
        if _realm_named:
            lead += (f"_Composed for the {_realm_named} realm. This engine RECORDS the realm and does not "
                     f"act on it: it composes from the text the calling tool identified as yours, and a house style is a "
                     f"directive only a served model can follow._\n\n")

        if sections:
            _personal = any(w in prompt.lower() for w in _PERSONAL_MARKERS)      # W631 (FU-557)
            blocks = [f"## {title}\n{self._section_body(title, subject or _SUBJECT_NOT_TOLD, domain, terms, personal=_personal)}"
                      for title in sections]
            body = lead + "\n\n".join(blocks)
        else:
            #  W593 (P2.20 a.i) — WHAT THE UNDERSTANDING LINE SAYS WHEN NO LABEL NAMED A SUBJECT. `_subject`
            #  used to return the longest sentence here, and in a prompt carrying a platform directive the
            #  longest sentence IS the directive: a report on a Kenyan clinic opened "Subject: Lead with the
            #  decision and its cost...". It now returns "" and this says so, which is true and checkable.
            _understanding = (f"The request concerns: {subject} (domain: {domain}).\n\n" if subject else
                              f"{_NOT_TOLD} (domain: {domain}).\n\n")
            #  W593 (P2.20 a.ii) — AND THE TERM LIST IS WITHHELD RATHER THAN COUNTED OVER THE PLATFORM'S OWN
            #  PROMPT. With no labelled field there is nothing of the user's to count, and a list here under
            #  a heading that says "in your request" would be false. Withholding is the house move: W489
            #  renamed this heading and dropped "grounded in the input", W498 made the hadith tool withhold
            #  bigram-filled sections, and the halal tool already withholds three.
            #  W615 (FU-494, FU-503, M1 v8 R4.0 R5.4) — THE HEADING STOPS CLAIMING WHOSE WORDS THESE ARE.
            #  "most frequent in YOUR REQUEST" was a claim this engine cannot check: a labelled field reaches it
            #  the same way whether the user typed it, the platform composed it (the Native AI page's default
            #  "Task: Analyse the objective and key factors"), an upstream node produced it ("Subject:" in a
            #  workflow tree), or it is the entity's own grounding (the avatar's Objectives line). W593 fixed
            #  this by excluding labels, one at a time, and v8 found it on two more surfaces, because a label
            #  list can never know provenance. So the claim is removed rather than chased (ACCEPT 4): the list
            #  is named for what it is counted over, and says that is not necessarily the user's words.
            #  AND THE WITHHELD REASON IS THE TRUE ONE. A request in Arabic carries a labelled field; it was
            #  withheld because the tokeniser counts Latin-script words only, and was told "no labelled field".
            _termsec = (f"## Terms most frequent in the text you wrote\n"
                        f"_Extracted by counting words and adjacent pairs — not an analysis of "
                        f"the subject. Counted over the text the calling tool identified as yours, and "
                        f"over nothing else._\n"
                        f"{self._bullets(terms, 6)}\n\n" if terms else
                        f"## Terms most frequent in the text you wrote\n"
                        + (f"_WITHHELD: the text identified as yours holds no word this engine can count — it "
                           f"counts Latin-script words only, so text in another script yields no list. Nothing "
                           f"was counted in its place._\n\n" if _told else
                           f"_WITHHELD: the calling tool did not identify which text is yours, so any list "
                           f"here would be counted over the platform's own prompt._\n\n"))
            body = (
                f"{lead}## Understanding\n{_understanding}"
                # W489 (sweep S4.6, C3) — "Key factors" named an analysis nobody performed. The bullets
                # are the most frequent non-stopword words and adjacent bigrams in the request text; a
                # term appearing often is not a factor in the subject. The heading now says what the list
                # actually is, so a reader cannot mistake a word count for a judgement — and "grounded in
                # the input" is gone, which read as "grounded in YOUR subject" when the input could carry
                # another request's recalled text (closed at the gateway in the same round).
                f"{_termsec}"
                f"## Native approach\nWorkstation composes a structured response from its own "
                f"process-intelligence and knowledge for the agent '{agent}', framing the request above "
                f"rather than analysing it.\n\n"
                f"## Next steps\n{self._plan(domain)}"
            )
        return f"{_MARKER}\n\n{body}"

    # ── per-archetype structured scaffolds (useful, grounded, never fabricated) ──
    def _section_body(self, title: str, subject: str, domain: str, terms: List[str], personal: bool = False) -> str:
        t = title.lower()

        def has(*ks: str) -> bool:
            return any(k in t for k in ks)

        if has("risk", "gap", "failure", "weakness", "threat", "limitation"):
            #  W633 (FU-569) - the terms are words FROM THE REQUEST, not identified risks: worded as things to check
            return ("Structured risk frame for this dimension — surface, don't invent. The items below are terms "
                    "taken from the request to CHECK, not risks this engine identified:\n"
                    + self._dims(terms, "Check:") +
                    "\n- Likelihood × impact to be scored; mitigations and owners to be assigned.\n"
                    "- The native engine flags areas needing attention; a model resource details them.")
        if has("architecture", "component", "system", "technical", "build", "mvp", "stack", "blueprint"):
            return (f"Structured architecture frame for: {subject}.\n"
                    f"- Core capability: address {terms[0] if terms else 'the primary need'}.\n"
                    + self._dims(terms[:4], "Component for") +
                    "\n- Interfaces & data: specify inputs/outputs and contracts.\n"
                    f"- Non-functionals: reliability, security, and constitutional governance (gaas.v5), fit for {domain}.")
        if has("value proposition", "value prop"):
            return (f"Structured value-proposition frame for: {subject}.\n"
                    "- For [segment] who [need], this delivers [benefit] — unlike [the alternative].\n"
                    + self._dims(terms[:3], "Differentiator from") +
                    "\n- The single measurable outcome the user gets.")
        if has("hero", "call to action", "call-to-action", "cta", "headline", "landing"):
            return (f"Structured hero/conversion frame for: {subject}.\n"
                    "- Headline: the one-line promise of the OUTCOME (not the feature).\n"
                    + self._dims(terms[:3], "Proof point from") +
                    "\n- Primary call-to-action: the single next step for the visitor.\n"
                    "- Trust: the reassurance that lowers the risk of acting.")
        if has("feature", "capabilit"):
            return (f"Structured feature frame for: {subject}.\n"
                    + self._dims(terms[:5], "Capability") +
                    "\n- Tie each feature to a user job and an outcome — not a bare spec list.")
        if has("how it works", "user flow", "user journey", "journey", "onboarding"):
            return (f"Structured flow frame for: {subject}.\n"
                    "- Entry: how the user arrives and what they want.\n"
                    "- Steps: the shortest path from intent to value (number them).\n"
                    + self._dims(terms[:3], "Step touching") +
                    "\n- Exit: the value delivered + the next loop.")
        if has("offering", "delivery model", "sla", "service level", "service overview", "quality"):
            return (f"Structured service frame for: {subject}.\n"
                    "- Offering: what is delivered and the scope boundary.\n"
                    "- Delivery model: how it is provided (cadence, channel, roles).\n"
                    + self._dims(terms[:3], "Quality measure for") +
                    f"\n- SLAs & assurance: the commitments and how they're governed for {domain}.")
        if has("revenue", "pricing", "monetis", "monetiz", "unit econ"):
            return (f"Structured revenue frame for: {subject}.\n"
                    "- Units: what is charged for, and the pricing model.\n"
                    "- Unit economics: cost-to-serve vs price; contribution margin (to be quantified).\n"
                    + self._dims(terms[:3], "Stream from") +
                    "\n- Sensitivity: the key drivers to stress-test.")
        #  W631 (FU-557) - the go-to-market frame (segment, CAC, moat) belongs to a VENTURE. A salary plan or a CV
        #  that carries a "Market Positioning" heading is about a person in a labour market, and filling it with
        #  CAC and a moat contradicted the floor note beside it. Outside a venture the generic frame is used.
        if not personal and has("market", "value", "business model", "go-to-market", "gtm",
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
                    f"Structured frame over the terms most frequent in the request (a term count, not an "
                    f"analysis):\n{self._bullets(terms, 6)}")
        # generic — a frame over the request's own words, which is all the floor has
        return (f"Native structured frame for '{title}' over: {subject} (domain: {domain}). The list below "
                f"is the request's most frequent terms, not findings about them.\n"
                f"{self._bullets(terms, 5)}")

    # ── small builders ───────────────────────────────────────────────────────────
    def _dims(self, terms: List[str], prefix: str) -> str:
        picks = terms[:4] or ["the stated context"]
        return "\n".join(f"- {prefix} {p}." for p in picks)

    def _bullets(self, terms: List[str], n: int) -> str:
        #  W640 - the empty case states a fact about the COUNT. It used to read as a finding about the request
        #  ("no salient terms") when the list was empty because nobody had said which text was the person's.
        return "\n".join(f"- {k}" for k in terms[:n]) or "- (no terms were counted for this reply)"

    def _plan(self, domain: str) -> str:
        return ("- Validate the structured outputs above against the stated objective.\n"
                "- Route richer generation to a model resource (local-first; external only if enabled).\n"
                f"- Iterate via the orchestrator's cascade for {domain}; record outcomes to memory/UEG.")


native_engine = NativeReasoningEngine()
