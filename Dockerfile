FROM python:3.12-slim-bookworm AS dependencies

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.2

WORKDIR /build

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./

RUN poetry export --only main --format=requirements.txt --without-hashes --output=requirements.txt \
    && pip wheel --wheel-dir /wheels -r requirements.txt


FROM python:3.12-slim-bookworm AS app-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN groupadd --gid 10001 wagtail \
    && useradd --uid 10001 --gid wagtail --create-home --shell /usr/sbin/nologin wagtail

WORKDIR /app

COPY --from=dependencies /wheels /wheels
RUN pip install /wheels/* \
    && rm -rf /wheels

COPY --chown=wagtail:wagtail sauna_landing/ /app/
RUN mkdir -p /app/static \
    && chown -R wagtail:wagtail /app


FROM app-base AS static-builder

# collectstatic does not contact PostgreSQL or MinIO, but settings validate that
# their required configuration is present.
RUN SECRET_KEY=build-only-secret \
    POSTGRES_DB=build \
    POSTGRES_USER=build \
    POSTGRES_PASSWORD=build \
    DB_HOST=build \
    MINIO_ROOT_USER=build \
    MINIO_ROOT_PASSWORD=build \
    python manage.py collectstatic --noinput


FROM app-base AS app

COPY --from=static-builder --chown=wagtail:wagtail /app/static/staticfiles.json /app/static/staticfiles.json

USER wagtail

CMD ["gunicorn", "sauna_landing.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]


FROM nginx:1.26-alpine AS nginx

RUN rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /var/cache/nginx

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=static-builder /app/static /app/static
