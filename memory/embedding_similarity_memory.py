import math
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .base_memory import BaseMemory


class EmbeddingSimilarityMemory(BaseMemory):
    """
    Memory strategy using dense embeddings and cosine similarity.
    
    Uses sentence-transformers/all-MiniLM-L6-v2 for semantic embeddings.
    Stores embeddings for all memory items and ranks retrieval by cosine similarity.
    Evicts the least similar item when capacity is reached.
    
    This is a realistic RAG baseline that mimics semantic search systems.
    """
    
    def __init__(self, capacity=20):
        super().__init__(capacity)
        self.memory = {}  # {item_id: {"content": str, "embedding": np.array, "impact": float, "timestamp": float}}
        self.item_counter = 0
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.stats_data = {}
    
    def add(self, memory_item: Dict[str, Any]):
        """
        Add an item to memory with semantic embedding.
        If at capacity, evict the least similar item.
        
        Args:
            memory_item: Dict with keys: content, impact, timestamp
        """
        content = memory_item.get("content", "")
        impact = memory_item.get("impact", 0.1)
        timestamp = memory_item.get("timestamp", 0.0)
        
        # Compute embedding for new item
        embedding = self.model.encode(content, convert_to_tensor=False)
        
        item_id = self.item_counter
        self.item_counter += 1
        
        self.memory[item_id] = {
            "content": content,
            "embedding": embedding,
            "impact": impact,
            "timestamp": timestamp
        }
        
        # Track stats
        if impact > 0.5:
            self.stats_data[item_id] = "high"
        else:
            self.stats_data[item_id] = "low"
        
        # Evict if at capacity
        if len(self.memory) > self.capacity:
            self._evict_least_similar()
    
    def _evict_least_similar(self):
        """
        Evict the item with lowest average similarity to all other items.
        This heuristic removes items that are least connected semantically.
        """
        if not self.memory:
            return
        
        # Get all embeddings
        item_ids = list(self.memory.keys())
        embeddings = [self.memory[idx]["embedding"] for idx in item_ids]
        
        # Compute average similarity for each item to all others
        if len(embeddings) == 1:
            # Only one item, can't evict
            return
        
        similarities = cosine_similarity(embeddings)
        avg_sims = [similarities[i].mean() for i in range(len(item_ids))]
        
        # Evict item with lowest similarity (most anomalous / least connected)
        min_idx = avg_sims.index(min(avg_sims))
        evicted_id = item_ids[min_idx]
        del self.memory[evicted_id]
        if evicted_id in self.stats_data:
            del self.stats_data[evicted_id]
    
    def retrieve(self, query: str, top_k: int = 1, current_time: float = None) -> List[Dict[str, Any]]:
        """
        Retrieve items by cosine similarity to query embedding.
        Returns top_k items sorted by similarity (highest first).
        
        Args:
            query: Query string
            top_k: Number of top results to return
            current_time: Current time (for compatibility, not used here)
            
        Returns:
            List of dicts with keys: content, score, impact
        """
        if not self.memory:
            return []
        
        # Encode query
        query_embedding = self.model.encode(query, convert_to_tensor=False)
        
        # Compute similarity to all items
        results = []
        item_ids = list(self.memory.keys())
        embeddings = [self.memory[idx]["embedding"] for idx in item_ids]
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        
        for idx, item_id in enumerate(item_ids):
            similarity_score = similarities[idx]
            results.append({
                "content": self.memory[item_id]["content"],
                "score": similarity_score,
                "impact": self.memory[item_id]["impact"]
            })
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]
    
    def stats(self):
        """Return statistics about memory state."""
        high_impact = sum(1 for v in self.stats_data.values() if v == "high")
        low_impact = sum(1 for v in self.stats_data.values() if v == "low")
        return {
            "total": len(self.memory),
            "capacity": self.capacity,
            "high_impact": high_impact,
            "low_impact": low_impact
        }
