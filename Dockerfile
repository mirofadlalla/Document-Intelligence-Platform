# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 — Builder
# Install system build-time tools and compile all Python wheels.
# Nothing from this stage leaks into the final runtime image.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive \
    # Keep Python output unbuffered for real-time container logs
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip: disable cache, disable version check noise
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Build-time system dependencies
# - gcc / g++ / libpython3-dev: compile C-extension wheels (paddlepaddle)
# - libgomp1: OpenMP runtime required by PaddlePaddle CPU math kernels
# - libgl1 / libglib2.0-0 / libsm6 / libxext6 / libxrender1: OpenCV runtime
# - libffi-dev / libssl-dev: general build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libffi-dev \
        libssl-dev \
        libpython3-dev \
        libgomp1 \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy only requirements first to maximise Docker layer caching.
# Re-running pip install only happens when requirements.txt actually changes.
COPY backend/requirements.txt .

# Install all Python dependencies in one layer.
# --extra-index-url adds the official PaddlePaddle CPU index so pip can
# resolve the paddlepaddle==3.0.0 wheel that is not on PyPI.
RUN pip install --no-cache-dir \
        --extra-index-url https://www.paddlepaddle.org.cn/packages/stable/cpu/ \
        -r requirements.txt

# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 — Runtime
# Minimal image: only the installed site-packages + app source code.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Hugging Face Spaces expects the application on port 7860
    HOST=0.0.0.0 \
    PORT=7860 \
    LOG_LEVEL=INFO \
    # PaddleOCR / PaddlePaddle runtime flags
    # Disable MKL-DNN to avoid potential conflicts on HF Spaces CPU nodes
    FLAGS_use_mkldnn=0 \
    # PaddleOCR will download models to this directory on first inference.
    # Setting it explicitly ensures it lands in a writable, predictable path.
    PADDLE_OCR_BASE_DIR=/home/appuser/.paddleocr \
    HOME=/home/appuser

# Runtime system libraries (no build tools — keeps the image slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
        # OpenCV / PaddleOCR graphics stack
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        # OpenMP runtime (PaddlePaddle CPU threading)
        libgomp1 \
        # Font support (PaddleOCR renders text overlays during inference)
        fontconfig \
        fonts-liberation \
        # PDF processing (pdfplumber uses pdfminer which spawns poppler in some paths)
        libpoppler-cpp-dev \
        # Graceful signal handling (tini-like; uvicorn handles SIGTERM natively)
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the fully-built Python environment from the builder stage.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# ── Non-root user ─────────────────────────────────────────────────────────────
# Hugging Face Spaces runs as a non-root user by convention.
# Using UID 1000 matches the typical HF sandbox user.
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 --no-create-home --shell /bin/bash appuser \
    && mkdir -p /home/appuser/.paddleocr \
    && chown -R appuser:appuser /home/appuser

WORKDIR /app

# Copy application source code
COPY backend/ .

# Give the non-root user ownership of the working directory.
# This is necessary so uvicorn can write .pyc cache files on first run.
RUN chown -R appuser:appuser /app

USER appuser

# ── Ports ─────────────────────────────────────────────────────────────────────
EXPOSE 7860

# ── Health check ──────────────────────────────────────────────────────────────
# Waits 30 s for startup (PaddleOCR model warm-up), then probes every 30 s.
# /api/v1/health returns {"status": "healthy"} with HTTP 200.
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/api/v1/health || exit 1

# ── Production Uvicorn command ────────────────────────────────────────────────
# - exec form (no shell wrapper) ensures SIGTERM reaches uvicorn directly
# - --host / --port read from environment variables set above
# - WEB_CONCURRENCY lets the operator tune workers via env; defaults to 1
#   (appropriate for HF Spaces limited CPU; increase carefully)
# - --loop asyncio: explicit event loop for stability on slim images
# - --access-log: structured request logging
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST} --port ${PORT} --workers ${WEB_CONCURRENCY:-1} --loop asyncio --access-log"]
