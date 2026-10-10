"""
Constitutional Policy Gate — GaaS v5.

A deterministic, explainable pre/post execution gate (Article 11.1). It screens
an agent action *before* it runs and screens the produced output *afterwards*.
Every denial carries a human-readable reason and the constitutional article it
derives from, so decisions are auditable rather than opaque.
"""
from __future__ import annotations

import re
from typing import Any, Dict

# Intents an autonomous agent may never execute without explicit human escalation.
#  W580 (FU-372) — DRIVEN, and the result split two ways. These are matched as SUBSTRINGS of a
#  lowercased intent, so they catch the snake_case label a caller generates and MISS the same intent
#  written any other way: "delete all records" and "drop database" went straight through, because a
#  space is not an underscore. Seven of sixteen driven intents were missed.
#  TWO REMEDIES, kept apart on purpose.
#  (1) THE SPELLING IS NORMALISED rather than enumerated — see _normalise_intent below. Normalising is
#      strictly safer than adding patterns: it cannot widen WHAT is prohibited, only how it may be
#      spelled, so it introduces no new way to refuse a legitimate action.
#  (2) THE SYNONYMS OF DESTRUCTION ARE ADDED, because a gate that stops `delete_all` and allows
#      `purge_all_data` is not screening the act, it is screening one author's vocabulary.
#  AND THE LIMIT IS DECLARED: see _COVERAGE_LIMIT. A prose sentence of intent is NOT reliably screened
#  here and must not be treated as cleared by it.
_PROHIBITED_INTENTS = {
    "delete_all", "drop_database", "exfiltrate", "self_replicate_uncontrolled",
    "disable_governance", "bypass_constitution", "mass_email", "wire_funds",
    "rm_rf_root",
    #  W580 (FU-372) — added by the driven list
    "purge_all", "wipe_all", "wipe_everything", "truncate_all", "truncate_table",
    "destroy_all", "erase_all", "drop_all",
}

#  W580 (FU-372) — WHAT THIS SCREEN DOES NOT COVER, stated so a caller cannot read a pass as a clearance.
#  It matches tokens inside an intent LABEL. A free-prose intent ("transfer funds to an external
#  account", "turn off the constitution") expresses a prohibited act in words this screen does not
#  model, and widening it to prose would mean writing a language model as a regex. Those belong to a
#  screen that reads prose; this one says it did not read it.
_OUTPUT_COVERAGE_LIMIT = (
    "screened for a small set of unsafe payload patterns only (a destructive shell command, DROP / "
    "TRUNCATE, an unbounded DELETE, a private-key header). `compliant` means none of those matched. It is "
    "NOT an assessment of the output against the constitution, the law or any framework."
)
_COVERAGE_LIMIT = (
    "matches tokens inside an intent LABEL after normalising separators and case. A free-prose "
    "sentence of intent is NOT reliably screened here: `allowed: True` from this gate means no "
    "prohibited token was found in the label, never that the action was understood and cleared."
)


def _normalise_intent(raw: str) -> str:
    """Lowercase, and collapse every separator to a single underscore.

    W580 (FU-372) — so `delete all records`, `Delete-All-Records` and `delete_all_records` are the same
    label to this screen. The driven list showed the gate stopping `delete_all` and allowing `delete all
    records`, which is a gate on a spelling rather than on an act.
    """
    import re as _re
    out = _re.sub(r"[^a-z0-9]+", "_", str(raw or "").lower())
    return _re.sub(r"_+", "_", out).strip("_")

