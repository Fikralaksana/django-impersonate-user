from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

from .utils import PERMISSION_NAME, auto_generate_permission, impersonate_user


class AutoGeneratePermissionTestCase(TestCase):
    def test_auto_generate_permission_return_type(self):
        permission = auto_generate_permission()
        self.assertIsInstance(permission, Permission)

    def test_auto_generate_permission_correct_data(self):
        permission = auto_generate_permission()
        content_type = ContentType.objects.get_for_model(get_user_model())
        self.assertEqual(permission.name, PERMISSION_NAME)
        self.assertEqual(permission.content_type, content_type)
        self.assertEqual(permission.codename, PERMISSION_NAME)


class ImpersonateUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username="superuser", password="testpassword"
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.request = self.factory.get("/")

    def test_impersonate_user_with_permission(self):
        # Test impersonating a user with permission
        permission = auto_generate_permission()
        assert Permission.objects.filter(name=permission.name).exists()

        user_id: int = 2
        self.request.COOKIES["LOGIN_AS"] = str(user_id)
        impersonate_user(self.user, self.request)
        self.assertEqual(self.user.id, user_id)

    def test_impersonate_user_without_permission(self):
        # Test impersonating a user without permission
        permissions = Permission.objects.filter(name=PERMISSION_NAME)
        if permissions.exists():
            permissions.delete()

        user_id: int = 2
        self.request.COOKIES["LOGIN_AS"] = str(user_id)
        impersonate_user(self.user, self.request)
        self.assertEqual(self.user.id, user_id)

    def test_impersonate_user_with_invalid_id(self):
        # Test impersonating a user with an invalid id
        user_id: str = "invalid"
        self.request.COOKIES["LOGIN_AS"] = user_id
        impersonate_user(self.user, self.request)
        self.assertNotEqual(self.user.id, user_id)

    def test_impersonate_user_with_does_not_exist_id(self):
        # Test impersonating a user with a non-existent id
        user_id: int = 999
        self.request.COOKIES["LOGIN_AS"] = str(user_id)
        impersonate_user(self.user, self.request)
        self.assertNotEqual(self.user.id, user_id)

    def test_impersonate_user_with_superuser(self):
        # Test impersonating a user with a superuser
        user_id: int = self.superuser.id
        self.request.COOKIES["LOGIN_AS"] = str(user_id)
        impersonate_user(self.superuser, self.request)
        self.assertEqual(self.superuser.id, user_id)
