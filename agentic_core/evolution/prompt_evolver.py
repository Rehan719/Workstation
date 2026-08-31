import logging
import random
import re
from typing import Dict, List, Optional
from agentic_core.ethics.constitutional_enforcer import ConstitutionalEnforcer

logger = logging.getLogger(__name__)

class RecursivePromptEvolver:
    """
    ARTICLE 140: Recursive Prompt Evolution.
    Evolves agent directives using genetic operators and constitutional filtering.
    """
    def __init__(self):
        self.prompt_pool = {}
        self.enforcer = ConstitutionalEnforcer()
        self.mutation_history = []

    def register_prompt(self, agent_id: str, prompt: str):
        self.prompt_pool[agent_id] = prompt

    def evolve(self, agent_id: str, fitness_score: float) -> str:
        """
        Main evolution loop.
        Uses crossover, mutation, and constitutional vetting.
        """
        current_prompt = self.prompt_pool.get(agent_id)
        if not current_prompt:
            return ""

        if fitness_score >= 0.95:
            logger.info(f"Prompt for {agent_id} has high fitness ({fitness_score}). Stabilizing.")
            return current_prompt

        logger.info(f"Evolving prompt for {agent_id} (Fitness: {fitness_score})...")

        # Select mutation strategy
        strategy = random.choice(["mutate", "crossover", "perturb"])

        if strategy == "mutate":
            new_prompt = self._mutate(current_prompt)
        elif strategy == "crossover":
            # Crossover with a high-performing baseline or random other prompt
            other_prompt = "Execute tasks with 100% functional logic and zero stubs. Maintain SIH priority."
            new_prompt = self._crossover(current_prompt, other_prompt)
        else:
            new_prompt = self._perturb(current_prompt)

        # Constitutional Vetting (Article 140)
        if self.enforcer.verify_action("prompt_mutation", {"new_prompt": new_prompt}):
            logger.info("Mutation PASSED constitutional audit.")
            self.prompt_pool[agent_id] = new_prompt
            self.mutation_history.append({"agent": agent_id, "strategy": strategy, "score": fitness_score})
            return new_prompt
        else:
            logger.warning("Mutation REJECTED by Constitutional Enforcer. Reverting.")
            return current_prompt

    def _mutate(self, prompt: str) -> str:
        """Injects goal-directed refinements."""
        refinements = [
            " Ensure all outputs are formatted as ScholarlyObjects with full provenance.",
            " Prioritize adversarial robustness using minimax strategy evaluation.",
            " Implement behavior-driven granularity based on interaction signals.",
            " Enforce strict SIH: Immune > Nervous > Digestive > Aging."
        ]
        return prompt + random.choice(refinements)

    def _crossover(self, p1: str, p2: str) -> str:
        """Combines components of two prompts."""
        # Split by sentence
        s1 = re.split(r'(?<=[.!?]) +', p1)
        s2 = re.split(r'(?<=[.!?]) +', p2)

        # Ensure at least one part of p1 is kept to maintain identity in tests
        idx = max(1, len(s1)//2)
        combined = s1[:idx] + s2[len(s2)//2:]
        return " ".join(combined)

    def _perturb(self, prompt: str) -> str:
        """Semantic perturbation of existing directives."""
        words = prompt.split()
        if not words: return prompt

        # Replace common words with more 'transcendent' variants
        mapping = {
            "good": "optimal",
            "fast": "low-latency",
            "check": "verify",
            "rule": "constitutional mandate",
            "think": "deliberate via meta-cognitive executive"
        }

        new_words = [mapping.get(w.lower(), w) for w in words]
        return " ".join(new_words)

if __name__ == "__main__":
    evolver = RecursivePromptEvolver()
    base = "You are a helpful AI agent. Think about the rule before you act. Do a good job."
    evolver.register_prompt("agent_alpha", base)

    for i in range(3):
        res = evolver.evolve("agent_alpha", 0.7)
        print(f"Iteration {i+1}: {res}")
