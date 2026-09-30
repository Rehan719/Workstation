"""Content integrity digests. NOT post-quantum cryptography, and no longer shaped to look like it.

W506 (P2.4/FU-076, and P3.15's first half) — WHAT THIS MODULE USED TO DO:

    def sign_dilithium5(message, private_key="PQC_SECRET"):
        \"\"\"High-fidelity simulation of Dilithium-5 signing.\"\"\"
        ...
        signature_hash = hashlib.sha3_512(payload + private_key.encode()).hexdigest()
        padding = "0" * 4000            # "Dilithium-5 signatures are large (~4.5KB)"
        full_sig = f"{signature_hash}.{nonce}.{padding}"

Three separate problems, and the third is the one that made it more than a stub:

  1. it is a SHA3-512 digest, not a lattice signature;
  2. the default key was the LITERAL "PQC_SECRET", present in this file, so anyone holding the source can
     recompute any "signature" — it proved nothing about origin;
  3. (retired) it PADDED WITH 4000 ZEROS to match a Dilithium-5 signature's length — this module performs no
     such operation now. That padding had no function except
     to make the output resemble a post-quantum signature to anything that inspects it.

Two callers published the result as `pqc_signature` — `governance/gaas/gaas.py` on a partner certification and
`reactor/religion/qep_flagship.py` on a learner's course certificate, which is written to an on-disk store and
returned with a `verify_url`. A learner's credential carrying a field named for cryptography the platform does
not perform is the clearest form of the defect this programme exists to remove.

WHAT IT DOES NOW: a keyed SHA3-512 digest over a canonical payload, named as that, with its own limits stated in
the value it returns. The digest is real and useful — it detects alteration of the payload — and it is NOT proof
of origin, because the key lives in the process that computes it. Anything wanting proof of origin needs P3.15's
signing service with a named algorithm and a stated key source; until that exists, nothing here claims it.

The words Dilithium, Kyber and post-quantum do not appear as descriptions of what this computes. A guard forbids
their return.
"""
import hashlib
import json
import os
import time
from typing import Any, Dict, Optional

# W506 — the key source is NAMED rather than hard-coded. When the environment supplies nothing, the digest is
# UNKEYED and says so: a built-in constant masquerading as a secret is worse than no key, because it invites a
# reader to believe the digest authenticates something.
_KEY_ENV = "WORKSTATION_DIGEST_KEY"
ALGORITHM = "SHA3-512"


def _key() -> tuple[bytes, str]:
    """The digest key and a plain statement of where it came from."""
    k = os.getenv(_KEY_ENV)
    if k:
        return k.encode(), f"a key supplied by the environment ({_KEY_ENV})"
    return b"", ("UNKEYED - no key is configured, so this digest detects alteration and says nothing "
                 "whatever about who produced the payload")


class ContentIntegrity:
    """Canonical-payload digests. Integrity, not authenticity, and it says which."""

    @staticmethod
    def digest(payload: Any) -> Dict[str, Any]:
        """A digest over the payload, with the algorithm, the key source and the limits stated beside it.

        Returns a dict rather than a bare string deliberately: a bare hex string invites a caller to publish it
        under whatever name it likes, which is exactly how this became `pqc_signature`.
        """
        canonical = (payload if isinstance(payload, (bytes, bytearray))
                     else json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        key, key_source = _key()
        return {
            "algorithm": ALGORITHM,
            "digest": hashlib.sha3_512(canonical + key).hexdigest(),
            "computed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "key_source": key_source,
            "proves": "that this exact payload has not been altered since the digest was computed",
            "does_not_prove": ("who produced the payload, nor that any authority endorsed it. The key, when "
                               "there is one, lives in the process that computes the digest, so the digest can "
                               "be recomputed by anything holding it"),
        }

    @staticmethod
    def verify(payload: Any, expected_digest: str) -> Dict[str, Any]:
        """Recompute and compare. Reports WHY it failed rather than a bare False."""
        if not expected_digest or not isinstance(expected_digest, str):
            return {"verified": False, "why": "no digest was supplied to check against"}
        fresh = ContentIntegrity.digest(payload)
        ok = fresh["digest"] == expected_digest
        return {
            "verified": ok,
            "algorithm": ALGORITHM,
            "why": (None if ok else
                    "the payload does not match the digest - it was altered, or the digest was computed with a "
                    "different key than this process holds"),
            "key_source": fresh["key_source"],
        }


content_integrity = ContentIntegrity()


def digest_or_none(payload: Any) -> Optional[Dict[str, Any]]:
    """A digest, or None when one cannot be computed. Never raises into a caller's response path."""
    try:
        return ContentIntegrity.digest(payload)
    except Exception as exc:   # pragma: no cover - hashlib over canonical bytes does not normally fail
        import logging
        logging.getLogger("security.integrity").error("a content digest could not be computed: %s", exc)
        return None
