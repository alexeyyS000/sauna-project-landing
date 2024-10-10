FROM python:3.11 as build

WORKDIR /app

ENV POETRY_VERSION=1.8.3

RUN pip install poetry==$POETRY_VERSION

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export --format=requirements.txt > requirements.txt

RUN pip install -r requirements.txt

COPY sauna_landing .
COPY .env .

RUN python manage.py collectstatic

FROM nginx:1.19.2-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
COPY --from=build app/static /app/static