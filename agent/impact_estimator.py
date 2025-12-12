"""
Automatic impact estimation without manual labeling.

Provides multiple strategies:
1. Rule-based: Keywords indicating importance (policy, security, alert, etc.)
2. TF-IDF based: Rarity of words
3. Random: Baseline (no signal)
"""

import re
from typing import Callable


class ImpactEstimator:
    """Estimates importance of text without manual labels."""
    
    @staticmethod
    def rule_based(text: str) -> float:
        """
        Keyword-based impact estimation.
        
        Returns:
            1.0 if contains critical keywords (policy, security, alert, error, critical)
            0.7 if contains config/setup keywords (config, limit, threshold, setting)
            0.3 if contains action keywords (update, change, create, delete)
            0.1 otherwise (generic logs, chat, debug)
        """
        text_lower = text.lower()
        
        # Critical keywords
        critical_keywords = [
            "policy", "security", "alert", "error", "critical", "compliance",
            "access", "permission", "fail", "failure", "breach", "unauthorized",
            "confidential", "secret", "credential", "password", "api.key"
        ]
        
        # Config keywords
        config_keywords = [
            "config", "setting", "limit", "threshold", "parameter",
            "quota", "tier", "retention", "rate", "timeout"
        ]
        
        # Action keywords
        action_keywords = [
            "update", "change", "modify", "create", "delete", "remove",
            "grant", "revoke", "enable", "disable"
        ]
        
        # Check for critical
        if any(kw in text_lower for kw in critical_keywords):
            return 1.0
        
        # Check for config
        if any(kw in text_lower for kw in config_keywords):
            return 0.7
        
        # Check for action
        if any(kw in text_lower for kw in action_keywords):
            return 0.3
        
        # Generic log
        return 0.1
    
    @staticmethod
    def severity_based(text: str) -> float:
        """
        Estimate impact from log level severity patterns.
        
        Returns:
            1.0 for ERROR, CRITICAL, FATAL
            0.7 for WARNING
            0.3 for INFO
            0.1 for DEBUG
        """
        text_lower = text.lower()
        
        if any(x in text_lower for x in ["error", "critical", "fatal", "exception"]):
            return 1.0
        if "warning" in text_lower:
            return 0.7
        if "info" in text_lower:
            return 0.3
        
        return 0.1
    
    @staticmethod
    def tfidf_based(text: str, corpus_stats: dict = None) -> float:
        """
        Estimate impact from TF-IDF rarity.
        
        Rare words indicate importance.
        Common words (the, a, is, etc.) are noise.
        
        Args:
            text: Text to estimate
            corpus_stats: Precomputed corpus statistics (optional)
            
        Returns:
            Score 0.1 to 1.0 based on rarity
        """
        # Very basic: count unique tokens
        tokens = re.findall(r'\b\w+\b', text.lower())
        unique_tokens = len(set(tokens))
        total_tokens = len(tokens)
        
        if total_tokens == 0:
            return 0.1
        
        # Uniqueness ratio
        uniqueness = unique_tokens / total_tokens
        
        # Normalize to [0.1, 1.0] range
        # More unique tokens -> higher impact (less repetitive, more signal)
        impact = 0.1 + (uniqueness * 0.9)
        
        return min(1.0, impact)
    
    @staticmethod
    def random_impact(text: str = None) -> float:
        """
        Random impact (baseline - no signal).
        Used to show that manual/automatic labels are necessary.
        """
        import random
        return random.uniform(0.1, 1.0)
    
    @staticmethod
    def combined(text: str) -> float:
        """
        Combine multiple estimators with weights.
        """
        rule_score = ImpactEstimator.rule_based(text)
        severity_score = ImpactEstimator.severity_based(text)
        tfidf_score = ImpactEstimator.tfidf_based(text)
        
        # Weighted average: rules are strongest signal
        combined = (0.6 * rule_score + 
                   0.2 * severity_score + 
                   0.2 * tfidf_score)
        
        return combined


def get_estimator(estimator_name: str) -> Callable[[str], float]:
    """
    Factory function to get an impact estimator by name.
    
    Args:
        estimator_name: "rule", "severity", "tfidf", "random", or "combined"
        
    Returns:
        Function that estimates impact from text
    """
    estimators = {
        "rule": ImpactEstimator.rule_based,
        "severity": ImpactEstimator.severity_based,
        "tfidf": ImpactEstimator.tfidf_based,
        "random": ImpactEstimator.random_impact,
        "combined": ImpactEstimator.combined,
    }
    
    return estimators.get(estimator_name, ImpactEstimator.rule_based)
