# TradingAgents Dockerfile
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./
COPY setup.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Create directories for data and results
RUN mkdir -p /app/results /app/data /app/logs

# Create non-root user
RUN useradd --create-home --shell /bin/bash tradingagents \
    && chown -R tradingagents:tradingagents /app

# Switch to non-root user
USER tradingagents

# Set default command to run CLI
CMD ["python", "-m", "cli.main"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph; print('healthy')" || exit 1

# Expose port for potential web interface
EXPOSE 8000

# Labels for metadata
LABEL org.opencontainers.image.title="TradingAgents" \
      org.opencontainers.image.description="Multi-Agents LLM Financial Trading Framework" \
      org.opencontainers.image.url="https://github.com/TauricResearch/TradingAgents" \
      org.opencontainers.image.source="https://github.com/TauricResearch/TradingAgents" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Tauric Research"