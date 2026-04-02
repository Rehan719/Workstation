from scripts.automation.skeleton_orchestrator import SkeletonOrchestratorV7

if __name__ == "__main__":
    care = SkeletonOrchestratorV7("Care", "DOM-CAR-001", "CQC / Ethics Board", ["Healthcare Standards", "Safeguarding"])
    care.execute_workflow()
