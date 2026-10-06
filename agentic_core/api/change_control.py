"""
Change Control Agency (CCA) — Arms-Length Governance for Organism Changes.

The CCA is an autonomous governance body that reviews and approves/rejects
changes to the IDBO organism — configuration changes, VSB mutations,
platform upgrades, policy amendments, and capability additions.

Biological analogy: the CCA mirrors the adaptive immune system's memory B-cells
— every significant change is reviewed, recorded, and either integrated or
rejected with reasoning.

Governance tiers (W459 — this list is what the code DOES; the earlier version promised a
constitutional GaaS gate, a 24h cooling period and a manual flag, none of which exist here):
  LOW    — auto-approved at submit when composite health >= 0.6 AND immune threat is
           NOMINAL/ELEVATED; otherwise held for review
  MEDIUM — review required. A single [DECISION: …] marker from the serving model decides it. With
           no marker (the deterministic floor) or conflicting markers, the verdict is the
           ORGANISM-HEALTH THRESHOLD RULE (composite_health >= 0.5 → approved, else rejected), and the
           record says so in `decision_source` and at the head of the review text. With auth
           enabled, a rule verdict is applied only when an ADMIN requests the review; a non-admin's
           review is HELD with the rule's verdict recorded as a recommendation.
  HIGH   — as MEDIUM, plus a recorded §17.5 pre-validation PASS before /implement. W464 (FU-012, the Owner's
           ruling of 2026-09-14): a HIGH change approved by a REVIEW (the model's marker or the health rule)
           waits for BOARD RATIFICATION — /implement, and anything else acting on the approval, refuses it until
           the Board records the Owner's direction (POST /api/v1/board/ratifications/{cca_id}). The Owner's own
           explicit decision (override_decision) needs no ratification.
  CRITICAL — NEVER decided by a review. A model marker is recorded as a RECOMMENDATION and the health
           rule never applies: the change is HELD until an explicit admin decision
           (admin_decision_for_critical; auth ON: an admin principal). W464 (FU-014): economy materiality
           holds (change_type economy_material) are CRITICAL — every material economy action is decided only
           by the Owner's explicit decision in the Governance hub's Sovereign Sanctum — and code_change is HIGH.
  A record is decided and implemented under its EFFECTIVE tier (effective_tier): the tier it was filed with,
  raised to its change type's tier-map entry, so a record filed before a tier-map change is decided under the
  tier the map now gives it.

Decisions on the constitutional ledger (W464, FU-013): every Change Control decision — an approval (a review's, the
Owner's, the LOW auto-approval, the immune reflex), a rejection, a retirement through /implement, and a Board
ratification decision — writes one UEG event (cca.change_approved / cca.change_rejected / cca.change_retired /
board.change_ratified / board.change_ratification_refused) after the record lands; submissions and holds stay in
the record's own audit trail. The economy gate's own withdrawals of its holds (superseded, unreleasable, not the
Owner's) are the economy's machine actions and reach the UEG as economy.materiality_hold_withdrawn. Decisions made
before W464 have no such event. A ledger write that fails never undoes the decision: the response says
`ueg_logged: false` and the failure is logged.

  Governed live levers (config_change on a wired key, or a config reset): with auth enabled only an
  admin may IMPLEMENT them — the same bar as /immune-reconfigure, which applies those levers.

Identity (W459): with auth enabled every human-requested submission and decision is stamped with the
AUTHENTICATED principal — a client cannot claim another name — and carries `by_verified`, which
says whether the name was checked. Reflex and machine entries (biobus auto-approval, the immune
reflex, the VSB evolution apply, the economy cycle) name the mechanism instead. With auth disabled
(the shipped single-user default) the caller-supplied name is kept for back-compat and
`by_verified` is false; no synthetic "admin" identity is ever fabricated into the record.

§17.5 pre-validation (W459): there is NO twin model. When the serving resource returns no
[TWIN: …] marker the verdict comes from an organism HEALTH GATE, and the record now says
"no twin model — organism health gate only" instead of claiming a forward simulation.

  POST /api/v1/cca/submit           — submit a change request
  GET  /api/v1/cca/queue            — pending change requests
  POST /api/v1/cca/{cca_id}/review  — request a review, or record an explicit admin decision
  GET  /api/v1/cca/approved         — approved change log
  GET  /api/v1/cca/rejected         — rejected change log
  GET  /api/v1/cca/{cca_id}         — get a specific change request
  POST /api/v1/cca/{cca_id}/implement — apply + mark an approved change implemented (refused 409 while the
                                       change awaits Board ratification; an approved
                                       economy_material hold is never implemented here: refused 409 while an
                                       action can still release it or that cannot be determined, otherwise
                                       retired as 'withdrawn' — admin only)
  GET  /api/v1/cca/impact/{cca_id}  — AI impact assessment
  GET  /api/v1/cca                  — every change record
  GET  /api/v1/cca/implemented      — implemented change log
  POST /api/v1/cca/{cca_id}/twin-prevalidate — run/refresh the §17.5 pre-validation
  POST /api/v1/cca/immune-reconfigure — the immune system's governed defensive reflex (admin)
"""
from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.auth.core import auth_enabled, get_current_user, request_owner_id, require_admin
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/api/v1/cca", tags=["change-control-agency"])

_CCA_STORE = data_path("change_control")
_CCA_STORE.mkdir(parents=True, exist_ok=True)

ChangeStatus = Literal["submitted", "under_review", "approved", "rejected", "implemented", "withdrawn"]
ImpactTier = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


_CCA_ID_RE = __import__("re").compile(r"[A-Za-z0-9_-]{1,80}")


def _valid_cca_id(cca_id: str) -> bool:
    """W459 — a change id is ONE safe path segment. Checked before the store is touched: on Windows a
    backslash or a drive-letter path passes as a single route segment, and taking the record lock on
    such an id created directories outside the store and could break another store's stale lockfile."""
    return isinstance(cca_id, str) and bool(_CCA_ID_RE.fullmatch(cca_id))


def _cca_path(cca_id: str) -> Path:
    return _CCA_STORE / f"{cca_id}.json"


def _load_change(cca_id: str) -> dict | None:
    """W459 — one loader for every reader. STRICT: a governance record that does not parse is never
    half-read and decided upon (a tolerant loader would hand back a recovered prefix that still
    carries its cca_id); it is treated as absent and the corruption is LOGGED, so the listing and
    the by-id routes can never disagree about whether a record exists."""
    import logging
    if not _valid_cca_id(cca_id):
        return None
    p = _cca_path(cca_id)
    if not p.exists():
        return None
    for attempt in range(6):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
            break
        except PermissionError as e:
            # Windows: a read that meets another request's atomic os.replace mid-flight is a sharing
            # violation, not corruption — retry briefly, as the writer itself does
            if attempt == 5:
                logging.getLogger("change_control").warning("change record %s stayed locked: %s", cca_id, e)
                return None
            time.sleep(0.015 * (attempt + 1))
        except (OSError, ValueError) as e:
            logging.getLogger("change_control").error("change record %s is unreadable: %s", cca_id, e)
            return None
    if not (isinstance(c, dict) and c.get("cca_id")):
        logging.getLogger("change_control").warning("change record %s is not a change record", cca_id)
        return None
    return c


def _mtime(p: Path) -> float:
    try:
        return p.stat().st_mtime
    except OSError:          # removed between the glob and the stat — sort it last, never raise
        return 0.0


def _save_change(change: dict) -> None:
    # W438 — atomic per the store convention (a torn change file poisons the audit record). W459: the
    # per-record serialisation lives in _update_change / _change_mutation; this plain writer is only
    # for creating a fresh record or for writes already inside that critical section.
    from agentic_core.config import atomic_write_json
    atomic_write_json(_cca_path(change["cca_id"]), change)


def _principal(user: Any) -> dict | None:
    """W459 — the authenticated principal, or None. An in-process call that never went through
    FastAPI leaves the `Depends(...)` sentinel in the parameter; that is not an identity."""
    return user if isinstance(user, dict) else None


def _actor(user: Any, fallback: str = "single-user-mode") -> str:
    """Who to STAMP on a record. Auth ON → always the authenticated username (a client cannot claim
    another name). Auth OFF → the caller-supplied/machine string, never a fabricated 'admin'."""
    return request_owner_id(_principal(user), fallback)


def _verified(user: Any) -> bool:
    """Whether the name in `by` was actually CHECKED by the auth layer."""
    return bool(auth_enabled() and _principal(user))


@contextmanager
def _change_mutation(cca_id: str):
    """W459 — the per-record critical section. Every load→modify→write on one change now runs
    inside it (concurrent review/implement used to clobber each other's audit entries).

    MUST stay fully synchronous: never `await` inside. The in-process half of store_lock is a
    per-path RLock — reentrant on the single asyncio thread, so it does NOT separate two
    coroutines — and acquisition spins on time.sleep, which would block the event loop.
    """
    from agentic_core.config import store_lock
    if not _valid_cca_id(cca_id):
        raise HTTPException(status_code=404, detail="Change not found.")
    # A short timeout: the sections are milliseconds long, and a stale lockfile must not freeze the
    # event loop for 10s on every call. Only a timeout ACQUIRING this record's lock is reported as
    # "busy" — a TimeoutError raised inside the section (e.g. the organism config store's own lock
    # during /implement) keeps its own origin instead of being blamed on the change record.
    lock = store_lock(_cca_path(cca_id), timeout=3.0)
    try:
        lock.__enter__()
    except TimeoutError:
        raise HTTPException(status_code=503,
                            detail="Change record is busy — another decision is being written. Retry.") from None
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


def _update_change(cca_id: str, mutate) -> dict:
    """Re-read INSIDE the lock, mutate the FRESH record, write atomically — so a record loaded
    before an await is never written back over a newer decision."""
    from agentic_core.config import atomic_write_json
    with _change_mutation(cca_id):
        fresh = _load_change(cca_id)
        if fresh is None:
            raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
        mutate(fresh)
        atomic_write_json(_cca_path(cca_id), fresh)
        return fresh


def _economy_releasable(c: dict) -> bool:
    try:
        from agentic_core.economy.governance import releasable_by_gate
        return bool(releasable_by_gate(c))
    except Exception:
        return True   # unknown: never retire on a guess (implement stays refused)


def _list_changes(status_filter: str | None = None) -> list[dict]:
    result = []
    # W459 — stat() ran outside the try, so a record removed mid-scan raised out of GET /queue; and
    # the listing now reads through _load_change, so it agrees with the by-id routes on every file
    for p in sorted(_CCA_STORE.glob("*.json"), key=_mtime, reverse=True):
        try:
            c = _load_change(p.stem)
            if not c:
                continue
            if status_filter and c.get("status") != status_filter:
                continue
            result.append({
                "cca_id": c["cca_id"],
                "title": c.get("title", ""),
                "change_type": c.get("change_type", ""),
                # W464 — the tier the record is decided under (a record filed before a tier-map change reads its new tier)
                "impact_tier": effective_tier(c),
                "status": c.get("status", "submitted"),
                "submitted_by": c.get("submitted_by", "system"),
                "submitted_at": c.get("submitted_at", ""),
                "reviewed_at": c.get("reviewed_at"),
                "decision": c.get("decision"),
                # W464 (FU-012) — what decided it, and whether the approval still waits for the Board
                "decision_source": approval_source(c),
                "awaiting_board_ratification": awaiting_board_ratification(c),
                "board_ratification": _ratification_decision(c),
                # W463 — a held record (awaiting an explicit decision) and an economy hold's current amount
                "hold_reason": c.get("hold_reason"),
                "est_distributable_wst": c.get("est_distributable_wst"),
                # W581 (FU-313) — the promise and the variance reach the QUEUE, which is the list the
                # growing tip reads. A commitment held only on the individual record is a promise nobody
                # sees while the work is in flight, which is the whole point of recording one.
                "commitment": c.get("commitment"),
                "variance": c.get("variance"),
                "variance_basis": c.get("variance_basis"),
                # W463 (third refutation) — a hold filed after a rejection needs an explicit decision from the moment
                # it is filed (before any review sets hold_reason)
                "follows_rejection": ((c.get("follows_rejection") or {}).get("cca_id")
                                      if isinstance(c.get("follows_rejection"), dict) else None),
                # W463 (fourth refutation) — whether running the economy action can ever release this record
                **({"releasable": _economy_releasable(c)} if c.get("change_type") == "economy_material" else {}),
            })
        except Exception:
            pass
    return result


# ── Impact tier determination ─────────────────────────────────────────────────

_TIER_MAP: dict[str, ImpactTier] = {
    "config_minor":         "LOW",
    "config_major":         "MEDIUM",
    "organism_mutation":    "HIGH",
    "vsb_evolution":        "MEDIUM",
    "genome_edit":          "HIGH",
    "constitutional":       "CRITICAL",
    "platform_upgrade":     "MEDIUM",
    "capability_add":       "MEDIUM",
    "capability_remove":    "HIGH",
    "policy_amendment":     "HIGH",
    "data_schema":          "MEDIUM",
    "security_change":      "HIGH",
    "integration_add":      "LOW",
    "integration_remove":   "MEDIUM",
    # P3.26 clause (3) (W608) — the death of an entity is a MAJOR change: twin pre-validation, and Board
    # ratification when a review rather than the Owner approved it
    "entity_retirement":    "HIGH",
    # W464 (FU-014, the Owner's ruling of 2026-09-14) — both fell through to MEDIUM by the default, so their tier
    # was an accident rather than a decision. A code correction is HIGH (a review's approval waits for Board
    # ratification); a material economy action is CRITICAL (decided only by the Owner's explicit decision).
    "code_change":          "HIGH",
    "economy_material":     "CRITICAL",
}


# W505 (FU-157, S1.18) — the phrases that raise a change to CRITICAL whatever its declared type. Matched on
# WORD BOUNDARIES: as bare substrings "constitution" also matched "deconstitutionalise" and "unconstitutional",
# so a description merely discussing constitutionality was filed CRITICAL.
_CRITICAL_PHRASES = ("constitution", "genome core", "delete all", "reset organism", "override gaas")


