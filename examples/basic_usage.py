#!/usr/bin/env python3
"""
Basic usage examples for TradingAgents.
Demonstrates how to use the framework with different configurations.
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from config.development import DEVELOPMENT_CONFIG, MINIMAL_CONFIG
from config.production import PRODUCTION_CONFIG
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def basic_example():
    """Basic usage with default configuration."""
    print("🚀 Running basic example...")
    
    # Use development config for faster execution
    config = DEVELOPMENT_CONFIG.copy()
    
    # Initialize TradingAgents
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Run analysis
    ticker = "SPY"
    date = "2025-01-15"
    print(f"Analyzing {ticker} for {date}...")
    
    _, decision = ta.propagate(ticker, date)
    print(f"Decision: {decision}")
    
    return decision

def custom_analysts_example():
    """Example with custom analyst selection."""
    print("🎯 Running custom analysts example...")
    
    config = DEVELOPMENT_CONFIG.copy()
    
    # Select specific analysts
    selected_analysts = ["market", "news"]
    
    ta = TradingAgentsGraph(
        selected_analysts=selected_analysts,
        debug=True,
        config=config
    )
    
    ticker = "AAPL"
    date = "2025-01-15"
    print(f"Analyzing {ticker} with {selected_analysts} analysts...")
    
    _, decision = ta.propagate(ticker, date)
    print(f"Decision: {decision}")
    
    return decision

def minimal_example():
    """Minimal example for quick testing."""
    print("⚡ Running minimal example...")
    
    config = MINIMAL_CONFIG.copy()
    
    ta = TradingAgentsGraph(
        selected_analysts=["market"],  # Use only one analyst
        debug=True,
        config=config
    )
    
    ticker = "NVDA"
    date = "2025-01-15"
    print(f"Quick analysis of {ticker}...")
    
    _, decision = ta.propagate(ticker, date)
    print(f"Decision: {decision}")
    
    return decision

def multi_ticker_example():
    """Example analyzing multiple tickers."""
    print("📊 Running multi-ticker example...")
    
    config = MINIMAL_CONFIG.copy()
    tickers = ["SPY", "QQQ", "AAPL"]
    date = "2025-01-15"
    
    results = {}
    
    for ticker in tickers:
        print(f"\nAnalyzing {ticker}...")
        
        ta = TradingAgentsGraph(
            selected_analysts=["market"],
            debug=False,  # Reduce output for multiple runs
            config=config
        )
        
        try:
            _, decision = ta.propagate(ticker, date)
            results[ticker] = decision
            print(f"✅ {ticker}: {decision[:100]}...")
        except Exception as e:
            print(f"❌ {ticker}: Error - {e}")
            results[ticker] = f"Error: {e}"
    
    print("\n📈 Summary:")
    for ticker, decision in results.items():
        print(f"{ticker}: {decision[:50]}...")
    
    return results

def production_example():
    """Example with production configuration."""
    print("🏭 Running production example...")
    
    # Note: This will use more expensive models and take longer
    config = PRODUCTION_CONFIG.copy()
    
    ta = TradingAgentsGraph(
        selected_analysts=["market", "news", "fundamentals"],
        debug=True,
        config=config
    )
    
    ticker = "TSLA"
    date = "2025-01-15"
    print(f"Production-level analysis of {ticker}...")
    
    _, decision = ta.propagate(ticker, date)
    print(f"Decision: {decision}")
    
    return decision

def comparison_example():
    """Compare results from different configurations."""
    print("🔍 Running comparison example...")
    
    ticker = "MSFT"
    date = "2025-01-15"
    
    configs = {
        "Minimal": MINIMAL_CONFIG,
        "Development": DEVELOPMENT_CONFIG,
    }
    
    results = {}
    
    for name, config in configs.items():
        print(f"\n🔬 Testing {name} configuration...")
        
        ta = TradingAgentsGraph(
            selected_analysts=["market"],
            debug=False,
            config=config.copy()
        )
        
        try:
            _, decision = ta.propagate(ticker, date)
            results[name] = decision
            print(f"✅ {name}: {decision[:100]}...")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[name] = f"Error: {e}"
    
    print(f"\n📋 Comparison for {ticker}:")
    for config_name, decision in results.items():
        print(f"\n{config_name}:")
        print(f"  {decision[:200]}...")
    
    return results

def main():
    """Run all examples."""
    print("🎭 TradingAgents Usage Examples\n")
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Please set your API key.")
        return
    
    if not os.getenv("FINNHUB_API_KEY"):
        print("❌ FINNHUB_API_KEY not set. Please set your API key.")
        return
    
    examples = [
        ("Basic Usage", basic_example),
        ("Custom Analysts", custom_analysts_example),
        ("Minimal Example", minimal_example),
        ("Multi-Ticker", multi_ticker_example),
        ("Comparison", comparison_example),
        # ("Production", production_example),  # Uncomment for production testing
    ]
    
    for name, example_func in examples:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        try:
            result = example_func()
            print(f"✅ {name} completed successfully")
        except Exception as e:
            print(f"❌ {name} failed: {e}")
        
        print()

if __name__ == "__main__":
    main()