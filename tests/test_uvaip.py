import pytest
from agentic_core.synthesis.uvaip import UVAIPEngine

def test_uvaip_full_pipeline():
    engine = UVAIPEngine()
    report = engine.run_full_pipeline()

    assert "github_analysis" in report
    assert "version_assimilation" in report
    assert "convergence_results" in report
    assert "timestamp" in report
    assert report["github_analysis"]["status"] == "SUCCESS"
    assert report["convergence_results"]["convergence_score"] > 0.9

def test_github_ingestor():
    from agentic_core.synthesis.uvaip import GitHubIngestor
    ingestor = GitHubIngestor()
    data = ingestor.ingest_history()
    assert data["status"] == "SUCCESS"
    assert "commit_count" in data

def test_version_assimilator():
    from agentic_core.synthesis.uvaip import VersionAssimilator
    assimilator = VersionAssimilator()
    versions = assimilator.assimilate_versions()
    assert len(versions) > 0
    assert any(v["version"] == "v120.0.0" for v in versions)
