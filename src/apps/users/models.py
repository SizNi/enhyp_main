from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from apps.users.manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    # password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=20, blank=True, null=True)
    confirmation_code_dt = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_staff(self):
        return self.is_superuser

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"
