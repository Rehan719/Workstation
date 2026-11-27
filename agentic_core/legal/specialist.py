"""The legal specialist: a meticulous clerk, never counsel (P3.23, FU-278's acceptance bar).

It ASSEMBLES; it does not write prose about a matter. Every particular is filled only from a line located in a
document inside the ONE named folder (legal/bundle.py, the only reader), and carries that document and line;
a particular nothing in the bundle states is rendered as a BLANK the user must fill, never as text. Every
authority (a statute or a case) is emitted only if the corpus the platform holds names it; otherwise it is
REFUSED by name. A filing-shaped artefact is a DRAFT until the Owner records an approval against it. Nothing
here is legal advice, and every response says so where it is read.

THE CORPUS IS THIN, and that is reported rather than hidden: knowledge/Law/EmploymentTribunal names one statute.
An authority outside it is refused, not paraphrased.
"""
from __future__ import annotations

import bisect
import pathlib
import re
import time
import unicodedata
import uuid
from typing import Any, Dict, List, Optional, Tuple

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

FILING_SHAPED = ("et1_claim", "cease_desist")
#  W714 (OWNER RULING 2026-10-13) - A DEED IS HELD UNTIL A QUALIFIED PERSON HAS READ THE SCHEDULE. Preparing
#  certain instruments is an activity reserved to authorised persons (Legal Services Act 2007, section 12 and
#  Schedule 2). Whether a given deed falls inside that is a qualified person's reading, and none has been made.
#  Until one is recorded, no deed is composed here. This is a hold and never a statement that a deed is reserved.
HELD_FOR_A_QUALIFIED_READ = ("partnership_deed",)
HELD_REASON = ("it is a deed, and preparing certain instruments is reserved to authorised persons by the "
               "Legal Services Act 2007 (section 12 and Schedule 2). No qualified person has yet read that Schedule "
               "for this platform, so no deed is composed here. This is a hold, and says nothing about whether "
               "this particular deed is reserved.")


def held_for_a_qualified_read(template_id: Any) -> bool:
    """True for a template named as held, and for ANY id that names a deed: the hold is on the kind and never
    only on one spelling (before W1194 the generator composed a document for any id it had never seen)."""
    tid = str(template_id or "").strip().lower()
    return tid in HELD_FOR_A_QUALIFIED_READ or "deed" in re.split(r"[^a-z]+", tid)
NOT_LEGAL_ADVICE = ("Nothing here is legal advice. This platform assembles and cites as a clerk would; it is "
                    "never counsel, and it never forecasts an outcome.")
#  W1194 (P5.18 clause 4) - THE RESERVED DOCUMENTS: the four whose preparation is a reserved instrument activity,
#  in the clause's own words. What the law reserves is said only from the register of sources' row for the Schedule,
#  read when asked: its name, its page, the day it was read, whose reading it was and what it did not read (clause 8);
#  never its summary, which names Acts this platform holds no row for (P5.11 clause 6). The sentence says what the
#  draft form refuses, not what the platform never does, and apart from what was asked: it never says that the id
#  asked for is one of these, and it names no one as entitled (section 13 was not read). Help is the list of where
#  help is, by its place on the page, and never a statement of who may prepare one; the route is kept for API
#  readers. It ends "Nothing here is legal advice.": the clerk's own statement (NOT_LEGAL_ADVICE) describes the
#  clerk, not the draft form, which composes the whole document (review M4). A deed stays held (W714).
RESERVED_SOURCE = "lsa-2007-sch2"
RESERVED_INSTRUMENTS = ("an instrument of transfer or charge of land", "an instrument for land registration",
                        "a contract for the sale or other disposition of land beyond a short lease",
                        "a deed for registration")
HELP_ROUTE = "GET /api/v1/law/help"      # the one page of where help is (W953), for API readers
HELP_PLACES = ("the list of where help is ('Where to get help from a person' on the Law page, and the support "
               "page)")


def reserved_source() -> Dict[str, Any]:
    """The row the reserved documents are read from, through the reader the time limits use (W1162): its name,
    page, the day it was read, whose reading it was and what was not read; or, where it cannot be read, why."""
    from agentic_core.legal import time_limits as _tl
    rows = _tl._register()
    r = (rows or {}).get(RESERVED_SOURCE)
    if r is None or not r.get("read_on"):
        return {"id": RESERVED_SOURCE, "read": False,
                "basis": ("the register of sources could not be read" if rows is None else
                          "the register of sources holds no reading of it")}
    return {"id": RESERVED_SOURCE, "read": True, "name": (r.get("names") or [RESERVED_SOURCE])[0],
            "page": r.get("page"), "read_on": r["read_on"], "read_by": r.get("read_by") or "",
            "not_read": r.get("not_read") or "nothing is listed as not read"}


