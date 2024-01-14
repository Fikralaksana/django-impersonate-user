from django.db import models


# Create your models here.
class DjangoImpersonateUser(models.Model):
    class Meta:
        proxy = True
