
FROM python:3.9


RUN useradd wagtail


EXPOSE 8000


ENV PYTHONUNBUFFERED=1 \
    PORT=8000


RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
#    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*


RUN pip install "gunicorn==20.0.4"


ENV POETRY_VERSION=1.8.2
RUN pip install poetry==$POETRY_VERSION


COPY pyproject.toml .
COPY poetry.lock .


RUN poetry export --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt


WORKDIR /app


RUN chown wagtail:wagtail /app


COPY --chown=wagtail:wagtail sauna_landing .


RUN mkdir -p /app/static && chown wagtail:wagtail /app/static

RUN python manage.py collectstatic --noinput

USER wagtail
