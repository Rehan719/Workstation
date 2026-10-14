"""ONE PROVISION OF AN ACT, WORD FOR WORD, FROM ITS PUBLISHER (plan item P5.20, clauses 1 and 3).

Nothing here composes, summarises or explains, and no model is called. A provision is fetched from
legislation.gov.uk on a person's request, read as the publisher structured it, and returned with what must
travel with it: the publisher, the address, the date of the version, the extent as the publisher writes it,
the publisher's own list of changes it has not yet written into the text, and the licence it is reused under.
Nothing is stored. The text that is shown and the text that is hashed are one definition, so a difference of
one character between them can be found - `fidelity` is that check.
"""
import hashlib
import re
import time
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

import httpx

PUBLISHER = "legislation.gov.uk"
BASE = "https://www.legislation.gov.uk"
_HOSTS = ("www.legislation.gov.uk", "legislation.gov.uk")
LICENCE = ("Contains public sector information licensed under the Open Government Licence v3.0. "
           "(c) Crown and database right.")
WHAT_THIS_IS = ("the publisher's text of one provision, word for word. It is not advice, not an explanation, "
                "and not a statement that it applies to anyone's situation")
#  an address is built from parts that are each checked; nothing a caller types reaches the URL unchecked
KINDS = ("ukpga", "uksi", "asp", "anaw", "asc", "nia", "ukla")
_L = "{http://www.legislation.gov.uk/namespaces/legislation}"
_M = "{http://www.legislation.gov.uk/namespaces/metadata}"
_DC = "{http://purl.org/dc/elements/1.1/}"


class NotAnAddress(ValueError):
    """The parts given do not name a provision."""


class PublisherRefused(RuntimeError):
    def __init__(self, why: str, status: int | None = None):
        super().__init__(why)
        self.status = status


def address(kind: str, year: Any, number: Any, section: Any) -> str:
    if kind not in KINDS:
        raise NotAnAddress(f"the kind of legislation must be one of {list(KINDS)}")
    if not re.fullmatch(r"\d{4}", str(year)) or not (1800 <= int(year) <= 2100):
        raise NotAnAddress("the year must be four digits between 1800 and 2100")
    if not re.fullmatch(r"\d{1,5}", str(number)) or int(number) < 1:
        raise NotAnAddress("the number must be a whole number from 1")
    if not re.fullmatch(r"[0-9]{1,4}[A-Z]{0,3}", str(section)):
        raise NotAnAddress("the section must be a number, optionally followed by capital letters (111, 27A, 207B)")
    return f"{BASE}/{kind}/{int(year)}/{int(number)}/section/{section}"


def _lines(group: ET.Element) -> List[Dict[str, Any]]:
    """The provision as the publisher structured it: each numbered part with its own words, in order.
    Words are taken from the publisher's nodes and whitespace-normalised; none is added or dropped."""
    out: List[Dict[str, Any]] = []

    def walk(el: ET.Element) -> None:
        tag = el.tag.replace(_L, "")
        if tag in ("P1", "P2", "P3", "P4", "P5"):
            num = el.find(_L + "Pnumber")
            texts = [" ".join("".join(t.itertext()).split()) for t in el.findall(f"{_L}{tag}para/{_L}Text")]
            out.append({"level": int(tag[1]), "number": ("".join(num.itertext()).strip() if num is not None else ""),
                        "text": " ".join(x for x in texts if x)})
        for child in el:
            walk(child)
    walk(group)
    return out


def shown_text(parts: List[Dict[str, Any]]) -> str:
    """The one definition of the text: every part's number and words, in the publisher's order."""
    return "\n".join((f"{p['number']} " if p["number"] else "") + p["text"] for p in parts).strip()


def fidelity(parts: List[Dict[str, Any]], sha256: str) -> Dict[str, Any]:
    """Is what is about to be shown, character for character, what was read from the publisher?"""
    ok = hashlib.sha256(shown_text(parts).encode("utf-8")).hexdigest() == sha256
    return {"checked": True, "matches": ok,
            "basis": ("an automated check by this platform: the text shown was compared character for character "
                      "with the text read from the publisher for this request, and "
                      + ("matches" if ok else "DOES NOT MATCH") + ". It checks the copy, not the law")}


