from django.apps import AppConfig


class ImpersonateUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_impersonate_user"
    label = "impersonate"

    def ready(self) -> None:
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(get_user_model())
        Permission.objects.get_or_create(
            name="impersonate_user",
            content_type=content_type,
            codename="impersonate",
        )
