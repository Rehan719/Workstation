import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Any, Iterator, List, Optional, Tuple

#  W1205 (FU-1845) - THE DOCUMENT-CONTROL LEDGER. Until W1205 the registry was one JSON file, dcms_registry.json,
#  rewritten whole on every commit under a bare except, with every version's content resident in memory; a store it
#  could not read was loaded as {} or its prefix and then written back over the history. The store is now an
#  append-only file, one JSON line per version, appended under the store's lock with flush and fsync. It is read
#  strictly: a line that is torn or cannot be read refuses every later commit, and the platform never rewrites,
#  truncates or replaces a line it wrote whole (an append that fails takes back only its own unfinished tail). The
#  registry before W1205 is carried in once, behind a first migration line naming its sha256 and how many versions it
#  held, and the old file is kept untouched beside the ledger. A marker beside the ledger records that it was
#  created, so a ledger that goes missing is refused, never started again empty or carried in again.
#  NOT DETECTED, as before this round: each line's seal is recomputed alone and nothing outside the file anchors it,
#  so a line rewritten together with its hash, or the newest lines removed, still reads as intact.
LEDGER_NAME = "dcms_ledger.jsonl"
OLD_REGISTRY_NAME = "dcms_registry.json"
MARKER_NAME = "dcms_ledger.created"
#  the fields of one version's line, in the order they are written
RECORD_KEYS = ("artifact_id", "version", "hash", "actor", "timestamp", "content", "content_stored")
_OLD_KEYS = {"version", "hash", "actor", "timestamp", "content", "content_stored"}
#  what the Owner does when the ledger cannot be read whole (P1.15: refuse and say so, never replace the store)
REPAIR = ("to repair it, the Owner stops the platform, keeps a copy of the file, and cuts it back to the end of its "
          "last complete line (or restores the damaged line from a copy); the platform never rewrites, truncates or "
          "replaces a line it wrote whole, and no version is appended until the ledger reads whole")
OLD_REPAIR = ("to repair it, the Owner restores the old file from a copy, or creates an empty dcms_ledger.jsonl beside "
              "it, which the platform then takes as the store (the old file is kept either way); the platform never "
              "rewrites or replaces the old file")
MISSING_REPAIR = ("to repair it, the Owner restores dcms_ledger.jsonl from a copy; the platform does not start it "
                  "again empty and does not carry the old registry in again, because that would drop every version "
                  "since")


class AppendNotUndone(OSError):
    """An append failed and its own unfinished tail could not be taken back, so the version may or may not be in the
    ledger: it was not confirmed durable. `offset` is where the version's line began."""

    def __init__(self, message: str, offset: int):
        super().__init__(message)
        self.offset = offset


class _Unsettled(Exception):
    """A read outside the store's lock met a last line still being written: it is read again under the lock."""


def _no_constant(name):
    raise ValueError(f"a non-finite number ({name})")


def _open_raw(path):
    """The one door every read of the ledger and the old registry goes through (a binary file object)."""
    return open(path, "rb")


def _fsync_dir(path) -> None:
    """Make a new directory entry durable (POSIX); best effort, and nothing to do on Windows."""
    if os.name == "nt":
        return
    try:
        fd = os.open(str(Path(path).parent), os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def _append_bytes(path, data: bytes) -> int:
    """Append DATA to the file at PATH, flushed and fsynced, and return the offset it was written at, in binary mode
    on every platform. On any failure the call's own unfinished tail is taken back (truncated to the offset and
    fsynced), never a line written whole before it, and the error propagates; if that undo fails too,
    AppendNotUndone says the version may be in the ledger. A version that was not written is never answered as kept."""
    fd = os.open(str(path), os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0), 0o644)
    try:
        offset = os.fstat(fd).st_size
        try:
            view = memoryview(data)
            while view:
                n = os.write(fd, view)
                view = view[n:]
            os.fsync(fd)
        except BaseException as exc:
            try:
                os.ftruncate(fd, offset)
                os.fsync(fd)
            except OSError as undo:
                raise AppendNotUndone(
                    f"the append failed ({exc.__class__.__name__}: {exc}) and its own unfinished line from byte "
                    f"{offset} could not be taken back ({undo.__class__.__name__}: {undo}), so the version may or "
                    f"may not be in the ledger: it was not confirmed durable", offset) from exc
            raise
        return offset
    finally:
        os.close(fd)