def reserved_source_said() -> str:
    """The reading the reserved documents rest on, said as whose it is, where and when it was made and what it did
    not read; or why it is not shown."""
    s = reserved_source()
    if not s["read"]:
        return f"{RESERVED_SOURCE}: {s['basis']}, so the reading this rests on is not shown"
    by = str(s.get("read_by") or "").split(",")[0].strip()
    return (f"{s['name']}, read by this platform{f' ({by})' if by else ''}, not by a qualified person, at "
            f"{s['page']} on {s['read_on']}; not read: {s['not_read']}")


def reserved_reason() -> str:
    """The reserved documents, with the reading they rest on, what the draft form and the clerk refuse, and where
    help is. Since W1195 they refuse a request whose words the screen reads as an explicit ask to prepare one of
    these, and the draft form any template id it does not list."""
    return (f"Preparing any of these four documents is a reserved instrument activity: {'; '.join(RESERVED_INSTRUMENTS)} "
            f"({reserved_source_said()}). The Law draft form and the clerk refuse a request whose words the screen "
            f"reads as asking to prepare one of them, and the draft form any template id it does not list. For help "
            f"from a person, see {HELP_PLACES}. Nothing here is legal advice.")


def unlisted_reason(template_id: Any, drafted: List[str]) -> str:
    """An id the generator does not list: the templates it drafts. It says nothing else about the id asked for."""
    return (f"'{template_id}' is not a template this generator drafts, and nothing is composed for an id it does "
            f"not list. It drafts only these {len(drafted)}: {'; '.join(drafted)}.")


#  W1195 (P5.18 clause 4, and its ACCEPT: "the reserved documents are refused through the route a person would use") -
#  AN EXPLICIT ASK TO PREPARE ONE OF THE FOUR, READ IN A REQUEST'S WORDS. On the Law page a person picks a listed
#  template and types parties and instructions, and those words reach the composer; the clerk stores an artefact under
#  any template id. This screen reads only an explicit ask, in the words it knows: a drafting verb (draft, prepare,
#  write, draw up, do, complete, fill in, make, produce, create) standing as an ask, or I need or I want, governing
#  one of the documents it names - the forms TR1, TP1, AS1, CH1, AP1 or FR1, a transfer deed or a transfer of a house,
#  a flat or land, a legal charge or a mortgage deed, a contract for the sale of land, a lease of land for more than
#  three years, or the clause's own words for its four; or one of those named at a sentence's start and then please,
#  the please ending the sentence or followed by thanks, asap or by ("TP1 please"): the one ask with no ask word; or a
#  request whose document is one of those ("the document is a TR1", "draft it as a legal charge"); or, at the clerk, a
#  template id that names one. The ask's reach ends at a word that turns to another subject (covering, listing,
#  about ...) or at the first noun of a document it does not reserve (an NDA, an agreement, a letter, a schedule, a
#  summary, a copy ...). A mention with no ask word is not refused (a job's duties, a policy, a company's name, "your
#  mortgage"), and neither is an ask in a role's, a course's or a tool's words in its own sentence; but a request
#  about one of the documents, phrased as an ask ("I need my TR1 checked"), is refused. It misses most other ways of
#  asking: a request it does not read as one is drafted as before, which is not a
#  clearance. Measured on 2026-11-22, the word screen it replaces recognised 7 of the red team's 50 blind reserved asks
#  and refused 2 of their 70 ordinary drafts and 16 of 20 property-sector ones; this screen trades recall for
#  precision. Its labelled phrasings, and its stated limits with their reasons, are scripts/screen_phrasings.py's
#  RESERVED and RESERVED_LIMITS. The words are read after folding (NFKC, case folded, format characters and marks
#  dropped), in one pass with no recursion, so a field of any length is read in time linear in its length.
_POSS = r"(?:my|our|his|her|their|its|this|that|these|those|the|a|an)"
_P = r"(?:" + _POSS + r" )?"
#  up to two words before the place, never "your" (a request about the reader's own home is a mention)
_ADJ = r"(?:(?!your )[a-z0-9]+ ){0,2}?"
#  a place a transfer, a charge or a mortgage is of, read as one only when the next word leaves it one
_TPLACE = (r"(?:houses?|home(?! (?:insurance|rights|office|page|screen|working|care|loans?|contents|improvements?|"
           r"ownership|delivery|visits?|help|buyers?|owners?)\b)|flats?|apartments?|bungalows?|cottages?|"
           r"farm(?! (?:shop|machinery|equipment|animals|stock|produce|business)\b)|farmhouses?|farmland|"
           r"land(?! (?:registry|rover)\b)|fields?|plots?|premises|"
           r"buildings?(?! (?:work|works|contracts?|society|societies|regulations|insurance|materials|control)\b)|"
           r"freehold|leasehold|barns?|maisonettes?|gardens?|acres?|paddocks?|"
           r"propert(?:y|ies)(?! (?:in|rights|portfolios?|management|managers?|tax|insurance|data|details|law|"
           r"market|sector|industry)\b))\b")