def _tier_raise(description: str) -> str | None:
    """Which phrase raises this description to CRITICAL, or None. Pure, so the form can ask before submitting."""
    import re as _re
    low = str(description or "").lower()
    for k in _CRITICAL_PHRASES:
        if _re.search(r"\b" + _re.escape(k) + r"\b", low):
            return k
    return None


def _determine_tier(change_type: str, description: str) -> ImpactTier:
    base = _TIER_MAP.get(change_type, "MEDIUM")
    # Elevate if the description names something constitutional or organism-wide. Failing closed here is
    # right; doing it without telling the caller is what FU-157 (S1.18) is about, so submit() records the
    # raise and the response says which phrase did it.
    return "CRITICAL" if _tier_raise(description) else base


_TIER_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
REVIEW_DECISION_SOURCES = ("model_decision_marker", "health_threshold_rule")


def effective_tier(c: dict) -> str:
    """W464 (FU-014) — the tier a record is DECIDED and IMPLEMENTED under: the tier stamped when it was filed, raised
    to its change type's tier-map entry. The tier is stamped once, at filing, and nothing re-read the map when a
    decision was made — so after the Owner's ruling an economy hold filed as MEDIUM by the old default could still be
    approved by a model marker, and release money. A stored tier is never lowered (keyword elevation stands)."""
    stored = c.get("impact_tier") if isinstance(c, dict) and c.get("impact_tier") in _TIER_RANK else "MEDIUM"
    floor = _TIER_MAP.get(str((c or {}).get("change_type") or "")) if isinstance(c, dict) else None
    return floor if floor and _TIER_RANK[floor] > _TIER_RANK[stored] else stored


def _stamp_effective_tier(fresh: dict) -> None:
    """Raise a stored tier to its effective tier, keeping the tier it was filed with (call inside the record lock)."""
    tier = effective_tier(fresh)
    if fresh.get("impact_tier") != tier:
        fresh.setdefault("impact_tier_filed", fresh.get("impact_tier"))
        fresh["impact_tier"] = tier


def _ratification_decision(c: dict) -> str | None:
    r = c.get("board_ratification") if isinstance(c, dict) else None
    return r.get("decision") if isinstance(r, dict) else None


def approval_source(c: dict) -> str | None:
    """W464 (refutation) — what decided a record, including records decided before W459 wrote `decision_source`.
    Before W459 a review and an override both left only {event, by: "cca_ai"} in the trail; an override's review text
    began "Manual override:" (the only mark that tells them apart). A pre-W464 auto-approval names itself in
    `decision`. Anything else with no source is an UNRECORDED decision — read as a review's, never as the Owner's
    (fail closed: such an approval waits for the Board, and the economy gate does not release it)."""
    if not isinstance(c, dict):
        return None
    src = c.get("decision_source")
    if src:
        return str(src)
    if c.get("status") not in ("approved", "implemented", "rejected"):
        return None
    if str(c.get("review_result") or "").startswith("Manual override:"):
        return "admin_override"
    if c.get("decision") == "auto_approved":
        return "low_tier_auto_approval"
    if c.get("decision") == "auto_approved_immune_defence":
        return "immune_defence_reflex"
    return "unrecorded_decision"


def awaiting_board_ratification(c: dict) -> bool:
    """W464 (FU-012, the Owner's ruling of 2026-09-14) — a HIGH change approved by a REVIEW (the reviewing model's
    decision marker or the organism-health threshold rule — not the Owner's explicit decision) waits for the Board to
    ratify it, and nothing acts on the approval until then. Derived from the record itself, so an approval a review
    made before the ruling waits too — including one made before W459 recorded what decided it (approval_source: an
    unrecorded decision reads as a review's). A CRITICAL change is never approved by a review (and one that reached
    'approved' some other way is caught here as well). An economy materiality hold is excluded: it is decided only by
    the Owner, and its own gate never releases a review's approval (economy.governance)."""
    if not (isinstance(c, dict) and c.get("status") == "approved"
            and c.get("change_type") != "economy_material"
            and _TIER_RANK[effective_tier(c)] >= _TIER_RANK["HIGH"]
            and _ratification_decision(c) != "ratified"):
        return False
    _src = approval_source(c)
    if _src in REVIEW_DECISION_SOURCES + ("unrecorded_decision",):
        return True
    # W505 (FU-030) — an override is excluded from this queue because it IS the Owner's decision, and that
    # only holds if somebody acknowledged it as one. So a HIGH-or-above override carrying no
    # acknowledgement waits for the Board — failing closed, as an unrecorded_decision already does.
    #
    # NARROWED to an EXPLICITLY STORED admin_override, which is the population the row names: records
    # written between W459 (which began storing decision_source) and W505 (which added the flag). A
    # PRE-W459 record carries no decision_source at all and is identified only by its review text
    # beginning "Manual override:" — W464 already ruled on those and the suite pins that ruling, so using
    # the INFERRED source here would have silently overturned a decision another round reasoned through.
    return (c.get("decision_source") == "admin_override"
            and not c.get("owner_decision_acknowledged"))


def _log_decision(event: dict) -> bool:
    """W464 (FU-013) — write one Change Control DECISION to the constitutional ledger. Called only after the record has
    landed and outside its lock: a hash-chained entry cannot be taken back, so it must never describe a decision a
    compare-and-set then refused, and a slow ledger must never hold the record lock. Never raises: a failed write is
    logged and reported to the caller (`ueg_logged: false`) — it never undoes the decision."""
    return _log_decision_result(event)[0]


def _log_decision_result(event: dict) -> tuple[bool, str | None]:
    """As `_log_decision`, but returns (written, why_not). W505 (FU-031) — the reason was written to the
    server log and discarded; it has to travel so it can be written onto the record."""
    import logging
    try:
        from agentic_core.gaas.v5 import UEGLogger
        return bool(UEGLogger().log(event)), None
    except Exception as e:
        logging.getLogger("change_control").error("decision %s for %s was not written to the UEG: %s",
                                                  event.get("type"), event.get("cca_id"), e)
        return False, f"{type(e).__name__}: {e}"


def _log_decision_on(cca_id: str, event: dict, by: str = "cca") -> bool:
    """W505 (FU-031) — write a decision to the constitutional ledger and, if that fails, MARK THE RECORD.

    Without the mark a decision with no ledger node was reported once, in one HTTP response, and then existed
    nowhere: nothing could find it afterwards and nothing reconciled it. Marking never raises and never undoes
    the decision — a decision that stands with a recorded gap is honest; one that stands silently is not.
    """
    import logging
    written, why = _log_decision_result(event)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if written:
        # The SUCCESS is marked as well. Without it "no mark" is indistinguishable from "never written",
        # so the reconciliation below could never come back clean and would be no instrument at all.
        def _ok(fresh: dict) -> None:
            fresh.pop("ueg_pending", None)
            fresh.setdefault("audit_trail", []).append(
                {"event": "ueg_written", "ts": ts, "by": by, "by_verified": False,
                 "event_type": event.get("type")})
        try:
            _update_change(cca_id, _ok)
        except Exception as exc:
            logging.getLogger("change_control").warning(
                "%s reached the ledger but the record could not be marked: %s", cca_id, exc)
        return True

    def _mark(fresh: dict) -> None:
        fresh["ueg_pending"] = {"event_type": event.get("type"), "why": why, "at": ts, "by": by,
                                "note": ("this decision stands; its constitutional node is missing. A "
                                         "reconciliation writes it — the request that decided must not "
                                         "retry, because a chained entry cannot be taken back.")}
        fresh.setdefault("audit_trail", []).append(
            {"event": "ueg_write_failed", "ts": ts, "by": by, "by_verified": False,
             "event_type": event.get("type"), "why": why})
    try:
        _update_change(cca_id, _mark)
    except Exception as exc:
        logging.getLogger("change_control").error(
            "the ledger gap for %s could not be marked on the record either: %s", cca_id, exc)
    return False


def decisions_missing_ledger_node() -> list[dict]:
    """W505 (FU-031) — every decided change whose constitutional node is missing or unproven.

    Two classes, because a reconciliation that only sees observed failures is not a reconciliation:
      · `marked`   — the write failed and said so (`ueg_pending` is on the record).
      · `unproven` — the record holds a decision and no mark either way. A worker killed between the record
                     landing and the ledger write leaves exactly this, and nothing observed it. Reported as
                     unproven rather than missing: it may well be in the chain.
    """
    out = []
    for p in sorted(_CCA_STORE.glob("*.json"), key=_mtime, reverse=True):
        c = _load_change(p.stem)
        if not isinstance(c, dict) or c.get("status") not in ("approved", "rejected", "implemented", "retired"):
            continue
        pend = c.get("ueg_pending")
        if isinstance(pend, dict):
            out.append({"cca_id": c.get("cca_id"), "kind": "marked", "status": c.get("status"),
                        "event_type": pend.get("event_type"), "why": pend.get("why"), "at": pend.get("at"),
                        "title": str(c.get("title") or "")[:120]})
        elif not any((e or {}).get("event") == "ueg_written" for e in (c.get("audit_trail") or [])):
            out.append({"cca_id": c.get("cca_id"), "kind": "unproven", "status": c.get("status"),
                        "event_type": None,
                        "why": ("no mark either way: this was decided before the mark existed, or a worker "
                                "died between the record landing and the ledger write. The chain has to be "
                                "read to tell which — it is not a claim that the node is missing."),
                        "at": c.get("reviewed_at"), "title": str(c.get("title") or "")[:120]})
    return out


def _decision_fields(c: dict) -> dict:
    """The short, stable facts a decision event carries (never review text or model output: the Hub renders event data
    verbatim, and every UEG write rewrites the whole ledger)."""
    return {"cca_id": c.get("cca_id"), "title": str(c.get("title") or "")[:120],
            "change_type": c.get("change_type"), "impact_tier": effective_tier(c),
            **({"vsb_id": c.get("vsb_id")} if c.get("vsb_id") else {}),
            **({"est_distributable_wst": c.get("est_distributable_wst")}
               if c.get("est_distributable_wst") is not None else {}),
            **({"counterparty": c.get("counterparty")} if c.get("counterparty") else {})}


# ── Request models ────────────────────────────────────────────────────────────

class ConfigChangeSpec(BaseModel):
    # W438 — the CCA's execution arm for organism configuration. Either one (section, key, value)
    # change or reset: true. Validated/coerced at SUBMIT time so an unappliable change can never
    # be approved, and APPLIED by /implement (which used to only mark, never execute).
    section: str | None = None
    key: str | None = None
    value: Any = None
    reset: bool = False


def _record_variance(change: dict, now: str, outcome: str) -> None:
    """Fill `variance` once a change reaches an outcome, or say why it cannot be filled.

    W581 (FU-313). A commitment is made in ROUNDS and a round is not a clock unit, so what gets measured
    is the ELAPSED HOURS this record actually carries — submitted_at to the outcome — and the rounds
    figure is DERIVED from it by dividing by a median round length that is named in the result. Where the
    capacity was never measured at submit, the derived figure is None WITH A REASON: a figure may only
    carry the name of what it measured, and `0` would be a measured zero nobody measured.

    Called from BOTH places that mark a change implemented. One would have been the second-writer class.
    """
    import time as _t

    commitment = change.get("commitment")
    if not isinstance(commitment, dict):
        change["variance"] = None
        change["variance_basis"] = "no commitment was recorded, so no variance is defined"
        return

    def _secs(stamp):
        try:
            return _t.mktime(_t.strptime(str(stamp), "%Y-%m-%dT%H:%M:%SZ"))
        except (ValueError, TypeError):
            return None

    t0, t1 = _secs(change.get("submitted_at")), _secs(now)
    if t0 is None or t1 is None:
        change["variance"] = None
        change["variance_basis"] = ("the submit or outcome stamp could not be read, so the elapsed time "
                                    "is unknown - not zero")
        return

    elapsed_h = round(max(0.0, (t1 - t0) / 3600.0), 3)
    cap = commitment.get("capacity_at_submit") or {}
    median_h = cap.get("median_hours_per_round")
    committed = commitment.get("committed_rounds")

    rounds_equiv = over_by = None
    if isinstance(median_h, (int, float)) and median_h > 0:
        rounds_equiv = round(elapsed_h / float(median_h), 2)
        if isinstance(committed, int):
            over_by = round(rounds_equiv - committed, 2)
        derived = (f"DERIVED, not counted: {elapsed_h} elapsed hours divided by the {median_h} h median "
                   f"round length measured at submit over {cap.get('rounds_measured')} rounds. A round "
                   f"is not a clock unit, so this is an equivalence and not a count of rounds.")
    else:
        derived = ("NOT DERIVABLE: no median round length was measured at submit, so elapsed hours "
                   "cannot be expressed in rounds. The hours below ARE measured.")

    change["variance"] = {
        "outcome": outcome,
        "elapsed_hours": elapsed_h,
        "committed_rounds": committed,
        "rounds_equivalent": rounds_equiv,
        "over_by_rounds": over_by,
        "within_commitment": (None if over_by is None else bool(over_by <= 0)),
        "derivation": derived,
        #  W581 — THE CONFIDENCE IS NOT REPEATED HERE. The commitment block on the same record holds it
        #  WITH its declared/measured label, and the page renders that label; carrying a second copy on the
        #  variance gave two fields one fact, which is how they drift apart. The property "a variance does
        #  not turn a declared number into a measured one" is kept by the commitment's label surviving the
        #  outcome, which is what the guard now asserts. `measured_at` went for the same reason: the
        #  record's own implemented_at stamp is the outcome time.
    }
    change["variance_basis"] = (
        f"measured at the {outcome} outcome: elapsed hours are from this record's own stamps; the rounds "
        f"figure is derived and names what it divided by")


#  W581 (FU-313) — the repo root, for the measured round history the commitment is made against.
#  agentic_core/api/change_control.py -> parents[2] is the checkout.
_ROOT_FOR_FORECAST = Path(__file__).resolve().parents[2]


