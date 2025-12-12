# experiments/retention_curve.py

import sys
import os
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.simple_agent import SimpleAgent
from memory.fifo_memory import FIFOMemory
from memory.utility_weighted_memory import UtilityWeightedMemory
from memory.similarity_memory import SimilarityOnlyMemory


def run_retention(memory_class, label):
    memory = memory_class(capacity=20)
    agent = SimpleAgent(memory)

    high_impact = [f"API_KEY_{i}=SECRET" for i in range(5)]
    low_impact = [f"noise message {i}" for i in range(95)]

    retention = []

    # Insert high-impact first
    for fact in high_impact:
        agent.observe(fact, impact=1.0)

    # Gradually add noise and test recall
    for i, noise in enumerate(low_impact):
        agent.observe(noise, impact=0.1)

        recalled = 0
        for fact in high_impact:
            key = fact.split("=")[0]
            if agent.ask(key):
                recalled += 1

        retention.append(recalled / len(high_impact))

    return retention


if __name__ == "__main__":
    fifo_curve = run_retention(FIFOMemory, "FIFO")
    sim_curve = run_retention(SimilarityOnlyMemory, "Similarity")
    uwe_curve = run_retention(UtilityWeightedMemory, "Utility-Weighted")

    plt.figure(figsize=(8, 5))
    plt.plot(fifo_curve, label="FIFO")
    plt.plot(sim_curve, label="Similarity-Only")
    plt.plot(uwe_curve, label="Utility-Weighted")
    plt.xlabel("Number of Interactions")
    plt.ylabel("High-Impact Memory Recall")
    plt.title("Retention Under Memory Pressure")
    plt.legend()
    plt.tight_layout()
    plt.show()
