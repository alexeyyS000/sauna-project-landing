from .base import *


import environ

env = environ.Env(DEBUG=(bool, False))
env.read_env(str(f"{os.path.abspath(os.path.join(BASE_DIR, '..'))}/.env"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "5432",
    }
}


try:
    from .local import *
except ImportError:
    pass
