#!/usr/bin/env python3
"""
CLI usage examples for TradingAgents.
Demonstrates how to programmatically use the CLI interface.
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import time

def run_cli_command(command_args, timeout=300):
    """Run a CLI command and return the result."""
    try:
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(Path(__file__).parent.parent)
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def test_cli_import():
    """Test that CLI can be imported."""
    print("🔍 Testing CLI import...")
    
    command = [sys.executable, "-c", "from cli.main import app; print('CLI import successful')"]
    returncode, stdout, stderr = run_cli_command(command, timeout=30)
    
    if returncode == 0:
        print("✅ CLI import successful")
        return True
    else:
        print(f"❌ CLI import failed: {stderr}")
        return False

def test_cli_help():
    """Test CLI help command."""
    print("🔍 Testing CLI help...")
    
    command = [sys.executable, "-m", "cli.main", "--help"]
    returncode, stdout, stderr = run_cli_command(command, timeout=30)
    
    if returncode == 0 and "TradingAgents CLI" in stdout:
        print("✅ CLI help working")
        print(f"Help output preview: {stdout[:200]}...")
        return True
    else:
        print(f"❌ CLI help failed: {stderr}")
        return False

def simulate_cli_analysis():
    """Simulate a CLI analysis (non-interactive)."""
    print("🚀 Simulating CLI analysis...")
    
    # Note: This would require modifying the CLI to accept command-line arguments
    # or creating a non-interactive mode. For now, we'll just test the import.
    
    script = """
import sys
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from config.development import MINIMAL_CONFIG

try:
    config = MINIMAL_CONFIG.copy()
    ta = TradingAgentsGraph(
        selected_analysts=["market"],
        debug=False,
        config=config
    )
    
    # Quick test
    print("CLI simulation: Framework initialized successfully")
    sys.exit(0)
except Exception as e:
    print(f"CLI simulation error: {e}")
    sys.exit(1)
"""
    
    command = [sys.executable, "-c", script]
    returncode, stdout, stderr = run_cli_command(command, timeout=60)
    
    if returncode == 0:
        print("✅ CLI simulation successful")
        print(f"Output: {stdout}")
        return True
    else:
        print(f"❌ CLI simulation failed: {stderr}")
        return False

def test_cli_with_environment():
    """Test CLI with environment variables."""
    print("🔍 Testing CLI with environment...")
    
    # Create a test environment
    env = os.environ.copy()
    env["TRADINGAGENTS_ENV"] = "development"
    
    script = """
import os
from tradingagents.default_config import DEFAULT_CONFIG
from config.development import DEVELOPMENT_CONFIG

print(f"Environment: {os.getenv('TRADINGAGENTS_ENV', 'not set')}")
print(f"Config loaded successfully")
"""
    
    command = [sys.executable, "-c", script]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=str(Path(__file__).parent.parent)
        )
        
        if result.returncode == 0:
            print("✅ CLI environment test successful")
            print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ CLI environment test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI environment test error: {e}")
        return False

def create_cli_script():
    """Create a sample CLI automation script."""
    print("📝 Creating CLI automation script...")
    
    script_content = '''#!/usr/bin/env python3
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
            f.write(f"Ticker: {ticker}\\n")
            f.write(f"Date: {date}\\n")
            f.write(f"Config: {config_name}\\n")
            f.write(f"Analysts: {analysts}\\n")
            f.write(f"Decision: {decision}\\n")
        
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
'''
    
    script_path = Path("examples/automated_analysis.py")
    script_path.parent.mkdir(exist_ok=True)
    
    with open(script_path, "w") as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(script_path, 0o755)
    
    print(f"✅ CLI automation script created: {script_path}")
    return script_path

def main():
    """Run all CLI examples."""
    print("🖥️  TradingAgents CLI Examples\\n")
    
    tests = [
        ("CLI Import", test_cli_import),
        ("CLI Help", test_cli_help),
        ("CLI Simulation", simulate_cli_analysis),
        ("CLI Environment", test_cli_with_environment),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\\n{'='*50}")
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
    
    # Create automation script
    print(f"\\n{'='*50}")
    print("Creating CLI Scripts")
    print('='*50)
    
    try:
        script_path = create_cli_script()
        print(f"✅ Automation script created")
        passed += 1
        total += 1
    except Exception as e:
        print(f"❌ Script creation failed: {e}")
        total += 1
    
    print(f"\\n{'='*50}")
    print(f"SUMMARY: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All CLI tests passed!")
    else:
        print("⚠️  Some CLI tests failed.")

if __name__ == "__main__":
    main()