from pathlib import Path

import dj_database_url
from decouple import Csv, config
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config("SECRET_KEY", default="django-insecure$kahraba.configs.local")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())


INSTALLED_APPS = [
    # 'jet.dashboard',
    # 'jet',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
# Apps
    'core',
    'cart',
    'coupons',
    'delivery',
    'order',
    'atributes',
    'business',
# third party
    'mptt',
    "django_mptt_admin",
    'django_cleanup.apps.CleanupConfig',
    'import_export',
    'tinymce',
    'django_filters',
    "django_htmx",
    "compressor",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"

INTERNAL_IPS = ["127.0.0.1"]

WSGI_APPLICATION = "config.wsgi.application"



# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]


# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.trees",
                "cart.context_processors.cart_context",
                "business.context_processors.infos",
                'django.template.context_processors.request',
            ],
        },
    },
]


# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config('NAME'),
#         'USER': config('USER'),
#         'PASSWORD': config('PASSWORD'),
#         'HOST': config('HOST'),
#         'PORT': config('PORT'),
#     }
# }

# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="fr-fr")

TIME_ZONE = config("TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "assets"

# STATICFILES_DIRS = [BASE_DIR / "assets"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    'compressor.finders.CompressorFinder',
)

# ==============================================================================
# DJANGO COMPRESSOR
# ==============================================================================

# COMPRESS_FILTERS = {'css': ['core.admin.PostCSSFilter']}

COMPRESS_ROOT = BASE_DIR / 'assets'

COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]

COMPRESS_OFFLINE = True
if not COMPRESS_ENABLED:
    COMPRESS_ENABLED = True
    COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
    COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

CART_SESSION_ID = 'cart'


BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'



# TINYMCE_JS_URL = os.path.join(STATIC_URL, "tinymce/tinymce.min.js")
# TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, "tinymce")

# ==============================================================================
# THIRD-PARTY SETTINGS
# ==============================================================================


# ==============================================================================
# FIRST-PARTY SETTINGS
# ==============================================================================

kahraba_ENVIRONMENT = config("kahraba_ENVIRONMENT", default="local")

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    SERVER_EMAIL = 'octopus.emailing@gmail.com'
    EMAIL_HOST_USER = 'octopus.emailing@gmail.com'
    EMAIL_HOST_PASSWORD = 'miyou0209'

    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False

    

# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True

# SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_SSL_REDIRECT = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SESSION_COOKIE_SECURE = True


sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)