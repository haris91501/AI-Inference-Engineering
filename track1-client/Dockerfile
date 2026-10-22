FROM python:3.14.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_CACHE_DIR=/app/cache \
    HF_HOME=/app/cache/huggingface \
    TORCH_HOME=/app/cache/torch

WORKDIR /app

# Healthcheck aur debugging ke liye curl install karte hain
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system appuser && \
    useradd --system --gid appuser --create-home appuser

COPY requirements.txt requirements-server.txt ./

RUN python -m pip install --no-cache-dir \
    -r requirements.txt \
    -r requirements-server.txt

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY tests/fake_stream_server.py ./fake_stream_server.py

RUN python -m pip install --no-cache-dir --no-deps .

# logs aur model cache dono directories ke permissions appuser ko assign karte hain
RUN mkdir -p /app/logs /app/cache && \
    chown -R appuser:appuser /app

USER appuser

VOLUME ["/app/cache"]

EXPOSE 8765

# Container health probe: check karta hai ke server alive hai ya nahi
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8765/health || exit 1

CMD ["python", "fake_stream_server.py"]
