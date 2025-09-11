# Multi-stage build for optimized Font Identifier app (Production)
# ==============================================================

# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies (production)
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt --timeout 300

# Stage 2: Runtime image
FROM python:3.11-slim as runtime

# Set non-interactive environment
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    TERM=xterm

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user first
RUN useradd --create-home --shell /bin/bash --uid 1001 appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV=/opt/venv

# Set optimized environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false

# PyTorch optimizations
ENV TORCH_HOME=/app/torch_cache \
    PYTORCH_ENABLE_MPS_FALLBACK=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1

# Prevent GUI applications
ENV DISPLAY=:99 \
    MPLBACKEND=Agg

# App-specific environment variables
ENV STREAMLIT_WATCHER_IGNORE_ERRORS=true \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none \
    STREAMLIT_WATCHER_IGNORE_MODULES=torch \
    STREAMLIT_WATCH_SYSTEM_PYTHON=false

# Create application directories
RUN mkdir -p /app/recordings /app/config /app/static /app/backend/recordings /app/torch_cache /app/data && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application files (exclude unnecessary files via .dockerignore)
COPY --chown=appuser:appuser . .

# Create essential files if they don't exist
RUN touch /app/model.pth /app/app_users.db && \
    mkdir -p /app/data && \
    echo "Arial\nHelvetica\nTimes New Roman\nCalibri\nVerdana\nGeorgia\nComic Sans MS\nTrebuchet MS\nImpact\nPalatino" > /app/data/fontlist.txt && \
    # Create startup script (always use main.py which is the full app now) \
    echo '#!/bin/bash' > /app/start_app.sh && \
    echo 'echo "Starting Font Identifier (production)"' >> /app/start_app.sh && \
    echo 'exec python -m streamlit run "main.py" "$@"' >> /app/start_app.sh && \
    chmod +x /app/start_app.sh

# Expose port
EXPOSE 8501

# Health check with comprehensive fallback
HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health 2>/dev/null || \
        curl -f http://localhost:8501/ 2>/dev/null || \
        python -c "import requests; requests.get('http://localhost:8501', timeout=10)" || \
        exit 1

# Startup command (production)
CMD ["/app/start_app.sh", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false", \
     "--browser.gatherUsageStats=false"]
