from agentic_core.digestion.digestive_system import AppetitiveDigestiveSystem

def test_appetite():
    ds = AppetitiveDigestiveSystem()
    print(f"Initial hunger: {ds.hunger}")

    # 1. Low novelty content
    low_novelty = {"lexical_divergence": 0.2}
    ds.evaluate_content(low_novelty)
    print(f"Hunger after low novelty: {ds.hunger}")
    assert ds.hunger > 0.5

    # 2. High novelty content
    high_novelty = {"lexical_divergence": 0.85, "alignment": 0.95}
    ds.evaluate_content(high_novelty)
    print(f"Hunger after high novelty: {ds.hunger}")
    assert ds.hunger < 0.6 # It dropped back

    print("Appetitive Digestive System verification PASSED.")

if __name__ == "__main__":
    test_appetite()
