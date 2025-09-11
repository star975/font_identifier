# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false

# PyTorch optimization for better model loading
ENV TORCH_HOME=/app/torch_cache
ENV PYTORCH_ENABLE_MPS_FALLBACK=1
ENV OMP_NUM_THREADS=1

# Prevent browser windows from opening
ENV DISPLAY=:99
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
COPY requirements-docker.txt .

# Install Python dependencies in virtual environment
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir wheel setuptools && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements-docker.txt || \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p recordings config static backend/recordings torch_cache && \
    chmod 755 recordings config static backend/recordings torch_cache

# Create virtual environment and switch to non-root user
RUN python -m venv /opt/venv && \
    useradd --create-home --shell /bin/bash --uid 1001 appuser && \
    chown -R appuser:appuser /app /opt/venv

# Switch to non-root user
USER appuser

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv

# Expose port
EXPOSE 8501

# Health check (install curl for health checks)
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* && apt-get clean
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || curl -f http://localhost:8501 || exit 1

# Run the application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
