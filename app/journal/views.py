"""
Definition of API endpoints for the journal API
"""
from typing import Any

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Entry,
)
from journal.serializers import (
    EntrySerializer,
)


class ManageJournalViewSet(viewsets.ModelViewSet):
    """Creates, reads, update & delete journal entries"""
    serializer_class = EntrySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> Any:
        return Entry.objects.filter(author=self.request.user)

    def perform_create(self, serializer) -> Any | None:
        serializer.save(author=self.request.user)
        return None
