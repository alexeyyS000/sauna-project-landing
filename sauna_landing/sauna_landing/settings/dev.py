from .base import *

import environ

env = environ.Env(DEBUG=(bool, True))
env.read_env(
    str(f"{os.path.abspath(os.path.join(BASE_DIR, '..'))}/.env.local"), overwrite=True
)

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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x8gl*us_cb8eq*aujzb^l-r&db7x4##7y4ibi@8gv1zjmjf**3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