def touches(section: str, provisions: str) -> bool:
    """Does the publisher's description of what an amendment touches include this section? A single section
    is matched exactly (7 is not 70 and not 7A). A range is read by its whole-number ends, and a lettered
    section inside a numeric range counts as inside, which errs toward warning the reader."""
    sec = str(section)
    lead = int(re.match(r"\d+", sec).group(0))
    for m in re.finditer(r"ss?\.\s*(\d+[A-Z]*)(?:\([^)]*\))*(?:\s*[-–]\s*(\d+[A-Z]*))?", str(provisions or "")):
        first, last = m.group(1), m.group(2)
        if last is None:
            if first == sec:
                return True
            continue
        if int(re.match(r"\d+", first).group(0)) <= lead <= int(re.match(r"\d+", last).group(0)):
            return True
    return False


def parse(xml_text: str, section: str) -> Dict[str, Any]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        raise PublisherRefused("the publisher's answer could not be read as a provision", 200) from None
    groups = list(root.iter(_L + "P1group"))
    if len(groups) != 1:
        raise PublisherRefused(f"the publisher returned {len(groups)} provisions where one was asked for", 200)
    g = groups[0]
    title = g.find(_L + "Title")
    parts = _lines(g)
    if not any(p["text"] for p in parts):
        raise PublisherRefused("the publisher returned a provision with no words in it", 200)
    whole = shown_text(parts)
    listed = [{k: e.attrib.get(k) for k in ("Type", "AffectedProvisions", "AffectingYear", "AffectingNumber")}
              for e in root.iter(_M + "UnappliedEffect")
              if touches(section, e.attrib.get("AffectedProvisions") or "")]
    across = sum(1 for _ in root.iter(_M + "UnappliedEffect"))
    has_table = any(True for _ in g.iter("{http://www.w3.org/1999/xhtml}table")) or any(True for _ in g.iter(_L + "Tabular"))
    return {
        "act": root.findtext(".//" + _DC + "title"),
        "heading": ("".join(title.itertext()).strip() if title is not None else None),
        "section": str(section),
        "parts": parts,
        "sha256": hashlib.sha256(whole.encode("utf-8")).hexdigest(),
        "version_dated": root.attrib.get("RestrictStartDate"),
        "extent": root.attrib.get("RestrictExtent"),
        "changes_not_yet_applied_to_this_provision": listed,
        "changes_not_yet_applied_count": len(listed),
        "changes_not_yet_applied_across_the_act": across,
        "changes_basis": ("the publisher's own list of amendments it has not yet written into this text. "
                          + ("NONE is listed for this provision." if not listed else
                             f"{len(listed)} listed for this provision: the text may not be the law as it now stands.")),
        **({"not_shown": "this provision contains a table, which this page does not show; read it at the publisher"}
           if has_table else {}),
    }


async def provision(kind: str, year: Any, number: Any, section: Any) -> Dict[str, Any]:
    """Fetch one provision now. One request, to the publisher's own host, on a person's action."""
    url = address(kind, year, number, section)
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True,
                                     headers={"User-Agent": "Workstation (one provision on a person's request)"}) as c:
            r = await c.get(url + "/data.xml")
    except httpx.HTTPError as e:
        raise PublisherRefused(f"the publisher could not be reached ({type(e).__name__})") from None
    if r.url.host not in _HOSTS:                       # a redirect must stay on the publisher's own host
        raise PublisherRefused("the request was sent somewhere other than the publisher", r.status_code)
    if r.status_code == 404:
        raise PublisherRefused("the publisher has no such provision", 404)
    if r.status_code != 200:
        raise PublisherRefused("the publisher did not return the provision", r.status_code)
    out = parse(r.text, str(section))
    out["fidelity"] = fidelity(out["parts"], out["sha256"])
    if not out["fidelity"]["matches"]:
        raise PublisherRefused("the text read does not match its own record, so it is not shown", 200)
    return {**out, "publisher": PUBLISHER, "address": url, "licence": LICENCE,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "stored": False, "composed": False, "what_this_is": WHAT_THIS_IS}
