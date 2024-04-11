"""
Tests for the DB models created in the app.
"""
from parameterized import parameterized

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class TestDBModels(TestCase):
    """Tests for DB models"""

    def test_create_normal_user(self) -> None:
        """Tests that we can create a normal user"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
            'username': 'tester'
        }

        user = User.objects.create_user(**payload)

        self.assertIsInstance(user, User)
        self.assertEqual(user.email, payload.get('email'))
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_fail_create_user_without_email(self) -> None:
        """Tests that we fail to create a new user without supplying email.
        """
        payload = {
            'email': '',
            'password': 'testing123#',
            'username': 'tester'
        }

        with self.assertRaises(ValueError):
            User.objects.create_user(**payload)

        payload = {
            'password': 'testing123#',
            'username': 'tester'
        }

        with self.assertRaises(TypeError):
            User.objects.create_user(**payload)

    def test_create_superuser(self) -> None:
        """Tests that we can create a new superuser"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
            'username': 'tester'
        }

        user = User.objects.create_superuser(**payload)

        self.assertIsInstance(user, User)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)

    def test_user_email_must_be_unique(self) -> None:
        """Tests that a user email must be unique"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
            'username': 'tester'
        }
        User.objects.create_user(**payload)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**payload)

    @parameterized.expand([
        ('test@example.com', 'test@example.com'),
        ('test@EXAMPLE.com', 'test@example.com'),
        ('test@EXamPle.com', 'test@example.com'),
        ('Test@EXAMPle.com', 'Test@example.com'),
    ])
    def test_user_email_normalized(self, inputed_email: str,
                                   expected: str) -> None:
        """Tests that user's email is always normalized"""
        payload = {
            'email': inputed_email,
            'password': 'testing123#',
            'username': 'tester'
        }
        user = User.objects.create_user(**payload)

        self.assertEqual(user.email, expected)
