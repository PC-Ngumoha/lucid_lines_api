"""
Definitions of the API endpoint view logic for the user API.
"""
from typing import Any

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings

from user import serializers

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Handles creation of new users"""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserLoginView(ObtainAuthToken):
    """Handles login of existing users"""
    serializer_class = serializers.AuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieval, updation and deletion of currently authenticated
    user."""
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self) -> Any:
        return self.request.user
