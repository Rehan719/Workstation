"""Set an account's sign-in password on the machine that holds the users store (W1191, P4.5).

The release machine's first account, admin, is made with a random password no one is told (core.py,
_create_default_admin). The Owner sets its password once, over SSH on the machine, inside the platform's
container:

    sudo docker exec -it workstation python -m agentic_core.auth.set_password admin

The password is read twice without being shown (getpass), and refused when the two differ or it is shorter than
MIN_LENGTH characters; a password given on the command line is refused too, before anything is read. Only its hash
is stored, in the users store on the data disk, under the store's own lock, and the account is marked as set by the
Owner, so the login no longer takes ADMIN_PASSWORD for it. The password is never printed, logged, written to a file
of its own or put in an environment variable. An account the store does not hold is refused (accounts are made by
the platform, not here), and so is a store that is not there or cannot be read whole: the store is read strictly
BEFORE agentic_core.auth.core is imported, because importing it makes the first account from a tolerant read, and
would replace a store it could not read with one holding only the admin. Nothing is ever written over a store that
was not read whole.
"""
from __future__ import annotations

import getpass
import pathlib
import sys
import time

MIN_LENGTH = 12
SET_BY_OWNER = "owner-set"


def _refuse(why: str) -> int:
    print(f"refused: {why}, so nothing was changed", file=sys.stderr)
    return 1


def _account(store, username: str):
    """The store read whole and the account in it, or None and why not: a store that cannot be read is never
    taken as empty, and one that is not there is never taken as new."""
    from agentic_core.config import StoreUnavailable, read_json_strict
    try:
        users = read_json_strict(store, None, dict)
    except StoreUnavailable as exc:
        return None, None, f"the users store could not be read whole ({exc.problem})"
    if users is None:
        return None, None, "there is no users store on the data disk: the platform makes it at its first boot"
    if not isinstance(users.get(username), dict):
        return None, None, f"the users store holds no account named {username!r}"
    return users, users[username], None


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1 or not args[0].strip() or args[0].startswith("-"):
        print("usage: python -m agentic_core.auth.set_password USERNAME (the password is asked for, twice, and "
              "never taken from the command line)", file=sys.stderr)
        return 2
    username = args[0]
    #  the store, read strictly, before core is imported: its import would make the first account from a tolerant
    #  read, and replace a store it could not read
    from agentic_core.config import data_path
    store = data_path("users.json")
    _users, _acct, why = _account(store, username)
    if why:
        return _refuse(why)
    from fastapi import HTTPException
    from agentic_core.auth import core
    if pathlib.Path(core._USER_STORE).resolve() != pathlib.Path(store).resolve():
        return _refuse("the platform's users store is not the one that was read")
    if not core._AUTH_DEPS_OK:
        return _refuse(f"the password hasher is not installed ({core._AUTH_DEPS_ERR})")
    first = getpass.getpass(f"New password for {username}: ")
    if len(first) < MIN_LENGTH:
        return _refuse(f"the password is shorter than {MIN_LENGTH} characters")
    second = getpass.getpass("The same password again: ")
    if second != first:
        return _refuse("the two passwords differ")
    hashed = core._pwd_ctx.hash(first)
    try:
        with core._users_mutation():
            users, acct, why = _account(core._USER_STORE, username)    # again, whole, under the store's lock
            if why:
                return _refuse(why)
            acct["hashed_password"] = hashed
            acct["password_source"] = SET_BY_OWNER
            acct["password_set_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            core._save_users(users)
    except HTTPException as exc:
        return _refuse(f"the users store is busy ({exc.detail})")
    print(f"The password for {username} is set. Only its hash is stored, in the users store on the data disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
