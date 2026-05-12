import hashlib
from typing import List, Dict, Any

class DNA:
    """
    ARTICLE 161: The fundamental DNA sequence representation.
    Handles base-level encoding and decoding of genetic information.
    """
    def __init__(self, sequence: str):
        self.sequence = sequence
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        return hashlib.sha256(self.sequence.encode()).hexdigest()

    def get_subsequence(self, start: int, end: int) -> str:
        return self.sequence[start:end]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence": self.sequence,
            "hash": self.hash
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DNA':
        return cls(data["sequence"])
