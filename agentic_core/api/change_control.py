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
  MEDIUM — review required (economy materiality holds, change_type economy_material, are MEDIUM; one
           filed after a rejection of its action — follows_rejection — is never decided by a review: it is
           HELD with hold_reason follows_rejection_requires_explicit_decision until an explicit decision).
           Otherwise a single [DECISION: …] marker from the serving model decides it. With
           no marker (the deterministic floor) or conflicting markers, the verdict is the
           ORGANISM-HEALTH THRESHOLD RULE (composite_health >= 0.5 → approved, else rejected), and the
           record says so in `decision_source` and at the head of the review text. With auth
           enabled, a rule verdict is applied only when an ADMIN requests the review; a non-admin's
           review is HELD with the rule's verdict recorded as a recommendation.
  HIGH   — as MEDIUM, plus a recorded §17.5 pre-validation PASS before /implement
  CRITICAL — NEVER decided by a review. A model marker is recorded as a RECOMMENDATION and the health
           rule never applies: the change is HELD until an explicit admin decision
           (admin_decision_for_critical; auth ON: an admin principal)
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
  POST /api/v1/cca/{cca_id}/implement — apply + mark an approved change implemented (an approved
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
                "impact_tier": c.get("impact_tier", "MEDIUM"),
                "status": c.get("status", "submitted"),
                "submitted_by": c.get("submitted_by", "system"),
                "submitted_at": c.get("submitted_at", ""),
                "reviewed_at": c.get("reviewed_at"),
                "decision": c.get("decision"),
                # W463 — a held record (awaiting an explicit decision) and an economy hold's current amount
                "hold_reason": c.get("hold_reason"),
                "est_distributable_wst": c.get("est_distributable_wst"),
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
}


def _determine_tier(change_type: str, description: str) -> ImpactTier:
    base = _TIER_MAP.get(change_type, "MEDIUM")
    # Elevate if keywords suggest constitutional or organism impact
    critical_keywords = ["constitution", "genome core", "delete all", "reset organism", "override gaas"]
    if any(k in description.lower() for k in critical_keywords):
        return "CRITICAL"
    return base


# ── Request models ────────────────────────────────────────────────────────────

