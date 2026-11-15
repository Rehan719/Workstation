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
         "releases; an administrator records all three, so with sign-in on they wait on an administrator",
         #  W1088 (FU-1270)
         "your entities: a stage held at its review gate until you decide it, and an entity whose working name is "
         "not published until you name it",
         "your entities' service contracts: an offer to accept or decline, an accepted contract to deliver, and a "
         "delivered one to settle, each on the side that acts next; and a delivery to your entity waiting for you to "
         "accept its version",
         #  W1089 (FU-1270)
         "the reviewers' queues you are on the roster for: a composed item in scholar review and the children's "
         "approval pack, waiting on a scholar, and a GMP record waiting on a QA signatory"]
#  W1087 - the census of the stores that hold something waiting on a person found these as well; each is named until
#  the list reads it (FU-1270)
NOT_READ_YET = ["a legal artefact waiting on the Owner's approval, and an avatar mode waiting on an administrator's "
                "co-signature",
                "a support answer waiting on its asker's confirmation, and a quality defect waiting on a correction or "
                "a re-verification",
                "an evolution proposal and a proposed catalogue entry waiting on a decision",
                "a method amendment not yet carried out, a follow-up waiting on the Owner, and an immune defence "
                "waiting to be lifted"]
WHERE = {"agreement": "the agreements on the Law page", "asset": "the assets on the Law page",
         "change": "Change Control's queue", "ratification": "the Board's ratifications",
         #  W1088 (FU-1270)
         "entity": "the entity's Cockpit", "gate": "the entity's review gates on its Cockpit",
         "contract": "the service contracts on the VSB Economy page",
         "delivery": "the deliveries on the Living Organisation hub",
         #  W1089 (FU-1270)
         "review": "the scholar review panel on the Quran platform's hub",
         "pack": "the children's approval pack on the Quran platform's hub",
         "gmp": "the GMP sign-off on the Science page"}
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
         "readiness_withdrawn": 2, "unconfirmed": 3,
         "name": 1, "gate": 1, "offered": 1, "accepted": 1, "delivered": 1, "acceptance": 1,   # W1088
         "review": 1, "pack": 1, "qa": 1}   # W1089


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


def _theirs(user, owner) -> bool:
    """W1088 - whether a record owned by `owner` waits on this person: with sign-in on, it is theirs, or it is unowned and
    they are an administrator (an unowned record is an administrator's, user_can_access); with it off, every record
    is the one person's using this machine."""
    if not auth_enabled():
        return True
    me = user.get("username") if isinstance(user, dict) else None
    admin = isinstance(user, dict) and user.get("role") == "admin"
    return bool(me and owner == me) or (not owner and admin)


def _entities(user) -> tuple:
    """W1088 (FU-1270) - an entity of this person's waiting on them: a stage held at its review gate until they decide
    it (W452, Mode 3), and an entity whose working name is not published until its founder names it (W450). Every
    entity record is read here, counted when it cannot be; the owners and names read serve the contracts and the
    deliveries, whose own records name entities by id."""
    import json
    from agentic_core.api import vsb as vs
    items, unread, owners, names = [], 0, {}, {}
    for p in list(vs._VSB_STORE.glob("*.json")):
        try:
            v = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            if p.exists():
                unread += 1
            continue
        if isinstance(v, dict) and not v.get("vsb_id") and v.get("entity_id"):
            continue   # the synthesis studio keeps its own entities in this folder, by entity_id
        if not (isinstance(v, dict) and v.get("vsb_id")):
            unread += 1
            continue
        vid = str(v["vsb_id"])
        owners[vid], names[vid] = v.get("owner_id"), (v.get("name") or vid)
        if not _theirs(user, v.get("owner_id")):
            continue
        since = str(v.get("created_at") or "")
        if v.get("name_pending"):
            items.append({"source": "entity", "kind": "name", "vsb_id": vid, "what": "a name for this enterprise, from its founder",
                          "on": names[vid], "ref": None, "where": WHERE["entity"], "since": since,
                          "said": "its body is not published under a working name until it is named"})
        rg = v.get("review_gates") if isinstance(v.get("review_gates"), dict) else {}
        for st in (vs._gate_status(rg, s) for s in (rg.get("stages") or [])):
            if st.get("status") == "pending":
                items.append({"source": "entity", "kind": "gate", "vsb_id": vid,
                              "what": f"a decision at the review gate of its '{st['stage']}' stage",
                              "on": names[vid], "ref": None, "where": WHERE["gate"], "since": since,
                              "said": "the stage does not go ahead until it is decided"})
    return items, ([{"store": "entities", "said": (
        f"{unread} entity record(s) could not be read, so a decision or a name one of them waits on may not be "
        f"shown.")}] if unread else []), owners, names


