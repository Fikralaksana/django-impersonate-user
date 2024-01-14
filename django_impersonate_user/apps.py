from django.apps import AppConfig


class ImpersonateUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_impersonate_user"
    label = "impersonate"

    def ready(self) -> None:
        from django.contrib.auth.models import Permission

        Permission.objects.get_or_create(
            name="impersonate_user",
            content_type__name="global_permission",
            app_label=self.label,
            code_name="impersonate",
        )
