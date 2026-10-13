"""MEMORISATION PRACTICE - arithmetic over the FETCHED text; nothing here composes, alters or judges.

OWNER RULINGS 2026-10-12 (the plan item for the Quran platform's four areas, first clause): a portion plan in
three tracks set by the learner or a teacher, with NO default portions until a named source on the method has
been read and entered; hidden-verse practice; similar verses drilled as pairs, COMPUTED from the sourced text by
exact shared wording. The canon binds all of it: the Arabic is fetched and never generated; recitation is never
scored; nothing may appear to correct a live recitation.

WHAT THESE FUNCTIONS DO AND DO NOT DO
- They receive verse text the caller FETCHED from the named source and return positions and counts over it.
  A word here is a run of characters between spaces in the text as given - the text is cut, never changed, and a
  returned piece is always a contiguous slice of what was given.
- `similar_pairs` finds verses that share a run of identical words. It is exact matching: two verses that differ
  by one letter or one mark in the shared part are NOT paired, and that is said in every answer. It makes no
  claim that a pair is one a learner would confuse - only that the wording is shared.
- Nothing here knows whether a learner recalled a verse. The learner says so themselves.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, Tuple

TRACKS = ("new_lesson", "recent_revision", "old_revision")
UNITS = ("ayah_range", "page", "juz")
MIN_SHARED_WORDS = 3          # the least run of identical words that makes a pair (stated in every answer)
MIN_SHARED_WORDS_FLOOR = 2    # a caller may ask for more, never fewer than this


def words(text: str) -> List[str]:
    """The text as given, cut at spaces. Joining the result with single spaces gives the text back when the
    text had single spaces; nothing is normalised, stripped of marks or re-ordered."""
    return [w for w in str(text or "").split(" ") if w]


def hidden_view(text: str, shown_words: int = 1) -> Dict[str, Any]:
    """What a learner sees before recalling: the first `shown_words` words and how many remain. The rest is NOT
    in the answer - a page cannot leak what it was never sent."""
    w = words(text)
    n = max(0, min(int(shown_words), len(w)))
    return {"shown": " ".join(w[:n]), "shown_words": n, "hidden_words": len(w) - n, "total_words": len(w),
            "basis": ("the first words of the verse as fetched from the named source, cut at spaces; the hidden "
                      "part is not sent until it is asked for")}


def next_word(text: str, after_words: int) -> Dict[str, Any]:
    """The one word that follows the first `after_words` words - what a learner taps for when they pause.
    It reports a position in the fetched text. It says nothing about what the learner recited."""
    w = words(text)
    k = max(0, int(after_words))
    if k >= len(w):
        return {"word": None, "position": len(w), "total_words": len(w), "end_of_verse": True}
    return {"word": w[k], "position": k + 1, "total_words": len(w), "end_of_verse": k + 1 == len(w)}


def _longest_shared_run(a: Sequence[str], b: Sequence[str]) -> Tuple[int, int, int]:
    """(length, start in a, start in b) of the longest run of identical consecutive words. Ties: the earliest
    in `a`, then the earliest in `b` - a stated order, so the answer does not depend on iteration."""
    best = (0, 0, 0)
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best[0]:
                    best = (cur[j], i - cur[j], j - cur[j])
        prev = cur
    return best


def similar_pairs(verses: Iterable[Dict[str, Any]], min_shared_words: int = MIN_SHARED_WORDS,
                  limit: int = 200) -> Dict[str, Any]:
    """Pairs of verses that share a run of at least `min_shared_words` identical words.

    `verses` is [{"ref": "2:255", "text": <as fetched>}, ...]. The answer names how many verses were examined,
    because a list computed over part of the text is a list over that part and nothing more.
    """
    k = max(MIN_SHARED_WORDS_FLOOR, int(min_shared_words))
    items = [(str(v.get("ref")), words(v.get("text"))) for v in verses if v.get("ref") and v.get("text")]
    # index every run of k words, so only verses that share one are compared
    seen: Dict[Tuple[str, ...], List[int]] = {}
    for idx, (_ref, w) in enumerate(items):
        for s in range(0, len(w) - k + 1):
            seen.setdefault(tuple(w[s:s + k]), []).append(idx)
    candidates = set()
    for holders in seen.values():
        uniq = sorted(set(holders))
        for x in range(len(uniq)):
            for y in range(x + 1, len(uniq)):
                candidates.add((uniq[x], uniq[y]))
    pairs = []
    for i, j in candidates:
        length, sa, sb = _longest_shared_run(items[i][1], items[j][1])
        if length >= k:
            wa, wb = items[i][1], items[j][1]
            pairs.append({
                "a": items[i][0], "b": items[j][0], "shared_words": length,
                "shared": " ".join(wa[sa:sa + length]),
                "a_from_word": sa + 1, "b_from_word": sb + 1,
                # where each verse goes its own way - the point a learner has to hold apart
                "a_continues": wa[sa + length] if sa + length < len(wa) else None,
                "b_continues": wb[sb + length] if sb + length < len(wb) else None,
                "whole_verse_identical": wa == wb,
            })
    pairs.sort(key=lambda p: (-p["shared_words"], p["a"], p["b"]))
    cut = max(1, int(limit))
    return {
        "pairs": pairs[:cut], "pairs_found": len(pairs), "pairs_returned": min(len(pairs), cut),
        "verses_examined": len(items), "min_shared_words": k,
        "basis": (f"exact matching over the {len(items)} verse(s) given, each as fetched from the named source: "
                  f"two verses are paired when they share a run of at least {k} identical words. Verses that "
                  "differ by a letter or a mark inside the shared part are NOT paired. This is shared wording, "
                  "counted - not a list of what a learner will confuse, and not a scholar's list of similar "
                  "verses."),
    }


def validate_portion(track: str, unit: str, start: Any, end: Any) -> Dict[str, Any]:
    """A portion a learner or teacher SET. Nothing is proposed: there are no default portions until a named
    source on the method has been read and entered in the register of sources."""
    problems = []
    if track not in TRACKS:
        problems.append(f"track must be one of {list(TRACKS)}")
    if unit not in UNITS:
        problems.append(f"unit must be one of {list(UNITS)}")
    if unit == "page":
        ok = isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= 604
        if not ok:
            problems.append("a page portion is two whole numbers, 1 to 604, first not after last (the "
                            "fifteen-line Madinah page, the one layout in use)")
    elif unit == "juz":
        ok = isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= 30
        if not ok:
            problems.append("a juz portion is two whole numbers, 1 to 30, first not after last")
    elif unit == "ayah_range":
        def _ref(x):
            try:
                s, a = str(x).split(":")
                return int(s), int(a)
            except (ValueError, AttributeError):
                return None
        a, b = _ref(start), _ref(end)
        if not a or not b or not (1 <= a[0] <= 114 and 1 <= b[0] <= 114 and a[1] >= 1 and b[1] >= 1) or a > b:
            problems.append("an ayah range is 'surah:ayah' to 'surah:ayah', first not after last; whether each "
                            "ayah exists is checked against the source's own count when the portion is opened")
    return {"ok": not problems, "problems": problems}
