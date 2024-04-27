import os
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings.configure(
    SECRET_KEY="xxxxx",
    DEBUG=True,
    DATABASES={
        "default": {
            "NAME": ":memory:",
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                os.path.join(
                    BASE_DIR,
                    "django-impersonate-user/django_impersonate_user/templates",
                ),
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        }
    ],
    STATIC_URL="/static/",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.admin",
        "django_impersonate_user",
    ],
)

django.setup()

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(["django_impersonate_user"])
if failures:
    sys.exit(failures)
