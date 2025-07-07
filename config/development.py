"""
Development configuration for TradingAgents.
Optimized for fast development and testing with cost-effective models.
"""

import os
from tradingagents.default_config import DEFAULT_CONFIG

# Development configuration
DEVELOPMENT_CONFIG = DEFAULT_CONFIG.copy()
DEVELOPMENT_CONFIG.update({
    # LLM settings - use cost-effective models
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",      # Cost-effective for development
    "quick_think_llm": "gpt-4o-mini",     # Fast and cheap
    "backend_url": "https://api.openai.com/v1",
    
    # Reduce rounds for faster development
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 10,
    
    # Enable online tools for real data
    "online_tools": True,
    
    # Development directories
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results/dev"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        "tradingagents/dataflows/data_cache/dev",
    ),
})

# Alternative configuration for testing different providers
ANTHROPIC_DEV_CONFIG = DEVELOPMENT_CONFIG.copy()
ANTHROPIC_DEV_CONFIG.update({
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-haiku-20240307",
    "quick_think_llm": "claude-3-haiku-20240307",
    "backend_url": "https://api.anthropic.com",
})

GOOGLE_DEV_CONFIG = DEVELOPMENT_CONFIG.copy()
GOOGLE_DEV_CONFIG.update({
    "llm_provider": "google",
    "deep_think_llm": "gemini-1.5-flash",
    "quick_think_llm": "gemini-1.5-flash",
    "backend_url": "https://generativelanguage.googleapis.com/v1",
})

# Configuration for minimal testing (single analyst)
MINIMAL_CONFIG = DEVELOPMENT_CONFIG.copy()
MINIMAL_CONFIG.update({
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 5,
    "online_tools": False,  # Use cached data for speed
})

# Configuration for cost optimization
COST_OPTIMIZED_CONFIG = DEVELOPMENT_CONFIG.copy()
COST_OPTIMIZED_CONFIG.update({
    "deep_think_llm": "gpt-4o-mini",
    "quick_think_llm": "gpt-4o-mini",
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "online_tools": False,  # Use cached data to reduce API calls
})