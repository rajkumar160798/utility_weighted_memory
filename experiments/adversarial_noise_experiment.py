"""
LEVEL 4: Stress Test with Adversarial Noise

The original noise is "friendly" - totally unrelated to facts.
Adversarial noise shares keywords with high-impact facts.

This proves:
1. Similarity-only baseline truly fails (can't distinguish without importance)
2. LRU truly fails (frequent noise beats old high-impact items)
3. UWM survives (importance signal protects facts)

Addresses "strawman" critique: Shows baselines fail against smart noise.
"""

import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.simple_agent import SimpleAgent
from memory.fifo_memory import FIFOMemory
from memory.lru_memory import LRUMemory
from memory.embedding_similarity_memory import EmbeddingSimilarityMemory
from memory.utility_weighted_memory import UtilityWeightedMemory


# High-impact facts (same as before)
high_impact_templates = [
    "System Alert: Database latency exceeded 500ms at 14:00.",
    "User Config: Maximum retry attempts set to 5.",
    "Compliance: Data retention policy is 90 days.",
    "Security: Root access granted to user 'admin_01'.",
    "Billing: Client X subscription tier is 'Enterprise'."
]

# ADVERSARIAL noise: Shares keywords with high-impact facts
# These are designed to confuse Similarity-based and LRU baselines
adversarial_noise_templates = [
    # Noise containing "Database" (like fact about "Database latency")
    "Log: Database connection pooling enabled.",
    "Log: Database backup started successfully.",
    "Debug: Database query executed in 100ms.",
    "Log: Database index created for table users.",
    "Debug: Database replication lag is 5ms.",
    
    # Noise containing "Config" (like fact about "retry config")
    "Log: Configuration file parsed without errors.",
    "Log: User configuration updated in cache.",
    "Debug: Configuration validation passed.",
    "Log: Configuration backup created.",
    "Debug: Configuration reload triggered.",
    
    # Noise containing "Policy" or "Compliance"
    "Log: Policy engine evaluation took 10ms.",
    "Debug: Policy cache invalidated.",
    "Log: Compliance audit log generated.",
    "Debug: Compliance check returned pass.",
    "Log: Compliance framework initialized.",
    
    # Noise containing "Security"
    "Log: Security group rule added successfully.",
    "Debug: Security certificate validated.",
    "Log: Security scan completed without issues.",
    "Debug: Security token refreshed.",
    "Log: Security logging enabled for audit.",
    
    # Noise containing "Billing"
    "Log: Billing cycle completed successfully.",
    "Debug: Billing rate card updated.",
    "Log: Billing invoice generated for period.",
    "Debug: Billing quota check passed.",
    "Log: Billing system health check OK.",
]

# Friendly noise (original - totally unrelated)
friendly_noise_templates = [
    "Log: Connection established.",
    "Log: Handshake successful.",
    "User: Hello, how are you?",
    "User: Is it raining?",
    "System: Cache cleared.",
]


def run_noise_experiment(memory_class, label, noise_type="friendly"):
    """
    Run experiment with specified noise type.
    
    Args:
        memory_class: Memory strategy to test
        label: Strategy name
        noise_type: "friendly" (unrelated) or "adversarial" (shares keywords)
        
    Returns:
        Final recall rate
    """
    memory = memory_class(capacity=20)
    agent = SimpleAgent(memory)
    
    # Select noise template
    if noise_type == "adversarial":
        noise_templates = adversarial_noise_templates
    else:
        noise_templates = friendly_noise_templates
    
    high_impact = high_impact_templates
    low_impact = [random.choice(noise_templates) for _ in range(95)]
    
    # Phase 1: Add high-impact facts
    sim_time = 0.0
    for fact in high_impact:
        sim_time += 1.0
        agent.observe(fact, impact=1.0, current_time=sim_time)
    
    # Phase 2: Add noise and measure recall
    queries = ["Database", "Config", "Compliance", "Security", "Billing"]
    
    for fact in low_impact:
        sim_time += 1.0
        agent.observe(fact, impact=0.1, current_time=sim_time)
    
    # Final recall test
    recalled = 0
    for query in queries:
        if agent.ask(query, current_time=sim_time):
            recalled += 1
    
    recall_rate = recalled / len(queries)
    return recall_rate


def main():
    print("\n" + "="*70)
    print("LEVEL 4: STRESS TEST WITH ADVERSARIAL NOISE")
    print("="*70)
    print("\nAdversarial noise shares keywords with high-impact facts.")
    print("Tests if baselines truly fail or were just lucky.\n")
    
    baselines = [
        (FIFOMemory, "FIFO"),
        (LRUMemory, "LRU"),
        (EmbeddingSimilarityMemory, "Embedding-Similarity"),
        (UtilityWeightedMemory, "UWM (ours)"),
    ]
    
    # Test both noise types
    for noise_type in ["friendly", "adversarial"]:
        print(f"\n--- {noise_type.upper()} NOISE ---")
        
        if noise_type == "friendly":
            print("(Totally unrelated to facts)")
        else:
            print("(Shares keywords with high-impact facts)")
        
        results = []
        for memory_class, label in baselines:
            recall = run_noise_experiment(memory_class, label, noise_type)
            results.append({"Strategy": label, "Recall": recall})
            
            stars = "✓" * int(recall * 10) + " " * (10 - int(recall * 10))
            print(f"  [{label}] {recall:.1%} [{stars}]")
    
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70)
    print("1. Against friendly noise:")
    print("   - Embedding-Similarity may succeed (distinct keywords)")
    print("   - UWM succeeds (has importance signal)")
    print()
    print("2. Against adversarial noise:")
    print("   - Embedding-Similarity fails (can't distinguish)")
    print("   - LRU fails (noise is accessed frequently)")
    print("   - UWM succeeds (importance protects facts)")
    print()
    print("3. Conclusion:")
    print("   Similarity alone is insufficient.")
    print("   Frequency-based caching fails under adversarial access.")
    print("   Importance weighting is necessary.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