class DocumentControlManagementSystem:
    """
    VBS: DCMS.
    Cryptographic versioning and trace logic.

    §10×§13 (W327) — genuinely VERIFIABLE: every commit keeps the entry WITH the content it sealed
    (capped), verify_artifact re-hashes the stored content against the stored seal, and
    get_audit_integrity() is the RECOMPUTED fraction of entries whose seal still matches — a real
    measurement, never a constant.

    W1205 (FU-1845) — the store is the ledger dcms_ledger.jsonl, one line per version, APPENDED; no line
    written whole is ever rewritten. `registry` is a dict of artifact id to a list of version stubs
    (version, hash, actor, timestamp, content_stored, offset) and holds no content: verify_artifact and
    get_audit_integrity read the file a line at a time, by the same rules as the load, and recompute
    from it. The ledger is read strictly: when it cannot be read whole, `_store_incomplete` says why,
    the stubs hold only what was read before the problem, and commit_artifact raises StoreUnavailable
    rather than append to it.
    """
    _CONTENT_CAP = 16000   # serialised chars stored per entry (larger content: hash-only, declared)

    def __init__(self, config_path: str):
        self.logger = logging.getLogger("DCMS")
        self._store_problem: Optional[str] = None
        self._store_incomplete: Optional[str] = None
        self._unconfirmed: Optional[str] = None      # an append whose tail could not be taken back
        self._end = 0                  # the ledger's length in bytes as last read or appended
        self.migration: Optional[Dict[str, Any]] = None
        self.registry = self._load()   # id -> list of version stubs (no content)

    @property
    def refusal(self) -> Optional[str]:
        """Why a commit is refused now, or None."""
        return self._unconfirmed or self._store_incomplete

    def _store_path(self) -> str:
        from agentic_core.config import data_path
        return str(data_path(LEDGER_NAME))

    def _old_store_path(self) -> str:
        from agentic_core.config import data_path
        return str(data_path(OLD_REGISTRY_NAME))

    def _marker_path(self) -> str:
        from agentic_core.config import data_path
        return str(data_path(MARKER_NAME))

    def _refuse(self, problem: str, repair: str = REPAIR, name: str = LEDGER_NAME) -> None:
        self._store_problem = f"{problem}; {repair}"
        self._store_incomplete = f"{name} could not be read whole: {problem}; {repair}"
        self.logger.error("DCMS: %s", self._store_incomplete)

    #  ── reading: strict, a line at a time, by one set of rules ──
    def _open(self, path):
        """Open PATH for reading. A PermissionError (a sharing violation) is retried as read_json_strict retries it;
        one that lasts, or any other OSError, raises StoreUnavailable."""
        from agentic_core.config import StoreUnavailable
        for attempt in range(5):
            try:
                return _open_raw(path)
            except PermissionError as e:
                if attempt == 4:
                    raise StoreUnavailable(path, f"stayed locked by another process ({e.__class__.__name__})") from e
                time.sleep(0.05 * (attempt + 1))
            except OSError as e:
                raise StoreUnavailable(path, f"{e.__class__.__name__}: {str(e)[:80]}") from e

    @staticmethod
    def _parse(raw: bytes) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """One line of the ledger as a record, or why it is not one."""
        if not raw.endswith(b"\n"):
            return None, "torn: it does not end in a newline, so it was cut off while being written"
        try:
            rec = json.loads(raw.decode("utf-8"), parse_constant=_no_constant)
        except (UnicodeDecodeError, ValueError, RecursionError) as e:
            return None, f"not a JSON line ({e.__class__.__name__}: {str(e)[:80]})"
        if not isinstance(rec, dict):
            return None, "not a JSON object"
        if rec.get("kind") == "migration":
            return rec, None
        if any(k not in rec for k in RECORD_KEYS) or not isinstance(rec.get("artifact_id"), str) \
                or not isinstance(rec.get("version"), int) or not isinstance(rec.get("hash"), str):
            return None, "not a version record (a field is missing or of the wrong type)"
        if bool(rec.get("content_stored")) != isinstance(rec.get("content"), str):
            return None, "a version record whose content_stored flag does not match its content"
        return rec, None

    def _walk(self, locked: bool) -> Iterator[Tuple[int, int, Optional[Dict[str, Any]], Optional[str]]]:
        """Every line of the ledger, up to its length when the read began, as (offset, length, record or None,
        problem or None), streamed (memory is bounded by one line), by the rules every reader shares: a torn or
        unreadable line, a migration line that is not first, fewer carried lines than the migration line names, and
        a version out of order or repeated are each a problem. Outside the store's lock a last line without its
        newline may still be being written, so _Unsettled asks for the read again under the lock."""
        p = Path(self._store_path())
        if not p.exists():
            return
        with self._open(p) as f:
            size = os.fstat(f.fileno()).st_size
            off = 0
            have: Dict[str, int] = {}
            migration, carried, carrying = None, 0, False
            while off < size:
                raw = f.readline(size - off)
                if not raw:
                    break
                rec, problem = self._parse(raw)
                if problem and not raw.endswith(b"\n") and off + len(raw) >= size and not locked:
                    raise _Unsettled()
                if problem is None and rec.get("kind") == "migration":
                    if off != 0:
                        problem = "a migration line that is not the ledger's first line"
                    else:
                        migration, carrying = rec, True
                elif problem is None:
                    if carrying and not rec.get("migrated"):
                        carrying = False
                        if carried != int(migration.get("versions") or 0):
                            problem = (f"after the migration line, which carried {migration.get('versions')} "
                                       f"version(s), {carried} carried line(s) follow it")
                    elif not carrying and rec.get("migrated"):
                        problem = "a carried line that does not follow the migration line"
                    if problem is None and rec["version"] != have.get(rec["artifact_id"], 0) + 1:
                        problem = (f"version {rec['version']} of {rec['artifact_id']!r} follows version "
                                   f"{have.get(rec['artifact_id'], 0)}, so the versions are out of order or repeated")
                    if problem is None:
                        have[rec["artifact_id"]] = rec["version"]
                        carried += 1 if carrying else 0
                yield off, len(raw), rec, problem
                off += len(raw)
            if carrying and carried != int(migration.get("versions") or 0):
                yield off, 0, None, (f"the migration line carried {migration.get('versions')} version(s) and only "
                                     f"{carried} follow it")

    def _settled(self, read, locked: bool):
        """Run READ(locked) once; if it met a last line still being written outside the lock, run it again under the
        lock (or, if the lock cannot be had, strictly without it)."""
        if locked:
            return read(True)
        try:
            return read(False)
        except _Unsettled:
            from agentic_core.config import store_lock
            try:
                with store_lock(self._store_path()):
                    return read(True)
            except (TimeoutError, OSError):
                return read(True)

    def _load(self, _locked: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """The version stubs, replayed from the ledger, with `_store_incomplete` set when it could not be read whole.

        W577 (FU-298) answered an unreadable registry with {} or its prefix, and _persist then wrote that back over
        the history. W1205 (FU-1845): the read is strict. A torn or unreadable line, a version out of order or
        repeated, a ledger the OS would not hand over, or a ledger that was created and is now missing leaves the
        stubs read before it (so a reader still sees them, and is told) and refuses every commit until it reads
        whole. Nothing here ever writes the ledger, except the one migration of the registry before W1205, which
        creates it."""
        from agentic_core.config import StoreUnavailable
        self._store_problem = self._store_incomplete = None
        self.migration = None
        self._end = 0
        path = Path(self._store_path())
        try:
            if not path.exists():
                if Path(self._marker_path()).exists():
                    self._refuse(f"it is missing, and {MARKER_NAME} says it was created, so it was removed or lost",
                                 MISSING_REPAIR)
                    return {}
                if Path(self._old_store_path()).exists():
                    try:
                        self._migrate(path, _locked)
                    except OSError as e:     # not written (ENOSPC, the lock not had, ...): said, never a crash
                        self._refuse(f"the registry before W1205 could not be carried in ({e.__class__.__name__}: "
                                     f"{str(e)[:120]}), so {OLD_REGISTRY_NAME} stays the store, untouched, and no "
                                     "version is appended", OLD_REPAIR)
                        return {}

            def read(locked):
                stubs: Dict[str, List[Dict[str, Any]]] = {}
                self.migration, self._end = None, 0
                for off, n, rec, problem in self._walk(locked):
                    if problem is not None:
                        self._refuse((f"the line at byte {off} is {problem}" if n else problem)
                                     + f"; the {sum(len(v) for v in stubs.values())} version(s) before it were read "
                                     "and nothing after it was")
                        return stubs
                    if rec.get("kind") == "migration":
                        self.migration = rec
                    else:
                        stubs.setdefault(rec["artifact_id"], []).append({
                            "version": rec["version"], "hash": rec["hash"], "actor": rec.get("actor"),
                            "timestamp": rec.get("timestamp"), "content_stored": bool(rec.get("content_stored")),
                            "offset": off})
                    self._end = off + n     # the ledger's length as read, line by line
                return stubs
            return self._settled(read, _locked)
        except StoreUnavailable as e:
            if Path(e.path).name == OLD_REGISTRY_NAME:
                self._refuse(f"the registry before W1205 could not be read whole ({e.problem}), so it was not carried "
                             f"into {LEDGER_NAME} and stays the store, untouched, and no version is appended",
                             OLD_REPAIR, OLD_REGISTRY_NAME)
            else:
                self._refuse(f"it could not be read ({e.problem})")
        except OSError as e:     # never a crash at import: said, and every commit refused
            self._refuse(f"it could not be read ({e.__class__.__name__}: {str(e)[:120]})")
        return {}

    def _write_marker(self, source: str) -> None:
        """Record, durably and once, that the ledger was created; best effort (the ledger stands without it)."""
        marker = Path(self._marker_path())
        if marker.exists():
            return
        try:
            tmp = marker.with_name(f".{marker.name}.tmp")
            with open(tmp, "wb") as f:
                f.write((json.dumps({"ledger": LEDGER_NAME, "created_by": source,
                                     "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n").encode())
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, marker)
            _fsync_dir(marker)
        except OSError as e:
            self.logger.error("DCMS: %s could not be written (%s); a lost ledger would not be noticed", MARKER_NAME, e)

    def _migrate(self, path: Path, _locked: bool = False) -> None:
        """Carry the registry before W1205 into a new ledger, once: read dcms_registry.json strictly, write a first
        migration line naming its sha256 and its counts, then one line per version, marked migrated, into a
        temporary file that replaces nothing (the ledger does not exist yet). The old file is only read, never
        written or removed. If it cannot be read whole, or its versions are not 1..n in order, no ledger is made,
        the old file stays the store, and the load says so. _locked: the caller (a commit) holds the store's lock."""
        import contextlib
        from agentic_core.config import StoreUnavailable, store_lock
        old = Path(self._old_store_path())
        with (contextlib.nullcontext() if _locked else store_lock(path)):
            if path.exists():           # another process carried it in first
                return
            with self._open(old) as f:
                raw = f.read()
            try:
                data = json.loads(raw.decode("utf-8"), parse_constant=_no_constant) if raw else {}
            except (UnicodeDecodeError, ValueError, RecursionError) as e:
                raise StoreUnavailable(old, f"not valid JSON ({e.__class__.__name__}: {str(e)[:80]})") from e
            if not isinstance(data, dict) or not all(isinstance(v, list) and all(isinstance(e, dict) and
                                                                                isinstance(e.get("hash"), str)
                                                                                for e in v)
                                                     for v in data.values()):
                raise StoreUnavailable(old, "not a registry of version lists")
            for aid, entries in data.items():
                if [e.get("version", i + 1) for i, e in enumerate(entries)] != list(range(1, len(entries) + 1)):
                    raise StoreUnavailable(old, f"the versions of {aid!r} are not 1 to {len(entries)} in order")
            lines = [json.dumps({"kind": "migration", "from": OLD_REGISTRY_NAME,
                                 "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                                 "artifacts": len(data), "versions": sum(len(v) for v in data.values()),
                                 "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                 "basis": (f"the registry before W1205, carried in once; {OLD_REGISTRY_NAME} is "
                                           f"kept untouched beside this ledger")})]
            for aid, entries in data.items():
                for i, e in enumerate(entries):
                    rec = {"artifact_id": aid, "version": i + 1, "hash": e["hash"],
                           "actor": e.get("actor"), "timestamp": e.get("timestamp"),
                           "content": e.get("content") if isinstance(e.get("content"), str) else None,
                           "content_stored": bool(e.get("content_stored")) and isinstance(e.get("content"), str),
                           "migrated": True}
                    extra = {k: v for k, v in e.items() if k not in _OLD_KEYS}
                    if extra:
                        rec["old_extra"] = extra
                    lines.append(json.dumps(rec))
            tmp = path.with_name(f".{path.name}.migrating")
            try:
                with open(tmp, "wb") as f:
                    f.write(("\n".join(lines) + "\n").encode("utf-8"))
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp, path)
            except BaseException:
                try:
                    tmp.unlink()            # the platform's own temporary file, never the ledger or the old file
                except OSError:
                    pass
                raise
            _fsync_dir(path)
            self._write_marker(f"migration of {OLD_REGISTRY_NAME} (sha256 {hashlib.sha256(raw).hexdigest()})")
            self.logger.warning("DCMS: carried %s into %s (%s version(s)); the old file is kept",
                                OLD_REGISTRY_NAME, LEDGER_NAME, len(lines) - 1)

    #  ── writing: one appended line per version ──
    async def commit_artifact(self, artifact_id: str, content: Dict, actor: str) -> str:
        """Commit + version an artifact — the seal AND what it sealed are appended together, as one line.

        W1205 (FU-1845): raises StoreUnavailable when the ledger cannot be read whole (it is read again first, so a
        repaired ledger is taken up without a restart), and lets an OSError from the append propagate once the
        append's own unfinished tail is taken back. A version that was not written is never answered with a hash."""
        from agentic_core.config import StoreUnavailable, store_lock
        payload = json.dumps(content, sort_keys=True, default=str)
        h = hashlib.sha3_512(payload.encode()).hexdigest()
        path = self._store_path()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with store_lock(path):
            if self._unconfirmed:
                raise StoreUnavailable(path, f"{self._unconfirmed}; the Owner reads the ledger's last line, keeps or "
                                             "cuts it by hand, and restarts the platform")
            created = not Path(path).exists()
            size = 0 if created else Path(path).stat().st_size
            if self._store_incomplete or size != self._end or (created and Path(self._marker_path()).exists()):
                #  refused before, another writer appended since this instance read it, or the ledger went missing:
                #  read it again, strictly
                self.registry = self._load(_locked=True)
            if self._store_incomplete:
                raise StoreUnavailable(path, self._store_problem or self._store_incomplete)
            created = not Path(path).exists()
            stored = len(payload) <= self._CONTENT_CAP
            rec = {"artifact_id": artifact_id,
                   "version": len(self.registry.get(artifact_id, [])) + 1,
                   "hash": h,
                   "actor": actor,
                   "timestamp": time.time_ns(),
                   # W327 — the sealed content itself (capped): the verify path's raw material
                   "content": payload if stored else None,
                   "content_stored": stored}
            line = (json.dumps(rec) + "\n").encode("utf-8")
            try:
                offset = _append_bytes(path, line)
            except AppendNotUndone as e:
                self._unconfirmed = str(e)
                self.logger.error("DCMS: %s", e)
                raise
            self._end = offset + len(line)
            if created:
                _fsync_dir(path)
            self._write_marker("the first commit")
            self.registry.setdefault(artifact_id, []).append({
                "version": rec["version"], "hash": h, "actor": actor, "timestamp": rec["timestamp"],
                "content_stored": stored, "offset": offset})
        return h

    #  ── verifying: recomputed from the file, every time, by the load's rules ──
    def verify_artifact(self, artifact_id: str) -> Dict[str, Any]:
        """§13 (W327) — recompute every stored version's seal. A mutated entry is caught + named.
        W1205: read from the ledger's lines, by the load's rules: a ledger with a line that cannot be read, or a
        version out of order or repeated, verifies nothing, because the artifact that line belongs to cannot be
        known."""
        def read(locked):
            results = []
            for off, _n, rec, problem in self._walk(locked):
                if problem is not None:
                    return None, f"the ledger cannot be read whole: at byte {off}, {problem}"
                if rec.get("artifact_id") != artifact_id:
                    continue
                if rec.get("content_stored"):
                    ok = hashlib.sha3_512(rec["content"].encode()).hexdigest() == rec.get("hash")
                    results.append({"version": rec.get("version"), "verified": ok, "basis": "recomputed"})
                else:
                    results.append({"version": rec.get("version"), "verified": None,
                                    "basis": "hash_only (content exceeded storage cap — honest)"})
            return results, None
        try:
            results, why = self._settled(read, False)
        except Exception as e:      # noqa: BLE001 - an unreadable ledger verifies nothing, and says why
            results, why = None, f"the ledger could not be read ({e.__class__.__name__}: {str(e)[:120]})"
        if results is None:
            return {"artifact_id": artifact_id, "valid": False, "reason": why}
        if not results:
            return {"artifact_id": artifact_id, "valid": False, "reason": "unknown artifact"}
        recomputed = [r for r in results if r["basis"] == "recomputed"]
        return {"artifact_id": artifact_id,
                "valid": bool(recomputed) and all(r["verified"] for r in recomputed),
                "unverifiable": len(results) - len(recomputed),
                "versions": results}

    def get_audit_integrity(self) -> float:
        """The RECOMPUTED fraction of verifiable entries whose seal still matches (0.0 with no
        verifiable history — never a fabricated constant). W1205: read from the ledger a line at a time, by the
        load's rules; a line that cannot be read, or a version out of order or repeated, counts as a version whose
        seal cannot be shown."""
        def read(locked):
            total = ok = 0
            for _off, _n, rec, problem in self._walk(locked):
                if problem is not None:
                    total += 1
                    continue
                if rec.get("kind") == "migration":
                    continue
                if rec.get("content_stored"):
                    total += 1
                    if hashlib.sha3_512(rec["content"].encode()).hexdigest() == rec.get("hash"):
                        ok += 1
            return total, ok
        try:
            total, ok = self._settled(read, False)
        except Exception as e:      # noqa: BLE001
            self.logger.error("DCMS: the ledger could not be read for its integrity (%s)", e)
            return 0.0
        return round(ok / total, 4) if total else 0.0
