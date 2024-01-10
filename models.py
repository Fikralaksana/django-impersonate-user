from django.db import models


# Create your models here.
class ImpersonateSupport(models.Model):
    class Meta:
        default_permissions = ()  # disable defaults add, delete, view, change perms
        permissions = (
            (
                "impersonate_user",
                "impersonate or login as other user for admin diagnostic purposes",
            ),
        )
