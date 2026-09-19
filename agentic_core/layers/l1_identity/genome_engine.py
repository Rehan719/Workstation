"""Layer 1 (Identity) genome engine — constitutional articles, checkpoints and rollback.

W464 (FU-020, the Owner's ruling of 2026-09-14: fix it and keep it; it stays unwired — nothing imports it):
  * rollback(proposal_id) restores THAT proposal's own checkpoint. It used to pop the LAST checkpoint whatever was
    asked (after A then B, "undo A" removed B and kept A) and never wrote anything, so the disk copy kept the change.
    A checkpoint is a full snapshot of the genome taken BEFORE its change, so restoring it also discards every change
    applied after it — the result names them, and their checkpoints are dropped (they describe a history that no
    longer happened).
  * The genome and its checkpoints persist TOGETHER, in one document (GENOME_FILE), written atomically under the
    store lock, and every mutation re-reads the store inside that lock. The genome used to be written with a bare
    open() after the ratification was already logged, a failed write returned True, deletions were never written,
    and checkpoints lived only in memory (a restart had nothing to roll back to).
  * GENOME_FILE is defined here, under the data directory (so DATA_DIR isolation applies). It was bound at the bottom
    of the module through config.paths, whose BASE_DIR is one level above the repository — the store was
    <repo-parent>/genome/constitution.work, outside the repo and outside test isolation, and importing config.paths
    created directories there.
  * Importing the module reads and writes nothing of its own: the engine is loaded on first use of `genome_engine`.
  * A store that exists but does not parse is never replaced by the seed genome: the engine refuses to mutate it.
The events this module logs go to agentic_core.layers.ueg — an in-memory stub, NOT the hash-chained constitutional
ledger (agentic_core.gaas.v5.ueg).
"""
import copy
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from agentic_core.config import data_path
from agentic_core.layers.ueg import ueg
from agentic_core.layers.l1_identity.validator import validator_l1

logger = logging.getLogger("genome_engine")

GENOME_FILE: Path = data_path("genome_engine", "constitution.json")

_SEED_GENOME: Dict[str, Any] = {
    "constitution": {
        "articles": [
            {"id": 1, "title": "Sovereignty", "content": "Every Workstation node is a sovereign digital organism."},
            {"id": 42, "title": "Transparency", "content": "System decisions must be auditable and explained."},
            {"id": 1127, "title": "Autonomous Evolution", "content": "The system shall autonomously evolve its own code and constitution."}
        ],
        "root_hash": "0x-v1-init"
    }
}


class _Refused(Exception):
    """A mutation that must not happen; its message is the honest reason."""


