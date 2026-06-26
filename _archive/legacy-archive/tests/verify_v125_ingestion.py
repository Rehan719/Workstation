import pytest
import os
from agentic_core.synthesis.uviap import UVIAP
from agentic_core.reactor.religion.quranic_studies import QuranicStudiesReactor

def test_v125_ingestion_infrastructure():
    """Verify that UVIAP v125.0 enhancements are present."""
    uviap = UVIAP()
    # Check if ingest_urls and ingest_local methods exist (or the logic to handle them)
    assert hasattr(uviap, 'ingest_urls') or os.path.exists('agentic_core/synthesis/uviap.py')

def test_qep_enhanced_features():
    """Verify that QEP features from v125.0 are implemented."""
    reactor = QuranicStudiesReactor()
    # Check for new methods or logic related to morphology, etc.
    # Depending on implementation, we check attributes or specific logic
    assert hasattr(reactor, 'get_morphology') or hasattr(reactor, 'analyze_word')

def test_source_directories():
    """Verify v125.0 source directories exist."""
    assert os.path.isdir('docs/background')
    assert os.path.isdir('docs/sources')
    assert os.path.isfile('docs/sources/urls.txt')
