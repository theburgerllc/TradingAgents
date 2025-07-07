#!/usr/bin/env python3
"""
Docker deployment examples for TradingAgents.
Demonstrates various Docker deployment scenarios.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(command, timeout=300):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def build_docker_image():
    """Build the TradingAgents Docker image."""
    print("🐳 Building Docker image...")
    
    command = "docker build -t tradingagents:latest ."
    returncode, stdout, stderr = run_command(command, timeout=600)
    
    if returncode == 0:
        print("✅ Docker image built successfully")
        print(f"Build output: {stdout[-200:]}")  # Last 200 chars
        return True
    else:
        print(f"❌ Docker build failed: {stderr}")
        return False

def test_docker_image():
    """Test the Docker image."""
    print("🧪 Testing Docker image...")
    
    command = 'docker run --rm tradingagents:latest python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph; print(\'Docker test passed\')"'
    returncode, stdout, stderr = run_command(command, timeout=120)
    
    if returncode == 0:
        print("✅ Docker image test passed")
        print(f"Test output: {stdout}")
        return True
    else:
        print(f"❌ Docker image test failed: {stderr}")
        return False

def run_docker_container():
    """Run TradingAgents in a Docker container."""
    print("🚀 Running Docker container...")
    
    # Create a test command that doesn't require interactive input
    command = '''docker run --rm \
        -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
        -e FINNHUB_API_KEY="${FINNHUB_API_KEY}" \
        tradingagents:latest \
        python -c "
from tradingagents.graph.trading_graph import TradingAgentsGraph
from config.development import MINIMAL_CONFIG
import os

print('Testing TradingAgents in Docker...')
if not os.getenv('OPENAI_API_KEY'):
    print('Warning: OPENAI_API_KEY not set')
if not os.getenv('FINNHUB_API_KEY'):
    print('Warning: FINNHUB_API_KEY not set')

# Quick framework test
config = MINIMAL_CONFIG.copy()
ta = TradingAgentsGraph(debug=False, config=config)
print('TradingAgents framework initialized successfully in Docker!')
"'''
    
    returncode, stdout, stderr = run_command(command, timeout=180)
    
    if returncode == 0:
        print("✅ Docker container ran successfully")
        print(f"Container output: {stdout}")
        return True
    else:
        print(f"❌ Docker container failed: {stderr}")
        return False

def test_docker_compose():
    """Test Docker Compose setup."""
    print("🐳 Testing Docker Compose...")
    
    # First, try to validate the docker-compose file
    command = "docker-compose config"
    returncode, stdout, stderr = run_command(command, timeout=30)
    
    if returncode == 0:
        print("✅ Docker Compose configuration valid")
        print("Docker Compose services:")
        # Parse and show services
        for line in stdout.split('\n'):
            if line.strip().endswith(':') and not line.startswith(' '):
                service = line.strip().rstrip(':')
                if service != 'version' and service != 'services':
                    print(f"  - {service}")
        return True
    else:
        print(f"❌ Docker Compose configuration invalid: {stderr}")
        return False

def create_docker_run_script():
    """Create a convenient Docker run script."""
    print("📝 Creating Docker run script...")
    
    script_content = '''#!/bin/bash
# TradingAgents Docker Run Script

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo -e "${GREEN}🐳 TradingAgents Docker Runner${NC}"

# Check if API keys are set
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo -e "${RED}❌ OPENAI_API_KEY not set${NC}"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your-key-here'"
    exit 1
fi

if [[ -z "$FINNHUB_API_KEY" ]]; then
    echo -e "${RED}❌ FINNHUB_API_KEY not set${NC}"
    echo "Please set your Finnhub API key:"
    echo "export FINNHUB_API_KEY='your-key-here'"
    exit 1
fi

# Build image if it doesn't exist
if [[ "$(docker images -q tradingagents:latest 2> /dev/null)" == "" ]]; then
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    docker build -t tradingagents:latest .
fi

# Create results directory
mkdir -p ./results

# Run container
echo -e "${GREEN}🚀 Starting TradingAgents...${NC}"
docker run -it --rm \\
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \\
    -e FINNHUB_API_KEY="$FINNHUB_API_KEY" \\
    -v "$(pwd)/results:/app/results" \\
    tradingagents:latest \\
    "$@"

echo -e "${GREEN}✅ TradingAgents completed${NC}"
'''
    
    script_path = Path("run_docker.sh")
    
    with open(script_path, "w") as f:
        f.write(script_content)
    
    # Make executable
    import os
    os.chmod(script_path, 0o755)
    
    print(f"✅ Docker run script created: {script_path}")
    return script_path

def create_docker_compose_script():
    """Create a Docker Compose convenience script."""
    print("📝 Creating Docker Compose script...")
    
    script_content = '''#!/bin/bash
# TradingAgents Docker Compose Script

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

echo -e "${GREEN}🐳 TradingAgents Docker Compose Manager${NC}"

# Function to show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo "Commands:"
    echo "  up      - Start all services"
    echo "  down    - Stop all services"
    echo "  build   - Build images"
    echo "  logs    - Show logs"
    echo "  status  - Show service status"
    echo "  dev     - Start in development mode"
}

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose not found${NC}"
    echo "Please install Docker Compose"
    exit 1
fi

# Get command
COMMAND=${1:-help}

case $COMMAND in
    up)
        echo -e "${BLUE}🚀 Starting TradingAgents services...${NC}"
        docker-compose up -d
        echo -e "${GREEN}✅ Services started${NC}"
        docker-compose ps
        ;;
    down)
        echo -e "${YELLOW}🛑 Stopping TradingAgents services...${NC}"
        docker-compose down
        echo -e "${GREEN}✅ Services stopped${NC}"
        ;;
    build)
        echo -e "${BLUE}🔨 Building TradingAgents images...${NC}"
        docker-compose build
        echo -e "${GREEN}✅ Images built${NC}"
        ;;
    logs)
        echo -e "${BLUE}📋 Showing service logs...${NC}"
        docker-compose logs -f
        ;;
    status)
        echo -e "${BLUE}📊 Service status:${NC}"
        docker-compose ps
        ;;
    dev)
        echo -e "${BLUE}🛠️  Starting development environment...${NC}"
        docker-compose -f docker-compose.dev.yml up -d
        echo -e "${GREEN}✅ Development environment started${NC}"
        docker-compose -f docker-compose.dev.yml ps
        ;;
    help|*)
        show_usage
        ;;
esac
'''
    
    script_path = Path("docker-compose.sh")
    
    with open(script_path, "w") as f:
        f.write(script_content)
    
    # Make executable
    import os
    os.chmod(script_path, 0o755)
    
    print(f"✅ Docker Compose script created: {script_path}")
    return script_path

def main():
    """Run all Docker examples."""
    print("🐳 TradingAgents Docker Examples\n")
    
    # Check if Docker is available
    returncode, stdout, stderr = run_command("docker --version", timeout=10)
    if returncode != 0:
        print("❌ Docker not available. Please install Docker.")
        return
    
    print(f"Docker version: {stdout.strip()}")
    
    # Check if docker-compose is available
    returncode, stdout, stderr = run_command("docker-compose --version", timeout=10)
    if returncode == 0:
        print(f"Docker Compose version: {stdout.strip()}")
        compose_available = True
    else:
        print("⚠️  Docker Compose not available")
        compose_available = False
    
    print()
    
    tests = [
        ("Build Docker Image", build_docker_image),
        ("Test Docker Image", test_docker_image),
        ("Run Docker Container", run_docker_container),
    ]
    
    if compose_available:
        tests.append(("Test Docker Compose", test_docker_compose))
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
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
        
        print()
    
    # Create convenience scripts
    print("📝 Creating convenience scripts...")
    try:
        create_docker_run_script()
        create_docker_compose_script()
        print("✅ Scripts created successfully")
    except Exception as e:
        print(f"❌ Script creation failed: {e}")
    
    print(f"\n{'='*50}")
    print(f"SUMMARY: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All Docker tests passed!")
        print("\nNext steps:")
        print("1. Run: ./run_docker.sh")
        print("2. Or use: ./docker-compose.sh up")
    else:
        print("⚠️  Some Docker tests failed.")

if __name__ == "__main__":
    main()