#  ... and, for a lease or a sale, a shop, an office or a unit as well
_LPLACE = (r"(?:" + _TPLACE + r"|shops?|offices?|units?|warehouses?|yards?|studios?|storerooms?|floors?|pubs?|"
           r"restaurants?|cafes?|salons?|surgery|surgeries|garages?)\b")
_SPLACE = r"(?:" + _TPLACE + r"|shops?|offices?|warehouses?|garages?)\b"
#  a house given by its address: a number, a street word (abbreviated or Welsh), or a postcode
_ADDR = (r"(?:\d+[a-z]? (?:[a-z]+ ){1,3}?(?:street|st|road|rd|avenue|ave|lane|ln|close|cl|drive|way|wy|court|"
         r"crescent|cres|gardens|gdns|terrace|tce|terr|grove|row|square|walk|mews|mws|hill|park|place|parade|pde|"
         r"green|rise|view)\b|\d+[a-z]? (?:heol|ffordd|stryd|lon|rhodfa|cilgant|clos|maes|teras|sgwar|llwybr)"
         r"(?: [a-z]+){1,3}|\d+[a-z]? (?:[a-z]+ ){0,5}?[a-z]{1,2}\d[a-z0-9]? \d[a-z]{2}\b)")
_TERM4 = (r"(?:[4-9]|[1-9]\d+|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
          r"seventeen|eighteen|nineteen|twenty(?: one| five)?|thirty|forty|fifty|sixty|seventy|eighty|ninety(?: nine)?|"
          r"one hundred and twenty five|nine hundred and ninety nine)")
_OVER3 = r"(?:(?:more than|over) (?:three|3)|" + _TERM4 + r")"
#  a lease, an underlease or sublease, or a tenancy (a farm business tenancy among them): one of a place for more than
#  three years is a lease of it
_LEASE = r"(?:(?:under|sub) ?)?(?:leases?|(?:(?:farm )?business )?tenanc(?:y|ies))"
#  a form's code, never where an inward postcode, a sibling code (a range) or a label noun follows it ("Truro TR1 2LS",
#  "TR1 to TR5", "TR1 requirements")
_CODE_OK = (r"(?! \d[a-z]{2}\b)(?! (?:to|through|until)? ?(?:tr|tp|as|ch|ap|fr) ?\d)(?! (?:requirements?|reports?|"
            r"actions?|items?|tests?|milestones?|deliverables?|sections?|chapters?|points?|levels?|criteria|dataset|"
            r"data|grades?|class|classes|copy|copies|checklists?|guides?|guidance|process|bundles?|templates?|fees|"
            r"packs?|scans|forms)\b)")
_CODE_TC = r" (?:hm )?(?:land registry )?(?:form )?(?:tr ?1|tp ?1|as ?1|ch ?1)s?\b" + _CODE_OK
_CODE_LR = r" (?:hm )?(?:land registry )?(?:form )?(?:ap ?1|fr ?1)s?\b" + _CODE_OK

RESERVED_KINDS = (
    {"id": "transfer_or_charge", "said": "a transfer or legal charge of land, a house or a flat",
     "clause": "an instrument of transfer or charge of land", "match": (
        _CODE_TC, r" transfer deeds?\b", r" deeds? of transfer\b", r" transfers? of (?:the )?(?:whole|part)\b",
        r" transfers? of " + _P + _ADJ + _TPLACE, r" transfers? of " + _ADDR,
        r" transfers? of (?:the )?title (?:to|of|for) " + _P + _ADJ + r"(?:" + _TPLACE + r"|" + _ADDR + r")",
        r" (?:land|house|flat) transfers?(?! (?:tax|taxes|duty|duties)\b)\b",
        r" transfers? of equity (?:in|on|of|for) " + _P + _ADJ + _TPLACE,
        r" deeds? of gift (?:of|for) " + _P + _ADJ + _TPLACE,
        r" (?:(?:first|second|1st|2nd) )?legal charges?\b",
        r" (?:(?:first|second|1st|2nd) )?charges? (?:over|on|against) " + _P + _ADJ + r"(?:" + _TPLACE + r"|" + _ADDR + r")",
        r" mortgage deeds?\b", r" mortgages? (?:over|on|against) " + _P + _ADJ + r"(?:" + _TPLACE + r"|" + _ADDR + r")",
        r" instruments? of (?:transfer|charge)(?: or (?:transfer|charge))? of land\b")},
    {"id": "land_registration", "said": "a Land Registry application form (AP1 or FR1)",
     "clause": "an instrument for land registration", "match": (
        _CODE_LR, r" instruments? for (?:land )?registration\b",
        r" (?:(?:hm )?land registry )?(?:forms? |applications? )?(?:for )?first registrations?\b",
        (r" deeds? for registration\b", "a deed for registration"))},
    {"id": "sale_of_land", "said": "a contract for the sale of land, a house or a flat",
     "clause": "a contract for the sale or other disposition of land beyond a short lease", "match": (
        r" contracts? (?:for|of) (?:the )?(?:sale|purchase)(?: or other disposition)? of " + _P + _ADJ +
        r"(?:" + _SPLACE + r"|" + _ADDR + r")",
        r" (?:sale|purchase) contracts? (?:for|of) " + _P + _ADJ + r"(?:" + _SPLACE + r"|" + _ADDR + r")",
        r" contracts? to (?:buy|purchase|sell) " + _P + _ADJ + r"(?:" + _SPLACE + r"|" + _ADDR + r")",
        r" (?:land|house|property|flat|farm|bungalow|cottage) (?:sale|purchase) contracts?\b")},
    {"id": "lease_by_deed", "said": "a lease of land, a house or a flat for more than three years",
     "clause": "a contract for the sale or other disposition of land beyond a short lease", "match": (
        r" " + _TERM4 + r" ?years? (?:long )?" + _LEASE + r" (?:of|on|for) " + _P + _ADJ + r"(?:" + _LPLACE + r"|" +
        _ADDR + r")",
        r" " + _LEASE + r" (?:of|on|for) " + _P + _ADJ + r"(?:" + _LPLACE + r"|" + _ADDR + r")" +
        r" (?:[a-z0-9]+ ){0,6}?for (?:a (?:fixed )?term of )?" + _OVER3 + r" ?years?\b",
        r" " + _LEASE + r" for (?:a (?:fixed )?term of )?" + _OVER3 + r" ?years? (?:of|on|for) " + _P + _ADJ +
        r"(?:" + _LPLACE + r"|" + _ADDR + r")")},
)
#  a template id is a label, not a request: read for the document it names, with no ask, and these names as well
_ID_ONLY = (
    ("transfer_or_charge", r" transfers? of equity\b"), ("transfer_or_charge", r" second charges?\b"),
    ("sale_of_land", r" sale contracts?\b"),
    ("sale_of_land", r" contracts? for (?:the )?sale\b"))
