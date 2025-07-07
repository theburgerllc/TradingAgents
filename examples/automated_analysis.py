#!/usr/bin/env python3
"""
Automated CLI usage script for TradingAgents.
This script demonstrates how to automate TradingAgents analysis.
"""

import os
import sys
from pathlib import Path
from tradingagents.graph.trading_graph import TradingAgentsGraph
from config.development import DEVELOPMENT_CONFIG, MINIMAL_CONFIG

def automated_analysis(ticker, date, config_name="development"):
    """Run automated analysis for a ticker."""
    print(f"🤖 Running automated analysis for {ticker} on {date}")
    
    # Select configuration
    if config_name == "minimal":
        config = MINIMAL_CONFIG.copy()
        analysts = ["market"]
    else:
        config = DEVELOPMENT_CONFIG.copy()
        analysts = ["market", "news"]
    
    # Initialize framework
    ta = TradingAgentsGraph(
        selected_analysts=analysts,
        debug=False,
        config=config
    )
    
    # Run analysis
    try:
        _, decision = ta.propagate(ticker, date)
        
        # Save results
        results_dir = Path("results") / "automated" / ticker
        results_dir.mkdir(parents=True, exist_ok=True)
        
        with open(results_dir / f"{date}_decision.txt", "w") as f:
            f.write(f"Ticker: {ticker}\n")
            f.write(f"Date: {date}\n")
            f.write(f"Config: {config_name}\n")
            f.write(f"Analysts: {analysts}\n")
            f.write(f"Decision: {decision}\n")
        
        print(f"✅ Analysis complete. Results saved to {results_dir}")
        return decision
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

def main():
    """Main automation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated TradingAgents Analysis")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--date", default="2025-01-15", help="Analysis date")
    parser.add_argument("--config", default="development", 
                       choices=["development", "minimal"],
                       help="Configuration to use")
    
    args = parser.parse_args()
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        sys.exit(1)
    
    # Run analysis
    result = automated_analysis(args.ticker, args.date, args.config)
    
    if result:
        print(f"📊 Decision: {result[:100]}...")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
