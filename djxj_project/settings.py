"""
Django settings for djxj_project project.

Generated by 'django-admin startproject' using Django 2.2.0
Links updated for Django 3.0

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.contrib.messages import constants as messages

import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")


# Determine if this is a production environment
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# See resulting modifications the at end of this file
PRODUCTION = (os.environ.get("PRODUCTION", default="True")).lower().strip() == "true"


# Debug mode
# See modifications at the end of this file
DEBUG = (os.environ.get("DEBUG", default="False")).lower().strip() == "true"
if PRODUCTION:
    DEBUG = False


# See modifications to this setting at end of this file
ALLOWED_HOSTS = []


# Applications
# See modification to this setting at end of this file

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # whitenoise needs to precede staticfiles
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
    # Third-party
    "allauth",
    "allauth.account",
    "crispy_forms",
    # Local
    "users.apps.UsersConfig",
    "pages.apps.PagesConfig",
]


# Middleware. See modification to this setting at end of this file

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "djxj_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djxj_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# Database url can be retrieved from Dokku, etc.
DATABASES = {"default": dj_database_url.config(conn_max_age=600)}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Crispy forms settings
CRISPY_TEMPLATE_PACK = "bootstrap4"


# Custom user model
AUTH_USER_MODEL = "users.CustomUser"


# Django-Allauth config
# See also the conditional settings at the end of this file
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

ACCOUNT_SESSION_REMEMBER = None  # None means user chooses
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = False  # False means username derived from email
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


# Make message tags consistent with Bootstrap alert classes
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}


# Change settings based on environment type
if PRODUCTION:
    ALLOWED_HOSTS = [os.environ.get("EXTERNAL_HOST_NAME")]
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1"])

    # Improve security: most of these settings require https
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 2592000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Account adapter to accept no new users
    ACCOUNT_ADAPTER = "users.adapters.NoNewUsersAccountAdapter"

if DEBUG:
    # Debug is true if production is false
    DEBUG = True

    # Allowed hosts
    # SECURITY WARNING: don't run with wildcard hosts in production!
    ALLOWED_HOSTS = ["*"]

    # Django debug toolbar
    INSTALLED_APPS.append("debug_toolbar")
    # add toolbar middleware after commonMiddleware
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # Enable internal ips for django-debug-toolbar
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
