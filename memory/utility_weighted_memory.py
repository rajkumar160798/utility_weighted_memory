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
