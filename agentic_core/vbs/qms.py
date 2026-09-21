import logging
import time
import uuid
from typing import Dict, Any, List, Optional

from agentic_core.vbs.dcms import DocumentControlManagementSystem


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class QualityManagementSystem:
    """
    VBS: QMS Gatekeeper.
    Enforces ISO 9001-aligned quality thresholds and OAM validation.

    The QMS OWNS the Document Control Management System: in a real quality system (ISO 9001 §7.5),
    control of documented information is a core *function of* the QMS, not a sibling system. So the QMS
    holds the DCMS as its document-control subsystem and exposes `control_document(...)` to place any
    quality record / controlled document under versioned, SHA3-512-sealed control.

    §10 (W307) — genuinely stateful and honest:
    - defects PERSIST (atomic JSON store) and are TRACEABLE (unique id · label · metrics · timestamps);
    - the non-conformance rate is a REAL rate (gate failures / gates run), not a normalised constant;
    - the ISO 8.7/10.2 loop exists: a defect is corrected, then RE-VERIFIED by re-running the same
      gate on the corrected delivery's real metrics — it closes only on a genuine pass, and reopens
      when a correction does not hold.
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger("QMS")
        self.min_coverage = 0.95
        # ── The QMS owns document control (ISO 9001 §7.5). One DCMS instance, owned here.
        self.dcms = DocumentControlManagementSystem(config_path)
        self.controlled_documents = 0
        self._store_name = f"qms_state_{config_path}.json"
        self._state: Optional[Dict[str, Any]] = None

    # ── persistent state (lazy: data_path resolves the live DATA_DIR at first use) ──
    def _load_state(self) -> Dict[str, Any]:
        if self._state is None:
            from agentic_core.config import load_json_tolerant, data_path
            self._state = load_json_tolerant(
                data_path(self._store_name), {"gates_run": 0, "defects_total": 0, "defects": []})
        return self._state

    def _save_state(self) -> None:
        if self._state is not None:
            from agentic_core.config import atomic_write_json, data_path
            atomic_write_json(data_path(self._store_name), self._state)

    @property
    def defects(self) -> List[Dict[str, Any]]:
        return self._load_state()["defects"]

    async def run_quality_gates(self, metadata: Dict[str, Any], label: str = "delivery",
                                owner_id: str | None = None,
                                delivery_ref: Dict[str, Any] | None = None,
                                count_in_rate: bool = True) -> bool:
        """
        Enforces >95% test coverage and zero-stub policy. A failure opens a persistent,
        traceable defect (unique id, the label of the delivery surface, the real metrics,
        and — W320 — the owning tenant where the delivery carries one).
        """
        coverage = float(metadata.get("coverage", 0.0))
        stubs_found = bool(metadata.get("stubs_found", False))
        passed = (coverage >= self.min_coverage) and not stubs_found

        st = self._load_state()
        # W489 (sweep S9.4, C3) — A GATE RUN ON TYPED NUMBERS IS NOT A DELIVERY.
        # The cockpit's Gate button posts a coverage figure the USER TYPES (default 0.97, which passes)
        # and it counted into the same gates_run/gate_failures as every real delivery — on a single
        # platform-wide store shared by every entity and tenant. The chip then called the quotient
        # 'a real rate'. What-if runs are now counted separately and excluded from the rate, so the
        # rate stays what it claims to be: failures over gates run on actual deliveries.
        #   (refutation) The first cut of this RETURNED EARLY for a what-if, which silently stopped it
        # opening a defect at all — so a user who ran a failing gate got no traceable record, and the
        # §10 defect→correction→re-verify loop lost its only user-reachable entry point. Excluding a
        # run from the RATE and refusing to RECORD it are different things. A what-if now does
        # everything a delivery gate does except move the rate: the defect is opened, traceable and
        # correctable, and carries what_if so nothing downstream mistakes it for a delivery failure.
        if count_in_rate:
            st["gates_run"] = int(st.get("gates_run", 0)) + 1
        else:
            st["what_if_gates"] = int(st.get("what_if_gates", 0)) + 1
        if not passed:
            # read the prior count BEFORE defects_total moves: on a pre-W316 store the fallback IS
            # defects_total, so reading it after the increment would double-count this failure
            _prior_failures = self._gate_failures(st)
            st["defects_total"] = int(st.get("defects_total", 0)) + 1
            # §10 (W316) — gate FAILURES are counted separately from distinct defects: a failed
            # re-verification must also count as a failure (previously it inflated the
            # denominator only, so WORSE corrections produced a BETTER reported rate).
            if count_in_rate:
                st["gate_failures"] = _prior_failures + 1
            else:
                st["what_if_failures"] = int(st.get("what_if_failures", 0)) + 1
            st["defects"].append({
                "id": f"DEF-{uuid.uuid4().hex[:8]}",
                "label": label,
                "owner_id": owner_id,   # §14 (W320) — None = platform-level (admin-only under auth)
                "delivery_ref": delivery_ref,   # §10 (W316) — the REAL delivery this defect traces to
                "meta": {"coverage": coverage, "stubs_found": stubs_found},
                # W489 — a defect opened by a what-if is a real record of a real run, and is NOT a
                # delivery failure; it is excluded from the rate and says so on its own row.
                "what_if": not count_in_rate,
                "status": "open",
                "opened_at": _now(),
                "correction": None,
                "reverified": False,
            })
            st["defects"] = st["defects"][-500:]   # bounded list; defects_total keeps the true count
            self.logger.warning(f"QMS: Quality Gate FAILED ({label}). Coverage: {coverage}")
        self._save_state()

        return passed

    def get_non_conformance_rate(self) -> float:
        """Gate FAILURES over gates run (0.0 with no history — never fabricated).

        W489: this is a PLATFORM-WIDE figure. One QMS singleton serves every entity and tenant, so the
        rate is over all deliveries on this installation, not one entity's record — `rate_basis` in
        defect_summary() says so, and the surfaces that render it say so too. What-if gates run on
        typed metrics are excluded from both terms.
        §10 (W316): failures include failed re-verifications; the historical fallback for stores
        written before gate_failures existed is defects_total (the best available true count)."""
        st = self._load_state()
        gates = int(st.get("gates_run", 0))
        return round(self._gate_failures(st) / gates, 4) if gates > 0 else 0.0

    @staticmethod
    def _gate_failures(st: Dict[str, Any]) -> int:
        """Delivery-gate failures. W489 (refutation) — the historical fallback to `defects_total` (for
        stores written before gate_failures existed) was counting WHAT-IF failures as delivery ones:
        a what-if raises defects_total and never gate_failures, so on any store that has only ever
        seen what-ifs the fallback reported them as delivery failures — the exact confusion this round
        separated. The fallback now applies only to a store that predates BOTH keys."""
        if "gate_failures" in st:
            return int(st["gate_failures"])
        if "what_if_gates" in st or "what_if_failures" in st:
            return 0                      # a modern store that has recorded only what-ifs
        return int(st.get("defects_total", 0))      # genuinely pre-W316 store

    # ── §10 (W307) — the defect → correction → re-verify loop (ISO 9001 §8.7 / §10.2) ──
    def correct_defect(self, defect_id: str, correction: str, actor: str = "owner") -> Optional[Dict[str, Any]]:
        """Record the correction taken for an OPEN defect. The defect is not closed here —
        closure requires re-verification against real metrics."""
        st = self._load_state()
        for d in st["defects"]:
            if d["id"] == defect_id and d["status"] == "open":
                d["status"] = "corrected"
                d["correction"] = str(correction)[:2000]
                d["corrected_at"] = _now()
                d["corrected_by"] = actor
                self._save_state()
                return d
        return None

    def reverify_defect(self, defect_id: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Re-run the SAME gate on the corrected delivery's REAL metrics. Closes only on a genuine
        pass; a failed re-verification REOPENS the defect (the correction did not hold)."""
        st = self._load_state()
        for d in st["defects"]:
            if d["id"] == defect_id and d["status"] == "corrected":
                coverage = float(metadata.get("coverage", 0.0))
                stubs_found = bool(metadata.get("stubs_found", False))
                passed = (coverage >= self.min_coverage) and not stubs_found
                # W489 (refutation) — a re-verification is counted the way its DEFECT was. Re-verifying
                # a what-if defect used to move the delivery rate, which made the new rate_basis false
                # the moment a user corrected the defect their own typed gate had opened.
                _what_if = bool(d.get("what_if"))
                if _what_if:
                    st["what_if_gates"] = int(st.get("what_if_gates", 0)) + 1
                else:
                    st["gates_run"] = int(st.get("gates_run", 0)) + 1
                if not passed:
                    # §10 (W316) — a FAILED re-verification RAISES the non-conformance rate
                    # (previously it only inflated the denominator, rewarding bad corrections)
                    if _what_if:
                        st["what_if_failures"] = int(st.get("what_if_failures", 0)) + 1
                    else:
                        st["gate_failures"] = self._gate_failures(st) + 1
                d["reverified"] = passed
                d["reverify_meta"] = {"coverage": coverage, "stubs_found": stubs_found}
                d["reverify_basis"] = str(metadata.get("basis", "caller_attested"))
                d["reverified_at"] = _now()
                d["status"] = "closed" if passed else "open"
                self._save_state()
                return {"defect": d, "passed": passed}
        return None

    def defect_summary(self) -> Dict[str, Any]:
        st = self._load_state()
        by = {"open": 0, "corrected": 0, "closed": 0}
        for d in st["defects"]:
            by[d.get("status", "open")] = by.get(d.get("status", "open"), 0) + 1
        return {"gates_run": int(st.get("gates_run", 0)),
                "defects_total": int(st.get("defects_total", 0)),
                "gate_failures": self._gate_failures(st), **by,
                "non_conformance_rate": self.get_non_conformance_rate(),
                # W489 — what the rate is OVER, and what it deliberately leaves out
                "what_if_gates": int(st.get("what_if_gates", 0)),
                "what_if_failures": int(st.get("what_if_failures", 0)),
                "rate_basis": ("gate failures / gates run across ALL deliveries on this platform (every "
                               "entity and tenant share one QMS store) — not one entity's record. "
                               "What-if gates run on typed metrics, and re-verifications of the defects "
                               "they open, are counted separately and excluded. A re-verification of a "
                               "DELIVERY defect does count, including one attested by its caller "
                               "(W316: a correction that does not hold must raise the rate).")}

    async def control_document(self, doc_id: str, content: Dict[str, Any], actor: str) -> str:
        """Place a document under QMS document control — versioned + SHA3-512 sealed via the OWNED DCMS.
        Returns the controlled-document hash (the proof the record is under quality document control)."""
        h = await self.dcms.commit_artifact(doc_id, content, actor)
        self.controlled_documents += 1
        return h

    def document_control_status(self) -> Dict[str, Any]:
        """The QMS's document-control posture — proves the DCMS is owned and operating under the QMS."""
        return {
            "owned_subsystem": "DCMS (Document Control Management System)",
            "controlled_documents": self.controlled_documents,
            "registered_artifacts": len(self.dcms.registry),
            "audit_integrity": self.dcms.get_audit_integrity(),
        }
