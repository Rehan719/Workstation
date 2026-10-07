"""Drive BLINDS against a guard: mutate the source, expect the guard to go RED, restore the bytes exactly.

    python scripts/round_tools/blinds.py <blinds_file.py> -k <pytest -k expression>

<blinds_file.py> defines BLINDS = [(name, relative_path, old, new), ...]. Each `old` must occur exactly once in
the file AS STORED — in a CRLF file write the anchor with "\\r\\n" (unlike patch.py, this matches raw text,
because a blind must reproduce the exact bytes it restores). For each blind: the file is mutated, the -k
selection runs on an isolated data root, and the file is restored and its SHA-256 asserted.

Verdicts: BLIND(red) — the guard caught the mutation (good); VACUOUS — the guard passed with the fix
broken, so it does not test the fix (strengthen the guard); BAD BLIND — the anchor did not match once.
Exit code is the count of VACUOUS + BAD. Read the exit code from this script, never through a pipe.
"""
import hashlib
import os
import pathlib
import runpy
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main(argv):
    if len(argv) < 4 or argv[2] != "-k":
        sys.exit(__doc__)
    blinds = runpy.run_path(argv[1])["BLINDS"]
    sel = argv[3]
    bad = 0
    for name, rel, old, new in blinds:
        p = ROOT / rel
        raw = p.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8")
        n = text.count(old)
        if n != 1:
            print(f"BAD BLIND  {name}: anchor matched {n} times")
            bad += 1
            continue
        data = tempfile.mkdtemp(prefix="blind_")
        env = dict(os.environ, DATA_DIR=data, WORKSTATION_DATA_DIR=data, WORKSTATION_UEG_PATH=os.path.join(data, "ueg.json"),
                   PROJECTS_DIR=os.path.join(data, "projects"), AI_DISABLE_LOCAL="1")
        try:
            p.write_bytes(text.replace(old, new).encode("utf-8"))
            r = subprocess.run([sys.executable, "-m", "pytest", "integration_tests/test_mvp_spine.py", "-q", "--no-header",
                                "-p", "no:warnings", "-k", sel], cwd=ROOT, env=env, capture_output=True, text=True)
        finally:
            p.write_bytes(raw)
            assert hashlib.sha256(p.read_bytes()).hexdigest() == sha, f"RESTORE FAILED for {rel}"
        if r.returncode == 5:
            sys.exit(f"ABORT: no tests collected for -k {sel!r} (blind {name})")
        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]
        print(("BLIND(red)" if r.returncode != 0 else "VACUOUS   ") + f"  {name}  ->  {tail}")
        bad += r.returncode == 0
    print("bad:", bad)
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv))
