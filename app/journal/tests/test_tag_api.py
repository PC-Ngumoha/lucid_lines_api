"""
Tests to simulate requests to the Tag Listing API
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from journal.serializers import TagSerializer


TAG_URL = reverse('journal:tags')


def create_tag(**params):
    """Creating tags for testing purposes"""
    payload = {'name': 'tag name'}
    payload.update(params)
    return Tag.objects.create(**payload)


class PublicTagAPITests(TestCase):
    """Public unauthenticated tests for the Tags API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_all_tags(self) -> None:
        """Tests listing all tags in the API."""
        tag_names = ('Bumblebee', 'Lisinum', 'Lucifer', 'Islam')
        for tag_name in tag_names:
            create_tag(name=tag_name)

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(len(serializer.data), len(tag_names))
        self.assertEqual(res.data, serializer.data)