# Output markers indicating a constitutional violation / unsafe payload.
#  W580 (FU-372) — DRIVEN: four of eleven payloads were missed, and each is the same act in another
#  form. `-----BEGIN\s+(RSA|OPENSSH|PRIVATE)` enumerated THREE key types, so an EC or PGP private key —
#  the same secret — passed; and `DROP TABLE` was the only destructive statement listed, so TRUNCATE and
#  an unbounded DELETE passed. The key's ALGORITHM is incidental to the fact that it is a private key,
#  and that is what this screen is for.
_UNSAFE_OUTPUT = re.compile(
    r"(rm\s+-rf\s+/"
    r"|DROP\s+(?:TABLE|DATABASE|SCHEMA)"
    r"|TRUNCATE\s+TABLE"
    r"|DELETE\s+FROM\s+\w+\s+WHERE\s+1\s*=\s*1"          # an unbounded delete wearing a WHERE
    r"|DELETE\s+FROM\s+\w+\s*(?:;|$)"                       # or with no WHERE at all
    r"|--no-preserve-root"
    r"|-----BEGIN\s+[A-Z0-9 ]*PRIVATE\s+KEY"                  # any algorithm: EC, PGP, DSA, RSA
    r"|-----BEGIN\s+(?:RSA|OPENSSH|PRIVATE))",
    re.IGNORECASE,
)


class ConstitutionalPolicyGate:
    """Deterministic pre/post action gate (Articles 11.1 + 7.3)."""

    def __init__(self, domain: str = "global"):
        self.domain = domain

    def validate(self, action_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Pre-execution gate. Returns ``{allowed, reason, article}``."""
        # W580 (FU-372) — NORMALISED, not merely lowercased. The driven list showed this gate stopping
        # `delete_all` and allowing `delete all records`: a space is not an underscore, so the screen was
        # on a spelling rather than on an act. Normalising cannot widen WHAT is prohibited, only how it
        # may be written, so it adds no way to refuse a legitimate action.
        raw_intent = str(action_type or context.get("intent", ""))
        intent = _normalise_intent(raw_intent)

        for prohibited in _PROHIBITED_INTENTS:
            if prohibited in intent:
                return {
                    "allowed": False,
                    # the RAW label is reported, because that is what the caller sent and what they must
                    # recognise; the normalised form is what matched and is named beside it
                    "reason": f"Intent '{raw_intent}' is constitutionally prohibited "
                              f"(matched '{prohibited}' in the normalised label '{intent}')",
                    "article": "11.1",
                }

        if context.get("requires_human") and not context.get("human_approved"):
            return {
                "allowed": False,
                "reason": "Action requires human approval that was not granted",
                "article": "7.3",
            }

        # W580 (FU-372) — A PASS SAYS WHAT IT DID NOT SCREEN. `allowed: True` was a bare boolean, and the
        # driven list is the reason that matters: this gate reads an intent LABEL, so a prose sentence
        # expressing a prohibited act ("transfer funds to an external account") passes it. Widening the
        # screen to prose would mean writing a language model as a regex; declaring the limit, and
        # carrying that declaration to whoever reads `allowed`, is the honest alternative — a caller can
        # then route a prose intent to something that reads prose instead of taking this as a clearance.
        return {"allowed": True, "reason": None, "article": None,
                "screened": "intent_label", "coverage_limit": _COVERAGE_LIMIT,
                "label_screened": intent}

    def validate_output(self, output: Any) -> Dict[str, Any]:
        """Post-execution gate. Returns ``{compliant, violations}``."""
        text = output if isinstance(output, str) else str(output)
        match = _UNSAFE_OUTPUT.search(text)
        #  W656 (ledger v15 R6.4) - A PASS SAYS WHAT IT SCREENED, as the pre-gate's has since W580. `compliant`
        #  keeps its meaning for its readers; these two say how narrow the check behind it is.
        if match:
            return {"compliant": False,
                    "violations": [f"Unsafe pattern detected in output: '{match.group(0).strip()}'"],
                    "screened": "unsafe_payload_patterns", "coverage_limit": _OUTPUT_COVERAGE_LIMIT}
        return {"compliant": True, "violations": [],
                "screened": "unsafe_payload_patterns", "coverage_limit": _OUTPUT_COVERAGE_LIMIT}
