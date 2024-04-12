"""
Tests for the user authentication API endpoints
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from user import serializers

User = get_user_model()
CREATE_URL = reverse('user:create')
LOGIN_URL = reverse('user:login')
ME_URL = reverse('user:me')


def create_user(**params):
    """Creates a new user to be used for testing purposes."""
    payload = {
        'email': 'test@example.com',
        'password': 'testing123#',
        'username': 'test_user',
    }
    payload.update(params)
    return User.objects.create_user(**payload)


class PublicUserAPITests(TestCase):
    """Public unauthenticated tests to user API endpoints"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_created_successfully(self) -> None:
        """Tests that user can be successfully created"""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
            'username': 'test_user'
        }
        res = self.client.post(CREATE_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload.get('email'))
        self.assertIsNotNone(user)
        self.assertEqual(user.username, payload.get('username'))
        self.assertTrue(user.check_password(payload.get('password')))

    def test_fail_create_user_without_email(self) -> None:
        """Tests that the user cannot be created without an email"""
        payload = {
            'password': 'testing123#',
            'username': 'test_user'
        }
        res = self.client.post(CREATE_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_user_with_nonunique_email(self) -> None:
        """Tests that the user cannot be created with an email that is not
        unique."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
            'username': 'test_user'
        }
        self.client.post(CREATE_URL, data=payload)
        res = self.client.post(CREATE_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_user_with_password_less_8_characters(self) -> None:
        """Tests that user cannot be created with password less than 8
        characters long."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing',
            'username': 'test_user'
        }
        res = self.client.post(CREATE_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_successfully(self) -> None:
        """Tests that the user can login successfully."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
        }
        create_user(**payload)
        res = self.client.post(LOGIN_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_fail_login_user_without_email(self) -> None:
        """Tests that the user fails to login without providing an email.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
        }
        create_user(**payload)
        payload.pop('email')
        res = self.client.post(LOGIN_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserAPITests(TestCase):
    """Private authenticated tests for requests to the user API."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_details_successfully(self):
        """Tests successful retrieval of user details."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = serializers.UserSerializer(self.user)
        self.assertEqual(res.data, serializer.data)

    def test_update_user_details_successfully(self):
        """Tests successful updation of user details."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123#',
            'username': 'update_user',
        }
        res = self.client.put(ME_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload.get('username'))

    def test_delete_user_details_successfully(self):
        """Tests successful deletion of user details."""
        res = self.client.delete(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
