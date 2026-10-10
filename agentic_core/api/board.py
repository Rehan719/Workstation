"""
Board of Directors — the apex governance tier of the Workstation IDBO / VSB.

Sits ABOVE the AI CEO (honouring the Arms-Length Agency invariant: the AI CEO
cannot instruct the board — direction flows down, not up). The board is led by
the **Chief** — the Owner's digital twin AS A ROLE (W492: no twin MODEL is trained; Mode 2
is planned, P3.4 — the Chief is a standing charter plus the Owner's recorded instructions,
and it represents only what the Owner has actually stated) — who represents the Owner faithfully
in their presence and absence, with diligence, honesty, loyalty, determination
and perfectionism. The Chief leads/appraises/develops a swarm of specialist
Directors who together own the Business plan, strategy, aims, mission and
objectives, and delegate a timelined/resourced/scheduled living action plan to
the AI CEO (→ C-Suite → CoE → BTO → operational delivery).

Every VSB IDBO entity generated for a user receives its own Board + a Chief that
holds the standing charter of *that* VSB's owner (again: a role, not a trained model).

  GET  /api/v1/board/status           — board composition, hierarchy, owner it represents
  GET  /api/v1/board/charter          — the board charter + arms-length governance model
  POST /api/v1/board/chief/instruct   — Owner instructs their Chief twin → board directive → AI CEO action plan
  POST /api/v1/board/directive        — the board issues a directive on a topic (directors weigh in)
  GET  /api/v1/board/ratifications    — W464: HIGH changes a review approved, waiting for the Board to ratify them
  POST /api/v1/board/ratifications/{cca_id} — W464: record the Board's decision (ratify | refuse) on the Owner's
                                        direction (admin only with auth on; on_owner_direction: true in both modes)
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.api._strict_models import STRICT

from agentic_core.auth.core import auth_enabled, get_current_user, request_owner_id

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/board", tags=["board-of-directors"])

_STORE = data_path("board_directives.json")

# The Owner this top-level board represents. (Per-VSB boards carry their own owner.)
_OWNER = {
    "name": "Rehan",
    "role": "Founder / Owner / Curator",
    "vision_summary": (
        "Workstation IDBO AI-mediates working for any user in any realm/domain — taking a "
        "challenge end-to-end (Concept → Design → Delivery) and generating a bespoke, living "
        "Enterprise IDBO (a VSB) that commercialises the user's solution. One self-running, "
        "self-healing, self-improving living organism."
    ),
    "fidelity_charter": (
        "Represent the Owner precisely, effectively, efficiently, systematically and punctually — "
        "reflecting their exact wishes and instructions, perfectly understood and remembered, with "
        "due diligence, honesty, sincerity, loyalty, determination, resilience and perfectionism."
    ),
}

# The Board roster. The Chief is the Owner's digital twin; directors own areas of direction.
_BOARD: List[Dict[str, str]] = [
    {"id": "chief", "title": "Chief of the Board (the Owner's charter and instructions — no twin model is trained)",
     "mandate": "Represent the Owner; set direction; lead/appraise/develop the board; delegate to the AI CEO."},
    {"id": "dir_strategy", "title": "Director of Strategy & Vision",
     "mandate": "Business plan, strategy, aims, mission, objectives — coherence with the Owner's vision."},
    {"id": "dir_technology", "title": "Director of Technology & Architecture",
     "mandate": "Technical direction, architecture integrity, build quality, scalability."},
    {"id": "dir_governance", "title": "Director of Governance & Compliance",
     "mandate": "Constitutional alignment, gaas.v5 gate, risk, change control, audit integrity."},
    {"id": "dir_biomimetic", "title": "Director of Biomimetic Systems",
     "mandate": "Highest authority to monitor/change/control all VSB living processes (immune/nervous/genome/evolution)."},
    {"id": "dir_operations", "title": "Director of Operations & Delivery",
     "mandate": "BTO, Build-to-Order, facilities management, operational delivery to timeline."},
    {"id": "dir_finance", "title": "Director of Finance & Capital",
     "mandate": "Capital allocation, unit economics, commercial sustainability."},
    {"id": "dir_evolution", "title": "Director of Evolution & Learning",
     "mandate": "Continual self-improvement; ties the Sovereign Evolution Office to board direction."},
]


def _load() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


#  W637 — the sentence lives beside the computation it describes (organism/immune.py); this name is kept
#  for its reader below.
from agentic_core.organism.immune import HEALTH_SCOPE as _ORGANISM_HEALTH_SCOPE  # noqa: E402


def _load_strict() -> List[Dict[str, Any]]:
    """W624 (FU-524, M1 v9 R3.1) — the board store read WHOLE or refused. `_load` answers a corrupt store with [],
    which is right for a reader that only displays, and wrong for two kinds of caller: the founder model, which
    then reported a corrupt store as "no instruction written", and every WRITER, which appended to that [] and
    atomically replaced the Owner's whole directive history with one row. Those use this."""
    from agentic_core.config import read_json_strict
    return read_json_strict(_STORE, list, expect=list)


def _load_for_write() -> List[Dict[str, Any]]:
    from agentic_core.config import StoreUnavailable
    try:
        return _load_strict()
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=(
            f"the board store could not be read whole ({e}), so nothing was written: appending to an empty read "
            f"would replace every directive on record with this one"))


def _save(rows: List[Dict[str, Any]]) -> None:
    from agentic_core.config import atomic_write_json
    atomic_write_json(_STORE, rows)


async def _q(prompt: str, agent: str, provenance: Dict[str, Any] | None = None) -> str:
    """§6 (W270) — the APEX tier runs on the same in-house-first fabric as every lower tier:
    query_meta with owned-resource provenance recorded per call (the Board was previously the only
    AI-driven governance tier without served_by/any_external)."""
    _t0 = time.time()
    try:
        # W488 (sweep S2.3, C5) — augment=False. Without it the gateway injects cross-request memory
        # recall into the prompt, so the Chief's directive — presented as 'Faithfully interpreted →
        # board directive' — could carry another request's content as the Owner's intent. The apex tier
        # reads the Owner's words and nothing else.
        #   The first cut of this comment ended "every other generation surface already does this" — a
        # claim the repo did not back: a refutation found eleven callers still on recall, including the
        # SAME Chief twin in business_plan.py and the org cascade's apex in swarm.py, both of which
        # PERSIST their output. W488 closed all of them; the deliberate exceptions are the avatar
        # conversation (avatars/api.py) and the AI-CEO chat (api/v138/ceo.py) — both conversations,
        # both keeping tenant-scoped recall, both saying why in place.
        res = await gateway.query_meta(prompt, agent=agent, augment=False)
        if provenance is not None:
            sb = res.get("served_by", "native")
            provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
            provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
        # §5×§6 (W275) — the APEX accrues real operational rows like every lower tier (it was the
        # only AI-driven tier invisible to the learning loop and the measured-outcomes blocks).
        try:
            from agentic_core.api.operational_excellence import record_outcome
            record_outcome("ai_call", f"agent:{agent}", served_by=res.get("served_by", "native"),
                           is_external=bool(res.get("is_external")),
                           duration_ms=int((time.time() - _t0) * 1000),
                           # W495 (FU-125, S7.3) — no gate assesses a board directive, so the run is
                           # recorded as having produced output, with no verdict claimed
                           success=bool((res.get("output") or "").strip()),
                           quality_gate=None)
        except Exception:
            pass
        return res.get("output", "")
    except Exception as e:
        try:
            from agentic_core.api.operational_excellence import record_outcome
            record_outcome("ai_call", f"agent:{agent}", served_by="none", is_external=False,
                           duration_ms=int((time.time() - _t0) * 1000), success=False)
        except Exception:
            pass
        return f"[{agent} unavailable: {e}]"


