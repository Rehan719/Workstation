"""Attestation — the route that RE-COMPUTES a signature rather than reporting a stored verdict. P3.15.

The item's bar is *a tampered payload fails verification; no placeholder signature is written*. A route that
returned a stored `verified: true` would satisfy neither: it would be repeating a claim rather than checking
one. Every answer here is recomputed from the payload the caller supplies.

WHY THE VERDICT IS THREE-STATE. `verified: null` means COULD NOT CHECK — the payload was never signed, or it
was signed under a key this process does not hold. Reporting that as `false` would make a missing key
indistinguishable from tampering, and an operator would chase the wrong fault. Only a recomputed signature
that genuinely differs returns `false`.

NOT POST-QUANTUM, stated on the route itself. This is HMAC-SHA3-512 over a symmetric secret: it shows the
holder of the configured key produced the payload. It does not identify a signer to a third party, and no
part of it is post-quantum. Five modules in this repository once named Dilithium and Kyber over operations
that never happened, and the retired `pqc_hardening` module keyed its "Dilithium-5 signature" with a literal
in the source and padded it with 4000 zeros so it would look the part.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core import attestation as _att

router = APIRouter(prefix="/api/v1/attestation", tags=["attestation"])


class AttestRequest(BaseModel):
    payload: Any


class VerifyRequest(BaseModel):
    payload: Any
    attestation: Dict[str, Any]


@router.get("/status")
async def attestation_status():
    """Whether this process can sign at all, and what it would sign with. No secret is returned."""
    probe = _att.attest({"probe": "status"})
    return {
        "can_sign": bool(probe.get("signed")),
        "algorithm": _att.ALGORITHM,
        "key_source": f"env:{_att.KEY_ENV}",
        "key_configured": bool(probe.get("signed")),
        "key_fingerprint": probe.get("key_fingerprint"),
        "canonical_form": _att.CANONICAL_FORM,
        "basis": (probe.get("basis") if not probe.get("signed") else
                  "an attestation key is configured, so gate verdicts are signed"),
        "what_this_is_not": _att.WHAT_THIS_IS_NOT,
        # said on the surface, not only in the module, because this is where a reader arrives
        "post_quantum": False,
        "post_quantum_basis": ("nothing here performs a post-quantum operation. The word is used on this "
                               "platform only where the operation is post-quantum, and it is not here"),
    }


@router.post("/sign")
async def sign_payload(req: AttestRequest):
    """Attest a payload, or refuse and say which key is missing. Never returns a placeholder."""
    return {"attestation": _att.attest(req.payload)}


@router.post("/verify")
async def verify_payload(req: VerifyRequest):
    """RECOMPUTE the signature over the supplied payload and compare it in constant time.

    Nothing stored is trusted: the signature is recomputed from `payload` as given, so altering one byte of
    it changes the verdict. That is the whole point of the route.
    """
    result = _att.verify(req.payload, req.attestation)
    return {
        "verified": result.get("verified"),
        "basis": result.get("basis"),
        "payload_digest_matches": result.get("payload_digest_matches"),
        "algorithm": result.get("algorithm"),
        "verdict_is_three_state": ("null means COULD NOT CHECK - unsigned, or signed under a key this "
                                   "process does not hold. Only a recomputed signature that differs "
                                   "returns false, so a missing key is never reported as tampering"),
        "recomputed": True,
    }
