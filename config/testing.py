"""
Testing configuration for TradingAgents.
Optimized for automated testing and CI/CD pipelines.
"""

import os
from tradingagents.default_config import DEFAULT_CONFIG

# Base testing configuration
TESTING_CONFIG = DEFAULT_CONFIG.copy()
TESTING_CONFIG.update({
    # LLM settings - use minimal models for testing
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",      # Fastest and cheapest
    "quick_think_llm": "gpt-4o-mini",     # Same for consistency
    "backend_url": "https://api.openai.com/v1",
    
    # Minimal rounds for speed
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 5,
    
    # Disable online tools for consistent testing
    "online_tools": False,
    
    # Testing directories
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./test_results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        "tradingagents/dataflows/data_cache/test",
    ),
})

# Mock configuration for unit tests (no API calls)
MOCK_CONFIG = TESTING_CONFIG.copy()
MOCK_CONFIG.update({
    "online_tools": False,
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    # Add mock LLM settings if needed
})

# Integration testing configuration
INTEGRATION_CONFIG = TESTING_CONFIG.copy()
INTEGRATION_CONFIG.update({
    "online_tools": True,  # Enable for integration tests
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
})

# Performance testing configuration
PERFORMANCE_CONFIG = TESTING_CONFIG.copy()
PERFORMANCE_CONFIG.update({
    "max_debate_rounds": 2,
    "max_risk_discuss_rounds": 2,
    "online_tools": True,
})

# Configuration for testing different LLM providers
ANTHROPIC_TEST_CONFIG = TESTING_CONFIG.copy()
ANTHROPIC_TEST_CONFIG.update({
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-haiku-20240307",
    "quick_think_llm": "claude-3-haiku-20240307",
})

GOOGLE_TEST_CONFIG = TESTING_CONFIG.copy()
GOOGLE_TEST_CONFIG.update({
    "llm_provider": "google",
    "deep_think_llm": "gemini-1.5-flash",
    "quick_think_llm": "gemini-1.5-flash",
})