#  P3.4 (W587) — the standing canon, named once. It is the PLATFORM's, shared by every Chief, and not
#  something an Owner wrote into a store: `founder_model()` labels it accordingly rather than letting a
#  constant read as this Owner's declaration.
_STANDING_CANON = ("Standing values from the Owner's documented canon: faith-rooted halal ethics and "
                   "beneficence · honesty over polish (never fabricate, never pad) · decide-and-build · "
                   "real user enablement · virtual/simulated finance only (real rails stay Owner-gated).")


def _owner_decisions(limit: int = 5) -> List[Dict[str, Any]]:
    """The Owner's own recorded DECISIONS — the Board ratifications, read from Change Control.

    P3.4 clause (1) names decisions as one of the three inputs a founder model is built from, and nothing
    read them before. A ratification is the Owner's direction recorded by the Board (W464), so it is the
    one place this platform holds a decision the Owner actually made rather than inferred.

    Never raises into a model build: a store that cannot be read yields NO decisions, and the count then
    says zero — which the caller reports as "none read" rather than as "none made".
    """
    out: List[Dict[str, Any]] = []
    try:
        from agentic_core.api import change_control as _cca
        for _p in sorted(_cca._CCA_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            c = _cca._load_change(_p.stem)
            if not c:
                continue
            d = _cca._ratification_decision(c)
            if not d:
                continue
            r = c.get("board_ratification") or {}
            out.append({"cca_id": c.get("cca_id"), "decision": d,
                        "title": str(c.get("title") or "")[:120],
                        "at": r.get("at") or r.get("decided_at"),
                        "notes": str(r.get("notes") or "")[:160]})
            if len(out) >= max(0, int(limit)):
                break
    except Exception:
        return out
    return out


def founder_model(scope: "str | None" = None, owner: "str | None" = None) -> Dict[str, Any]:
    """The Chief's founder model as a STRUCTURE: three inputs, each counted and each naming its source.

    P3.4 clause (1). A Chief with NO instructions and NO decisions is reported as a ROLE and not as a
    modelled twin — which is the distinction W492 forced onto the fidelity ledger and which the previous
    string could not make, because its values line was an unconditional constant and so every Chief read
    as "the Owner's lived record".

    THE PROFILE IS LABELLED, NOT COUNTED AS A DECLARATION. The canon is the platform's and is identical
    for every Chief, so `declared_by_owner` is False: a constant shared by everyone is not this Owner's
    own statement, which is the same reading W585 applied to a VSB's values. Only instructions and
    decisions — things the Owner actually wrote or decided — make a model a twin.
    """
    instructions: List[Dict[str, Any]] = []
    instructions_readable = True
    n_i_all: "int | None" = None
    try:
        #  ONLY THE OWNER'S OWN WORDS. A directive the twin issued unprompted carries an `instruction`
        #  too - its restatement of what the Owner last asked for - and counting that as a new input
        #  would make the model read its own output back as its principal's record: the count would rise
        #  without the Owner saying anything, and the beat's idempotence would never hold. A row with no
        #  marker predates the unprompted path and IS the Owner's.
        #  W624 (FU-524) — THE COUNT IS EVERY INSTRUCTION, the recent list is the last five. The count was taken
        #  from the five-row display slice, so it could never exceed 5; it ignored scope and owner, so one
        #  entity's Chief counted every entity's instructions; and the read swallowed a corrupt store as [].
        _own = [x for x in _load_strict()
                if x.get("instruction") and not x.get("unprompted")
                #  W645 (FU-636) - a row with NO scope predates scoping and is the apex plan's: it used to
                #  match no scope at all, so once the twin read its model per scope those rows would have
                #  belonged to nobody
                and (scope is None or (x.get("business_plan_scope") or "workstation") == scope)
                and (owner is None or x.get("owner") == owner)]
        n_i_all = len(_own)
        for r in _own[-5:]:
            instructions.append({"at": str(r.get("created_at") or "")[:19],
                                 "instruction": str(r.get("instruction"))[:200]})
    except Exception:
        instructions_readable = False
    decisions = _owner_decisions()
    n_i, n_d = (n_i_all or 0), len(decisions)
    is_twin = (n_i + n_d) > 0

    return {
        "profile": {
            "text": _STANDING_CANON,
            "source": "the platform's standing canon, identical for every Chief",
            #  NOT this Owner's declaration: a shared constant cannot be one
            "declared_by_owner": False,
        },
        "instructions": {"count": (n_i_all if instructions_readable else None), "recent": instructions,
                         "scope": scope, "owner": owner,
                         "source": ("the board store's instruction rows"
                                    + (f" for scope {scope!r}" if scope else " across every scope")
                                    + (f" and owner {owner!r}" if owner else "")),
                         "readable": instructions_readable},
        "decisions": {"count": n_d, "recent": decisions,
                      "source": "the Owner's ratify/refuse decisions recorded by the Board in Change Control"},
        "owner_inputs": n_i + n_d,
        "is_modelled_twin": is_twin,
        #  W635 (FU-583) - nothing is fitted or evaluated, so the word 'modelled' is not used: the Chief CARRIES
        #  what the Owner wrote (is_modelled_twin keeps its name for callers; its meaning is 'has an Owner record')
        "reported_as": "chief carrying your record" if is_twin else "role",
        "basis": (
            (f"CARRYING YOUR RECORD, NOT A FITTED MODEL: {n_i} instruction(s) the Owner wrote and {n_d} decision(s) "
             f"the Owner made are handed to the Chief's prompt; nothing is trained, fitted or evaluated on them. The standing canon is also carried and is the PLATFORM's, identical for every "
             f"Chief - it is not counted as this Owner's own declaration."
             if is_twin else
             "A ROLE, NOT A MODELLED TWIN: this Owner has written no instruction and made no recorded "
             "decision, so there is nothing of theirs to model. The standing canon is carried and is the "
             "platform's, identical for every Chief, so it cannot stand in for a lived record - a Chief "
             "built from it alone represents the platform's values and not this person.")
            + ("" if instructions_readable else
               " NOTE: the board store could not be read, so the instruction count is what was READ and "
               "not necessarily what exists.")),
    }


def founder_profile() -> str:
    """§5 (W281) — the Chief's grounding text, DERIVED from `founder_model()` (P3.4, W587).

    This used to open "FOUNDER MODEL (the Owner's lived record — reason AS this person)" unconditionally,
    because the values line above it is a constant: an Owner who had written nothing still got a header
    claiming a lived record. The header now follows the model's own verdict, so a ROLE says it is a role.

    The signature and return type are UNCHANGED on purpose: board.py, business_plan.py and swarm.py all
    call this, and changing what it returns would break them. Only its content moved.
    """
    m = founder_model()
    head = ("FOUNDER MODEL (the Owner's lived record — reason AS this person)"
            if m["is_modelled_twin"] else
            "CHIEF AS A ROLE (no lived record of this Owner exists — represent the platform's standing "
            "values only, and say so when a question needs this Owner's own view)")
    out = f"\n{head}:\n{m['profile']['text']}\n"
    if m["instructions"]["count"]:
        hist = "\n".join(f"- ({str(i.get('at') or '?')[:10]}) {i.get('instruction')}"
                          for i in m["instructions"]["recent"])
        out += f"The Owner's recent instructions (remember them; stay consistent):\n{hist}\n"
    if m["decisions"]["count"]:
        dec = "\n".join(f"- ({str(d.get('at') or '?')[:10]}) {d.get('decision')}: {d.get('title')}"
                         for d in m["decisions"]["recent"])
        out += f"The Owner's recorded decisions (ratified or refused - stay consistent):\n{dec}\n"
    out += f"BASIS: {m['basis']}\n"
    return out


def _live_intelligence(scope: str) -> str:
    """LIVE intelligence for the Chief's directive (W270): the scoped plan's real progress, the
    recent operational success rate, and the prior directives — so the apex instructs from today's
    measured state, not just the static charter. Every figure read from the system that measured it."""
    lines: List[str] = []
    try:
        from agentic_core.api.business_plan import _load as _bp_load
        objs = (_bp_load(scope) or {}).get("objectives", [])
        if objs:
            by = {}
            for o in objs:
                by[o.get("status", "?")] = by.get(o.get("status", "?"), 0) + 1
            lines.append(f"- Living plan ({scope}): {len(objs)} objectives — " +
                         ", ".join(f"{k}: {v}" for k, v in sorted(by.items())))
    except Exception:
        pass
    try:
        from agentic_core.api.operational_excellence import _load as _ops_load
        rows = _ops_load()[-50:]
        if rows:
            ok = sum(1 for r in rows if r.get("success"))
            lines.append(f"- Recent operations: {len(rows)} runs, success rate {round(ok / len(rows), 2)}")
    except Exception:
        pass
    try:
        prior = _load()[-2:]
        for p in prior:
            lines.append(f"- Prior directive {p.get('directive_id', p.get('topic', '?'))}: "
                         f"{str(p.get('instruction') or p.get('topic') or '')[:100]}")
    except Exception:
        pass
    if not lines:
        return ""
    return "\n\nLIVE INTELLIGENCE (today's measured state — ground your directive in it):\n" + "\n".join(lines)


#  P3.11 clause (4) — A.8's EIGHT-POINTED STAR, as the Religion-domain EXECUTIVE tier.
#  Transliterations and division names are A.8's own; the mandates describe what the division OWNS and
#  deliberately claim no authority from the Name. A division called Knowledge does not make its output
#  authoritative — it names who owns the area, and §11 plus the R7 scholar gate still govern what a learner
#  reads. Recording that here rather than leaving it to be inferred is the point.
EIGHT_ATTRIBUTE_BOARD: List[Dict[str, str]] = [
    {"id": "exec_majesty", "attribute": "Al-ʿAzīz", "division": "Majesty",
     "mandate": "Institutional standing and stewardship: the platform's integrity as an endowment."},
    {"id": "exec_beauty", "attribute": "Al-Wadūd", "division": "Beauty",
     "mandate": "The learner's experience — that studying here is a thing done with care, not processed."},
    {"id": "exec_knowledge", "attribute": "Al-ʿAlīm", "division": "Knowledge",
     "mandate": "Curriculum and scholarship liaison. Owns the AREA; rules on nothing — a named human "
                "scholar approves religious teaching content before a learner sees it (A.12.3 / R7)."},
    {"id": "exec_creation", "attribute": "Al-Khāliq", "division": "Creation",
     "mandate": "Building what is taught with: tooling, surfaces, and the owned fabric that serves them."},
    {"id": "exec_justice", "attribute": "Al-ʿAdl", "division": "Justice",
     "mandate": "Fairness of access and of the finances: free at the point of use, the surplus cap, and "
                "who is charged what."},
    {"id": "exec_forgiveness", "attribute": "Al-Ghaffār", "division": "Forgiveness",
     "mandate": "How the platform treats failure — a learner who lapses, a mistake in a record, a wrong "
                "figure disclosed rather than quietly corrected."},
    {"id": "exec_transcendence", "attribute": "Al-Aḥad", "division": "Transcendence",
     "mandate": "The boundaries: what this platform will NOT do, including the six §11 refusals and the "
                "Fitrah Spectrum deferral, which no round may schedule."},
    {"id": "exec_guidance", "attribute": "Al-Hādī", "division": "Guidance",
     "mandate": "Direction and sequencing — where the platform goes next, and saying plainly when it does "
                "not know."},
]

EIGHT_ATTRIBUTE_BASIS = (
    "vision A.8's eight-pointed star of Divine Attributes, each attribute leading a division. The names are "
    "the Owner's own design and are used here as DIVISION TITLES: they identify who owns an area and confer "
    "no authority on anything a division produces. Nothing composed by a division carries divine sanction, "
    "§11's boundaries are unchanged, and religious teaching content still requires a named human scholar's "
    "approval before a learner sees it. This tier sits BESIDE the standing board rather than replacing it — "
    "A.8 lists it as an EXECUTIVE board, separately from the Waqf/Trust dual body and separately from "
    "oversight (Board of Trustees, Sharia Supervisory Council, the four steering committees).")


def board_for_owner(owner_name: str, vision_summary: str = "", domain: str = "") -> Dict[str, Any]:
    """Compose a Board (with a Chief = digital twin of the given owner) for a VSB entity.

    P3.11 clause (4) — `domain` is ADDED with an empty default, so every existing caller is unchanged and
    only a caller that names a domain gets the extra tier. A Religion-domain entity additionally carries
    A.8's eight-attribute EXECUTIVE board; the standing chief and directors are untouched, because A.8 lists
    the eight separately from oversight and a replacement would delete the governance tier other callers
    depend on.
    """
    _executive = (
        {"executive_board": [dict(x) for x in EIGHT_ATTRIBUTE_BOARD],
         "executive_board_basis": EIGHT_ATTRIBUTE_BASIS,
         "executive_board_source": "vision A.8 (Owner-authored)"}
        if str(domain or "").strip().lower() in ("religion", "religious") else
        #  ABSENT rather than empty for every other domain: an empty list would read as "this domain has an
        #  executive board with nobody on it", which is a different and false statement.
        {})
    return {
        **_executive,
        "owner": owner_name,
        "chief": {
            # W475 (ledger v4 R3.4) — no twin model is trained (/api/v1/twin/models holds none): the Chief is the
            # founder's standing charter and last instructions on the owned fabric, and is titled so.
            # P3.4 (W587) — "Mode 2 planned" is gone because Mode 2 is DELIVERED: the Chief is now built
            # from the Owner's recorded instructions and decisions, and reports itself a ROLE when there
            # are none (see founder_model). "No twin model is trained" STAYS, because it is still true and
            # is exactly the distinction clause (1) turns on: a model assembled from a record is not a
            # trained one.
            "title": (f"Chief of the Board — {owner_name if owner_name and owner_name != 'default' else 'the founder'}'s "
                      "standing charter, instructions and recorded decisions on the owned fabric (no twin "
                      "model is trained; the Chief reports whether it is a modelled twin or a role)"),
            "fidelity_charter": _OWNER["fidelity_charter"],
        },
        "directors": [d for d in _BOARD if d["id"] != "chief"],
        "governance": "arms-length: AI CEO cannot instruct the board; board directs the AI CEO",
        "vision_summary": vision_summary or _OWNER["vision_summary"],
    }


@router.get("/status")
async def board_status(scope: str = "workstation"):
    """§14 (W300) — the apex-governance READ side is scope-aware: scope='workstation' returns the
    platform apex board (unchanged); scope=<vsb_id> returns THAT entity's own board (from its
    entity record — every generated VSB carries one, §3.3) + the directives issued to its scope.
    Honest 404 when the VSB doesn't exist or carries no board."""
    snapshot: Dict[str, Any] = {}
    try:
        from agentic_core.organism.immune import immune
        snapshot["organism_health"] = immune.status().get("health")
        snapshot["organism_health_basis"] = _ORGANISM_HEALTH_SCOPE      # W635 (FU-587)
    except Exception:
        pass
    if scope != "workstation":
        from agentic_core.api.vsb import _load_vsb
        vsb = _load_vsb(scope)
        board = (vsb or {}).get("board")
        if not vsb or not board:
            raise HTTPException(status_code=404, detail=f"No board found for VSB {scope}.")
        return {
            "board": f"{vsb.get('name', scope)} — Board of Directors",
            "scope": scope,
            "represents_owner": vsb.get("owner_id") or board.get("chief", {}).get("represents") or "the founder",
            "hierarchy": ["Founder", "Chief (the founder's charter)", "Board of Directors",
                          "AI CEO", "C-Suite", "CoE", "BTO", "Operational Delivery"],
            "chief": board.get("chief"),
            "directors": board.get("directors", []),
            "live": snapshot,
            "recent_directives": [r for r in _load() if r.get("business_plan_scope") == scope][-5:],
        }
    return {
        "board": "Workstation IDBO Board of Directors",
        "scope": "workstation",
        "represents_owner": _OWNER["name"],
        "hierarchy": ["Owner", "Chief (the Owner's charter)", "Board of Directors",
                      "AI CEO", "C-Suite", "CoE", "BTO", "Operational Delivery"],
        "chief": _BOARD[0],
        "directors": [d for d in _BOARD if d["id"] != "chief"],
        "live": snapshot,
        "recent_directives": _load()[-5:],
        # W464 (FU-012) — how many changes wait for the Board (the queue itself: GET /ratifications)
        "pending_ratifications": _pending_ratification_count(),
    }


def _pending_ratification_count() -> Optional[int]:
    try:
        from agentic_core.api.change_control import pending_ratifications as _pr
        return len(_pr())
    except Exception:
        return None


async def twin_directive_unprompted(scope: str = "workstation") -> Dict[str, Any]:
    """Issue a board directive UNPROMPTED, as the twin — or refuse, and say which.

    P3.4 clause (2). Called by the heartbeat when the Owner has switched `auto_align` on. Three outcomes,
    and each is a different fact:

      * the Chief is a ROLE — no instruction and no decision of the Owner's exists, so there is nothing of
        theirs to act on. Acting anyway would be the platform issuing its own direction under the Owner's
        name, so it REFUSES. This is the coupling to clause (1): the model's verdict decides.
      * nothing NEW since the last unprompted directive — the beat visits every sixty seconds, and a
        directive per visit would churn the living plan. Measured by the Owner's input COUNTS, so a new
        instruction or a new decision is what moves it.
      * issued — through `chief_instruct`, which runs the gaas.v5 pre-gate and cascades to the AI CEO, so
        the directive EXECUTES rather than being filed.

    The instruction the twin acts on is the Owner's OWN most recent one, carried verbatim. Nothing is
    invented: an unprompted directive restates what the Owner last asked for, in the light of what the
    plan now records, which is what a twin staying consistent with its principal means.
    """
    #  W645 (FU-636, ledger v14 R3) - THE MODEL IS READ FOR THIS SCOPE. It was read with no scope, so an
    #  instruction the Owner wrote for one entity was restated as a directive on whichever plan the beat
    #  was visiting - the Workstation apex plan by default - and recorded as executed there.
    m = founder_model(scope)
    if not m["is_modelled_twin"]:
        return {"issued": False, "reason": "role", "founder_model_basis": m["basis"], "scope": scope,
                "owner_inputs": m["owner_inputs"],
                "basis": ("REFUSED: this Chief is a ROLE, not a modelled twin - the Owner has written no "
                          "instruction and made no recorded decision, so there is nothing of theirs to act "
                          "on. Issuing a directive from the platform's standing canon alone would be the "
                          "platform directing itself under the Owner's name")}

    #  IDEMPOTENT ON THE OWNER'S RECORD, not on a clock: the beat may visit a thousand times between two
    #  instructions, and the plan must not grow an objective for each visit.
    try:
        #  ...and so is the record of what was already issued: one scope's last directive must not silence
        #  (or satisfy) another's
        prior = [r for r in _load() if r.get("kind") == "twin_directive_unprompted"
                 and (r.get("scope") or r.get("business_plan_scope") or "workstation") == scope]
    except Exception:
        prior = []
    last = prior[-1] if prior else None
    if last and int(last.get("owner_inputs") or -1) == int(m["owner_inputs"]):
        return {"issued": False, "reason": "nothing_new", "owner_inputs": m["owner_inputs"],
                "last_directive_id": last.get("directive_id"),
                "founder_model_basis": m["basis"],
                "basis": (f"NOT ISSUED: the Owner's record is unchanged since the last unprompted "
                          f"directive ({m['owner_inputs']} input(s) then and now), so there is nothing new "
                          f"to act on. A directive per beat would grow the living plan without the Owner "
                          f"having asked for anything")}

    #  the Owner's OWN latest words, verbatim — an unprompted directive restates what they asked for
    _latest = ""
    if m["instructions"]["count"]:
        _latest = str(m["instructions"]["recent"][-1].get("instruction") or "")
    elif m["decisions"]["count"]:
        _d = m["decisions"]["recent"][0]
        _latest = f"Act on the Owner's recorded decision to {_d.get('decision')}: {_d.get('title')}"
    if not _latest.strip():
        return {"issued": False, "reason": "no_readable_input", "owner_inputs": m["owner_inputs"],
                "founder_model_basis": m["basis"],
                "basis": ("NOT ISSUED: the model counts inputs but none carried readable text, so there is "
                          "nothing to restate. Nothing is invented in its place")}

    #  `unprompted=True` is what keeps this from becoming its own input on the next beat
    res = await chief_instruct(
        ChiefInstruction(instruction=_latest, cascade_to_ceo=True, scope=scope, unprompted=True),
        user=None)
    out = {
        "issued": True,
        "directive_id": res.get("directive_id"),
        "scope": scope,
        "acted_on": _latest[:200],
        #  W587 — REPORTED FROM THE OUTCOME, not from the request. A blind proved the guard vacuous
        #  because these were literals: asserting a flag the same dict hardcodes cannot fail (W497's
        #  shape). `objectives_added` is what the cascade actually landed on the living plan, so both of
        #  these now follow it rather than announcing an intention.
        "executed": bool(res.get("objectives_added")),
        "cascaded_to_ceo": bool(res.get("objectives_added")) or res.get("ceo_action_plan") not in (None, ""),
        "objectives_added": res.get("objectives_added"),
        "governance": (res.get("governance") or {}).get("status"),
        "owner_inputs": m["owner_inputs"],
        "founder_model_basis": m["basis"],
        "basis": (f"ISSUED UNPROMPTED by the twin, driven by a beat and not by a manual call. It restates "
                  f"the Owner's own latest input verbatim and nothing is invented. It ran through the "
                  f"gaas.v5 apex gate and was cascaded to the AI CEO, so it EXECUTES rather than being "
                  f"filed. Built from {m['instructions']['count']} instruction(s) and "
                  f"{m['decisions']['count']} decision(s) of the Owner's"),
        "kind": "twin_directive_unprompted",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        rows = _load_for_write()
        rows.append(dict(out))
        _save(rows)
    except Exception:
        out["recorded"] = False
    return out


@router.get("/chief/model")
async def chief_model(scope: "str | None" = None, owner: "str | None" = None):
    """The Chief's founder model and its BASIS — which inputs it was built from, and how many.

    P3.4 clause (3): every twin output is rendered with its basis. The model itself is the thing a reader
    needs in order to know whether the Chief speaking to them is a modelled twin or a role, so it is a
    surface of its own rather than a field buried in a directive's response.
    """
    m = founder_model(scope=scope, owner=owner)
    return {
        **m,
        "method": ("a Chief is a MODELLED TWIN only when the Owner has written an instruction or made a "
                   "recorded decision. The standing canon is carried either way and is the platform's, "
                   "identical for every Chief, so it is never counted as this Owner's own declaration"),
    }


@router.get("/charter")
async def board_charter():
    return {
        "owner": _OWNER,
        "board": _BOARD,
        "arms_length_agency": (
            "The AI CEO and below cannot instruct the board or mutate the genome directly. "
            "Direction flows Owner → Chief → Board → AI CEO. The board can monitor, change, "
            "update, control and impact all VSB living processes (highest authority)."
        ),
        "applies_to": "The Workstation IDBO and every VSB IDBO entity it generates.",
        # W464 (FU-012, the Owner's ruling of 2026-09-14) — the Board's ratification duty. A change reaching the Board
        # for ratification is a request flowing UP from Change Control, not an instruction to the Board.
        "ratification": (
            "A HIGH-tier change approved by a review (the reviewing model's decision marker or the organism-health "
            "threshold rule) waits for the Board to ratify it; nothing implements it until the Board, on the Owner's "
            "direction, ratifies or refuses it. The Owner's own explicit decisions need no ratification, and every "
            "material economy action is decided by the Owner directly (CRITICAL)."),
    }


def _ratifying_board(vsb_id: str | None) -> Dict[str, Any]:
    """W505 (FU-029) — which board ratifies a change: the VSB's own when it carries a vsb_id, else the apex.

    The Chief of a VSB's board is the standing charter of THAT VSB's owner (a role, not a trained model),
    which is the whole reason a VSB-scoped change must not be attributed to the workstation apex board.
    """
    if not vsb_id:
        return {"scope": "workstation", "tier": "apex",
                "represents_owner": _OWNER["name"], "vsb_id": None}
    owner = vsb_id
    try:
        from agentic_core.economy.living_vsbs import _load as _vsb_roster
        _v = (_vsb_roster() or {}).get(vsb_id) or {}
        owner = _v.get("owner_id") or _v.get("owner") or vsb_id
    except Exception as exc:
        # the VSB's own record could not be read; say whose board this is as far as can be told rather
        # than falling through to the apex, which would be the misattribution this row is about.
        return {"scope": vsb_id, "tier": "vsb", "represents_owner": None, "vsb_id": vsb_id,
                "owner_unresolved_because": f"{type(exc).__name__}: {exc}"}
    return {"scope": vsb_id, "tier": "vsb", "represents_owner": owner, "vsb_id": vsb_id}


class RatificationDecision(BaseModel):
    model_config = STRICT   # W628 (FU-398): an undeclared field here is a lost instruction - see _strict_models
    decision: Literal["ratify", "refuse"]
    notes: str = ""
    # A ratification is the Owner's decision recorded by the Board, never incidental: required in BOTH auth modes
    # (with auth off there is no admin role to check, so the acknowledgement is the whole gate).
    on_owner_direction: bool = False


@router.get("/ratifications")
async def ratification_queue():
    """W464 (FU-012) — the Board's ratification queue: every HIGH change a review approved that no Board decision has
    ratified yet (read from the full Change Control records, uncapped)."""
    from agentic_core.api.change_control import pending_ratifications
    rows = pending_ratifications()
    # W505 (FU-029) — WHICH BOARD. One global queue whose rule sentence said "the Board" read as the
    # workstation apex board deciding a change that belongs to a VSB. A change carrying a vsb_id is
    # ratified by THAT VSB's own board, whose Chief is that VSB owner's charter, and the row says so.
    for _r in rows:
        _r["ratifying_board"] = _ratifying_board(_r.get("vsb_id"))
    _vsb_scoped = sum(1 for _r in rows if _r.get("vsb_id"))
    return {"pending": rows, "total": len(rows),
            "apex_scoped": len(rows) - _vsb_scoped, "vsb_scoped": _vsb_scoped,
            "rule": ("A HIGH change approved by a review waits here; the board named on the row ratifies or refuses "
                     "it on that owner's direction. Nothing implements it until then."),
            "routing": ("A change carrying a vsb_id belongs to that VSB's own board, not to the workstation apex "
                        "board. Both queue here; `ratifying_board` on each row says which decides it.")}


@router.post("/ratifications/{cca_id}")
async def decide_ratification(cca_id: str, req: RatificationDecision,
                              user: dict | None = Depends(get_current_user)):
    """W464 (FU-012) — the Board records the Owner's decision on a change awaiting ratification. With auth enabled only
    an admin principal may (the name stamped is the authenticated one — a client cannot claim the Owner's); in both
    modes the caller must send on_owner_direction: true. No AI call decides it."""
    from agentic_core.api import change_control as cca
    u = cca._principal(user)
    if auth_enabled() and (not u or u.get("role") != "admin"):
        raise HTTPException(status_code=403, detail="Only an admin may record a Board ratification decision.")
    if not req.on_owner_direction:
        raise HTTPException(status_code=403, detail=(
            "A ratification is the Owner's decision, recorded by the Board: resend with on_owner_direction: true."))
    _out = cca.ratify_change(cca_id, req.decision, req.notes, cca._actor(user), cca._verified(user))
    # W505 (FU-029) — the decision records WHICH board recorded it, so a VSB-scoped ratification is never
    # read back as the apex board's.
    if isinstance(_out, dict):
        _rec = _out.get("change") if isinstance(_out.get("change"), dict) else _out
        _out["ratifying_board"] = _ratifying_board((_rec or {}).get("vsb_id"))
    return _out


class ChiefInstruction(BaseModel):
    model_config = STRICT   # W628 (FU-398): an undeclared field here is a lost instruction - see _strict_models
    instruction: str
    owner: str = "Rehan"
    cascade_to_ceo: bool = True
    scope: str = "workstation"   # which living business plan receives the objectives (e.g. a vsb_id)
    # P3.4 (W587) — WHOSE WORDS THE INSTRUCTION IS. The twin can issue a directive unprompted from the
    # beat, restating what the Owner last asked for; that restatement is NOT a new instruction from the
    # Owner, and counting it as one makes the twin read its own output back as its principal's record —
    # which would both inflate the "lived record" of a person who said nothing more and defeat the
    # beat's idempotence, issuing a directive on every visit forever. Default False: a request with no
    # marker is a human's, which is what every directive before this change was.
    unprompted: bool = False


@router.post("/chief/instruct")
async def chief_instruct(req: ChiefInstruction, user: dict | None = Depends(get_current_user)):
    """
    The Owner instructs their Chief. The Chief interprets the instruction
    faithfully (representing the Owner), issues a board-level directive, and delegates a
    timelined/resourced action plan to the AI CEO.
    """
    directive_id = f"dir-{uuid.uuid4().hex[:8]}"
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    # 1. The Chief (Owner's digital twin) interprets and represents the Owner faithfully — grounded
    #    in LIVE intelligence (plan progress · operations · prior directives), not just the charter.
    chief_prompt = (
        # W492 (refutation) - no twin model is trained; represent only what the Owner has stated
        f"You are the Chief of the Board — the standing charter of {req.owner}, the Owner/Founder of "
        f"the Workstation IDBO. You hold NO trained model of them: represent only what they have "
        f"actually stated, and say so when a question goes beyond it. "
        f"{_OWNER['fidelity_charter']}\n\n"
        f"The Owner's vision: {_OWNER['vision_summary']}"
        f"{founder_profile()}"
        f"{_live_intelligence(req.scope)}\n\n"
        f"The Owner's instruction:\n\"{req.instruction}\"\n\n"
        "Acting AS the Owner, produce a board-level directive that precisely realises their intent:\n"
        "## Owner Intent (restated faithfully, what they truly want)\n"
        "## Board Directive (the decision the board issues)\n"
        "## Director Assignments (which Director owns which part)\n"
        "## Success Criteria (how we know the Owner's wish is fulfilled)"
    )

    # §11 (W270) — the APEX direction runs under the same gaas.v5 constitutional gate as every lower
    # tier (a gate failure logs a LOUD UEG bypass event, never silent — the W249/W261 pattern).
    async def _directive_action() -> str:
        return await _q(chief_prompt, "board_chief", provenance)
    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        _gov = UnifiedConstitutionalInterceptorV16Omega("board-node", UEGLogger())
        _res = await _gov.intercept({"intent": "board_chief_instruct", "owner": req.owner,
                                     "scope": req.scope}, _directive_action)
        directive = _res.output if isinstance(_res.output, str) else await _directive_action()
        # W505 (FU-195) — WHAT IT SCREENED, carried with the verdict. The interceptor screens the declared
        # intent plus the owner and scope labels; it never reads the directive's text, so "allowed" is not
        # a clearance over the directive and must not be rendered as one.
        governance = {"status": _res.status, "checkpoint": _res.checkpoint_id,
                      "screened": "the declared intent, owner and scope labels of this request",
                      "covers_directive_content": False,
                      "basis": ("the gaas.v5 pre-gate compares the DECLARED INTENT against a fixed list of "
                                "prohibited intents and checks whether a declared human approval is "
                                "outstanding. It does not read the directive's prose. A status of "
                                "'allowed' therefore means nothing on that list matched \u2014 it is not a "
                                "judgement that the directive is constitutional.")}
    except Exception as _e:
        directive = await _directive_action()
        try:
            from agentic_core.gaas.v5 import UEGLogger
            UEGLogger().log({"type": "board.governance_bypass", "directive_id": directive_id,
                             "error": str(_e)[:200],
                             "note": "gaas.v5 gate unavailable — apex directive ran ungated (logged loudly)."})
        except Exception:
            pass
        governance = {"status": "ungated_bypass_logged", "error": str(_e)[:160]}

    # 2. Delegate to the AI CEO as a timelined, resourced, scheduled action plan.
    action_plan = ""
    if req.cascade_to_ceo:
        ceo_prompt = (
            "You are the AI CEO receiving a directive from the Board of Directors. Break it into an "
            "executable, timelined, resourced action plan integrated with the VSB living systems and "
            "agent swarm.\n\n"
            f"Board directive:\n{directive[:1200]}\n\n"
            "## Strategic Objectives (one per line, EXACTLY formatted: TITLE | KPI | TIMELINE | OWNER_ROLE)\n"
            "## Action Plan (numbered tasks, each with owner-role, resource, and timeline)\n"
            "## Delegation (C-Suite → CoE → BTO assignments)\n"
            "## KPIs & Review Cadence"
        )
        action_plan = await _q(ceo_prompt, "board_ceo_delegate", provenance)

    # §5 apex closure (W265) — the delegation LANDS: parsed objectives (TITLE|KPI|TIMELINE|OWNER_ROLE)
    # are appended to the scoped LIVING business plan, tagged with this directive. When the serving
    # model yields no machine-readable lines (e.g. the deterministic native floor), the Owner's
    # instruction itself becomes ONE objective — the apex direction never again evaporates into prose.
    objectives_added = 0
    # W488 (refutation) — WHEN THE DIRECTIVE DOES NOT LAND, THE ANSWER SAYS SO.
    # `except Exception: objectives_added = 0` reported a bare 0 for every failure and sealed that 0
    # into the UEG ledger — and the same round made `bp_mod._load` RAISE on an unreadable plan, so the
    # commonest failure became the silent one: the Owner's apex instruction evaporated behind a count
    # that reads exactly like 'the model produced no objectives'. The direction still never fails on
    # plan I/O (a 500 would lose the directive record), but the reason is now part of the record and of
    # the response, and a caller can tell 'nothing to add' from 'could not be added'.
    objectives_not_added_reason: str | None = None
    if req.cascade_to_ceo:
        from agentic_core.config import StoreUnavailable
        try:
            from agentic_core.api import business_plan as bp_mod
            new_objs = bp_mod.parse_objective_lines(action_plan, extra={"directive_id": directive_id})
            if not new_objs:
                new_objs = bp_mod.parse_objective_lines(
                    #  W593 (FU-427) — THE TIMELINE IS LEFT EMPTY, not filled with "next review". This
                    #  wrote a non-temporal placeholder into the TIMELINE position, so the platform itself
                    #  fed a fake phase into what it calls a time-phased roadmap and the roadmap then had
                    #  to defend against its own writer. An empty timeline lands in Unscheduled honestly.
                    f"{req.instruction[:110]} | (KPI to be set by the Board) |  | AI CEO",
                    extra={"directive_id": directive_id, "source": "chief_instruct_fallback"})
            plan = bp_mod._load(req.scope)
            plan.setdefault("objectives", []).extend(new_objs)
            bp_mod._save(plan)
            objectives_added = len(new_objs)
        except StoreUnavailable as e:
            objectives_added = 0
            objectives_not_added_reason = (
                f"the '{req.scope}' business plan could not be read whole ({e}), so the directive's objectives "
                f"were NOT added and the plan was not written — the directive itself is recorded. Fix or restore "
                f"the plan file and re-issue the instruction.")
        except Exception as e:
            objectives_added = 0
            objectives_not_added_reason = (
                f"the directive's objectives were NOT added to the '{req.scope}' business plan "
                f"({type(e).__name__}: {e}); the directive itself is recorded.")

    # W505 (FU-029) — the owner is STAMPED, not claimed. With auth off this is the caller's own label
    # (single-user back-compat); with auth on it is the authenticated username, server-side, so a client
    # cannot issue a directive in the Owner's name and have it written into the Owner's business plan.
    _owner = request_owner_id(user, req.owner)
    record = {
        "directive_id": directive_id,
        "owner": _owner,
        "owner_source": ("the authenticated principal (a client-supplied owner is not trusted while auth "
                         "is enabled)" if auth_enabled() else
                         "the caller's own label \u2014 single-user mode has no principal to stamp"),
        "owner_as_requested": req.owner,
        "instruction": req.instruction,
        # P3.4 (W587) — stamped so the founder model can tell the Owner's own words from the twin's
        # restatement of them. A row without this field predates the unprompted path and is the Owner's.
        "unprompted": bool(req.unprompted),
        "instruction_source": ("the Owner's twin, restating their latest input on a beat - NOT a new "
                               "instruction from the Owner, and not counted as one"
                               if req.unprompted else
                               "supplied directly by the caller as the Owner's own instruction"),
        "chief_directive": directive,
        #  W633 (FU-565) - on the floor the directive is a structured frame that did not read the instruction;
        #  said beside it, as /business-plan/generate does, instead of under a 'Modelled twin' banner alone
        "directive_reason": (("the native floor composed this directive: it did NOT read your instruction, so the "
                              "text below is a structured frame, not the Chief's response to it. Your instruction "
                              "itself is recorded verbatim above")
                             if str((provenance.get("served_by") or {}).get("board_chief", "native")).startswith("native")
                             else None),
        "ceo_action_plan": action_plan,
        "business_plan_scope": req.scope,
        "objectives_added": objectives_added,
        "objectives_not_added_reason": objectives_not_added_reason,   # W488 — a 0 that says why, or None
        "ai_provenance": provenance,     # §6 — which OWNED resource served the apex (W270)
        "governance": governance,        # §11 — the gaas.v5 gate verdict over the apex direction
        # W613 (FU-510, M1 v8 R3.6) — THE CHAIN NAMES THE TIERS THAT RAN. It was a constant six-tier list on
        # every record, printed under the result as "chain: Chief → Board → AI CEO → C-Suite → CoE → BTO",
        # while this path runs the Chief's prompt and, when cascading, the AI CEO's — nothing else. The
        # C-Suite, CoE and BTO run in the org cascade (POST /api/v1/swarm/cascade), not here.
        "delegation_chain": (["Chief", "AI CEO"] if req.cascade_to_ceo else ["Chief"]),
        "delegation_chain_basis": ("the tiers whose prompts ran for this directive. The C-Suite, CoE and BTO "
                                   "are NOT invoked by a directive; the org cascade runs them."),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    rows = _load_for_write()
    rows.append(record)
    _save(rows)

    # §6 (W270) — seal the apex direction into the tamper-evident UEG ledger.
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "board.chief_instruct", "directive_id": directive_id,
                         "owner": req.owner, "scope": req.scope,
                         "objectives_added": objectives_added,
                         "objectives_not_added_reason": objectives_not_added_reason,
                         "served_by": provenance["served_by"],
                         "any_external": provenance["any_external"],
                         "governance": governance.get("status")})
    except Exception:
        pass

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "board.chief_instruct",
                           f"{req.owner}: {req.instruction[:60]}", 0.85)
    except Exception:
        pass

    return record


