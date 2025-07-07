#!/usr/bin/env python3
"""
Quick start script for TradingAgents deployment validation.
This script provides a simple way to test the complete setup.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def welcome_message():
    """Display welcome message."""
    print("🎭 TradingAgents Quick Start")
    print("=" * 50)
    print("Welcome to the TradingAgents multi-agent trading framework!")
    print("This script will help you validate your deployment setup.\n")

def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment setup...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major != 3 or python_version.minor < 10:
        print("⚠️  Warning: Python 3.10+ recommended")
    else:
        print("✅ Python version OK")
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    if openai_key and len(openai_key) > 20:
        print("✅ OPENAI_API_KEY set")
    else:
        print("❌ OPENAI_API_KEY not properly set")
        return False
    
    if finnhub_key and len(finnhub_key) > 20:
        print("✅ FINNHUB_API_KEY set")
    else:
        print("❌ FINNHUB_API_KEY not properly set")
        return False
    
    return True

def test_basic_import():
    """Test basic framework import."""
    print("\n🧪 Testing framework import...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        print("✅ Framework import successful")
        return True
    except ImportError as e:
        print(f"❌ Framework import failed: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_quick_test():
    """Run a quick analysis test."""
    print("\n🚀 Running quick analysis test...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from config.development import MINIMAL_CONFIG
        
        # Use minimal config for speed
        config = MINIMAL_CONFIG.copy()
        config["max_debate_rounds"] = 1
        config["max_risk_discuss_rounds"] = 1
        
        ta = TradingAgentsGraph(
            selected_analysts=["market"],  # Single analyst for speed
            debug=False,
            config=config
        )
        
        print("📊 Analyzing SPY (this may take 30-60 seconds)...")
        _, decision = ta.propagate("SPY", "2025-01-15")
        
        if decision:
            print("✅ Quick test successful!")
            print(f"Decision preview: {decision[:150]}...")
            return True
        else:
            print("⚠️  Test completed but no decision returned")
            return False
            
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for users."""
    print("\n🎯 Next Steps:")
    print("=" * 50)
    print("1. CLI Interface:")
    print("   python -m cli.main")
    print("\n2. Python API Examples:")
    print("   python examples/basic_usage.py")
    print("\n3. Docker Deployment:")
    print("   docker build -t tradingagents .")
    print("   docker-compose up")
    print("\n4. Documentation:")
    print("   - See DEPLOYMENT_GUIDE.md for complete setup")
    print("   - See DEPLOYMENT_SUMMARY.md for overview")
    print("   - Check examples/ directory for usage patterns")

def main():
    """Main quick start function."""
    welcome_message()
    
    # Run validation steps
    steps = [
        ("Environment Check", check_environment),
        ("Framework Import", test_basic_import),
        ("Quick Analysis", run_quick_test),
    ]
    
    passed = 0
    total = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        print(f"Step: {step_name}")
        print('='*50)
        
        try:
            if step_func():
                passed += 1
                print(f"✅ {step_name} PASSED")
            else:
                print(f"❌ {step_name} FAILED")
                break  # Stop on first failure for quick start
        except Exception as e:
            print(f"❌ {step_name} ERROR: {e}")
            break
    
    print(f"\n{'='*50}")
    print(f"QUICK START RESULTS: {passed}/{total} steps completed")
    print('='*50)
    
    if passed == total:
        print("🎉 TradingAgents is ready to use!")
        show_next_steps()
    else:
        print("⚠️  Setup incomplete. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure API keys are set correctly")
        print("2. Run: pip install -r requirements.txt")
        print("3. Check DEPLOYMENT_GUIDE.md for detailed setup")

if __name__ == "__main__":
    main()