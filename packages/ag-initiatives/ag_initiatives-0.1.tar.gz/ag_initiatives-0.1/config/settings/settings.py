import os

from django.contrib import admin

import config.settings.sentry  # noqa
from config.admin import custom_admin_site
from config.settings import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = "=6nnyym8qyx*tb(xd80@hukpcrsuxp0$60a^)6u7s0ttc(4q#5"

DEBUG = os.environ.get("DEBUG", "False").lower() in ("on", "yes", "true", "t", "1")
DEBUG_TOOLBAR = os.environ.get("DEBUG_TOOLBAR", "False")

DEBUG_TIMER = os.environ.get("DEBUG_TIMER", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)

DISPLAY_TOKENS = os.environ.get("DISPLAY_TOKENS", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)

ADMIN_URL = os.environ.get("ADMIN_URL", "admin")

INITIATIVES_HIDE_USERNAME = os.environ.get("INITIATIVES_HIDE_USERNAME", "").split(";")

RECAPTCHA_ENABLED = os.environ.get("RECAPTCHA_ENABLED", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "")

SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)

USE_X_FORWARDED_HOST = os.environ.get("USE_X_FORWARDED_HOST", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATA_UPLOAD_MAX_NUMBER_FIELDS = os.environ.get("DATA_UPLOAD_MAX_NUMBER_FIELDS", 2048)

INVENTORY_STANDALONE = os.environ.get("INVENTORY_STANDALONE", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)

BONUS_PROGRAM = os.environ.get("BONUS_PROGRAM", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)

REGION_ID = os.environ.get("REGION_ID", 24)

POS_CLIENT_ID = os.environ.get(
    "POS_CLIENT_ID", "0bbb23fb-7502-4d5a-af3c-ae90fa10dcfb"
)
POS_ORGN = os.environ.get("POS_ORGN", "1022402674744")
POS_ENV = os.environ.get("POS_ENV", "TEST")
POS_BODY_PASSWORD = os.environ.get(
    "POS_BODY_PASSWORD", "aa8fbf4d-ee31-4ea2-8e35-7e8c6c43c76c"
)
POS_BASIC_AUTH_USERNAME = os.environ.get("POS_BASIC_AUTH_USERNAME", "sourceMap1")
POS_BASIC_AUTH_PASSWORD = os.environ.get("POS_BASIC_AUTH_PASSWORD", "sourceMap2")
POS_DEBUG = os.environ.get("POS_DEBUG", "False").lower() in (
    "on",
    "yes",
    "true",
    "t",
    "1",
)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.postgres",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_gis",
    "corsheaders",
    "nested_admin",
    "django_fsm",
    "des",
    "drf_yasg",
    "drf_excel",
    "embed_video",
    "django_summernote",
    "rangefilter",
    "adminsortable",
    "dal",
    "dal_select2",
    "import_export",
    "debug_toolbar",

    "modules.core",
    "modules.voting",
    "modules.initiatives",
    "modules.esia",
    "modules.appeals",
    "modules.ecology",
    "modules.map_works",
    "modules.plans",
    "modules.inventory",
    "modules.feedback",
    "modules.appeals_pos",
    "modules.subscriptions",
    "modules.integration",

]
AUTH_USER_MODEL = "core.User"

AUTHENTICATION_BACKENDS = [
    "modules.esia.auth_backend.EsiaAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "modules.core.middleware.ExternalSystemMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG_TOOLBAR:
    MIDDLEWARE.extend(
        [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]
    )

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
        "drf_excel.renderers.XLSXRenderer",
    ),
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

EMBED_VIDEO_BACKENDS = (
    "embed_video.backends.YoutubeBackend",
    "embed_video.backends.VimeoBackend",
    "embed_video.backends.SoundCloudBackend",
)

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
        "NAME": os.environ.get("POSTGRES_DB", "db_vote"),
        "USER": os.environ.get("POSTGRES_USER", "db_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "db_pwd"),
    },
}

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

LOGGING = logging.CONFIG

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Asia/Krasnoyarsk"

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILE_UPLOAD_PERMISSIONS = 0o644

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_files"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ORIGIN_ALLOW_ALL = True if DEBUG else False

EMAIL_BACKEND = "des.backends.ConfiguredEmailBackend"
FEEDBACK_RECEIVER_EMAIL = os.environ.get("FEEDBACK_RECEIVER_EMAIL", "")

X_FRAME_OPTIONS = "SAMEORIGIN"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "http://24ag-dev.cifra-k.ru")

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
    STATICFILES_DIRS = []

ADMIN_SITE = "AG.config.admin.CustomAdminSite"
admin.site = custom_admin_site
admin.sites.site = custom_admin_site
