import asyncio
import time
from agentic_core.pulse.pulse_clock import PulseClock

async def test_pulse_clock():
    clock = PulseClock()
    print(f"Start pulse: {clock.get_current_pulse()}")
    time.sleep(0.01) # 10ms
    current_pulse = clock.get_current_pulse()
    print(f"Pulse after 10ms: {current_pulse}")

    # Expect roughly frequency * 0.01 = 1.2M * 0.01 = 12000 pulses
    assert 10000 < current_pulse < 14000
    print("Pulse clock verification PASSED.")

if __name__ == "__main__":
    asyncio.run(test_pulse_clock())
