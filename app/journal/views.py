"""
Definition of API endpoints for the journal API
"""
from typing import Any

from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Entry,
    Tag,
)
from journal.serializers import (
    EntrySerializer,
    TagSerializer,
)


class ManageJournalViewSet(viewsets.ModelViewSet):
    """Creates, reads, update & delete journal entries"""
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> Any:
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer) -> Any | None:
        serializer.save(author=self.request.user)
        return None


class TagListView(generics.ListAPIView):
    """List all tags that are available in the API"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
