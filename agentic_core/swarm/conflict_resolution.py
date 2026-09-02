import logging
from typing import List, Any, Dict, Optional
from .signal_types import SwarmSignal, SignalType

logger = logging.getLogger(__name__)

class ConflictResolution:
    """
    DN: Swarm-Level Conflict Resolution.
    Triggered when consensus cannot be reached.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def resolve(self, conflict_id: str, options: List[Any]) -> Any:
        # W437: this is the §4.5 archetype and must not be wired as-is — it returns options[0] by
        # POSITION with zero discrimination. The old comment said "pick the most robust option" and
        # the log claimed arbitration; nothing computes robustness. Zero live callers exist. If this
        # is ever revived, route through ConsensusEngine.consensus_detail or an actual criterion.
        resolved_option = options[0]
        logger.warning("GOVERNANCE: conflict %s — returning the FIRST option by position "
                       "(no discrimination performed): %s", conflict_id, resolved_option)
        return resolved_option

class ConsensusEngine:
    """Helper for reaching consensus among swarm members."""
    def __init__(self, threshold: float = 0.66):
        self.threshold = threshold
        self.votes: Dict[str, Dict[str, int]] = {}

    def record_vote(self, proposal_id: str, voter_id: str, choice: str):
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}
        self.votes[proposal_id][voter_id] = choice

    def check_consensus(self, proposal_id: str, total_nodes: int) -> Optional[str]:
        """The strongest choice that clears the threshold, or None. See `consensus_detail`."""
        return self.consensus_detail(proposal_id, total_nodes)["choice"]

    def consensus_detail(self, proposal_id: str, total_nodes: int) -> Dict[str, Any]:
        """W431 — §4.5 class: this returned the FIRST choice to clear the threshold in insertion
        order, not the strongest. Proved live: ALPHA with 2 votes was reported as the consensus over
        BETA with 3 at threshold 0.4, because ALPHA's first voter appeared earlier in the array —
        and the payload said `"reached": true, "choice": "ALPHA"` with no hint that BETA held a
        strictly larger share. Reversing the input array flipped the "consensus" on identical votes.

        Now: the strongest clearing choice wins, an exact tie at the top is DISCLOSED rather than
        resolved by insertion order, and the tally travels with the verdict so a caller can check it.
        `distinct_voters` is reported separately from the raw ballot count because votes are keyed by
        voter and later ballots OVERWRITE earlier ones — three entries from one voter is one vote,
        and the old response reported it as three.
        """
        ballots = self.votes.get(proposal_id) or {}
        counts: Dict[str, int] = {}
        for choice in ballots.values():
            counts[choice] = counts.get(choice, 0) + 1

        denom = total_nodes if total_nodes > 0 else len(ballots)
        shares = {c: (n / denom if denom else 0.0) for c, n in counts.items()}
        clearing = sorted((c for c, s in shares.items() if s >= self.threshold),
                          key=lambda c: (-shares[c], c))
        top = [c for c in clearing if shares[c] == shares[clearing[0]]] if clearing else []
        tied = len(top) > 1

        return {
            "choice": None if (not clearing or tied) else clearing[0],
            "reached": bool(clearing) and not tied,
            "tied": tied,
            "tied_choices": top if tied else [],
            "tally": counts,
            "shares": {c: round(s, 4) for c, s in shares.items()},
            "distinct_voters": len(ballots),
            "threshold": self.threshold,
            "basis": ("no proposal recorded" if not ballots else
                      f"{len(top)} choices tied at {round(shares[top[0]], 4)} - not resolved by vote share" if tied
                      else f"{clearing[0]} holds {round(shares[clearing[0]], 4)} >= {self.threshold}" if clearing
                      else f"no choice reached {self.threshold}; best was {round(max(shares.values()), 4)}"
                           if shares else "no votes cast"),
        }
