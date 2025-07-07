#!/usr/bin/env python3
"""
Test script to validate TradingAgents setup and API integration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_environment_variables():
    """Test that required environment variables are set."""
    print("🔍 Testing environment variables...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not set")
        return False
    elif len(openai_key) < 20:
        print(f"⚠️  OPENAI_API_KEY seems too short: {len(openai_key)} chars")
        return False
    else:
        print(f"✅ OPENAI_API_KEY set ({len(openai_key)} chars)")
    
    if not finnhub_key:
        print("❌ FINNHUB_API_KEY not set")
        return False
    elif len(finnhub_key) < 20:
        print(f"⚠️  FINNHUB_API_KEY seems too short: {len(finnhub_key)} chars")
        return False
    else:
        print(f"✅ FINNHUB_API_KEY set ({len(finnhub_key)} chars)")
    
    return True

def test_dependencies():
    """Test that required packages are installed."""
    print("\n🔍 Testing dependencies...")
    
    required_packages = [
        "langchain_openai",
        "langchain_experimental", 
        "langgraph",
        "pandas",
        "yfinance",
        "finnhub",
        "rich",
        "questionary",
        "typer"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_api_connections():
    """Test API connections."""
    print("\n🔍 Testing API connections...")
    
    # Test OpenAI API
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=10)
        response = llm.invoke("Hello")
        print("✅ OpenAI API connection successful")
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False
    
    # Test Finnhub API
    try:
        import finnhub
        finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
        # Test with a simple quote request
        quote = finnhub_client.quote("SPY")
        if quote and 'c' in quote:
            print("✅ Finnhub API connection successful")
        else:
            print("⚠️  Finnhub API responded but with unexpected format")
    except Exception as e:
        print(f"❌ Finnhub API connection failed: {e}")
        return False
    
    return True

def test_framework_import():
    """Test that TradingAgents framework can be imported."""
    print("\n🔍 Testing TradingAgents framework import...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        print("✅ TradingAgents framework imported successfully")
        
        # Test basic initialization
        config = DEFAULT_CONFIG.copy()
        config["deep_think_llm"] = "gpt-4o-mini"
        config["quick_think_llm"] = "gpt-4o-mini"
        
        ta = TradingAgentsGraph(debug=True, config=config)
        print("✅ TradingAgentsGraph initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ TradingAgents framework import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality with a simple analysis."""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Use minimal config for testing
        config = DEFAULT_CONFIG.copy()
        config["deep_think_llm"] = "gpt-4o-mini"
        config["quick_think_llm"] = "gpt-4o-mini"
        config["max_debate_rounds"] = 1
        config["max_risk_discuss_rounds"] = 1
        
        ta = TradingAgentsGraph(
            selected_analysts=["market"],  # Use only one analyst for faster testing
            debug=True,
            config=config
        )
        
        print("🚀 Running basic analysis (this may take a minute)...")
        _, decision = ta.propagate("SPY", "2025-01-15")
        
        if decision:
            print("✅ Basic analysis completed successfully")
            print(f"📊 Decision preview: {decision[:100]}...")
            return True
        else:
            print("⚠️  Analysis completed but no decision returned")
            return False
            
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 TradingAgents Setup Validation\n")
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Dependencies", test_dependencies),
        ("API Connections", test_api_connections),
        ("Framework Import", test_framework_import),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n{'='*50}")
    print(f"SUMMARY: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All tests passed! TradingAgents is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)