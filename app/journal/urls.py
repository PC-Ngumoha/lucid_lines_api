"""
URL config for the journal API endpoints
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from journal import views

app_name = 'journal'
router = DefaultRouter()
router.register('journal', views.ManageJournalViewSet, basename='journal')

urlpatterns = [
  path('', include(router.urls)),
]
