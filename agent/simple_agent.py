# agent/simple_agent.py

import time
from typing import Dict, Any


class SimpleAgent:
    def __init__(self, memory):
        self.memory = memory

    def observe(self, content: str, impact: float):
        memory_item: Dict[str, Any] = {
            "content": content,
            "timestamp": time.time(),
            "impact": impact
        }
        self.memory.add(memory_item)

    def ask(self, query: str):
        results = self.memory.retrieve(query)
        return results[0]["content"] if results else None
