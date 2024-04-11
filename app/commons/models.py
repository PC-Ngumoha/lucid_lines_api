from django.db import models


class Commons(models.Model):
    """Abstract base model class containing common DB fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
