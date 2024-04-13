"""
Tests to simulate requests made to the journal API.
"""
from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

User = get_user_model()
JOURNAL_URL = reverse('journal:journal-list')


def entry_detail_url(entry_id) -> str:
    """Returns the detailed URL"""
    return reverse('journal:journal-detail', args=[entry_id])


def create_user(**params) -> Any:
    """Creates users for testing purposes."""
    payload = {
        'email': 'test@example.com',
        'password': 'testing123#',
        'username': 'test_user',
    }
    payload.update(params)
    return User.objects.create_user(**payload)


class PrivateJournalAPITests(TestCase):
    """Private tests for authenticated requests to the journal API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)
