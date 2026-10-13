"""The Quran Foundation content API - the READING side only (W704, on the Owner's word of 2026-10-13).

What this is: a reference recitation's audio address and its word timings, fetched from the publisher AT THE
TIME OF USE, with credentials that stay on the server. What it is not: a store, a copy, or anything that
listens to a person - nothing here records, scores or corrects a recitation (A.9.1).

THE PUBLISHER'S CONDITIONS, as read at its developer terms (docs/SOURCES.json, row
`quran-foundation-developer-terms`), and how each is kept here:
  - nothing cached or stored longer than a week        -> NOTHING is stored: no file is written by this module
  - no prepackaged copy                                 -> every answer is fetched for the request that asked
  - credentials held on a server only                   -> the secret is read from the environment at the call,
                                                           is never returned, logged or put in an error
  - no model is trained on the content                  -> the answer goes to the caller and nowhere else
  - production use needs the publisher's approval       -> the environment defaults to pre-production

WHAT IS NOT YET ESTABLISHED: the two content paths below are taken from the publisher's reference pages and
have not been called from this machine with real credentials. If the publisher answers otherwise, the route
says what it answered; it never substitutes another source for it.
"""
from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import httpx

SOURCE_ROW = "quran-foundation-developer-terms"
_ENVIRONMENTS = {
    "prelive": {"token": "https://prelive-oauth2.quran.foundation/oauth2/token",
                "content": "https://apis-prelive.quran.foundation"},
    "production": {"token": "https://oauth2.quran.foundation/oauth2/token",
                   "content": "https://apis.quran.foundation"},
}
DEFAULT_ENVIRONMENT = "prelive"
_CHAPTER_AUDIO = "/content/api/v4/chapter_recitations/{reciter_id}/{chapter}"
_CHAPTER_RECITERS = "/content/api/v4/resources/chapter_reciters"
_EARLY_S = 120          # a token is replaced this long before the publisher's stated expiry
CREDIT = "Audio and word timings from the Quran Foundation (quran.foundation), fetched for this request and not stored."

#  the access token only, in this process's memory: never on disk, never in an answer
_token: Dict[str, Any] = {"value": None, "expires_at": 0.0, "environment": None}


class NotConfigured(Exception):
    """No credentials are set, so the publisher is not asked."""


class PublisherRefused(Exception):
    """The publisher answered with something other than the content. Carries its status, never a secret."""
    def __init__(self, what: str, status: Optional[int] = None):
        super().__init__(what)
        self.status = status


def environment() -> str:
    env = (os.getenv("QURAN_FOUNDATION_ENV") or DEFAULT_ENVIRONMENT).strip().lower()
    return env if env in _ENVIRONMENTS else DEFAULT_ENVIRONMENT


def _credentials() -> tuple:
    return ((os.getenv("QURAN_FOUNDATION_CLIENT_ID") or "").strip(),
            (os.getenv("QURAN_FOUNDATION_CLIENT_SECRET") or "").strip())


def configured() -> bool:
    cid, secret = _credentials()
    return bool(cid and secret)


def status() -> Dict[str, Any]:
    """What a person may know about this source. No credential, and no part of one, is in it."""
    env = environment()
    return {
        "source": "Quran Foundation content API",
        "configured": configured(),
        "configured_basis": ("both credentials are set in this server's environment" if configured() else
                             "one or both credentials are not set in this server's environment, so the "
                             "publisher is not asked and no recitation audio is served from it"),
        "environment": env,
        "environment_basis": ("pre-production: the publisher's test service. Production needs the publisher's "
                              "approval and the Owner's setting" if env == "prelive" else
                              "production: set by the Owner"),
        "stored": False,
        "stored_basis": "nothing fetched from this source is written to disk; each answer is fetched for its request",
        "conditions_row": SOURCE_ROW,
        "credit": CREDIT,
        "called_from_this_machine": bool(_token["value"]),
        "listens_to_a_person": False,
    }


async def _access_token(client: httpx.AsyncClient) -> str:
    env = environment()
    if _token["value"] and _token["environment"] == env and time.time() < _token["expires_at"]:
        return _token["value"]
    cid, secret = _credentials()
    if not (cid and secret):
        raise NotConfigured("the Quran Foundation credentials are not set in this server's environment")
    try:
        resp = await client.post(_ENVIRONMENTS[env]["token"], auth=(cid, secret),
                                 data={"grant_type": "client_credentials", "scope": "content"})
    except httpx.HTTPError as e:
        raise PublisherRefused(f"the publisher's sign-in service could not be reached ({type(e).__name__})") from None
    if resp.status_code != 200:
        raise PublisherRefused("the publisher's sign-in service did not issue a token", resp.status_code)
    body = resp.json()
    value = body.get("access_token")
    if not value:
        raise PublisherRefused("the publisher's sign-in service answered without a token", resp.status_code)
    _token.update(value=value, environment=env,
                  expires_at=time.time() + max(0, int(body.get("expires_in") or 0) - _EARLY_S))
    return value


async def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    env = environment()
    async with httpx.AsyncClient(timeout=15.0) as client:
        token = await _access_token(client)
        cid, _ = _credentials()
        try:
            resp = await client.get(_ENVIRONMENTS[env]["content"] + path, params=params or {},
                                    headers={"x-auth-token": token, "x-client-id": cid})
        except httpx.HTTPError as e:
            raise PublisherRefused(f"the publisher's content service could not be reached ({type(e).__name__})") from None
    if resp.status_code == 401:
        _token.update(value=None, expires_at=0.0)        # a refused token is not offered again
    if resp.status_code != 200:
        raise PublisherRefused("the publisher's content service did not return the content", resp.status_code)
    return resp.json()


async def chapter_audio(chapter: int, reciter_id: int) -> Dict[str, Any]:
    """One chapter's reference recitation: where its audio is, and each verse's and word's timing in it."""
    body = await _get(_CHAPTER_AUDIO.format(reciter_id=int(reciter_id), chapter=int(chapter)), {"segments": "true"})
    audio = body.get("audio_file") if isinstance(body, dict) else None
    if not isinstance(audio, dict) or not audio.get("audio_url"):
        raise PublisherRefused("the publisher answered without an audio file for this chapter and reciter", 200)
    verses = [{"verse_key": t.get("verse_key"), "from_ms": t.get("timestamp_from"), "to_ms": t.get("timestamp_to"),
               "words": [{"word": s[0], "from_ms": s[1], "to_ms": s[2]}
                         for s in (t.get("segments") or []) if isinstance(s, list) and len(s) >= 3]}
              for t in (audio.get("timestamps") or []) if isinstance(t, dict)]
    return {"chapter": int(chapter), "reciter_id": int(reciter_id), "audio_url": audio["audio_url"],
            "format": audio.get("format"), "verses": verses, "verses_timed": len(verses),
            "words_timed": sum(len(v["words"]) for v in verses)}


async def chapter_reciters() -> Dict[str, Any]:
    """The reciters the publisher offers whole-chapter audio for. Names are the publisher's own."""
    body = await _get(_CHAPTER_RECITERS)
    rows = body.get("reciters") if isinstance(body, dict) else None
    return {"reciters": [{"id": r.get("id"), "name": r.get("name")} for r in (rows or []) if isinstance(r, dict)]}