_CONTRACT_WAITS = {   # status -> (whose side acts, what waits)
    "offered": ("provider_vsb", "an answer to this offer of a service contract: accept it or decline it"),
    "accepted": ("provider_vsb", "the delivery of this accepted service contract"),
    "delivered": ("client_vsb", "the settlement of this delivered service contract"),
}


def _contracts(user, owners: dict, names: dict) -> list:
    """W1088 (FU-1270) - a service contract between entities waits on the owner of the side that acts next: an offer
    on the provider's, to accept or decline; an accepted contract on the provider's, to deliver; a delivered one on the
    client's, to settle. The contract store is read strictly, and a store it cannot read is said by its caller."""
    from agentic_core.api.economy import _read_contracts
    items = []
    for c in _read_contracts():
        side = _CONTRACT_WAITS.get(c.get("status"))
        if not side:
            continue
        vid = str(c.get(side[0]) or "")
        if vid not in owners or not _theirs(user, owners[vid]):
            continue
        since = str(c.get("offered_at") or "")
        items.append({"source": "contract", "kind": c.get("status"), "contract_id": c.get("id"), "vsb_id": vid,
                      "what": side[1], "on": names.get(vid, vid),
                      "ref": f"{c.get('brief', '')[:80]}; {c.get('price_wst')} virtual WST", "where": WHERE["contract"],
                      "since": since, "said": _ago(since)})
    return items


def _deliveries(user, owners: dict, names: dict) -> tuple:
    """W1088 (FU-1270) - a cascade's delivery to an entity waits on its owner's acceptance of that version (W851): a run
    scoped to an entity, with the version it delivered, and no acceptance recorded for it. The run history is read
    tolerantly and says when it was not read whole; the acceptances are read strictly."""
    from agentic_core.config import StoreUnavailable, data_path, read_json_reported
    from agentic_core.api.swarm import _acceptances
    unread = []
    runs, why = read_json_reported(data_path("org_cascade_runs.json"), [])
    if why:
        unread.append({"store": "cascade runs", "said": (
            f"The cascade run history could not be read whole ({why}), so a delivery waiting to be accepted may not "
            f"be shown.")})
    try:
        accepted = {a.get("run_id") for a in _acceptances()}
    except StoreUnavailable as e:
        return [], unread + [{"store": "acceptances", "said": (
            f"The record of accepted deliveries could not be read ({e}), so no delivery is said to wait on you: one "
            f"may already be accepted.")}]
    items = []
    for r in runs if isinstance(runs, list) else []:
        if not isinstance(r, dict):
            continue
        vid = str(r.get("business_plan_scope") or "")
        if vid in ("", "workstation") or not r.get("delivery_sha256") or r.get("run_id") in accepted:
            continue
        if vid not in owners or not _theirs(user, owners[vid]):
            continue
        since = str(r.get("created_at") or "")
        items.append({"source": "delivery", "kind": "acceptance", "run_id": r.get("run_id"), "vsb_id": vid,
                      "what": f"an acceptance of this version of the delivery for '{str(r.get('mission') or '')[:80]}'",
                      "on": names.get(vid, vid), "ref": None, "where": WHERE["delivery"], "since": since,
                      "said": _ago(since)})
    return items, unread


def _reviewer(user, roster: dict) -> bool:
    """W1089 (FU-1270) - whether a reviewers' queue waits on this person. With sign-in on, on the account whose username
    is on the roster (a scholar decides only from their own account; a QA signatory is named on the roster), or, while
    the roster is empty, on an administrator, who adds the first; with sign-in off, on the one person using this
    machine, who enters a decision on a named reviewer's behalf."""
    if not auth_enabled():
        return True
    me = user.get("username") if isinstance(user, dict) else None
    admin = isinstance(user, dict) and user.get("role") == "admin"
    return bool(me and me in roster) or (not roster and admin)


