from django.apps import AppConfig


class ImpersonateUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_impersonate_user"
    label = "impersonate"
