# experiments/simulate_tasks.py

import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.fifo_memory import FIFOMemory
from memory.utility_weighted_memory import UtilityWeightedMemory
from agent.simple_agent import SimpleAgent


def run_experiment(memory_class, label):
    memory = memory_class(capacity=20)
    agent = SimpleAgent(memory)

    high_impact_facts = [f"API_KEY_{i}=SECRET" for i in range(5)]
    low_impact_facts = [f"Random chit-chat {i}" for i in range(95)]

    # Insert memories
    for fact in high_impact_facts:
        agent.observe(fact, impact=1.0)

    for fact in low_impact_facts:
        agent.observe(fact, impact=0.1)

    # Query high-impact facts
    recalled = 0
    for fact in high_impact_facts:
        key = fact.split("=")[0]
        if agent.ask(key):
            recalled += 1

    print(f"[{label}] Recall: {recalled}/{len(high_impact_facts)}")


if __name__ == "__main__":
    run_experiment(FIFOMemory, "FIFO")
    run_experiment(UtilityWeightedMemory, "Utility-Weighted")