class ConfigChangeSpec(BaseModel):
    # W438 — the CCA's execution arm for organism configuration. Either one (section, key, value)
    # change or reset: true. Validated/coerced at SUBMIT time so an unappliable change can never
    # be approved, and APPLIED by /implement (which used to only mark, never execute).
    section: str | None = None
    key: str | None = None
    value: Any = None
    reset: bool = False


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
    if req.change_type == "economy_material" or _title.startswith(("[economy] material distribution",
                                                                    "[economy] material transfer")):
        raise HTTPException(status_code=422, detail=(
            "change_type 'economy_material' and the '[economy] material distribution/transfer' titles are "
            "reserved for the economy's own materiality holds, which it files and keeps current itself; run "
            "the action (a cycle or transfer) and review the hold it files."))
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
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    # the name on the record is the authenticated one when there is one; otherwise the caller's
    _by = principal or req.submitted_by or "system"

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
        "status": "submitted",
        "vsb_id": req.vsb_id,
        "rollback_plan": req.rollback_plan,
        "review_result": None,
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
    if tier == "LOW" and ctx["composite_health"] >= 0.6 and threat in ("NOMINAL", "ELEVATED"):
        change["status"] = "approved"
        change["decision"] = "auto_approved"
        change["reviewed_at"] = now
        change["review_result"] = f"Auto-approved: LOW impact, organism healthy, immune threat {threat}."
        change["audit_trail"].append({"event": "auto_approved", "ts": now, "by": "biobus", "immune_threat": threat})
        biobus.fire_signal("motor", "cca.auto_approve", f"Auto-approved: {req.title}", 0.3)
    else:
        if tier == "LOW" and threat in ("HIGH", "CRITICAL"):
            change["review_result"] = (f"Held for review: immune threat {threat} — auto-approval paused "
                                       "while the organism defends itself.")
            change["audit_trail"].append({"event": "held_immune_threat", "ts": now, "by": "biobus",
                                          "immune_threat": threat})
        biobus.fire_signal("sensory", "cca.submit", f"Change submitted: {req.title} [{tier}] (immune: {threat})", 0.5)

    _save_change(change)
    return {
        "cca_id": cca_id,
        "impact_tier": tier,
        "status": change["status"],
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


@router.post("/immune-reconfigure")
async def immune_reconfigure(req: ImmuneReconfigureRequest = ImmuneReconfigureRequest(),
                             user: dict = Depends(require_admin)):
    """Immune-system reconfigurator, governed arms-length by the CCA.

    Biomimetic defence: when the immune system is under threat it proposes a SAFE, REVERSIBLE
    defensive reconfiguration (tighten generation → throttle load → quarantine failing endpoints).
    The CCA records it as a change-controlled, audited action and — because these are low-risk,
    reversible defensive levers — auto-approves and APPLIES it via the reconfiguration engine (a fast
    innate-immune reflex that is nonetheless governed). Admin-only: it applies governed live levers.
    This wires the arms-length CCA to the Immune system and the Reconfiguration engine.
    """
    threat = (req.simulate_threat or _immune_threat()).upper()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    plan = _IMMUNE_DEFENCE.get(threat)
    if plan is None:
        return {"threat_level": threat, "action": "none", "governed_by": "Change Control Agency (arms-length)",
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
        # The flag is gone rather than left as a claim about a process that does not exist.
        "rollback_plan": f"Revert {plan['section']}.{plan['key']} to its prior value via /config/update.",
        "review_result": None, "decision": None, "reviewed_at": None, "implemented_at": None,
        "audit_trail": [{"event": "submitted", "ts": now, "by": "immune_system", "immune_threat": threat,
                         "requested_by": _actor(user), "by_verified": _verified(user)}],
    }
    biobus.fire_signal("sensory", "cca.immune_reconfigure", f"Immune defence proposed [{threat}]", 0.6)

    # Arms-length governance: auto-approve the defensive (reversible) reconfiguration, then apply it.
    change["status"] = "approved"
    change["decision"] = "auto_approved_immune_defence"
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
        _consumer = _LEVER_CONSUMERS.get(plan["key"])
        if _consumer:
            change["status"] = "implemented"
            change["implemented_at"] = now
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
    return {
        "cca_id": cca_id,
        "threat_level": threat,
        "impact_tier": plan["tier"],
        "status": change["status"],
        "reconfiguration": {"section": plan["section"], "key": plan["key"], "value": plan["value"], "why": plan["why"]},
        "applied": applied,
        "governed_by": "Change Control Agency (arms-length)",
        "message": f"Immune reconfigurator: {threat} → {plan['section']}.{plan['key']}={plan['value']} ({change['status']}).",
    }


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
    return c


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
        f"  Composite health: {ctx['composite_health']:.0%} | mode: {ctx['mode']}\n"
        f"  Immune threat: {ctx['immune']['threat_level']} | circadian: {ctx['circadian']['cycle']}\n\n"
        f"Proposed change ({change['impact_tier']}): {change['title']}\n"
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
        sim = await gateway.query(prompt, agent="cca_twin_prevalidation", timeout=25)
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
        healthy = ctx["composite_health"] >= 0.6 and ctx["immune"]["threat_level"] in ("NOMINAL", "ELEVATED")
        verdict, source = ("pass" if healthy else "fail"), "health_gate_default"
    return {
        "verdict": verdict,
        "source": source,
        "composite_health_at_sim": ctx["composite_health"],
        "immune_threat_at_sim": ctx["immune"]["threat_level"],
        "summary": (sim or "")[:600],
        "simulated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        # W459 — this string was unconditional, so the health-gate fallback (the only branch the
        # deterministic floor can reach) claimed a forward simulation that never ran.
        "method": ("digital-twin forward simulation over the live organism state"
                   if source == "twin_marker" else
                   "no twin model — organism health gate only (composite_health >= 0.6 and immune "
                   "threat in NOMINAL/ELEVATED); the proposed change was NOT simulated"),
        "source_label": ("model twin verdict" if source == "twin_marker"
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
    marker decides a MEDIUM/HIGH change — except an economy hold filed after a rejection of its action
    (follows_rejection), which any review HOLDS (hold_reason follows_rejection_requires_explicit_decision, the
    verdict kept as a recommendation) for an explicit decision. With no marker, or conflicting markers, the organism-health
    threshold RULE decides it and the record says so — except that with auth enabled a rule verdict
    is applied only when an admin requested the review (a non-admin's review is held, with the rule's
    verdict as a recommendation). (3) The decision is
    stamped with WHO asked (`by`, `by_verified`) and WHAT decided (`decided_by`), instead of an
    unconditional "cca_ai" on a human's override.
    """
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] not in ("submitted", "under_review"):
        raise HTTPException(status_code=400, detail=f"Change is {c['status']} — cannot review.")

    principal = _actor(user)
    if req.override_decision:
        u = _principal(user)
        if auth_enabled() and (not u or u.get("role") != "admin"):
            raise HTTPException(status_code=403,
                                detail="Only an admin may override a Change Control decision.")
        if c["impact_tier"] == "CRITICAL" and not req.admin_decision_for_critical:
            raise HTTPException(status_code=403, detail=(
                "A CRITICAL change is never decided incidentally: resend with "
                "admin_decision_for_critical: true to record this as an explicit admin decision."))

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
        fresh["status"] = "under_review"
        fresh.setdefault("audit_trail", []).append(
            {"event": "review_started", "ts": now, "by": principal, "by_verified": _verified(user)})

    c = _update_change(cca_id, _start)
    # W463 — what the reviewer is deciding: an economy hold's amount and intake as they stood at the start
    reviewed_amount = (c.get("est_distributable_wst"), c.get("intake"))

    biobus.fire_signal("cognitive", "cca.review", f"Reviewing: {c['title']}", 0.6)

    held, hold_reason, recommendation = False, None, None
    if req.override_decision:
        decision, decision_source = req.override_decision, "admin_override"
        review_text = f"Manual override: {req.reviewer_notes or 'No notes.'}"
    else:
        # a review by the serving resource (a model, or the deterministic floor)
        ctx = biobus.organism_context()
        prompt = (
            f"You are the Chief Governance Officer of Workstation IDBO, reviewing a change request.\n\n"
            f"Change Title: {c['title']}\n"
            f"Type: {c['change_type']}\n"
            f"Impact Tier: {c['impact_tier']}\n"
            f"Description: {c['description']}\n"
            f"Rationale: {c['rationale'] or 'Not provided.'}\n"
            f"Affected Systems: {', '.join(c['affected_systems']) or 'Not specified.'}\n"
            f"Rollback Plan: {c['rollback_plan'] or 'Not provided.'}\n\n"
            f"Current Organism Health:\n"
            f"  Composite health: {ctx['composite_health']:.0%}\n"
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
        review_text = await gateway.query(prompt, agent="cca_review")

        _up = (review_text or "").upper()
        _yes, _no = "[DECISION: APPROVED]" in _up, "[DECISION: REJECTED]" in _up
        marker = "approved" if (_yes and not _no) else "rejected" if (_no and not _yes) else None
        why_no_marker = ("the serving resource returned BOTH [DECISION: APPROVED] and [DECISION: REJECTED] "
                         "(conflicting markers)" if (_yes and _no) else
                         "no [DECISION: …] marker was returned")
        _h = float(ctx["composite_health"])
        rule_verdict = "approved" if _h >= 0.5 else "rejected"
        # print the value with enough precision that the stated comparison is TRUE as written (0.4999
        # rounded to "0.50 < 0.5" was a false sentence in the record)
        _shown = next(f"{_h:.{n}f}" for n in range(2, 12)
                      if (float(f"{_h:.{n}f}") >= 0.5) == (_h >= 0.5))
        rule_clause = f"composite_health {_shown} {'>=' if rule_verdict == 'approved' else '<'} 0.5 → {rule_verdict}"
        _u = _principal(user)
        admin_requested = (not auth_enabled()) or bool(_u and _u.get("role") == "admin")
        model_out = "\n\n--- model output ---\n" + (review_text or "")
        if c["impact_tier"] == "CRITICAL":
            # never decided by a review: a model marker is a recommendation; the rule never applies
            decision, held, hold_reason = None, True, "critical_requires_admin_decision"
            decision_source = "held_awaiting_admin"
            recommendation = ({"verdict": marker, "source": "model_decision_marker"} if marker else None)
            review_text = (
                "HELD — a CRITICAL change is decided only by an explicit admin decision. "
                + (f"The serving model recommended {marker.upper()}; that is recorded as a "
                   "recommendation, not a decision." if marker else
                   f"No model recommendation: {why_no_marker}; the organism-health threshold rule "
                   "never decides a CRITICAL change.")
                + model_out)
        elif c.get("follows_rejection"):
            # W463 — the economy re-filed an action after the Owner rejected it: a review (model or rule) never
            # decides that; the recommendation is recorded and an explicit decision is required
            decision, held, hold_reason = None, True, "follows_rejection_requires_explicit_decision"
            decision_source = "held_awaiting_admin"
            recommendation = ({"verdict": marker, "source": "model_decision_marker"} if marker
                              else {"verdict": rule_verdict, "source": "health_threshold_rule"})
            review_text = (
                f"HELD — this economy hold follows the rejection of {c['follows_rejection'].get('cca_id')}; only an "
                "explicit decision (override_decision) can approve or reject it. The review's verdict is recorded "
                "as a recommendation." + model_out)
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
        else:
            decision, decision_source = rule_verdict, "health_threshold_rule"
            review_text = (
                f"DECIDED BY RULE, NOT BY THE MODEL: {why_no_marker}, so the verdict is the "
                f"organism-health threshold rule (tier is not CRITICAL; {rule_clause}). The prose below "
                "is the model's and had NO bearing on the decision."
                + model_out)

    # §17.5 — an APPROVED major change (HIGH/CRITICAL) is pre-validated at approval time so
    # /implement can enforce "pre-validation before major change" without a second round-trip.
    # The await stays OUTSIDE the lock.
    tp = None
    if decision == "approved" and c["impact_tier"] in ("HIGH", "CRITICAL"):
        tp = await _twin_prevalidate(c)

    def _decide(fresh: dict) -> None:
        if fresh["status"] != "under_review":
            raise HTTPException(status_code=409,
                                detail=f"Change was decided concurrently (status {fresh['status']}).")
        if (fresh.get("est_distributable_wst"), fresh.get("intake")) != reviewed_amount:
            raise HTTPException(status_code=409, detail=(
                "The hold's amount changed during the review; nothing was decided. Re-read it and review again."))
        fresh["review_result"] = review_text
        fresh["decision_source"] = decision_source
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
        if tp is not None:
            fresh["twin_prevalidation"] = tp
            trail.append({"event": f"twin_prevalidation_{tp['verdict']}", "ts": tp["simulated_at"],
                          "source": tp["source"], "by": principal, "by_verified": _verified(user)})

    c = _update_change(cca_id, _decide)

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
        return _implement_locked(cca_id, force, principal, _verified(user), is_admin)


def _implement_locked(cca_id: str, force: bool, principal: str, verified: bool,
                      is_admin: bool = True) -> dict:
    c = _load_change(cca_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Change {cca_id} not found.")
    if c["status"] != "approved":
        raise HTTPException(status_code=400, detail=f"Change must be approved before implementation. Status: {c['status']}")
    if c.get("change_type") == "economy_material":
        # W463 (third refutation) — an economy hold carries no config to apply: implementing it only marked the record
        # "implemented", which spent the Owner's approval with nothing distributed or transferred. W463 (sixth
        # refutation): one reading decides AND explains a retirement; an unknown answer never retires.
        try:
            from agentic_core.economy.governance import _ueg_log as _econ_log, unreleasable_reason
            why = unreleasable_reason(c)
        except Exception:
            _econ_log, why = None, None
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
        if _econ_log:
            _econ_log({"type": "economy.materiality_hold_withdrawn", "vsb_id": c.get("vsb_id"), "cca_id": cca_id,
                       "superseded_by": None, "reason": f"retired: {why}"[:200], "by": principal})
        return {"cca_id": cca_id, "status": "withdrawn",
                "note": f"This economy record can never be released by running an action ({why}), so it was retired "
                        "(withdrawn) — nothing was distributed or transferred."}
    _spec = c.get("config_change") or {}
    if _spec and not is_admin:
        from agentic_core.organism.reconfiguration import _GOVERNED_KEYS
        if _spec.get("reset") or (_spec.get("section"), _spec.get("key")) in _GOVERNED_KEYS:
            raise HTTPException(status_code=403, detail=(
                "Only an admin may implement a change to a governed live lever (or a config reset) — "
                "the same bar as the immune reflex that applies those levers."))

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if c["impact_tier"] in ("HIGH", "CRITICAL"):
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

    c["status"] = "implemented"
    c["implemented_at"] = now
    c["audit_trail"].append({"event": "implemented", "ts": now, "by": principal,
                             "by_verified": verified})
    _save_change(c)

    biobus.fire_signal("motor", "cca.implement", f"Implemented: {c['title']}", 0.7)
    return {"cca_id": cca_id, "status": "implemented", "implemented_at": now, "applied": applied,
            "twin_prevalidation": (c.get("twin_prevalidation") or {}).get("verdict")}


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
    assessment = await gateway.query(prompt, agent="cca_impact")
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