class SubmitChangeRequest(BaseModel):
    title: str
    change_type: str = "config_minor"
    description: str
    rationale: str = ""
    affected_systems: list[str] = []
    submitted_by: str = "system"
    vsb_id: str | None = None
    rollback_plan: str = ""
    config_change: ConfigChangeSpec | None = None
    # W581 (FU-313) — WHAT WAS PROMISED, so a variance can be read back against it. These were being
    # sent to /transformation/orchestrate and SILENTLY DROPPED, because an undeclared field on a
    # Pydantic model is discarded and the caller still gets a 200 (the platform-wide half of that is
    # registered separately). A commitment about the platform's OWN delivery is admissible under
    # CAPACITY_FACULTY_MODEL §2; a number a caller hands over is not a MEASUREMENT, so `confidence` is
    # recorded as DECLARED and both require a basis.
    committed_rounds: int | None = None
    confidence: float | None = None
    commitment_basis: str = ""


class ReviewDecision(BaseModel):
    # W459 — the override used to be free text: `override_decision: "implemented"` jumped a CRITICAL
    # change straight past approval with nothing applied and no pre-validation recorded, and any
    # other word was written into `status` outside the ChangeStatus vocabulary.
    override_decision: Literal["approved", "rejected"] | None = None   # None → review
    reviewer_notes: str = ""
    # An override on a CRITICAL change is never incidental: the caller must say, explicitly, that
    # this is an admin decision. Required in BOTH auth modes (with auth off there is no admin role
    # to check, so the acknowledgement is the whole gate).
    admin_decision_for_critical: bool = False
    # W505 (FU-030) — an override on a HIGH-or-above change is never incidental either. A CRITICAL change
    # required the flag above and a HIGH change required NOTHING, so with auth off any client's override was
    # recorded as the Owner's explicit decision (admin_override) — which is exactly the decision class
    # awaiting_board_ratification excludes from the queue. Required in both modes, because with auth off
    # there is no admin role to check and the acknowledgement is the whole gate.
    owner_decision_acknowledged: bool = False
    # W463 — an economy materiality hold is kept current while submitted (its amount grows with new intake).
    # A reviewer who read an amount sends it here; if the hold no longer carries that amount the decision is
    # refused (409) rather than approving an amount nobody saw.
    expected_est_distributable_wst: float | None = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

# ── Biomimetic immune integration ─────────────────────────────────────────────

def _immune_threat() -> str:
    """Current immune threat level (NOMINAL | ELEVATED | HIGH | CRITICAL); safe if immune absent."""
    try:
        from agentic_core.organism.immune import immune
        return immune.status().get("threat_level", "NOMINAL")
    except Exception:
        return "NOMINAL"


# The immune system's defensive reconfiguration levers — SAFE, REVERSIBLE config changes only,
# escalating with threat. Applied via the reconfiguration engine under arms-length CCA governance.
# §8 (W318) — honesty rule: a lever may report 'implemented' ONLY when a real consumer is wired
# to it. Every lever names its consumer here; setting a lever with no wired consumer records
# 'lever_set_no_consumer' instead — no future lever ships decorative.
_LEVER_CONSUMERS: dict[str, str] = {
    # W438 refactor of this map against a grep of actual readers: temperature_bias was listed here
    # with "ai.gateway generation parameters (per-call)" — but its only behavioural read sits in
    # gateway._call, which nothing invokes (the native orchestrator superseded it and never reads
    # reconfig). Recording the ELEVATED defence as "implemented" against a consumer that does not
    # exist violated this map's own W318 rule; that defence now honestly records
    # lever_set_no_consumer until a real consumer is wired.
    "metabolic_throttle": "organism.heartbeat evolve tick (suppressed at low ATP) — W310",
    "immune_quarantine": "self_healing.is_open strict containment + attempt_heal hold — W318",
    "evolution_auto_apply": "organism.heartbeat post-approval auto-apply — W310",
    "rpm_limit": "ai.gateway rate limiter (re-synced ~30s via _sync_reconfig)",
}

_IMMUNE_DEFENCE: dict[str, dict] = {
    "ELEVATED": {"section": "gateway",  "key": "temperature_bias",  "value": "precise", "tier": "LOW",
                 "why": "Elevated error patterns — tighten generation to precise."},
    "HIGH":     {"section": "organism", "key": "metabolic_throttle", "value": True,     "tier": "LOW",
                 "why": "High threat — throttle metabolic load to relieve the organism."},
    "CRITICAL": {"section": "organism", "key": "immune_quarantine",  "value": True,     "tier": "MEDIUM",
                 "why": "Critical threat — quarantine failing endpoints (innate containment)."},
}


def _blend_clause(ctx: dict) -> str:
    """What the blended composite actually is, in THIS state - computed, never asserted.

    W494 (refutation) - the first version hard-coded "carries a defaulted and a simulated term and
    cannot fall below 0.6, so it could not have refused" into every permanent CCA record. Both clauses
    are false once a circuit is tracked: self-healing is then MEASURED (no defaulted term) and the blend
    can and does fall below 0.6 - reproduced at 0.472 with eight real record_failure calls, a sentence
    contradicted by the number printed inside it. A verdict's basis that cannot come out otherwise is
    the very class this round removes, so this derives every clause from composite_health_terms.
    """
    terms = ctx.get("composite_health_terms") or {}
    unmeasured = [(k, t) for k, t in terms.items() if isinstance(t, dict) and not t.get("measured")]
    if not terms:
        return (f"the blended figure {ctx.get('composite_health')} is a fallback constant - the organism "
                f"context errored, so no term was measured")
    if not unmeasured:
        return (f"the blended figure {ctx.get('composite_health')} is measured throughout, and the "
                f"decision was still taken on the measured-only score so the two agree")
    # the blend's FLOOR is the sum of the unmeasured terms' contributions: the measured ones can go to 0
    floor = 0.0
    for _k, t in unmeasured:
        floor += float(t.get("weight") or 0) * float(t.get("value") or 0)
    names = ", ".join(k.replace("_", " ") for k, _t in unmeasured)
    return (f"the blended figure {ctx.get('composite_health')} carries {len(unmeasured)} unmeasured "
            f"term(s) ({names}), which hold it at or above {round(floor, 3)} whatever the measured terms "
            f"read - so it cannot refuse below that, and the decision was taken on the measured part")


