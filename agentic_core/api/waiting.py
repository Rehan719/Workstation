"""P5.14 clause 4 and P5.18 clause 3 (W1085, W1087) - THE ONE LIST OF WHAT WAITS ON A PERSON.

One list, reached from the first screen, of what waits on the person asking, read from the stores that exist:
- the obligations on their agreement records (W1085): each one falling due within the window or past its date, and
  each one no person has confirmed;
- their projects (W867): each proposal to move one to another stage, which waits on their decision;
- their asset records (W1082): a fact whose evidence lapses within the window, a fact whose evidence has lapsed with
  nothing current in its place, and a declaration of readiness withdrawn because what it rests on lapsed;
- Change Control: each change waiting on a decision, each a review approved that waits for the Board's ratification,
  and each material economy action a review approved, which only the Owner's own decision releases. An administrator
  records all three, so they wait on an administrator; with sign-in off, on the one person using this machine.
The census of the stores that hold something waiting on a person (W1087) found more; each is named as not read yet
until the list reads it (FU-1270).
The agreement and asset records are kept only for a signed-in person (the Owner's ruling of 2026-10-12), so with
sign-in off the list says so and reads the rest. A store it cannot read is said in its place, with why, and the rest
of the list still stands. What it does not read yet is named, so an empty list is never taken for nothing waiting
anywhere. A date on it is a record's own; none is computed here and none is taken from a model."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from agentic_core.auth.core import auth_enabled, get_current_user

router = APIRouter(prefix="/api/v1/waiting", tags=["waiting"])

READS = ["the obligations on your agreement records: each one falling due within the window or past its date, and "
         "each one no person has confirmed",
         "your projects: each proposal to move one to another stage, which waits on your decision",
         "your asset records: a fact whose evidence lapses within the window, a fact whose evidence has lapsed with "
         "nothing current in its place, and a declaration of readiness withdrawn because what it rests on lapsed",
         "Change Control: each change waiting on a decision, each a review approved that waits for the Board's "
         "ratification, and each material economy action a review approved, which only the Owner's own decision "
         "releases; an administrator records all three, so with sign-in on they wait on an administrator"]
#  W1087 - the census of the stores that hold something waiting on a person found these as well; each is named until
#  the list reads it (FU-1270)
NOT_READ_YET = ["an entity's review gate waiting on its owner's decision, and an entity waiting to be named",
                "a service contract waiting on its provider or its client, and a delivery waiting to be accepted",
                "the scholar review queue, the children's approval pack, and a GMP record waiting on a signatory",
                "a legal artefact waiting on the Owner's approval, and an avatar mode waiting on an administrator's "
                "co-signature",
                "a support answer waiting on its asker's confirmation, and a quality defect waiting on a correction or "
                "a re-verification",
                "an evolution proposal and a proposed catalogue entry waiting on a decision",
                "a method amendment not yet carried out, a follow-up waiting on the Owner, and an immune defence "
                "waiting to be lifted"]
WHERE = {"agreement": "the agreements on the Law page", "asset": "the assets on the Law page",
         "change": "Change Control's queue", "ratification": "the Board's ratifications"}
NOT_KEPT = ("Your agreement and asset records are kept only once you are signed in, and sign-in is off, so nothing "
            "of theirs is on this list.")
BASIS = ("One list of what waits on you, from the records it reads; a record it could not read is said with why, and "
         "what it does not read yet is named, so an empty list says only that nothing it reads is waiting.")
DATE_BASIS = ("Each date here is a record's own: an obligation's date and when a piece of evidence lapses are a "
              "person's entries, and a proposal or a change is dated when it was raised. None is computed by this "
              "platform, and none is taken from a model.")
NOTHING = "Nothing that this list reads is waiting on you."
NOTHING_READ = ("Nothing in what this list could read is waiting on you; what it could not read is said with it, so "
                "this is not a list of none.")
#  soonest first: what has a date (falling due, lapsing, lapsed), then decisions, oldest first, then the rest
_RANK = {"falls_due": 0, "evidence_lapses": 0, "evidence_lapsed": 0, "decision": 1, "ratification": 1,
         "readiness_withdrawn": 2, "unconfirmed": 3}


def _iso(ts) -> str:
    return datetime.fromtimestamp(float(ts), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ago(iso: str) -> str:
    try:
        days = (datetime.now(timezone.utc).date() - datetime.fromisoformat(str(iso).replace("Z", "+00:00")).date()).days
    except ValueError:
        return "raised on a date its record does not say"
    return "raised today" if days <= 0 else f"raised {days} day{'s' if days != 1 else ''} ago"


def _decider(user) -> bool:
    """Whether Change Control's decisions are this person's to record: with sign-in on, an administrator's."""
    return not auth_enabled() or (isinstance(user, dict) and user.get("role") == "admin")


