"""
Definition of serializers for the user API endpoints
"""
from typing import Any

from django.contrib.auth import (get_user_model, authenticate)
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


User = get_user_model()


class AuthSerializer(serializers.Serializer):
    """Serializes and Deserializes data for other CRUD operations on user
    API"""
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False,
                                     style={'input_type': 'password'})

    def validate(self, attrs: Any) -> Any:
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            message = _('Unable to authenticate with credentials provided.')
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializes and Deserializer data for user creation API."""

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
            },
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            }
        }

    def create(self, validated_data: Any) -> Any:
        return User.objects.create_user(**validated_data)
