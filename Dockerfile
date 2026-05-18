FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SCRIPTS_DIR=/app/scripts

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /usr/sbin/nologin appuser

COPY pyproject.toml README.md ./
COPY telegram_script_bot ./telegram_script_bot

RUN pip install --no-cache-dir .

RUN mkdir -p /app/scripts && chown -R appuser:appuser /app

USER appuser

CMD ["telegram-script-bot"]
