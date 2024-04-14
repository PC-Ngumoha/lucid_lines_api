"""
Tests to simulate requests made to the journal API.
"""
from typing import (
    Any,
)

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Entry,
)
from journal.serializers import (
    EntrySerializer,
)

User = get_user_model()
JOURNAL_URL = reverse('journal:journal-list')


def detail_url(entry_id: int) -> str:
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


def create_entry(user: Any, **params) -> Any:
    """Creates entries for testing purposes."""
    payload = {
        'title': 'Test title',
        'content': 'Test content',
    }
    payload.update(params)
    return Entry.objects.create(author=user, **payload)


class PrivateJournalAPITests(TestCase):
    """Private tests for authenticated requests to the journal API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_create_entry_successfully(self) -> None:
        """Tests we can create entry."""
        payload = {
            'title': 'Test title',
            'content': 'Test content',
        }
        res = self.client.post(JOURNAL_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        entry = Entry.objects.all()[0]
        self.assertIsNotNone(entry)

    def test_list_entries_successfully(self) -> None:
        """Tests we can list all entries belonging to current user."""
        titles = ('Test #1', 'Test #2', 'Test #3')
        for title in titles:
            create_entry(user=self.user, title=title)
        res = self.client.get(JOURNAL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        entries = Entry.objects.filter(author=self.user)
        serializer = EntrySerializer(entries, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_entry_successfully(self) -> None:
        """Tests that we can retrieve an entry."""
        entry = create_entry(user=self.user, title='Retrieve me')
        url = detail_url(entry.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = EntrySerializer(entry)
        self.assertEqual(res.data, serializer.data)

    def test_update_entry_successfully(self) -> None:
        """Tests that we can update an entry."""
        entry = create_entry(user=self.user, title='Update me')
        url = detail_url(entry.id)
        payload = {'title': 'Updated'}
        res = self.client.patch(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        entry.refresh_from_db()
        self.assertEqual(entry.title, payload.get('title'))

    def test_delete_entry_successfully(self) -> None:
        """Tests that we can delete an entry."""
        entry = create_entry(user=self.user, title='Delete me')
        url = detail_url(entry.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Entry.DoesNotExist):
            entry.refresh_from_db()

    def test_create_entry_with_tags(self) -> None:
        """Tests that we can create entries along with their tags specified.
        """
        payload = {
            'title': 'Test title',
            'content': 'Test content',
            'tags': [{'name': 'DailyJournal'},
                     {'name': 'Prompt'},
                     {'name': 'Goosebumps'}],
        }
        res = self.client.post(JOURNAL_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        entry = Entry.objects.filter(author=self.user,
                                     title=payload.get('title')).first()
        serializer = EntrySerializer(entry)
        self.assertIn('tags', serializer.data)
        tags = serializer.data.get('tags')
        payload_tags = payload.get('tags')
        for tag, p_tag in zip(tags, payload_tags):
            self.assertEqual(tag['name'], p_tag['name'])

    def test_update_tags_on_entry(self) -> None:
        """Tests that we can update the list of tags through the entry
        API."""
        payload = {
            'title': 'Test title',
            'content': 'Test content',
            'tags': [{'name': 'DailyJournal'},
                     {'name': 'Prompt'},
                     {'name': 'Goosebumps'}],
        }
        self.client.post(JOURNAL_URL, data=payload)
        entry = Entry.objects.filter(author=self.user,
                                     title=payload.get('title')).first()
        update = {
            'title': 'Test title',
            'content': 'Test content',
            'tags': [{'name': 'DailyJournal'},
                     {'name': 'Goosebumps'},
                     {'name': 'Spinal'}],
        }
        url = detail_url(entry.id)
        res = self.client.put(url, data=update)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        entry.refresh_from_db()
        serializer = EntrySerializer(entry)
        self.assertIn('tags', serializer.data)
        tags = serializer.data.get('tags')
        payload_tags = update.get('tags')
        for tag, p_tag in zip(tags, payload_tags):
            self.assertEqual(tag['name'], p_tag['name'])
