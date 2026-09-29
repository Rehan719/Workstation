import re

# W505 (P2.6) — A TERM AND A HARMFUL OBJECT, not a bare substring. The previous list matched "malware",
# "hacker" and "exploit" anywhere in the text, case-insensitively and without word boundaries, and a False
# verdict makes the gateway REPLACE the answer with a policy notice - so the user lost the whole answer for
# writing "exploit the market opportunity" (P2.6's own acceptance example), "malware detection guidance",
# "growth hacker" or "exploitation of a resource".
#
# A word list cannot distinguish exploiting a vulnerability from exploiting an opportunity. The standing rule
# in this programme is that a screen may FLAG and escalate but never CLEAR, so this is narrowed to what a list
# can honestly do: a term counts only when a harmful object appears near it. Nothing matching means nothing
# matched - it is not a safety clearance, and `screen_reason` says so.
_TERMS = (r"malware", r"ransomware", r"spyware", r"keylogger", r"rootkit",
          r"exploit", r"exploits", r"exploiting", r"hacker", r"hackers", r"hacking")
_HARMFUL_OBJECT = (r"vulnerabilit(?:y|ies)", r"zero[- ]day", r"cve-\d", r"unpatched", r"payload",
                   r"privilege escalation", r"backdoor", r"credential(?:s)? (?:theft|dump|stuffing)",
                   r"exfiltrat(?:e|ion)", r"botnet", r"command[- ]and[- ]control",
                   r"bypass (?:authentication|the gate|detection)")
_WINDOW = 120   # characters either side — a term and its object in the same clause, not the same document


def screen_reason(text: str) -> str:
    """Why the screen refused, or "" when nothing matched. A term alone is NOT a refusal."""
    body = text or ""
    for term in _TERMS:
        for m in re.finditer(r"\b" + term + r"\b", body, re.IGNORECASE):
            near = body[max(0, m.start() - _WINDOW): m.end() + _WINDOW]
            for obj in _HARMFUL_OBJECT:
                om = re.search(obj, near, re.IGNORECASE)
                if om:
                    return (f"the term {m.group(0)!r} appears within {_WINDOW} characters of "
                            f"{om.group(0)!r}")
    return ""


def validate_response(text: str) -> bool:
    """False only when a listed term appears NEAR a harmful object. True means nothing matched.

    W505 (P2.6) — True is not a safety clearance. A word list cannot clear text; it can only fail to
    match, and the caller must not present a True here as "screened safe". `screen_reason` gives the
    refusal's basis when there is one."""
    return not screen_reason(text)
