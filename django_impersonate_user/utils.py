from logging import getLogger
from typing import TypeVar

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest

logger = getLogger(__name__)
U = TypeVar("U", bound=AbstractUser)

EXCLUDE_PATHS = ["/admin/"]


def impersonate_user(user: U, request: HttpRequest, auto_permission=True) -> U:
    """
    utils to change user object to the impersonate other user by its cookie.
    can be applied on `.authenticate()` method of django backend.
    if user id not found will fail to impersonate user,
    will log the error and return the real user.
    """
    if auto_permission:
        auto_generate_permission()

    user_class: U = get_user_model()
    permission: str = f"{user_class._meta.app_label}.impersonate"

    if user.has_perm(permission) or user.is_superuser:
        user_id = request.COOKIES.get("LOGIN_AS")
        try:
            user = user_class.objects.get(id=user_id)
        except user_class.DoesNotExist:
            pass  # no need to log an error
        except user_class.MultipleObjectsReturned:
            user = user_class.objects.filter(id=user_id).first()
        except Exception as error:
            logger.error(f"Impersonate user failed. Error: {error}")
    return user


def auto_generate_permission() -> Permission:
    content_type = ContentType.objects.get_for_model(get_user_model())
    permission, _ = Permission.objects.get_or_create(
        name="impersonate",
        content_type=content_type,
        codename="impersonate",
    )
    return permission
