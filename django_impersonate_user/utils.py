from logging import getLogger
from typing import TypeVar

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest

logger = getLogger(__name__)
U = TypeVar("U", bound=AbstractUser)
PERMISSION_NAME: str = "impersonate"


def auto_generate_permission() -> Permission:
    """
    Generates a permission object for impersonating users.

    This function retrieves the content type for the user model using `get_for_model`
    from the `ContentType` model. It then creates or retrieves a permission object
    with the name "impersonate", the specified content type, and the codename
    "impersonate" using `get_or_create` from the `Permission` model.

    Returns:
        Permission: The generated permission object.

    """
    content_type = ContentType.objects.get_for_model(get_user_model())
    permission, _ = Permission.objects.get_or_create(
        name=PERMISSION_NAME,
        content_type=content_type,
        codename=PERMISSION_NAME,
    )
    return permission


def impersonate_user(user: U, request: HttpRequest, auto_permission=True) -> U:
    """
    Utility function to change the user object
    to impersonate another user based on a cookie.
    Can be applied on `.authenticate()` method of django backend.
    If user id not found will fail to impersonate user,
    will log the error and return the real user.

    Args:
        user (U): The original user object.
        request (HttpRequest): The HTTP request object.
        auto_permission (bool, optional): Whether to automatically
            generate the permission for impersonation. Defaults to True.

    Returns:
        User: The impersonated user object.

    Raises:
        DoesNotExist: If the impersonated user does not exist.
        MultipleObjectsReturned: If multiple users with the same ID are found.
        Exception: If an error occurs while impersonating the user.
    """
    if auto_permission:
        auto_generate_permission()

    user_class: U = get_user_model()
    permission: str = f"{user_class._meta.app_label}.impersonate"
    user_id = request.COOKIES.get("LOGIN_AS")

    if user_id and (user.has_perm(permission) or user.is_superuser):
        try:
            user = user_class.objects.get(id=user_id)
        except user_class.DoesNotExist:
            pass  # no need to log an error
        except user_class.MultipleObjectsReturned:  # pragma: no cover
            user = user_class.objects.filter(id=user_id).first()
        except Exception as error:  # pragma: no cover
            logger.error(f"Impersonate user failed. Error: {error}")
    return user
