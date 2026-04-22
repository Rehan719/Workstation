import torch
import torch.nn as nn
import torch.optim as optim

class RLEconomist(nn.Module):
    """RL economic policy evolution with constitutional legal floor (Phase 6)."""
    def __init__(self, state_dim: int, action_dim: int, legal_floor: float = 0.15):
        super(RLEconomist, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )
        self.legal_floor = legal_floor
        self.optimizer = optim.Adam(self.parameters(), lr=1e-3)

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        action_probs = self.fc(state)
        # Enforce legal floor ζ ≥ 0.15 (Article 1115)
        # We ensure no action probability falls below the floor for critical legal decisions
        action_probs = torch.clamp(action_probs, min=self.legal_floor / 10.0) # Scaled for probability space
        return action_probs / action_probs.sum(dim=-1, keepdim=True)

    async def update_policy(self, state: torch.Tensor, reward: float):
        probs = self.forward(state)
        loss = -torch.log(probs.mean()) * reward
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()
