from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_phone_number


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Phone number",
        validators=[validate_phone_number],
    )
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Full name")
    had_booked = models.BooleanField(default=False, verbose_name="Had booked")
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Token")
    password_reset_token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Reset_Token")


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            "full_name",
        ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} - {self.email}"
