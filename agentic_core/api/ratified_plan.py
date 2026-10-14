"""THE OWNER'S RATIFIED BUSINESS PLAN, READ FOR ENTRY INTO THE PRODUCT'S OWN PLAN (W726).

Pure functions: the document is read and what WOULD be entered is returned; nothing is written here.
The text entered is the document's own - sections unwrapped, tags kept - and never reworded. The plan's
routes decide who may enter it and record that it was entered from the ratified document by one action
of the Owner's, not typed field by field (Owner ruling 2026-10-14).
"""
import hashlib
import pathlib
import re
from typing import Any, Dict, List

DOCUMENT = "docs/business/BUSINESS_PLAN.md"
#  product field -> the document's heading
FIELDS = (("executive_summary", "Executive summary"), ("concept", "Concept"), ("vision", "Vision"),
          ("mission", "Mission"), ("strategy", "Strategy"))
NOT_ENTERED = ("Roadmap", "Operating model", "Costs", "Risks", "What must be true before launch")
CANVAS_NOTE = ("the business model canvas is not entered: the product's plan has no place for it, and it "
               "stays the ratified document docs/business/BUSINESS_MODEL_CANVAS.md")


def _sections(text: str) -> Dict[str, str]:
    parts = re.split(r"(?m)^## (.+?)\s*$", text)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def _bullets(body: str) -> List[str]:
    """Each top-level bullet as one string, its wrapped lines joined; the words are the document's."""
    out, cur = [], None
    for line in body.splitlines():
        if line.startswith("- "):
            if cur is not None:
                out.append(cur)
            cur = line[2:].strip()
        elif cur is not None and line.startswith("  ") and line.strip():
            cur += " " + line.strip()
        elif cur is not None and not line.strip():
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return out


def _prose(body: str) -> str:
    """A section as text: paragraphs and list items unwrapped, one per line, nothing reworded."""
    lines, cur = [], ""
    for line in body.splitlines():
        s = line.strip()
        starts = bool(re.match(r"(- |\d+\. )", s))
        if not s:
            if cur:
                lines.append(cur)
            cur = ""
        elif starts:
            if cur:
                lines.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def preview(root: pathlib.Path) -> Dict[str, Any]:
    raw = (root / DOCUMENT).read_bytes()
    text = raw.decode("utf-8").replace("\r\n", "\n")
    opening = " ".join(text.split("\n## ", 1)[0].split())
    m = re.search(r"\*\*Ratified by the Owner on (20\d\d-\d\d-\d\d)\*\*", opening)
    draft = "DRAFT until the Owner ratifies it" in opening
    secs = _sections(text)
    missing = [h for _f, h in FIELDS if not secs.get(h)] + [h for h in ("Aims", "Objectives") if not secs.get(h)]
    objectives = []
    for ln in secs.get("Objectives", "").splitlines():
        if ln.startswith("| ") and "---" not in ln and "Plan item" not in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 3:
                #  READ 2026-10-14: the plan's release gate counts any non-empty `kpi` as a measure that is
                #  set. A cell that SAYS "NOT MEASURED" must therefore not be entered as one: the measure is
                #  left empty and the document's own words travel beside it.
                unmeasured = cells[2].upper().startswith("NOT MEASURED")
                objectives.append({"title": cells[0], "plan_item": cells[1], "kpi": "" if unmeasured else cells[2],
                                   "measure_as_ratified": cells[2],
                                   "timeline": "in rounds; no date is promised", "owner_role": "the Owner",
                                   "source": "ratified document"})
    changed = re.search(r"Changed once since, with the Owner's word, on (20\d\d-\d\d-\d\d): ([^.]+)\.", opening)
    return {
        "document": DOCUMENT, "sha256": hashlib.sha256(raw).hexdigest(),
        "ratified_on": (m.group(1) if m and not draft else None),
        "changed_since": ({"on": changed.group(1), "what": changed.group(2)} if changed else None),
        "fields": {f: _prose(secs.get(h, "")) for f, h in FIELDS},
        "aims": _bullets(secs.get("Aims", "")),
        "objectives": objectives,
        "not_entered": [h for h in NOT_ENTERED if h in secs],
        "canvas": CANVAS_NOTE,
        "document_faults": ([f"the document has no section headed '{h}'" for h in missing]
                            + ([] if (m and not draft) else ["the document does not open by saying it is ratified, with a date"])),
    }
