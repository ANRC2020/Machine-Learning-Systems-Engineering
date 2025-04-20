FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update \
    && apt-get install curl -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH=/root/.local/bin:${PATH}

RUN python -m venv ./venv

COPY pyproject.toml poetry.lock ./
RUN . /app/venv/bin/activate && poetry install --only main

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /app/venv /app/venv

ENV PATH=/app/venv/bin:${PATH}

COPY . .

# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl --fail http://localhost:8000/healthcheck || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
