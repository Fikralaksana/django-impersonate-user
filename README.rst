============
django-impersonate-user
============

django-impersonate-user is a Django app to give ability to some user
with permission to login as other user (impersonate)

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_impersonate_user" to your INSTALLED_APPS setting like this above `"django.contrib.admin"` ::

    INSTALLED_APPS = [
        ...,
        "django_polls",
        "django.contrib.admin",
    ]

2. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.