_KIND = {k["id"]: k for k in RESERVED_KINDS}


def _nouns(extra=()):
    alts, meta = [], {}
    for k in RESERVED_KINDS:
        for p in k["match"]:
            pat, clause = (p, k["clause"]) if isinstance(p, str) else p
            meta[f"g{len(alts)}"] = (k["id"], clause)
            alts.append(f"(?P<g{len(alts)}>{pat})")
    for kid, pat in extra:
        meta[f"g{len(alts)}"] = (kid, _KIND[kid]["clause"])
        alts.append(f"(?P<g{len(alts)}>{pat})")
    return re.compile("|".join(alts)), meta


_NOUNS, _NOUN_META = _nouns()
_NOUNS_ID, _NOUN_ID_META = _nouns(_ID_ONLY)

#  THE ASK: where a drafting verb stands as an ask - at a sentence's start (after "please", "can you", "I need you to"
#  and the like), after "please", after "can you", after "I need" or "I want"; or "the document is", "draft it as"
_VERB = (r"(?:draft|redraft|prepare|write|draw up|do|complete|fill in|fill out|make|produce|create|put together|"
         r"type up)")
_LEAD = r"(?:(?:and|then|also|now|so|ok|okay|hi|hello|please|kindly|pls|plz|just) )*"
_ASK = re.compile(
    r"(?:^|(?<= \.)) " + _LEAD + r"(?:(?:just |urgently |also )?need(?= )"
    r"|(?:(?:can|could|would|will) you (?:(?:please|kindly|just|also) )*|(?:i|we) "
    r"(?:(?:just|really|also|urgently|only) )?(?:need|want|would like|d like) (?:you|someone) to |help (?:me|us) )?" +
    _VERB + r"(?= ))"
    r"| (?:please|kindly|pls|plz) " + _VERB + r"(?= )"
    r"| (?:can|could|would|will) you (?:(?:please|kindly|just|also) )*" + _VERB + r"(?= )"
    r"| (?:i|we) (?:(?:just|really|also|urgently|only) )?(?:need|want|would like|d like|require|am after|are after)"
    r"(?: (?:you|someone|somebody) to " + _VERB + r")?(?= )"
    r"| (?:the |this |my |our )?(?:document|deed|paperwork) (?:is|will be|should be|must be|needs to be|has to be)(?= )"
    r"| " + _VERB + r" (?:it|this|that|them|the document|the deed|the agreement) as(?= )")
#  how far the ask reaches for its document (do and make reach only past a determiner and one word), and the words
#  that end its reach: a word that turns to another subject, or the first noun of a document it does not reserve
_REACH = 6
_SHORT_REACH = 2
_STOP = frozenset(("nda", "ndas", "agreement", "agreements", "policy", "policies", "terms", "letter", "letters",
                   "schedule", "schedules", "clause", "clauses", "checklist", "checklists", "guide", "guides",
                   "summary", "summaries", "copy", "copies", "notes", "email", "emails", "minutes", "memo", "memos",
                   "report", "reports", "contract", "contracts"))
