# Utility-Weighted Memory

A comparative study of memory management strategies for AI agents.

## Overview

This project implements and compares three different memory eviction strategies for an agent system:

1. **FIFO Memory** - First-In-First-Out eviction. Forgets memories in the order they were added, regardless of importance.

2. **Utility-Weighted Memory** - Intelligent eviction based on a scoring function that combines:
   - **Frequency**: How often a memory has been accessed
   - **Impact**: The importance/impact level of the memory
   - **Temporal Decay**: Recent memories are valued more than old ones
   
3. **Similarity-Only Memory** - Eviction based on semantic similarity scores between memories and queries.

## Project Structure

```
memory/
├── base_memory.py              # Abstract base class for memory implementations
├── fifo_memory.py              # FIFO eviction strategy
├── utility_weighted_memory.py  # Utility-weighted scoring strategy
└── similarity_memory.py        # Similarity-based retrieval
agent/
└── simple_agent.py             # Simple agent that observes facts and queries memory
experiments/
├── simulate_tasks.py           # Compares memory strategies on synthetic tasks
└── retention_curve.py          # Plots retention curves for different strategies
results/                        # Output directory for experiment results
```

## How It Works

### Memory Operations

- **Add**: Insert a new memory item into the memory system
- **Retrieve**: Query the memory and retrieve relevant items
- **Stats**: Get statistics about memory usage

### Eviction Strategy (Utility-Weighted)

When memory reaches capacity, the item with the lowest utility score is removed:

```
Score = (w_freq * access_count + w_impact * impact) * exp(-decay_lambda * age)
```

Where:
- `w_freq` & `w_impact` are configurable weights
- `decay_lambda` controls how quickly memories age

## Running Experiments

Run the task simulation:
```bash
python experiments/simulate_tasks.py
```

Generate retention curves (requires matplotlib):
```bash
python experiments/retention_curve.py
```

## Key Insights

- **Utility-Weighted Memory** retains high-impact information better than FIFO
- The weighting parameters can be tuned for different use cases
- Temporal decay ensures important recent information isn't forgotten
