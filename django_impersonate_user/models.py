from django.db import models
from django.contrib.auth.models import Permission


# Create your models here.
class ImpersonateSupport(Permission):
    class Meta:
        proxy = True
