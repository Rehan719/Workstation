import pytest
from agentic_core.tools.context_aware_integrator import ContextAwareToolIntegrator

@pytest.mark.asyncio
async def test_context_aware_activation():
    integrator = ContextAwareToolIntegrator()
    task = {
        'id': 'quantum_task',
        'quantum': True,
        'circuit_depth': 150,
        'circuit': 'H(0); CNOT(0,1)',
        'produces_artifact': True
    }
    result = await integrator.process_task(task)
    assert 'mlir_qir' in result['tools_used']
    assert 'sigstore' in result['tools_used']
    assert 'circuit_qir' in result
    assert 'signature' in result

@pytest.mark.asyncio
async def test_simple_task_bypass():
    integrator = ContextAwareToolIntegrator()
    task = {
        'id': 'simple_task',
        'quantum': False,
        'produces_artifact': False
    }
    result = await integrator.process_task(task)
    assert 'mlir_qir' not in result['tools_used']
    assert 'sigstore' not in result['tools_used']
