"""Remove an account from the users store on the machine that holds it (W1198, P4.1).

An account the Owner made and no longer wants is removed with this command, over SSH on the machine, inside the
platform's container, never by editing users.json by hand:

    sudo docker exec -it workstation python -m agentic_core.auth.remove_account NAME

It takes one name, shows the account's role, when it was made and how many API keys it holds, and asks for the name
again; a mismatch is refused, and so are no name, more than one and a name starting with '-' or blank (unless it
comes after --), before anything is read. The admin account is never removed. Neither is an account the store does
not hold, and a store that is not there or cannot be read whole is refused and left byte for byte: the store is read
strictly BEFORE the command imports agentic_core.auth.core, because importing it makes the first account from a
tolerant read, and would replace a store it could not read with one holding only the admin. A store that holds no
admin account is not the platform's and is refused, and so is a store another user owns: written by the command's
user, it would become one the platform could no longer read. Under the store's own lock the store is read whole
again, the account that was shown is taken out with the API keys it holds, and core._save_users writes the store, so
an account another writer added meanwhile is kept; if a different account holds the name by then, nothing is
removed. A lock another writer keeps past the lock's wait, and a store that cannot be written, are refused in a
sentence. Nothing else is written: no event, and no file of the command's own. The person's records in the
platform's other stores are not touched.

Those records stay under the account's name, so a removed name is given to no other person: the command says so when
it is done. A sign-in token carries the account's id (W1198b), so a token issued before the removal is refused by an
account given the name later.
"""
from __future__ import annotations

import os
import pathlib
import sys

ADMIN = "admin"
RULE = ("Give this name to no other person: the person's records in the platform's other stores are still kept under "
        "that name, so an account given it would be shown them.")


class _Said(str):
    """A reason that already says nothing was changed, with what to do after it: _refuse prints it as it is."""


def _refuse(why: str) -> int:
    said = why if isinstance(why, _Said) else f"{why}, so nothing was changed"
    print(f"refused: {said}", file=sys.stderr)
    return 1


def _busy(exc) -> str:
    return f"the users store stayed locked by another writer ({exc.detail})"


def _owner(store):
    """The uid that owns the store, or None when it cannot be looked at (stat needs no read permission)."""
    try:
        return pathlib.Path(store).stat().st_uid
    except OSError:
        return None


def _keys(acct: dict) -> str:
    keys = acct.get("api_keys")
    n = len(keys) if isinstance(keys, list) else 0
    return "no API key" if n == 0 else ("1 API key" if n == 1 else f"{n} API keys")


def _removable(store, username: str):
    """The store read whole and the account in it, or None and why not: the admin is never removed, a store that
    cannot be read is never taken as empty, one that is not there is never taken as new, and one another user owns,
    or that holds no admin account, is not written."""
    if username == ADMIN:
        return None, None, "the admin account is never removed: it is the account the Owner signs in with"
    from agentic_core.config import StoreUnavailable, read_json_strict
    try:
        users = read_json_strict(store, None, dict)
    except StoreUnavailable as exc:
        if os.name == "posix" and isinstance(exc.__cause__, PermissionError):
            owner = _owner(store)
            if owner is None:                       # the store could not even be looked at: the plain words
                return None, None, _Said("the command's user may not read the users store (permission denied), so "
                                         "nothing was changed: run it as the platform's user, as docker exec does by "
                                         "default")
            return None, None, _Said(f"the users store could not be read whole: it belongs to uid {owner} and the "
                                     f"command runs as uid {os.geteuid()}, which may not read it (permission denied), "
                                     "so nothing was changed: run it as the platform's user, as docker exec does by "
                                     "default; if it ran so, the store is not the platform's own: restore the data "
                                     "disk (step 9)")
        return None, None, f"the users store could not be read whole ({exc.problem})"
    if users is None:
        return None, None, "there is no users store on the data disk"
    owner = _owner(store) if os.name == "posix" else None
    if owner is not None and owner != os.geteuid():
        return None, None, _Said(f"the users store belongs to uid {owner}, not to the command's uid {os.geteuid()}, so "
                                 "nothing was changed: run it as the platform's user, as docker exec does by default; "
                                 "if it ran so, the store is not the platform's own: restore the data disk (step 9)")
    if not isinstance(users.get(ADMIN), dict):
        return None, None, _Said("the users store holds no admin account, so it is not the platform's, and nothing was "
                                 "changed: restore the data disk (step 9)")
    if username in users and not isinstance(users[username], dict):
        return None, None, f"the users store's entry for {username!r} is not an account"
    if username not in users:
        return None, None, f"the users store holds no account named {username!r}"
    return users, users[username], None


