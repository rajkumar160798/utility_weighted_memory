# memory/base_memory.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseMemory(ABC):
    def __init__(self, capacity: int):
        self.capacity = capacity

    @abstractmethod
    def add(self, memory: Dict[str, Any]):
        pass

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 1, current_time: float = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def stats(self) -> Dict[str, Any]:
        pass
