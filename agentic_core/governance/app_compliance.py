import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AppCompliance:
    """
    ARTICLE 146: Application Generation Integrity.
    Screens user-generated code for one hardcoded-secret pattern. This is NOT a security or
    constitutional audit — see verify_app's `rules_not_checked` for what does not run.
    """
    # W415 — self.rules declared three rules ("no_hardcoded_secrets", "privacy_safe",
    # "sih_aligned") while only the first was ever evaluated, and only as the literal substring
    # "API_KEY =". Declaring a rule in the object a consumer inspects asserts that the rule is
    # enforced. There is no privacy analyser in this repo and no definition of "SIH" anywhere
    # outside this line, so the two unimplemented rules are now declared as absent rather than
    # counted among the rules that ran.
    RULES_IMPLEMENTED = ["no_hardcoded_secrets"]
    RULES_NOT_IMPLEMENTED = ["privacy_safe", "sih_aligned"]

    def __init__(self):
        self.rules = list(self.RULES_IMPLEMENTED)
        self.rules_not_implemented = list(self.RULES_NOT_IMPLEMENTED)

    def verify_app(self, app_id: str, source_code: str) -> Dict[str, Any]:
        logger.info(f"Compliance: Auditing app {app_id}")

        # The one real check: a literal substring match for an assigned API key.
        violations = []
        if "API_KEY =" in source_code:
            violations.append("HARDCODED_SECRET")

        # W415 — this returned {"status": "passed"/"failed", "violations": [...],
        # "report_id": f"REP-{app_id}"}. A "passed" verdict carrying a report id reads as a
        # completed three-rule security + constitutional audit that cleared the code. Executed
        # live, verify_app('app1', 'import os; os.system("rm -rf /"); token="sk-live-abc"')
        # returned {'status': 'passed', 'violations': []}. A single substring match cannot
        # certify anything, so a clean result no longer says "passed", the rules that never ran
        # are reported as NOT_IMPLEMENTED, and the report id — which identified an audit report
        # that is never written anywhere and cannot be retrieved — is reported as absent.
        return {
            "status": "failed" if violations else "clean_on_implemented_rules",
            "violations": violations,
            "rules_checked": {r: ("failed" if violations else "clean")
                              for r in self.RULES_IMPLEMENTED},
            "rules_not_checked": {r: "NOT_IMPLEMENTED" for r in self.RULES_NOT_IMPLEMENTED},
            "report_id": None,
            "detail": (
                "Only no_hardcoded_secrets runs, as a literal 'API_KEY =' substring match. "
                "privacy_safe and sih_aligned have no implementation in this repo and were not "
                "evaluated. No audit report is generated or stored, so there is no report id. "
                "A clean result means this one match found nothing — it is not a security or "
                "constitutional certification."
            ),
        }