class BoardDirective(BaseModel):
    model_config = STRICT   # W628 (FU-398): an undeclared field here is a lost instruction - see _strict_models
    topic: str
    domain: str = "enterprise"
    # §14 (W300) — deliberate for a specific entity's plan (a vsb_id) instead of the apex
    scope: str = "workstation"


def _director_grounding(did: str, scope: str = "workstation") -> str:
    """§5 (W279) — LIVE readings of the systems each director OWNS, so a director's input is
    grounded in the real state of their mandate, not invented. Best-effort per system; a system
    that cannot be read is reported 'unavailable' — never fabricated."""
    try:
        if did == "dir_strategy":
            # W300 — grounds in the SCOPED plan (a VSB's own objectives when deliberating for it)
            from agentic_core.api.business_plan import _load as _bp
            objs = (_bp(scope) or {}).get("objectives", [])
            by = {}
            for o in objs:
                by[o.get("status", "?")] = by.get(o.get("status", "?"), 0) + 1
            return f"living plan objectives by status: {by or 'none yet'}"
        if did == "dir_technology":
            from agentic_core.api.resource_fabric import _BY_ID
            from agentic_core.api.operational_excellence import model_health
            return (f"fabric catalogue: {len(_BY_ID)} resources; "
                    f"measured model resources: {len(model_health())}")
        if did == "dir_governance":
            from agentic_core.gaas.v5 import UEGLogger
            g = UEGLogger()._read()
            return f"UEG audit chain: {len(g.get('nodes', []))} sealed events, root {str(g.get('root_hash'))[:12]}…"
        if did == "dir_biomimetic":
            from agentic_core.organism.biobus import biobus
            ctx = biobus.organism_context()
            return (f"immune threat {(ctx.get('immune') or {}).get('threat_level')}; "
                    f"circadian {(ctx.get('circadian') or {}).get('cycle')}; "
                    f"ATP {(ctx.get('metabolic') or {}).get('atp_ratio')}")
        if did == "dir_operations":
            from agentic_core.config import data_path, read_json_reported
            runs, _why = read_json_reported(data_path("org_cascade_runs.json"), [])
            runs = runs if isinstance(runs, list) else []
            last = runs[-1] if runs else {}
            # W577 (FU-298) — this string IS the director's premise. An unreadable history read as
            # "org cascade runs: 0", which a deliberation takes as the fact that none have run. This
            # function's own docstring promises a system that cannot be read is reported unavailable
            # and never fabricated; a tolerant count was fabricating one.
            return (f"org cascade runs: {len(runs)}"
                    + (f" (INCOMPLETE — the run history could not be read whole: {_why}; the true "
                       f"count is at least this)" if _why else "")
                    + f"; last quality: "
                    + f"qms={((last.get('quality') or {}).get('qms_gate_passed'))} "
                    + f"coverage={((last.get('quality') or {}).get('delivery_coverage'))}")
        if did == "dir_finance":
            from agentic_core.api.operational_excellence import _load as _ops
            rows = [r for r in _ops()][-100:]
            ok = sum(1 for r in rows if r.get("success"))
            return f"recent operational rows: {len(rows)}, success rate {round(ok / len(rows), 2) if rows else 'n/a'} (virtual WST economy; real-money rails DISABLED)"
        if did == "dir_evolution":
            from agentic_core.config import data_path, read_json_reported
            dev, _why = read_json_reported(data_path("tier_development.json"), {})
            dev = dev if isinstance(dev, dict) else {}
            #  W615 (FU-489) — only a model-written action counts as improvement. Rows stored before W615 carry
            #  no served_by, and a floor-written one is boilerplate; both are named and not counted.
            from agentic_core.vbs.quality import floor_served as _fl615
            _model = [k for k, v in dev.items() if isinstance(v, dict) and v.get("served_by")
                      and not _fl615(v.get("served_by"))]
            _other = len(dev) - len(_model)
            return (f"Development Actions written by a served model: {len(_model)} tier edge(s)"
                    + (f"; {_other} other stored action(s) are floor-written or of unrecorded provenance and "
                       f"are NOT counted as improvement" if _other else "")
                    + (f" (INCOMPLETE — the development record could not be read whole: {_why}; the "
                       f"true number is at least this)" if _why else ""))
    except Exception as exc:
        return f"live reading unavailable ({str(exc)[:60]})"
    return "no live reading defined"


