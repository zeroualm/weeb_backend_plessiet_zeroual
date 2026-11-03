FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /app/data \
    && chown -R app:app /app \
    && chmod +x /app/docker-entrypoint.sh

USER app

ENV DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
    DJANGO_DB_PATH=/app/data/db.sqlite3 \
    DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173 \
    DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173 \
    DJANGO_SECURE_COOKIES=False \
    GUNICORN_WORKERS=3 \
    PORT=8000

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