_BREAK = frozenset(("for", "to", "so", "that", "which", "who", "whom", "whose", "asking", "ask", "asks", "about",
                    "covering", "cover", "covers", "listing", "including", "containing", "setting", "summarising",
                    "summarizing",
                    "regarding", "re", "concerning", "enclosing", "attaching", "attached", "enclosed", "with",
                    "without", "under", "from", "by", "if", "whether", "because", "after", "before", "until",
                    "explaining", "confirming", "chasing", "requesting", "telling", "saying", "while", "when", "where",
                    "once", "between", "against", "via", "using", "not", "never", "no", "except", "but", "instead",
                    "rather", "than", "like", "such", "unlike", "."))
#  an ask that is said, not made: a role's duties, a course, a tool, a negation
_CUE = frozenset(("duties", "duty", "responsibilities", "responsibility", "responsible", "role", "roles", "job", "jobs",
                  "task", "tasks", "candidate", "candidates", "applicant", "applicants", "employee", "employees",
                  "vacancy", "vacancies", "recruit", "recruiting", "recruitment", "hiring", "trainee", "trainees",
                  "apprentice", "apprentices", "training", "course", "courses", "lesson", "lessons", "module",
                  "modules", "software", "app", "apps", "platform", "platforms", "tool", "tools", "feature",
                  "features", "system", "systems", "quiz", "exam", "exams", "example", "examples"))
_NEG = frozenset(("not", "never", "no", "dont", "without", "nobody", "stop", "cannot", "cant", "neither", "nor"))
_NEG2 = frozenset((("don", "t"), ("do", "not"), ("does", "not"), ("doesn", "t"), ("didn", "t"), ("did", "not"),
                   ("won", "t"), ("will", "not"), ("no", "need"), ("need", "not"), ("needn", "t"), ("shouldn", "t"),
                   ("should", "not"), ("can", "t"), ("isn", "t"), ("aren", "t")))
_CUE_REACH = 12


def _fold(text: Any) -> Tuple[str, List[int], List[Tuple[int, int]]]:
    """A request's words as the screen reads them, with where each came from: NFKC, case folded, format characters
    (zero-width, soft hyphen, ...) and marks dropped, then plain letters and digits, one space apart, and a sentence's
    end kept as " . ". Returns the folded words (padded with a space each side), each word's offset in them, and each
    word's span in the text as typed."""
    s = str(text or "")
    words: List[str] = []
    spans: List[Tuple[int, int]] = []
    cur: List[str] = []
    start = -1
    n = len(s)

    def flush(end):
        nonlocal start
        if cur:
            words.append("".join(cur))
            spans.append((start, end))
            cur.clear()
        start = -1

    for i, ch in enumerate(s):
        if ch < "\x80":
            outs = (ch.lower(),)
        else:
            t = unicodedata.normalize("NFKD", unicodedata.normalize("NFKC", ch).casefold())
            outs = tuple(x for x in t if unicodedata.category(x)[0] != "M" and unicodedata.category(x) != "Cf")
            if not outs:
                continue        # a format character or a mark joins the word it stands in
        for c in outs:
            if c.isalnum():
                if start < 0:
                    start = i
                cur.append(c)
            elif c in ".;:!?" and (i + 1 >= n or s[i + 1].isspace() or s[i + 1] in "\"')]" or c in ";!?"):
                flush(i)
                if words and words[-1] != ".":
                    words.append(".")
                    spans.append((i, i + 1))
            else:
                flush(i)
    flush(n)
    offs: List[int] = []
    pos = 1
    for w in words:
        offs.append(pos)
        pos += len(w) + 1
    return " " + " ".join(words) + " ", offs, spans


def _said_as_typed(text: str, offs: List[int], spans: List[Tuple[int, int]], a: int, b: int) -> str:
    """The words a match covers, as the person typed them."""
    i = max(0, bisect.bisect_right(offs, a) - 1)
    j = max(i, bisect.bisect_left(offs, b) - 1)
    while i < j and spans[i] and text[spans[i][0]:spans[i][1]] in ".;:!?":
        i += 1
    return " ".join(str(text)[spans[i][0]:spans[j][1]].split())


def _said_not_made(f: str, start: int) -> bool:
    """True when the ask is negated, or stands in a role's, a course's or a tool's words."""
    before = f[max(0, start - 200):start].split()
    if "." in before:          # only the ask's own sentence, and a heading just before it (final check F6)
        cut = len(before) - before[::-1].index(".")
        head = before[cut - 2:cut - 1]                 # "Duties: draft ..." - the word the heading's colon follows
        before = before[cut:]
        if any(w in _CUE for w in head):
            return True
    last = before[-3:]
    if any(w in _NEG for w in last) or any((a, b) in _NEG2 for a, b in zip(last, last[1:])):
        return True
    return any(w in _CUE for w in before[-_CUE_REACH:])


_LEAD_WORDS = frozenset(("and", "then", "also", "now", "so", "ok", "okay", "hi", "hello", "just"))
_PLEASE_ENDS = ("thanks", "thank", "asap", "by", "cheers", "ta")


