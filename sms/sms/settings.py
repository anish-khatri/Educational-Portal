import os
from pathlib import Path
from django.contrib.messages import constants as messages
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-ea)tuq8179e_y8w+!q&f9&9tkjh^shv$7h@%xbn1^*9o_4nc!7'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'dashboard.apps.DashboardConfig',
    'student.apps.StudentConfig',
    'schools.apps.SchoolsConfig',
    'applications.apps.ApplicationsConfig',
    'auth.apps.AuthConfig',
    'models.apps.ModelsConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.auth_middleware.AuthMiddleware',
]

ROOT_URLCONF = 'sms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sms.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sms',
        'USER': 'postgres',
        'PASSWORD': 'asdf',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


env = environ.Env()

environ.Env.read_env()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('MAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('MAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('MAIL_USERNAME')
EMAIL_HOST_PASSWORD = env('MAIL_PASSWORD')
DEFAULT_FROM_EMAIL = env('MAIL_FROM', default='MeroGym')