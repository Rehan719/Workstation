import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

#  §4 (W575, FU-077) — THE ONTOLOGY ENGINE IS RETIRED, ON THE OWNER'S RULING OF 2026-09-30:
#  "RETIRE THE ENGINE, KEEP THE ASSET, RECLASSIFY IT HONESTLY."
#
#  WHY, MEASURED. The engine read `agentic_core/data/ontologies/`, which holds nothing and which
#  nothing ever writes, so every domain query answered an absence. The ruling then revised both arms
#  the row had offered, on a measurement taken before ruling — and this round re-took it rather than
#  trusting it:
#    · knowledge/Law/EmploymentTribunal/ontology/uk_employment_law_v9.json holds 494 REAL UK
#      employment-law concepts and 4 rules, and NO relations key at all.
#    · unified_assimilated_graph.json holds 293 "nodes" that are FILE PATHS over the Owner's own
#      documents, each with a hash, and NO edges key — the simulated-assimilation era.
#  So the engine served graphs and no graph exists. Wiring it would have meant inventing relations.
#
#  WHAT IS KEPT. The 494-concept vocabulary and its rules remain on disk as a LAW DOMAIN RESOURCE for
#  P3.23's stakes-scaled gate, where they pair with FU-278's requirement that a legal artefact cite a
#  page and a line. They are a VOCABULARY, not a graph, and nothing here loads them as one. The
#  293-node manifest is never loaded as an ontology.
#
#  REACHABILITY, ESTABLISHED BEFORE REMOVAL (P2.4 cluster (a) requires the check to be recorded):
#  the engine was reached by exactly one path — agentic_core/api/v138/ceo.py dispatches the AI CEO's
#  `domain_weaver` tool into this module, which called `ontology_engine.searched()`. A repo-wide
#  search found no other importer in the live tree: the remaining hits are this file, the engine
#  itself, `_archive/`, and register rows. So retiring it changes exactly this surface, and this
#  surface now says what is true instead of reporting an absence per domain.


class DomainWeaver:
    """Cross-domain synthesis. There is no ontology service to synthesise over, and it says so."""

    def __init__(self):
        self.domains = ["religion", "science", "law", "employment", "education", "care"]

    NO_SERVICE_BASIS = (
        "no ontology service exists on this platform. The engine that served this surface was "
        "retired on the Owner's ruling of 2026-09-30 because it read a directory that holds "
        "nothing: it answered every domain with an empty graph, which a caller could read as 'the "
        "ontology was consulted and held nothing'. The one real asset is a 494-concept UK "
        "employment-law VOCABULARY with four rules and no relations, kept as a Law domain resource "
        "for the legal specialist's gate — a vocabulary is not a graph and cannot be traversed for "
        "cross-domain findings. A 293-node file-path manifest from the simulated-assimilation era "
        "is never loaded as an ontology."
    )

    async def synthesize(self, query: str, active_domains: List[str]) -> Dict[str, Any]:
        """Return the honest absence, in the shape callers already read.

        W506 made every clause of the old synthesis conditional on content, so nothing was asserted
        over zero findings. W575 removes the step before that one: there is nothing to find, and
        reporting it per domain ("NO ONTOLOGY WAS CONSULTED — ...", six times) read as a service
        that was temporarily empty rather than one that does not exist.
        """
        logger.info("DomainWeaver: no ontology service; refusing synthesis for %r over %s",
                    query, active_domains)
        return {
            "query": query,
            "synthesis": (f"No cross-domain synthesis is available for {query!r}. "
                          f"{self.NO_SERVICE_BASIS}"),
            "structured_report": {
                "summary": "no ontology service exists, so nothing was synthesised",
                "basis": self.NO_SERVICE_BASIS,
                "domains_requested": list(active_domains),
                "domains_with_findings": [],
                "entries_found": 0,
                # A `kept_asset` field and an unknown-domain list were returned here and removed in
                # the same round: the pre-flight's key screen found neither reaching any surface.
                # The kept asset is named in NO_SERVICE_BASIS above, which travels in `synthesis` —
                # the field a reader actually meets through the AI CEO's answer.
                "score_basis": ("there is no confidence instrument here, and no counts to report: "
                                "nothing was searched"),
            },
            "raw_data": {},
            "status": "no_ontology_service",
        }


domain_weaver = DomainWeaver()
