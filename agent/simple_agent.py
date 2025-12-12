# agent/simple_agent.py

import time
from typing import Dict, Any, Optional


class SimpleAgent:
    def __init__(self, memory):
        self.memory = memory

    def observe(self, content: str, impact: float, current_time: Optional[float] = None):
        if current_time is None:
            current_time = time.time()
            
        memory_item: Dict[str, Any] = {
            "content": content,
            "timestamp": current_time,
            "impact": impact
        }
        self.memory.add(memory_item)

    def ask(self, query: str, current_time: Optional[float] = None):
        if current_time is None:
            current_time = time.time()
        
        results = self.memory.retrieve(query, current_time=current_time)
        return results[0]["content"] if results else None
