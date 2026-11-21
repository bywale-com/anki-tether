FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
        libatomic1 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY pipeline ./pipeline

RUN --mount=type=secret,id=pip_ca \
    if [ -f /run/secrets/pip_ca ]; then export PIP_CERT=/run/secrets/pip_ca; fi; \
    pip install --no-cache-dir ".[app]"

ENV ANKI_DATA_DIR=/data \
    ANKI_COLLECTION=/data/collection.anki2 \
    HOST=0.0.0.0 \
    PORT=8000 \
    SECURE_COOKIES=true \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Single worker: Anki collections are not safe for concurrent writers.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
