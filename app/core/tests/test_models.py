"""
Tests for the DB models created in the app.
"""
from datetime import date
from parameterized import parameterized
from typing import Any

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from core.models import (
    Entry,
    Tag,
)

User = get_user_model()


def create_user(**params) -> Any:
    """Creates User objects for testing purposes."""
    payload = {
        'email': 'test@example.com',
        'password': 'testing123#',
        'username': 'tester'
    }
    payload.update(params)
    return User.objects.create(**payload)


def create_entry(user: Any, **params) -> Any:
    """Creates Entry objects for testing purposes."""
    payload = {
        'title': 'An entry',
        'content': 'Entry content',
    }
    payload.update(params)
    return Entry.objects.create(author=user, **payload)


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

    def test_create_entry_successfully(self) -> None:
        """Tests that we can create a new entry."""
        payload = {
            'title': 'A new entry',
            'content': 'This is a new entry aimed at testing this model.',
        }
        user = create_user()
        entry = create_entry(user=user, **payload)

        self.assertIsNotNone(entry)

    def test_when_entry_title_supplied_use_title(self) -> None:
        """Tests that when title is supplied, we use title."""
        payload = {
            'title': 'A new entry',
            'content': 'This is a new entry aimed at testing this model.',
        }
        user = create_user()
        entry = Entry.objects.create(author=user, **payload)

        self.assertEqual(entry.title, payload.get('title'))

    def test_when_entry_title_not_supplied_use_date_today(self) -> None:
        """Tests that when title is not supplied, use today's date."""
        payload = {
            'content': 'This is a new entry aimed at testing this model.',
        }
        user = create_user()
        entry = Entry.objects.create(author=user, **payload)
        date_today = date.today().strftime('%d %B, %Y')

        self.assertEqual(entry.title, date_today)

    def test_datetime_fields_set_on_creation(self) -> None:
        """Tests that the 'created_at' & 'updated_at' fields are set
        on creation of model instance.
        """
        payload = {
            'content': 'This is a new entry aimed at testing this model.',
        }
        user = create_user()
        entry = create_entry(user=user, **payload)

        self.assertIsNotNone(entry.created_at)
        self.assertIsNotNone(entry.updated_at)

    def test_create_tags_in_DB(self) -> None:
        """Tests that we can create tags successfully."""
        tag_names = ('Picnic', 'Sunday vibes', 'happiness', 'at_peace')
        for tag_name in tag_names:
            Tag.objects.create(name=tag_name)

        tags = Tag.objects.all()
        self.assertEqual(tags.count(), len(tag_names))
        self.assertEqual(tags[0].name, tag_names[0])

    def test_tags_must_be_unique(self) -> None:
        """Tests that all Tag objects must be unique"""
        Tag.objects.create(name='A Tag')

        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='A Tag')

    def test_entry_can_have_many_tags(self) -> None:
        """Tests that all entry objects must have many tags.
        """
        user = create_user()
        entry = create_entry(user=user)

        tag_names = ('Picnic', 'Sunday vibes', 'happiness', 'at_peace')
        for tag_name in tag_names:
            tag = Tag.objects.create(name=tag_name)
            entry.tags.add(tag)

        self.assertEqual(entry.tags.count(), len(tag_names))

    def test_tag_can_have_many_entries(self) -> None:
        """Tests that all tag objects can have many entries.
        """
        user = create_user()
        tag = Tag.objects.create(name='Test')

        entry_titles = ('Entry #1', 'Entry #1', 'Entry #1', 'Entry #1')
        for entry_title in entry_titles:
            entry = create_entry(user=user, title=entry_title)
            entry.tags.add(tag)

        self.assertEqual(tag.entries.count(), len(entry_titles))