def _hit(text, offs, spans, meta, n, a, b=None) -> Dict[str, str]:
    """The kind a match names, with the words that asked as typed: from the ask's first word that is not a greeting
    or a joining word, through the document (or its please)."""
    kid, clause = meta[n.lastgroup]
    k = _KIND[kid]
    i = max(0, bisect.bisect_right(offs, a + 1) - 1)        # the word that starts after the space at a
    end = n.end() if b is None else b
    while i + 1 < len(offs) and offs[i + 1] < end and \
            str(text)[spans[i][0]:spans[i][1]].lower().strip(",") in _LEAD_WORDS:
        i += 1
    return {"id": kid, "said": k["said"], "clause": clause,
            "words": _said_as_typed(text, offs, spans, offs[i] if offs else a, end)}


def _please_asks(f: str, n) -> int:
    """The end of '<document> please' when it is an ask: the document opens its sentence (a determiner or a lead
    word before it at most), and please ends the sentence or the field, or is followed by thanks, asap or by.
    Returns 0 when it is not one."""
    for tok in (" please", " pls", " plz"):
        if f.startswith(tok + " ", n.end()):
            break
    else:
        return 0
    after = f[n.end() + len(tok) + 1:].split(" ", 1)[0]
    if after not in ("", ".") and after not in _PLEASE_ENDS:
        return 0
    before = f[:n.start()].split()
    if "." in before:
        before = before[len(before) - before[::-1].index("."):]
    if [w for w in before if w not in _LEAD_WORDS and w not in ("the", "a", "an", "my", "our", "this", "that")]:
        return 0
    if _said_not_made(f, n.start()):
        return 0
    return n.end() + len(tok)


def reserved_match(text: Any, as_id: bool = False) -> Optional[Dict[str, str]]:
    """The reserved kind an explicit ask in a request's words is for - or, as_id, the kind a template id names - with
    the words that asked (as typed), and the clause's words it falls under; or None. None is NOT a clearance."""
    f, offs, spans = _fold(text)
    if as_id:
        n = _NOUNS_ID.search(f)
        return _hit(text, offs, spans, _NOUN_ID_META, n, n.start()) if n else None
    for n in _NOUNS.finditer(f):
        e = _please_asks(f, n)
        if e:
            return _hit(text, offs, spans, _NOUN_META, n, n.start(), e)
    asked_other = False      # an explicit ask already made in this field for a document the screen does not reserve
    for m in _ASK.finditer(f):
        said = m.group(0)
        bare = re.search(r"(?:need|want|like|require|after)$", said) is not None
        if _said_not_made(f, m.start()) or (bare and asked_other):
            continue
        reach = _SHORT_REACH if re.search(r" (?:do|make)$", said) else _REACH
        pos = m.end()
        for _k in range(reach + 1):
            n = _NOUNS.match(f, pos)
            if n:
                return _hit(text, offs, spans, _NOUN_META, n, m.start())
            nxt = f.find(" ", pos + 1)
            w = f[pos + 1:nxt] if nxt >= 0 else ""
            if w in _STOP and not bare:
                asked_other = True
            if nxt < 0 or w in _BREAK or w in _STOP:
                break
            pos = nxt
    return None


def reserved_kind(text: Any) -> Optional[Dict[str, str]]:
    """The reserved kind an explicit ask in a request's words is for, or None. None is NOT a clearance."""
    m = reserved_match(text)
    return {"id": m["id"], "said": m["said"]} if m else None


def reserved_refusal(template_id: Any, where: str, kind: Dict[str, str], act: str = "drafted",
                     kept: str = "composed", reading: str = "as asking to prepare") -> str:
    """The refusal of a request the screen read as asking for a reserved kind: what it read, in which field, what it
    took it as asking for and the clause's words that would fall under; never that the person's document is one."""
    clause = kind.get("clause") or _KIND.get(kind.get("id"), {}).get("clause", "")
    return (f"'{template_id}' is not {act}: the words \"{kind.get('words') or ''}\" in {where} were read {reading} "
            f"{kind['said']}, which would fall under \"{clause}\", one of the reserved documents, so nothing was "
            f"{kept}. The screen reads words, not what a document is. {reserved_reason()}")


