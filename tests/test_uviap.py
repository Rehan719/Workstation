import pytest
from agentic_core.synthesis.uviap import UVIAPEngine

def test_uviap_full_pipeline():
    engine = UVIAPEngine()
    report = engine.run_full_pipeline()

    assert "github_analysis" in report
    assert "version_assimilation" in report
    assert "convergence_results" in report
    assert "learning_reflection" in report
    assert "timestamp" in report
    assert report["github_analysis"]["status"] == "SUCCESS"
    assert report["convergence_results"]["convergence_score"] > 0.9
    assert report["learning_reflection"]["reflection_status"] == "OPTIMAL"

def test_github_ingestor():
    from agentic_core.synthesis.uviap import GitHubIngestor
    ingestor = GitHubIngestor()
    data = ingestor.ingest_history()
    assert data["status"] == "SUCCESS"
    assert "commit_count" in data

def test_version_assimilator():
    from agentic_core.synthesis.uviap import VersionAssimilator
    assimilator = VersionAssimilator()
    versions = assimilator.assimilate_versions()
    assert len(versions) > 0
    # The dna_generator.py generates CONSTITUTION_v120.0.0.md
    assert any(v["version"] == "v120.0.0" for v in versions)
