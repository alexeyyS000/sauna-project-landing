# Sauna rental landing

Wagtail CMS landing page served by Gunicorn and Nginx, with PostgreSQL and
MinIO for media storage.

## Run with Docker

1. Create the local configuration and replace every `change-me` value:

   ```sh
   cp .env.example .env
   ```

   If a value contains `$`, enclose the complete value in single quotes. This
   prevents Docker Compose from expanding it as an environment variable.

2. Start the production-shaped stack:

   ```sh
   docker compose up --build -d
   ```

   The landing is available on port 80. The MinIO console is bound only to
   `127.0.0.1:9001`.

3. To expose PostgreSQL while developing locally, add the separate development
   overlay:

   ```sh
   docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
   ```

The `migrate` container applies migrations and creates the configured Django
superuser on first run. It is intentionally a one-off service; the web app
starts only after it succeeds.

## Configuration

All deployment settings come from `.env`; `.env.example` documents the full
set. Important production values are `SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS`, `WAGTAILADMIN_BASE_URL`, and the MinIO
credentials. Set the `DJANGO_SECURE_*` values only when HTTPS terminates at
this Nginx container, or a trusted upstream proxy forwards the original HTTPS
scheme.

`HOST` is the public host (and optional port) used to build media and Wagtail
URLs. It is not used as an Nginx routing restriction, so changing domains does
not require rebuilding the Nginx image.

## Initial database backup

`backups/initial.sql` is a local PostgreSQL snapshot. When `postgres-data` is
new or empty, the official Postgres image imports it automatically during its
first initialization. Existing database volumes are never overwritten. The
backup is ignored by Git because it contains application data.
