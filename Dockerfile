FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
        libatomic1 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY pipeline ./pipeline

RUN pip install --no-cache-dir . "anki==25.9.4"

ENV ANKI_DATA_DIR=/data \
    ANKI_COLLECTION=/data/collection.anki2 \
    HOST=0.0.0.0 \
    PORT=8000 \
    SECURE_COOKIES=true \
    PYTHONUNBUFFERED=1

EXPOSE 8000
VOLUME ["/data"]

# Single worker: Anki collections are not safe for concurrent writers.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
