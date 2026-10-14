"""NO CREDENTIAL IS COMMITTED TO THIS REPOSITORY (W729).

Found on 2026-10-14: three archived copies of one pasted text file carried an environment block with real
values - an AI provider key, a database address with its password, a sign-in client secret, an email password
and more - in a PUBLIC repository since June. The values were redacted and are revoked at their providers.
This test reads every tracked file and fails on a key-shaped value, so the next one cannot arrive unnoticed.
It reports the path, the line and the KIND, and never prints a value.
"""
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
#  each pattern is written so that it does not match its own source text
SHAPES = [
    ("an AI provider key", re.compile(r"sk-(?:proj-|ant-)?[A-Za-z0-9_\-]{32,}")),
    ("a payment provider key", re.compile(r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}")),
    ("a webhook signing secret", re.compile(r"whsec_[A-Za-z0-9]{24,}")),
    ("a Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("a Google sign-in client secret", re.compile(r"GOCSPX-[A-Za-z0-9_\-]{20,}")),
    ("a database address with a password", re.compile(r"mongodb(?:\+srv)?://[^\s:/@<]+:[^\s@/<]{4,}@")),
    ("a source-host token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("a cloud access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("a private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("a service-account file", re.compile(r'"type"\s*:\s*"service_account"')),
]
#  a file that holds the SHAPE on purpose, as a phrase its own screen must recognise - by exact path and kind
ALLOWED = {("scripts/screen_phrasings.py", "a private key block")}
REDACTED = ["_archive/docs/archive/AI-Driven Quranic Education Platfor SAVED.txt",
            "_archive/docs/background/AI-Driven Quranic Education Platfor SAVED.txt",
            "_archive/docs/background_text_files_sources/historical_directives/AI-Driven Quranic Education Platfor SAVED.txt"]
MARK = "<REDACTED-2026-10-14: a credential was pasted here; it is revoked at its provider>"


def _tracked():
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True)
    assert out.returncode == 0 and out.stdout, "the tracked files could not be listed, so nothing was scanned"
    return [r for r in out.stdout.decode("utf-8", "replace").split("\0") if r]


def _find(text):
    return [(text.count("\n", 0, m.start()) + 1, kind) for kind, rx in SHAPES for m in rx.finditer(text)]


def test_no_tracked_file_holds_a_key_shaped_value():
    tracked = _tracked()
    assert len(tracked) > 1000, ("too few files were listed for this to be the repository", len(tracked))
    found, read = [], 0
    for rel in tracked:
        p = ROOT / rel
        try:
            if p.stat().st_size > 3_000_000:
                continue
            text = p.read_bytes().decode("utf-8", "ignore")
        except OSError:
            continue
        read += 1
        found += [(rel, line, kind) for line, kind in _find(text) if (rel, kind) not in ALLOWED]
    assert read > 1000, read
    assert found == [], ("a key-shaped value is committed (path, line, kind - the value is not shown): "
                         + "; ".join(f"{r}:{n} {k}" for r, n, k in sorted(set(found))[:20]))
    #  no settings file is tracked, in any folder
    assert [r for r in tracked if r == ".env" or r.endswith("/.env") or r.endswith(".env.local")] == []


def test_the_scan_itself_can_fail_and_the_three_archived_copies_stay_redacted():
    #  the check, driven: a value of each shape, BUILT here so that none is written in this file, is found
    made = {
        "an AI provider key": "sk-" + "a1B2" * 10,
        "a payment provider key": "sk_" + "live_" + "a1B2c3D4" * 3,
        "a webhook signing secret": "whsec_" + "a1B2c3D4" * 4,
        "a Google API key": "AIza" + "a1B2c3D" * 5,
        "a Google sign-in client secret": "GOCSPX-" + "a1B2c3D4" * 3,
        "a database address with a password": "mongodb+srv://" + "user" + ":" + "p4ssw0rdvalue" + "@cluster.invalid",
        "a source-host token": "ghp_" + "a1B2c3D4e5F6" * 3,
        "a cloud access key id": "AKIA" + "ABCDEFGH12345678",
        "a private key block": "-----BEGIN " + "PRIVATE KEY-----",
        "a service-account file": '{"type": ' + '"service_account"}',
    }
    assert set(made) == {k for k, _ in SHAPES}
    for kind, value in made.items():
        assert kind in [k for _, k in _find("line one\nNAME=" + value + "\n")], kind
    assert _find("NAME=" + MARK) == [] and _find("a sentence about keys and secrets, with no value") == []
    #  the redaction stands: each copy carries the marker where the values were, and no shape
    for rel in REDACTED:
        text = (ROOT / rel).read_bytes().decode("utf-8", "ignore")
        assert text.count(MARK) >= 20, (rel, text.count(MARK))
        assert _find(text) == [], rel
        for name in ("OPENAI_API_KEY", "MONGODB_URI", "GOOGLE_CLIENT_SECRET", "EMAIL_PASSWORD", "DEEPGRAM_API_KEY"):
            lines = [ln for ln in text.splitlines() if ln.strip().startswith(name + "=")]
            assert lines and all(MARK in ln or len(ln.split("=", 1)[1].strip()) < 40 for ln in lines), (rel, name)
