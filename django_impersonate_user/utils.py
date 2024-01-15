from django.contrib.auth.models import AbstractUser
from typing import TypeVar, Union
from logging import getLogger

from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


logger = getLogger(__name__)
U = TypeVar("U", bound=AbstractUser)

EXCLUDE_PATHS = ["/admin/"]


def impersonate_user(user: U, request: HttpRequest, auto_permission=True) -> U:
    """
    utils to change user object to the impersonate other user by its cookie.
    can be applied on `.authenticate()` method of django backend.
    if user id not found will fail to impersonate user, will log the error and return the real user
    """
    if auto_permission:
        auto_generate_permission()
    user_class = get_user_model()
    if user.has_perm(f"{user_class._meta.label}.impersonate") or user.is_superuser:
        user_id = request.COOKIES.get("LOGIN_AS")
        try:
            user = user.__class__.objects.get(id=user_id)
        except Exception as e:
            logger.error(e)
    return user


def auto_generate_permission():
    content_type = ContentType.objects.get_for_model(get_user_model())
    permission, is_created = Permission.objects.get_or_create(
        name="impersonate", content_type=content_type, codename="impersonate"
    )
    return permission
