# memory/utility_weighted_memory.py

import math
import time
from typing import List, Dict, Any
from memory.base_memory import BaseMemory


class UtilityWeightedMemory(BaseMemory):
    def __init__(
        self,
        capacity: int,
        w_freq: float = 0.4,
        w_impact: float = 0.6,
        decay_lambda: float = 0.01,
    ):
        super().__init__(capacity)
        self.memories: List[Dict[str, Any]] = []
        self.w_freq = w_freq
        self.w_impact = w_impact
        self.decay_lambda = decay_lambda

    def _score(self, memory: Dict[str, Any], current_time: float) -> float:
        freq = memory.get("access_count", 0)
        impact = memory.get("impact", 0)
        age = current_time - memory.get("timestamp", current_time)
        decay = math.exp(-self.decay_lambda * age)
        return self.w_freq * freq + self.w_impact * impact * decay

    def add(self, memory: Dict[str, Any]):
        memory["access_count"] = 0
        if len(self.memories) >= self.capacity:
            # Find memory with lowest utility score
            current_time = time.time()
            scores = [self._score(m, current_time) for m in self.memories]
            min_idx = scores.index(min(scores))
            self.memories.pop(min_idx)
        self.memories.append(memory)

    def retrieve(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        # Keyword match and update access count
        results = []
        for m in self.memories:
            if query.lower() in m["content"].lower():
                m["access_count"] = m.get("access_count", 0) + 1
                results.append(m)
        return results[:top_k]

    def stats(self) -> Dict[str, Any]:
        return {
            "size": len(self.memories),
            "capacity": self.capacity,
            "w_freq": self.w_freq,
            "w_impact": self.w_impact
        }
