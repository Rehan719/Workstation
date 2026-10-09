"""Exact-once, line-ending-preserving source edits — the helper every round since W602 has used.

    from scripts.round_tools.patch import patch
    patch("agentic_core/api/vsb.py", [("old text\\n", "new text\\n")])

Each `old` must occur EXACTLY ONCE in the file (after CRLF is normalised to LF), or the edit is refused and
nothing is written. Write anchors with plain "\\n": a CRLF file is converted to LF for matching and converted
back on write, byte for byte. Never use pathlib.write_text for source edits — on Windows it rewrites every
line ending (W599 committed a whole-file EOL flip that way).
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def patch(path, reps, root=ROOT):
    p = pathlib.Path(root) / path
    raw = p.read_bytes()
    crlf = b"\r\n" in raw
    s = raw.decode("utf-8").replace("\r\n", "\n") if crlf else raw.decode("utf-8")
    for old, new in reps:
        n = s.count(old)
        if n != 1:
            raise SystemExit(f"REFUSED {path}: anchor matched {n} times (must be exactly 1): {old[:80]!r}")
        s = s.replace(old, new)
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))


if __name__ == "__main__":
    sys.exit("import patch() from this module; it has no CLI")
