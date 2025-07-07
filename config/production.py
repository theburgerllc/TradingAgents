"""
Production configuration for TradingAgents.
Optimized for performance and comprehensive analysis.
"""

import os
from tradingagents.default_config import DEFAULT_CONFIG

# Production configuration
PRODUCTION_CONFIG = DEFAULT_CONFIG.copy()
PRODUCTION_CONFIG.update({
    # LLM settings - use high-performance models
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",          # Use o1 for deep thinking
    "quick_think_llm": "gpt-4o",          # Use GPT-4o for quick responses
    "backend_url": "https://api.openai.com/v1",
    
    # Comprehensive analysis settings
    "max_debate_rounds": 3,               # More thorough debate
    "max_risk_discuss_rounds": 2,         # Detailed risk analysis
    "max_recur_limit": 100,
    
    # Enable all features
    "online_tools": True,
    
    # Production directories
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "/app/results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        "tradingagents/dataflows/data_cache/prod",
    ),
})

# High-performance configuration for critical decisions
HIGH_PERFORMANCE_CONFIG = PRODUCTION_CONFIG.copy()
HIGH_PERFORMANCE_CONFIG.update({
    "deep_think_llm": "o4-mini",          # Best reasoning model
    "quick_think_llm": "gpt-4o",          # Fast but powerful
    "max_debate_rounds": 5,               # Extensive debate
    "max_risk_discuss_rounds": 3,         # Thorough risk assessment
})

# Balanced production configuration
BALANCED_PROD_CONFIG = PRODUCTION_CONFIG.copy()
BALANCED_PROD_CONFIG.update({
    "deep_think_llm": "gpt-4o",
    "quick_think_llm": "gpt-4o-mini",
    "max_debate_rounds": 2,
    "max_risk_discuss_rounds": 2,
})

# Multi-model production configuration
MULTI_MODEL_CONFIG = PRODUCTION_CONFIG.copy()
MULTI_MODEL_CONFIG.update({
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",
    "quick_think_llm": "gpt-4o",
    "max_debate_rounds": 2,
    "max_risk_discuss_rounds": 2,
    # Could be extended to use different models for different agents
})