def _another(shown: dict, now: dict):
    """Why the account the name holds now is not the one that was shown, or None. It is compared by its id, or by when
    it was made when it has no id. A key made meanwhile changes nothing: it goes with the account."""
    key = "user_id" if shown.get("user_id") else "created_at"
    if now.get(key) == shown.get(key):
        return None
    said = "id" if key == "user_id" else "made"
    return _Said(f"a different account now holds the name ({said} {now.get(key, '-')}, not {shown.get(key, '-')}), so "
                 "nothing was changed: run the command again")


def remove(username: str, shown=None):
    """Take one account out of the users store, never the admin. Under the store's own lock the store is read whole
    again, the account is removed with the API keys it holds, and core._save_users writes the store, so an account
    another writer added meanwhile is kept. Given the account a caller showed, a different account holding the name
    by then is refused. Returns (the removed account, None), or (None, why) with nothing written. Called first in a
    process, it reads the store strictly before it imports agentic_core.auth.core, as main() does."""
    from fastapi import HTTPException
    if "agentic_core.auth.core" not in sys.modules:
        from agentic_core.config import data_path
        why = _removable(data_path("users.json"), username)[2]
        if why:
            return None, why
        try:
            from agentic_core.auth import core    # noqa: F401 - the import takes the store's lock
        except HTTPException as exc:
            return None, _busy(exc)
    from agentic_core.auth import core
    try:
        with core._users_mutation():
            users, acct, why = _removable(core._USER_STORE, username)    # again, whole, under the store's lock
            if why:
                return None, why
            if shown is not None:
                why = _another(shown, acct)
                if why:
                    return None, why
            del users[username]
            core._save_users(users)
    except HTTPException as exc:
        return None, _busy(exc)
    except OSError as exc:
        return None, f"the users store could not be written ({exc.__class__.__name__}: {exc}); it is as it was"
    return acct, None


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    after_dashes = args[:1] == ["--"]
    named = args[1:] if after_dashes else args
    if len(named) != 1 or (not after_dashes and (not named[0].strip() or named[0].startswith("-"))):
        print("usage: python -m agentic_core.auth.remove_account [--] USERNAME (one account, never admin; its name is "
              "asked for again before anything is removed; a name that starts with '-' or is blank goes after --)",
              file=sys.stderr)
        return 2
    username = named[0]
    #  the store, read strictly, before core is imported: its import would make the first account from a tolerant
    #  read, and replace a store it could not read
    from agentic_core.config import data_path
    store = data_path("users.json")
    _users, acct, why = _removable(store, username)
    if why:
        return _refuse(why)
    from fastapi import HTTPException
    try:
        from agentic_core.auth import core          # its import takes the store's lock to make the first account
    except HTTPException as exc:
        return _refuse(_busy(exc))
    if pathlib.Path(core._USER_STORE).resolve() != pathlib.Path(store).resolve():
        return _refuse("the platform's users store is not the one that was read")
    try:
        typed = input(f"{username}: role {acct.get('role', '-')}, made {acct.get('created_at', '-')}, {_keys(acct)}. "
                      "Type its name again to remove it: ")
    except (EOFError, KeyboardInterrupt):
        return _refuse("the name was not typed again")
    if typed != username:
        return _refuse("the name typed again is not the account's")
    removed, why = remove(username, shown=acct)
    if why:
        return _refuse(why)
    print(f"Removed {username} (role {removed.get('role', '-')}) from the users store on the data disk, with "
          f"{_keys(removed)}. Its sign-in tokens and API keys are refused from their next request. The person's "
          f"records in the platform's other stores are not touched. {RULE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
