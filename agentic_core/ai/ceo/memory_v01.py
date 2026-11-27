"""
The C-Suite meeting log (MeetingLog and its instance meeting_log), which the AI CEO's debate flow writes and reads.

THE AVATAR AND UPLOAD MEMORY IS RETIRED (W1196, FU-1843), as the Owner ruled on 2026-11-22 (P3.32). This module
held it: MemoryV01 and its instance, which every avatar message and every extracted upload wrote and which no
production caller read back. It opened a chromadb collection with no embedding function, so its first write fetched
chromadb's default embedding model from an outside host into the user's home; its client kept everything in this
process only, while this docstring said the memory was kept for good. MemoryV01, its instance and the chromadb
import are removed, so nothing writes that memory, nothing reads it and nothing fetches a model for it. The AI CEO
and the avatars recall from VectorMemory (agentic_core/ai/memory.py), which this does not change.

The ruling's reason, which any later memory must meet: if conversation memory is wanted later, it is to be built
after sign-in, with a retention period and with no outside download. chromadb stays declared until the dependency
round (W1230) removes it; no module imports it.
"""
import datetime as _dt


class MeetingLog:
    """The C-Suite debate record.

    W400 - this was a type('Mock', ...) whose lambdas took no self, so EVERY bound call raised
    "TypeError: <lambda>() takes 0 positional arguments but 1 was given". Two live paths hit it:
    GET /api/v138/ceo/meeting/minutes (a 500 on a plain GET) and ceo.py's debate flow, which calls
    get_recent_debate() before synthesising. post_argument survived only because "lambda *a" happens
    to swallow self - so every argument the C-Suite posted went nowhere, silently.

    It also returned the literal string "# Minutes" as the meeting minutes. It now records what was
    actually argued and renders that; with nothing recorded it says so, rather than emitting a
    header that looks like a document.
    """

    MAX_ENTRIES = 500

    def __init__(self) -> None:
        self.log: list[dict] = []

    def post_argument(self, agent: str, argument: str, stance: str = "", served_by: str = "") -> None:
        self.log.append({
            "agent": agent,
            "argument": argument,
            "stance": stance,
            "served_by": served_by,          # W475 (ledger v4 R3.0) — who produced the position
            "at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        })
        del self.log[:-self.MAX_ENTRIES]

    def get_recent_debate(self, limit: int = 12) -> str:
        recent = self.log[-limit:]
        if not recent:
            return "No recent debates recorded."
        out = []
        for e in recent:
            stance = " (" + e["stance"] + ")" if e.get("stance") else ""
            out.append(e["agent"] + stance + ": " + e["argument"])
        return chr(10).join(out)

    def export_minutes(self) -> str:
        if not self.log:
            return ("# C-Suite meeting minutes" + chr(10) + chr(10)
                    + "No arguments have been recorded. Nothing is minuted because nothing was said."
                    + chr(10))
        lines = ["# C-Suite meeting minutes", ""]
        for e in self.log:
            stance = " - **" + e["stance"] + "**" if e.get("stance") else ""
            lines.append("- `" + str(e.get("at", "")) + "` **" + e["agent"] + "**"
                         + stance + ": " + e["argument"])
        lines.append("")
        lines.append("_" + str(len(self.log)) + " argument(s) recorded._")
        return chr(10).join(lines)


meeting_log = MeetingLog()
