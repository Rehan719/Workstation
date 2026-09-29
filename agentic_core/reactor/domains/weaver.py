import logging
from typing import Dict, Any, List
from agentic_core.reactor.domains.ontology_engine import ontology_engine

logger = logging.getLogger(__name__)

class DomainWeaver:
    """v0.1: Cross-Domain Knowledge Synthesis Engine."""
    def __init__(self):
        self.domains = ["religion", "science", "law", "employment", "education", "care"]

    async def synthesize(self, query: str, active_domains: List[str]) -> Dict[str, Any]:
        """Cross-domain synthesis over what the ontologies ACTUALLY return.

        W506 (FU-077) - every clause here used to be asserted regardless of content. The comparative-analysis
        line fired because two KEYS existed in a dict whose values were both empty lists; the ethical-guardrail
        line cited a numbered constitutional article on patient sovereignty that exists nowhere in this
        repository - the number is in the commit that removed it and is not repeated here, because an invented
        citation is worth recording once and not carrying forward; the conclusion
        confirmed "sovereign alignment"; the confidence score was the constant 0.98; and the status was SUCCESS.
        All of it over zero findings, in the care and law domains.

        Now: a claim appears only when the findings support it, the absence of an ontology is stated with its
        reason, and the score is replaced by counts a reader can verify against `raw_data`.
        """
        logger.info("DomainWeaver: synthesising across %s for %r", active_domains, query)

        searched: Dict[str, Any] = {}
        for domain in active_domains:
            if domain in self.domains:
                searched[domain] = ontology_engine.searched(domain, query)

        results = {d: v["results"][:3] for d, v in searched.items()}
        with_findings = [d for d, items in results.items() if items]
        unavailable = [d for d, v in searched.items() if not v["available"]]

        lines = [f"Cross-domain synthesis for {query!r}:"]

        # a comparison requires BOTH sides to have returned something. The old test was `key in results`.
        if "religion" in with_findings and "science" in with_findings:
            lines.append("Comparative analysis: both the religion and science ontologies returned entries for "
                         "this query; the intersection below is drawn from those entries.")
        if "care" in with_findings and "law" in with_findings:
            # the invented article citation is GONE. No constitutional article is cited unless it exists.
            lines.append("Care and law both returned entries; any guardrail a reader needs must come from the "
                         "entries below, not from this summary.")

        for domain in active_domains:
            if domain not in searched:
                lines.append(f"- [{domain.upper()}]: not a known domain for this weaver.")
                continue
            items = results.get(domain) or []
            if items:
                lines.append(f"- [{domain.upper()}]: {', '.join(str(i.get('id', i)) for i in items)}")
            elif not searched[domain]["available"]:
                lines.append(f"- [{domain.upper()}]: NO ONTOLOGY WAS CONSULTED - "
                             f"{searched[domain]['basis']}")
            else:
                lines.append(f"- [{domain.upper()}]: the ontology was consulted and held no entry "
                             f"matching this query.")

        if not with_findings:
            lines.append("NOTHING WAS SYNTHESISED: no domain returned an entry, so there is no cross-domain "
                         "finding to report. This is not a negative result about the query.")

        return {
            "query": query,
            "synthesis": "\n".join(lines),
            "structured_report": {
                "summary": (f"cross-domain synthesis over {len(with_findings)} domain(s) that returned entries"
                            if with_findings else
                            "no domain returned an entry, so nothing was synthesised"),
                "domains_requested": list(active_domains),
                "domains_with_findings": with_findings,
                "domains_without_an_ontology": unavailable,
                "entries_found": sum(len(v) for v in results.values()),
                "score_basis": ("there is no confidence instrument here. The counts above are what can be "
                                "checked; a score would be a number nothing computed"),
            },
            "raw_data": results,
            "status": "synthesised" if with_findings else "nothing_to_synthesise",
        }

domain_weaver = DomainWeaver()