def _relevant_directors(topic: str, domain: str, k: int = 3) -> List[Dict[str, str]]:
    """Deterministic selection: score each director's mandate-word overlap with the topic+domain
    (the match reason IS the overlap — no AI guessing which specialists 'sound' relevant)."""
    import re as _re
    low = f" {topic.lower()} {domain.lower()} "
    scored = []
    for d in _BOARD:
        if d["id"] == "chief":
            continue
        words = set(_re.findall(r"[a-z]{5,}", (d["mandate"] + " " + d["title"]).lower()))
        hits = sum(1 for w in words if w in low)
        if hits:
            scored.append((hits, d["id"], d))
    scored.sort(key=lambda x: (-x[0], x[1]))
    chosen = [d for _, _, d in scored[:k]]
    if not chosen:   # no overlap → the strategy + operations directors hold the default mandate
        chosen = [d for d in _BOARD if d["id"] in ("dir_strategy", "dir_operations")]
    return chosen


@router.post("/directive")
async def board_directive(req: BoardDirective, user: dict | None = Depends(get_current_user)):
    """§5 (W279) — the board deliberates as SPECIALISTS: the relevant directors are selected
    deterministically, EACH contributes through its own AI call GROUNDED in live readings of the
    systems it owns, and the Chief chairs a synthesis over the directors' ACTUAL inputs — no more
    single-call invented 'Director Inputs'."""
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False}
    directors = _relevant_directors(req.topic, req.domain)
    director_inputs: Dict[str, Dict[str, str]] = {}
    for d in directors:
        grounding = _director_grounding(d["id"], req.scope)
        text = await _q(
            f"You are the {d['title']} on the Workstation IDBO Board.\n"
            f"Your mandate: {d['mandate']}\n"
            f"LIVE readings of the systems you own: {grounding}\n\n"
            f"Topic before the board: {req.topic}\nDomain: {req.domain}\n\n"
            "Give your specialist direction (under 80 words), grounded in the readings above — "
            "cite them where relevant.", f"board_{d['id']}", provenance)
        director_inputs[d["id"]] = {"title": d["title"], "live_grounding": grounding, "input": text}
    inputs_block = "\n\n".join(f"[{v['title']}] (live: {v['live_grounding']})\n{v['input'][:400]}"
                               for v in director_inputs.values())
    resolution = await _q(
        "You are the Chief (the Owner's standing charter — no trained model of them exists; represent "
        "only what the Owner has stated), chairing the Workstation IDBO Board. "
        f"Topic: {req.topic}\nDomain: {req.domain}\n\n"
        f"The directors have ACTUALLY deliberated — their real inputs:\n{inputs_block}\n\n"
        "Synthesise and resolve (do not invent inputs beyond those above):\n"
        "## Board Position (the resolved direction)\n"
        "## Directive to the AI CEO (what to execute)\n"
        "## Guardrails (governance / arms-length constraints)", "board_directive", provenance)
    from agentic_core.vbs.quality import floor_served as _floor623
    record = {
        "kind": "board_directive",
        "topic": req.topic,
        "domain": req.domain,
        "resolution": resolution,
        # §5 (W279) — the directors' REAL specialist inputs + the live groundings they drew on.
        "director_inputs": director_inputs,
        "directors_engaged": [d["id"] for d in directors],
        "ai_provenance": provenance,     # §6 — apex provenance (W270)
        "chaired_by": "Chief (the Owner's charter and instructions)",
        #  W623 (FU-527, M1 v9 R3.4) — THE STATUS IS WHAT HAPPENED. Every deliberation was stored "resolved", so a
        #  board whose directors and Chief were all served by the deterministic floor - frames composed from the
        #  topic, no director weighing anything - read as a decided question. A floor-served board FRAMED the
        #  topic; only a model-served one deliberated.
        "status": ("framed_floor_not_deliberated" if _floor623(provenance.get("served_by")) else "resolved"),
        "status_basis": (("every director and the Chief were served by the deterministic floor, so the topic was "
                          "FRAMED, not deliberated: nothing here weighed it") if _floor623(provenance.get("served_by"))
                         else "a served model composed the directors' inputs and the resolution"),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    # W270 — board deliberations PERSIST (previously the resolution evaporated at response time).
    rows = _load_for_write()
    rows.append(record)
    _save(rows)
    return record
