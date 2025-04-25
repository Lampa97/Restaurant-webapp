from django.core.exceptions import ValidationError
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

    number = models.SmallIntegerField(unique=True, verbose_name="Table Number")
    capacity = models.SmallIntegerField(
        verbose_name="Capacity", choices=CAPACITY_CHOICES
    )
    is_reserved = models.BooleanField(default=False, verbose_name="Is Reserved")

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} - Capacity: {self.capacity}"


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations", verbose_name="Table")
    date = models.DateField(verbose_name="Reservation Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations", verbose_name="Customer")
    total_persons = models.PositiveIntegerField(verbose_name="Total Persons", validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ["date", "start_time"]

    def clean(self):
        # Ensure total_persons does not exceed the table's capacity
        if self.total_persons > self.table.capacity:
            raise ValidationError(f"Total persons ({self.total_persons}) cannot exceed the table's capacity ({self.table.capacity}).")

    def __str__(self):
        return f"Reservation for {self.customer} on {self.date} at {self.start_time}"