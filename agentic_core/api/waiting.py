"""P5.18 clause 3 (W1085, FU-1267) - THE ONE LIST OF WHAT WAITS ON A PERSON.

What falls due on a person's agreement records is shown on one list, with what else waits on that person. It reads,
today, the obligations on the person's agreement records: each one falling due within the window or past its date, and
each one no person has confirmed. It says what it does not read yet, so an empty list is never taken for nothing
waiting anywhere. A date on it is a person's entry from the text; none is computed here and none is taken from a model.
Kept only for a signed-in person, as the agreement records are."""
from fastapi import APIRouter, Depends, HTTPException

from agentic_core.api.agreements import DATE_BASIS, falling_due
from agentic_core.auth.core import auth_enabled, get_current_user

router = APIRouter(prefix="/api/v1/waiting", tags=["waiting"])

READS = ["the obligations on your agreement records: each one falling due within the window or past its date, and "
         "each one no person has confirmed"]
NOT_READ_YET = ["an asset record's evidence as it nears its lapse", "a project's decision waiting on you",
                "a change waiting on your decision"]
NOT_KEPT = "Nothing is kept before sign-in, so nothing here waits on anyone yet."
BASIS = ("One list of what waits on you, from the records it reads; what it does not read yet is named, so an empty "
         "list says only that nothing it reads is waiting.")


@router.get("")
async def what_waits(within_days: int = 30, user: dict | None = Depends(get_current_user)):
    """What waits on this person, from the records the list reads, soonest first; and what it does not read yet."""
    if not 0 <= within_days <= 365:
        raise HTTPException(status_code=400, detail=(
            f"The window is a number of days from 0 to 365; {within_days} is not one, so nothing was read."))
    out = {"reads": READS, "not_read_yet": NOT_READ_YET, "basis": BASIS, "date_basis": DATE_BASIS}
    if not auth_enabled():
        return {**out, "items": [], "kept": False, "said": NOT_KEPT}
    got = falling_due(user, within_days)
    return {**out, "items": got["items"], "kept": True, "within_days": within_days,
            **({} if got["items"] else {"said": "Nothing that this list reads is waiting on you."})}
