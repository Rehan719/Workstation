from scripts.automation.skeleton_orchestrator import SkeletonOrchestratorV7

if __name__ == "__main__":
    science = SkeletonOrchestratorV7("Science", "DOM-SCI-001", "Peer Review Board", ["Scientific Method"])
    science.execute_workflow()
