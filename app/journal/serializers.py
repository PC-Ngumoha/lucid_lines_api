"""
Definition of Serializers useful for the Journal API.
"""
from rest_framework import serializers

from core.models import (
    Entry,
)


class EntrySerializer(serializers.ModelSerializer):
    """Serialize & Deserialize journal entries"""

    class Meta:
        model = Entry
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            }
        }
