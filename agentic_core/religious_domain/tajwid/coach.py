import logging
import re
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

_ARABIC = re.compile(r"[؀-ۿ]")


class TajwidCoach:
    """Written-recall comparison against an authoritative ayah text — TEXT ONLY.

    W439 honesty rewrite. The old class claimed "real-time recitation analysis with feedback on
    makharij, sifat, and ahkam" over "10 Qira'at", and "emulated phoneme-level pitch contour
    extraction". None of that existed: it Levenshtein-compared the Arabic reference against
    WHATEVER STRING arrived (the API passed English educator notes, or the literal default
    "No audio — text-based analysis only."), then reported the garbage ratio as recitation
    "accuracy" with a HARDCODED confidence of 0.95 and a "makharij" verdict a text diff cannot
    make. A fabricated judgement about someone's recitation of the Qur'an is the repo's W403
    "false witness" case — the exact thing the frontend was already scrubbed of.

    What a text engine can honestly do, it now does: compare the learner's TYPED Arabic
    recollection with the authoritative text (real normalised Levenshtein), and report which
    madd/ghunnah MARKERS present in the reference are missing from the written attempt — a
    memorisation aid about the WRITTEN text. It refuses non-Arabic input instead of scoring it,
    and it makes no claim about pronunciation, articulation, or recitation. Two riwayah rule-sets
    are configured (Hafs, Warsh) — two, not "10 Qira'at".
    """

    def __init__(self, qiraat: str = "Hafs"):
        self.qiraat_rules = self._load_qiraat_rules()
        # W439 audit catch: an unknown riwayah used to be accepted silently and echoed in the
        # payload as if a qiraat-aware comparison ran; unconfigured values fall back, disclosed.
        self.qiraat = qiraat if qiraat in self.qiraat_rules else "Hafs"
        self.qiraat_fallback = qiraat if qiraat not in self.qiraat_rules else None

    def _load_qiraat_rules(self) -> Dict[str, Any]:
        """Rule-marker sets for the CONFIGURED riwayat (two exist; nothing claims more)."""
        return {
            "Hafs": {"madd_length": [2, 4, 5], "ghunnah_active": True},
            "Warsh": {"madd_length": [2, 6], "taghlib_lam": True},
        }

    def compare_written_recall(self, reference_text: Any, recited_text: Any) -> Dict[str, Any]:
        """Compare a typed Arabic recollection against the authoritative reference text."""
        if isinstance(reference_text, bytes):
            reference_text = reference_text.decode("utf-8", errors="ignore")
        if isinstance(recited_text, bytes):
            recited_text = recited_text.decode("utf-8", errors="ignore")
        reference_text = (reference_text or "").strip()
        recited_text = (recited_text or "").strip()

        if not reference_text or not _ARABIC.search(reference_text):
            return {"comparable": False,
                    "reason": "the reference text is empty or not Arabic — nothing to compare against"}
        if not recited_text or not _ARABIC.search(recited_text):
            return {"comparable": False,
                    "reason": ("the written attempt is empty or contains no Arabic — the old code "
                               "scored whatever string arrived; nothing is scored that cannot be "
                               "compared")}

        similarity = self._levenshtein_similarity(reference_text, recited_text)
        missing_markers = self._missing_rule_markers(reference_text, recited_text)

        result = {
            "comparable": True,
            "qiraat": self.qiraat,
            **({"qiraat_note": f"requested riwayah {self.qiraat_fallback!r} is not configured - "
                               f"compared using the Hafs marker set"}
               if self.qiraat_fallback else {}),
            "text_similarity": round(similarity, 4),
            "similarity_basis": ("normalised Levenshtein distance between the typed attempt and "
                                 "the authoritative text — a WRITTEN-recall measure only"),
            "missing_rule_markers": missing_markers,
            "markers_basis": ("madd/ghunnah character sequences present in the reference but "
                              "absent from the written attempt — an aid for memorising the "
                              "written text, not a judgement of pronunciation"),
            "scope": ("TEXT comparison only. This says NOTHING about recitation, pronunciation, "
                      "makharij, or sifat — assessing those requires hearing the recitation, and "
                      "no phonetic model is provisioned."),
            "timestamp": datetime.now().isoformat(),
        }
        logger.info("TajwidCoach: written recall compared, similarity %.3f", similarity)
        return result

    def _levenshtein_similarity(self, ref: str, usr: str) -> float:
        """Real normalised Levenshtein similarity (1.0 = identical)."""
        ref_n, usr_n = ref.strip(), usr.strip()
        if ref_n == usr_n:
            return 1.0
        rows, cols = len(ref_n) + 1, len(usr_n) + 1
        dist = [[0] * cols for _ in range(rows)]
        for i in range(1, rows):
            dist[i][0] = i
        for j in range(1, cols):
            dist[0][j] = j
        for col in range(1, cols):
            for row in range(1, rows):
                cost = 0 if ref_n[row - 1] == usr_n[col - 1] else 1
                dist[row][col] = min(dist[row - 1][col] + 1, dist[row][col - 1] + 1,
                                     dist[row - 1][col - 1] + cost)
        return 1.0 - (dist[rows - 1][cols - 1] / max(len(ref_n), len(usr_n)))

    def _missing_rule_markers(self, ref: str, usr: str) -> List[str]:
        """Rule-relevant character sequences present in the reference but absent in the attempt."""
        missing = []
        madd_chars = {"َا": "madd (fatha+alif)", "ُو": "madd (damma+waw)",
                      "ِي": "madd (kasra+ya)"}
        for seq, label in madd_chars.items():
            if seq in ref and seq not in usr:
                missing.append(f"{label} sequence present in reference, absent in attempt")
        # W439 audit catch: the old check required " نْ " with surrounding SPACES — a standalone
        # token that never occurs in real Quran text, so the marker could never fire (a blind
        # instrument). Nun-sukun occurs mid-word and word-final; match it bare.
        if self.qiraat == "Hafs" and "نْ" in ref and "نْ" not in usr:
            missing.append("sakin nun (ghunnah context) present in reference, absent in attempt")
        return missing
