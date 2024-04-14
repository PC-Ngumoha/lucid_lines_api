"""
Definition of Serializers useful for the Journal API.
"""
from typing import Any

from rest_framework import serializers

from core.models import (
    Entry,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serialize & Deserialize entry tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
        }


class EntrySerializer(serializers.ModelSerializer):
    """Serialize & Deserialize journal entries"""
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Entry
        fields = ['id', 'title', 'content', 'tags',
                  'created_at', 'updated_at']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            }
        }

    def _add_tags_to_entry(self, tags_list: list, instance: Any) -> Any:
        """Handles adding tags to entry object"""
        for tag_info in tags_list:
            tag, _ = Tag.objects.get_or_create(**tag_info)
            instance.tags.add(tag)

    def create(self, validated_data: Any) -> Any:
        tags_list = validated_data.pop('tags', [])

        instance = Entry.objects.create(**validated_data)
        self._add_tags_to_entry(tags_list, instance)

        return instance

    def update(self, instance: Any, validated_data: Any) -> Any:
        tags_list = validated_data.pop('tags', None)

        if tags_list is not None:
            instance.tags.clear()
            self._add_tags_to_entry(tags_list, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
