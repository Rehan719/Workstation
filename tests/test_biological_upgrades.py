from agentic_core.digestion.nutrient_quality import NutrientQualityScore
from agentic_core.immune.memory_b_cells import MemoryBCells
from agentic_core.immune.t_cell_regulation import TCellRegulator
from agentic_core.pulse.pulse_clock import PulseClock
from agentic_core.pulse.clock_distribution import ClockDistributionNetwork

def test_biological_upgrades():
    # 1. Digestive Quality
    nqs = NutrientQualityScore()
    meta = {"lexical_divergence": 0.7, "reproducibility_score": 0.9}
    score = nqs.compute_score(meta)
    assert score > 0.5

    # 2. Immune Memory
    mbc = MemoryBCells()
    mbc.log_neutralized_threat(12345, {"type": "buffer_overflow"})
    assert mbc.quick_search(12345) is True
    assert mbc.quick_search(67890) is False

    # 3. T-Cell Regulation
    tcr = TCellRegulator()
    assert tcr.is_self({"signature": "sig:v62.0.1"}) is True
    assert tcr.is_self({"signature": "sig:v61"}) is False

    # 4. Multi-core Clock
    clock = PulseClock()
    cdn = ClockDistributionNetwork(clock)
    p1 = cdn.get_synchronized_pulse(0)
    p2 = cdn.get_synchronized_pulse(1)
    # They should be very close, but may differ by a few pulses due to execution time
    assert abs(p1 - p2) < 100

    print("Biological Subsystem Upgrades verification PASSED.")

if __name__ == "__main__":
    test_biological_upgrades()
