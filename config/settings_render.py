import os

import dj_database_url

from .settings import *


# Render proporciona estos valores mediante variables de entorno.
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = [os.environ["RENDER_EXTERNAL_HOSTNAME"]]

# La aplicación publicada usará su propia base de datos PostgreSQL.
DATABASES = {
    "default": dj_database_url.parse(os.environ["DATABASE_URL"]),
}

# WhiteNoise permite servir los archivos estáticos en Render.
MIDDLEWARE = MIDDLEWARE.copy()
MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)
STATIC_ROOT = BASE_DIR / "staticfiles"