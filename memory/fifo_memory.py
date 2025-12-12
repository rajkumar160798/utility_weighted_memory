# memory/fifo_memory.py

from typing import List, Dict, Any
from collections import deque
from memory.base_memory import BaseMemory


class FIFOMemory(BaseMemory):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.buffer = deque()

    def add(self, memory: Dict[str, Any]):
        if len(self.buffer) >= self.capacity:
            self.buffer.popleft()  # FIFO eviction
        self.buffer.append(memory)

    def retrieve(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        # naive keyword match
        results = [m for m in self.buffer if query.lower() in m["content"].lower()]
        return results[:top_k]

    def stats(self):
        return {
            "size": len(self.buffer),
            "capacity": self.capacity
        }
