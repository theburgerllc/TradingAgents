"""
Configuration module for TradingAgents.
Provides environment-specific configurations for development, production, and testing.
"""

from .development import (
    DEVELOPMENT_CONFIG,
    ANTHROPIC_DEV_CONFIG,
    GOOGLE_DEV_CONFIG,
    MINIMAL_CONFIG,
    COST_OPTIMIZED_CONFIG,
)
from .production import (
    PRODUCTION_CONFIG,
    HIGH_PERFORMANCE_CONFIG,
    BALANCED_PROD_CONFIG,
    MULTI_MODEL_CONFIG,
)
from .testing import (
    TESTING_CONFIG,
    MOCK_CONFIG,
    INTEGRATION_CONFIG,
    PERFORMANCE_CONFIG,
    ANTHROPIC_TEST_CONFIG,
    GOOGLE_TEST_CONFIG,
)

__all__ = [
    # Development configurations
    "DEVELOPMENT_CONFIG",
    "ANTHROPIC_DEV_CONFIG",
    "GOOGLE_DEV_CONFIG",
    "MINIMAL_CONFIG",
    "COST_OPTIMIZED_CONFIG",
    
    # Production configurations
    "PRODUCTION_CONFIG",
    "HIGH_PERFORMANCE_CONFIG",
    "BALANCED_PROD_CONFIG",
    "MULTI_MODEL_CONFIG",
    
    # Testing configurations
    "TESTING_CONFIG",
    "MOCK_CONFIG",
    "INTEGRATION_CONFIG",
    "PERFORMANCE_CONFIG",
    "ANTHROPIC_TEST_CONFIG",
    "GOOGLE_TEST_CONFIG",
]

def get_config(environment="development"):
    """
    Get configuration based on environment.
    
    Args:
        environment: Environment name ("development", "production", "testing")
        
    Returns:
        Configuration dictionary
    """
    if environment.lower() == "development":
        return DEVELOPMENT_CONFIG
    elif environment.lower() == "production":
        return PRODUCTION_CONFIG
    elif environment.lower() == "testing":
        return TESTING_CONFIG
    else:
        raise ValueError(f"Unknown environment: {environment}")

def get_provider_config(provider="openai", environment="development"):
    """
    Get configuration for a specific LLM provider and environment.
    
    Args:
        provider: LLM provider ("openai", "anthropic", "google")
        environment: Environment name ("development", "testing")
        
    Returns:
        Configuration dictionary
    """
    if environment.lower() == "development":
        if provider.lower() == "anthropic":
            return ANTHROPIC_DEV_CONFIG
        elif provider.lower() == "google":
            return GOOGLE_DEV_CONFIG
        else:
            return DEVELOPMENT_CONFIG
    elif environment.lower() == "testing":
        if provider.lower() == "anthropic":
            return ANTHROPIC_TEST_CONFIG
        elif provider.lower() == "google":
            return GOOGLE_TEST_CONFIG
        else:
            return TESTING_CONFIG
    else:
        return get_config(environment)