# TradingAgents Deployment Guide

## Overview

TradingAgents is a sophisticated multi-agent trading framework that uses LLM-powered agents to analyze markets, conduct research, make trading decisions, and manage risk. This guide provides comprehensive setup and deployment instructions.

## System Architecture

The framework follows a sequential multi-agent workflow:
1. **Analyst Team** → Market, Social, News, Fundamentals Analysis
2. **Research Team** → Bull/Bear debate and Research Manager decision
3. **Trading Team** → Trader formulates investment plan
4. **Risk Management** → Risk analysts debate and assess
5. **Portfolio Management** → Final trading decision

## Prerequisites

- Python 3.13 (recommended) or Python 3.10+
- Git
- OpenAI API key
- Finnhub API key (free tier supported)
- 4GB+ RAM recommended
- Internet connection for live data feeds

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# Create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Alternative with venv
  # On Windows: tradingagents-env\Scripts\activate
`python -m venv tradingagents-env
source tradingagents-env/bin/activate``

### 2. Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### 3. Set Environment Variables

```bash
# Set required API keys
export OPENAI_API_KEY="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"
export FINNHUB_API_KEY="d1ko19pr01qt8fopi30gd1ko19pr01qt8fopi310"

# On Windows
set OPENAI_API_KEY=your-openai-api-key-here
set FINNHUB_API_KEY=your-finnhub-api-key-here
```

### 4. Quick Test

```bash
# Test CLI interface
python -m cli.main

# Test Python API
python main.py
```

## Configuration

### Default Configuration

The framework uses `tradingagents/default_config.py` for configuration. Key settings:

```python
DEFAULT_CONFIG = {
    # LLM Settings
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",        # Cost-effective for development
    "quick_think_llm": "gpt-4o-mini",   # Fast responses
    "backend_url": "https://api.openai.com/v1",
    
    # Debate Settings
    "max_debate_rounds": 1,             # Increase for deeper analysis
    "max_risk_discuss_rounds": 1,
    
    # Data Settings
    "online_tools": True,               # Enable live data feeds
}
```

### Custom Configuration

Create a custom configuration for your needs:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o"  # More powerful model
config["max_debate_rounds"] = 3       # Deeper analysis
config["online_tools"] = True         # Live data

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)
```

## Usage

### CLI Interface

```bash
# Interactive CLI with guided setup
python -m cli.main

# The CLI will guide you through:
# 1. Ticker selection (default: SPY)
# 2. Analysis date
# 3. Analyst team selection
# 4. Research depth
# 5. LLM provider selection
# 6. Model selection
```

### Python API

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Basic usage
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate("AAPL", "2025-01-15")
print(decision)

# With custom analysts
ta = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals"],
    debug=True,
    config=DEFAULT_CONFIG.copy()
)
_, decision = ta.propagate("NVDA", "2025-01-15")
print(decision)
```

### Advanced Usage

```python
# Multiple LLM providers
config = DEFAULT_CONFIG.copy()

# OpenAI
config["llm_provider"] = "openai"
config["backend_url"] = "https://api.openai.com/v1"

# Anthropic
config["llm_provider"] = "anthropic"
config["backend_url"] = "https://api.anthropic.com"

# Google
config["llm_provider"] = "google"
config["backend_url"] = "https://generativelanguage.googleapis.com/v1"

# Custom OpenAI-compatible endpoint
config["llm_provider"] = "openai"
config["backend_url"] = "https://your-custom-endpoint.com/v1"
```

## Testing and Validation

### Basic Validation

```bash
# Test API connections
python -c "
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
print('Setup successful!')
"
```

### Example Test Run

```bash
# Run analysis for SPY
python -c "
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate('SPY', '2025-01-15')
print('Decision:', decision)
"
```

## Deployment Options

### Local Development

```bash
# Activate environment
conda activate tradingagents

# Run with development settings
python -m cli.main
```

### Production Deployment

```bash
# Use production configuration
export TRADINGAGENTS_ENV=production
export OPENAI_API_KEY=$PROD_OPENAI_KEY
export FINNHUB_API_KEY=$PROD_FINNHUB_KEY

# Run with production settings
python -m cli.main
```

### Docker Deployment

```bash
# Build image
docker build -t tradingagents .

# Run container
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -e FINNHUB_API_KEY=$FINNHUB_API_KEY tradingagents

# Or use docker-compose
docker-compose up
```

## Performance Optimization

### Cost Optimization

```python
# Use cost-effective models for development
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-3.5-turbo"
config["max_debate_rounds"] = 1
```

### Performance Tuning

```python
# Optimize for speed
config = DEFAULT_CONFIG.copy()
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1
config["online_tools"] = False  # Use cached data
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   # Verify API keys are set
   echo $OPENAI_API_KEY
   echo $FINNHUB_API_KEY
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Memory Issues**
   ```bash
   # Reduce debate rounds
   config["max_debate_rounds"] = 1
   ```

4. **Network Issues**
   ```bash
   # Test API connectivity
   curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
   ```

### Debug Mode

```python
# Enable debug mode for detailed logs
ta = TradingAgentsGraph(debug=True, config=config)
```

## Security Considerations

### API Key Management

```bash
# Never commit API keys to version control
# Use environment variables or secure vaults
export OPENAI_API_KEY="your-key-here"

# Or use .env file (not committed)
echo "OPENAI_API_KEY=your-key-here" > .env
echo "FINNHUB_API_KEY=your-key-here" >> .env
```

### Production Security

- Use secure secret management (AWS Secrets Manager, Azure Key Vault, etc.)
- Implement proper access controls
- Monitor API usage and costs
- Enable logging for audit trails

## Monitoring and Logging

### Result Storage

Results are automatically saved to:
- `./results/{ticker}/{date}/reports/` - Individual reports
- `./results/{ticker}/{date}/message_tool.log` - Full execution log

### Custom Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use in your code
ta = TradingAgentsGraph(debug=True, config=config)
logger.info("Starting analysis...")
```

## API Reference

### TradingAgentsGraph

Main class for the trading framework.

```python
class TradingAgentsGraph:
    def __init__(self, selected_analysts=None, debug=False, config=None):
        """
        Args:
            selected_analysts: List of analyst types ["market", "social", "news", "fundamentals"]
            debug: Enable debug mode
            config: Configuration dictionary
        """
    
    def propagate(self, ticker: str, date: str) -> Tuple[Any, str]:
        """
        Run analysis for a ticker on a specific date.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL", "SPY")
            date: Analysis date in YYYY-MM-DD format
            
        Returns:
            Tuple of (state, decision)
        """
```

### Configuration Options

```python
DEFAULT_CONFIG = {
    "llm_provider": "openai",           # "openai", "anthropic", "google"
    "deep_think_llm": "o4-mini",        # Model for deep analysis
    "quick_think_llm": "gpt-4o-mini",   # Model for quick responses
    "backend_url": "https://api.openai.com/v1",
    "max_debate_rounds": 1,             # Research team debate rounds
    "max_risk_discuss_rounds": 1,       # Risk team discussion rounds
    "online_tools": True,               # Enable live data feeds
    "results_dir": "./results",         # Output directory
}
```

## Support and Community

- **GitHub**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **Discord**: [TradingResearch Community](https://discord.com/invite/hk9PGKShPK)
- **Paper**: [arXiv:2412.20138](https://arxiv.org/abs/2412.20138)
- **Website**: [Tauric Research](https://tauric.ai/)

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Disclaimer

TradingAgents is designed for research purposes. Trading performance may vary based on many factors including model selection, market conditions, and data quality. This framework is not intended as financial, investment, or trading advice.