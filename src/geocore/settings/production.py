from .base import *             # NOQA
from django.utils.translation import gettext_lazy as _

INSTALLED_APPS.extend([
    'home',
    'metadb',
])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

DEBUG = False

ALLOWED_HOSTS = ['']

TIME_ZONE = 'Asia/Novosibirsk'

STATIC_ROOT = '/var/www/static'