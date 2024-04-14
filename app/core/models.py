"""
Definition of all the DB models that are important for this app to function.
"""
from datetime import date
from typing import Any

from django.contrib.auth.models import (
  AbstractBaseUser,
  PermissionsMixin,
  BaseUserManager,
)
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from commons.models import Commons


class CustomUserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email: str, password: str | None = None,
                    **extras: Any) -> Any:
        """Create normal users"""
        if not email:
            raise ValueError(_('email field is REQUIRED'))

        user = self.model(
            email=self.normalize_email(email),
            **extras
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str,
                         **extras: Any) -> Any:
        """Create super users"""
        user = self.create_user(email, password, **extras)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, Commons):
    """Custom user model"""
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self) -> str:
        """String representation"""
        return self.email


class Tag(models.Model):
    """Tags to provide more context for each entry"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        """prints/returns tag_name"""
        return self.name


class Entry(Commons):
    """Journal entries DB model"""
    title = models.CharField(max_length=255,
                             default=date.today().strftime('%d %B, %Y'))
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries',
    )
    tags = models.ManyToManyField(Tag, related_name='entries', default=[])

    def __str__(self) -> str:
        """String representation"""
        return f'{self.created_at}: {self.title}'
