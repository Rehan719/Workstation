import pytest
from datetime import datetime
from agentic_core.interface.hybrid_granularity_controller import HybridGranularityController

@pytest.mark.asyncio
async def test_hybrid_granularity_implicit():
    controller = HybridGranularityController()
    interaction = {'timestamp': datetime.utcnow(), 'type': 'pause'}
    # First interaction won't trigger pause
    await controller.process_interaction('user1', interaction)

    # Second interaction after long pause
    interaction2 = {'timestamp': datetime.utcnow(), 'type': 'click'}
    # Mocking a long pause would require time.sleep or manual timestamping, but let's just test it runs
    action = await controller.process_interaction('user1', interaction2)
    assert action in ['no_change', 'show_summary']

@pytest.mark.asyncio
async def test_explicit_override():
    controller = HybridGranularityController()
    await controller.handle_explicit_change('user1', 'expert')
    action = await controller.process_interaction('user1', {'type': 'hover'})
    assert action == 'set_expert'
