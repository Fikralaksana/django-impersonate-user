from django.contrib.auth.models import AbstractUser
from typing import TypeVar, Union
from logging import getLogger

from django.http import HttpRequest
from django.apps import apps

logger = getLogger(__name__)
U = TypeVar("U", bound=AbstractUser)

EXCLUDE_PATHS = ["/admin/"]


def impersonate_user(user: U, request: HttpRequest) -> U:
    """
    utils to change user object to the impersonate other user by its cookie.
    can be applied on `.authenticate()` method of django backend.
    if user id not found will fail to impersonate user, will log the error and return the real user
    """
    if user.has_perm("impersonate.impersonate_user") or user.is_superuser:
        user_id = request.COOKIES.get("LOGIN_AS")
        try:
            user = user.__class__.objects.get(id=user_id)
        except Exception as e:
            logger.error(e)
    return user
