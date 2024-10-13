migrate:
	sudo docker compose --profile migrate run --rm migrations

createsuperuser:
	sudo docker compose run --rm app python manage.py createsuperuser --noinput


up:
    -include .env

    ENV_CONF = -f docker-compose.yml

    ifeq (${ENV},prod)
        ENV_CONF = -f docker-compose.yml
    endif

    ifeq (${ENV},dev)
        ENV_CONF = -f docker-compose.yml -f docker-compose.dev.yml
    endif

    ifeq (${ENV},local)
        ENV_CONF = -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.local.yml
    endif