# ---- Stage 1 : builder (installe les dépendances et entraîne les modèles) ----
FROM python:3.11-slim AS builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --retries 10 --default-timeout 100 -r requirements.txt
COPY train.py .
RUN MODEL_DIR=/models python train.py

# ---- Stage 2 : runtime ----
FROM python:3.11-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /models /models
ENV PATH="/opt/venv/bin:$PATH" \
    MODEL_DIR=/models \
    PYTHONUNBUFFERED=1
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]