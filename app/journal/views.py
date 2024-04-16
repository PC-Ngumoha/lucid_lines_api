"""
Definition of API endpoints for the journal API
"""
from typing import Any

from rest_framework import (
    viewsets,
    generics,
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import (
    Entry,
    Tag,
)
from journal.serializers import (
    EntrySerializer,
    EntryImageSerializer,
    TagSerializer,
)


class ManageJournalViewSet(viewsets.ModelViewSet):
    """Creates, reads, update & delete journal entries"""
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> Any:
        return self.queryset.filter(author=self.request.user) or []

    def get_serializer_class(self) -> Any:
        serializer_class = self.serializer_class

        if self.action == 'upload_image':
            serializer_class = EntryImageSerializer

        return serializer_class

    def perform_create(self, serializer) -> Any | None:
        serializer.save(author=self.request.user)
        return None

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        entry = self.get_object()
        serializer = self.get_serializer(entry, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagListView(generics.ListAPIView):
    """List all tags that are available in the API"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