def _agreements(user, within_days: int) -> list:
    from agentic_core.api.agreements import falling_due
    return [{**i, "source": "agreement", "on": i.get("agreement_title"), "ref": i.get("clause"),
             "where": WHERE["agreement"]} for i in falling_due(user, within_days)["items"]]


def _assets(user, within_days: int) -> list:
    from agentic_core.api.assets import lapsing
    return [{**i, "source": "asset", "where": WHERE["asset"]} for i in lapsing(user, within_days)["items"]]


def _projects(user) -> tuple:
    """A pending proposal on a project of this person's waits on their decision (the project's owner decides it, W883).
    With sign-in on, an unowned project is an administrator's; with it off, every project is the one person's."""
    from agentic_core.projects import api as pj
    projects, unread_projects = pj._projects_read()
    read = pj._proposals_read()
    me = user.get("username") if isinstance(user, dict) else None
    admin = isinstance(user, dict) and user.get("role") == "admin"
    items = []
    for p in projects:
        if auth_enabled() and not (me and p.owner_id == me or (not p.owner_id and admin)):
            continue
        w = pj._waiting_on_person(p, read)
        for on in w.get("on") or []:
            since = _iso(on["since"])
            items.append({"source": "project", "kind": "decision", "project_id": p.id, "proposal_id": on["proposal_id"],
                          "what": on["what"], "on": p.title, "ref": None, "where": w.get("where"), "since": since,
                          "said": _ago(since)})
    unread = []
    if unread_projects:
        unread.append({"store": "projects", "said": (
            f"{unread_projects} project record(s) could not be read, so a decision on one of them that waits on you "
            f"is not shown.")})
    if read[1]:
        unread.append({"store": "proposals", "said": (
            f"{read[1]} proposal record(s) could not be read, so a decision that waits on you may not be shown.")})
    return items, unread


def _changes(user) -> tuple:
    """Change Control's queue and the Board's ratifications, for the person who records their decisions. Every record
    is read through Change Control's own loader; one it could not read is counted and said."""
    if not _decider(user):
        return [], []
    from agentic_core.api import change_control as cc
    from agentic_core.economy.governance import _owner_decided
    items, unread = [], 0
    for p in list(cc._CCA_STORE.glob("*.json")):
        c = cc._load_change(p.stem)
        if c is None:
            if p.exists():
                unread += 1
            continue
        if c.get("status") in ("submitted", "under_review"):
            kind, what, where = "decision", "a decision on this change", WHERE["change"]
        elif cc.awaiting_board_ratification(c):
            kind, what, where = ("ratification", "the Board's ratification of this change, on the Owner's direction",
                                 WHERE["ratification"])
        elif (c.get("status") == "approved" and c.get("change_type") == "economy_material"
              and not _owner_decided(c)):
            #  a material economy action is released only by the Owner's explicit decision (W464): an approval
            #  recorded any other way releases nothing, so it still waits
            kind, what, where = ("decision", "the Owner's own decision on this change: a review's approval of a "
                                             "material economy action releases nothing", WHERE["change"])
        else:
            continue
        since = str(c.get("submitted_at") or "")
        items.append({"source": "change", "kind": kind, "cca_id": c.get("cca_id"), "what": what,
                      "on": c.get("title") or c.get("cca_id"), "ref": f"tier {cc.effective_tier(c)}", "where": where,
                      "since": since, "said": _ago(since)})
    return items, ([{"store": "changes", "said": (
        f"{unread} Change Control record(s) could not be read, so a change waiting on a decision may not be shown.")}]
        if unread else [])


@router.get("")
async def what_waits(within_days: int = 30, user: dict | None = Depends(get_current_user)):
    """What waits on this person, from the records the list reads, soonest first; each store it could not read, with
    why; and what it does not read yet."""
    if not 0 <= within_days <= 365:
        raise HTTPException(status_code=400, detail=(
            f"The window is a number of days from 0 to 365; {within_days} is not one, so nothing was read."))
    if user is not None and not isinstance(user, dict):
        user = None
    items, unread = [], []
    #  each store on its own: one that cannot be read is said in its place, and the others still stand
    kept_records = auth_enabled()
    for store, read in ((("agreements", lambda: _agreements(user, within_days)),
                         ("assets", lambda: _assets(user, within_days))) if kept_records else ()):
        try:
            items += read()
        except HTTPException as e:
            if e.status_code != 503:
                raise
            unread.append({"store": store, "said": str(e.detail)})
    for read in (lambda: _projects(user), lambda: _changes(user)):
        got, missed = read()
        items += got
        unread += missed
    items.sort(key=lambda i: (_RANK.get(i["kind"], 9), i.get("days") if i.get("days") is not None else 0,
                              str(i.get("since") or "")))
    return {"reads": READS, "not_read_yet": NOT_READ_YET, "basis": BASIS, "date_basis": DATE_BASIS,
            "within_days": within_days, "items": items, "unread": unread,
            **({} if kept_records else {"not_kept": NOT_KEPT}),
            **({} if items else {"said": NOTHING_READ if unread else NOTHING})}
