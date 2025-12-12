# memory/similarity_memory.py

from typing import List, Dict, Any
from memory.base_memory import BaseMemory


class SimilarityOnlyMemory(BaseMemory):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.memories: List[Dict[str, Any]] = []

    def _similarity(self, query: str, content: str) -> float:
        # simple token overlap (acts like weak embedding similarity)
        q_tokens = set(query.lower().split())
        c_tokens = set(content.lower().split())
        return len(q_tokens & c_tokens)

    def add(self, memory: Dict[str, Any]):
        if len(self.memories) >= self.capacity:
            self.memories.pop(0)  # naive eviction
        self.memories.append(memory)

    def retrieve(self, query: str, top_k: int = 1, current_time: float = None) -> List[Dict[str, Any]]:
        scored = [
            (self._similarity(query, m["content"]), m)
            for m in self.memories
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for score, m in scored if score > 0][:top_k]

    def stats(self):
        return {
            "size": len(self.memories),
            "capacity": self.capacity
        }