async def submit_change(req: SubmitChangeRequest, principal: str | None = None) -> dict:
    """Submit a change request to the Change Control Agency.

    W459 — this is the plain CORE, callable in-process (the compliance screen, the VSB evolution
    gate, homeostasis, the Sovereign Evolution Office and the transformation pipeline all call it
    without a request). The HTTP route below reads the authenticated principal and passes it in;
    a FastAPI dependency must NEVER be added here, or those callers would receive a Depends
    sentinel instead of an identity.

    W438 — a change may carry a structured `config_change` payload; it is validated and coerced
    HERE (so nothing unappliable can be approved), and /implement APPLIES it through the
    reconfiguration engine's audited core. Governed live levers are forced to config_major
    (MEDIUM — never auto-approved as a minor tweak)."""
    # W463 — the economy's materiality holds are filed by the economy itself (governance.py writes them
    # directly). A submitted change carrying their type or title prefix was indistinguishable from one:
    # a LOW 'config_minor' request titled "[economy] material distribution — <vsb>" was auto-approved
    # here and released a 4,000,000-WST distribution nobody reviewed. Refused for every caller.
    _title = req.title.strip().lower()
    # W502 (FU-035) — the contract-settlement hold title is reserved with the other two. A new hold
    # title that is NOT reserved here is one a submitted change can impersonate, which is the W463
    # hole this check exists to close.
    if req.change_type == "economy_material" or _title.startswith(("[economy] material distribution",
                                                                    "[economy] material transfer",
                                                                    "[economy] material contract settlement")):
        raise HTTPException(status_code=422, detail=(
            "change_type 'economy_material' and the '[economy] material distribution/transfer/contract "
            "settlement' titles are "
            "reserved for the economy's own materiality holds, which it files and keeps current itself; run "
            "the action (a cycle or transfer) and decide the hold it files in the Governance hub's Sovereign Sanctum."))
    cca_id = f"cca-{uuid.uuid4().hex[:10]}"
    change_type = req.change_type
    cc = req.config_change
    if cc is not None:
        from agentic_core.organism.reconfiguration import (coerce_value, _GOVERNED_KEYS,
                                                           _DEFAULT_CONFIG, wiring_for)
        if cc.reset:
            if cc.section or cc.key:
                raise HTTPException(status_code=422,
                                    detail="config_change: pass either reset:true OR section/key/value, not both")
            change_type = "config_major"
        else:
            if not cc.section or not cc.key:
                raise HTTPException(status_code=422,
                                    detail="config_change needs section and key (or reset: true)")
            if cc.section not in _DEFAULT_CONFIG or not isinstance(_DEFAULT_CONFIG.get(cc.section), dict):
                raise HTTPException(status_code=422, detail=f"Unknown config section: {cc.section}")
            try:
                cc.value = coerce_value(cc.section, cc.key, cc.value)
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e))
            if (cc.section, cc.key) in _GOVERNED_KEYS:
                change_type = "config_major"   # a live lever is never a minor tweak
    tier = _determine_tier(change_type, req.description)
    # W505 (FU-157, S1.18) — WHY the tier is what it is. The form shows a type's tier before submitting and a
    # phrase in the description can raise it to CRITICAL; the record carried no trace, so the page appeared to
    # contradict itself. `_raised_by` is None whenever the type's own tier stands.
    _raised_by = _tier_raise(req.description)
    _tier_from = _TIER_MAP.get(change_type, "MEDIUM")
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    # the name on the record is the authenticated one when there is one; otherwise the caller's
    _by = principal or req.submitted_by or "system"

    #  W581 (FU-313) — THE COMMITMENT, and the capacity it is made against.
    #  `confidence` is stored as DECLARED, never as measured: §2 of the capacity model admits a
    #  probability about SELF as a measurement, and a figure a caller supplies is not one. A commitment
    #  with no basis is refused rather than stored, because a number this platform cannot explain is the
    #  thing it spends every round removing.
    _commitment = None
    if req.committed_rounds is not None or req.confidence is not None:
        if not (req.commitment_basis or "").strip():
            raise HTTPException(
                status_code=422,
                detail="a commitment must say what it is based on: committed_rounds or confidence was "
                       "given with no commitment_basis, and an unexplained figure on a governance record "
                       "is read by a later round as a measurement")
        if req.confidence is not None and not (0.0 <= float(req.confidence) <= 1.0):
            raise HTTPException(status_code=422,
                                detail=f"confidence must be a fraction between 0 and 1, not "
                                       f"{req.confidence!r}")
        if req.committed_rounds is not None and int(req.committed_rounds) < 1:
            raise HTTPException(status_code=422,
                                detail="committed_rounds must be at least 1 - a promise of zero rounds "
                                       "is not a commitment")
        #  THE CAPACITY IS MEASURED, not declared, and says so. It is the platform's own observed round
        #  length from its commit history, which is what makes a promise in ROUNDS mean anything.
        _capacity, _cap_basis = None, None
        try:
            import importlib.util as _ilu313
            _sf313 = _ROOT_FOR_FORECAST / "scripts" / "session_forecast.py"
            if _sf313.exists():
                _spec313 = _ilu313.spec_from_file_location("_sf313", _sf313)
                _mod313 = _ilu313.module_from_spec(_spec313)
                _spec313.loader.exec_module(_mod313)
                _d313 = _mod313.round_durations()
                if _d313.get("assessable"):
                    _capacity = {"median_hours_per_round": _d313.get("median_h"),
                                 "p25_hours": _d313.get("p25_h"), "p75_hours": _d313.get("p75_h"),
                                 "rounds_measured": _d313.get("n")}
                    _cap_basis = str(_d313.get("basis") or "")[:300]
                else:
                    _cap_basis = ("NOT MEASURED: " + str(_d313.get("basis") or "the forecaster could "
                                  "not assess the round history")[:260])
            else:
                _cap_basis = "NOT MEASURED: the round-history forecaster is not present in this checkout"
        except Exception as _exc313:
            _cap_basis = (f"NOT MEASURED: the round history could not be read "
                          f"({_exc313.__class__.__name__})")
        _commitment = {
            "committed_rounds": req.committed_rounds,
            "confidence": req.confidence,
            #  the one thing a later reader must not get wrong about this record
            "confidence_is_declared": req.confidence is not None,
            # W581 — FOLDED. The page renders the word "declared" from `confidence_is_declared`, so a
            # second prose field saying the same thing reached no surface. The attribution is not lost:
            # it is appended to the basis the chip's title already shows.
            "basis": ((req.commitment_basis or "").strip()[:400]
                      + (" (the confidence above is DECLARED BY THE SUBMITTER, not measured by this "
                         "platform)" if req.confidence is not None else "")),
            "capacity_at_submit": _capacity,
            "capacity_basis": _cap_basis,
        }

    change = {
        "cca_id": cca_id,
        "title": req.title,
        "change_type": change_type,
        "config_change": (cc.model_dump() if cc is not None else None),
        "description": req.description,
        "rationale": req.rationale,
        "affected_systems": req.affected_systems,
        "submitted_by": _by,
        **({"submitted_by_claimed": req.submitted_by}
           if (principal and "submitted_by" in req.model_fields_set
               and req.submitted_by and req.submitted_by != principal) else {}),
        "submitted_by_verified": bool(principal) and auth_enabled(),
        "submitted_at": now,
        "impact_tier": tier,
        **({"impact_tier_raised_by": _raised_by, "impact_tier_raised_from": _tier_from,
            "impact_tier_raised_because": (
                f"the description names {_raised_by!r}, which raises any change to CRITICAL whatever its "
                f"declared type ({change_type} is normally {_tier_from}). Failing closed on a description "
                f"that names something constitutional or organism-wide is deliberate.")}
           if _raised_by and tier != _tier_from else {}),
        "status": "submitted",
        "vsb_id": req.vsb_id,
        "rollback_plan": req.rollback_plan,
        "review_result": None,
        # W581 (FU-313) — the promise, and the variance that can only be read once there is an outcome.
        # `variance` is None with a REASON rather than absent, so a reader can tell "not yet" from
        # "nobody measured it" — the distinction this programme keeps paying for elsewhere.
        "commitment": _commitment,
        "variance": None,
        "variance_basis": ("no outcome yet, so there is nothing to compare the commitment against"
                           if _commitment else "no commitment was recorded, so no variance is defined"),
        "decision": None,
        "reviewed_at": None,
        "implemented_at": None,
        "audit_trail": [{"event": "submitted", "ts": now, "by": _by,
                         "by_verified": bool(principal) and auth_enabled()}],
    }

    # AUTO-APPROVE low-tier changes only when the organism is healthy AND the immune system is not
    # under active threat — biomimetic: do NOT push changes while the organism is fighting an
    # infection (HIGH/CRITICAL immune threat holds even LOW changes for human/AI review).
    ctx = biobus.organism_context()
    threat = _immune_threat()
    change["immune_threat_at_submit"] = threat
    # §5 (W494, FU-107/FU-116) — the health leg of this gate could not refuse. It read the BLENDED
    # composite, which is 0.4·immune + 0.4 (self-healing defaulted to 1.0 when no circuit is tracked)
    # + 0.2·atp, and the ATP simulator only ever rises, so within about half a minute of a process's
    # reads the blend is >= 0.6 for EVERY immune value, including 0.0 with threat CRITICAL. A gate
    # that cannot refuse is not a gate: it grants. It decides on the MEASURED score now, and where too
    # little is measured to decide it HOLDS for review rather than granting on absent evidence.
    # Decided on the measured score whenever there IS one: immune health is a real measurement of the
    # thing that matters most here (errors in the window and the threat level), and gating on it gives
    # the rule a failing branch it never had. Only a context that measured NOTHING holds.
    _measured = ctx.get("composite_health_measured_only")
    _health_decidable = _measured is not None
    _health_ok = bool(_health_decidable and float(_measured) >= 0.6)
    change["health_gate"] = {
        "decided_on": "composite_health_measured_only" if _health_decidable else None,
        "measured_health": _measured,
        "measured_weight": ctx.get("composite_health_measured_weight"),
        "verdict": ("pass" if _health_ok else "held_not_decidable" if not _health_decidable else "fail"),
        # W494 (refutation) - this sentence was hard-coded and stated two clauses that are false
        # whenever a circuit is tracked. It is computed from the terms now.
        "basis": (f"decided on the measured part of the composite "
                  f"({float(ctx.get('composite_health_measured_weight') or 0):.0%} of its weight); "
                  + _blend_clause(ctx)
                  if _health_decidable else
                  "nothing was measured (the organism context errored), so the auto-approval is "
                  "HELD for review rather than granted on absent evidence"),
    }
    if tier == "LOW" and _health_ok and threat in ("NOMINAL", "ELEVATED"):
        change["status"] = "approved"
        change["decision"] = "auto_approved"
        # W464 — every record says what decided it (the mechanism, named)
        change["decision_source"] = "low_tier_auto_approval"
        change["reviewed_at"] = now
        change["review_result"] = (
            f"Auto-approved: LOW impact, measured organism health "
            f"{float(_measured):.0%} (over {float(ctx.get('composite_health_measured_weight') or 0):.0%} "
            f"of the composite's weight, the part that is measured), immune threat {threat}.")
        change["audit_trail"].append({"event": "auto_approved", "ts": now, "by": "biobus", "immune_threat": threat})
        biobus.fire_signal("motor", "cca.auto_approve", f"Auto-approved: {req.title}", 0.3)
    else:
        if tier == "LOW" and threat in ("HIGH", "CRITICAL"):
            change["review_result"] = (f"Held for review: immune threat {threat} — auto-approval paused "
                                       "while the organism defends itself.")
            change["audit_trail"].append({"event": "held_immune_threat", "ts": now, "by": "biobus",
                                          "immune_threat": threat})
        elif tier == "LOW" and not _health_decidable:      # the context measured nothing at all
            # W494 — a LOW change is no longer auto-approved on a score that is mostly unmeasured; the
            # record says which part could not be assessed rather than implying the organism failed.
            change["review_result"] = (
                "Held for review: the organism's composite health is not decidable — "
                + (ctx.get("mode_decidable_basis") or "")
                + ". Auto-approval requires a measured health signal.")
            change["audit_trail"].append({"event": "held_health_not_decidable", "ts": now,
                                          "by": "biobus",
                                          "measured_weight": ctx.get("composite_health_measured_weight")})
        elif tier == "LOW":
            change["review_result"] = (
                f"Held for review: measured organism health "
                f"{float(_measured):.0%} is below the 60% auto-approval threshold.")
            change["audit_trail"].append({"event": "held_measured_health", "ts": now, "by": "biobus",
                                          "measured_health": _measured})
        biobus.fire_signal("sensory", "cca.submit", f"Change submitted: {req.title} [{tier}] (immune: {threat})", 0.5)

    # ── THE METHOD GATE, ARMS-LENGTH (W508, P2.10(c)) ────────────────────────────────────────────────────
    # Every submission is checked against the delivery method the agency holds, from the REPO'S OWN
    # ARTEFACTS and never from what the submitter claims about itself. Three states per requirement, and
    # NOT_ASSESSABLE is the majority answer by design: a change record cannot show whether a blind was added
    # or whether a basis string was computed rather than asserted, and reporting those as MET would be the
    # exact defect the method exists to remove.
    #
    # THE ONE TEETH THIS GATE HAS: a change may not be AUTO-approved while a mechanically-checkable
    # requirement is UNMET. A NOT_ASSESSABLE requirement never blocks anything, because that would block
    # every change and turn the gate into a stop sign rather than a check.
    try:
        from agentic_core.api.method import check_change as _method_check
        change["method_check"] = _method_check(change)
    except Exception as _me:                       # noqa: BLE001 — recorded, and it does not pass by default
        change["method_check"] = {
            "method_available": False, "may_auto_approve": False,
            "summary": f"the method check could not run ({_me.__class__.__name__}: {_me})",
            "why_not_approvable": ("the method check did not run, so this change is not reported as checked; "
                                   "refusing the auto-approval is the honest state, not passing it")}
    if change["status"] == "approved" and change["method_check"].get("may_auto_approve") is False:
        change["status"] = "submitted"
        change["auto_approval_withheld"] = change["method_check"].get("why_not_approvable")
        change["audit_trail"].append({
            "event": "auto_approval_withheld_by_method_gate", "ts": now, "by": "method_gate",
            "why": change["method_check"].get("why_not_approvable"),
            "note": ("the change stands as submitted and may still be approved by review; only the AUTOMATIC "
                     "approval is withheld, and only for a requirement the platform could actually check")})

    # ── THE APPRAISAL CELL (W510) — the change against its SCOPE's real state ────────────────────────────
    # A reviewer sees the change against what is actually finished, blocked and moved-under in the scope it
    # declares, rather than against the change's own description of itself. Best-effort and NEVER a gate: an
    # appraisal is eight readings and two of its faculties are largely judgement, so gating on it would be a
    # judgement wearing a gate's clothes. Its absence is SAID, never a silent omission.
    try:
        from agentic_core.api.method import appraise_scope_for
        _sc = appraise_scope_for(change.get("affected_systems") or [])
        if _sc.get("slot"):
            # AWAITED, not asyncio.run: this function is async and inside a running loop, where asyncio.run
            # raises. The cell's Depends default is resolved only by FastAPI, so user=None is right in-process.
            from agentic_core.api.method import appraise as _appraise_cell
            _ap = await _appraise_cell(scope=_sc["slot"], user=None)
            change["scope_appraisal"] = {
                "scope": _sc["slot"], "why_this_scope": _sc.get("why"),
                "faculties": {k: _ap["faculties"][k] for k in ("reflection", "reasoning", "extrospection")
                              if k in _ap["faculties"]},
                "full": f"GET /api/v1/method/appraise?scope={_sc['slot']}",
                "not_a_gate": ("eight readings, not a verdict. Nothing here refuses or approves a change, and "
                               "two of the cell's faculties are largely judgement."),
            }
        else:
            change["scope_appraisal"] = {"scope": None, "why_this_scope": _sc.get("why"),
                                         "not_a_gate": "no scope was inferred, so none is appraised"}
    except Exception as _ae:                     # noqa: BLE001 — said, never a silent omission
        change["scope_appraisal"] = {"scope": None, "unavailable": f"{_ae.__class__.__name__}: {_ae}",
                                     "not_a_gate": "an appraisal never gates a change"}

    _save_change(change)
    ueg_logged = None
    if change["status"] == "approved":
        # W464 (FU-013) — an auto-approval is a decision; the submission itself stays in the audit trail
        ueg_logged = _log_decision({"type": "cca.change_approved", **_decision_fields(change),
                                    "decision": "approved", "decision_source": "low_tier_auto_approval",
                                    "decided_by": "biobus", "by": "biobus", "by_verified": False,
                                    "immune_threat": threat,
                                    # W494 — the UEG recorded only the blended score, which is the one
                                    # figure that could not have refused; both travel now
                                    "composite_health": round(float(ctx["composite_health"]), 4),
                                    "composite_health_measured_only": _measured,
                                    "composite_health_measured_weight":
                                        ctx.get("composite_health_measured_weight"),
                                    "decided_on": "composite_health_measured_only"})
    return {
        "cca_id": cca_id,
        "impact_tier": tier,
        "status": change["status"],
        # W505 (FU-157) — the facts the caller needs to describe what happened. S1.11: the gate's own
        # measurement, so no caller has to invent the word "healthy" over a composite that is 60%
        # defaulted or simulated. S1.18: the tier raise, so a caller shown a type's tier before submitting
        # is told when the description changed it, and by which phrase.
        "health_gate": change.get("health_gate"),
        "immune_threat_at_submit": change.get("immune_threat_at_submit"),
        # W581 (FU-313) — THE COMMITMENT TRAVELS WITH THE SUBMISSION, for the same reason the method
        # check does: a promise stored on a record and absent from the response is a fact rendered
        # nowhere, and the caller that made the promise is exactly who needs to see what was kept of it
        # (the declared/measured labelling included). `variance_basis` comes too, so a caller reading
        # `variance: None` can tell "no outcome yet" from "no commitment was recorded".
        "commitment": change.get("commitment"),
        "variance": change.get("variance"),
        "variance_basis": change.get("variance_basis"),
        # W508 (P2.10(c)/(d)) — the method check TRAVELS WITH the submission. A check stored on a record and
        # absent from the response is a fact rendered nowhere, which is the shape this whole method warns of.
        "method_check": change.get("method_check"),
        # W512 — the SCOPE APPRAISAL travels with the submission too, for exactly the reason the line above
        # gives. It was written onto the record and omitted from this projection, and the omission was found by
        # reading a real submission's response and seeing "scope: None" for an appraisal that had in fact run
        # and found P3.12 with twelve matching rows. A fact stored on a record and absent from the response is
        # rendered nowhere — the writer-without-its-reader class this method exists to catch.
        "scope_appraisal": change.get("scope_appraisal"),
        **({"auto_approval_withheld": change["auto_approval_withheld"]}
           if change.get("auto_approval_withheld") else {}),
        **({"impact_tier_raised_by": change["impact_tier_raised_by"],
            "impact_tier_raised_from": change.get("impact_tier_raised_from"),
            "impact_tier_raised_because": change.get("impact_tier_raised_because")}
           if change.get("impact_tier_raised_by") else {}),
        **({"ueg_logged": ueg_logged} if ueg_logged is not None else {}),
        "message": f"Change request {cca_id} submitted. Tier: {tier}. Status: {change['status']}.",
    }


# NOTE: the decorator must sit directly above its handler — a helper def inserted between them
# silently rebinds the route (the endpoint then 422s at call time).
@router.post("/submit")
async def submit_change_route(req: SubmitChangeRequest,
                              user: dict | None = Depends(get_current_user)):
    """HTTP entry: stamps the authenticated principal (auth ON) or keeps the caller's name (OFF)."""
    return await submit_change(req, principal=_actor(user, req.submitted_by or "system"))


class ImmuneReconfigureRequest(BaseModel):
    # Default reads the LIVE immune threat. `simulate_threat` is an honest demonstration/test input
    # that exercises the defensive mapping without mutating global immune state.
    simulate_threat: str | None = None


