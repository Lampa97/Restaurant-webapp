from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Table(models.Model):
    TWO = 2
    FOUR = 4
    SIX = 6
    EIGHT = 8
    TEN = 10

    CAPACITY_CHOICES = [(TWO, 2), (FOUR, 4), (SIX, 6), (EIGHT, 8), (TEN, 10)]

    number = models.SmallIntegerField(
        unique=True, verbose_name="Table Number", validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    capacity = models.SmallIntegerField(verbose_name="Capacity", choices=CAPACITY_CHOICES)
    is_reserved = models.BooleanField(default=False, verbose_name="Is Reserved")

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = ["number"]
        permissions = [
            ("can_admin_website", "Can administer the website"),
        ]

    def __str__(self):
        return f"Table {self.number} - Capacity: {self.capacity} Persons"


class Reservation(models.Model):

    TOTAL_PERSONS_CHOICES = [(i, i) for i in range(1, 11)]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations", verbose_name="Table")
    date = models.DateField(verbose_name="Reservation Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name="reservations",
        verbose_name="User",
    )
    user_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="User Name")
    user_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="User Phone")
    total_persons = models.PositiveIntegerField(
        verbose_name="Total Persons",
        choices=TOTAL_PERSONS_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ["date", "start_time"]
        permissions = [
            ("can_admin_website", "Can administer the website"),
        ]

    def __str__(self):
        return f"Reservation for {self.user} on {self.date} at {self.start_time}"
