from django import template
from django.contrib.auth.models import AbstractUser

register = template.Library()


def has_impersonate_perm(user: AbstractUser, arg):
    """Removes all values of arg from the given string"""
    return user.has_perm(f"{user._meta.label}.impersonate")