def engage_immune_defence(threat: str | None = None, requested_by: str = "immune_system",
                         requested_by_verified: bool = False) -> dict:
    """The immune reconfigurator's UNGATED core. W506 (P2.7(3)).

    Extracted from the HTTP route so the organism can engage its own defence without crossing an admin
    perimeter, while the governed path and the reflex path stay ONE body of code - a second copy would
    drift the first time either changed (W475). The heartbeat calls this at threat >= HIGH; the route
    calls it on behalf of an admin and passes that admin as the REQUESTER, never as the decider.

    Everything here was already true of the route except the reversal: the prior value is now captured
    from the write path's own `old_value`, so `revert_immune_defence` has something to restore.
    """
    threat = (threat or _immune_threat()).upper()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    plan = _IMMUNE_DEFENCE.get(threat)
    if plan is None:
        # W506 (pre-flight) - the reversibility fields are carried here too. A caller that reads
        # `reversible` on every response got undefined from this branch, which reads as "not stated"
        # rather than "nothing was applied, so there is nothing to revert".
        # W581 — FU-334's class, found by the pre-flight on a function this round touched. The branch
        # below carries seven keys this one omitted, so a caller indexing `cca_id` or `status` on the
        # nominal path got undefined. None where nothing happened, with the reason beside it.
        return {"threat_level": threat, "action": "none", "governed_by": "Change Control Agency (arms-length)",
                "reversible": False, "reverts_to": None,
                "revert_with": "nothing to revert - no reconfiguration was applied",
                "cca_id": None, "impact_tier": None, "status": None, "applied": None,
                "reconfiguration": None, "ueg_logged": None,
                "message": "no defensive reconfiguration was required, so no change was filed",
                "reason": "Immune state nominal — no defensive reconfiguration required."}

    cca_id = f"cca-{uuid.uuid4().hex[:10]}"
    change = {
        "cca_id": cca_id,
        "title": f"Immune defence: {plan['section']}.{plan['key']} = {plan['value']}",
        "change_type": "immune_reconfiguration",
        "description": plan["why"],
        "rationale": f"Immune threat level {threat}; defensive, reversible reconfiguration.",
        "affected_systems": ["organism", plan["section"], "immune_system", "reconfiguration_engine"],
        "submitted_by": "immune_system",
        "submitted_at": now,
        "impact_tier": plan["tier"],
        "status": "submitted",
        "immune_threat_at_submit": threat,
        # W459 — `requires_ratification` was set here and read NOWHERE in the repo: the record said
        # "flagged for Board ratification" while marking itself implemented in the same request.
        # The flag is gone. W464: Board ratification now exists (awaiting_board_ratification), for HIGH
        # changes a review approved; this reflex is LOW/MEDIUM and decided by the mechanism, so it is outside it.
        # W506 (P2.7(3)) - this said "revert to its prior value" and no prior value was stored. Now the
        # plan names the mechanism that exists, and `reversible` below is set only when the prior value was
        # actually captured, so a failed apply does not leave a record promising a rollback.
        "rollback_plan": f"revert_immune_defence({cca_id!r}) restores {plan['section']}.{plan['key']} to "
                         f"the value captured when this change was applied",
        "reversible": False,
        "reverts_to": None,
        "review_result": None, "decision": None, "reviewed_at": None, "implemented_at": None,
        "audit_trail": [{"event": "submitted", "ts": now, "by": "immune_system", "immune_threat": threat,
                         "requested_by": requested_by, "by_verified": requested_by_verified}],
    }
    biobus.fire_signal("sensory", "cca.immune_reconfigure", f"Immune defence proposed [{threat}]", 0.6)

    # Arms-length governance: auto-approve the defensive (reversible) reconfiguration, then apply it.
    change["status"] = "approved"
    change["decision"] = "auto_approved_immune_defence"
    change["decision_source"] = "immune_defence_reflex"   # W464 — the mechanism that decided, named
    change["reviewed_at"] = now
    change["review_result"] = f"Auto-approved defensive reconfiguration under immune threat {threat}."
    # the reflex decided, not the caller — the caller's identity is never stamped as the decider
    change["audit_trail"].append({"event": "auto_approved", "ts": now, "by": "cca",
                                 "decided_by": "auto_approve_immune_defence"})

    applied = None
    try:
        # W438: the CCA's execution arm is the ungated core, not the HTTP route — the route now
        # refuses governed levers (that refusal exists precisely so THIS audited path is the only
        # way they change)
        from agentic_core.organism.reconfiguration import apply_config_change
        applied = apply_config_change(
            plan["section"], plan["key"], plan["value"],
            reason=f"Immune reconfigurator (threat={threat}, cca={cca_id})",
            updated_by="cca-immune")
        # W506 (P2.7(3)) - THE REVERSAL, captured. `rollback_plan` was a sentence saying to revert the
        # lever "to its prior value" while nothing stored that value: the record asserted reversibility in
        # three places and no mechanism could revert it. apply_config_change already returns `old_value`,
        # so the prior value was in hand and being discarded.
        if isinstance(applied, dict):
            change["reverts_to"] = {"section": plan["section"], "key": plan["key"],
                                    "value": applied.get("old_value")}
            change["reversible"] = True
        _consumer = _LEVER_CONSUMERS.get(plan["key"])
        if _consumer:
            change["status"] = "implemented"
            change["implemented_at"] = now
            _record_variance(change, now, "implemented")      # W581 (FU-313)
            change["audit_trail"].append({"event": "implemented", "ts": now, "applied": applied,
                                          "consumer": _consumer})
        else:
            # W318 honesty — the lever was SET but nothing consumes it: never claim 'implemented'
            change["status"] = "approved"
            change["audit_trail"].append({"event": "lever_set_no_consumer", "ts": now,
                                          "applied": applied,
                                          "note": "config value set; no wired consumer exists"})
        biobus.fire_signal("motor", "cca.immune_reconfigure.apply",
                           f"Applied immune defence: {plan['section']}.{plan['key']}={plan['value']}", 0.7)
    except Exception as e:
        change["audit_trail"].append({"event": "apply_failed", "ts": now, "error": str(e)})

    _save_change(change)
    # W464 (FU-013) — the reflex's approval is a decision. Written after the record is saved: the config_update node
    # the reconfiguration engine wrote precedes it in the chain.
    ueg_logged = _log_decision({"type": "cca.change_approved", **_decision_fields(change), "decision": "approved",
                                "decision_source": "immune_defence_reflex", "decided_by": "auto_approve_immune_defence",
                                "by": "cca", "by_verified": False, "requested_by": requested_by,
                                "requested_by_verified": requested_by_verified, "immune_threat": threat,
                                "implemented": change["status"] == "implemented"})
    # W581 — the nominal-state sibling above carries `action` and `reason`; a caller reading either here
    # got undefined. This branch DID reconfigure, so it says which action and why rather than omitting both.
    return {
        "cca_id": cca_id,
        "threat_level": threat,
        "impact_tier": plan["tier"],
        "status": change["status"],
        "action": "reconfigured",
        "reason": plan["why"],
        "ueg_logged": ueg_logged,
        "reconfiguration": {"section": plan["section"], "key": plan["key"], "value": plan["value"], "why": plan["why"]},
        "applied": applied,
        # W506 (P2.7(3)) - computed from whether the prior value was captured, never asserted
        "reversible": change["reversible"],
        "reverts_to": change["reverts_to"],
        "revert_with": (f"POST /api/v1/cca/immune-reconfigure/{cca_id}/revert" if change["reversible"]
                        else "nothing to revert - the lever was not applied, so no prior value was captured"),
        "governed_by": "Change Control Agency (arms-length)",
        "message": f"Immune reconfigurator: {threat} → {plan['section']}.{plan['key']}={plan['value']} ({change['status']}).",
    }


def revert_immune_defence(cca_id: str, reason: str = "") -> dict:
    """Restore the lever an immune defence moved, to the value captured when it was applied.

    W506 (P2.7(3)) - the mechanism the record used to describe in prose. It refuses rather than
    guesses: a change with no captured prior value cannot be reverted, and saying so is the honest
    answer where restoring a default would silently invent one.
    """
    change = _load_change(cca_id)
    if change is None:
        return {"cca_id": cca_id, "reverted": False, "reason": "no such change record"}
    if change.get("change_type") != "immune_reconfiguration":
        return {"cca_id": cca_id, "reverted": False,
                "reason": f"this path reverts immune reconfigurations; that record is a "
                          f"{change.get('change_type')}"}
    target = change.get("reverts_to")
    if not isinstance(target, dict) or not change.get("reversible"):
        return {"cca_id": cca_id, "reverted": False,
                "reason": "no prior value was captured for this change, so there is nothing to restore - "
                          "the lever was never applied, or it was applied before the capture existed"}
    if change.get("reverted_at"):
        return {"cca_id": cca_id, "reverted": False, "reason": "already reverted",
                "reverted_at": change["reverted_at"]}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        from agentic_core.organism.reconfiguration import apply_config_change
        applied = apply_config_change(
            target["section"], target["key"], target["value"],
            reason=f"Reverting immune defence {cca_id}" + (f": {reason}" if reason else ""),
            updated_by="cca-immune-revert")
    except Exception as exc:
        change["audit_trail"].append({"event": "revert_failed", "ts": now,
                                     "error": f"{exc.__class__.__name__}: {exc}"})
        _save_change(change)
        return {"cca_id": cca_id, "reverted": False,
                "reason": f"the write path refused the restore: {exc.__class__.__name__}: {exc}"}
    change["reverted_at"] = now
    change["status"] = "reverted"
    change["audit_trail"].append({"event": "reverted", "ts": now, "by": "cca-immune-revert",
                                 "restored": target, "applied": applied, "reason": reason})
    _save_change(change)
    ueg_logged = _log_decision({"type": "cca.change_reverted", **_decision_fields(change),
                                "decision": "reverted", "decision_source": "immune_defence_revert",
                                "decided_by": "revert_immune_defence", "by": "cca",
                                "by_verified": False, "restored": target})
    biobus.fire_signal("motor", "cca.immune_reconfigure.revert",
                       f"Reverted {target['section']}.{target['key']} to {target['value']}", 0.6)
    return {"cca_id": cca_id, "reverted": True, "restored": target, "applied": applied,
            "ueg_logged": ueg_logged, "status": change["status"],
            "message": f"Immune defence {cca_id} reverted: {target['section']}.{target['key']} "
                       f"restored to {target['value']}."}


@router.post("/immune-reconfigure")
async def immune_reconfigure(req: ImmuneReconfigureRequest = ImmuneReconfigureRequest(),
                             user: dict = Depends(require_admin)):
    """Immune-system reconfigurator, governed arms-length by the CCA.

    Biomimetic defence: when the immune system is under threat it proposes a SAFE, REVERSIBLE
    defensive reconfiguration (tighten generation -> throttle load -> quarantine failing endpoints).
    The CCA records it as a change-controlled, audited action and - because these are low-risk,
    reversible defensive levers - auto-approves and APPLIES it via the reconfiguration engine (a fast
    innate-immune reflex that is nonetheless governed). Admin-only: it applies governed live levers.

    W506 (P2.7(3)) - the body moved to `engage_immune_defence`, which the heartbeat also calls at
    threat >= HIGH. One body of code, two callers: the reflex is no longer a button nobody presses.
    The admin is recorded as the REQUESTER; the reflex remains the decider.
    """
    return engage_immune_defence(req.simulate_threat, _actor(user), _verified(user))


@router.post("/immune-reconfigure/{cca_id}/revert")
async def immune_reconfigure_revert(cca_id: str, user: dict = Depends(require_admin)):
    """Revert an immune defence to the lever value captured when it was applied. W506 (P2.7(3)).

    P2.7(3) requires the reversal to be DRIVEN rather than asserted, and before this the record
    carried a rollback SENTENCE over a prior value nothing had stored.
    """
    return revert_immune_defence(cca_id, reason=f"requested by {_actor(user)}")


@router.get("/ledger-gaps")
async def ledger_gaps():
    """W505 (FU-031) — decisions whose constitutional node is missing or unproven, so a reconciliation has
    something to read. A gap never undoes the decision; it says the audit trail is incomplete and where."""
    rows = decisions_missing_ledger_node()
    return {"gaps": rows, "total": len(rows),
            "marked": sum(1 for r in rows if r.get("kind") == "marked"),
            "unproven": sum(1 for r in rows if r.get("kind") == "unproven"),
            "rule": ("`marked` means a ledger write failed and said so. `unproven` means the record carries no "
                     "mark either way — decided before the mark existed, or a worker died between the record "
                     "landing and the write. Neither is a claim that the decision is invalid.")}


@router.get("/queue")
async def get_queue():
    """List all pending change requests awaiting review."""
    pending = _list_changes("submitted") + _list_changes("under_review")
    return {"queue": pending, "total": len(pending)}


@router.get("/approved")
async def get_approved():
    return {"changes": _list_changes("approved"), "total": len(_list_changes("approved"))}


@router.get("/rejected")
async def get_rejected():
    return {"changes": _list_changes("rejected"), "total": len(_list_changes("rejected"))}


@router.get("/implemented")
async def get_implemented():
    return {"changes": _list_changes("implemented"), "total": len(_list_changes("implemented"))}


@router.get("/{cca_id}")
async def get_change(cca_id: str):
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    # W464 — the tier it is decided under, and whether the approval waits for the Board (read-time; the stored
    # record keeps the tier it was filed with until a decision stamps the effective one)
    tier = effective_tier(c)
    return {**c, "impact_tier": tier,
            **({"impact_tier_filed": c.get("impact_tier")} if tier != c.get("impact_tier") else {}),
            # a record decided before W459 carries no decision_source: say what it is read as (approval_source)
            **({"decision_source": approval_source(c), "decision_source_inferred": True}
               if not c.get("decision_source") and approval_source(c) else {}),
            "awaiting_board_ratification": awaiting_board_ratification(c)}


