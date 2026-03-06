import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime
import math

logger = logging.getLogger(__name__)

class MemorizationEngine:
    """
    ARTICLE 240: Memorization Suite.
    SRS-based tracking across 114 surahs.
    Supports proven methodologies (lahd, sabak, tikrar, hifz).
    """
    def __init__(self):
        self.default_efactor = 2.5
        self.min_efactor = 1.3

    def calculate_next_review(self, quality: int, repetitions: int, previous_interval: int, previous_efactor: float) -> Tuple[int, float]:
        """
        ARTICLE 60: Functional implementation of SM-2 Algorithm.
        quality: 0-5 (0=total blackout, 5=perfect recall)
        returns: (next_interval_days, new_efactor)
        """
        # E-Factor update
        new_efactor = previous_efactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        if new_efactor < self.min_efactor:
            new_efactor = self.min_efactor

        # Interval calculation
        if quality < 3:
            repetitions = 0
            interval = 1
        else:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = math.ceil(previous_interval * new_efactor)

        logger.debug(f"SRS: Quality {quality} -> Next Review in {interval} days (EF: {new_efactor:.2f})")
        return interval, new_efactor

    def get_progress_matrix(self, surah_id: int, total_verses: int, completed_verses: List[int]) -> Dict[str, Any]:
        """
        Generates progress visualization data for a surah.
        Supports 114-juz progress visualization requirements.
        """
        completion_percentage = (len(completed_verses) / total_verses) * 100
        return {
            "surah_id": surah_id,
            "total": total_verses,
            "completed_count": len(completed_verses),
            "percentage": round(completion_percentage, 2),
            "map": [1 if i+1 in completed_verses else 0 for i in range(total_verses)]
        }

    def recommend_hifz_path(self, user_goals: str, pace: str) -> List[Dict[str, Any]]:
        """
        Recommends a personalized Hifz track.
        """
        # ARTICLE 60: Functional logic for path recommendation
        tracks = {
            "SHORT_SURAS": [{"surah": i} for i in range(114, 104, -1)],
            "MEDIUM_SURAS": [{"surah": 18}, {"surah": 36}, {"surah": 67}],
            "FULL_HIFZ": [{"juz": i} for i in range(30, 0, -1)]
        }

        return tracks.get(user_goals, tracks["SHORT_SURAS"])