def _rehash(genome: Dict[str, Any]) -> None:
    articles = genome["constitution"]["articles"]
    genome["constitution"]["root_hash"] = "0x" + hashlib.sha256(
        json.dumps(articles, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    ident = genome.setdefault("identity", {})
    ident.pop("merkle_root", None)
    ident["merkle_root"] = hashlib.sha256(json.dumps(genome, sort_keys=True).encode("utf-8")).hexdigest()


def _next_article_id(genome: Dict[str, Any]) -> int:
    """A fresh article id for `genome` — called inside the store lock on the genome just read. The generators used
    time-derived ids whose ranges include 1127, and apply_mutation UPDATES an article whose id matches — a generated
    "new" amendment could silently rewrite a seeded article."""
    ids = [a.get("id") for a in (genome.get("constitution") or {}).get("articles") or [] if _is_article_id(a.get("id"))]
    return max(ids + [1127]) + 1


def _is_article_id(v: Any) -> bool:
    """An integer article id — never a bool (True == 1 matched, and rewrote, seeded article 1)."""
    return isinstance(v, int) and not isinstance(v, bool)


def _genome_ok(genome: Any) -> bool:
    """The shape every reader and writer relies on: a constitution whose articles are objects, and an identity object."""
    constitution = genome.get("constitution") if isinstance(genome, dict) else None
    articles = constitution.get("articles") if isinstance(constitution, dict) else None
    return (isinstance(articles, list) and all(isinstance(a, dict) for a in articles)
            and isinstance(genome.get("identity", {}), dict))


def _read_store(path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """(document, None) · (None, None) when the store does not exist · (None, reason) when it exists but is unreadable.
    Strict on purpose: a recovered prefix of a genome is not a genome, and saving it would lose the rest."""
    if not path.exists():
        return None, None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"the genome store {path} is unreadable ({e}); nothing was changed"
    # the whole shape, checked without calling a method on an unchecked value (a list constitution raised
    # AttributeError out of the constructor), and every part a mutation reads or rewrites (a non-list rollbacks record
    # was coerced and written back, losing it)
    history = doc.get("history") if isinstance(doc, dict) else None
    rollbacks = doc.get("rollbacks", []) if isinstance(doc, dict) else None
    if (not isinstance(doc, dict) or not _genome_ok(doc.get("genome"))
            or not isinstance(history, list) or not all(isinstance(h, dict) for h in history)
            or not isinstance(rollbacks, list) or not all(isinstance(r, dict) for r in rollbacks)):
        return None, f"the genome store {path} is not a genome document; nothing was changed"
    return doc, None


class ConstitutionalAI:
    """
    LAYER 1: IDENTITY - Infinite Constitutional Adaptation.
    Specialized agent to generate, debate, and propose genome amendments.
    """
    def generate_amendment(self, trigger_context: str) -> Dict[str, Any]:
        """Proposes a constitutional amendment based on system-detected needs. NOTE: a fixed template, not a model
        output. The id is a placeholder — the engine assigns a fresh one before applying it."""
        return {
            "id": None,
            "title": f"Adaptive Response to {trigger_context}",
            "content": f"The system shall autonomously optimize for {trigger_context}.",
            "rationale": "Empirical data from L11 indicates a need for dynamic scaling protocols.",
            "impact_level": "LOW"
        }


class GenomeMutationWorkflow:
    """
    Eternal Sovereignty Genome Engine.
    Handles ratification, checkpoints and rollback of constitutional amendments.

    `store_path` None keeps the engine in memory only (nothing persists); otherwise every mutation is a
    read-modify-write of the store document {"genome", "history", "rollbacks"} under its lock.
    """
    def __init__(self, current_genome: Optional[Dict[str, Any]] = None, store_path: Optional[Path] = None,
                 history: Optional[List[Dict[str, Any]]] = None):
        self.store_path = Path(store_path) if store_path is not None else None
        self.genome: Dict[str, Any] = copy.deepcopy(current_genome if current_genome is not None else _SEED_GENOME)
        self.history: List[Dict[str, Any]] = list(history or [])
        self.rollbacks: List[Dict[str, Any]] = []
        self.load_error: Optional[str] = None
        self.last_error: Optional[str] = None
        self.last_article_id: Optional[int] = None
        self.ai = ConstitutionalAI()
        if self.store_path is not None:
            doc, err = _read_store(self.store_path)
            if err:
                self.load_error = err
                logger.error(err)
            elif doc is not None:
                self.genome, self.history = doc["genome"], doc["history"]
                self.rollbacks = doc.get("rollbacks", [])

    # ── the one write path ────────────────────────────────────────────────────
    def _commit(self, change: Callable[[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]], Any]) -> Tuple[bool, Any]:
        """Apply `change(genome, history, rollbacks)` to COPIES of the current state and persist the result; memory is
        updated only once the write has landed. Returns (True, change's result) or (False, the reason)."""
        self.last_error = None
        try:
            if self.store_path is None:
                g, h, r = copy.deepcopy(self.genome), copy.deepcopy(self.history), copy.deepcopy(self.rollbacks)
                out = change(g, h, r)
            else:
                from agentic_core.config import atomic_write_json, store_lock
                self.store_path.parent.mkdir(parents=True, exist_ok=True)
                with store_lock(self.store_path):
                    doc, err = _read_store(self.store_path)
                    if err:
                        raise _Refused(err)
                    if doc is None:          # the first write seeds the store from this engine's state
                        g, h, r = copy.deepcopy(self.genome), copy.deepcopy(self.history), copy.deepcopy(self.rollbacks)
                    else:
                        g, h, r = doc["genome"], doc["history"], doc.get("rollbacks", [])
                    out = change(g, h, r)
                    atomic_write_json(self.store_path, {"genome": g, "history": h, "rollbacks": r})
        except _Refused as e:
            self.last_error = str(e)
            return False, str(e)
        except Exception as e:     # the write (or the lock) failed: nothing changed, and it is said
            self.last_error = f"the genome change was not persisted: {e}"
            logger.error(self.last_error)
            return False, self.last_error
        self.genome, self.history, self.rollbacks = g, h, r
        return True, out

    @staticmethod
    def _checkpoint(genome: Dict[str, Any], history: List[Dict[str, Any]], proposal_id: str) -> None:
        # Checkpoint for Rollback (Article 1111): the whole genome BEFORE the change, under a unique proposal id —
        # "the proposal's own checkpoint" must name exactly one entry
        if not isinstance(proposal_id, str) or not proposal_id.strip():
            raise _Refused("a proposal id is required")
        if any(cp.get("proposal_id") == proposal_id for cp in history):
            # an id names ONE live checkpoint; a proposal rolled back (its checkpoint gone) may be applied again
            raise _Refused(f"proposal {proposal_id} already has a live checkpoint; an id names one checkpoint at a time")
        history.append({"proposal_id": proposal_id, "timestamp": time.time(), "data": json.dumps(genome)})

    # ── mutations ─────────────────────────────────────────────────────────────
    def run_self_healing_cycle(self, issue_report: str) -> bool:
        """Article 1118: autonomous self-healing triggered by a system report. W473 (register FU-028) — refused by
        rule, not by accident: generate_amendment is a FIXED TEMPLATE, not a model output, and ratifying it with
        authorized=True would write a constitutional article nothing reasoned about. It used to be unreachable only
        because the validator's PQC rule refused the context. The module stays unwired (the Owner's ruling, W464);
        the cycle now says why it applies nothing."""
        amendment = self.ai.generate_amendment(issue_report)
        self.last_error = ("self-healing amendment not applied: the amendment is a fixed template, not a model "
                           f"output ({amendment.get('title')!r}); a constitutional change goes through Change Control")
        return False

    def apply_mutation(self, proposal_id: str, patch: Dict[str, Any], authorized: bool) -> bool:
        """Apply a constitutional mutation, re-hash, and persist it with its checkpoint. A patch with an integer id
        updates that article (or adds it under that id); a patch with id None is a NEW article, whose id is chosen
        inside the store lock from the genome just re-read — an id chosen from this engine's memory could already be
        taken on disk (another engine, or an earlier proposal of this one), and the "new" article then overwrote it.
        The id used is left in `last_article_id`. Ratification is logged only after the write has landed; a failed
        write returns False."""
        self.last_article_id = None
        if not authorized:
            self.last_error = "not authorized"
            return False
        # the key must be present (a typo such as "ID" is refused, never read as a new article), and never a bool
        if not isinstance(patch, dict) or "id" not in patch or not (patch["id"] is None or _is_article_id(patch["id"])):
            self.last_error = "a patch needs an integer article id, or id None for a new article"
            return False

        def change(g: Dict[str, Any], h: List[Dict[str, Any]], r: List[Dict[str, Any]]) -> int:
            self._checkpoint(g, h, proposal_id)
            articles = g["constitution"]["articles"]
            if patch.get("id") is None:
                new_id = _next_article_id(g)
                articles.append({**patch, "id": new_id})
                _rehash(g)
                return new_id
            for a in articles:
                if a.get("id") == patch["id"]:
                    a.update(patch)
                    break
            else:
                articles.append(dict(patch))
            _rehash(g)
            return patch["id"]

        ok, article_id = self._commit(change)
        if ok:
            self.last_article_id = article_id
            ueg.log_event("L1", "Genome", "AMENDMENT_RATIFIED", {"id": article_id, "proposal_id": proposal_id,
                                                               "type": "AUTONOMOUS"})
        return ok

    def delete_article(self, article_id: int, authorized: bool, proposal_id: Optional[str] = None) -> bool:
        """Delete a constitutional article, with its own checkpoint, and persist it (a deletion used to stay in memory)."""
        if not authorized:
            self.last_error = "not authorized"
            return False
        if not _is_article_id(article_id):
            # the same rule as apply_mutation: True == 1 and 42.0 == 42 matched, and deleted, real articles
            self.last_error = "an article id must be an integer"
            return False
        pid = proposal_id or f"del-{article_id}-{time.time_ns()}"

        def change(g: Dict[str, Any], h: List[Dict[str, Any]], r: List[Dict[str, Any]]) -> None:
            articles = g["constitution"]["articles"]
            if not any(a.get("id") == article_id for a in articles):
                raise _Refused(f"article {article_id} does not exist")
            self._checkpoint(g, h, pid)
            g["constitution"]["articles"] = [a for a in articles if a.get("id") != article_id]
            _rehash(g)

        ok, _ = self._commit(change)
        if ok:
            ueg.log_event("L1", "Genome", "ARTICLE_DELETED", {"id": article_id, "proposal_id": pid})
        return ok

    def rollback(self, proposal_id: str) -> Dict[str, Any]:
        """Restore the genome to proposal `proposal_id`'s own checkpoint (the genome as it was just before that
        proposal) and persist it. Every change applied after it is discarded too — named in `discarded` — and their
        checkpoints are dropped with it. Refused (rolled_back False, with the reason) for an unknown id."""
        def change(g: Dict[str, Any], h: List[Dict[str, Any]], r: List[Dict[str, Any]]) -> List[str]:
            at = [i for i, cp in enumerate(h) if cp.get("proposal_id") == proposal_id]
            if not at:
                raise _Refused(f"no checkpoint for proposal {proposal_id}")
            if len(at) > 1:
                raise _Refused(f"proposal {proposal_id} names {len(at)} checkpoints; refusing to guess which")
            i = at[0]
            try:
                snapshot = json.loads(h[i]["data"])
            except (KeyError, TypeError, ValueError) as e:
                raise _Refused(f"the checkpoint for proposal {proposal_id} is unreadable ({e})")
            if not _genome_ok(snapshot):
                # checked BEFORE anything is replaced: restoring it would write a store the engine then refuses for ever
                raise _Refused(f"the checkpoint for proposal {proposal_id} is not a genome; nothing was changed")
            discarded = [cp.get("proposal_id") for cp in h[i + 1:]]
            g.clear()
            g.update(snapshot)
            del h[i:]
            r.append({"proposal_id": proposal_id, "at": time.time(), "discarded": discarded})
            return discarded

        ok, out = self._commit(change)
        if not ok:
            return {"rolled_back": False, "proposal_id": proposal_id, "reason": out}
        ueg.log_event("L1", "Genome", "ROLLBACK", {"proposal_id": proposal_id, "discarded": out})
        return {"rolled_back": True, "proposal_id": proposal_id, "discarded": out,
                "root_hash": (self.genome.get("constitution") or {}).get("root_hash")}

    def propose_autonomous_evolution(self, metrics: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """v0.5: Autonomous Constitutional Amendment proposals based on system vitals."""
        # Article 1118: Self-Healing / Self-Evolution
        if metrics.get("latency_ms", 0) > 200:
            return {
                "id": None,          # a new article: apply_mutation assigns its id inside the store lock
                "title": "Autonomous Latency Optimization",
                "content": "The system shall prioritize compute allocation to the C-Suite during high load.",
                "rationale": f"System latency detected at {metrics['latency_ms']}ms."
            }
        return None

    def get_behavioral_params(self) -> Dict[str, Any]:
        """v0.1: Dynamic Behavioral Mapping from Articles."""
        params = {"temperature": 0.7, "system_prompt": "Standard AI CEO"}
        articles = self.genome.get("constitution", {}).get("articles", [])
        for a in articles:
            content = a.get("content", "").lower()
            if "article 42" in content or "transparency" in content:
                params["temperature"] = 0.4
                params["system_prompt"] += " (Transparent & Rigid Mode)"
            if "evolution" in content:
                params["temperature"] = 0.9
        return params


_ENGINE: Optional[GenomeMutationWorkflow] = None


def get_genome_engine() -> GenomeMutationWorkflow:
    """The default engine over GENOME_FILE, loaded on first use (importing this module touches no store)."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = GenomeMutationWorkflow(store_path=GENOME_FILE)
    return _ENGINE


def __getattr__(name: str) -> Any:
    # PEP 562 — `from ...genome_engine import genome_engine` keeps working, lazily
    if name == "genome_engine":
        return get_genome_engine()
    raise AttributeError(name)