async def _twin_prevalidate(change: dict) -> dict:
    """§17.5 invariant — pre-validation before a MAJOR change (HIGH/CRITICAL). There is no registered
    twin model: the serving resource is ASKED to forward-simulate the change over the live organism
    state and to end with [TWIN: PASS]/[TWIN: FAIL]. Only a single such marker counts as a model
    verdict (source twin_marker). With no marker, or both (the deterministic floor echoes the
    prompt), the verdict is the ORGANISM HEALTH GATE — pass only when the organism is healthy and not
    under immune threat — recorded as source health_gate_default, "no twin model — health gate only"."""
    ctx = biobus.organism_context()
    prompt = (
        f"You are the digital-twin simulator pre-validating a change BEFORE implementation.\n\n"
        f"Twin model — the live organism state:\n"
        # W494 (refutation) - the model was handed the blend after the rule stopped deciding on it
        f"  Measured composite health: {float(ctx.get('composite_health_measured_only') or 0):.0%} over "
        f"{float(ctx.get('composite_health_measured_weight') or 0):.0%} of the composite's weight "
        f"(the blended {ctx['composite_health']:.0%} is not what any gate decides on) | mode: {ctx['mode']}\n"
        f"  Immune threat: {ctx['immune']['threat_level']} | circadian: {ctx['circadian']['cycle']}\n\n"
        f"Proposed change ({effective_tier(change)}): {change['title']}\n"
        f"Type: {change['change_type']}\nDescription: {change['description']}\n"
        f"Affected systems: {', '.join(change.get('affected_systems') or []) or 'not specified'}\n"
        f"Rollback plan: {change.get('rollback_plan') or 'not provided'}\n\n"
        "Forward-simulate applying this change to the twin:\n"
        "## State Trajectory (immediately after → 24h → steady state)\n"
        "## Failure Modes Triggered (if any)\n"
        "## Rollback Viability\n"
        "## Verdict — end with exactly one of: [TWIN: PASS] or [TWIN: FAIL]"
    )
    try:
        # W506 (P2.2) - the pre-validation names the resource that ran it, beside the source label W459
        # already records. A verdict whose origin is unnamed is what the 17.5 invariant reads as holding.
        _tr = await gateway.query_meta(prompt, agent="cca_twin_prevalidation", timeout=25, augment=False)
        sim = _tr.get("output", "")
        _twin_served = _tr.get("served_by")
    except Exception as e:
        sim = f"[twin simulation unavailable: {e}]"
    up = (sim or "").upper()
    has_pass, has_fail = "[TWIN: PASS]" in up, "[TWIN: FAIL]" in up
    if has_pass and not has_fail:
        verdict, source = "pass", "twin_marker"
    elif has_fail and not has_pass:
        verdict, source = "fail", "twin_marker"
    else:
        # no marker — or BOTH markers (a floor/echo artifact, not a real verdict): fall back to the
        # honest organism health gate rather than trusting an echoed marker.
        # §17.5 (W494, FU-107/FU-116) — this fell back to a health gate that could not refuse, so on
        # the deterministic floor (the only branch reachable without a twin) the pre-validation always
        # returned PASS. It decides on the measured score, and where too little is measured it is
        # NOT ASSESSABLE — never a pass by default.
        _m = ctx.get("composite_health_measured_only")
        if _m is None:
            verdict, source = "not_assessable", "health_gate_not_decidable"
        else:
            healthy = float(_m) >= 0.6 and ctx["immune"]["threat_level"] in ("NOMINAL", "ELEVATED")
            verdict, source = ("pass" if healthy else "fail"), "health_gate_default"
    return {
        "verdict": verdict,
        "source": source,
        "composite_health_at_sim": ctx["composite_health"],
        "composite_health_measured_only_at_sim": ctx.get("composite_health_measured_only"),
        "composite_health_measured_weight_at_sim": ctx.get("composite_health_measured_weight"),
        "immune_threat_at_sim": ctx["immune"]["threat_level"],
        "summary": (sim or "")[:600],
        "simulated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        # W459 — this string was unconditional, so the health-gate fallback (the only branch the
        # deterministic floor can reach) claimed a forward simulation that never ran.
        "method": ("digital-twin forward simulation over the live organism state"
                   if source == "twin_marker" else
                   "no twin model — organism health gate only, decided on the MEASURED part of the "
                   "composite (>= 0.6) and immune threat in NOMINAL/ELEVATED; where too little is "
                   "measured the gate returns not_assessable rather than a pass. The proposed change "
                   "was NOT simulated"),
        "source_label": ("model twin verdict" if source == "twin_marker"
                         else "no twin model — health not decidable, nothing assessed"
                         if source == "health_gate_not_decidable"
                         else "no twin model — health gate only"),
    }


@router.post("/{cca_id}/twin-prevalidate")
async def twin_prevalidate(cca_id: str, user: dict | None = Depends(get_current_user)):
    """Run (or refresh) the §17.5 pre-validation for a change. Required before /implement on
    HIGH/CRITICAL tiers. With no twin model the verdict is an organism health gate, said so."""
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] in ("implemented", "withdrawn"):
        raise HTTPException(status_code=400, detail=f"Change is {c['status']} — pre-validation is moot.")
    tp = await _twin_prevalidate(c)          # the await stays OUTSIDE the lock
    principal = _actor(user)

    def _merge(fresh: dict) -> None:
        if fresh["status"] in ("implemented", "withdrawn"):
            raise HTTPException(status_code=400,
                                detail=f"Change is {fresh['status']} — pre-validation is moot.")
        fresh["twin_prevalidation"] = tp
        fresh.setdefault("audit_trail", []).append(
            {"event": f"twin_prevalidation_{tp['verdict']}", "ts": tp["simulated_at"],
             "source": tp["source"], "by": principal, "by_verified": _verified(user)})

    c = _update_change(cca_id, _merge)
    biobus.fire_signal("cognitive", "cca.twin_prevalidate",
                       f"Twin pre-validation {tp['verdict'].upper()}: {c['title']}", 0.6)
    return {"cca_id": cca_id, "twin_prevalidation": tp}


