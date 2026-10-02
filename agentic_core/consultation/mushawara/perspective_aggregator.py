import numpy as np
from typing import List, Dict, Any

class PerspectiveAggregator:
    """Aggregate the positions a deliberation produced.

    W538 (FU-343) — this took an `mjm_learner` and stored it as self.mjm. Its only constructor passed None and
    NOTHING ever read the attribute, on any path. The seam is removed rather than wired: consulting the MJM
    tier would import agentic_core/mjm's figures, and those were typed rather than measured until this same
    round fixed them. A parameter that is always None and never read is not an extension point, it is a
    statement that an extension was intended; the intent belongs in the register, where FU-343 records it.
    """

    def __init__(self, mjm_learner=None):
        #  accepted and ignored, so no caller breaks; it is not stored, so no reader can mistake it for wired
        self.mjm_learner_accepted_and_unused = mjm_learner is not None

    async def synthesize(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate what the perspectives ACTUALLY carry, and say what is missing.

        W533 — this previously bundled a 10,000-dimensional vector that every caller supplied as a constant
        array of ones. With all vectors identical, the agreement expression mean(|sum(w_i*V_i)|)/n reduces
        algebraically to sum(w_i)/n: the aggregate named "agreement" WAS the arithmetic mean of the engines'
        confidences, and could not express disagreement, because identical vectors agree by construction.
        sign(v_sum) likewise made the consensus a constant. A computed figure over invented inputs survives
        an audit that only asks whether a number is a literal, which is why it is spelled out here.

        It also could not run. `confidence` is three-state (None = nothing computed it), and this multiplied
        by it, so a refusing engine raised a TypeError -- which is what stopped the recirculation loop at
        stage ANALYZE.

        Agreement is now CONCORDANCE OF THE CONSTITUTIONAL VERDICTS, which is a real disagreement the
        perspectives can actually express, reported three-state with the coverage it was computed over. The
        mean confidence keeps its own name. The hyperdimensional path is kept for real vectors and refuses
        rather than inventing them.
        """
        n = len(responses)
        if not responses:
            return {"consensus_vector": None,
                    "consensus_vector_basis": "no perspectives were supplied, so nothing was bundled",
                    "agreement_score": None,
                    "agreement_basis": "no perspectives were supplied, so concordance is undefined",
                    "confidence_mean": None,
                    "confidence_basis": "no perspectives were supplied",
                    "verdicts_supplied": 0,
                    "engine_count": 0}

        vecs = [r.get("vector") for r in responses]
        supplied = [v for v in vecs if v is not None]
        confs = [r.get("confidence") for r in responses]
        numeric = [c for c in confs if isinstance(c, (int, float)) and not isinstance(c, bool)]
        verdicts = [(r.get("trace") or {}).get("passed") for r in responses]
        opinions = [v for v in verdicts if v is not None]

        # ── the hyperdimensional bundle, only over vectors something actually computed ──────────
        if len(supplied) == n and len({len(v) for v in supplied}) == 1:
            weighted = len(numeric) == n
            v_sum = np.zeros(len(supplied[0]))
            for v, w in zip(supplied, confs):
                v_sum += (w if weighted else 1.0) * np.array(v)
            consensus = np.sign(v_sum).tolist()
            consensus_basis = (f"bundled over {n} supplied vector(s) of {len(supplied[0])} dimension(s), "
                               + ("weighted by each engine's confidence" if weighted else
                                  f"UNWEIGHTED: only {len(numeric)} of {n} engines reported a confidence, "
                                  "and a weight nothing computed would be invented"))
        else:
            consensus, consensus_basis = None, (
                f"NOT BUNDLED: {len(supplied)} of {n} perspective(s) supplied a vector"
                + ("" if len(supplied) != n else " but their dimensions differ")
                + ". No embedding is fabricated to stand in for a missing one")

        # ── agreement = concordance of the verdicts, three-state, with its coverage ─────────────
        if not opinions:
            agreement, agreement_basis = None, (
                f"NOT COMPUTED: none of the {n} perspective(s) supplied a constitutional verdict (all are "
                "three-state None, meaning nothing assessed them), so concordance is undefined. This is "
                "not agreement and must never be read as 1.0")
        else:
            modal = max({True, False} & set(opinions), key=opinions.count)
            agreement = opinions.count(modal) / len(opinions)
            agreement_basis = (f"{opinions.count(modal)} of {len(opinions)} verdict(s) agree on "
                               f"passed={modal}; computed over {len(opinions)} of {n} perspective(s), the "
                               f"other {n - len(opinions)} having supplied no verdict")

        return {
            "consensus_vector": consensus,
            "consensus_vector_basis": consensus_basis,
            "agreement_score": agreement,
            "agreement_basis": agreement_basis,
            "confidence_mean": (sum(numeric) / len(numeric)) if numeric else None,
            "confidence_basis": (f"mean over {len(numeric)} of {n} engine(s) that reported one"
                                 if numeric else
                                 f"NOT COMPUTED: none of the {n} engine(s) reported a confidence"),
            "verdicts_supplied": len(opinions),
            "engine_count": n,
        }
