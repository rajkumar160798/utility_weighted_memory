# experiments/retention_curve.py

import sys
import os
import random
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.simple_agent import SimpleAgent
from memory.fifo_memory import FIFOMemory
from memory.utility_weighted_memory import UtilityWeightedMemory
from memory.lru_memory import LRUMemory
from memory.similarity_memory import SimilarityOnlyMemory


# Realistic Data Generators
high_impact_templates = [
    "System Alert: Database latency exceeded 500ms at 14:00.",
    "User Config: Maximum retry attempts set to 5.",
    "Compliance: Data retention policy is 90 days.",
    "Security: Root access granted to user 'admin_01'.",
    "Billing: Client X subscription tier is 'Enterprise'."
]

low_impact_templates = [
    "Log: Connection established.",
    "Log: Handshake successful.",
    "User: Hello, how are you?",
    "User: Is it raining?",
    "System: Cache cleared.",
    "Debug: Variable x is null."
]


def run_retention(memory_class, label, w_freq=None, w_impact=None):
    if w_freq is not None and w_impact is not None and hasattr(memory_class, '__init__'):
        # Special handling for UtilityWeightedMemory with custom weights
        if memory_class == UtilityWeightedMemory:
            memory = memory_class(capacity=20, w_freq=w_freq, w_impact=w_impact)
        else:
            memory = memory_class(capacity=20)
    else:
        memory = memory_class(capacity=20)
    
    agent = SimpleAgent(memory)

    high_impact = high_impact_templates
    low_impact = [f"{random.choice(low_impact_templates)} [{i}]" for i in range(95)]

    retention = []

    # Insert high-impact first
    for fact in high_impact:
        agent.observe(fact, impact=1.0)

    # Gradually add noise and test recall
    queries = ["Database", "Config", "Compliance", "Security", "Billing"]
    for i, noise in enumerate(low_impact):
        agent.observe(noise, impact=0.1)

        recalled = 0
        for query in queries:
            if agent.ask(query):
                recalled += 1

        retention.append(recalled / len(queries))

    return retention


def run_sensitivity_sweep():
    """Test robustness across different w_impact weights."""
    impact_weights = [0.1, 0.3, 0.5, 0.7, 0.9]
    final_retentions = []

    for w_impact in impact_weights:
        w_freq = 1.0 - w_impact  # Complementary weight
        curve = run_retention(UtilityWeightedMemory, f"UWM (w_impact={w_impact})", 
                            w_freq=w_freq, w_impact=w_impact)
        final_retention = curve[-1]  # Get final retention score
        final_retentions.append(final_retention)
    
    print("\n=== Sensitivity Analysis ===")
    print("Impact Weight vs Final Retention:")
    for w, retention in zip(impact_weights, final_retentions):
        print(f"  w_impact={w:.1f}: {retention:.2%}")
    
    return impact_weights, final_retentions


if __name__ == "__main__":
    print("=== Retention Curves ===")
    fifo_curve = run_retention(FIFOMemory, "FIFO")
    lru_curve = run_retention(LRUMemory, "LRU")
    sim_curve = run_retention(SimilarityOnlyMemory, "Similarity")
    uwe_curve = run_retention(UtilityWeightedMemory, "Utility-Weighted")

    # Plot retention curves
    plt.figure(figsize=(10, 6))
    plt.plot(fifo_curve, label="FIFO", linewidth=2)
    plt.plot(lru_curve, label="LRU", linewidth=2)
    plt.plot(sim_curve, label="Similarity-Only", linewidth=2)
    plt.plot(uwe_curve, label="Utility-Weighted", linewidth=2)
    plt.xlabel("Number of Interactions")
    plt.ylabel("High-Impact Memory Recall")
    plt.title("Retention Under Memory Pressure (Enterprise System Logs)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("retention_curves.png")
    print("Retention curve saved to retention_curves.png")
    plt.show()
    
    # Run sensitivity analysis
    print("\n")
    impact_weights, final_retentions = run_sensitivity_sweep()