@router.post("/{cca_id}/review")
async def review_change(cca_id: str, req: ReviewDecision,
                        user: dict | None = Depends(get_current_user)):
    """
    Review a change request, or record an admin's explicit decision on it.

    W459 — three things changed. (1) An override is AUTHORISED before anything is written: with auth
    enabled only an admin principal may override, and a CRITICAL change additionally requires an
    explicit `admin_decision_for_critical`. (2) What a review can decide is explicit: a CRITICAL change
    is ALWAYS held for an explicit admin decision (a model marker is stored only as a recommendation;
    it used to be silently rejected by the health rule, and rejection is terminal). A single model
    marker decides a MEDIUM/HIGH change. With no marker, or conflicting markers, the organism-health
    threshold RULE decides it and the record says so — except that with auth enabled a rule verdict
    is applied only when an admin requested the review (a non-admin's review is held, with the rule's
    verdict as a recommendation). (3) The decision is
    stamped with WHO asked (`by`, `by_verified`) and WHAT decided (`decided_by`), instead of an
    unconditional "cca_ai" on a human's override.

    W464 — the tier is the record's EFFECTIVE tier (effective_tier), stamped on the record when the review starts.
    Economy materiality holds are CRITICAL (FU-014): a review of one records a recommendation only, and the Owner's
    explicit decision (with admin_decision_for_critical) decides it; the §17.5 pre-validation is not run for one (its
    implement path never reads it). A HIGH change a review approves waits for Board ratification (FU-012). Every
    decision — not a hold — is written to the UEG after the record lands (FU-013); the response says `ueg_logged`.
    """
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] not in ("submitted", "under_review"):
        raise HTTPException(status_code=400, detail=f"Change is {c['status']} — cannot review.")

    principal = _actor(user)
    # W464 (FU-014) — decided under the EFFECTIVE tier: the change type fixes the floor, and it never changes
    tier = effective_tier(c)
    if req.override_decision:
        u = _principal(user)
        if auth_enabled() and (not u or u.get("role") != "admin"):
            raise HTTPException(status_code=403,
                                detail="Only an admin may override a Change Control decision.")
        if (_TIER_RANK[tier] >= _TIER_RANK["HIGH"] and tier != "CRITICAL"
                and not (req.owner_decision_acknowledged or req.admin_decision_for_critical)):
            raise HTTPException(status_code=403, detail=(
                f"A {tier} change decided by override skips Board ratification, because an override is "
                f"recorded as the Owner's own decision. Resend with owner_decision_acknowledged: true to "
                f"record this as the Owner's explicit decision, or omit override_decision to have it "
                f"reviewed and ratified."))
        if tier == "CRITICAL" and not req.admin_decision_for_critical:
            raise HTTPException(status_code=403, detail=(
                "A CRITICAL change is never decided incidentally: resend with "
                "admin_decision_for_critical: true to record this as an explicit admin decision."
                + (" A material economy action is CRITICAL: it is decided only by the Owner's explicit decision "
                   "(the Governance hub's Sovereign Sanctum)." if c.get("change_type") == "economy_material" else "")))

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def _start(fresh: dict) -> None:
        if fresh["status"] not in ("submitted", "under_review"):
            raise HTTPException(status_code=409,
                                detail=f"Change was decided concurrently (status {fresh['status']}).")
        if (req.expected_est_distributable_wst is not None and fresh.get("est_distributable_wst") is not None
                and abs(float(fresh["est_distributable_wst"]) - float(req.expected_est_distributable_wst)) > 0.005):
            raise HTTPException(status_code=409, detail=(
                f"The hold's amount changed since it was read: it now carries {fresh['est_distributable_wst']} WST, "
                f"not {req.expected_est_distributable_wst}. Re-read it and decide the current amount."))
        _stamp_effective_tier(fresh)
        fresh["status"] = "under_review"
        fresh.setdefault("audit_trail", []).append(
            {"event": "review_started", "ts": now, "by": principal, "by_verified": _verified(user)})

    c = _update_change(cca_id, _start)
    tier = effective_tier(c)
    # W463 — what the reviewer is deciding: an economy hold's amount and intake as they stood at the start
    reviewed_amount = (c.get("est_distributable_wst"), c.get("intake"))

    biobus.fire_signal("cognitive", "cca.review", f"Reviewing: {c['title']}", 0.6)

    held, hold_reason, recommendation = False, None, None
    # W505 (FU-033) - bound for BOTH branches: `_decide` below closes over it, and an override never reaches
    # the review branch that computes it.
    _absent: list = []
    if req.override_decision:
        decision, decision_source = req.override_decision, "admin_override"
        review_text = f"Manual override: {req.reviewer_notes or 'No notes.'}"
        # W505 (FU-030) — stamped, so a HIGH override that was NOT acknowledged is findable afterwards.
        _ack_override = bool(req.owner_decision_acknowledged or req.admin_decision_for_critical)
    else:
        # a review by the serving resource (a model, or the deterministic floor)
        ctx = biobus.organism_context()
        # W505 (FU-033) — which of the review-bearing fields this record simply does not have
        _absent = [_f for _f in ("rationale", "affected_systems", "rollback_plan") if not c.get(_f)]
        prompt = (
            f"You are the Chief Governance Officer of Workstation IDBO, reviewing a change request.\n\n"
            f"Change Title: {c['title']}\n"
            f"Type: {c['change_type']}\n"
            f"Impact Tier: {tier}\n"
            f"Description: {c.get('description') or 'Not provided.'}\n"
            # W505 (FU-033) — .get, not []. A record written without these raised KeyError here, AFTER
            # _start had already moved it to under_review, leaving the change stuck in a state no review
            # could leave. The absences are NAMED below rather than papered over: a change with no
            # rollback plan is a different proposition from one that has one.
            f"Rationale: {c.get('rationale') or 'Not provided.'}\n"
            f"Affected Systems: {', '.join(c.get('affected_systems') or []) or 'Not specified.'}\n"
            f"Rollback Plan: {c.get('rollback_plan') or 'Not provided.'}\n"
            + (f"RECORD INCOMPLETE — this change was submitted without: {', '.join(_absent)}. Weigh that in "
               f"your assessment; do not assume the missing parts are satisfactory.\n\n" if _absent else "\n")
            + 
            f"Current Organism Health:\n"
            # W494 (refutation) - same: the reviewer saw only the blend
            f"  Measured composite health: {float(ctx.get('composite_health_measured_only') or 0):.0%} "
            f"over {float(ctx.get('composite_health_measured_weight') or 0):.0%} of the composite's "
            f"weight; the blended figure is {ctx['composite_health']:.0%} and is not what the rule "
            f"decides on\n"
            f"  Immune threat: {ctx['immune']['threat_level']}\n"
            f"  Organism mode: {ctx['mode']}\n"
            f"  Circadian cycle: {ctx['circadian']['cycle']}\n\n"
            f"Assess this change against:\n"
            f"1. Necessity — is this change truly needed?\n"
            f"2. Risk — what could go wrong? Is the rollback plan adequate?\n"
            f"3. Timing — is now the right time given organism health?\n"
            f"4. Alignment — does this align with the IDBO mission and constitution?\n"
            f"5. Decision — APPROVED or REJECTED, with one clear sentence of reasoning.\n\n"
            f"End your response with exactly one of: [DECISION: APPROVED] or [DECISION: REJECTED]"
        )
        # W505 (FU-157, S1.12) — WITH PROVENANCE. `query` returns bare text, so the record below called the
        # prose "the model's" even when the deterministic floor wrote it, which is the normal case when no
        # local model is present. query_meta says what served it.
        # W505 — `augment=False` STATED, not inherited. A repo-wide guard requires every query_meta call
        # site to name its recall decision: W489 flipped the default after 29 generation callers had
        # another request's content prepended and presented as analysis of their own subject, and an
        # inherited default is exactly what let that go unnoticed for 29 sites.
        # §17.5 invariant 1 (W343, FU-276) — the caller's identity reaches the memory layer, or what they asked for is stored where even they cannot recall it.
        _owner_id = user.get("username") if isinstance(user, dict) else None
        _rv = await gateway.query_meta(prompt, agent="cca_review", augment=False, owner_id=_owner_id)
        review_text = _rv.get("output", "")
        _served = str(_rv.get("served_by") or "unknown")
        # the GATEWAY's own floor test, which imports the engine's declared name instead of matching a
        # string. A second, weaker test here (looking for "engine" in the name) reported the floor as
        # "the serving resource 'native'", which says no more than the old sentence did.
        from agentic_core.ai.gateway import ModelGateway as _MG
        _is_floor = bool(_MG._is_floor(_served)) and not _rv.get("is_external")
        # a NOUN PHRASE: it lands mid-sentence in three places, and a clause here ("— not a model") read as
        # "...written by the floor, not a model and had NO bearing on the decision."
        _writer = ("Workstation's own deterministic native engine (the floor, which is not a model)"
                   if _is_floor else f"the serving resource '{_served}'")

        _up = (review_text or "").upper()
        _yes, _no = "[DECISION: APPROVED]" in _up, "[DECISION: REJECTED]" in _up
        marker = "approved" if (_yes and not _no) else "rejected" if (_no and not _yes) else None
        why_no_marker = ("the serving resource returned BOTH [DECISION: APPROVED] and [DECISION: REJECTED] "
                         "(conflicting markers)" if (_yes and _no) else
                         "no [DECISION: …] marker was returned")
        # §5 (W494, FU-107) — this decided on the blended composite, and 0.4·immune + 0.4 + 0.2·atp
        # is >= 0.5 for every immune value once the (only-rising) ATP term passes 0.5, which happens
        # within seconds of boot. So "composite_health >= 0.5 → approved" could not reject anything,
        # and MEDIUM changes became implementable on a rule that had no failing branch. It decides on
        # the MEASURED score; where too little is measured, there is no rule verdict at all and the
        # change is HELD for an explicit decision rather than approved by default.
        _h = float(ctx["composite_health"])
        _hm = ctx.get("composite_health_measured_only")
        rule_verdict = (None if _hm is None else
                        "approved" if float(_hm) >= 0.5 else "rejected")
        # print the value with enough precision that the stated comparison is TRUE as written (0.4999
        # rounded to "0.50 < 0.5" was a false sentence in the record)
        if rule_verdict is None:
            # W494 - a rule with no evaluable input has no verdict; writing "< 0.5 -> None" would
            # put a false sentence in the permanent record
            rule_clause = ("the organism-health threshold rule could NOT be evaluated: "
                           + (ctx.get("mode_decidable_basis") or "nothing was measured"))
        else:
            _mh = float(_hm)
            _shown = next(f"{_mh:.{n}f}" for n in range(2, 12)
                          if (float(f"{_mh:.{n}f}") >= 0.5) == (_mh >= 0.5))
            # W494 (refutation) - "the blended {_h} has no failing branch" was hard-coded, and it
            # printed "the blended 0.27 has no failing branch" for a blend that WOULD have failed this
            # very 0.5 rule. The clause is derived from the terms.
            rule_clause = (f"MEASURED composite_health {_shown} "
                           f"{'>=' if rule_verdict == 'approved' else '<'} 0.5 → {rule_verdict}"
                           f" (that is the measured part, "
                           f"{float(ctx.get('composite_health_measured_weight') or 0):.0%} of the "
                           f"composite's weight; " + _blend_clause(ctx) + ")")
        _u = _principal(user)
        admin_requested = (not auth_enabled()) or bool(_u and _u.get("role") == "admin")
        model_out = f"\n\n--- output of {_writer} ---\n" + (review_text or "")
        if tier == "CRITICAL":
            # never decided by a review: a model marker is a recommendation; the rule never applies.
            # W464 — this now covers every economy materiality hold (FU-014), so the W463 branch that held only a hold
            # filed after a rejection is gone: no review decides any of them. The follows link stays information.
            decision, held, hold_reason = None, True, "critical_requires_admin_decision"
            decision_source = "held_awaiting_admin"
            recommendation = ({"verdict": marker, "source": "model_decision_marker"} if marker else None)
            _follows = c.get("follows_rejection") if isinstance(c.get("follows_rejection"), dict) else None
            review_text = (
                ("HELD — a material economy action is CRITICAL: it is decided only by the Owner's explicit decision "
                 "(the Governance hub's Sovereign Sanctum). "
                 + (f"It follows the rejection of {_follows.get('cca_id')}. " if _follows else "")
                 if c.get("change_type") == "economy_material" else
                 "HELD — a CRITICAL change is decided only by an explicit admin decision. ")
                + (f"{_writer.capitalize()} recommended {marker.upper()}; that is recorded as a "
                   "recommendation, not a decision." if marker else
                   f"No recommendation from the serving resource: {why_no_marker}; the organism-health "
                   "threshold rule never decides a CRITICAL change.")
                + model_out)
        elif marker:
            decision, decision_source = marker, "model_decision_marker"
        elif not admin_requested:
            # auth ON and a non-admin asked: a RULE verdict is not handed to a non-admin requester
            decision, held, hold_reason = None, True, "rule_verdict_requires_admin_requester"
            decision_source = "held_awaiting_admin"
            recommendation = {"verdict": rule_verdict, "source": "health_threshold_rule"}
            review_text = (
                f"HELD — {why_no_marker}, so only the organism-health threshold rule could decide this "
                f"change ({rule_clause}). With authentication enabled a rule verdict is applied only "
                "when an admin requests the review; it is recorded here as a recommendation."
                + model_out)
        elif rule_verdict is None:
            # W494 - the rule could not be evaluated, and a rule that cannot be evaluated does not
            # approve by default. Held for an explicit decision, with the reason on the record.
            decision, held, hold_reason = None, True, "health_rule_not_evaluable"
            decision_source = "held_awaiting_admin"
            recommendation = ({"verdict": marker, "source": "model_decision_marker"} if marker else None)
            review_text = (
                f"HELD — {why_no_marker}, so only the organism-health threshold rule could decide "
                f"this change, and {rule_clause}. A rule with no evaluable input is not an "
                "approval: this waits for an explicit decision."
                + model_out)
        else:
            decision, decision_source = rule_verdict, "health_threshold_rule"
            review_text = (
                f"DECIDED BY RULE, NOT BY THE SERVING RESOURCE: {why_no_marker}, so the verdict is the "
                f"organism-health threshold rule (tier is not CRITICAL; {rule_clause}). The prose below was "
                f"written by {_writer} and had NO bearing on the decision."
                + model_out)

    # §17.5 — an APPROVED major change (HIGH/CRITICAL) is pre-validated at approval time so
    # /implement can enforce "pre-validation before major change" without a second round-trip.
    # The await stays OUTSIDE the lock.
    tp = None
    # W464 — not for an economy hold: its implement path returns before the §17.5 check and the gate never reads the
    # verdict, so every Sanctum vote paid for a model call whose FAIL was shown in red on a record that then released
    if decision == "approved" and tier in ("HIGH", "CRITICAL") and c.get("change_type") != "economy_material":
        tp = await _twin_prevalidate(c)

    def _decide(fresh: dict) -> None:
        if fresh["status"] != "under_review":
            raise HTTPException(status_code=409,
                                detail=f"Change was decided concurrently (status {fresh['status']}).")
        if (fresh.get("est_distributable_wst"), fresh.get("intake")) != reviewed_amount:
            raise HTTPException(status_code=409, detail=(
                "The hold's amount changed during the review; nothing was decided. Re-read it and review again."))
        fresh["review_result"] = review_text
        # W505 (FU-033, second pass) — ON THE RECORD, not only in the prompt. The absences were named to the
        # reviewing resource and nowhere a person reading this record back could see them, and a change
        # reviewed without a rollback plan is a different proposition from one that had one.
        if _absent:
            fresh["reviewed_without"] = list(_absent)
            fresh["reviewed_without_note"] = (
                f"this change was reviewed while missing: {', '.join(_absent)}. The reviewer was told so; the "
                f"decision was taken on what the record held.")
        fresh["decision_source"] = decision_source
        # W505 (FU-030) — stamped so awaiting_board_ratification can tell an ACKNOWLEDGED Owner decision
        # from an override nobody acknowledged. Without this the backwards check has nothing to read.
        if req.override_decision:
            fresh["owner_decision_acknowledged"] = _ack_override
        fresh["reviewed_at"] = now
        trail = fresh.setdefault("audit_trail", [])
        if held:
            fresh["hold_reason"] = hold_reason
            fresh["recommendation"] = recommendation
            trail.append({"event": "held_awaiting_admin_decision", "ts": now, "by": principal,
                          "by_verified": _verified(user), "hold_reason": hold_reason,
                          "recommendation": recommendation})
            return
        fresh.pop("hold_reason", None)
        fresh.pop("recommendation", None)   # superseded by the decision; the held audit entry keeps it
        fresh["status"] = decision
        fresh["decision"] = decision
        trail.append({"event": decision, "ts": now, "by": principal, "by_verified": _verified(user),
                      "via": "admin_override" if req.override_decision else "review_request",
                      "decided_by": ("admin_override" if decision_source == "admin_override"
                                     else "cca_ai_model_marker" if decision_source == "model_decision_marker"
                                     else "organism_health_threshold_rule")})
        if awaiting_board_ratification(fresh):
            # W464 (FU-012) — a hold on the approval, so it stays in the record's own trail (not the ledger)
            trail.append({"event": "awaiting_board_ratification", "ts": now, "by": "cca", "by_verified": False,
                          "approved_by": decision_source,
                          "note": "a HIGH change approved by a review waits for the Board to ratify it on the "
                                  "Owner's direction before anything acts on it"})
        if tp is not None:
            fresh["twin_prevalidation"] = tp
            trail.append({"event": f"twin_prevalidation_{tp['verdict']}", "ts": tp["simulated_at"],
                          "source": tp["source"], "by": principal, "by_verified": _verified(user)})

    c = _update_change(cca_id, _decide)
    awaiting = awaiting_board_ratification(c)

    # W464 (FU-013) — the decision is on the record; now it goes to the constitutional ledger (never a hold). Written
    # before anything else can raise, so a later failure cannot skip it.
    ueg_logged = None
    if not held:
        _decided_by = ("admin_override" if decision_source == "admin_override"
                       else "cca_ai_model_marker" if decision_source == "model_decision_marker"
                       else "organism_health_threshold_rule")
        _common = {**_decision_fields(c), "decision_source": decision_source, "decided_by": _decided_by,
                   "via": "admin_override" if req.override_decision else "review_request",
                   "by": principal, "by_verified": _verified(user),
                   **({"follows_rejection": c["follows_rejection"].get("cca_id")}
                      if isinstance(c.get("follows_rejection"), dict) else {}),
                   **({"notes": req.reviewer_notes[:200]} if req.override_decision and req.reviewer_notes else {})}
        if decision == "approved":
            ueg_logged = _log_decision_on(cca_id, {"type": "cca.change_approved", **_common,
                                        "decision": "approved",
                                        "awaiting_board_ratification": awaiting,
                                        **({"twin_prevalidation": {"verdict": tp["verdict"], "source": tp["source"]}}
                                           if tp else {})})
        else:
            ueg_logged = _log_decision_on(cca_id, {"type": "cca.change_rejected", **_common,
                                                   "decision": "rejected"})

    if held:
        biobus.fire_signal("reflex", "cca.decision", f"CCA HELD ({hold_reason}): {c['title']}", 0.6)
    else:
        biobus.fire_signal("motor" if decision == "approved" else "reflex", "cca.decision",
                           f"CCA {decision.upper()}: {c['title']}", 0.6)

    return {
        "cca_id": cca_id,
        "decision": decision,
        "decision_source": decision_source,
        "hold_reason": hold_reason,
        "recommendation": recommendation,
        "review_result": review_text[:500],
        "status": c["status"],
        "impact_tier": tier,
        "awaiting_board_ratification": awaiting,
        **({"ueg_logged": ueg_logged} if ueg_logged is not None else {}),
    }


@router.post("/{cca_id}/implement")
async def implement_change(cca_id: str, force: bool = False,
                           user: dict | None = Depends(get_current_user)):
    """Apply and mark an approved change implemented. An economy materiality hold (change_type
    economy_material) is never implemented here: it is refused 409 unless the record's own reading shows no
    action can ever release it (running the action it was filed for is what spends the approval), and only
    then retired as 'withdrawn' (admin only when auth is enabled).
    §17.5 invariant: HIGH/CRITICAL changes REQUIRE a
    recorded pre-validation PASS (run at review-approval, or via POST /{cca_id}/twin-prevalidate); a
    FAIL blocks implementation unless an admin overrides with ?force=true (audit-trailed). With auth
    enabled, a change that sets a governed live lever (or resets the config) is implemented only by an
    admin — the same bar as /immune-reconfigure."""
    principal = _actor(user)
    _u = _principal(user)
    is_admin = (not auth_enabled()) or bool(_u and _u.get("role") == "admin")
    if force and auth_enabled() and (not _principal(user) or _principal(user).get("role") != "admin"):
        raise HTTPException(status_code=403,
                            detail="Only an admin may force past a failed pre-validation.")
    # W459 — the whole body is one critical section: it contains no await, and two concurrent
    # /implement calls used to both pass the status check and apply the change twice. The record must
    # exist (and the id be a safe segment) BEFORE the lock touches the store.
    if not _valid_cca_id(cca_id) or not _cca_path(cca_id).exists():
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    with _change_mutation(cca_id):
        result = _implement_locked(cca_id, force, principal, _verified(user), is_admin)
    # W464 (FU-013) — a retirement's ledger events are written after the record lock is released (a slow ledger never
    # holds the record, and the entries describe a write that has landed)
    retired = result.pop("_retired", None)
    if retired:
        try:
            from agentic_core.economy.governance import _ueg_log as _econ_log
            _econ_log({"type": "economy.materiality_hold_withdrawn", "vsb_id": retired.get("vsb_id"), "cca_id": cca_id,
                       "superseded_by": None, "reason": f"retired: {retired['why']}"[:200], "by": principal})
        except Exception:
            pass
        result["ueg_logged"] = _log_decision({"type": "cca.change_retired", **_decision_fields(retired["record"]),
                                              "decision": "withdrawn", "reason": str(retired["why"])[:200],
                                              "by": principal, "by_verified": _verified(user)})
    return result


