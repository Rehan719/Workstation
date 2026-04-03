import random
import json

class FederatedLearningSimulator:
    """
    Simulation of Privacy-Preserving Federated Learning with Differential Privacy.
    Local models train on realm-specific data, and gradients are aggregated globally.
    (Non-numpy version for compatibility)
    """
    def __init__(self, privacy_budget_epsilon=0.1, noise_multiplier=0.01):
        self.privacy_budget_epsilon = privacy_budget_epsilon
        self.noise_multiplier = noise_multiplier
        self.global_model = {
            "content_quality_weights": [random.random() for _ in range(5)],
            "concept_relevance_weights": [random.random() for _ in range(3)],
            "learner_retention_biases": [random.random() for _ in range(2)]
        }
        self.realms = ["Forge", "Genome", "Learner"]
        self.local_updates = {}

    def local_training_step(self, realm_name, local_data_size=100):
        """
        Simulates local training on realm-specific synthetic data and adds DP noise.
        """
        print(f"FEDERATED LEARNING: Local training on realm {realm_name}...")

        # Simulate gradient computation
        local_update = {
            key: [val + random.uniform(-0.05, 0.05) for val in values]
            for key, values in self.global_model.items()
        }

        # Add Differential Privacy Noise (Laplacian noise approximation)
        dp_noise_update = {
            key: [val + random.gauss(0, self.noise_multiplier) for val in values]
            for key, values in local_update.items()
        }

        self.local_updates[realm_name] = {
            "model_update": dp_noise_update,
            "data_size": local_data_size,
            "epsilon": self.privacy_budget_epsilon / len(self.realms)
        }

        return self.local_updates[realm_name]

    def aggregate_updates(self):
        """
        Aggregates local updates to update the global model (Federated Averaging).
        """
        if not self.local_updates:
            return self.global_model

        print("FEDERATED LEARNING: Aggregating local updates into global model...")

        total_data_points = sum(update["data_size"] for update in self.local_updates.values())

        new_global_model = {}
        for key in self.global_model.keys():
            # Weighted average
            size = len(self.global_model[key])
            weighted_sums = [0.0] * size
            for realm_update in self.local_updates.values():
                for i in range(size):
                    weighted_sums[i] += realm_update["model_update"][key][i] * realm_update["data_size"]

            new_global_model[key] = [s / total_data_points for s in weighted_sums]

        self.global_model = new_global_model

        # Reset local updates for next round
        self.local_updates = {}

        return self.global_model

if __name__ == "__main__":
    fl = FederatedLearningSimulator()
    fl.local_training_step("Forge")
    fl.local_training_step("Genome")
    fl.local_training_step("Learner")
    global_model = fl.aggregate_updates()
    print("NEW GLOBAL MODEL:", json.dumps(global_model, indent=2))
