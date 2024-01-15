from django import template
from django.contrib.auth.models import AbstractUser

register = template.Library()


def has_impersonate_perm(user: AbstractUser):
    """Removes all values of arg from the given string"""
    return user.has_perm(f"{user._meta.app_label}.impersonate")


register.filter("has_impersonate_perm", has_impersonate_perm)