def _reviews(user) -> tuple:
    """W1089 (FU-1270) - a composed item in the scholar review queue (in review), and the children's approval pack while
    it awaits a decision or has changed since one, wait on a scholar on the roster. The item is named by where it was
    composed and its reference, never by its text."""
    from agentic_core.config import StoreUnavailable
    from agentic_core.api import scholar_review as sr
    try:
        roster = sr.roster()
        recs = sr._load(sr._review_path())
    except StoreUnavailable as e:
        return [], [{"store": "scholar review", "said": (
            f"The scholar review queue or its roster could not be read ({e}), so an item waiting on a scholar may not "
            f"be shown.")}]
    if not _reviewer(user, roster):
        return [], []
    items, unread = [], []
    for key, r in recs.items():
        if not isinstance(r, dict) or r.get("state") != sr.IN_REVIEW:
            continue
        since = str(r.get("submitted_at") or "")
        items.append({"source": "review", "kind": "review", "content_key": key,
                      "what": "a scholar's decision on this composed item", "on": str(r.get("surface") or key),
                      "ref": r.get("reference") or None, "where": WHERE["review"], "since": since,
                      "said": (_ago(since) if roster else
                               "no scholar is on the roster, so it cannot be decided until one is added")})
    try:
        from agentic_core.religious_domain import approval_pack as ap
        pack = ap.assemble()
    except StoreUnavailable as e:
        unread.append({"store": "approval pack", "said": (
            f"The children's approval pack could not be read ({e}), so whether it waits on a scholar is not known.")})
    else:
        if pack.get("state") in ("awaiting_review", "changed_since_approval"):
            items.append({"source": "review", "kind": "pack", "pack_hash": pack.get("pack_hash"),
                          "what": "a scholar's decision on the children's approval pack, as a whole",
                          "on": "the children's approval pack", "ref": None, "where": WHERE["pack"], "since": "",
                          "said": (str(pack.get("basis") or pack.get("state")) if roster else
                                   "no scholar is on the roster, so it cannot be decided until one is added")})
    return items, unread


def _gmp(user) -> tuple:
    """W1089 (FU-1270) - a GMP record pending QA waits on a signatory on the QA roster. Records name no owner, so the
    roster is who they wait on."""
    from agentic_core.config import StoreUnavailable
    from agentic_core.science import gmp_signoff as gs
    try:
        roster, recs = gs._load("roster"), gs._load("records")
    except StoreUnavailable as e:
        return [], [{"store": "GMP records", "said": (
            f"The GMP records or their QA roster could not be read ({e}), so a record waiting on a signatory may not "
            f"be shown.")}]
    if not _reviewer(user, roster):
        return [], []
    items = []
    for rid, r in recs.items():
        if not isinstance(r, dict) or r.get("state") != gs.PENDING:
            continue
        since = str(r.get("submitted_at") or "")
        items.append({"source": "gmp", "kind": "qa", "record_id": rid, "what": "a QA signatory's sign-off",
                      "on": f"the GMP {r.get('kind') or 'record'} {rid}", "ref": None, "where": WHERE["gmp"],
                      "since": since, "said": (_ago(since) if roster else
                                               "no QA signatory is on the roster, so it cannot be signed until one is "
                                               "added")})
    return items, []


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
    #  W1088 (FU-1270) - an entity's own waits, then the contracts and deliveries that name entities by id
    got, missed, owners, names = _entities(user)
    items += got
    unread += missed
    try:
        items += _contracts(user, owners, names)
    except HTTPException as e:
        if e.status_code != 503:
            raise
        unread.append({"store": "contracts", "said": str(e.detail)})
    got, missed = _deliveries(user, owners, names)
    items += got
    unread += missed
    #  W1089 (FU-1270) - the reviewers' queues the person is on the roster for
    for read in (lambda: _reviews(user), lambda: _gmp(user)):
        got, missed = read()
        items += got
        unread += missed
    items.sort(key=lambda i: (_RANK.get(i["kind"], 9), i.get("days") if i.get("days") is not None else 0,
                              str(i.get("since") or "")))
    return {"reads": READS, "not_read_yet": NOT_READ_YET, "basis": BASIS, "date_basis": DATE_BASIS,
            "within_days": within_days, "items": items, "unread": unread,
            **({} if kept_records else {"not_kept": NOT_KEPT}),
            **({} if items else {"said": NOTHING_READ if unread else NOTHING})}
