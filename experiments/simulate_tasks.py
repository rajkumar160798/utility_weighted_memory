# experiments/simulate_tasks.py

import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.fifo_memory import FIFOMemory
from memory.utility_weighted_memory import UtilityWeightedMemory
from memory.lru_memory import LRUMemory
from agent.simple_agent import SimpleAgent


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


def run_experiment(memory_class, label):
    memory = memory_class(capacity=20)
    agent = SimpleAgent(memory)

    # Use realistic business data
    high_impact_facts = high_impact_templates
    low_impact_facts = [f"{random.choice(low_impact_templates)} [{i}]" for i in range(95)]

    # Insert memories
    for fact in high_impact_facts:
        agent.observe(fact, impact=1.0)

    for fact in low_impact_facts:
        agent.observe(fact, impact=0.1)

    # Query high-impact facts by keywords
    recalled = 0
    queries = ["Database", "Config", "Compliance", "Security", "Billing"]
    for query in queries:
        if agent.ask(query):
            recalled += 1

    print(f"[{label}] Recall: {recalled}/{len(queries)}")


if __name__ == "__main__":
    run_experiment(FIFOMemory, "FIFO")
    run_experiment(LRUMemory, "LRU")
    run_experiment(UtilityWeightedMemory, "Utility-Weighted")
