import asyncio
import logging
from agentic_core.pulse.pulse_clock import PulseClock
from agentic_core.sensory.vision import VisualCortex
from agentic_core.sensory.audition import AuditoryCortex
from agentic_core.sensory.transduction import SensoryTransducer
from agentic_core.perception.fusion import SensoryFusionCortex
from agentic_core.perception.binding import PerceptualBinding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_sensory_perception_flow():
    clock = PulseClock()
    vision = VisualCortex()
    audition = AuditoryCortex()
    transducer = SensoryTransducer(clock)
    fusion = SensoryFusionCortex()
    binding = PerceptualBinding()

    logger.info("Starting Sensory-Perception Integration Test...")

    # 1. Sensory Capture
    v_raw = vision.process_visual_input(None)
    a_raw = audition.process_audio_input(None)

    # 2. Transduction
    v_spike = transducer.transduce(v_raw)
    a_spike = transducer.transduce(a_raw)

    # 3. Fusion
    fused = fusion.fuse_signals([v_raw, a_raw])
    assert fused["is_coherent"] is True

    # 4. Binding
    obj = binding.create_perceptual_object([v_spike, a_spike])
    assert obj["type"] == "perceptual_entity"
    assert "vision" in obj["constituents"]
    assert "audition" in obj["constituents"]

    print("Sensory-Perception Flow verification PASSED.")

if __name__ == "__main__":
    asyncio.run(test_sensory_perception_flow())
