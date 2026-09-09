"""
Autonomous Agent Epidemic Gossip Protocol Skill
Pure Python Standard Library implementation.
"""
import random
from typing import List, Dict, Set, Any

class GossipCluster:
    """
    Epidemic Anti-Entropy Gossip Dissemination Engine.
    """
    def __init__(self, node_ids: List[str], seed: int = 42):
        self.nodes = node_ids
        self.state = {n: set() for n in node_ids}
        self.rng = random.Random(seed)

    def inject_rumor(self, origin: str, rumor_id: str):
        self.state[origin].add(rumor_id)

    def step_round(self, fanout: int = 2):
        new_state = {n: set(s) for n, s in self.state.items()}
        for node in self.nodes:
            if not self.state[node]:
                continue
            targets = [p for p in self.nodes if p != node]
            selected = self.rng.sample(targets, min(fanout, len(targets)))
            for t in selected:
                new_state[t].update(self.state[node])
        self.state = new_state

    def dissemination_ratio(self, rumor_id: str) -> float:
        infected = sum(1 for n in self.nodes if rumor_id in self.state[n])
        return round(infected / len(self.nodes), 4)
