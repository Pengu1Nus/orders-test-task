## ------------------------------- Build ------------------------------ ## 
FROM python:3.11-bookworm AS builder

RUN apt update && apt install --no-install-recommends -y \
        build-essential curl && \
    apt clean && rm -rf /var/lib/apt/lists/*



RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# COPY ./pyproject.toml .
# COPY ./poetry.lock .
# COPY ./README.md .
COPY . .

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi --without dev --verbose

## ------------------------------- Production ------------------------------ ##
FROM python:3.11-slim-bookworm AS production

EXPOSE 8000
WORKDIR /app

COPY ./run.sh ./run.sh
COPY /app src

RUN adduser \
        --disabled-password \
        --gecos "" \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x ./run.sh

COPY --from=builder /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

USER django-user
WORKDIR /app/src
CMD ["./run.sh"]
