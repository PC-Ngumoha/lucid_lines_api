"""
Definition of Serializers useful for the Journal API.
"""
from rest_framework import serializers


class EntrySerializer(serializers.ModelSerializer):
    """Serialize & Deserialize journal entries"""
    pass
