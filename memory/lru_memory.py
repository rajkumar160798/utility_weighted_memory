# memory/lru_memory.py

from typing import List, Dict, Any
from collections import OrderedDict
from memory.base_memory import BaseMemory


class LRUMemory(BaseMemory):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        # OrderedDict handles LRU logic automatically
        self.cache = OrderedDict()

    def add(self, memory: Dict[str, Any]):
        # Use content string as key for simulation
        key = memory["content"]
        if key in self.cache:
            self.cache.move_to_end(key)  # Mark as recently used
        else:
            self.cache[key] = memory
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)  # Evict first item (Least Recently Used)

    def retrieve(self, query: str, top_k: int = 1, current_time: float = None) -> List[Dict[str, Any]]:
        results = []
        # Iterate over items to find matches
        for key, memory in list(self.cache.items()):  # Cast to list to avoid runtime errors
            if query.lower() in memory["content"].lower():
                self.cache.move_to_end(key)  # Update recency on read
                results.append(memory)
        return results[-top_k:][::-1]  # Return most recent matches

    def stats(self):
        return {"size": len(self.cache), "capacity": self.capacity}