RESERVED_SCREEN = ("The screen reads only an explicit ask to prepare one of the reserved documents, in the words it "
                   "knows: a drafting verb (draft, prepare, write, draw up, do, complete, fill in, make, produce or "
                   "create) standing as an ask, or I need or I want, for the form TR1, TP1, AS1, CH1, AP1 or FR1, a "
                   "transfer deed or a transfer of a house, a flat or land, a legal charge or a mortgage deed, a "
                   "contract for the sale of land, or a lease of land for more than three years; or one of those named "
                   "at a sentence's start and then please, with nothing after the please but thanks, asap or by (\"TP1 please\"), the one "
                   "ask the screen reads with no ask word; or a request whose document is one of those. It reads the draft form's words "
                   "(each party's label and details, the instructions and the jurisdiction) for such an ask, and the "
                   "template id the clerk is given for the document it names. A request or an id it reads so is "
                   "refused before anything is composed or stored. A mention with no ask word is not refused, but a request "
                   "about one of these documents, phrased as an ask (\"I need my TR1 checked by a solicitor\"), can "
                   "still be refused: the screen reads words, not what is asked for. It misses "
                   "most other ways of asking: a request it does not read as one, whatever it asks for, is drafted as "
                   "before, and that is not a clearance. "
                   "Schedule 2 paragraph 5(1)(c), as this platform read it, also reaches any other instrument "
                   "relating to real or personal estate, or to court proceedings, other than a will, an agreement not "
                   "intended to be executed as a deed, a letter or power of attorney, or a transfer of stock with no "
                   "trust or limitation. The screen reads none of those (a declaration of trust, an easement, an "
                   "assignment made as a deed, a partnership deed), and whether the clerk's own templates are "
                   "instruments relating to court proceedings has not been read; the draft form and the clerk hold a "
                   "template whose id names a deed all the same. Whether this platform may prepare any of these is a "
                   "question for the solicitor whose reading of the Law pages comes before any public release. The "
                   "platform's other free-text generators are not screened, among them the Generator page's POST "
                   "/api/v1/generator/produce and the Synthesis Studio page's POST /api/v1/synthesis/generate and "
                   "/stream.")


_CORPUS = pathlib.Path(__file__).resolve().parents[2] / "knowledge" / "Law" / "EmploymentTribunal"


def _corpus_text() -> str:
    parts = []
    for p in sorted(_CORPUS.rglob("*.json")) + sorted(_CORPUS.rglob("*.md")):
        try:
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
    return "\n".join(parts)