def _implement_locked(cca_id: str, force: bool, principal: str, verified: bool,
                      is_admin: bool = True) -> dict:
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] != "approved":
        raise HTTPException(status_code=400, detail=f"Change must be approved before implementation. Status: {c['status']}")
    if awaiting_board_ratification(c):
        # W464 (FU-012) — before anything is written or applied, and ?force never passes it (force answers a failed
        # pre-validation, not a missing ratification)
        raise HTTPException(status_code=409, detail=(
            "This HIGH change was approved by a review ("
            + ("the reviewing model's decision marker" if approval_source(c) == "model_decision_marker"
               else "the organism-health threshold rule" if approval_source(c) == "health_threshold_rule"
               else "a decision recorded before W459 with no source, read as a review's")
            + "), so it waits for the Board to ratify it on the Owner's direction before it is implemented. "
              "Ratify or refuse it on the Board page (POST /api/v1/board/ratifications/" + cca_id + ")."))
    if c.get("change_type") == "economy_material":
        # W463 (third refutation) — an economy hold carries no config to apply: implementing it only marked the record
        # "implemented", which spent the Owner's approval with nothing distributed or transferred. W463 (sixth
        # refutation): one reading decides AND explains a retirement; an unknown answer never retires.
        try:
            from agentic_core.economy.governance import unreleasable_reason
            why = unreleasable_reason(c)
        except Exception:
            why = None
        if why is None:
            raise HTTPException(status_code=409, detail=(
                "An economy materiality hold is released by running the action it was filed for (the cycle or the "
                "transfer), which spends the approval; implementing it here would spend it with nothing run."))
        # W463 (fourth refutation) — a record the gate can never match (a transfer hold filed before W463 names no
        # counterparty) could otherwise never leave 'approved': it is retired as what it is — releasing nothing
        if not is_admin:
            # W463 (fifth refutation) — with auth enabled a retirement is an admin decision (any authenticated user
            # could retire another tenant's record)
            raise HTTPException(status_code=403, detail="Only an admin may retire an economy record.")
        now_w = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        c["status"] = "withdrawn"
        c.setdefault("audit_trail", []).append(
            {"event": "withdrawn_unreleasable", "ts": now_w, "by": principal, "by_verified": verified,
             "reason": f"{why}; nothing ran"})
        _save_change(c)
        # W581 — the sibling below carries `applied`; a caller reading it here got undefined. Nothing was
        # applied on this path and None says so, where an empty dict would read as an empty application.
        return {"cca_id": cca_id, "status": "withdrawn", "applied": None,
                "note": f"This economy record can never be released by running an action ({why}), so it was retired "
                        "(withdrawn) — nothing was distributed or transferred.",
                "_retired": {"why": why, "vsb_id": c.get("vsb_id"), "record": c}}
    _spec = c.get("config_change") or {}
    if _spec and not is_admin:
        from agentic_core.organism.reconfiguration import _GOVERNED_KEYS
        if _spec.get("reset") or (_spec.get("section"), _spec.get("key")) in _GOVERNED_KEYS:
            raise HTTPException(status_code=403, detail=(
                "Only an admin may implement a change to a governed live lever (or a config reset) — "
                "the same bar as the immune reflex that applies those levers."))

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if effective_tier(c) in ("HIGH", "CRITICAL"):     # W464 — the effective tier (a re-tiered type needs it too)
        tp = c.get("twin_prevalidation")
        if not tp:
            raise HTTPException(status_code=409, detail=(
                "§17.5 invariant: this MAJOR change has no recorded pre-validation. "
                f"Run POST /api/v1/cca/{cca_id}/twin-prevalidate first."))
        if tp.get("verdict") != "pass" and not force:
            c["audit_trail"].append({"event": "implement_blocked_twin_fail", "ts": now,
                                     "by": principal, "by_verified": verified,
                                     "twin_source": tp.get("source")})
            _save_change(c)
            raise HTTPException(status_code=409, detail=(
                "§17.5 invariant: the pre-validation FAILED "
                f"({tp.get('source_label') or tp.get('source')}). Implementation blocked; an admin may "
                "override with ?force=true."))
        if tp.get("verdict") != "pass" and force:
            # W459 — was "twin_fail_overridden_by_owner": an authorship claim the route never read
            c["audit_trail"].append({"event": "twin_fail_overridden", "ts": now,
                                     "by": principal, "by_verified": verified})

    # W438 — the CCA gains its EXECUTION ARM: /implement used to only MARK a change implemented
    # while applying nothing (the raw ungoverned config route did the applying — that inversion was
    # the governance bypass). A change carrying a config_change payload is now genuinely applied
    # here, through the reconfiguration engine's audited core, under the W318 consumer-honesty rule.
    applied = None
    spec = c.get("config_change")
    if spec:
        from agentic_core.organism.reconfiguration import (apply_config_change, apply_config_reset,
                                                           wiring_for)
        try:
            if spec.get("reset"):
                applied = apply_config_reset(reason=f"CCA {cca_id}: {c['title']}",
                                             updated_by=f"cca:{cca_id}")["change"]
                wired = True   # a reset flips wired levers back to defaults
                consumer = "reset — includes every wired lever (rpm_limit, metabolic_throttle, immune_quarantine, evolution_auto_apply)"
            else:
                applied = apply_config_change(spec["section"], spec["key"], spec.get("value"),
                                              reason=f"CCA {cca_id}: {c['title']}",
                                              updated_by=f"cca:{cca_id}")
                w = wiring_for(spec["section"], spec["key"])
                wired, consumer = w["wired"], w["consumer"]
        except ValueError as e:
            c["audit_trail"].append({"event": "apply_failed", "ts": now, "error": str(e)})
            _save_change(c)
            raise HTTPException(status_code=422, detail=f"config change could not be applied: {e}")
        if not wired:
            # W318 — the value was set but nothing consumes it: never claim 'implemented'
            c["audit_trail"].append({"event": "config_set_no_consumer", "ts": now, "applied": applied,
                                     "note": "config value set; stored-only key — no live behaviour changed"})
            _save_change(c)
            biobus.fire_signal("motor", "cca.implement", f"Config set (no consumer): {c['title']}", 0.5)
            return {"cca_id": cca_id, "status": c["status"], "applied": applied,
                    "note": ("the value was stored, but this key has no wired consumer — no live "
                             "behaviour changed, so the change is NOT marked implemented (W318)")}
        c["audit_trail"].append({"event": "config_applied", "ts": now, "applied": applied,
                                 "consumer": consumer})

    # P3.26 clauses (3) and (7) (W608) — A RETIREMENT IS APPLIED HERE AND NOWHERE ELSE, and it re-checks the
    # never-auto-retire rules first: an entity can become protected between filing and approval.
    _retirement_effect = None
    if c.get("change_type") == "entity_retirement":
        from agentic_core.economy.turnover import apply_retirement
        _ret = apply_retirement(str(c.get("vsb_id") or ""), cca_id)
        if not _ret.get("retired"):
            c["audit_trail"].append({"event": "implement_refused_protected", "ts": now, "by": principal,
                                     "by_verified": verified, "basis": _ret.get("basis")})
            _save_change(c)
            raise HTTPException(status_code=409, detail=_ret)
        applied = _ret
        _retirement_effect = _ret["basis"]
        c["audit_trail"].append({"event": "entity_retired", "ts": now, "applied": _ret})

    c["status"] = "implemented"
    c["implemented_at"] = now
    _record_variance(c, now, "implemented")                   # W581 (FU-313) — the SECOND of two sites
    # W505 (FU-157, S1.10) — WHAT IT DID. A change with no config_change payload applies nothing, and every
    # change submitted from the page's own form is one; the record read IMPLEMENTED and counted in the
    # Implemented stat regardless. `status` keeps its vocabulary (many readers, and the record IS closed out);
    # the effect is stated separately so nobody has to infer it from a null.
    _effect = "applied" if applied else "recorded_only"
    c["implementation_effect"] = _effect
    c["implementation_effect_basis"] = (
        _retirement_effect if _retirement_effect else
        "the change carried a config_change payload and the reconfiguration engine applied it"
        if applied else
        "this change carried nothing for the platform to apply, so implementing it recorded the decision and "
        "closed the record; no platform behaviour changed. Work described in prose is carried out elsewhere.")
    c["audit_trail"].append({"event": "implemented", "ts": now, "by": principal,
                             "by_verified": verified, "effect": _effect})
    _save_change(c)

    biobus.fire_signal("motor", "cca.implement", f"Implemented: {c['title']}", 0.7)
    # W581 — `note` is carried by the withdrawn sibling above, so a caller reading it here got undefined.
    return {"cca_id": cca_id, "status": "implemented", "implemented_at": now, "applied": applied,
            "note": None,
            "implementation_effect": _effect,
            "implementation_effect_basis": c["implementation_effect_basis"],
            "twin_prevalidation": (c.get("twin_prevalidation") or {}).get("verdict")}


def pending_ratifications() -> list[dict]:
    """W464 (FU-012) — every change awaiting Board ratification, newest first, read from the FULL records (a list row
    carries no review text or pre-validation). Uncapped: the queue must never hide one."""
    rows = []
    for p in sorted(_CCA_STORE.glob("*.json"), key=_mtime, reverse=True):
        c = _load_change(p.stem)
        if not c or not awaiting_board_ratification(c):
            continue
        tp = c.get("twin_prevalidation") if isinstance(c.get("twin_prevalidation"), dict) else None
        approved_at = next((e.get("ts") for e in reversed(c.get("audit_trail") or [])
                            if e.get("event") == "approved"), c.get("reviewed_at"))
        rows.append({"cca_id": c["cca_id"], "title": c.get("title", ""), "change_type": c.get("change_type"),
                     "impact_tier": effective_tier(c), "status": c.get("status"),
                     "decision_source": approval_source(c), "approved_at": approved_at,
                     "submitted_by": c.get("submitted_by"), "submitted_at": c.get("submitted_at"),
                     "vsb_id": c.get("vsb_id"), "description": str(c.get("description") or "")[:600],
                     "review_result": str(c.get("review_result") or "")[:1200],
                     "twin_prevalidation": ({"verdict": tp.get("verdict"), "source": tp.get("source"),
                                             "source_label": tp.get("source_label")} if tp else None)})
    return rows


def ratify_change(cca_id: str, decision: str, notes: str, principal: str, verified: bool) -> dict:
    """W464 (FU-012) — record the Board's ratification decision on a change awaiting it: the Owner's direction, recorded
    by the Board (no model decides it — the Chief has no twin model). Compare-and-set under the record's lock: the
    change must still be approved, by a review, and not already ratified — so a ratification can never race an
    implement, a second ratification, or a refusal. Ratified: the approval stands and /implement may proceed (its
    §17.5 pre-validation check still applies). Refused: the change is REJECTED (decision_source board_refusal), which
    nothing implements. The decision is then written to the UEG (FU-013)."""
    if decision not in ("ratify", "refuse"):
        raise HTTPException(status_code=422, detail="decision must be 'ratify' or 'refuse'.")
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    seen: dict = {}

    def _ratify(fresh: dict) -> None:
        if not awaiting_board_ratification(fresh):
            raise HTTPException(status_code=409, detail=(
                f"Change {cca_id} is not awaiting Board ratification (status {fresh.get('status')}, decided by "
                f"{approval_source(fresh) or 'nothing recorded'}"
                + (f", Board decision {_ratification_decision(fresh)}" if _ratification_decision(fresh) else "")
                + "). Only a HIGH change approved by a review waits for the Board."))
        seen["approval_decision_source"] = approval_source(fresh)
        fresh["board_ratification"] = {
            "decision": "ratified" if decision == "ratify" else "refused", "at": now, "by": principal,
            "by_verified": verified, "on_owner_direction": True, "notes": (notes or "")[:500],
            "approval_decision_source": approval_source(fresh)}
        trail = fresh.setdefault("audit_trail", [])
        if decision == "ratify":
            trail.append({"event": "board_ratified", "ts": now, "by": principal, "by_verified": verified,
                          "on_owner_direction": True})
        else:
            fresh["status"] = "rejected"
            fresh["decision"] = "rejected"
            fresh["decision_source"] = "board_refusal"
            fresh["reviewed_at"] = now
            trail.append({"event": "board_ratification_refused", "ts": now, "by": principal, "by_verified": verified,
                          "on_owner_direction": True, "approval_decision_source": seen["approval_decision_source"]})

    c = _update_change(cca_id, _ratify)
    _event = {**_decision_fields(c), "approval_decision_source": seen.get("approval_decision_source"),
              "by": principal, "by_verified": verified, "on_owner_direction": True,
              **({"notes": notes[:200]} if notes else {}), "status_after": c.get("status")}
    if decision == "ratify":
        ueg_logged = _log_decision_on(cca_id, {"type": "board.change_ratified", **_event,
                                               "decision": "ratified"})
    else:
        ueg_logged = _log_decision_on(cca_id, {"type": "board.change_ratification_refused", **_event,
                                               "decision": "refused"})
    try:
        biobus.fire_signal("motor" if decision == "ratify" else "reflex", "board.ratification",
                           f"Board {'RATIFIED' if decision == 'ratify' else 'REFUSED'}: {c.get('title')}", 0.7)
    except Exception:
        pass
    return {"cca_id": cca_id, "decision": "ratified" if decision == "ratify" else "refused",
            "status": c.get("status"), "by": principal, "by_verified": verified, "ueg_logged": ueg_logged,
            "note": ("Ratified — the approval stands; the change may now be implemented (a HIGH change still needs a "
                     "recorded §17.5 pre-validation PASS)." if decision == "ratify" else
                     "Refused — the change is rejected and will not be implemented.")}


@router.get("/impact/{cca_id}")
async def impact_assessment(cca_id: str):
    """AI-generated impact assessment for a change request."""
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")

    ctx = biobus.organism_context()
    prompt = (
        f"You are an impact assessment specialist for Workstation IDBO.\n\n"
        f"Change: {c['title']}\n"
        f"Description: {c['description']}\n"
        f"Affected systems: {', '.join(c['affected_systems']) or 'unknown'}\n"
        f"Current organism mode: {ctx['mode']}\n\n"
        f"Provide a concise impact assessment:\n"
        f"## Direct Impacts (systems affected)\n"
        f"## Indirect Impacts (downstream effects)\n"
        f"## Risks (what could go wrong)\n"
        f"## Mitigation (how to reduce risk)\n"
        f"## Estimated Recovery Time (if something goes wrong)\n"
        f"## Recommended Implementation Window (best time relative to circadian cycle)\n"
    )
    # W506 (P2.2)
    _ia = await gateway.query_meta(prompt, agent="cca_impact", augment=False)
    assessment = _ia.get("output", "")
    biobus.fire_signal("cognitive", "cca.impact", f"Impact assessed: {c['title']}", 0.4)
    return {"cca_id": cca_id, "assessment": assessment, "organism_mode": ctx["mode"]}


@router.get("")
async def list_all_changes():
    """List all change requests across all statuses."""
    all_changes = _list_changes()
    by_status: dict[str, int] = {}
    for c in all_changes:
        s = c["status"]
        by_status[s] = by_status.get(s, 0) + 1
    return {"changes": all_changes[:50], "total": len(all_changes), "by_status": by_status}
