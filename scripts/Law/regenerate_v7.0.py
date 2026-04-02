from scripts.automation.skeleton_orchestrator import SkeletonOrchestratorV7

if __name__ == "__main__":
    law = SkeletonOrchestratorV7("Law", "DOM-LAW-001", "Bar Association / Legal Experts", ["UK/EU Law", "Statutes"])
    law.execute_workflow()
