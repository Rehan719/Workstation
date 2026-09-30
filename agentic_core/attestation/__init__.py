"""Attestations that are attestations — P3.15.

WHAT THIS REPLACES. The clearance chain wrote five literal strings into the UEG as signatures
(`SIG_MUSHAWARA_v1` and its four siblings), and five modules named Dilithium and Kyber over operations that
never happened. `security/pqc_hardening.py` had already been retired for the sharpest version of this: it
keyed a "Dilithium-5 signature" with a literal in the source and padded the output with 4000 zeros so it
would resemble a post-quantum signature to anything that inspected it.

WHAT THIS DOES. Signs a CANONICAL payload with HMAC-SHA3-512 under a key read from the environment, and
records the algorithm, the key SOURCE and a key fingerprint beside the signature so a verifier can say what
it checked. The canonical form is fixed and stated, because a signature over an unstated serialisation cannot
be recomputed by anyone else.

WHAT IT REFUSES TO DO, and this is the whole design. With no key configured it does NOT sign. It returns a
refusal naming the missing key. A signature keyed with a constant in the source verifies against itself and
proves nothing to anybody — it is a decoration shaped like evidence, which is the defect this module exists
to end. So an unconfigured platform gets `signed: False` with a reason, never a placeholder.

AND IT IS NOT POST-QUANTUM. HMAC-SHA3-512 is a keyed MAC over a symmetric secret. It proves that the holder
of the key produced the payload; it is not a public-key signature, and no part of it is post-quantum. The
words Dilithium, Kyber and post-quantum do not appear here as descriptions of what this computes, and a guard
forbids them. If this platform ever gains a post-quantum signature, the word becomes available then.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any, Dict

#  The environment variable that holds the secret. Named once, reported in every result, and never defaulted
#  to a value: a default key is the defect, not the convenience.
KEY_ENV = "WORKSTATION_ATTESTATION_KEY"

ALGORITHM = "HMAC-SHA3-512"

#  Stated, because a signature over an unstated serialisation is not reproducible. Sorted keys and compact
#  separators mean two equal payloads always canonicalise identically, whatever order they were built in.
CANONICAL_FORM = "json.dumps(payload, sort_keys=True, separators=(',', ':'), default=str), UTF-8 encoded"

NOT_SIGNED_BASIS = (
    f"NOT SIGNED: no attestation key is configured ({KEY_ENV} is unset or empty), so nothing was signed. "
    "This is a refusal rather than a fallback: a signature keyed with a constant in the source verifies "
    "against itself and proves nothing to anyone, which is what the retired pqc_hardening module did. No "
    "placeholder is written in its place"
)

WHAT_THIS_IS_NOT = (
    "a keyed MAC over a symmetric secret, not a public-key signature and not post-quantum. It shows that "
    "the holder of the configured key produced this payload; it does not identify a signer to a third party"
)


def canonical_bytes(payload: Any) -> bytes:
    """The exact bytes that get signed. Separate and public so a verifier can reproduce them."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _key() -> bytes:
    return (os.environ.get(KEY_ENV) or "").encode("utf-8")


def key_fingerprint(key: bytes) -> str:
    """A fingerprint of the KEY, so two results can be compared without the key appearing anywhere."""
    return hashlib.sha3_256(key).hexdigest()[:16]


def attest(payload: Any) -> Dict[str, Any]:
    """Sign `payload`, or refuse and say why. Never returns a placeholder signature."""
    key = _key()
    body = canonical_bytes(payload)
    digest = hashlib.sha3_512(body).hexdigest()

    if not key:
        return {
            "signed": False,
            "basis": NOT_SIGNED_BASIS,
            "algorithm": None,
            "key_source": f"env:{KEY_ENV} (unset)",
            # the digest is still useful and is NOT a signature: it proves nothing about who produced the
            # payload, only that these bytes hash to this value, and it is named accordingly
            "payload_digest": digest,
            "payload_digest_algorithm": "SHA3-512",
            "canonical_form": CANONICAL_FORM,
            "what_this_is_not": WHAT_THIS_IS_NOT,
        }

    return {
        "signed": True,
        "algorithm": ALGORITHM,
        "key_source": f"env:{KEY_ENV}",
        "key_fingerprint": key_fingerprint(key),
        "signature": hmac.new(key, body, hashlib.sha3_512).hexdigest(),
        "payload_digest": digest,
        "payload_digest_algorithm": "SHA3-512",
        "canonical_form": CANONICAL_FORM,
        "what_this_is_not": WHAT_THIS_IS_NOT,
    }


def verify(payload: Any, attestation: Dict[str, Any]) -> Dict[str, Any]:
    """Recompute the signature over `payload` and compare it, in constant time.

    Returns a three-state verdict, because "could not check" is not "failed": an attestation that was never
    signed, or one produced under a key this process does not hold, is UNVERIFIABLE rather than invalid, and
    reporting either as a failure would make a missing key look like tampering.
    """
    if not isinstance(attestation, dict):
        return {"verified": None, "basis": f"no attestation record to check (got {type(attestation).__name__})"}

    body = canonical_bytes(payload)
    digest = hashlib.sha3_512(body).hexdigest()

    if not attestation.get("signed"):
        return {"verified": None,
                "basis": ("this payload was never signed, so there is nothing to verify. "
                          + str(attestation.get("basis") or "")),
                "payload_digest_matches": digest == attestation.get("payload_digest")}

    key = _key()
    if not key:
        return {"verified": None,
                "basis": (f"the attestation was signed, but this process holds no key ({KEY_ENV} is unset), "
                          "so the signature cannot be recomputed. Unverifiable is not invalid"),
                "payload_digest_matches": digest == attestation.get("payload_digest")}

    if attestation.get("algorithm") != ALGORITHM:
        return {"verified": None,
                "basis": (f"the attestation names algorithm {attestation.get('algorithm')!r}, and this "
                          f"verifier only recomputes {ALGORITHM}")}

    fp = attestation.get("key_fingerprint")
    if fp and fp != key_fingerprint(key):
        return {"verified": None,
                "basis": ("the attestation was produced under a different key (fingerprints differ), so "
                          "this process cannot recompute its signature. Unverifiable is not invalid"),
                "payload_digest_matches": digest == attestation.get("payload_digest")}

    expected = hmac.new(key, body, hashlib.sha3_512).hexdigest()
    ok = hmac.compare_digest(expected, str(attestation.get("signature") or ""))
    return {
        "verified": bool(ok),
        "algorithm": ALGORITHM,
        "payload_digest_matches": digest == attestation.get("payload_digest"),
        "basis": ("the signature recomputed over the canonical payload matches"
                  if ok else
                  "THE SIGNATURE DOES NOT MATCH: the payload, the signature or the key differs from what "
                  "was attested. Either the payload was altered after signing, or it was not this payload "
                  "that was signed"),
    }
