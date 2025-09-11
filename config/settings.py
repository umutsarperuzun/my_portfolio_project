# settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-hsqc*l&x0_-!2&#!dva8!q&pb=lxw3pml7q_ie*jt2zw^hcjrb")

# Production'da DEBUG False olacak
# DEBUG = os.environ.get("DEBUG", "False") == "True"
DEBUG=True

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    _hosts_env = os.environ.get("ALLOWED_HOSTS", "")
    ALLOWED_HOSTS = [h.strip() for h in _hosts_env.split(",") if h.strip()]
    if not ALLOWED_HOSTS:
        ALLOWED_HOSTS = ["umut-sarper-portfolio.onrender.com"]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio",
    "tailwind",
    "theme",
    "django_browser_reload",
]

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]
NPM_BIN_PATH = "C:/nodejs/npm.cmd"

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ EKLENDİ
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database (Render'da ileride PostgreSQL de bağlayabilirsin)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "portfolio" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ✅ Whitenoise için storage ayarı
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
