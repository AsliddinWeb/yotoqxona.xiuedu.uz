from .base import *
from decouple import config

CSRF_TRUSTED_ORIGINS = ["https://yotoqxona.xiuedu.uz", "https://www.yotoqxona.xiuedu.uz"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', default=5432),
    }
}