def _ontology_rules() -> List[str]:
    """The provisions the ontology file lists by name - the only names an authority is resolved against."""
    import json
    try:
        d = json.loads((_CORPUS / "ontology" / "uk_employment_law_v9.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [str(r) for r in (d.get("rules") or []) if isinstance(r, str) and r.strip()]


def _authorities_held() -> Dict[str, Any]:
    """W821 (FU-1001) - how many provisions an authority can be resolved against, and of which statutes."""
    rules = _ontology_rules()
    statutes = sorted({_statute_of(r) for r in rules})
    return {"provisions": len(rules), "statutes": statutes,
            "basis": (f"an authority is resolved only against the {len(rules)} provision(s) the employment-law "
                      f"corpus's ontology lists by name ({'; '.join(statutes) or 'none'}); the ontology's other "
                      f"concepts are not read, and anything else named is refused" if rules else
                      "the ontology lists no provision (or could not be read), so every authority is refused")}


def _norm_authority(s: str) -> str:
    return " ".join(str(s or "").lower().split())


def _statute_of(rule: str) -> str:
    """'Equality Act 2010 Section 13 (...)' -> 'Equality Act 2010'; a rule with no section is returned whole."""
    import re
    return re.split(r"\s+(?:section|s\.)\s*\d", rule, maxsplit=1, flags=re.I)[0].strip()


def resolve_authority(name: str) -> Dict[str, Any]:
    n = str(name or "").strip()
    if not n:
        return {"authority": n, "resolved": False, "basis": "no authority was named"}
    #  W666 (ledger v16 R5.0) - this was a substring test over every file in the corpus folder, one of
    #  which is a manifest of file paths: a single letter resolved, and so did any fragment of a file name.
    #  A name now resolves only as a WHOLE provision the ontology lists, or as the whole title of a statute
    #  one of those provisions belongs to - and the basis says which, and what the corpus holds of it.
    key = _norm_authority(n)
    rules = _ontology_rules()
    for rule in rules:
        if key in (_norm_authority(rule), _norm_authority(rule.split("(")[0])):
            return {"authority": n, "resolved": True, "matched": "provision",
                    "basis": ("named in the employment-law corpus this platform holds "
                              "(knowledge/Law/EmploymentTribunal): the ontology lists this provision")}
    held = [r for r in rules if _norm_authority(_statute_of(r)) == key and _statute_of(r) != r]
    if held:
        return {"authority": n, "resolved": True, "matched": "statute",
                "basis": ("named in the employment-law corpus this platform holds "
                          "(knowledge/Law/EmploymentTribunal): the ontology lists " + str(len(held)) +
                          " provision(s) of this statute and no others - " +
                          "; ".join(r.split("(")[0].strip() for r in held))}
    return {"authority": n, "resolved": False,
            "basis": ("REFUSED: the corpus this platform holds does not name it, so it is not cited - an authority "
                      "is resolved against a real source or not emitted at all")}


def locate(words: List[str]) -> Dict[str, Any]:
    """The first line in the bundle containing every word, with its document and 1-based line, or a blank."""
    from agentic_core.legal import bundle
    ws = [w.lower() for w in words if str(w).strip()]
    ls = bundle.list_documents()
    if not ws or ls["documents"] is None:
        return {"found": False, "document": None, "line": None, "text": None,
                "basis": ls["basis"] if ls["documents"] is None else "no search words were given"}
    for doc in ls["documents"]:
        o = bundle.open_document(doc)
        if not o["opened"]:
            continue
        for i, ln in enumerate(o["text"].splitlines(), start=1):
            low = ln.lower()
            if all(w in low for w in ws):
                return {"found": True, "document": doc, "line": i, "text": ln.strip(),
                        "basis": f"located at {doc}:{i}"}
    return {"found": False, "document": None, "line": None, "text": None,
            "basis": f"no line in the {ls['count']} document(s) of the named folder states this"}


def verify_located(p: Dict[str, Any]) -> Dict[str, Any]:
    """Re-read the cited line through the bundle reader and check the quoted text is there."""
    from agentic_core.legal import bundle
    if not p.get("found"):
        return {"verdict": "NOT_ASSESSABLE", "basis": "a blank cites nothing, so there is nothing to verify"}
    o = bundle.open_document(p["document"])
    if not o["opened"]:
        return {"verdict": "NOT_ASSESSABLE", "basis": o["basis"]}
    lines = o["text"].splitlines()
    ok = 1 <= p["line"] <= len(lines) and p["text"] in lines[p["line"] - 1]
    return {"verdict": "MET" if ok else "UNMET",
            "basis": (f"the quoted text is present at {p['document']}:{p['line']}" if ok else
                      f"the quoted text is NOT at {p['document']}:{p['line']}")}


def assemble(template_id: str, particulars: List[Dict[str, Any]], authorities: List[str]) -> Dict[str, Any]:
    from agentic_core.legal import bundle
    filled = []
    for spec in particulars or []:
        name = str((spec or {}).get("name") or "").strip()
        words = [w for w in (spec or {}).get("words") or [] if str(w).strip()]
        loc = locate(words)
        item = {"particular": name, **loc}
        item["verification"] = verify_located(loc)
        item["rendered"] = (loc["text"] if loc["found"] else
                            f"[BLANK: {name} - no document in the bundle states this; fill it in yourself]")
        filled.append(item)
    auth = [resolve_authority(a) for a in authorities or []]
    sourced = [f["particular"] for f in filled if f["found"]]
    blanks = [f["particular"] for f in filled if not f["found"]]
    unresolved_checks = [f["particular"] for f in filled if f["verification"]["verdict"] != "MET" and f["found"]]
    filing = template_id in FILING_SHAPED
    art = {"artefact_id": "lgl-" + uuid.uuid4().hex[:10], "template_id": template_id,
           "status": "draft_awaiting_owner_approval" if filing else "draft",
           "filing_shaped": filing, "particulars": filled, "authorities": auth,
           "sourced": sourced, "blanks": blanks, "unresolved_checks": unresolved_checks,
           "authorities_refused": [a["authority"] for a in auth if not a["resolved"]],
           #  W821 (FU-1001) - what an authority is resolved against, said beside the result: the ontology's
           #  named provisions alone (its machine-made concepts are not read), however few they are
           "authorities_held": _authorities_held(),
           "is_template": not sourced,
           "bundle": bundle.status(), "not_legal_advice": NOT_LEGAL_ADVICE,
           "face": (f"{len(sourced)} particular(s) from a document, {len(blanks)} BLANK for you to fill"
                    + (f"; {len(unresolved_checks)} located line(s) failed re-verification" if unresolved_checks else "")
                    + ("; this is a TEMPLATE - the bundle stated none of its particulars" if not sourced else "")),
           "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with store_lock(_store()):
        d = read_json_strict(_store(), missing={"artefacts": {}}, expect=dict)
        d.setdefault("artefacts", {})[art["artefact_id"]] = art
        atomic_write_json(_store(), d)
    return art


def _store():
    return data_path("legal/artefacts.json")


def approve(artefact_id: str, by: str) -> Dict[str, Any]:
    if not str(by or "").strip():
        return {"approved": False, "refused": "unattributed", "basis": "REFUSED: the approver is not named"}
    with store_lock(_store()):
        d = read_json_strict(_store(), missing={"artefacts": {}}, expect=dict)
        a = (d.get("artefacts") or {}).get(artefact_id)
        if not a:
            return {"approved": False, "refused": "not_found", "basis": f"REFUSED: no artefact {artefact_id}"}
        if not a.get("filing_shaped"):
            return {"approved": False, "refused": "not_filing_shaped",
                    "basis": "REFUSED: only a filing-shaped artefact needs the Owner's approval"}
        a["status"] = "approved_by_owner"
        a["approved_by"], a["approved_at"] = str(by), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        atomic_write_json(_store(), d)
    return {"approved": True, "refused": None, "artefact": a,
            "basis": f"approved by {by}; it is still not legal advice and nothing about the matter leaves this machine"}
